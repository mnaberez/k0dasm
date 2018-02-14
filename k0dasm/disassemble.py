
def disassemble(mem, pc):

    # nop                         ;00
    if mem[0] == 0x00:
        new_pc = pc + 1
        return ("nop", new_pc)

    # not1 cy                     ;01
    elif mem[0] == 0x01:
        new_pc = pc + 1
        return ('not1 cy', new_pc)

    # movw ax,0fe20h              ;02 CE AB       saddrp
    elif mem[0] == 0x02:
        new_pc = pc + 3
        saddrp = mem[1] + (mem[2] << 8)
        return ('movw ax,0%04xh' % saddrp, new_pc)

    # MOVW 0fe20h,AX              ;03 CE AB       saddrp
    elif mem[0] == 0x03:
        new_pc = pc + 3
        saddrp = mem[1] + (mem[2] << 8)
        return ('movw 0%04xh,ax' % saddrp, new_pc)

    # DBNZ 0fe20h,$label0         ;04 20 FD       saddr
    elif mem[0] == 0x04:
        new_pc = pc + 3
        saddr = _saddr(mem[1])
        reldisp = mem[2]
        reltarget = _resolve_rel(new_pc, reldisp)
        return ('dbnz 0%04xh,$0%04xh' % (saddr, reltarget), new_pc)

    # XCH A,[DE]
    elif mem[0] == 0x05:
        new_pc = pc + 1
        return ("xch a,[de]", new_pc)

    # 'XCH A,[HL]'
    elif mem[0] == 0x07:
        new_pc = pc + 1
        return ('xch a,[hl]', new_pc)

    # ADD A,!0abcdh               ;08 CD AB
    elif mem[0] == 0x08:
        new_pc = pc + 3
        addr16 = mem[1] + (mem[2] << 8)
        return ("add a,!0%04xh" % addr16, new_pc)

    # ADD A,[HL+0abh]             ;09 AB
    elif mem[0] == 0x09:
        new_pc = pc + 2
        byte = mem[1]
        return ("add a,[hl+0%02xh]" % byte, new_pc)

    # SET1 0fe20h.7               ;7A 20          saddr
    # SET1 PSW.7                  ;7A 1E
    # EI                          ;7A 1E          alias for SET1 PSW.7
    elif mem[0] in (0x0a, 0x1a, 0x2a, 0x3a, 0x4a, 0x5a, 0x6a, 0x7a):
        new_pc = pc + 2
        bit = _bit(mem[0])
        saddr = _saddr(mem[1])
        if saddr == 0xff1e:
            if bit == 7:
                return ("ei", new_pc) # alias for set1 psw.7
            else:
                return ('set1 psw.%d' % bit, new_pc)
        else:
            return ('set1 0%04xh.%d' % (saddr, bit), new_pc)

    # CLR1 0fe20h.7               ;7B 20          saddr
    # CLR1 PSW.7                  ;7B 1E
    # DI                          ;7B 1E          alias for CLR1 PSW.7
    elif mem[0] in (0x0b, 0x1b, 0x2b, 0x3b, 0x4b, 0x5b, 0x6b, 0x7b):
        new_pc = pc + 2
        bit = _bit(mem[0])
        saddr = _saddr(mem[1])
        if saddr == 0xff1e:
            if bit == 7:
                return ("di", new_pc) # alias for clr1 psw.7
            else:
                return ('clr1 psw.%d' % bit, new_pc)
        else:
            return ('clr1 0%04xh.%d' % (saddr, bit), new_pc)

    # callt [0040H]               ;C1
    # CALLT [{addr5}]             0b11ttttt1                            1
    elif (mem[0] & 0b11000001) == 0b11000001:
        new_pc = pc + 1
        offset = (mem[0] & 0b00111110) >> 1
        addr5 = 0x40 + (offset * 2)
        return ("callt [%04xh]" % addr5, new_pc)

    # callf !0800h                ;0C 00          0c = callf 0800h-08ffh
    # CALLF !{addr11}             0b0xxx1100         0bffffffff         2
    elif (mem[0] & 0b10001111) == 0b00001100:
        new_pc = pc + 2
        base = 0x0800 + ((mem[0] >> 4) << 8)
        address = base + mem[1]
        return ("callf !%04xh" % address, new_pc)

    # 0x0d: 'ADD A,#byte'
    # ADD A,#0abh                 ;0D AB
    elif mem[0] == 0x0d:
        new_pc = pc + 2
        byte = mem[1]
        return ('add a,#0%02xh' % byte, new_pc)

    # 0x0e: 'ADD A,saddr'
    # ADD A,0fe20h                ;0E 20          saddr
    elif mem[0] == 0x0e:
        new_pc = pc + 2
        saddr = _saddr(mem[1])
        return ('add a,0%04xh' % saddr, new_pc)

    # 0x0f: 'ADD A,[HL]'
    # ADD A,[HL]                  ;0F
    elif mem[0] == 0x0f:
        new_pc = pc + 1
        return ('add a,[hl]', new_pc)

    # MOVW {regpair},#word        0b00010pp0                            3
    # MOVW AX,#0abcdh             ;10 CD AB
    # MOVW BC,#0abcdh             ;12 CD AB
    # MOVW DE,#0abcdh             ;14 CD AB
    # MOVW HL,#0abcdh             ;16 CD AB
    elif (mem[0] & 0b11111001) == 0b00010000:
        new_pc = pc + 3
        regpair = _regpair(mem[0])
        imm16 = mem[1] + (mem[2] << 8)
        return ("movw %s,#0%04xh" % (regpair, imm16), new_pc)

    # MOV 0fe20h,#0abh            ;11 20 AB       saddr
    # MOV PSW,#0abh               ;11 1E AB
    elif mem[0] == 0x11:
        new_pc = pc + 3
        saddr = _saddr(mem[1])
        imm8 = mem[2]
        if saddr == 0xff1e:
            return ('mov psw,#0%02xh' % imm8, new_pc)
        else:
            return ('mov 0%04xh,#0%02xh' % (saddr, imm8), new_pc)

    # 0x13: 'MOV sfr,#byte'
    elif mem[0] == 0x13:
        new_pc = pc + 3
        sfr = _sfr(mem[1])
        imm8 = mem[2]
        return ("mov 0%04xh,#0%02xh" % (sfr, imm8), new_pc)

    # 0x18: 'SUB A,!addr16'
    elif mem[0] == 0x18:
        new_pc = pc + 3
        addr16 = mem[1] + (mem[2] << 8)
        return ('sub a,!0%04xh' % addr16, new_pc)

    # 0x19: 'SUB A,[HL+byte]'
    elif mem[0] == 0x19:
        new_pc = pc + 2
        offset = mem[1]
        return ('sub a,[hl+0%02xh]' % offset, new_pc)

    # 0x1d: 'SUB A,#byte'
    elif mem[0] == 0x1d:
        new_pc = pc + 2
        imm8 = mem[1]
        return ('sub a,#0%02xh' % imm8, new_pc)

    elif mem[0] == 0x1e:
        new_pc = pc + 2
        saddr = _saddr(mem[1])
        return ('sub a,0%04xh' % saddr, new_pc)

    elif mem[0] == 0x1f:
        new_pc = pc + 1
        return ('sub a,[hl]', new_pc)

    # 0x20: 'SET1 CY'
    elif mem[0] == 0x20:
        new_pc = pc + 1
        return ('set1 cy', new_pc)

    # 0x21: 'CLR1 CY'
    elif mem[0] == 0x21:
        new_pc = pc + 1
        return ('clr1 cy', new_pc)

    # 0x22: 'PUSH PSW'
    elif mem[0] == 0x22:
        new_pc = pc + 1
        return ('push psw', new_pc)

    # 0x23: 'POP PSW'
    elif mem[0] == 0x23:
        new_pc = pc + 1
        return ('pop psw', new_pc)

    # 0x24: 'ROR A,1'
    elif mem[0] == 0x24:
        new_pc = pc + 1
        return ('ror a,1', new_pc)

    # 0x25: 'RORC A,1'
    elif mem[0] == 0x25:
        new_pc = pc + 1
        return ('rorc a,1', new_pc)

    # 0x26: 'ROL A,1'
    elif mem[0] == 0x26:
        new_pc = pc + 1
        return ('rol a,1', new_pc)

    # 0x27: 'ROLC A,1'
    elif mem[0] == 0x27:
        new_pc = pc + 1
        return ('rolc a,1', new_pc)

    # 0x28: 'ADDC A,!addr16'
    elif mem[0] == 0x28:
        new_pc = pc + 3
        addr16 = mem[1] + (mem[2] << 8)
        return ('addc a,!0%04xh' % addr16, new_pc)

    # 0x38: 'SUBC A,!addr16'
    elif mem[0] == 0x38:
        new_pc = pc + 3
        addr16 = mem[1] + (mem[2] << 8)
        return ('subc a,!0%04xh' % addr16, new_pc)

    # 0x2e: 'ADDC A,saddr'
    elif mem[0] == 0x2e:
        new_pc = pc + 2
        saddr = _saddr(mem[1])
        return ('addc a,0%04xh' % saddr, new_pc)

    # 0x27: 'ADDC A,[HL]'
    elif mem[0] == 0x2f:
        new_pc = pc + 1
        return ('addc a,[hl]', new_pc)

    # ADDC A,[HL+0abh]            ;29 AB
    elif mem[0] == 0x29:
        new_pc = pc + 2
        offset = mem[1]
        return ('addc a,[hl+0%02xh]' % offset, new_pc)

    # 0x2d: 'ADDC A,#byte'
    elif mem[0] == 0x2d:
        new_pc = pc + 2
        imm8 = mem[1]
        return ('addc a,#0%02xh' % imm8, new_pc)

    # 0x30: 'XCH A,X' .. 0x37: 'XCH A,H'
    # except 0x31
    elif mem[0] in (0x30, 0x32, 0x33, 0x34, 0x35, 0x36, 0x37):
        new_pc = pc + 1
        reg = _reg(mem[0])
        return ("xch a,%s" % reg, new_pc)

    # 0x39: 'SUBC A,[HL+byte]'
    elif mem[0] == 0x39:
        new_pc = pc + 2
        offset = mem[1]
        return ('subc a,[hl+0%02xh]' % offset, new_pc)

    # 0x3d: 'SUBC A,#byte'
    elif mem[0] == 0x3d:
        new_pc = pc + 2
        imm8 = mem[1]
        return ('subc a,#0%02xh' % imm8, new_pc)

    # 0x3e: 'SUBC A,saddr'
    elif mem[0] == 0x3e:
        new_pc = pc + 2
        saddr = _saddr(mem[1])
        return ('subc a,0%04xh' % saddr, new_pc)

    # 0x3f: 'SUBC A,[HL]'
    elif mem[0] == 0x3f:
        new_pc = pc + 1
        return ('subc a,[hl]', new_pc)

    # 0x40: 'INC X' .. 0x47: 'INC H'
    elif mem[0] in (0x40, 0x41, 0x42, 0x43, 0x44, 0x45, 0x46, 0x47):
        new_pc = pc + 1
        reg = _reg(mem[0])
        return ("inc %s" % reg, new_pc)

    # 0x48: 'CMP A,!addr16'
    elif mem[0] == 0x48:
        new_pc = pc + 3
        addr16 = mem[1] + (mem[2] << 8)
        return ('cmp a,!0%04xh' % addr16, new_pc)

    # 0x49: 'CMP A,[HL+byte]'
    elif mem[0] == 0x49:
        new_pc = pc + 2
        offset = mem[1]
        return ('cmp a,[hl+0%02xh]' % offset, new_pc)

    # 0x4d: 'CMP A,#byte'
    elif mem[0] == 0x4d:
        new_pc = pc + 2
        imm8 = mem[1]
        return ('cmp a,#0%02xh' % imm8, new_pc)

    # 0x4e: 'CMP A,saddr
    elif mem[0] == 0x4e:
        new_pc = pc + 2
        saddr = _saddr(mem[1])
        return ('cmp a,0%04xh' % saddr, new_pc)

    # 0x4f: 'CMP A,[HL]'
    elif mem[0] == 0x4f:
        new_pc = pc + 1
        return ('cmp a,[hl]', new_pc)

    # 0x50: 'DEC X' .. 0x57: 'DEC H'
    elif mem[0] in (0x50, 0x51, 0x52, 0x53, 0x54, 0x55, 0x56, 0x57):
        new_pc = pc + 1
        reg = _reg(mem[0])
        return ("dec %s" % reg, new_pc)

    # 0x58: 'AND A,!addr16'
    elif mem[0] == 0x58:
        new_pc = pc + 3
        addr16 = mem[1] + (mem[2] << 8)
        return ('and a,!0%04xh' % addr16, new_pc)

    # 0x59: 'AND A,[HL+byte]'
    elif mem[0] == 0x59:
        new_pc = pc + 2
        offset = mem[1]
        return ('and a,[hl+0%02xh]' % offset, new_pc)

    # 0x5d: 'AND A,#byte'
    elif mem[0] == 0x5d:
        new_pc = pc + 2
        imm8 = mem[1]
        return ('and a,#0%02xh' % imm8, new_pc)

    # 0x5e: 'AND A,saddr'
    elif mem[0] == 0x5e:
        new_pc = pc + 2
        saddr = _saddr(mem[1])
        return ('and a,0%04xh' % saddr, new_pc)

    # 0x5f: 'AND A,[HL]'
    elif mem[0] == 0x5f:
        new_pc = pc + 1
        return ('and a,[hl]', new_pc)

    # 0x60: 'MOV A,X' .. 0x67: 'MOV A,H'
    # except 0x61
    elif mem[0] in (0x60, 0x62, 0x63, 0x64, 0x65, 0x66, 0x67):
        new_pc = pc + 1
        reg = _reg(mem[0])
        return ("mov a,%s" % reg, new_pc)

    # 0x68: 'OR A,!addr16'
    elif mem[0] == 0x68:
        new_pc = pc + 3
        addr16 = mem[1] + (mem[2] << 8)
        return ('or a,!0%04xh' % addr16, new_pc)

    # 0x69: 'OR A,[HL+byte]'
    elif mem[0] == 0x69:
        new_pc = pc + 2
        offset = mem[1]
        return ('or a,[hl+0%02xh]' % offset, new_pc)

    # 0x6d: 'OR A,#byte'
    elif mem[0] == 0x6d:
        new_pc = pc + 2
        imm8 = mem[1]
        return ('or a,#0%02xh' % imm8, new_pc)

    # 0x6e: 'OR A,saddr'
    elif mem[0] == 0x6e:
        new_pc = pc + 2
        saddr = _saddr(mem[1])
        return ('or a,0%04xh' % saddr, new_pc)

    # 0x7e: 'XOR A,saddr'
    elif mem[0] == 0x7e:
        new_pc = pc + 2
        saddr = _saddr(mem[1])
        return ('xor a,0%04xh' % saddr, new_pc)

    # 0x6f: 'OR A,[HL]'
    elif mem[0] == 0x6f:
        new_pc = pc + 1
        return ('or a,[hl]', new_pc)

    # 0x70: 'MOV X,A' .. 0x77: 'MOV H,A'
    # except 0x71
    elif mem[0] in (0x70, 0x72, 0x73, 0x74, 0x75, 0x76, 0x77):
        new_pc = pc + 1
        reg = _reg(mem[0])
        return ("mov %s,a" % reg, new_pc)

    # 0x78: 'XOR A,!addr16'
    elif mem[0] == 0x78:
        new_pc = pc + 3
        addr16 = mem[1] + (mem[2] << 8)
        return ('xor a,!0%04xh' % addr16, new_pc)

    # 0x79: 'XOR A,[HL+byte]'
    elif mem[0] == 0x79:
        new_pc = pc + 2
        offset = mem[1]
        return ('xor a,[hl+0%02xh]' % offset, new_pc)

    # 0x7d: 'XOR A,#byte'
    elif mem[0] == 0x7d:
        new_pc = pc + 2
        imm8 = mem[1]
        return ('xor a,#0%02xh' % imm8, new_pc)

    # 0x7f: 'XOR A,[HL]'
    elif mem[0] == 0x7f:
        new_pc = pc + 1
        return ('xor a,[hl]', new_pc)

    elif mem[0] in (0x80, 0x82, 0x84, 0x86):
        new_pc = pc + 1
        regpair = _regpair(mem[0])
        return ("incw %s" % regpair, new_pc)

    # 0x81: 'INC saddr'
    # INC 0fe20h                  ;81 20          saddr
    elif mem[0] == 0x81:
        new_pc = pc + 2
        saddr = _saddr(mem[1])
        return ('inc 0%04xh' % saddr, new_pc)

    # 0x83: 'XCH A,saddr'
    elif mem[0] == 0x83:
        new_pc = pc + 2
        saddr = _saddr(mem[1])
        return ('xch a,0%04xh' % saddr, new_pc)

    # 0x85: 'MOV A,[DE]'
    elif mem[0] == 0x85:
        new_pc = pc + 1
        return ('mov a,[de]', new_pc)

    # 0x87: 'MOV A,[HL]'
    elif mem[0] == 0x87:
        new_pc = pc + 1
        return ('mov a,[hl]', new_pc)

    # 0x88: 'ADD saddr,#byte'
    elif mem[0] == 0x88:
        new_pc = pc + 3
        saddr = _saddr(mem[1])
        imm8 = mem[2]
        return ('add 0%04xh,#0%02xh' % (saddr, imm8), new_pc)

    # MOVW AX,0fe20h              ;89 20          saddrp
    # MOVW AX,SP                  ;89 1C
    elif mem[0] == 0x89:
        new_pc = pc + 2
        saddrp = _saddrp(mem[1])
        if saddrp == 0xff1c:
            return ('movw ax,sp', new_pc)
        else:
            return ('movw ax,0%04xh' % saddrp, new_pc)

    # 0x8a: 'DBNZ C,$rel   '
    elif mem[0] == 0x8a:
        new_pc = pc + 2
        reldisp = mem[1]
        reltarget = _resolve_rel(new_pc, reldisp)
        return ('dbnz c,$0%04xh' % reltarget, new_pc)

    # 0x8b: 'DBNZ B,$rel   '
    elif mem[0] == 0x8b:
        new_pc = pc + 2
        reldisp = mem[1]
        reltarget = _resolve_rel(new_pc, reldisp)
        return ('dbnz b,$0%04xh' % reltarget, new_pc)

    # BT 0fe20h.0,$label8         ;8C 20 FD       saddr
    # BT PSW.0,$label9            ;8C 1E FD
    elif mem[0] in (0x8c, 0x9c, 0xac, 0xbc, 0xcc, 0xdc, 0xec, 0xfc):
        new_pc = pc + 3
        bit = _bit(mem[0])
        saddr = _saddr(mem[1])
        reldisp = mem[2]
        reltarget = _resolve_rel(new_pc, reldisp)
        if saddr == 0xff1e:
            return ('bt psw.%d,$0%04xh' % (bit, reltarget), new_pc)
        else:
            return ('bt 0%04xh.%d,$0%04xh' % (saddr, bit, reltarget), new_pc)

    # 0x8d: 'BC $rel'
    elif mem[0] == 0x8d:
        new_pc = pc + 2
        reldisp = mem[1]
        reltarget = _resolve_rel(new_pc, reldisp)
        return ('bc $0%04xh' % reltarget, new_pc)

    # 0x8e: 'MOV A,!addr16'
    elif mem[0] == 0x8e:
        new_pc = pc + 3
        addr16 = mem[1] + (mem[2] << 8)
        return ('mov a,!0%04xh' % addr16, new_pc)

    elif mem[0] == 0x8f:
        new_pc = pc + 1
        return ("reti", new_pc)

    elif mem[0] in (0x90, 0x92, 0x94, 0x96):
        new_pc = pc + 1
        regpair = _regpair(mem[0])
        return ("decw %s" % regpair, new_pc)

    # 0x91: 'DEC saddr'
    # DEC 0fe20h                  ;91 20          saddr
    elif mem[0] == 0x91:
        new_pc = pc + 2
        saddr = _saddr(mem[1])
        return ('dec 0%04xh' % saddr, new_pc)

    # 0x93: 'XCH A,sfr'
    elif mem[0] == 0x93:
        new_pc = pc + 2
        sfr = _sfr(mem[1])
        return ("xch a,0%04xh" % sfr, new_pc)

    # 0x95: MOV [DE],A
    elif mem[0] == 0x95:
        new_pc = pc + 1
        return ('mov [de],a', new_pc)

    # 0x97: 'MOV [HL],A'
    elif mem[0] == 0x97:
        new_pc = pc + 1
        return ('mov [hl],a', new_pc)

    # 0x98: 'SUB saddr,#byte'
    elif mem[0] == 0x98:
        new_pc = pc + 3
        saddr = _saddr(mem[1])
        imm8 = mem[2]
        return ('sub 0%04xh,#0%02xh' % (saddr, imm8), new_pc)

    # MOVW 0fe20h,AX              ;99 20          saddrp
    # MOVW SP,AX                  ;99 1C
    elif mem[0] == 0x99:
        new_pc = pc + 2
        saddrp = _saddrp(mem[1])
        if saddrp == 0xff1c:
            return ('movw sp,ax', new_pc)
        else:
            return ('movw 0%04xh,ax' % saddrp, new_pc)

    # 0x9a: 'CALL !addr16'
    elif mem[0] == 0x9a:
        new_pc = pc + 3
        addr16 = mem[1] + (mem[2] << 8)
        return ('call !0%04xh' % addr16, new_pc)

    # 0x9b: 'BR !addr16'
    elif mem[0] == 0x9b:
        new_pc = pc + 3
        addr16 = mem[1] + (mem[2] << 8)
        return ('br !0%04xh' % addr16, new_pc)

    # 0x9d: 'BNC $rel'
    elif mem[0] == 0x9d:
        new_pc = pc + 2
        reldisp = mem[1]
        reltarget = _resolve_rel(new_pc, reldisp)
        return ('bnc $0%04xh' % reltarget, new_pc)

    # 0x9e: 'MOV !addr16,A'
    elif mem[0] == 0x9e:
        new_pc = pc + 3
        addr16 = mem[1] + (mem[2] << 8)
        return ('mov !0%04xh,a' % addr16, new_pc)

    elif mem[0] == 0x9f:
        new_pc = pc + 1
        return ("retb", new_pc)

    elif mem[0] in (0xa0, 0xa1, 0xa2, 0xa3, 0xa4, 0xa5, 0xa6, 0xa7):
        new_pc = pc + 2
        reg = _reg(mem[0])
        byte = mem[1]
        return ("mov %s,#0%02xh" % (reg, byte), new_pc)

    # 0xa8: 'ADDC saddr,#byte'
    elif mem[0] == 0xa8:
        new_pc = pc + 3
        saddr = _saddr(mem[1])
        imm8 = mem[2]
        return ('addc 0%04xh,#0%02xh' % (saddr, imm8), new_pc)

    # 0xa9: 'MOVW AX,sfrp'
    elif mem[0] == 0xa9:
        new_pc = pc + 2
        sfrp = _sfrp(mem[1])
        return ("movw ax,0%04xh" % sfrp, new_pc)

    elif mem[0] == 0xaa:
        new_pc = pc + 1
        return ("mov a,[hl+c]", new_pc)

    elif mem[0] == 0xab:
        new_pc = pc + 1
        return ("mov a,[hl+b]", new_pc)

    # 0xad: 'BZ $rel   '
    elif mem[0] == 0xad:
        new_pc = pc + 2
        reldisp = mem[1]
        reltarget = _resolve_rel(new_pc, reldisp)
        return ('bz $0%04xh' % reltarget, new_pc)

    # 0xae: 'MOV A,[HL+byte]'
    elif mem[0] == 0xae:
        new_pc = pc + 2
        imm8 = mem[1]
        return ("mov a,[hl+0%02xh]" % imm8, new_pc)

    elif mem[0] == 0xaf:
        new_pc = pc + 1
        return ("ret", new_pc)

    elif mem[0] in (0xb0, 0xb2, 0xb4, 0xb6):
        new_pc = pc + 1
        regpair = _regpair(mem[0])
        return ("pop %s" % regpair, new_pc)

    elif mem[0] in (0xb1, 0xb3, 0xb5, 0xb7):
        new_pc = pc + 1
        regpair = _regpair(mem[0])
        return ("push %s" % regpair, new_pc)

    # 0xb8: 'SUBC saddr,#byte'
    elif mem[0] == 0xb8:
        new_pc = pc + 3
        saddr = _saddr(mem[1])
        imm8 = mem[2]
        return ('subc 0%04xh,#0%02xh' % (saddr, imm8), new_pc)

    # 0xb9: 'MOVW sfrp,AX'
    elif mem[0] == 0xb9:
        new_pc = pc + 2
        sfrp = _sfrp(mem[1])
        return ("movw 0%04xh,ax" % sfrp, new_pc)

    # 0xba: 'MOV [HL+C],A'
    # MOV [HL+C],A                ;BA
    elif mem[0] == 0xba:
        new_pc = pc + 1
        return ("mov [hl+c],a", new_pc)

    # MOV [HL+B],A                ;BB
    elif mem[0] == 0xbb:
        new_pc = pc + 1
        return ("mov [hl+b],a", new_pc)

    # 0xbd: 'BNZ $rel'
    elif mem[0] == 0xbd:
        new_pc = pc + 2
        reldisp = mem[1]
        reltarget = _resolve_rel(new_pc, reldisp)
        return ('bnz $0%04xh' % reltarget, new_pc)

    # 0xbe: 'MOV [HL+byte],A'
    elif mem[0] == 0xbe:
        new_pc = pc + 2
        imm8 = mem[1]
        return ("mov [hl+0%02xh],a" % imm8, new_pc)

    elif mem[0] == 0xbf:
        new_pc = pc + 1
        return ("brk", new_pc)

    elif mem[0] in (0xc2, 0xc4, 0xc6):
        new_pc = pc + 1
        regpair = _regpair(mem[0])
        return ("movw ax,%s" % regpair, new_pc)

    # 0xc8: 'CMP saddr,#byte'
    elif mem[0] == 0xc8:
        new_pc = pc + 3
        saddr = _saddr(mem[1])
        imm8 = mem[2]
        return ('cmp 0%04xh,#0%02xh' % (saddr, imm8), new_pc)

    # ADDW AX,#0abcdh             ;CA CD AB
    elif mem[0] == 0xca:
        new_pc = pc + 3
        imm16 = mem[1] + (mem[2] << 8)
        return ("addw ax,#0%04xh" % imm16, new_pc)

    # 0xce: 'XCH A,!addr16'
    elif mem[0] == 0xce:
        new_pc = pc + 3
        addr16 = mem[1] + (mem[2] << 8)
        return ('xch a,!0%04xh' % addr16, new_pc)

    elif mem[0] in (0xd2, 0xd4, 0xd6):
        new_pc = pc + 1
        regpair = _regpair(mem[0])
        return ("movw %s,ax" % regpair, new_pc)

    # 0xd8: 'AND saddr,#byte'
    elif mem[0] == 0xd8:
        new_pc = pc + 3
        saddr = _saddr(mem[1])
        imm8 = mem[2]
        return ('and 0%04xh,#0%02xh' % (saddr, imm8), new_pc)

    # SUBW AX,#0abcdh             ;DA CD AB
    elif mem[0] == 0xda:
        new_pc = pc + 3
        imm16 = mem[1] + (mem[2] << 8)
        return ("subw ax,#0%04xh" % imm16, new_pc)

    # 0xde: 'XCH A,[HL+byte]'
    elif mem[0] == 0xde:
        new_pc = pc + 2
        imm8 = mem[1]
        return ("xch a,[hl+0%02xh]" % imm8, new_pc)

    elif mem[0] in (0xe2, 0xe4, 0xe6):
        new_pc = pc + 1
        regpair = _regpair(mem[0])
        return ("xchw ax,%s" % regpair, new_pc)

    # 0xe8: 'OR saddr,#byte'
    elif mem[0] == 0xe8:
        new_pc = pc + 3
        saddr = _saddr(mem[1])
        imm8 = mem[2]
        return ('or 0%04xh,#0%02xh' % (saddr, imm8), new_pc)

    # CMPW AX,#0abcdh             ;EA CD AB
    elif mem[0] == 0xea:
        new_pc = pc + 3
        imm16 = mem[1] + (mem[2] << 8)
        return ("cmpw ax,#0%04xh" % imm16, new_pc)

    # MOVW 0fe20h,#0abcdh         ;EE 20 CD AB    saddrp
    # MOVW SP,#0abcdh             ;EE 1C CD AB
    elif mem[0] == 0xee:
        new_pc = pc + 4
        saddrp = _saddrp(mem[1])
        imm16 = mem[2] + (mem[3] << 8)
        if saddrp == 0xff1c:
            return ('movw sp,#0%04xh' % imm16, new_pc)
        else:
            return ('movw 0%04xh,#0%04xh' % (saddrp, imm16), new_pc)

    # mov a,0fe20h                ;F0 20          saddr
    # mov a,psw                   ;F0 1E
    elif mem[0] == 0xf0:
        new_pc = pc + 2
        saddr = _saddr(mem[1])
        if saddr == 0xff1e:
            return ('mov a,psw', new_pc)
        else:
            return ('mov a,0%04xh' % saddr, new_pc)

    # MOV 0fe20h,A                ;F2 20          saddr
    # MOV PSW,A                   ;F2 1E
    elif mem[0] == 0xf2:
        new_pc = pc + 2
        saddr = _saddr(mem[1])
        if saddr == 0xff1e:
            return ('mov psw,a', new_pc)
        else:
            return ('mov 0%04xh,a' % saddr, new_pc)

    # 0xf4: 'MOV A,sfr'
    elif mem[0] == 0xf4:
        new_pc = pc + 2
        sfr = _sfr(mem[1])
        return ("mov a,0%04xh" % sfr, new_pc)

    # 0xf6: 'MOV sfr,A'
    elif mem[0] == 0xf6:
        new_pc = pc + 2
        sfr = _sfr(mem[1])
        return ("mov 0%04xh,a" % sfr, new_pc)

    # 0xf8: 'XOR saddr,#byte'
    elif mem[0] == 0xf8:
        new_pc = pc + 3
        saddr = _saddr(mem[1])
        imm8 = mem[2]
        return ('xor 0%04xh,#0%02xh' % (saddr, imm8),new_pc)

    # 0xfa: 'BR $rel'
    elif mem[0] == 0xfa:
        new_pc = pc + 2
        reldisp = mem[1]
        reltarget = _resolve_rel(new_pc, reldisp)
        return ('br $0%04xh' % reltarget, new_pc)

    # MOVW 0fffeh,#0abcdh         ;FE FE CD AB    sfrp
    elif mem[0] == 0xfe:
        new_pc = pc + 4
        sfrp = _sfrp(mem[1])
        imm16 = mem[2] + (mem[3] << 8)
        return ('movw 0%04xh,#0%04xh' % (sfrp, imm16), new_pc)

    elif mem[0] == 0x31:
        if mem[1] == 0x80:
            new_pc = pc + 2
            return ('rol4 [hl]', new_pc)
        elif mem[1] == 0x82:
            new_pc = pc + 2
            return ('divuw c', new_pc)
        elif mem[1] == 0x88:
            new_pc = pc + 2
            return ('mulu x', new_pc)
        elif mem[1] == 0x90:
            new_pc = pc + 2
            return ('ror4 [hl]', new_pc)
        elif mem[1] == 0x98:
            new_pc = pc + 2
            return ('br ax', new_pc)
        elif (mem[1] >> 4) < 0x09 and (mem[1] & 0x0f) in (0x0a, 0x0b):
            new_pc = pc + 2
            inst = mem[1] >> 4
            instname = ('add', 'sub', 'addc', 'subc',
                        'cmp', 'and', 'or', 'xor', 'xch')[inst]

            mode = mem[1] & 0x0f
            modename = "a,[hl+b]" if mode == 0x0b else "a,[hl+c]"

            return ("%s %s" % (instname, modename), new_pc)
        elif (mem[1] >> 4) < 0x08 and (mem[1] & 0x0f) in (0x0d, 0x0e, 0x0f):
            new_pc = pc + 3

            inst = (mem[1] & 0x0f) - 0x0d
            instname = ('btclr', 'bt', 'bf')[inst]

            bit = mem[1] >> 4
            reldisp = mem[2]
            reltarget = _resolve_rel(new_pc, reldisp)

            return ("%s a.%d,$0%04xh" % (instname, bit, reltarget), new_pc)
        elif (mem[1] >> 4) < 0x08 and (mem[1] & 0x0f) in (0x01, 0x03):
            new_pc = pc + 4

            instname = 'btclr' if (mem[1] & 0x0f) == 0x01 else 'bf'
            bit = mem[1] >> 4
            saddr = _saddr(mem[2])
            reldisp = mem[3]
            reltarget = _resolve_rel(new_pc, reldisp)

            if saddr == 0xff1e:
                return ("%s psw.%d,$0%04xh" % (instname, bit, reltarget), new_pc)
            else:
                return ("%s 0%04xh.%d,$0%04xh" % (instname, saddr, bit, reltarget), new_pc)
        elif (mem[1] >> 4) < 0x08 and (mem[1] & 0x0f) in (0x5, 0x6, 0x7):
            new_pc = pc + 4

            inst = (mem[1] & 0x0f) - 0x05
            instname = ('btclr', 'bt', 'bf')[inst]

            bit = mem[1] >> 4
            sfr = _sfr(mem[2])
            reldisp = mem[3]
            reltarget = _resolve_rel(new_pc, reldisp)

            return ("%s 0%04xh.%d,$0%04xh" % (instname, sfr, bit, reltarget), new_pc)
        elif (mem[1] >> 4) in range(0x8, 0xf+1) and (mem[1] & 0x0f) in (0x5, 0x6, 0x7):
            new_pc = pc + 3

            inst = (mem[1] & 0x0f) - 0x05
            instname = ('btclr', 'bt', 'bf')[inst]

            bit = (mem[1] >> 4) - 0x08
            reldisp = mem[2]
            reltarget = _resolve_rel(new_pc, reldisp)

            return ("%s [hl].%d,$0%04xh" % (instname, bit, reltarget), new_pc)
        else:
            raise NotImplementedError("31 %02x" % mem[1])

    elif mem[0] == 0x61:
        new_pc = pc + 2
        bit = _bit(mem[1])
        reg = _reg(mem[1])
        if mem[1] == 0x80:
            return ('adjba', new_pc)
        elif mem[1] == 0x90:
            return ('adjbs', new_pc)
        elif mem[1] == 0xd0:
            return ('sel rb0', new_pc)
        elif mem[1] == 0xd8:
            return ('sel rb1', new_pc)
        elif mem[1] == 0xf0:
            return ('sel rb2', new_pc)
        elif mem[1] == 0xf8:
            return ('sel rb3', new_pc)
        elif mem[1] in range(0x00, 0x80):
            inst = mem[1] >> 4
            instname = ('add', 'sub', 'addc', 'subc',
                        'cmp', 'and', 'or', 'xor')[inst]

            mode = mem[1] & 0x0f
            modetpl = "%s,a" if mode in range(0x00, 0x08) else "a,%s"

            template = instname + " " + modetpl
            return (template % reg), new_pc
        elif mem[1] in (0x89, 0x99, 0xa9, 0xb9, 0xc9, 0xd9, 0xe9, 0xf9):
            return ('mov1 a.%d,cy' % bit, new_pc)
        elif mem[1] in (0x8a, 0x9a, 0xaa, 0xba, 0xca, 0xda, 0xea, 0xfa):
            return ('set1 a.%d' % bit, new_pc)
        elif mem[1] in (0x8b, 0x9b, 0xab, 0xbb, 0xcb, 0xdb, 0xeb, 0xfb):
            return ('clr1 a.%d' % bit, new_pc)
        elif mem[1] in (0x8c, 0x9c, 0xac, 0xbc, 0xcc, 0xdc, 0xec, 0xfc):
            return ('mov1 cy,a.%d' % bit, new_pc)
        elif mem[1] in (0x8d, 0x9d, 0xad, 0xbd, 0xcd, 0xdd, 0xed, 0xfd):
            return ('and1 cy,a.%d' % bit, new_pc)
        elif mem[1] in (0x8e, 0x9e, 0xae, 0xbe, 0xce, 0xde, 0xee, 0xfe):
            return ('or1 cy,a.%d' % bit, new_pc)
        elif mem[1] in (0x8f, 0x9f, 0xaf, 0xbf, 0xcf, 0xdf, 0xef, 0xff):
            return ('xor1 cy,a.%d' % bit, new_pc)
        else:
            raise NotImplementedError("61 %02x" % mem[1])

    elif mem[0] == 0x71:
        if mem[1] == 0x00:
            new_pc = pc + 2
            return ('stop', new_pc)
        elif mem[1] == 0x10:
            new_pc = pc + 2
            return ('halt', new_pc)
        elif mem[1] in (0x82, 0x92, 0xa2, 0xb2, 0xc2, 0xd2, 0xe2, 0xf2):
            new_pc = pc + 2
            bit = (mem[1] >> 4) - 8
            return ('set1 [hl].%d' % bit, new_pc)
        elif mem[1] in (0x83, 0x93, 0xa3, 0xb3, 0xc3, 0xd3, 0xe3, 0xf3):
            new_pc = pc + 2
            bit = (mem[1] >> 4) - 8
            return ('clr1 [hl].%d' % bit, new_pc)
        elif (mem[1] >> 4) in range(8, 0x0f+1) and (mem[1] & 0x0f) in (0x4, 0x5, 0x6, 0x7):
            new_pc = pc + 2
            bit = (mem[1] >> 4) - 8
            inst = (mem[1] & 0x0f) - 4
            instname = ('mov1', 'and1', 'or1', 'xor1')[inst]
            return ('%s cy,[hl].%d' % (instname, bit), new_pc)
        elif (mem[1] >> 4) in range(8, 0x0f+1) and (mem[1] & 0x0f) == 1:
            new_pc = pc + 2
            bit = (mem[1] >> 4) - 8
            return ('mov1 [hl].%d,cy' % bit, new_pc)
        elif (mem[1] >> 4) < 8 and (mem[1] & 0x0f) in (0x0a, 0x0b):
            new_pc = pc + 3
            bit = (mem[1] >> 4)
            instname = 'set1' if (mem[1] & 0x0f) == 0x0a else 'clr1'
            sfr = _sfr(mem[2])
            return ('%s 0%04xh.%d' % (instname, sfr, bit), new_pc)
        elif (mem[1] >> 4) < 8 and (mem[1] & 0x0f) == 0x09:
            new_pc = pc + 3
            bit = (mem[1] >> 4)
            sfr = _sfr(mem[2])
            return ('mov1 0%04xh.%d,cy' % (sfr, bit), new_pc)
        elif (mem[1] >> 4) < 8 and (mem[1] & 0x0f) in range(0x0c, 0x0f+1):
            new_pc = pc + 3
            bit = (mem[1] >> 4)
            sfr = _sfr(mem[2])
            inst = (mem[1] & 0x0f) - 0x0c
            instname = ('mov1', 'and1', 'or1', 'xor1')[inst]
            return ('%s cy,0%04xh.%d' % (instname, sfr, bit), new_pc)
        elif (mem[1] >> 4) < 8 and (mem[1] & 0x0f) == 1:
            new_pc = pc + 3
            bit = (mem[1] >> 4)
            saddr = _saddr(mem[2])
            if saddr == 0xff1e:
                return ('mov1 psw.%d,cy' % bit, new_pc)
            else:
                return ('mov1 0%04xh.%d,cy' % (saddr, bit), new_pc)
        elif (mem[1] >> 4) < 8 and (mem[1] & 0x0f) in (0x4, 0x5, 0x6, 0x7):
            new_pc = pc + 3
            bit = (mem[1] >> 4)
            inst = (mem[1] & 0x0f) - 4
            instname = ('mov1', 'and1', 'or1', 'xor1')[inst]
            saddr = _saddr(mem[2])
            if saddr == 0xff1e:
                return ('%s cy,psw.%d' % (instname, bit), new_pc)
            else:
                return ('%s cy,0%04xh.%d' % (instname, saddr, bit), new_pc)
        else:
            raise NotImplementedError("71 %02x" % mem[1])

    else:
        new_pc = pc + 1
        return ("illegal 0x%02x" % mem[0], new_pc)


def _reg(opcode):
    r = opcode & 0b111
    return ('x', 'a', 'c', 'b', 'e', 'd', 'l', 'h')[r]

def _regpair(opcode):
    rp = (opcode >> 1) & 0b11
    return ('ax', 'bc', 'de', 'hl')[rp]

def _bit(opcode):
    return (opcode & 0b01110000) >> 4

def _saddr(operand):
    saddr = 0xfe00 + operand
    if operand < 0x20:
        saddr += 0x100
    return saddr
_saddrp = _saddr

def _sfr(operand):
    sfr = 0xff00 + operand
    return sfr
_sfrp = _sfr

def _resolve_rel(pc, displacement):
    if displacement & 0x80:
        displacement = -((displacement ^ 0xFF) + 1)
    return (pc + displacement) & 0xffff
