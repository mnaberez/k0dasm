
def disassemble(mem, pc):
    # nop                         ;00
    if mem[0] == 0x00:
        return ("NOP", pc+1)

    # not1 cy                     ;01
    elif mem[0] == 0x01:
        return ('NOT1 CY', pc+1)

    # movw ax,!0abceh             ;02 CE AB       saddrp TODO is this really saddrp?
    elif mem[0] == 0x02:
        saddrp = mem[1] + (mem[2] << 8)
        return ('MOVW AX,!0%04xH' % saddrp, pc+3)

    # MOVW !0abceh,AX             ;03 CE AB       saddrp TODO is this really saddrp?
    elif mem[0] == 0x03:
        saddrp = mem[1] + (mem[2] << 8)
        return ('MOVW !0%04xH,AX' % saddrp, pc+3)

    # DBNZ 0fe20h,$label0         ;04 20 FD       saddr
    elif mem[0] == 0x04:
        saddr = _saddr(mem[1])
        disp = mem[2]
        # TODO calculate pc from displacement
        return ('DBNZ 0%04xH,$disp=%02x' % (saddr, disp), pc+3)

    # XCH A,[DE]
    elif mem[0] == 0x05:
        return ("XCH A,[DE]", pc+1)

    # ILLEGAL
    elif mem[0] == 0x06:
        return ("ILLEGAL 0x06", pc+1)

    # 'XCH A,[HL]'
    elif mem[0] == 0x07:
        return ('XCH A,[HL]', pc+1)

    # ADD A,!0abcdh               ;08 CD AB
    elif mem[0] == 0x08:
        addr16 = mem[1] + (mem[2] << 8)
        return ("ADD A,!0%04xh" % addr16, pc+3)

    # ADD A,[HL+0abh]             ;09 AB
    elif mem[0] == 0x09:
        byte = mem[1]
        return ("ADD A,[HL+%02xH]" % byte, pc+2)

    # callt [0040H]               ;C1
    # CALLT [{addr5}]             0b11ttttt1                            1
    elif (mem[0] & 0b11000001) == 0b11000001:
        offset = (mem[0] & 0b00111110) >> 1
        addr5 = 0x40 + (offset * 2)
        return ("CALLT [%04xH]" % addr5, pc+1)

    # callf !0800h                ;0C 00          0c = callf 0800h-08ffh
    # CALLF !{addr11}             0b0xxx1100         0bffffffff         2
    elif (mem[0] & 0b10001111) == 0b00001100:
        base = 0x0800 + ((mem[0] >> 4) << 8)
        address = base + mem[1]
        return ("CALLF !%04xH" % address, pc+2)

    # 0x0d: 'ADD A,#byte'
    # ADD A,#0abh                 ;0D AB
    elif mem[0] == 0x0d:
        byte = mem[1]
        return ('ADD A,#0%02xH' % byte, pc+2)

    # 0x0e: 'ADD A,saddr'
    # ADD A,0fe20h                ;0E 20          saddr
    elif mem[0] == 0x0e:
        saddr = _saddr(mem[1])
        return ('ADD A,0%04xH' % saddr, pc+2)

    # 0x0f: 'ADD A,[HL]'
    # ADD A,[HL]                  ;0F
    elif mem[0] == 0x0f:
        return ('ADD A,[HL]', pc+1)

    # MOVW {regpair},#word        0b00010pp0                            3
    # MOVW AX,#0abcdh             ;10 CD AB
    # MOVW BC,#0abcdh             ;12 CD AB
    # MOVW DE,#0abcdh             ;14 CD AB
    # MOVW HL,#0abcdh             ;16 CD AB
    elif (mem[0] & 0b11111001) == 0b00010000:
        regpair = (mem[0] >> 1) & 0b11
        regpairname = _regpairname(regpair)
        imm16 = mem[1] + (mem[2] << 8)
        return ("MOVW %s,#0%04xH" % (regpairname, imm16), pc+3)

    # 0x15: ILLEGAL
    elif mem[0] == 0x15:
        return ("ILLEGAL 0x15", pc+1)

    # 0x17: ILLEGAL
    elif mem[0] == 0x17:
        return ("ILLEGAL 0x17", pc+1)

    elif mem[0] == 0x1f:
        return ('SUB A,[HL]', pc+1)

    # 0x20: 'SET1 CY'
    elif mem[0] == 0x20:
        return ('SET1 CY', pc+1)

    # 0x21: 'CLR1 CY'
    elif mem[0] == 0x21:
        return ('CLR1 CY', pc+1)

    # 0x22: 'PUSH PSW'
    elif mem[0] == 0x22:
        return ('PUSH PSW', pc+1)

    # 0x23: 'POP PSW'
    elif mem[0] == 0x23:
        return ('POP PSW', pc+1)

    # 0x24: 'ROR A,1'
    elif mem[0] == 0x24:
        return ('ROR A,1', pc+1)

    # 0x25: 'RORC A,1'
    elif mem[0] == 0x25:
        return ('RORC A,1', pc+1)

    # 0x26: 'ROL A,1'
    elif mem[0] == 0x26:
        return ('ROL A,1', pc+1)

    # 0x27: 'ROLC A,1'
    elif mem[0] == 0x27:
        return ('ROLC A,1', pc+1)

    # 0x27: 'ADDC A,[HL]'
    elif mem[0] == 0x2f:
        return ('ADDC A,[HL]', pc+1)

    # 0x30: 'XCH A,X' .. 0x37: 'XCH A,H'
    elif (mem[0] & 0b11111000) == 0b00110000:
        reg = mem[0] & 0b111
        regname = _regname(reg)
        return ("XCH A,%s" % regname, pc+1)

    # 0x3f: 'SUBC A,[HL]'
    elif mem[0] == 0x3f:
        return ('SUBC A,[HL]', pc+1)

    # 0x40: 'INC X' .. 0x47: 'INC H'
    elif (mem[0] & 0b11111000) == 0b01000000:
        reg = mem[0] & 0b111
        regname = _regname(reg)
        return ("INC %s" % regname, pc+1)

    # 0x4f: 'CMP A,[HL]'
    elif mem[0] == 0x4f:
        return ('CMP A,[HL]', pc+1)

    # 0x50: 'DEC X' .. 0x57: 'DEC H'
    elif (mem[0] & 0b11111000) == 0b01010000:
        reg = mem[0] & 0b111
        regname = _regname(reg)
        return ("DEC %s" % regname, pc+1)

    # 0x60: 'MOV A,X' .. 0x67: 'MOV A,H'
    elif (mem[0] & 0b11111000) == 0b01100000:
        reg = mem[0] & 0b111
        regname = _regname(reg)
        return ("MOV A,%s" % regname, pc+1)

    # 0x70: 'MOV X,A' .. 0x77: 'MOV H,A'
    elif (mem[0] & 0b11111000) == 0b01110000:
        reg = mem[0] & 0b111
        regname = _regname(reg)
        return ("MOV %s,A" % regname, pc+1)

    # 0x80, 0x82, 0x84, 0x86
    elif (mem[0] & 0b11111001) == 0b10000000:
        regpair = (mem[0] >> 1) & 0b11
        regpairname = _regpairname(regpair)
        return ("INCW %s" % regpairname, pc+1)

    # 0x81: 'INC saddr'
    # INC 0fe20h                  ;81 20          saddr
    elif mem[0] == 0x81:
        saddr = _saddr(mem[1])
        return ('INC 0%04xH' % saddr, pc+2)

    # 0x87: 'MOV A,[HL]'
    elif mem[0] == 0x87:
        return ('MOV A,[HL]', pc+1)

    elif mem[0] == 0x8f:
        return ("RETI", pc+1)

    # 0x90, 0x92, 0x94, 0x96
    elif (mem[0] & 0b11111001) == 0b10010000:
        regpair = (mem[0] >> 1) & 0b11
        regpairname = _regpairname(regpair)
        return ("DECW %s" % regpairname, pc+1)

    # 0x91: 'DEC saddr'
    # DEC 0fe20h                  ;91 20          saddr
    elif mem[0] == 0x91:
        saddr = _saddr(mem[1])
        return ('DEC 0%04xH' % saddr, pc+2)

    # 0x95: MOV [DE],A
    elif mem[0] == 0x95:
        return ('MOV [DE],A', pc+1)

    # 0x97: 'MOV [HL],A'
    elif mem[0] == 0x97:
        return ('MOV [HL],A', pc+1)

    # 0x9a: 'CALL !addr16'
    elif mem[0] == 0x9a:
        addr16 = mem[1] + (mem[2] << 8)
        return ('CALL !0%04xH' % addr16, pc+3)

    # 0x9b: 'BR !addr16'
    elif mem[0] == 0x9b:
        addr16 = mem[1] + (mem[2] << 8)
        return ('BR !0%04xH' % addr16, pc+3)

    elif mem[0] == 0x9f:
        return ("RETB", pc+1)

    # 0xa0: 'MOV X,#byte' .. 0xa7: 'MOV H,#byte'
    elif (mem[0] & 0b11111000) == 0b10100000:
        reg = mem[0] & 0b111
        regname = _regname(reg)
        byte = mem[1]
        return ("MOV %s,#0%02xH" % (regname, byte), pc+1)

    elif mem[0] == 0xaf:
        return ("RET", pc+1)

    # 0xB0, 0xB2, 0xB4, 0xB6
    elif (mem[0] & 0b11111001) == 0b10110000:
        regpair = (mem[0] >> 1) & 0b11
        regpairname = _regpairname(regpair)
        return ("POP %s" % regpairname, pc+1)

    # 0xB1, 0xB3, 0xB5, 0xB7
    elif (mem[0] & 0b11111001) == 0b10110001:
        regpair = (mem[0] >> 1) & 0b11
        regpairname = _regpairname(regpair)
        return ("PUSH %s" % regpairname, pc+1)

    # 0xba: 'MOV [HL+C],A'
    # MOV [HL+C],A                ;BA
    elif mem[0] == 0xba:
        return ("MOV [HL+C],A", 1)

    # MOV [HL+B],A                ;BB
    elif mem[0] == 0xbb:
        return ("MOV [HL+B],A", 1)

    elif mem[0] == 0xbf:
        return ("BRK", pc+1)

    # 0xC0, 0xC2, 0xC4, 0xC6
    elif (mem[0] & 0b11111001) == 0b11000000:
        # TODO emit ILLEGAL for 0xC0
        regpair = (mem[0] >> 1) & 0b11
        regpairname = _regpairname(regpair)
        return ("MOVW AX,%s" % regpairname, pc+1)

    # ADDW AX,#0abcdh             ;CA CD AB
    elif mem[0] == 0xCA:
        imm16 = mem[1] + (mem[2] << 8)
        return ("ADDW AX,#0%04xH" % imm16, 3)

    # 0xD0, 0xD2, 0xD4, 0xD6
    elif (mem[0] & 0b11111001) == 0b11010000:
        # TODO emit ILLEGAL for 0xD0
        regpair = (mem[0] >> 1) & 0b11
        regpairname = _regpairname(regpair)
        return ("MOVW %s,AX" % regpairname, pc+1)

    # SUBW AX,#0abcdh             ;DA CD AB
    elif mem[0] == 0xDA:
        imm16 = mem[1] + (mem[2] << 8)
        return ("SUBW AX,#0%04xH" % imm16, 3)

    # 0xE0, 0xE2, 0xE4, 0xE6
    elif (mem[0] & 0b11111001) == 0b11100000:
        # TODO emit ILLEGAL for 0xD0
        regpair = (mem[0] >> 1) & 0b11
        regpairname = _regpairname(regpair)
        return ("XCHW AX,%s" % regpairname, pc+1)

    # CMPW AX,#0abcdh             ;EA CD AB
    elif mem[0] == 0xea:
        imm16 = mem[1] + (mem[2] << 8)
        return ("CMPW AX,#0%04xH" % imm16, 3)

    else:
        raise NotImplementedError()


def _regpairname(regpair):
    return ('AX', 'BC', 'DE', 'HL')[regpair]

def _regname(reg):
    return ('X', 'A', 'C', 'B', 'E', 'D', 'L', 'H')[reg]

def _saddr(byte):
    # When 8-bit immediate data is at 20H to FFH,
    # bit 8 of an effective address is set to 0. When
    # it is at 00H to 1FH, bit 8 is set to 1.
    saddr = 0xfe00 + byte
    if byte in range(0x20):
        saddr |= 0b100000000
    return saddr
