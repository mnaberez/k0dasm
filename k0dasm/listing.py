import struct


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

    def print_header(self):
        print('    .area CODE1 (ABS)')
        print('    .org 0x%04x\n' % self.start_address)

    def print_symbols(self):
        symbol_addresses = set(self.symbol_table.symbols.keys())
        used_addresses = set()

        for _, inst in self.memory.iter_instructions():
            for address in inst.referenced_addresses:
                if address in symbol_addresses:
                    used_addresses.add(address)

        for _, target in self.memory.iter_vectors():
            if target in self.symbol_table.symbols:
                used_addresses.add(target)

        for address in sorted(used_addresses):
            if address > self.end_address:
                name, comment = self.symbol_table.symbols[address]
                line = ("    %s = 0x%04x" % (name, address)).ljust(28)
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
        if symbol is not None:
            name, desc = symbol
            print("\n%s:" % name)

    def print_data_line(self, address):
        line = ('    .byte 0x%02x' % self.memory[address]).ljust(28)
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
        target_address = struct.unpack('<H', self.memory[address:address+2])[0]

        if target_address in self.symbol_table.symbols:
            name, comment = self.symbol_table.symbols[target_address]
            target = name
        else:
            target = '0x%04x' % target_address

        line = ('    .word %s' % target).ljust(28)
        line += ';%04x  %02x %02x       VECTOR' % (address, self.memory[address], self.memory[address+1])
        name, comment = self.symbol_table.symbols.get(address, ('',''))
        if comment:
            line += ' ' + comment
        print(line)

    def print_instruction_line(self, address, inst):
        disasm = inst.to_string(symbols=self.symbol_table.symbols)
        hexdump = (' '.join([ '%02x' % h for h in inst.all_bytes ])).ljust(8)

        # TODO handle amgibuous reassembly
        # TODO handle relative branch to address without a symbol

        line = '    ' + disasm.ljust(24)
        if not line.endswith(' '):
            line += ' '
        line += ';%04x  %s' % (address, hexdump)

        print(line)
