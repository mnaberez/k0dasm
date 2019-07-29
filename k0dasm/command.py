'''
Usage: k0dasm <filename.bin>

'''

import sys

from k0dasm.disassemble import disassemble
from k0dasm.memory import Memory
from k0dasm.trace import Tracer
from k0dasm.listing import Printer
from k0dasm.symbols import SymbolTable, D78F0831Y_SYMBOLS

def main():
    if len(sys.argv) != 2:
        sys.stderr.write(__doc__)
        sys.exit(1)

    with open(sys.argv[1], 'rb') as f:
        rom = bytearray(f.read())
    memory = Memory(rom)

    start_address = 0
    entry_points = []
    hardware_vectors = [ # TODO these are uPD78F0831Y specific
        0x0000, # RST
        0x0002, # (unused)
        0x0004, # INTWDT
        0x0004, # INTWDT
        0x0006, # INTP0
        0x0008, # INTP1
        0x000a, # INTP2
        0x000c, # INTP3
        0x000e, # INTP4
        0x0010, # INTP5
        0x0012, # INTP6
        0x0014, # INTP7
        0x0016, # INTSER0
        0x0018, # INTSR0
        0x001a, # INTST0
        0x001c, # INTCSI30
        0x001e, # INTCSI31
        0x0020, # INTIIC0
        0x0022, # INTC2
        0x0024, # INTWTNI0
        0x0026, # INTTM000
        0x0028, # INTTM010
        0x002a, # INTTM001
        0x002c, # INTTM011
        0x002e, # INTAD00
        0x0030, # INTAD01
        0x0032, # (unused)
        0x0034, # INTWTN0
        0x0036, # INTKR
        0x0038, # (unused)
        0x003a, # (unused)
        0x003c, # (unused)
        0x003e,  # BRK_I
    ]
    callt_vectors = list(range(0x40, 0x7f, 2))
    all_vectors = hardware_vectors + callt_vectors

    traceable_range = range(start_address, start_address + len(rom) + 1)
    tracer = Tracer(memory, entry_points, all_vectors, traceable_range)
    tracer.trace(disassemble)

    symbol_table = SymbolTable(D78F0831Y_SYMBOLS)
    symbol_table.generate(memory, start_address) # xxx should pass traceable_range

    printer = Printer(memory,
                      start_address,
                      traceable_range[-1] - 1,
                      symbol_table
                      )
    printer.print_listing()
