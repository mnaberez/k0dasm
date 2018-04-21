import sys

from k0dasm.disassemble import disassemble, IllegalInstructionError

def main():
    with open(sys.argv[1], 'rb') as f:
        rom = bytearray(f.read())

    pc = rom[0] + (rom[1] << 8) # reset vector

    print("    org 0%04xh" % pc)
    while pc < len(rom):
        try:
            disasm = disassemble(rom[pc:], pc)
            new_pc = pc + len(disasm)
            illegal = False
        except IllegalInstructionError as e:
            disasm = "db 0%02xh ;illegal" % rom[pc]
            new_pc = pc + 1
            illegal = True

        length = new_pc - pc
        instdata = rom[pc:pc+length]

        if not illegal: # if illegal, instdata will only one byte
            if (instdata[0] == 0x03) and (instdata[2] == 0xff):
                disasm = "db 0%02xh, 0%02xh, 0%02xh ;ambiguous %s" % (
                    instdata[0], instdata[1], instdata[2], disasm)

        inst = ' '.join(['%02x' % x for x in instdata])
        print("    %s ;%04x %s" % (str(disasm).ljust(22), pc, inst))
        pc = new_pc
    print("    end")
