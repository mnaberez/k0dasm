
def disassemble(mem, pc):
    #
    # Instructions that require only the first byte to recognize
    #

    # nop                         ;00
    if mem[0] == 0x00:
        return ("NOP", pc+1)

    # not1 cy                     ;01
    elif mem[0] == 0x01:
        return ('NOT1 CY', pc+1)

    # movw ax,0fe20h              ;02 CE AB       saddrp
    elif mem[0] == 0x02:
        saddrp = mem[1] + (mem[2] << 8)
        return ('MOVW AX,0%04xH' % saddrp, pc+3)

    # MOVW 0fe20h,AX              ;03 CE AB       saddrp
    elif mem[0] == 0x03:
        saddrp = mem[1] + (mem[2] << 8)
        return ('MOVW 0%04xH,AX' % saddrp, pc+3)

    # DBNZ 0fe20h,$label0         ;04 20 FD       saddr
    elif mem[0] == 0x04:
        saddr = _saddr(mem[1])
        disp = mem[2]
        new_pc = pc + 3
        target = _resolve_rel(new_pc, disp)
        return ('DBNZ 0%04xH,$0%04xH' % (saddr, target), new_pc)

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
        return ("ADD A,[HL+0%02xH]" % byte, pc+2)

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

    # 0x18: 'SUB A,!addr16'
    elif mem[0] == 0x18:
        addr16 = mem[1] + (mem[2] << 8)
        return ('SUB A,!0%04xH' % addr16, pc+3)

    # 0x19: 'SUB A,[HL+byte]'
    elif mem[0] == 0x19:
        offset = mem[1]
        return ('SUB A,[HL+0%02xH]' % offset, pc+2)

    # 0x1d: 'SUB A,#byte'
    elif mem[0] == 0x1d:
        imm8 = mem[1]
        return ('SUB A,#0%02xH' % imm8, pc+2)

    elif mem[0] == 0x1e:
        saddr = _saddr(mem[1])
        return ('SUB A,0%04xH' % saddr, pc+2)

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

    # 0x28: 'ADDC A,!addr16'
    elif mem[0] == 0x28:
        addr16 = mem[1] + (mem[2] << 8)
        return ('ADDC A,!0%04xH' % addr16, pc+3)

    # 0x38: 'SUBC A,!addr16'
    elif mem[0] == 0x38:
        addr16 = mem[1] + (mem[2] << 8)
        return ('SUBC A,!0%04xH' % addr16, pc+3)

    # 0x2e: 'ADDC A,saddr'
    elif mem[0] == 0x2e:
        saddr = _saddr(mem[1])
        return ('ADDC A,0%04xH' % saddr, pc+2)

    # 0x27: 'ADDC A,[HL]'
    elif mem[0] == 0x2f:
        return ('ADDC A,[HL]', pc+1)

    # ADDC A,[HL+0abh]            ;29 AB
    elif mem[0] == 0x29:
        offset = mem[1]
        return ('ADDC A,[HL+0%02xH]' % offset, pc+2)

    # 0x2d: 'ADDC A,#byte'
    elif mem[0] == 0x2d:
        imm8 = mem[1]
        return ('ADDC A,#0%02xH' % imm8, pc+2)

    # 0x30: 'XCH A,X' .. 0x37: 'XCH A,H'
    # except 0x31
    elif mem[0] in (0x30, 0x32, 0x33, 0x34, 0x35, 0x36, 0x37):
        reg = mem[0] & 0b111
        regname = _regname(reg)
        return ("XCH A,%s" % regname, pc+1)

    # 0x39: 'SUBC A,[HL+byte]'
    elif mem[0] == 0x39:
        offset = mem[1]
        return ('SUBC A,[HL+0%02xH]' % offset, pc+2)

    # 0x3d: 'SUBC A,#byte'
    elif mem[0] == 0x3d:
        imm8 = mem[1]
        return ('SUBC A,#0%02xH' % imm8, pc+2)

    # 0x3e: 'SUBC A,saddr'
    elif mem[0] == 0x3e:
        saddr = _saddr(mem[1])
        return ('SUBC A,0%04xH' % saddr, pc+2)

    # 0x3f: 'SUBC A,[HL]'
    elif mem[0] == 0x3f:
        return ('SUBC A,[HL]', pc+1)

    # 0x40: 'INC X' .. 0x47: 'INC H'
    elif mem[0] in (0x40, 0x41, 0x42, 0x43, 0x44, 0x45, 0x46, 0x47):
        reg = mem[0] & 0b111
        regname = _regname(reg)
        return ("INC %s" % regname, pc+1)

    # 0x48: 'CMP A,!addr16'
    elif mem[0] == 0x48:
        addr16 = mem[1] + (mem[2] << 8)
        return ('CMP A,!0%04xH' % addr16, pc+3)

    # 0x49: 'CMP A,[HL+byte]'
    elif mem[0] == 0x49:
        offset = mem[1]
        return ('CMP A,[HL+0%02xH]' % offset, pc+2)

    # 0x4d: 'CMP A,#byte'
    elif mem[0] == 0x4d:
        imm8 = mem[1]
        return ('CMP A,#0%02xH' % imm8, pc+2)

    # 0x4e: 'CMP A,saddr
    elif mem[0] == 0x4e:
        saddr = _saddr(mem[1])
        return ('CMP A,0%04xH' % saddr, pc+2)

    # 0x4f: 'CMP A,[HL]'
    elif mem[0] == 0x4f:
        return ('CMP A,[HL]', pc+1)

    # 0x50: 'DEC X' .. 0x57: 'DEC H'
    elif mem[0] in (0x50, 0x51, 0x52, 0x53, 0x54, 0x55, 0x56, 0x57):
        reg = mem[0] & 0b111
        regname = _regname(reg)
        return ("DEC %s" % regname, pc+1)

    # 0x58: 'AND A,!addr16'
    elif mem[0] == 0x58:
        addr16 = mem[1] + (mem[2] << 8)
        return ('AND A,!0%04xH' % addr16, pc+3)

    # 0x59: 'AND A,[HL+byte]'
    elif mem[0] == 0x59:
        offset = mem[1]
        return ('AND A,[HL+0%02xH]' % offset, pc+2)

    # 0x5d: 'AND A,#byte'
    elif mem[0] == 0x5d:
        imm8 = mem[1]
        return ('AND A,#0%02xH' % imm8, pc+2)

    # 0x5e: 'AND A,saddr'
    elif mem[0] == 0x5e:
        saddr = _saddr(mem[1])
        return ('AND A,0%04xH' % saddr, pc+2)

    # 0x5f: 'AND A,[HL]'
    elif mem[0] == 0x5f:
        return ('AND A,[HL]', pc+1)

    # 0x60: 'MOV A,X' .. 0x67: 'MOV A,H'
    # except 0x61
    elif mem[0] in (0x60, 0x62, 0x63, 0x64, 0x65, 0x66, 0x67):
        reg = mem[0] & 0b111
        regname = _regname(reg)
        return ("MOV A,%s" % regname, pc+1)

    # 0x68: 'OR A,!addr16'
    elif mem[0] == 0x68:
        addr16 = mem[1] + (mem[2] << 8)
        return ('OR A,!0%04xH' % addr16, pc+3)

    # 0x69: 'OR A,[HL+byte]'
    elif mem[0] == 0x69:
        offset = mem[1]
        return ('OR A,[HL+0%02xH]' % offset, pc+2)

    # 0x6d: 'OR A,#byte'
    elif mem[0] == 0x6d:
        imm8 = mem[1]
        return ('OR A,#0%02xH' % imm8, pc+2)

    # 0x6e: 'OR A,saddr'
    elif mem[0] == 0x6e:
        saddr = _saddr(mem[1])
        return ('OR A,0%04xH' % saddr, pc+2)

    # 0x7e: 'XOR A,saddr'
    elif mem[0] == 0x7e:
        saddr = _saddr(mem[1])
        return ('XOR A,0%04xH' % saddr, pc+2)

    # 0x6f: 'OR A,[HL]'
    elif mem[0] == 0x6f:
        return ('OR A,[HL]', pc+1)

    # 0x70: 'MOV X,A' .. 0x77: 'MOV H,A'
    # except 0x71
    elif mem[0] in (0x70, 0x72, 0x73, 0x74, 0x75, 0x76, 0x77):
        reg = mem[0] & 0b111
        regname = _regname(reg)
        return ("MOV %s,A" % regname, pc+1)

    # 0x78: 'XOR A,!addr16'
    elif mem[0] == 0x78:
        addr16 = mem[1] + (mem[2] << 8)
        return ('XOR A,!0%04xH' % addr16, pc+3)

    # 0x79: 'XOR A,[HL+byte]'
    elif mem[0] == 0x79:
        offset = mem[1]
        return ('XOR A,[HL+0%02xH]' % offset, pc+2)

    # 0x7d: 'XOR A,#byte'
    elif mem[0] == 0x7d:
        imm8 = mem[1]
        return ('XOR A,#0%02xH' % imm8, pc+2)

    # 0x7f: 'XOR A,[HL]'
    elif mem[0] == 0x7f:
        return ('XOR A,[HL]', pc+1)

    elif mem[0] in (0x80, 0x82, 0x84, 0x86):
        regpair = (mem[0] >> 1) & 0b11
        regpairname = _regpairname(regpair)
        return ("INCW %s" % regpairname, pc+1)

    # 0x81: 'INC saddr'
    # INC 0fe20h                  ;81 20          saddr
    elif mem[0] == 0x81:
        saddr = _saddr(mem[1])
        return ('INC 0%04xH' % saddr, pc+2)

    # 0x83: 'XCH A,saddr'
    elif mem[0] == 0x83:
        saddr = _saddr(mem[1])
        return ('XCH A,0%04xH' % saddr, pc+2)

    # 0x85: 'MOV A,[DE]'
    elif mem[0] == 0x85:
        return ('MOV A,[DE]', pc+1)

    # 0x87: 'MOV A,[HL]'
    elif mem[0] == 0x87:
        return ('MOV A,[HL]', pc+1)

    # 0x88: 'ADD saddr,#byte'
    elif mem[0] == 0x88:
        saddr = _saddr(mem[1])
        imm8 = mem[2]
        return ('ADD 0%04xH,#0%02xH' % (saddr, imm8), pc+3)

    # 0x8a: 'DBNZ C,$rel   '
    elif mem[0] == 0x8a:
        disp = mem[1]
        new_pc = pc + 2
        target = _resolve_rel(new_pc, disp)
        return ('DBNZ C,$0%04xH' % target, new_pc)

    # 0x8b: 'DBNZ B,$rel   '
    elif mem[0] == 0x8b:
        disp = mem[1]
        new_pc = pc + 2
        target = _resolve_rel(new_pc, disp)
        return ('DBNZ B,$0%04xH' % target, new_pc)

    # 0x8d: 'BC $rel'
    elif mem[0] == 0x8d:
        disp = mem[1]
        new_pc = pc + 2
        target = _resolve_rel(new_pc, disp)
        return ('BC $0%04xH' % target, pc+2)

    # 0x8e: 'MOV A,!addr16'
    elif mem[0] == 0x8e:
        addr16 = mem[1] + (mem[2] << 8)
        return ('MOV A,!0%04xH' % addr16, pc+3)

    elif mem[0] == 0x8f:
        return ("RETI", pc+1)

    elif mem[0] in (0x90, 0x92, 0x94, 0x96):
        regpair = (mem[0] >> 1) & 0b11
        regpairname = _regpairname(regpair)
        return ("DECW %s" % regpairname, pc+1)

    # 0x91: 'DEC saddr'
    # DEC 0fe20h                  ;91 20          saddr
    elif mem[0] == 0x91:
        saddr = _saddr(mem[1])
        return ('DEC 0%04xH' % saddr, pc+2)

    # 0x93: 'XCH A,sfr'
    elif mem[0] == 0x93:
        sfr = _sfr(mem[1])
        return ("XCH A,0%04xH" % sfr, pc+2)

    # 0x13: 'MOV sfr,#byte'
    elif mem[0] == 0x13:
        sfr = _sfr(mem[1])
        imm8 = mem[2]
        return ("MOV 0%04xH,#0%02xH" % (sfr, imm8), pc+3)

    # 0x95: MOV [DE],A
    elif mem[0] == 0x95:
        return ('MOV [DE],A', pc+1)

    # 0x97: 'MOV [HL],A'
    elif mem[0] == 0x97:
        return ('MOV [HL],A', pc+1)

    # 0x98: 'SUB saddr,#byte'
    elif mem[0] == 0x98:
        saddr = _saddr(mem[1])
        imm8 = mem[2]
        return ('SUB 0%04xH,#0%02xH' % (saddr, imm8), pc+3)

    # 0x9a: 'CALL !addr16'
    elif mem[0] == 0x9a:
        addr16 = mem[1] + (mem[2] << 8)
        return ('CALL !0%04xH' % addr16, pc+3)

    # 0x9b: 'BR !addr16'
    elif mem[0] == 0x9b:
        addr16 = mem[1] + (mem[2] << 8)
        return ('BR !0%04xH' % addr16, pc+3)

    # 0x9d: 'BNC $rel'
    elif mem[0] == 0x9d:
        disp = mem[1]
        new_pc = pc + 2
        target = _resolve_rel(new_pc, disp)
        return ('BNC $0%04xH' % target, new_pc)

    # 0x9e: 'MOV !addr16,A'
    elif mem[0] == 0x9e:
        addr16 = mem[1] + (mem[2] << 8)
        return ('MOV !0%04xH,A' % addr16, pc+3)

    elif mem[0] == 0x9f:
        return ("RETB", pc+1)

    elif mem[0] in (0xa0, 0xa1, 0xa2, 0xa3, 0xa4, 0xa5, 0xa6, 0xa7):
        reg = mem[0] & 0b111
        regname = _regname(reg)
        byte = mem[1]
        return ("MOV %s,#0%02xH" % (regname, byte), pc+2)

    # 0xa8: 'ADDC saddr,#byte'
    elif mem[0] == 0xa8:
        saddr = _saddr(mem[1])
        imm8 = mem[2]
        return ('ADDC 0%04xH,#0%02xH' % (saddr, imm8), pc+3)

    # 0xa9: 'MOVW AX,sfrp'
    elif mem[0] == 0xa9:
        sfrp = _sfrp(mem[1])
        return ("MOVW AX,0%04xH" % sfrp, pc+2)

    elif mem[0] == 0xaa:
        return ("MOV A,[HL+C]", pc+1)

    elif mem[0] == 0xab:
        return ("MOV A,[HL+B]", pc+1)

    # 0xad: 'BZ $rel   '
    elif mem[0] == 0xad:
        disp = mem[1]
        new_pc = pc + 2
        target = _resolve_rel(new_pc, disp)
        return ('BZ $0%04xH' % target, new_pc)

    # 0xae: 'MOV A,[HL+byte]'
    elif mem[0] == 0xae:
        imm8 = mem[1]
        return ("MOV A,[HL+0%02xH]" % imm8, pc+2)

    elif mem[0] == 0xaf:
        return ("RET", pc+1)

    elif mem[0] in (0xb0, 0xb2, 0xb4, 0xb6):
        regpair = (mem[0] >> 1) & 0b11
        regpairname = _regpairname(regpair)
        return ("POP %s" % regpairname, pc+1)

    elif mem[0]in (0xb1, 0xb3, 0xb5, 0xb7):
        regpair = (mem[0] >> 1) & 0b11
        regpairname = _regpairname(regpair)
        return ("PUSH %s" % regpairname, pc+1)

    # 0xb8: 'SUBC saddr,#byte'
    elif mem[0] == 0xb8:
        saddr = _saddr(mem[1])
        imm8 = mem[2]
        return ('SUBC 0%04xH,#0%02xH' % (saddr, imm8), pc+3)

    # 0xb9: 'MOVW sfrp,AX'
    elif mem[0] == 0xb9:
        sfrp = _sfrp(mem[1])
        return ("MOVW 0%04xH,AX" % sfrp, pc+2)

    # 0xba: 'MOV [HL+C],A'
    # MOV [HL+C],A                ;BA
    elif mem[0] == 0xba:
        return ("MOV [HL+C],A", pc+1)

    # MOV [HL+B],A                ;BB
    elif mem[0] == 0xbb:
        return ("MOV [HL+B],A", pc+1)

    # 0xbd: 'BNZ $rel'
    elif mem[0] == 0xbd:
        disp = mem[1]
        new_pc = pc + 2
        target = _resolve_rel(new_pc, disp)
        return ('BNZ $0%04xH' % target, new_pc)

    # 0xbe: 'MOV [HL+byte],A'
    elif mem[0] == 0xbe:
        imm8 = mem[1]
        return ("MOV [HL+0%02xH],A" % imm8, pc+2)

    elif mem[0] == 0xbf:
        return ("BRK", pc+1)

    elif mem[0] == 0xc0:
        return ("ILLEGAL 0xc0", pc+1)

    elif mem[0] in (0xc2, 0xc4, 0xc6):
        regpair = (mem[0] >> 1) & 0b11
        regpairname = _regpairname(regpair)
        return ("MOVW AX,%s" % regpairname, pc+1)

    # 0xc8: 'CMP saddr,#byte'
    elif mem[0] == 0xc8:
        saddr = _saddr(mem[1])
        imm8 = mem[2]
        return ('CMP 0%04xH,#0%02xH' % (saddr, imm8), pc+3)

    # ADDW AX,#0abcdh             ;CA CD AB
    elif mem[0] == 0xCA:
        imm16 = mem[1] + (mem[2] << 8)
        return ("ADDW AX,#0%04xH" % imm16, pc+3)

    # 0xce: 'XCH A,!addr16'
    elif mem[0] == 0xce:
        addr16 = mem[1] + (mem[2] << 8)
        return ('XCH A,!0%04xH' % addr16, pc+3)

    elif mem[0] == 0xd0:
        return ("ILLEGAL 0xd0", pc+1)

    elif mem[0] in (0xd2, 0xd4, 0xd6):
        regpair = (mem[0] >> 1) & 0b11
        regpairname = _regpairname(regpair)
        return ("MOVW %s,AX" % regpairname, pc+1)

    # 0xd8: 'AND saddr,#byte'
    elif mem[0] == 0xd8:
        saddr = _saddr(mem[1])
        imm8 = mem[2]
        return ('AND 0%04xH,#0%02xH' % (saddr, imm8), pc+3)

    # SUBW AX,#0abcdh             ;DA CD AB
    elif mem[0] == 0xDA:
        imm16 = mem[1] + (mem[2] << 8)
        return ("SUBW AX,#0%04xH" % imm16, pc+3)

    # 0xde: 'XCH A,[HL+byte]'
    elif mem[0] == 0xde:
        imm8 = mem[1]
        return ("XCH A,[HL+0%02xH]" % imm8, pc+2)

    elif mem[0] == 0xe0:
        return ("ILLEGAL 0xe0", pc+1)

    elif mem[0] in (0xe2, 0xe4, 0xe6):
        regpair = (mem[0] >> 1) & 0b11
        regpairname = _regpairname(regpair)
        return ("XCHW AX,%s" % regpairname, pc+1)

    # 0xe8: 'OR saddr,#byte'
    elif mem[0] == 0xe8:
        saddr = _saddr(mem[1])
        imm8 = mem[2]
        return ('OR 0%04xH,#0%02xH' % (saddr, imm8), pc+3)

    # CMPW AX,#0abcdh             ;EA CD AB
    elif mem[0] == 0xea:
        imm16 = mem[1] + (mem[2] << 8)
        return ("CMPW AX,#0%04xH" % imm16, pc+3)

    # 0xf4: 'MOV A,sfr'
    elif mem[0] == 0xf4:
        sfr = _sfr(mem[1])
        return ("MOV A,0%04xH" % sfr, pc+2)

    # 0xf6: 'MOV sfr,A'
    elif mem[0] == 0xf6:
        sfr = _sfr(mem[1])
        return ("MOV 0%04xH,A" % sfr, pc+2)

    # 0xf8: 'XOR saddr,#byte'
    elif mem[0] == 0xf8:
        saddr = _saddr(mem[1])
        imm8 = mem[2]
        return ('XOR 0%04xH,#0%02xH' % (saddr, imm8), pc+3)

    # 0xfa: 'BR $rel'
    elif mem[0] == 0xfa:
        disp = mem[1]
        new_pc = pc + 2
        target = _resolve_rel(new_pc, disp)
        return ('BR $0%04xH' % target, new_pc)

    # MOVW 0fffeh,#0abcdh         ;FE FE CD AB    sfrp
    elif mem[0] == 0xfe:
        sfrp = _sfrp(mem[1])
        imm16 = mem[2] + (mem[3] << 8)
        return ('MOVW 0%04xH,#0%04xH' % (sfrp, imm16), pc+4)

    #
    # Instructions that require multiple bytes to recognize
    #

    # MOV 0fe20h,#0abh            ;11 20 AB       saddr
    # MOV PSW,#0abh               ;11 1E AB
    elif mem[0] == 0x11:
        saddr = _saddr(mem[1])
        imm8 = mem[2]
        if saddr == 0xff1e:
            return ('MOV PSW,#0%02xH' % imm8, pc+3)
        else:
            return ('MOV 0%04xH,#0%02xH' % (saddr, imm8), pc+3)

    # SET1 0fe20h.7               ;7A 20          saddr
    # SET1 PSW.7                  ;7A 1E
    # EI                          ;7A 1E          alias for SET1 PSW.7
    elif mem[0] in (0x0a, 0x1a, 0x2a, 0x3a, 0x4a, 0x5a, 0x6a, 0x7a):
        bit = _bit(mem[0])
        saddr = _saddr(mem[1])
        if saddr == 0xff1e:
            if bit == 7:
                return ("EI", pc+2) # alias for SET1 PSW.7
            else:
                return ('SET1 PSW.%d' % bit, pc+2)
        else:
            return ('SET1 0%04xH.%d' % (saddr, bit), pc+2)

    # CLR1 0fe20h.7               ;7B 20          saddr
    # CLR1 PSW.7                  ;7B 1E
    # DI                          ;7B 1E          alias for CLR1 PSW.7
    elif mem[0] in (0x0b, 0x1b, 0x2b, 0x3b, 0x4b, 0x5b, 0x6b, 0x7b):
        bit = _bit(mem[0])
        saddr = _saddr(mem[1])
        if saddr == 0xff1e:
            if bit == 7:
                return ("DI", pc+2) # alias for CLR1 PSW.7
            else:
                return ('CLR1 PSW.%d' % bit, pc+2)
        else:
            return ('CLR1 0%04xH.%d' % (saddr, bit), pc+2)

    elif mem[0] == 0x31:
        if mem[1] == 0x80:
            new_pc = pc + 2
            return ('ROL4 [HL]', new_pc)
        elif mem[1] == 0x82:
            new_pc = pc + 2
            return ('DIVUW C', new_pc)
        elif mem[1] == 0x88:
            new_pc = pc + 2
            return ('MULU X', new_pc)
        elif mem[1] == 0x90:
            new_pc = pc + 2
            return ('ROR4 [HL]', new_pc)
        elif mem[1] == 0x98:
            new_pc = pc + 2
            return ('BR AX', new_pc)
        elif (mem[1] >> 4) < 0x09 and (mem[1] & 0x0f) in (0x0a, 0x0b):
            new_pc = pc + 2
            inst = mem[1] >> 4
            names = ('ADD', 'SUB', 'ADDC', 'SUBC', 'CMP', 'AND', 'OR', 'XOR', 'XCH')
            instname = names[inst]

            mode = mem[1] & 0x0f
            modename = "A,[HL+B]" if mode == 0x0b else "A,[HL+C]"

            return ("%s %s" % (instname, modename), new_pc)
        elif (mem[1] >> 4) < 0x08 and (mem[1] & 0x0f) in (0x0d, 0x0e, 0x0f):
            new_pc = pc + 3

            inst = (mem[1] & 0x0f) - 0x0d
            names = ('BTCLR', 'BT', 'BF')
            instname = names[inst]

            bit = mem[1] >> 4
            disp = mem[2]
            target = _resolve_rel(new_pc, disp)

            return ("%s A.%d,$0%04xH" % (instname, bit, target), new_pc)
        elif (mem[1] >> 4) < 0x08 and (mem[1] & 0x0f) in (0x01, 0x03):
            new_pc = pc + 4

            instname = 'BTCLR' if (mem[1] & 0x0f) == 0x01 else 'BF'
            bit = mem[1] >> 4
            saddr = _saddr(mem[2])
            disp = mem[3]
            target = _resolve_rel(new_pc, disp)

            if saddr == 0xff1e:
                return ("%s PSW.%d,$0%04xH" % (instname, bit, target), new_pc)
            else:
                return ("%s 0%04xH.%d,$0%04xH" % (instname, saddr, bit, target), new_pc)
        elif (mem[1] >> 4) < 0x08 and (mem[1] & 0x0f) in (0x5, 0x6, 0x7):
            new_pc = pc + 4

            inst = (mem[1] & 0x0f) - 0x05
            names = ('BTCLR', 'BT', 'BF')
            instname = names[inst]

            bit = mem[1] >> 4
            sfr = _sfr(mem[2])
            disp = mem[3]
            target = _resolve_rel(new_pc, disp)

            return ("%s 0%04xH.%d,$0%04xH" % (instname, sfr, bit, target), new_pc)
        elif (mem[1] >> 4) in range(0x8, 0xf+1) and (mem[1] & 0x0f) in (0x5, 0x6, 0x7):
            new_pc = pc + 3

            inst = (mem[1] & 0x0f) - 0x05
            names = ('BTCLR', 'BT', 'BF')
            instname = names[inst]

            bit = (mem[1] >> 4) - 0x08
            disp = mem[2]
            target = _resolve_rel(new_pc, disp)

            return ("%s [HL].%d,$0%04xH" % (instname, bit, target), new_pc)
        else:
            raise NotImplementedError("31 %02x" % mem[1])

    elif mem[0] == 0x61:
        new_pc = pc + 2
        bit = _bit(mem[1])
        regname = _regname(mem[1] & 0b111)
        if mem[1] == 0x80:
            return ('ADJBA', new_pc)
        elif mem[1] == 0x90:
            return ('ADJBS', new_pc)
        elif mem[1] == 0xd0:
            return ('SEL RB0', new_pc)
        elif mem[1] == 0xd8:
            return ('SEL RB1', new_pc)
        elif mem[1] == 0xf0:
            return ('SEL RB2', new_pc)
        elif mem[1] == 0xf8:
            return ('SEL RB3', new_pc)
        elif mem[1] in range(0x00, 0x80):
            inst = mem[1] >> 4
            names = ('ADD', 'SUB', 'ADDC', 'SUBC', 'CMP', 'AND', 'OR', 'XOR')
            instname = names[inst]

            mode = mem[1] & 0x0f
            modetpl = "%s,A" if mode in range(0x00, 0x08) else "A,%s"

            template = instname + " " + modetpl
            return (template % regname), new_pc
        elif mem[1] in (0x89, 0x99, 0xa9, 0xb9, 0xc9, 0xd9, 0xe9, 0xf9):
            return ('MOV1 A.%d,CY' % bit, new_pc)
        elif mem[1] in (0x8a, 0x9a, 0xaa, 0xba, 0xca, 0xda, 0xea, 0xfa):
            return ('SET1 A.%d' % bit, new_pc)
        elif mem[1] in (0x8b, 0x9b, 0xab, 0xbb, 0xcb, 0xdb, 0xeb, 0xfb):
            return ('CLR1 A.%d' % bit, new_pc)
        elif mem[1] in (0x8c, 0x9c, 0xac, 0xbc, 0xcc, 0xdc, 0xec, 0xfc):
            return ('MOV1 CY,A.%d' % bit, new_pc)
        elif mem[1] in (0x8d, 0x9d, 0xad, 0xbd, 0xcd, 0xdd, 0xed, 0xfd):
            return ('AND1 CY,A.%d' % bit, new_pc)
        elif mem[1] in (0x8e, 0x9e, 0xae, 0xbe, 0xce, 0xde, 0xee, 0xfe):
            return ('OR1 CY,A.%d' % bit, new_pc)
        elif mem[1] in (0x8f, 0x9f, 0xaf, 0xbf, 0xcf, 0xdf, 0xef, 0xff):
            return ('XOR1 CY,A.%d' % bit, new_pc)
        else:
            raise NotImplementedError("61 %02x" % mem[1])

    elif mem[0] == 0x71:
        if mem[1] == 0x00:
            return ('STOP', pc+2)
        elif mem[1] == 0x10:
            return ('HALT', pc+2)
        elif mem[1] in (0x82, 0x92, 0xa2, 0xb2, 0xc2, 0xd2, 0xe2, 0xf2):
            bit = (mem[1] >> 4) - 8
            return ('SET1 [HL].%d' % bit, pc+2)
        elif mem[1] in (0x83, 0x93, 0xa3, 0xb3, 0xc3, 0xd3, 0xe3, 0xf3):
            bit = (mem[1] >> 4) - 8
            return ('CLR1 [HL].%d' % bit, pc+2)
        elif (mem[1] >> 4) in range(8, 0x0f+1) and (mem[1] & 0x0f) in (0x4, 0x5, 0x6, 0x7):
            bit = (mem[1] >> 4) - 8
            inst = (mem[1] & 0x0f) - 4
            names = ('MOV1', 'AND1', 'OR1', 'XOR1')
            instname = names[inst]
            return ('%s CY,[HL].%d' % (instname, bit), pc+2)
        elif (mem[1] >> 4) in range(8, 0x0f+1) and (mem[1] & 0x0f) == 1:
            bit = (mem[1] >> 4) - 8
            return ('MOV1 [HL].%d,CY' % bit, pc+2)
        elif (mem[1] >> 4) < 8 and (mem[1] & 0x0f) in (0x0a, 0x0b):
            bit = (mem[1] >> 4)
            instname = 'SET1' if (mem[1] & 0x0f) == 0x0a else 'CLR1'
            sfr = _sfr(mem[2])
            return ('%s 0%04xH.%d' % (instname, sfr, bit), pc+3)
        elif (mem[1] >> 4) < 8 and (mem[1] & 0x0f) == 0x09:
            bit = (mem[1] >> 4)
            sfr = _sfr(mem[2])
            return ('MOV1 0%04xH.%d,CY' % (sfr, bit), pc+3)
        elif (mem[1] >> 4) < 8 and (mem[1] & 0x0f) in range(0x0c, 0x0f+1):
            bit = (mem[1] >> 4)
            sfr = _sfr(mem[2])
            inst = (mem[1] & 0x0f) - 0x0c
            names = ('MOV1', 'AND1', 'OR1', 'XOR1')
            instname = names[inst]
            return ('%s CY,0%04xH.%d' % (instname, sfr, bit), pc+3)
        elif (mem[1] >> 4) < 8 and (mem[1] & 0x0f) == 1:
            bit = (mem[1] >> 4)
            saddr = _saddr(mem[2])
            if saddr == 0xff1e:
                return ('MOV1 PSW.%d,CY' % bit, pc+3)
            else:
                return ('MOV1 0%04xH.%d,CY' % (saddr, bit), pc+3)
        elif (mem[1] >> 4) < 8 and (mem[1] & 0x0f) in (0x4, 0x5, 0x6, 0x7):
            bit = (mem[1] >> 4)
            inst = (mem[1] & 0x0f) - 4
            names = ('MOV1', 'AND1', 'OR1', 'XOR1')
            instname = names[inst]
            saddr = _saddr(mem[2])
            if saddr == 0xff1e:
                return ('%s CY,PSW.%d' % (instname, bit), pc+3)
            else:
                return ('%s CY,0%04xH.%d' % (instname, saddr, bit), pc+3)
        else:
            raise NotImplementedError("71 %02x" % mem[1])

    # MOVW AX,0fe20h              ;89 20          saddrp
    # MOVW AX,SP                  ;89 1C
    elif mem[0] == 0x89:
        saddrp = _saddrp(mem[1])
        if saddrp == 0xff1c:
            return ('MOVW AX,SP', pc+2)
        else:
            return ('MOVW AX,0%04xH' % saddrp, pc+2)

    # BT 0fe20h.0,$label8         ;8C 20 FD       saddr
    # BT PSW.0,$label9            ;8C 1E FD
    elif mem[0] in (0x8c, 0x9c, 0xac, 0xbc, 0xcc, 0xdc, 0xec, 0xfc):
        bit = _bit(mem[0])
        saddr = _saddr(mem[1])
        disp = mem[2]
        new_pc = pc + 3
        target = _resolve_rel(new_pc, disp)
        if saddr == 0xff1e:
            return ('BT PSW.%d,$0%04xH' % (bit, target), new_pc)
        else:
            return ('BT 0%04xH.%d,$0%04xH' % (saddr, bit, target), new_pc)

    # MOVW 0fe20h,AX              ;99 20          saddrp
    # MOVW SP,AX                  ;99 1C
    elif mem[0] == 0x99:
        saddrp = _saddrp(mem[1])
        if saddrp == 0xff1c:
            return ('MOVW SP,AX', pc+2)
        else:
            return ('MOVW 0%04xH,AX' % saddrp, pc+2)

    # MOVW 0fe20h,#0abcdh         ;EE 20 CD AB    saddrp
    # MOVW SP,#0abcdh             ;EE 1C CD AB
    elif mem[0] == 0xee:
        saddrp = _saddrp(mem[1])
        imm16 = mem[2] + (mem[3] << 8)
        if saddrp == 0xff1c:
            return ('MOVW SP,#0%04xH' % imm16, pc+4)
        else:
            return ('MOVW 0%04xH,#0%04xH' % (saddrp, imm16), pc+4)

    # mov a,0fe20h                ;F0 20          saddr
    # mov a,psw                   ;F0 1E
    elif mem[0] == 0xf0:
        saddr = _saddr(mem[1])
        if saddr == 0xff1e:
            return ('MOV A,PSW', pc+2)
        else:
            return ('MOV A,0%04xH' % saddr, pc+2)

    # MOV 0fe20h,A                ;F2 20          saddr
    # MOV PSW,A                   ;F2 1E
    elif mem[0] == 0xf2:
        saddr = _saddr(mem[1])
        if saddr == 0xff1e:
            return ('MOV PSW,A', pc+2)
        else:
            return ('MOV 0%04xH,A' % saddr, pc+2)

    else:
        raise NotImplementedError(hex(mem[0]))


def _regpairname(regpair):
    return ('AX', 'BC', 'DE', 'HL')[regpair]

def _regname(reg):
    return ('X', 'A', 'C', 'B', 'E', 'D', 'L', 'H')[reg]

def _saddr(byte):
    saddr = 0xfe00 + byte
    if byte < 0x20:
        saddr += 0x100
    return saddr
_saddrp = _saddr

def _sfr(byte):
    sfr = 0xff00 + byte
    return sfr
_sfrp = _sfr

def _bit(byte):
    return (byte & 0b01110000) >> 4

def _resolve_rel(pc, displacement):
    if displacement & 0x80:
        displacement = -((displacement ^ 0xFF) + 1)
    return (pc + displacement) & 0xFFFF
