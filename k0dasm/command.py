import sys

from k0dasm.disassemble import disassemble
from k0dasm.memory import Memory
from k0dasm.trace import Tracer
from k0dasm.listing import Printer
from k0dasm.symbols import SymbolTable, D78F0831Y_SYMBOLS

def main():
    with open(sys.argv[1], 'rb') as f:
        rom = bytearray(f.read())


    memory = Memory(rom)

    start_address = 0
    entry_points = []

    hardware_vectors = [
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

    vectors = hardware_vectors + callt_vectors


    traceable_range = range(start_address, start_address + len(rom) + 1)
    tracer = Tracer(memory, entry_points, vectors, traceable_range)
    tracer.trace(disassemble)

    symbol_table = SymbolTable(D78F0831Y_SYMBOLS)
    symbol_table.generate(memory, start_address) # xxx should pass traceable_range

    printer = Printer(memory,
                      start_address,
                      traceable_range[-1] - 1,
                      symbol_table
                      )
    printer.print_listing()

    #   pc = rom[0] + (rom[1] << 8) # reset vector
    # print("    org 0%04xh" % pc)
    # while pc < len(rom):
    #     try:
    #         disasm = disassemble(rom[pc:], pc)
    #         new_pc = pc + len(disasm)
    #         illegal = False
    #     except IllegalInstructionError as e:
    #         disasm = "db 0%02xh ;illegal" % rom[pc]
    #         new_pc = pc + 1
    #         illegal = True
    #
    #     length = new_pc - pc
    #     instdata = rom[pc:pc+length]
    #
    #     if not illegal: # if illegal, instdata will only one byte
    #         if (instdata[0] == 0x03) and (instdata[2] == 0xff):
    #             disasm = "db 0%02xh, 0%02xh, 0%02xh ;ambiguous %s" % (
    #                 instdata[0], instdata[1], instdata[2], disasm)
    #
    #     inst = ' '.join(['%02x' % x for x in instdata])
    #     print("    %s ;%04x %s" % (str(disasm).ljust(22), pc, inst))
    #     pc = new_pc
    # print("    end")
