
class SymbolTable(object):
    def __init__(self, initial_symbols=None):
        if initial_symbols is None:
            initial_symbols = {}
        self.symbols = initial_symbols.copy()

    def generate(self, memory, start_address):
        self.generate_code_symbols(memory, start_address)

    def generate_code_symbols(self, memory, start_address):
        for address in range(start_address, len(memory)):
            if memory.is_call_target(address):
                if memory.is_instruction_start(address):
                    self.symbols[address] = ('sub_%04x' % address, '')
            elif memory.is_jump_target(address):
                if memory.is_instruction_start(address):
                    self.symbols[address] = ('lab_%04x' % address, '')

NEC78K0_COMMON_SYMBOLS = {}
for i, address in enumerate(range(0x40, 0x7f, 2)):
    NEC78K0_COMMON_SYMBOLS[address] = ("callt_%d_vect" % i, "CALLT #%d" % i)

D78F0831Y_SYMBOLS = NEC78K0_COMMON_SYMBOLS.copy()
D78F0831Y_SYMBOLS.update(
{
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
})
