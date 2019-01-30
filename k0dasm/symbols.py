
class SymbolTable(object):
    def __init__(self, initial_symbols=None):
        if initial_symbols is None:
            initial_symbols = {}
        self.symbols = initial_symbols.copy()

    def generate(self, memory, start_address):
        self.generate_code_symbols(memory, start_address)
        self.generate_data_symbols(memory, start_address)

    def generate_code_symbols(self, memory, start_address):
        for address in range(start_address, len(memory)):
            if memory.is_call_target(address):
                if memory.is_instruction_start(address):
                    self.symbols[address] = ('sub_%04x' % address, '')
            elif memory.is_jump_target(address) or memory.is_entry_point(address):
                if memory.is_instruction_start(address):
                    self.symbols[address] = ('lab_%04x' % address, '')
        # XXX do not overwrite

    def generate_data_symbols(self, memory, start_address):
        data_addresses = set()
        modes_always_data = ('saddrp', 'saddr', 'addrp16', 'sfr', 'sfrp',)
        modes_sometimes_data = ('addr16', )
        # never data: addr16
        # todo: imm16

        for _, inst in memory.iter_instructions():
            for mode in modes_always_data:
                address = getattr(inst, mode, None)
                if address is not None:
                    data_addresses.add(address)

            for mode in modes_sometimes_data:
                address = getattr(inst, mode, None)
                if address is not None:
                    jumped = memory.is_jump_target(address)
                    called = memory.is_call_target(address)
                    if (not jumped) and (not called):
                        data_addresses.add(address)

        for address in data_addresses:
            if address not in self.symbols:
                self.symbols[address] = ('mem_%04x' % address, '')


NEC78K0_COMMON_SYMBOLS = {}
for i, address in enumerate(range(0x40, 0x7f, 2)):
    NEC78K0_COMMON_SYMBOLS[address] = ("callt_%d_vect" % i, "CALLT #%d" % i)

