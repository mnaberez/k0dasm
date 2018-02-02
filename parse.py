import re
from collections import defaultdict

with open("opcodes.txt", "r") as f:
    lines = [l.strip() for l in f.readlines()[1:] if l.strip()]

opcodes = defaultdict(list)
for l in lines:
    cols = re.split('\s{2,}', l)

    # fix rows without second byte column
    if len(cols) != 4:
        cols.insert(2, '')

    # remove 0b prefixes from numbers
    for i in (1,2):
        if cols[i].startswith('0b'):
            cols[i] = cols[i][2:]
        if cols[i]:
            assert len(cols[i]) == 8

    desc, byte0, byte1, numbytes = cols
    needs_expansion = re.sub('\d', '', byte0)

    if not needs_expansion:
        opcodes[int(byte0, 2)].append(desc)
    else:
        nondigit_indexes = []
        for i, c in enumerate(byte0):
            if c not in ('0', '1'):
                nondigit_indexes.append(i)

        count = len(nondigit_indexes)
        for i in range(2 ** count):
            binstr = bin(i)[2:].rjust(count, '0')
            assert len(binstr) == count

            byte0list = list(byte0)
            for j, c in enumerate(list(binstr)):
                byte0list[ nondigit_indexes[j] ] = c
            expandedbyte0 = ''.join(byte0list)
            #print(expandedbyte0 + ': ' + desc)

            x = int(expandedbyte0, 2)
            s = desc.ljust(30) + '(expanded)'
            opcodes[x].append(s)

for k in sorted(opcodes.keys()):
    l = opcodes[k]
    print('0x%02x: %r' % (k, l))


