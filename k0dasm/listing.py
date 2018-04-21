import struct
from f2mc8dasm.tables import AddressModes

class Printer(object):
    def __init__(self, memory, start_address, symbol_table):
        self.memory = memory
        self.start_address = start_address
        self.symbol_table = symbol_table
        self.last_line_type = None

        class Foo:
            symbols = {}
        self.symbol_table = Foo


    def print_listing(self):
        #self.print_header()
        #self.print_symbols()

        address = self.start_address
        while address < len(self.memory):
            #self.print_blank(address)
            #self.print_label(address)

            if self.memory.is_instruction_start(address):
                inst = self.memory.get_instruction(address)
                self.print_instruction_line(address, inst)
                address += len(inst)
            else:
                if self.memory.is_vector_start(address):
                    self.print_vector_line(address)
                    address += 2
                elif self.memory.is_data(address):
                    self.print_data_line(address)
                    address += 1
                else:
                    msg = "Unhandled location type %r at 0x%04x" % (
                        self.memory.types[address], address)
                    raise NotImplementedError(msg) # always a bug

    def print_header(self):
        print('    .F2MC8L')
        print('    .area CODE1 (ABS)')
        print('    .org 0x%04x\n' % self.start_address)

    def print_symbols(self):
        return
        used_symbols = set()
        for address, inst in self.memory.iter_instructions():
            if inst.address in self.symbol_table.symbols:
                used_symbols.add(inst.address)
            if inst.bittest_address in self.symbol_table.symbols:
                used_symbols.add(inst.bittest_address)
            if inst.stores_immediate_word_in_pointer:
                if inst.immediate in self.symbol_table.symbols:
                    used_symbols.add(inst.immediate)

        for address, target in self.memory.iter_vectors():
            if target in self.symbol_table.symbols:
                used_symbols.add(target)

        for address in sorted(used_symbols):
            if address < self.start_address:
                name, comment = self.symbol_table.symbols[address]
                line = ("    %s = 0x%02x" % (name, address)).ljust(28)
                if comment:
                    line += ";%s" % comment
                print(line)
        print('')

    def print_blank(self, address):
        typ = self.memory.types[address]
        if self.last_line_type is not None:
            if typ != self.last_line_type:
                if address not in self.symbol_table.symbols:
                    print('')
        self.last_line_type = typ

    def print_label(self, address):
        if address in self.symbol_table.symbols:
            print("\n%s:" % self.format_ext_address(address))

    def print_data_line(self, address):
        line = ('    .byte 0x%02x' % self.memory[address]).ljust(28)
        line += ';%04x  %02x          DATA %s ' % (address, self.memory[address], self._data_byte_repr(self.memory[address]))
        print(line)

    def _data_byte_repr(self, b):
        if (b >= 0x20) and (b <= 0x7e):  # printable 7-bit ascii
            return "0x%02x '%s'" % (b, chr(b))
        else:
            return "0x%02x" % b

    def print_vector_line(self, address):
        target = struct.unpack('<H', self.memory[address:address+2])[0]
        target = self.format_ext_address(target)
        line = ('    .word %s' % target).ljust(28)
        line += ';%04x  %02x %02x       VECTOR' % (address, self.memory[address], self.memory[address+1])
        name, comment = self.symbol_table.symbols.get(address, ('',''))
        if comment:
            line += ' ' + comment
        print(line)

    def print_mode_byte_line(self, address):
        line = ('    .byte 0x%02X' % self.memory[address]).ljust(28)
        line += ';%04x  %02x          MODE' % (address, self.memory[address])
        print(line)

    def print_reserved_byte_line(self, address):
        line = ('    .byte 0x%02X' % self.memory[address]).ljust(28)
        line += ';%04x  %02x          RESERVED' % (address, self.memory[address])
        print(line)

    def print_instruction_line(self, address, inst):
        print("%04x: %s" % (address, inst)) # XXX hack
        return
        if inst.stores_immediate_word_in_pointer:
            if inst.immediate in self.symbol_table.symbols:
                name, comment = self.symbol_table.symbols[inst.immediate]
                inst.disasm_template = inst.disasm_template.replace("IMW", name)
        if inst.stores_immediate_word_in_a:
            if inst.immediate in self.symbol_table.symbols and (inst.immediate >= self.start_address):
                name, comment = self.symbol_table.symbols[inst.immediate]
                inst.disasm_template = inst.disasm_template.replace("IMW", name)

        disasm = self.format_instruction(inst)
        hexdump = (' '.join([ '%02x' % h for h in inst.all_bytes ])).ljust(8)

        # render instruction as a .byte sequence if asf2mc8 would optimize an
        # extended address into a direct one, breaking identical reassembly
        ext_page_0 = inst.extended_address_page_0

        # render instruction as .byte sequence if it is a relative branch
        # to an address that does not have a symbol
        rel = (inst.addr_mode in (AddressModes.Relative,
                                  AddressModes.BitDirectWithRelative))
        branch_without_symbol = (rel and ((inst.address not in self.symbol_table.symbols) or
                                    (inst.address < self.start_address)))

        if ext_page_0 or branch_without_symbol:
            if ext_page_0:
                note = "EXTENDED_ADDRESS_PAGE_0"
            else: # bad_branch
                note = "BRANCH_WITHOUT_SYMBOL"

            line = ('    .byte ' + ', '.join([ '0x%02x' % h for h in inst.all_bytes ])).ljust(28)
            line += (';%04x  %s    %s  ' % (address, hexdump, note)).ljust(19)
            line += disasm
        else:
            line = '    ' + disasm.ljust(24)
            if not line.endswith(' '):
                line += ' '
            line += ';%04x  %s' % (address, hexdump)

        if self.memory.is_branch_always_taken(address):
            line = line.ljust(47) + "BRANCH_ALWAYS_TAKEN"
        if self.memory.is_branch_never_taken(address):
            line = line.ljust(47) + "BRANCH_NEVER_TAKEN"
        if inst.addr_mode == AddressModes.Vector:
            dest = self.format_ext_address(inst.address)
            line = line.ljust(47) + "CALLV #%d = %s" % (inst.callv, dest)
        print(line)

    def format_instruction(self, inst):
        d = {'OPC': '0x%02x' % inst.opcode}

        if inst.immediate is not None:
            d['IMB'] = '0x%02x' % inst.immediate
            d['IMW'] = '0x%04x' % inst.immediate
        if inst.address is not None:
            d['EXT'] = self.format_ext_address(inst.address)
            d['REL'] = self.format_ext_address(inst.address)
            d['DIR'] = self.format_dir_address(inst.address)
        if inst.bittest_address is not None:
            d['DIR'] = self.format_ext_address(inst.bittest_address)
        if inst.ixd_offset is not None:
            d['IXD'] = '0x%02x' % inst.ixd_offset
        if inst.callv is not None:
            d['VEC'] = '%d' % inst.callv
        if inst.bit is not None:
            d['BIT'] = '%d' % inst.bit
        if inst.register is not None:
            d['REG'] = '%d' % inst.register

        disasm = inst.disasm_template
        for k, v in d.items():
            disasm = disasm.replace(k, v)
        return disasm

    def format_ext_address(self, address):
        if address in self.symbol_table.symbols:
            name, comment = self.symbol_table.symbols[address]
            return name
        return '0x%04x' % address

    def format_dir_address(self, address):
        if address in self.symbol_table.symbols:
            name, comment = self.symbol_table.symbols[address]
            return name
        return '0x%02x' % address
