import struct

from k0dasm.utils import intel_byte, intel_word


class Printer(object):
    def __init__(self, memory, start_address, end_address, symbol_table):
        self.memory = memory
        self.start_address = start_address
        self.end_address = end_address
        self.symbol_table = symbol_table
        self.last_line_type = None

    def print_listing(self):
        self.print_header()
        self.print_symbols()

        address = self.start_address
        while address <= self.end_address:
            self.print_blank(address)
            self.print_label(address)

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
        self.print_footer()

    def print_header(self):
        print('    org 0%04xh\n' % self.start_address)

    def print_footer(self):
        print('    end')

    def print_symbols(self):
        symbol_addresses = set(self.symbol_table.symbols.values())
        used_addresses = set()

        for address, inst in self.memory.iter_instructions():
            if inst.target_address in symbol_addresses:
                used_addresses.add(inst.target_address)
            # TODO actually compute used symbols

        for address, target in self.memory.iter_vectors():
            if target in self.symbol_table.symbols:
                used_addresses.add(target)

        for address in sorted(used_addresses):
            if address > self.end_address:
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
        symbol = self.symbol_table.symbols.get(address)
        if symbol is None:
            return

        # special case to hide unnecessary labels for vectors
        if self.memory.is_vector_start(address):
            jumped = self.memory.is_jump_target(address)
            called = self.memory.is_call_target(address)
            if not jumped or called: # XXX may also be read as data
                return

        name, desc = symbol
        print("\n%s:" % name)

    def print_data_line(self, address):
        line = ('    db %s' % intel_byte(self.memory[address])).ljust(28)
        line += ';%04x  %02x          DATA %s ' % (address, self.memory[address], self._data_byte_repr(self.memory[address]))
        if self.memory.is_illegal_instruction(address):
            line += ' ILLEGAL_INSTRUCTION'
        print(line)

    def _data_byte_repr(self, b):
        if (b >= 0x20) and (b <= 0x7e):  # printable 7-bit ascii
            return "0x%02x '%s'" % (b, chr(b))
        else:
            return "0x%02x" % b

    def print_vector_line(self, address):
        target = struct.unpack('<H', self.memory[address:address+2])[0]
        target = self.format_ext_address(target)
        line = ('    dw %s' % target).ljust(28)
        line += ';%04x  %02x %02x       VECTOR' % (address, self.memory[address], self.memory[address+1])
        name, comment = self.symbol_table.symbols.get(address, ('',''))
        if comment:
            line += ' ' + comment
        print(line)

    def print_instruction_line(self, address, inst):
        # TODO leftovers from f2mc8dasm
        # if inst.stores_immediate_word_in_pointer:
        #     if inst.immediate in self.symbol_table.symbols:
        #         name, comment = self.symbol_table.symbols[inst.immediate]
        #         inst.disasm_template = inst.disasm_template.replace("IMW", name)
        # if inst.stores_immediate_word_in_a:
        #     if inst.immediate in self.symbol_table.symbols and (inst.immediate >= self.start_address):
        #         name, comment = self.symbol_table.symbols[inst.immediate]
        #         inst.disasm_template = inst.disasm_template.replace("IMW", name)

        disasm = self.format_instruction(inst)
        hexdump = (' '.join([ '%02x' % h for h in inst.all_bytes ])).ljust(8)

        # TODO handle amgibuous reassembly
        # TODO handle relative branch to address without a symbol

        line = '    ' + disasm.ljust(24)
        if not line.endswith(' '):
            line += ' '
        line += ';%04x  %s' % (address, hexdump)

        print(line)

    def format_instruction(self, inst):
        disasm = inst.template
        if inst.saddrp is not None:
            disasm = disasm.replace('{saddrp}', self.format_ext_address(inst.saddrp))
        if inst.saddr is not None:
            disasm = disasm.replace('{saddr}', self.format_ext_address(inst.saddr))
        if inst.reltarget is not None:
            disasm = disasm.replace('{reltarget}', '$' + self.format_ext_address(inst.reltarget))
        if inst.addr5 is not None:
            disasm = disasm.replace('{addr5}', '[%s]' % intel_word(inst.addr5))
        if inst.addr11 is not None:
            disasm = disasm.replace('{addr11}', '!' + self.format_ext_address(inst.addr11))
        if inst.addr16 is not None:
            disasm = disasm.replace('{addr16}', '!' + self.format_ext_address(inst.addr16))
        if inst.addr16p is not None:
            disasm = disasm.replace('{addr16p}', '!' + self.format_ext_address(inst.addr16p))
        if inst.offset is not None:
            disasm = disasm.replace('{offset}', intel_byte(inst.offset))
        if inst.bit is not None:
            disasm = disasm.replace('{bit}', '%d' % inst.bit)
        if inst.imm8 is not None:
            disasm = disasm.replace('{imm8}', '#' + intel_byte(inst.imm8))
        if inst.imm16 is not None:
            disasm = disasm.replace('{imm16}', '#' + self.format_imm16(inst.imm16))
        if inst.reg is not None:
            disasm = disasm.replace('{reg}', inst.reg)
        if inst.regpair is not None:
            disasm = disasm.replace('{regpair}', inst.regpair)
        if inst.sfr is not None:
            disasm = disasm.replace('{sfr}', self.format_ext_address(inst.sfr))
        if inst.sfrp is not None:
            disasm = disasm.replace('{sfrp}', self.format_ext_address(inst.sfrp))
        return disasm

    def format_imm16(self, imm16):
        if imm16 in self.symbol_table.symbols:
            name, comment = self.symbol_table.symbols[imm16]
            return name
        return intel_word(imm16)

    def format_ext_address(self, address):
        if address in self.symbol_table.symbols:
            name, comment = self.symbol_table.symbols[address]
            return name
        return intel_word(address)
