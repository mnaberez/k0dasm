'''
Parse NEC device file
'''

import struct
import sys

with open(sys.argv[1], 'rb') as f:
    f.seek(0x50)
    headers = {}
    for i in range(20):
        data = f.read(0x0c)
        name = data[0:2].decode('utf8')
        count = struct.unpack('<H', data[2:4])[0]
        start = struct.unpack('<H', data[4:6])[0]
        headers[name] = {'count': count, 'start': start}

    print("\n==== SPECIAL FUNCTION REGISTERS ====")
    f.seek(headers['SN']['start'])
    for i in range(headers['SN']['count']):
        data = bytearray(f.read(0x28))

        name = data[:10].replace(b'\0', b'').decode('utf-8')
        address = struct.unpack('<H', data[22:24])[0]
        datatype = data[22+4]

        typename = {0x01: 'BIT R',
                    0x02: 'BIT R/W',
                    0x03: 'BIT R/W',
                    0x10: 'BYTE R',
                    0x11: 'BYTE R',
                    0x20: 'BYTE W',
                    0x30: 'BYTE R/W',
                    0x33: 'BYTE R/W',
                    0x40: 'WORD R',
                    0xC0: 'WORD R/W',}[datatype]
        print("%04x: %s (%s)" % (address, name, typename))

    print("\n==== PINS ====")
    f.seek(headers['PI']['start'])
    for i in range(headers['PI']['count']):
        data = f.read(0x2c)
        datatype = bytearray(data)[-2]
        if datatype == 3:
            shortname = data[:8].replace(b'\0',b'')
            longname = data[8:30].replace(b'\0',b'')
            print(data)

    print("\n==== VECTORS ====")
    f.seek(headers['VN']['start'])
    for i in range(headers['VN']['count']):
        data = f.read(0x18)
        name = data[:10].replace(b'\0', b'').decode('utf-8')
        address = struct.unpack('<H', data[16:18])[0]
        print("%04x: %s" % (address, name))