D78F0831Y_SYMBOLS = NEC78K0_COMMON_SYMBOLS.copy()
D78F0831Y_SYMBOLS.update(
{
    # hardware vectors
    0x0000: ("rst_vect", "RST"),
    0x0002: ("unused0_vect", "(unused)"),
    0x0004: ("intwdt_vect", "INTWDT"),
    0x0006: ("intp0_vect", "INTP0"),
    0x0008: ("intp1_vect", "INTP1"),
    0x000a: ("intp2_vect", "INTP2"),
    0x000c: ("intp3_vect", "INTP3"),
    0x000e: ("intp4_vect", "INTP4"),
    0x0010: ("intp5_vect", "INTP5"),
    0x0012: ("intp6_vect", "INTP6"),
    0x0014: ("intp7_vect", "INTP7"),
    0x0016: ("intser0_vect", "INTSER0"),
    0x0018: ("intsr0_vect", "INTSR0"),
    0x001a: ("intst0_vect", "INTST0"),
    0x001c: ("intcsi30_vect", "INTCSI30"),
    0x001e: ("intcsi31_vect", "INTCSI31"),
    0x0020: ("intiic0_vect", "INTIIC0"),
    0x0022: ("intc2_vect", "INTC2"),
    0x0024: ("intwtni0_vect", "INTWTNI0"),
    0x0026: ("inttm000_vect", "INTTM000"),
    0x0028: ("inttm010_vect", "INTTM010"),
    0x002a: ("inttm001_vect", "INTTM001"),
    0x002c: ("inttm011_vect", "INTTM011"),
    0x002e: ("intad00_vect", "INTAD00"),
    0x0030: ("intad01_vect", "INTAD01"),
    0x0032: ("unused1_vect", "(unused)"),
    0x0034: ("intwtn0_vect", "INTWTN0"),
    0x0036: ("intkr_vect", "INTKR"),
    0x0038: ("unused2_vect", "(unused)"),
    0x003a: ("unused3_vect", "(unused)"),
    0x003c: ("unused4_vect", "(unused)"),
    0x003e: ("brk_i_vect", "BRK_I"),
    # special function registers
    0xff00: ('p0', 'Port 0'),
    0xff02: ('p2', 'Port 2'),
    0xff03: ('p3', 'Port 3'),
    0xff04: ('p4', 'Port 4'),
    0xff05: ('p5', 'Port 5'),
    0xff06: ('p6', 'Port 6'),
    0xff07: ('p7', 'Port 7'),
    0xff08: ('p8', 'Port 8'),
    0xff09: ('p9', 'Port 9'),
    0xff0a: ('cr000', '16-bit timer capture/compare register 000'),
    0xff0c: ('cr010', '16-bit timer capture/compare register 010'),
    0xff0e: ('tm00', '16-bit timer counter 00'),
    0xff10: ('cr001', '16-bit timer capture/compare register 001'),
    0xff12: ('cr011', '16-bit timer capture/compare register 011'),
    0xff14: ('tm01', '16-bit timer counter 01'),
    0xff17: ('adcr00', 'A/D conversion result register 00'),
    0xff18: ('rxb0_txs0', 'Transmit shift register 0 / Receive buffer register 0'),
    0xff1a: ('sio30', 'Serial shift register 30'),
    0xff1b: ('sio31', 'Serial shift register 31'),
    0xff1f: ('iic0', 'IIC shift register 0'),
    0xff20: ('pm0', 'Port mode register 0'),
    0xff22: ('pm2', 'Port mode register 2'),
    0xff23: ('pm3', 'Port mode register 3'),
    0xff24: ('pm4', 'Port mode register 4'),
    0xff25: ('pm5', 'Port mode register 5'),
    0xff26: ('pm6', 'Port mode register 6'),
    0xff27: ('pm7', 'Port mode register 7'),
    0xff28: ('pm8', 'Port mode register 8'),
    0xff29: ('pm9', 'Port mode register 9'),
    0xff30: ('pu0', 'Pull-up resistor option register 0'),
    0xff32: ('pu2', 'Pull-up resistor option register 2'),
    0xff33: ('pu3', 'Pull-up resistor option register 3'),
    0xff34: ('pu4', 'Pull-up resistor option register 4'),
    0xff35: ('pu5', 'Pull-up resistor option register 5'),
    0xff36: ('pu6', 'Pull-up resistor option register 6'),
    0xff37: ('pu7', 'Pull-up resistor option register 7'),
    0xff40: ('cks', 'Clock output selection register'),
    0xff41: ('wtnm0', 'Watch timer mode control register 0'),
    0xff42: ('wdcs', 'Watchdog timer clock selection register'),
    0xff47: ('mem', 'Memory expansion mode register'),
    0xff48: ('egp', 'External interrupt rising edge enable register'),
    0xff49: ('egn', 'External interrupt falling edge enable register'),
    0xff4a: ('flapl', 'XXX Undocumented in 78F0833Y Subseries Manual'),
    0xff4b: ('flaph', 'XXX Undocumented in 78F0833Y Subseries Manual'),
    0xff4c: ('flmc',  'XXX Undocumented in 78F0833Y Subseries Manual'),
    0xff4d: ('flrb',  'XXX Undocumented in 78F0833Y Subseries Manual'),
    0xff4e: ('flwb',  'XXX Undocumented in 78F0833Y Subseries Manual'),
    0xff4f: ('fltsl', 'XXX Undocumented in 78F0833Y Subseries Manual'),
    0xff60: ('tmc00', '16-bit timer mode control register 00'),
    0xff61: ('prm00', 'Prescaler mode register 00'),
    0xff62: ('crc00', 'Capture/compare control register 00'),
    0xff63: ('toc00', '16-bit timer output control register 00'),
    0xff68: ('tmc01', '16-bit timer mode control register 01'),
    0xff69: ('prm01', 'Prescaler mode register 01'),
    0xff6a: ('crc01', 'Capture/compare control register 01'),
    0xff6b: ('toc01', '16-bit timer output control register 01'),
    0xff80: ('adm00', 'A/D converter mode register 00'),
    0xff81: ('ads00', 'Analog input channel specification register 00'),
    0xff88: ('adm01', 'A/D converter mode register 01'),
    0xff89: ('ads01', 'Analog input channel specification register 01'),
    0xff8b: ('adcr01', 'A/D conversion result register 01'),
    0xffa0: ('asim0', 'Asynchronous serial interface mode register 0'),
    0xffa1: ('asis0', 'Asynchronous serial interface status register 0'),
    0xffa2: ('brgc0', 'Baud rate generator control register 0'),
    0xffa8: ('iicc0', 'IIC control register 0'),
    0xffa9: ('iics0', 'IIC status register 0'),
    0xffaa: ('iiccl0', 'IIC transfer clock selection register 0'),
    0xffab: ('sva0', 'Slave address register 0'),
    0xffb0: ('csim30', 'Serial operation mode register 30'),
    0xffb8: ('csim31', 'Serial operation mode register 31'),
    0xffc0: ('c2ct1', 'Class 2 control register 1'),
    0xffc1: ('c2ct2', 'Class 2 control register 2'),
    0xffc2: ('c2st1', 'Class 2 status register 1'),
    0xffc3: ('c2st2', 'Class 2 status register 2'),
    0xffc4: ('c2txfifo', 'Class 2 transmit FIFO register'),
    0xffc5: ('c2pdf', 'Class 2 rise time propagation delay correction register'),
    0xffc6: ('c2pdf', 'Class 2 fall time propagation delay correction register'),
    0xffc7: ('c2clk', 'Class 2 clock selection register'),
    0xffd0: ('ffd0', 'FFD0 (External Access Area)'),
    0xffd1: ('ffd1', 'FFD1 (External Access Area'),
    0xffd2: ('ffd2', 'FFD2 (External Access Area'),
    0xffd3: ('ffd3', 'FFD3 (External Access Area'),
    0xffd4: ('ffd4', 'FFD4 (External Access Area'),
    0xffd5: ('ffd5', 'FFD5 (External Access Area'),
    0xffd6: ('ffd6', 'FFD6 (External Access Area'),
    0xffd7: ('ffd7', 'FFD7 (External Access Area'),
    0xffd8: ('ffd8', 'FFD8 (External Access Area'),
    0xffd9: ('ffd9', 'FFD9 (External Access Area'),
    0xffda: ('ffda', 'FFDA (External Access Area'),
    0xffdb: ('ffdb', 'FFDB (External Access Area'),
    0xffdc: ('ffdc', 'FFDC (External Access Area'),
    0xffdd: ('ffdd', 'FFDD (External Access Area'),
    0xffde: ('ffde', 'FFDE (External Access Area'),
    0xffdf: ('ffdf', 'FFDF (External Access Area'),
    0xffe0: ('if0l', 'Interrupt request flag register 0L'),
    0xffe1: ('if0h', 'Interrupt request flag register 0H'),
    0xffe2: ('if1l', 'Interrupt request flag register 1L'),
    0xffe3: ('if1h', 'Interrupt request flag register 1H'),
    0xffe4: ('mk0l', 'Interrupt mask flag register 0L'),
    0xffe5: ('mk0h', 'Interrupt mask flag register 0H'),
    0xffe6: ('mk1l', 'Interrupt mask flag register 1L'),
    0xffe7: ('mk1h', 'Internal mask flag register 1H'),
    0xffe8: ('pr0l', 'Priority level specification flag register 0L'),
    0xffe9: ('pr0h', 'Priority level specification flag register 0H'),
    0xffea: ('pr1l', 'Priority level specification flag register 1L'),
    0xffeb: ('pr1h', 'Priority level specification flag register 1H'),
    0xfff0: ('ims', 'Memory size switching register'),
    0xfff2: ('clkm', 'XXX Undocumented in 78F0833Y Subseries Manual'),
    0xfff4: ('ixs', 'Internal expansion RAM size switching register'),
    0xfff8: ('mm', 'XXX Undocumented in 78F0833Y Subseries Manual'),
    0xfff9: ('wdtm', 'Watchdog timer mode register'),
    0xfffa: ('osts', 'Oscillation stabilization time selection register'),
    0xfffb: ('pcc', 'Processor clock control register'),
})
