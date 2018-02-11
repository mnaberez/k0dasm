import sys
from disassemble import disassemble

with open(sys.argv[1], 'rb') as f:
    data = bytearray(f.read())

pc = data[0] + (data[1] << 8) # reset vector

while pc < 0xf000:
    disasm, new_pc = disassemble(data[pc:], pc)
    length = new_pc - pc
    inst = (' '.join(['%02x' % x for x in data[pc:pc+length]])).ljust(12)
    print("%04x %s %s" % (pc, inst, disasm))
    pc = new_pc
