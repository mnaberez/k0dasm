import sys
from k0dasm.disassemble import disassemble

def main():
    with open(sys.argv[1], 'rb') as f:
        data = bytearray(f.read())

    pc = data[0] + (data[1] << 8) # reset vector

    print("    org 0%04xh" % pc)
    while pc < len(data):
        disasm, new_pc = disassemble(data[pc:], pc)
        if hasattr(disasm, 'ljust'):
            raise Exception(hex(data[pc]))
        length = new_pc - pc
        inst = ' '.join(['%02x' % x for x in data[pc:pc+length]])
        print("    %s ;%04x %s" % (str(disasm).ljust(22), pc, inst))
        pc = new_pc
    print("    end")
