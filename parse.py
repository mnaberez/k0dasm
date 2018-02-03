import re
from collections import defaultdict

ALIASES = {
    'regpair': ('AX', 'BC', 'DE', 'HL'),
    'regbank': ('RB0', 'RB1', 'RB2', 'RB3'),
    'reg': ('X', 'A', 'C', 'B', 'E', 'D', 'L', 'H'),
    'bit': ('0', '1', '2', '3', '4', '5', '6', '7'),
    }

BINARY_KEYS = {
    'r': 'reg',
    'p': 'regpair',
    'n': 'regbank',
    'f': 'addr11',
    't': 'addr5',
    'b': 'bit',
    }

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
        inst = {'desc': desc}
        opcodes[int(byte0, 2)].append(inst)
    else:
        nondigits = set()
        nondigit_indexes = []
        for i, c in enumerate(byte0):
            if c not in ('0', '1'):
                nondigits.add(c)
                nondigit_indexes.append(i)

        assert len(nondigits) in (0, 1)
        if len(nondigits):
            template_key = BINARY_KEYS[list(nondigits)[0]]
            #print(template_key)

        count = len(nondigit_indexes)
        for i in range(2 ** count):
            inst = {'desc': desc}
            inst[template_key] = i

            if template_key in ALIASES:
                inst[template_key] = ALIASES[template_key][i]

            binstr = bin(i)[2:].rjust(count, '0')
            assert len(binstr) == count

            byte0list = list(byte0)
            for j, c in enumerate(list(binstr)):
                byte0list[ nondigit_indexes[j] ] = c
            expandedbyte0 = ''.join(byte0list)

            x = int(expandedbyte0, 2)
            opcodes[x].append(inst)


for opcode in range(0x100):
    if opcode not in opcodes:
        print('0x%02x: ILLEGAL' % opcode)
    else:
        instructions = opcodes[opcode]
        for inst in instructions:
            desc = inst['desc']
            for templatekey in [ k for k in inst.keys() if k != 'desc' ]:
                template = ('{%s}' % templatekey)
                if template in desc:
                    desc = desc.replace(template, str(inst[templatekey]))
                inst['expanded_desc'] = desc
            # print('0x%02x: %s' % (opcode, inst.get('expanded_desc', inst['desc'])))
        if len(instructions) == 1:
            print('0x%02x: %r' % (opcode, instructions[0].get('expanded_desc', instructions[0]['desc'])  ))
