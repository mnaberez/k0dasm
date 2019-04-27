
def disassemble(mem, pc):
    # nop                         ;00
    if mem[pc+0] == 0x00:
        inst = Instruction("nop",
                           opcode=mem[pc+0],
                           operands=(),
                           flow_type=FlowTypes.Continue,)
        return inst

    # not1 cy                     ;01
    elif mem[pc+0] == 0x01:
        inst = Instruction('not1 cy',
                           opcode=mem[pc+0],
                           operands=(),
                           flow_type=FlowTypes.Continue,)
        return inst

    # movw ax,0fe20h              ;02 CE AB       addr16p
    elif mem[pc+0] == 0x02:
        addr16p = _addr16p(mem[pc+1], mem[pc+2])
        inst = Instruction('movw ax,{addr16p}',
                           opcode=mem[pc+0],
                           operands=(mem[pc+1], mem[pc+2]),
                           addr16p=addr16p,
                           flow_type=FlowTypes.Continue,)
        return inst

    # MOVW 0fe20h,AX              ;03 CE AB       addr16p
    elif mem[pc+0] == 0x03:
        addr16p = _addr16p(mem[pc+1], mem[pc+2])
        inst = Instruction('movw {addr16p},ax',
                           opcode=mem[pc+0],
                           operands=(mem[pc+1], mem[pc+2]),
                           addr16p=addr16p,
                           flow_type=FlowTypes.Continue,)
        return inst

    # DBNZ 0fe20h,$label0         ;04 20 FD       saddr
    elif mem[pc+0] == 0x04:
        saddr = _saddr(mem[pc+1])
        reldisp = mem[pc+2]
        reltarget = _resolve_rel(pc + 3, reldisp)
        inst = Instruction('dbnz {saddr},{reltarget}',
                           opcode=mem[pc+0],
                           operands=(mem[pc+1], mem[pc+2]),
                           saddr=saddr,
                           reltarget=reltarget,
                           flow_type=FlowTypes.ConditionalJump,)
        return inst

    # XCH A,[DE]
    elif mem[pc+0] == 0x05:
        inst = Instruction("xch a,[de]",
                           opcode=mem[pc+0],
                           operands=(),
                           flow_type=FlowTypes.Continue,)
        return inst

    # 'XCH A,[HL]'
    elif mem[pc+0] == 0x07:
        new_pc = pc + 1
        inst = Instruction('xch a,[hl]',
                           opcode=mem[pc+0],
                           operands=(),
                           flow_type=FlowTypes.Continue,)
        return inst

    # ADD A,!0abcdh               ;08 CD AB
    elif mem[pc+0] == 0x08:
        addr16 = mem[pc+1] + (mem[pc+2] << 8)
        inst = Instruction("add a,{addr16}",
                           opcode=mem[pc+0],
                           operands=(mem[pc+1], mem[pc+2]),
                           addr16=addr16,
                           flow_type=FlowTypes.Continue,)
        return inst

    # ADD A,[HL+0abh]             ;09 AB
    elif mem[pc+0] == 0x09:
        offset = mem[pc+1]
        inst = Instruction("add a,[hl+{offset}]",
                           opcode=mem[pc+0],
                           operands=(mem[pc+1],),
                           flow_type=FlowTypes.Continue,
                           offset=offset)
        return inst

    # SET1 0fe20h.7               ;7A 20          saddr
    # SET1 PSW.7                  ;7A 1E
    # EI                          ;7A 1E          alias for SET1 PSW.7
    elif mem[pc+0] in (0x0a, 0x1a, 0x2a, 0x3a, 0x4a, 0x5a, 0x6a, 0x7a):
        bit = _bit(mem[pc+0])
        saddr = _saddr(mem[pc+1])
        if saddr == 0xff1e:
            if bit == 7:
                inst = Instruction("ei",
                                   opcode=mem[pc+0],
                                   operands=(mem[pc+1],),
                                   flow_type=FlowTypes.Continue,)
                return inst # alias for set1 psw.7
            else:
                inst = Instruction("set1 psw.{bit}",
                                   opcode=mem[pc+0],
                                   operands=(mem[pc+1],),
                                   bit=bit,
                                   flow_type=FlowTypes.Continue,)
                return inst
        else:
            inst = Instruction('set1 {saddr}.{bit}',
                                opcode=mem[pc+0],
                                operands=(mem[pc+1],),
                                saddr=saddr,
                                bit=bit,
                                flow_type=FlowTypes.Continue,)
            return inst

    # CLR1 0fe20h.7               ;7B 20          saddr
    # CLR1 PSW.7                  ;7B 1E
    # DI                          ;7B 1E          alias for CLR1 PSW.7
    elif mem[pc+0] in (0x0b, 0x1b, 0x2b, 0x3b, 0x4b, 0x5b, 0x6b, 0x7b):
        bit = _bit(mem[pc+0])
        saddr = _saddr(mem[pc+1])
        if saddr == 0xff1e:
            if bit == 7:
                inst = Instruction("di",
                                   opcode=mem[pc+0],
                                   operands=(mem[pc+1],),
                                   flow_type=FlowTypes.Continue,)
                return inst # alias for clr1 psw.7
            else:
                inst = Instruction("clr1 psw.{bit}",
                                   opcode=mem[pc+0],
                                   operands=(mem[pc+1],),
                                   bit=bit,
                                   flow_type=FlowTypes.Continue,)
                return inst
        else:
            inst = Instruction("clr1 {saddr}.{bit}",
                               opcode=mem[pc+0],
                               operands=(mem[pc+1],),
                               saddr=saddr,
                               bit=bit,
                               flow_type=FlowTypes.Continue,)
            return inst

    # callt [0040H]               ;C1
    # CALLT [{addr5}]             0b11ttttt1                            1
    elif (mem[pc+0] & 0b11000001) == 0b11000001:
        # parse vector address from opcode
        offset = (mem[pc+0] & 0b00111110) >> 1
        addr5 = 0x40 + (offset * 2)

        # read address in vector
        target_low, target_high = mem[addr5], mem[addr5+1]
        target = (target_high << 8) + target_low

        inst = Instruction("callt {addr5}",
                           opcode=mem[pc+0],
                           operands=(),
                           addr5=addr5,
                           addr5target=target,
                           flow_type=FlowTypes.SubroutineCall,)
        return inst

    # callf !0800h                ;0C 00          0c = callf 0800h-08ffh
    # CALLF !{addr11}             0b0xxx1100         0bffffffff         2
    elif (mem[pc+0] & 0b10001111) == 0b00001100:
        base = 0x0800 + ((mem[pc+0] >> 4) << 8)
        addr11 = base + mem[pc+1]
        inst = Instruction("callf {addr11}",
                           opcode=mem[pc+0],
                           operands=(mem[pc+1],),
                           addr11=addr11,
                           flow_type=FlowTypes.SubroutineCall,)
        return inst

    # 0x0d: 'ADD A,#byte'
    # ADD A,#0abh                 ;0D AB
    elif mem[pc+0] == 0x0d:
        imm8 = mem[pc+1]
        inst = Instruction('add a,{imm8}',
                           opcode=mem[pc+0],
                           operands=(mem[pc+1],),
                           imm8=imm8,
                           flow_type=FlowTypes.Continue,)
        return inst

    # 0x0e: 'ADD A,saddr'
    # ADD A,0fe20h                ;0E 20          saddr
    elif mem[pc+0] == 0x0e:
        saddr = _saddr(mem[pc+1])
        inst = Instruction('add a,{saddr}',
                           opcode=mem[pc+0],
                           operands=(mem[pc+1],),
                           saddr=saddr,
                           flow_type=FlowTypes.Continue,)
        return inst

    # 0x0f: 'ADD A,[HL]'
    # ADD A,[HL]                  ;0F
    elif mem[pc+0] == 0x0f:
        inst = Instruction('add a,[hl]',
                           opcode=mem[pc+0],
                           operands=(),
                           flow_type=FlowTypes.Continue,)
        return inst

    # MOVW {regpair},#word        0b00010pp0                            3
    # MOVW AX,#0abcdh             ;10 CD AB
    # MOVW BC,#0abcdh             ;12 CD AB
    # MOVW DE,#0abcdh             ;14 CD AB
    # MOVW HL,#0abcdh             ;16 CD AB
    elif (mem[pc+0] & 0b11111001) == 0b00010000:
        regpair = _regpair(mem[pc+0])
        imm16 = mem[pc+1] + (mem[pc+2] << 8)
        inst = Instruction("movw {regpair},{imm16}",
                           opcode=mem[pc+0],
                           operands=(mem[pc+1], mem[pc+2]),
                           regpair=regpair,
                           imm16=imm16,
                           flow_type=FlowTypes.Continue,)
        return inst

    # MOV 0fe20h,#0abh            ;11 20 AB       saddr
    # MOV PSW,#0abh               ;11 1E AB
    elif mem[pc+0] == 0x11:
        saddr = _saddr(mem[pc+1])
        imm8 = mem[pc+2]
        if saddr == 0xff1e:
            inst = Instruction('mov psw,{imm8}',
                               opcode=mem[pc+0],
                               operands=(mem[pc+1], mem[pc+2]),
                               imm8=imm8,
                               flow_type=FlowTypes.Continue,)
            return inst
        else:
            inst = Instruction('mov {saddr},{imm8}',
                               opcode=mem[pc+0],
                               operands=(mem[pc+1], mem[pc+2]),
                               saddr=saddr,
                               imm8=imm8,
                               flow_type=FlowTypes.Continue,)
            return inst

    # 0x13: 'MOV sfr,#byte'
    elif mem[pc+0] == 0x13:
        sfr = _sfr(mem[pc+1])
        imm8 = mem[pc+2]
        inst = Instruction("mov {sfr},{imm8}",
                           opcode=mem[pc+0],
                           operands=(mem[pc+1], mem[pc+2]),
                           sfr=sfr,
                           imm8=imm8,
                           flow_type=FlowTypes.Continue,)
        return inst

    # 0x18: 'SUB A,!addr16'
    elif mem[pc+0] == 0x18:
        addr16 = mem[pc+1] + (mem[pc+2] << 8)
        inst = Instruction('sub a,{addr16}',
                           opcode=mem[pc+0],
                           operands=(mem[pc+1], mem[pc+2]),
                           addr16=addr16,
                           flow_type=FlowTypes.Continue,)
        return inst

    # 0x19: 'SUB A,[HL+byte]'
    elif mem[pc+0] == 0x19:
        offset = mem[pc+1]
        inst = Instruction('sub a,[hl+{offset}]',
                           opcode=mem[pc+0],
                           operands=(mem[pc+1],),
                           offset=offset,
                           flow_type=FlowTypes.Continue,)
        return inst

    # 0x1d: 'SUB A,#byte'
    elif mem[pc+0] == 0x1d:
        imm8 = mem[pc+1]
        inst = Instruction('sub a,{imm8}',
                           opcode=mem[pc+0],
                           operands=(mem[pc+1],),
                           imm8=imm8,
                           flow_type=FlowTypes.Continue,)
        return inst

    elif mem[pc+0] == 0x1e:
        saddr = _saddr(mem[pc+1])
        inst = Instruction('sub a,{saddr}',
                           opcode=mem[pc+0],
                           operands=(mem[pc+1],),
                           saddr=saddr,
                           flow_type=FlowTypes.Continue,)
        return inst

    elif mem[pc+0] == 0x1f:
        new_pc = pc + 1
        inst = Instruction('sub a,[hl]',
                           opcode=mem[pc+0],
                           operands=(),
                           flow_type=FlowTypes.Continue,)
        return inst

    # 0x20: 'SET1 CY'
    elif mem[pc+0] == 0x20:
        inst = Instruction('set1 cy',
                           opcode=mem[pc+0],
                           operands=(),
                           flow_type=FlowTypes.Continue,)
        return inst

    # 0x21: 'CLR1 CY'
    elif mem[pc+0] == 0x21:
        inst = Instruction('clr1 cy',
                           opcode=mem[pc+0],
                           operands=(),
                           flow_type=FlowTypes.Continue,)
        return inst

    # 0x22: 'PUSH PSW'
    elif mem[pc+0] == 0x22:
        inst = Instruction('push psw',
                           opcode=mem[pc+0],
                           operands=(),
                           flow_type=FlowTypes.Continue,)
        return inst

    # 0x23: 'POP PSW'
    elif mem[pc+0] == 0x23:
        inst = Instruction('pop psw',
                           opcode=mem[pc+0],
                           operands=(),
                           flow_type=FlowTypes.Continue,)
        return inst

    # 0x24: 'ROR A,1'
    elif mem[pc+0] == 0x24:
        inst = Instruction('ror a,1',
                           opcode=mem[pc+0],
                           operands=(),
                           flow_type=FlowTypes.Continue,)
        return inst

    # 0x25: 'RORC A,1'
    elif mem[pc+0] == 0x25:
        inst = Instruction('rorc a,1',
                           opcode=mem[pc+0],
                           operands=(),
                           flow_type=FlowTypes.Continue,)
        return inst

    # 0x26: 'ROL A,1'
    elif mem[pc+0] == 0x26:
        inst = Instruction('rol a,1',
                           opcode=mem[pc+0],
                           operands=(),
                           flow_type=FlowTypes.Continue,)
        return inst

    # 0x27: 'ROLC A,1'
    elif mem[pc+0] == 0x27:
        inst = Instruction('rolc a,1',
                           opcode=mem[pc+0],
                           operands=(),
                           flow_type=FlowTypes.Continue,)
        return inst

    # 0x28: 'ADDC A,!addr16'
    elif mem[pc+0] == 0x28:
        addr16 = mem[pc+1] + (mem[pc+2] << 8)
        inst = Instruction('addc a,{addr16}',
                           opcode=mem[pc+0],
                           operands=(mem[pc+1], mem[pc+2]),
                           addr16=addr16,
                           flow_type=FlowTypes.Continue,)
        return inst

    # 0x38: 'SUBC A,!addr16'
    elif mem[pc+0] == 0x38:
        addr16 = mem[pc+1] + (mem[pc+2] << 8)
        inst = Instruction('subc a,{addr16}',
                           opcode=mem[pc+0],
                           operands=(mem[pc+1], mem[pc+2]),
                           addr16=addr16,
                           flow_type=FlowTypes.Continue,)
        return inst

    # 0x2e: 'ADDC A,saddr'
    elif mem[pc+0] == 0x2e:
        saddr = _saddr(mem[pc+1])
        inst = Instruction('addc a,{saddr}',
                           opcode=mem[pc+0],
                           operands=(mem[pc+1],),
                           saddr=saddr,
                           flow_type=FlowTypes.Continue,)
        return inst

    # 0x27: 'ADDC A,[HL]'
    elif mem[pc+0] == 0x2f:
        inst = Instruction('addc a,[hl]',
                           opcode=mem[pc+0],
                           operands=(mem[pc+1],),
                           flow_type=FlowTypes.Continue,)
        return inst

    # ADDC A,[HL+0abh]            ;29 AB
    elif mem[pc+0] == 0x29:
        offset = mem[pc+1]
        inst = Instruction('addc a,[hl+{offset}]',
                           opcode=mem[pc+0],
                           operands=(mem[pc+1],),
                           offset=offset,
                           flow_type=FlowTypes.Continue,)
        return inst

    # 0x2d: 'ADDC A,#byte'
    elif mem[pc+0] == 0x2d:
        imm8 = mem[pc+1]
        inst = Instruction('addc a,{imm8}',
                           opcode=mem[pc+0],
                           operands=(mem[pc+1],),
                           imm8=imm8,
                           flow_type=FlowTypes.Continue,)
        return inst

    # 0x30: 'XCH A,X' .. 0x37: 'XCH A,H'
    # except 0x31
    elif mem[pc+0] in (0x30, 0x32, 0x33, 0x34, 0x35, 0x36, 0x37):
        reg = _reg(mem[pc+0])
        inst = Instruction("xch a,{reg}",
                           opcode=mem[pc+0],
                           operands=(),
                           reg=reg,
                           flow_type=FlowTypes.Continue,)
        return inst

    # 0x39: 'SUBC A,[HL+byte]'
    elif mem[pc+0] == 0x39:
        offset = mem[pc+1]
        inst = Instruction('subc a,[hl+{offset}]',
                           opcode=mem[pc+0],
                           operands=(mem[pc+1],),
                           offset=offset,
                           flow_type=FlowTypes.Continue,)
        return inst

    # 0x3d: 'SUBC A,#byte'
    elif mem[pc+0] == 0x3d:
        imm8 = mem[pc+1]
        inst = Instruction('subc a,{imm8}',
                           opcode=mem[pc+0],
                           operands=(mem[pc+1],),
                           imm8=imm8,
                           flow_type=FlowTypes.Continue,)
        return inst

    # 0x3e: 'SUBC A,saddr'
    elif mem[pc+0] == 0x3e:
        saddr = _saddr(mem[pc+1])
        inst = Instruction('subc a,{saddr}',
                           opcode=mem[pc+0],
                           operands=(mem[pc+1],),
                           saddr=saddr,
                           flow_type=FlowTypes.Continue,)
        return inst

    # 0x3f: 'SUBC A,[HL]'
    elif mem[pc+0] == 0x3f:
        inst = Instruction('subc a,[hl]',
                           opcode=mem[pc+0],
                           operands=(),
                           flow_type=FlowTypes.Continue,)
        return inst

    # 0x40: 'INC X' .. 0x47: 'INC H'
    elif mem[pc+0] in (0x40, 0x41, 0x42, 0x43, 0x44, 0x45, 0x46, 0x47):
        reg = _reg(mem[pc+0])
        inst = Instruction("inc {reg}",
                           opcode=mem[pc+0],
                           operands=(),
                           reg=reg,
                           flow_type=FlowTypes.Continue,)
        return inst

    # 0x48: 'CMP A,!addr16'
    elif mem[pc+0] == 0x48:
        addr16 = mem[pc+1] + (mem[pc+2] << 8)
        inst = Instruction('cmp a,{addr16}',
                           opcode=mem[pc+0],
                           operands=(mem[pc+1], mem[pc+2]),
                           addr16=addr16,
                           flow_type=FlowTypes.Continue,)
        return inst

    # 0x49: 'CMP A,[HL+byte]'
    elif mem[pc+0] == 0x49:
        offset = mem[pc+1]
        inst = Instruction('cmp a,[hl+{offset}]',
                           opcode=mem[pc+0],
                           operands=(mem[pc+1],),
                           offset=offset,
                           flow_type=FlowTypes.Continue,)
        return inst

    # 0x4d: 'CMP A,#byte'
    elif mem[pc+0] == 0x4d:
        imm8 = mem[pc+1]
        inst = Instruction('cmp a,{imm8}',
                           opcode=mem[pc+0],
                           operands=(mem[pc+1],),
                           imm8=imm8,
                           flow_type=FlowTypes.Continue,)
        return inst

    # 0x4e: 'CMP A,saddr
    elif mem[pc+0] == 0x4e:
        saddr = _saddr(mem[pc+1])
        inst = Instruction('cmp a,{saddr}',
                           opcode=mem[pc+0],
                           operands=(mem[pc+1],),
                           saddr=saddr,
                           flow_type=FlowTypes.Continue,)
        return inst

    # 0x4f: 'CMP A,[HL]'
    elif mem[pc+0] == 0x4f:
        inst = Instruction('cmp a,[hl]',
                           opcode=mem[pc+0],
                           operands=(),
                           flow_type=FlowTypes.Continue,)
        return inst

    # 0x50: 'DEC X' .. 0x57: 'DEC H'
    elif mem[pc+0] in (0x50, 0x51, 0x52, 0x53, 0x54, 0x55, 0x56, 0x57):
        reg = _reg(mem[pc+0])
        inst = Instruction("dec {reg}",
                           opcode=mem[pc+0],
                           operands=(),
                           reg=reg,
                           flow_type=FlowTypes.Continue,)
        return inst

    # 0x58: 'AND A,!addr16'
    elif mem[pc+0] == 0x58:
        addr16 = mem[pc+1] + (mem[pc+2] << 8)
        inst = Instruction('and a,{addr16}',
                           opcode=mem[pc+0],
                           operands=(mem[pc+1], mem[pc+2]),
                           addr16=addr16,
                           flow_type=FlowTypes.Continue,)
        return inst

    # 0x59: 'AND A,[HL+byte]'
    elif mem[pc+0] == 0x59:
        offset = mem[pc+1]
        inst = Instruction('and a,[hl+{offset}]',
                           opcode=mem[pc+0],
                           operands=(mem[pc+1],),
                           offset=offset,
                           flow_type=FlowTypes.Continue,)
        return inst

    # 0x5d: 'AND A,#byte'
    elif mem[pc+0] == 0x5d:
        imm8 = mem[pc+1]
        inst = Instruction('and a,{imm8}',
                           opcode=mem[pc+0],
                           operands=(mem[pc+1],),
                           imm8=imm8,
                           flow_type=FlowTypes.Continue,)
        return inst

    # 0x5e: 'AND A,saddr'
    elif mem[pc+0] == 0x5e:
        saddr = _saddr(mem[pc+1])
        inst = Instruction('and a,{saddr}',
                           opcode=mem[pc+0],
                           operands=(mem[pc+1],),
                           saddr=saddr,
                           flow_type=FlowTypes.Continue,)
        return inst

    # 0x5f: 'AND A,[HL]'
    elif mem[pc+0] == 0x5f:
        inst = Instruction('and a,[hl]',
                           opcode=mem[pc+0],
                           operands=(),
                           flow_type=FlowTypes.Continue,)
        return inst

    # 0x60: 'MOV A,X' .. 0x67: 'MOV A,H'
    # except 0x61
    elif mem[pc+0] in (0x60, 0x62, 0x63, 0x64, 0x65, 0x66, 0x67):
        reg = _reg(mem[pc+0])
        inst = Instruction("mov a,{reg}",
                           opcode=mem[pc+0],
                           operands=(),
                           reg=reg,
                           flow_type=FlowTypes.Continue,)
        return inst

    # 0x68: 'OR A,!addr16'
    elif mem[pc+0] == 0x68:
        addr16 = mem[pc+1] + (mem[pc+2] << 8)
        inst = Instruction('or a,{addr16}',
                           opcode=mem[pc+0],
                           operands=(mem[pc+1], mem[pc+2]),
                           addr16=addr16,
                           flow_type=FlowTypes.Continue,)
        return inst

    # 0x69: 'OR A,[HL+byte]'
    elif mem[pc+0] == 0x69:
        offset = mem[pc+1]
        inst = Instruction('or a,[hl+{offset}]',
                           opcode=mem[pc+0],
                           operands=(mem[pc+1],),
                           offset=offset,
                           flow_type=FlowTypes.Continue,)
        return inst

    # 0x6d: 'OR A,#byte'
    elif mem[pc+0] == 0x6d:
        imm8 = mem[pc+1]
        inst = Instruction('or a,{imm8}',
                           opcode=mem[pc+0],
                           operands=(mem[pc+1],),
                           imm8=imm8,
                           flow_type=FlowTypes.Continue,)
        return inst

    # 0x6e: 'OR A,saddr'
    elif mem[pc+0] == 0x6e:
        saddr = _saddr(mem[pc+1])
        inst = Instruction('or a,{saddr}',
                           opcode=mem[pc+0],
                           operands=(mem[pc+1],),
                           saddr=saddr,
                           flow_type=FlowTypes.Continue,)
        return inst

    # 0x7e: 'XOR A,saddr'
    elif mem[pc+0] == 0x7e:
        saddr = _saddr(mem[pc+1])
        inst = Instruction('xor a,{saddr}',
                           opcode=mem[pc+0],
                           operands=(mem[pc+1],),
                           saddr=saddr,
                           flow_type=FlowTypes.Continue,)
        return inst

    # 0x6f: 'OR A,[HL]'
    elif mem[pc+0] == 0x6f:
        inst = Instruction('or a,[hl]',
                           opcode=mem[pc+0],
                           operands=(),
                           flow_type=FlowTypes.Continue,)
        return inst

    # 0x70: 'MOV X,A' .. 0x77: 'MOV H,A'
    # except 0x71
    elif mem[pc+0] in (0x70, 0x72, 0x73, 0x74, 0x75, 0x76, 0x77):
        reg = _reg(mem[pc+0])
        inst = Instruction("mov {reg},a",
                           opcode=mem[pc+0],
                           operands=(),
                           reg=reg,
                           flow_type=FlowTypes.Continue,)
        return inst

    # 0x78: 'XOR A,!addr16'
    elif mem[pc+0] == 0x78:
        addr16 = mem[pc+1] + (mem[pc+2] << 8)
        inst = Instruction('xor a,{addr16}',
                           opcode=mem[pc+0],
                           operands=(mem[pc+1], mem[pc+2]),
                           addr16=addr16,
                           flow_type=FlowTypes.Continue,)
        return inst

    # 0x79: 'XOR A,[HL+byte]'
    elif mem[pc+0] == 0x79:
        offset = mem[pc+1]
        inst = Instruction('xor a,[hl+{offset}]',
                           opcode=mem[pc+0],
                           operands=(mem[pc+1],),
                           offset=offset,
                           flow_type=FlowTypes.Continue,)
        return inst

    # 0x7d: 'XOR A,#byte'
    elif mem[pc+0] == 0x7d:
        imm8 = mem[pc+1]
        inst = Instruction('xor a,{imm8}',
                           opcode=mem[pc+0],
                           operands=(mem[pc+1],),
                           imm8=imm8,
                           flow_type=FlowTypes.Continue,)
        return inst

    # 0x7f: 'XOR A,[HL]'
    elif mem[pc+0] == 0x7f:
        inst = Instruction('xor a,[hl]',
                           opcode=mem[pc+0],
                           operands=(),
                           flow_type=FlowTypes.Continue,)
        return inst

    elif mem[pc+0] in (0x80, 0x82, 0x84, 0x86):
        regpair = _regpair(mem[pc+0])
        inst = Instruction("incw {regpair}",
                           opcode=mem[pc+0],
                           operands=(),
                           regpair=regpair,
                           flow_type=FlowTypes.Continue,)
        return inst

    # 0x81: 'INC saddr'
    # INC 0fe20h                  ;81 20          saddr
    elif mem[pc+0] == 0x81:
        saddr = _saddr(mem[pc+1])
        inst = Instruction('inc {saddr}',
                           opcode=mem[pc+0],
                           operands=(mem[pc+1],),
                           saddr=saddr,
                           flow_type=FlowTypes.Continue,)
        return inst

    # 0x83: 'XCH A,saddr'
    elif mem[pc+0] == 0x83:
        saddr = _saddr(mem[pc+1])
        inst = Instruction('xch a,{saddr}',
                           opcode=mem[pc+0],
                           operands=(mem[pc+1],),
                           saddr=saddr,
                           flow_type=FlowTypes.Continue,)
        return inst

    # 0x85: 'MOV A,[DE]'
    elif mem[pc+0] == 0x85:
        inst = Instruction('mov a,[de]',
                           opcode=mem[pc+0],
                           operands=(),
                           flow_type=FlowTypes.Continue,)
        return inst

    # 0x87: 'MOV A,[HL]'
    elif mem[pc+0] == 0x87:
        inst = Instruction('mov a,[hl]',
                           opcode=mem[pc+0],
                           operands=(),
                           flow_type=FlowTypes.Continue,)
        return inst

    # 0x88: 'ADD saddr,#byte'
    elif mem[pc+0] == 0x88:
        saddr = _saddr(mem[pc+1])
        imm8 = mem[pc+2]
        inst = Instruction('add {saddr},{imm8}',
                           opcode=mem[pc+0],
                           operands=(mem[pc+1], mem[pc+2]),
                           saddr=saddr,
                           imm8=imm8,
                           flow_type=FlowTypes.Continue,)
        return inst

    # MOVW AX,0fe20h              ;89 20          saddrp
    # MOVW AX,SP                  ;89 1C
    elif mem[pc+0] == 0x89:
        new_pc = pc + 2
        saddrp = _saddrp(mem[pc+1])
        if saddrp == 0xff1c:
            inst = Instruction('movw ax,sp',
                               opcode=mem[pc+0],
                               operands=(mem[pc+1],),
                               flow_type=FlowTypes.Continue,)
            return inst
        else:
            inst = Instruction('movw ax,{saddrp}',
                               opcode=mem[pc+0],
                               operands=(mem[pc+1],),
                               saddrp=saddrp,
                               flow_type=FlowTypes.Continue,)
            return inst

    # 0x8a: 'DBNZ C,$rel   '
    elif mem[pc+0] == 0x8a:
        new_pc = pc + 2
        reldisp = mem[pc+1]
        reltarget = _resolve_rel(new_pc, reldisp)
        inst = Instruction('dbnz c,{reltarget}',
                           opcode=mem[pc+0],
                           operands=(mem[pc+1],),
                           reltarget=reltarget,
                           flow_type=FlowTypes.ConditionalJump,)
        return inst

    # 0x8b: 'DBNZ B,$rel   '
    elif mem[pc+0] == 0x8b:
        new_pc = pc + 2
        reldisp = mem[pc+1]
        reltarget = _resolve_rel(new_pc, reldisp)
        inst = Instruction('dbnz b,{reltarget}',
                           opcode=mem[pc+0],
                           operands=(mem[pc+1],),
                           reltarget=reltarget,
                           flow_type=FlowTypes.ConditionalJump,)
        return inst

    # BT 0fe20h.0,$label8         ;8C 20 FD       saddr
    # BT PSW.0,$label9            ;8C 1E FD
    elif mem[pc+0] in (0x8c, 0x9c, 0xac, 0xbc, 0xcc, 0xdc, 0xec, 0xfc):
        new_pc = pc + 3
        bit = _bit(mem[pc+0])
        saddr = _saddr(mem[pc+1])
        reldisp = mem[pc+2]
        reltarget = _resolve_rel(new_pc, reldisp)
        if saddr == 0xff1e:
            inst = Instruction('bt psw.{bit},{reltarget}',
                               opcode=mem[pc+0],
                               operands=(mem[pc+1], mem[pc+2]),
                               bit=bit,
                               reltarget=reltarget,
                               flow_type=FlowTypes.ConditionalJump,)
            return inst
        else:
            inst = Instruction('bt {saddr}.{bit},{reltarget}',
                               opcode=mem[pc+0],
                               operands=(mem[pc+1], mem[pc+2]),
                               saddr=saddr,
                               bit=bit,
                               reltarget=reltarget,
                               flow_type=FlowTypes.ConditionalJump,)
            return inst

    # 0x8d: 'BC $rel'
    elif mem[pc+0] == 0x8d:
        new_pc = pc + 2
        reldisp = mem[pc+1]
        reltarget = _resolve_rel(new_pc, reldisp)
        inst = Instruction('bc {reltarget}',
                           opcode=mem[pc+0],
                           operands=(mem[pc+1],),
                           reltarget=reltarget,
                           flow_type=FlowTypes.ConditionalJump,)
        return inst

    # 0x8e: 'MOV A,!addr16'
    elif mem[pc+0] == 0x8e:
        addr16 = mem[pc+1] + (mem[pc+2] << 8)
        inst = Instruction('mov a,{addr16}',
                           opcode=mem[pc+0],
                           operands=(mem[pc+1], mem[pc+2]),
                           addr16=addr16,
                           flow_type=FlowTypes.Continue,)
        return inst

    elif mem[pc+0] == 0x8f:
        inst = Instruction('reti',
                           opcode=mem[pc+0],
                           operands=(),
                           flow_type=FlowTypes.SubroutineReturn)
        return inst

    elif mem[pc+0] in (0x90, 0x92, 0x94, 0x96):
        regpair = _regpair(mem[pc+0])
        inst = Instruction('decw {regpair}',
                           opcode=mem[pc+0],
                           operands=(),
                           regpair=regpair,
                           flow_type=FlowTypes.Continue,)
        return inst

    # 0x91: 'DEC saddr'
    # DEC 0fe20h                  ;91 20          saddr
    elif mem[pc+0] == 0x91:
        saddr = _saddr(mem[pc+1])
        inst = Instruction('dec {saddr}',
                           opcode=mem[pc+0],
                           operands=(mem[pc+1],),
                           saddr=saddr,
                           flow_type=FlowTypes.Continue,)
        return inst

    # 0x93: 'XCH A,sfr'
    elif mem[pc+0] == 0x93:
        sfr = _sfr(mem[pc+1])
        inst = Instruction("xch a,{sfr}",
                           opcode=mem[pc+0],
                           operands=(mem[pc+1],),
                           sfr=sfr,
                           flow_type=FlowTypes.Continue,)
        return inst

    # 0x95: MOV [DE],A
    elif mem[pc+0] == 0x95:
        inst = Instruction('mov [de],a',
                           opcode=mem[pc+0],
                           operands=(),
                           flow_type=FlowTypes.Continue,)
        return inst

    # 0x97: 'MOV [HL],A'
    elif mem[pc+0] == 0x97:
        inst = Instruction('mov [hl],a',
                           opcode=mem[pc+0],
                           operands=(),
                           flow_type=FlowTypes.Continue,)
        return inst

    # 0x98: 'SUB saddr,#byte'
    elif mem[pc+0] == 0x98:
        saddr = _saddr(mem[pc+1])
        imm8 = mem[pc+2]
        inst = Instruction('sub {saddr},{imm8}',
                           opcode=mem[pc+0],
                           operands=(mem[pc+1], mem[pc+2]),
                           saddr=saddr,
                           imm8=imm8,
                           flow_type=FlowTypes.Continue,)
        return inst

    # MOVW 0fe20h,AX              ;99 20          saddrp
    # MOVW SP,AX                  ;99 1C
    elif mem[pc+0] == 0x99:
        new_pc = pc + 2
        saddrp = _saddrp(mem[pc+1])
        if saddrp == 0xff1c:
            inst = Instruction('movw sp,ax',
                               opcode=mem[pc+0],
                               operands=(mem[pc+1],),
                               flow_type=FlowTypes.Continue,)
            return inst
        else:
            inst = Instruction('movw {saddrp},ax',
                               opcode=mem[pc+0],
                               operands=(mem[pc+1],),
                               saddrp=saddrp,
                               flow_type=FlowTypes.Continue,)
            return inst

    # 0x9a: 'CALL !addr16'
    elif mem[pc+0] == 0x9a:
        addr16 = mem[pc+1] + (mem[pc+2] << 8)
        inst = Instruction('call {addr16}',
                            opcode=mem[pc+0],
                            operands=(mem[pc+1], mem[pc+2]),
                            addr16=addr16,
                            flow_type=FlowTypes.SubroutineCall,)
        return inst

    # 0x9b: 'BR !addr16'
    elif mem[pc+0] == 0x9b:
        addr16 = mem[pc+1] + (mem[pc+2] << 8)
        inst = Instruction('br {addr16}',
                           opcode=mem[pc+0],
                           operands=(mem[pc+1], mem[pc+2]),
                           addr16=addr16,
                           flow_type=FlowTypes.UnconditionalJump,)
        return inst

    # 0x9d: 'BNC $rel'
    elif mem[pc+0] == 0x9d:
        new_pc = pc + 2
        reldisp = mem[pc+1]
        reltarget = _resolve_rel(new_pc, reldisp)
        inst = Instruction('bnc {reltarget}',
                           opcode=mem[pc+0],
                           operands=(mem[pc+1],),
                           reltarget=reltarget,
                           flow_type=FlowTypes.ConditionalJump,)
        return inst

    # 0x9e: 'MOV !addr16,A'
    elif mem[pc+0] == 0x9e:
        addr16 = mem[pc+1] + (mem[pc+2] << 8)
        inst = Instruction('mov {addr16},a',
                           opcode=mem[pc+0],
                           operands=(mem[pc+1], mem[pc+2]),
                           addr16=addr16,
                           flow_type=FlowTypes.Continue,)
        return inst

    elif mem[pc+0] == 0x9f:
        inst = Instruction("retb",
                           opcode=mem[pc+0],
                           operands=(),
                           flow_type=FlowTypes.SubroutineReturn,)
        return inst

    elif mem[pc+0] in (0xa0, 0xa1, 0xa2, 0xa3, 0xa4, 0xa5, 0xa6, 0xa7):
        reg = _reg(mem[pc+0])
        imm8 = mem[pc+1]
        inst = Instruction("mov {reg},{imm8}",
                           opcode=mem[pc+0],
                           operands=(mem[pc+1],),
                           reg=reg,
                           imm8=imm8,
                           flow_type=FlowTypes.Continue,)
        return inst

    # 0xa8: 'ADDC saddr,#byte'
    elif mem[pc+0] == 0xa8:
        saddr = _saddr(mem[pc+1])
        imm8 = mem[pc+2]
        inst = Instruction('addc {saddr},{imm8}',
                           opcode=mem[pc+0],
                           operands=(mem[pc+1], mem[pc+2]),
                           saddr=saddr,
                           imm8=imm8,
                           flow_type=FlowTypes.Continue,)
        return inst

    # 0xa9: 'MOVW AX,sfrp'
    elif mem[pc+0] == 0xa9:
        sfrp = _sfrp(mem[pc+1])
        inst = Instruction("movw ax,{sfrp}",
                           opcode=mem[pc+0],
                           operands=(mem[pc+1],),
                           sfrp=sfrp,
                           flow_type=FlowTypes.Continue,)
        return inst

    elif mem[pc+0] == 0xaa:
        inst = Instruction("mov a,[hl+c]",
                           opcode=mem[pc+0],
                           operands=(),
                           flow_type=FlowTypes.Continue,)
        return inst

    elif mem[pc+0] == 0xab:
        inst = Instruction("mov a,[hl+b]",
                           opcode=mem[pc+0],
                           operands=(),
                           flow_type=FlowTypes.Continue,)
        return inst

    # 0xad: 'BZ $rel   '
    elif mem[pc+0] == 0xad:
        new_pc = pc + 2
        reldisp = mem[pc+1]
        reltarget = _resolve_rel(new_pc, reldisp)
        inst = Instruction('bz {reltarget}',
                            opcode=mem[pc+0],
                            operands=(mem[pc+1],),
                            reltarget=reltarget,
                            flow_type=FlowTypes.ConditionalJump,)
        return inst

    # 0xae: 'MOV A,[HL+byte]'
    elif mem[pc+0] == 0xae:
        offset = mem[pc+1]
        inst = Instruction("mov a,[hl+{offset}]",
                           opcode=mem[pc+0],
                           operands=(mem[pc+1],),
                           offset=offset,
                           flow_type=FlowTypes.Continue,)
        return inst

    elif mem[pc+0] == 0xaf:
        inst = Instruction("ret",
                           opcode=mem[pc+0],
                           operands=(),
                           flow_type=FlowTypes.SubroutineReturn,)
        return inst

    elif mem[pc+0] in (0xb0, 0xb2, 0xb4, 0xb6):
        regpair = _regpair(mem[pc+0])
        inst = Instruction("pop {regpair}",
                           opcode=mem[pc+0],
                           operands=(),
                           regpair=regpair,
                           flow_type=FlowTypes.Continue,)
        return inst

    elif mem[pc+0] in (0xb1, 0xb3, 0xb5, 0xb7):
        regpair = _regpair(mem[pc+0])
        inst = Instruction("push {regpair}",
                           opcode=mem[pc+0],
                           operands=(),
                           regpair=regpair,
                           flow_type=FlowTypes.Continue,)
        return inst

    # 0xb8: 'SUBC saddr,#byte'
    elif mem[pc+0] == 0xb8:
        new_pc = pc + 3
        saddr = _saddr(mem[pc+1])
        imm8 = mem[pc+2]
        inst = Instruction('subc {saddr},{imm8}',
                           opcode=mem[pc+0],
                           operands=(mem[pc+1], mem[pc+2]),
                           saddr=saddr,
                           imm8=imm8,
                           flow_type=FlowTypes.Continue,)
        return inst

    # 0xb9: 'MOVW sfrp,AX'
    elif mem[pc+0] == 0xb9:
        sfrp = _sfrp(mem[pc+1])
        inst = Instruction("movw {sfrp},ax",
                           opcode=mem[pc+0],
                           operands=(mem[pc+1],),
                           sfrp=sfrp,
                           flow_type=FlowTypes.Continue,)
        return inst

    # 0xba: 'MOV [HL+C],A'
    # MOV [HL+C],A                ;BA
    elif mem[pc+0] == 0xba:
        inst = Instruction("mov [hl+c],a",
                           opcode=mem[pc+0],
                           operands=(),
                           flow_type=FlowTypes.Continue,)
        return inst

    # MOV [HL+B],A                ;BB
    elif mem[pc+0] == 0xbb:
        inst = Instruction("mov [hl+b],a",
                           opcode=mem[pc+0],
                           operands=(),
                           flow_type=FlowTypes.Continue,)
        return inst

    # 0xbd: 'BNZ $rel'
    elif mem[pc+0] == 0xbd:
        new_pc = pc + 2
        reldisp = mem[pc+1]
        reltarget = _resolve_rel(new_pc, reldisp)
        inst = Instruction('bnz {reltarget}',
                           opcode=mem[pc+0],
                           operands=(mem[pc+1],),
                           reltarget=reltarget,
                           flow_type=FlowTypes.ConditionalJump,)
        return inst

    # 0xbe: 'MOV [HL+byte],A'
    elif mem[pc+0] == 0xbe:
        offset = mem[pc+1]
        inst = Instruction("mov [hl+{offset}],a",
                           opcode=mem[pc+0],
                           operands=(mem[pc+1],),
                           offset=offset,
                           flow_type=FlowTypes.Continue,)
        return inst

    elif mem[pc+0] == 0xbf:
        inst = Instruction("brk",
                           opcode=mem[pc+0],
                           operands=(),
                           flow_type=FlowTypes.Stop,)
        return inst

    elif mem[pc+0] in (0xc2, 0xc4, 0xc6):
        regpair = _regpair(mem[pc+0])
        inst = Instruction("movw ax,{regpair}",
                           opcode=mem[pc+0],
                           operands=(),
                           regpair=regpair,
                           flow_type=FlowTypes.Continue,)
        return inst

    # 0xc8: 'CMP saddr,#byte'
    elif mem[pc+0] == 0xc8:
        saddr = _saddr(mem[pc+1])
        imm8 = mem[pc+2]
        inst = Instruction('cmp {saddr},{imm8}',
                           opcode=mem[pc+0],
                           operands=(mem[pc+1], mem[pc+2]),
                           saddr=saddr,
                           imm8=imm8,
                           flow_type=FlowTypes.Continue,)
        return inst

    # ADDW AX,#0abcdh             ;CA CD AB
    elif mem[pc+0] == 0xca:
        imm16 = mem[pc+1] + (mem[pc+2] << 8)
        inst = Instruction("addw ax,{imm16}",
                           opcode=mem[pc+0],
                           operands=(mem[pc+1], mem[pc+2]),
                           imm16=imm16,
                           flow_type=FlowTypes.Continue,)
        return inst

    # 0xce: 'XCH A,!addr16'
    elif mem[pc+0] == 0xce:
        new_pc = pc + 3
        addr16 = mem[pc+1] + (mem[pc+2] << 8)
        inst = Instruction('xch a,{addr16}',
                           opcode=mem[pc+0],
                           operands=(mem[pc+1], mem[pc+2]),
                           addr16=addr16,
                           flow_type=FlowTypes.Continue,)
        return inst

    elif mem[pc+0] in (0xd2, 0xd4, 0xd6):
        regpair = _regpair(mem[pc+0])
        inst = Instruction("movw {regpair},ax",
                           opcode=mem[pc+0],
                           operands=(),
                           regpair=regpair,
                           flow_type=FlowTypes.Continue,)
        return inst

    # 0xd8: 'AND saddr,#byte'
    elif mem[pc+0] == 0xd8:
        saddr = _saddr(mem[pc+1])
        imm8 = mem[pc+2]
        inst = Instruction('and {saddr},{imm8}',
                           opcode=mem[pc+0],
                           operands=(mem[pc+1], mem[pc+2]),
                           saddr=saddr,
                           imm8=imm8,
                           flow_type=FlowTypes.Continue,)
        return inst

    # SUBW AX,#0abcdh             ;DA CD AB
    elif mem[pc+0] == 0xda:
        imm16 = mem[pc+1] + (mem[pc+2] << 8)
        inst = Instruction("subw ax,{imm16}",
                           opcode=mem[pc+0],
                           operands=(mem[pc+1], mem[pc+2]),
                           imm16=imm16,
                           flow_type=FlowTypes.Continue,)
        return inst

    # 0xde: 'XCH A,[HL+byte]'
    elif mem[pc+0] == 0xde:
        offset = mem[pc+1]
        inst = Instruction("xch a,[hl+{offset}]",
                           opcode=mem[pc+0],
                           operands=(mem[pc+1],),
                           offset=offset,
                           flow_type=FlowTypes.Continue,)
        return inst

    elif mem[pc+0] in (0xe2, 0xe4, 0xe6):
        regpair = _regpair(mem[pc+0])
        inst = Instruction("xchw ax,{regpair}",
                           opcode=mem[pc+0],
                           operands=(),
                           regpair=regpair,
                           flow_type=FlowTypes.Continue,)
        return inst

    # 0xe8: 'OR saddr,#byte'
    elif mem[pc+0] == 0xe8:
        saddr = _saddr(mem[pc+1])
        imm8 = mem[pc+2]
        inst = Instruction('or {saddr},{imm8}',
                           opcode=mem[pc+0],
                           operands=(mem[pc+1], mem[pc+2]),
                           saddr=saddr,
                           imm8=imm8,
                           flow_type=FlowTypes.Continue,)
        return inst

    # CMPW AX,#0abcdh             ;EA CD AB
    elif mem[pc+0] == 0xea:
        imm16 = mem[pc+1] + (mem[pc+2] << 8)
        inst = Instruction("cmpw ax,{imm16}",
                           opcode=mem[pc+0],
                           operands=(mem[pc+1], mem[pc+2]),
                           imm16=imm16,
                           flow_type=FlowTypes.Continue,)
        return inst

    # MOVW 0fe20h,#0abcdh         ;EE 20 CD AB    saddrp
    # MOVW SP,#0abcdh             ;EE 1C CD AB
    elif mem[pc+0] == 0xee:
        saddrp = _saddrp(mem[pc+1])
        imm16 = mem[pc+2] + (mem[pc+3] << 8)
        if saddrp == 0xff1c:
            inst = Instruction('movw sp,{imm16}',
                               opcode=mem[pc+0],
                               operands=(mem[pc+1], mem[pc+2], mem[pc+3]),
                               imm16=imm16,
                               flow_type=FlowTypes.Continue,)
            return inst
        else:
            inst = Instruction('movw {saddrp},{imm16}',
                               opcode=mem[pc+0],
                               operands=(mem[pc+1], mem[pc+2], mem[pc+3]),
                               saddrp=saddrp,
                               imm16=imm16,
                               flow_type=FlowTypes.Continue,)
            return inst

    # mov a,0fe20h                ;F0 20          saddr
    # mov a,psw                   ;F0 1E
    elif mem[pc+0] == 0xf0:
        saddr = _saddr(mem[pc+1])
        if saddr == 0xff1e:
            inst = Instruction('mov a,psw',
                               opcode=mem[pc+0],
                               operands=(mem[pc+1],),
                               flow_type=FlowTypes.Continue,)
            return inst
        else:
            inst = Instruction('mov a,{saddr}',
                               opcode=mem[pc+0],
                               operands=(mem[pc+1],),
                               saddr=saddr,
                               flow_type=FlowTypes.Continue,)
            return inst

    # MOV 0fe20h,A                ;F2 20          saddr
    # MOV PSW,A                   ;F2 1E
    elif mem[pc+0] == 0xf2:
        saddr = _saddr(mem[pc+1])
        if saddr == 0xff1e:
            inst = Instruction('mov psw,a',
                               opcode=mem[pc+0],
                               operands=(mem[pc+1],),
                               flow_type=FlowTypes.Continue,)
            return inst
        else:
            inst = Instruction('mov {saddr},a',
                               opcode=mem[pc+0],
                               operands=(mem[pc+1],),
                               saddr=saddr,
                               flow_type=FlowTypes.Continue,)
            return inst

    # 0xf4: 'MOV A,sfr'
    elif mem[pc+0] == 0xf4:
        sfr = _sfr(mem[pc+1])
        inst = Instruction("mov a,{sfr}",
                           opcode=mem[pc+0],
                           operands=(mem[pc+1],),
                           sfr=sfr,
                           flow_type=FlowTypes.Continue,)
        return inst

    # 0xf6: 'MOV sfr,A'
    elif mem[pc+0] == 0xf6:
        sfr = _sfr(mem[pc+1])
        inst = Instruction("mov {sfr},a",
                           opcode=mem[pc+0],
                           operands=(mem[pc+1],),
                           sfr=sfr,
                           flow_type=FlowTypes.Continue,)
        return inst

    # 0xf8: 'XOR saddr,#byte'
    elif mem[pc+0] == 0xf8:
        saddr = _saddr(mem[pc+1])
        imm8 = mem[pc+2]
        inst = Instruction('xor {saddr},{imm8}',
                           opcode=mem[pc+0],
                           operands=(mem[pc+1], mem[pc+2]),
                           saddr=saddr,
                           imm8=imm8,
                           flow_type=FlowTypes.Continue,)
        return inst

    # 0xfa: 'BR $rel'
    elif mem[pc+0] == 0xfa:
        new_pc = pc + 2
        reldisp = mem[pc+1]
        reltarget = _resolve_rel(new_pc, reldisp)
        inst = Instruction('br {reltarget}',
                           opcode=mem[pc+0],
                           operands=(mem[pc+1],),
                           reltarget=reltarget,
                           flow_type=FlowTypes.UnconditionalJump,)
        return inst

    # MOVW 0fffeh,#0abcdh         ;FE FE CD AB    sfrp
    elif mem[pc+0] == 0xfe:
        sfrp = _sfrp(mem[pc+1])
        imm16 = mem[pc+2] + (mem[pc+3] << 8)
        inst = Instruction('movw {sfrp},{imm16}',
                           opcode=mem[pc+0],
                           operands=(mem[pc+1], mem[pc+2], mem[pc+3]),
                           sfrp=sfrp,
                           imm16=imm16,
                           flow_type=FlowTypes.Continue,)
        return inst

    elif mem[pc+0] == 0x31:
        if mem[pc+1] == 0x80:
            inst = Instruction('rol4 [hl]',
                               opcode=mem[pc+0],
                               operands=(mem[pc+1],),
                               flow_type=FlowTypes.Continue,)
            return inst
        elif mem[pc+1] == 0x82:
            inst = Instruction('divuw c',
                               opcode=mem[pc+0],
                               operands=(mem[pc+1],),
                               flow_type=FlowTypes.Continue,)
            return inst
        elif mem[pc+1] == 0x88:
            inst = Instruction('mulu x',
                               opcode=mem[pc+0],
                               operands=(mem[pc+1],),
                               flow_type=FlowTypes.Continue,)
            return inst
        elif mem[pc+1] == 0x90:
            inst = Instruction('ror4 [hl]',
                               opcode=mem[pc+0],
                               operands=(mem[pc+1],),
                               flow_type=FlowTypes.Continue,)
            return inst
        elif mem[pc+1] == 0x98:
            inst = Instruction('br ax',
                               opcode=mem[pc+0],
                               operands=(mem[pc+1],),
                               flow_type=FlowTypes.Continue,)
            return inst
        elif (mem[pc+1] >> 4) < 0x09 and (mem[pc+1] & 0x0f) in (0x0a, 0x0b):
            inst = mem[pc+1] >> 4
            instname = ('add', 'sub', 'addc', 'subc',
                        'cmp', 'and', 'or', 'xor', 'xch')[inst]

            mode = mem[pc+1] & 0x0f
            modename = "a,[hl+b]" if mode == 0x0b else "a,[hl+c]"

            inst = Instruction("%s %s" % (instname, modename),
                               opcode=mem[pc+0],
                               operands=(mem[pc+1],),
                               flow_type=FlowTypes.Continue,)
            return inst
        elif (mem[pc+1] >> 4) < 0x08 and (mem[pc+1] & 0x0f) in (0x0d, 0x0e, 0x0f):
            new_pc = pc + 3

            inst = (mem[pc+1] & 0x0f) - 0x0d
            instname = ('btclr', 'bt', 'bf')[inst]

            bit = mem[pc+1] >> 4
            reldisp = mem[pc+2]
            reltarget = _resolve_rel(new_pc, reldisp)

            inst = Instruction("%s a.{bit},{reltarget}" % instname,
                               opcode=mem[pc+0],
                               operands=(mem[pc+1], mem[pc+2]),
                               bit=bit,
                               reltarget=reltarget,
                               flow_type=FlowTypes.ConditionalJump,)
            return inst
        elif (mem[pc+1] >> 4) < 0x08 and (mem[pc+1] & 0x0f) in (0x01, 0x03):
            new_pc = pc + 4

            instname = 'btclr' if (mem[pc+1] & 0x0f) == 0x01 else 'bf'
            bit = mem[pc+1] >> 4
            saddr = _saddr(mem[pc+2])
            reldisp = mem[pc+3]
            reltarget = _resolve_rel(new_pc, reldisp)

            if saddr == 0xff1e:
                inst = Instruction("%s psw.{bit},{reltarget}" % instname,
                                   opcode=mem[pc+0],
                                   operands=(mem[pc+1], mem[pc+2], mem[pc+3]),
                                   bit=bit,
                                   reltarget=reltarget,
                                   flow_type=FlowTypes.ConditionalJump,)
                return inst
            else:
                inst = Instruction("%s {saddr}.{bit},{reltarget}" % instname,
                                   opcode=mem[pc+0],
                                   operands=(mem[pc+1], mem[pc+2], mem[pc+3]),
                                   saddr=saddr,
                                   bit=bit,
                                   reltarget=reltarget,
                                   flow_type=FlowTypes.ConditionalJump,)
                return inst
        elif (mem[pc+1] >> 4) < 0x08 and (mem[pc+1] & 0x0f) in (0x5, 0x6, 0x7):
            new_pc = pc + 4

            index = (mem[pc+1] & 0x0f) - 0x05
            name = ('btclr', 'bt', 'bf')[index]

            bit = mem[pc+1] >> 4
            sfr = _sfr(mem[pc+2])
            reldisp = mem[pc+3]
            reltarget = _resolve_rel(new_pc, reldisp)

            inst = Instruction(name + " {sfr}.{bit},{reltarget}",
                               opcode=mem[pc+0],
                               operands=(mem[pc+1], mem[pc+2], mem[pc+3]),
                               sfr=sfr,
                               bit=bit,
                               reltarget=reltarget,
                               flow_type=FlowTypes.ConditionalJump,)
            return inst
        elif (mem[pc+1] >> 4) in range(0x8, 0xf+1) and (mem[pc+1] & 0x0f) in (0x5, 0x6, 0x7):
            new_pc = pc + 3

            index = (mem[pc+1] & 0x0f) - 0x05
            name = ('btclr', 'bt', 'bf')[index]

            bit = (mem[pc+1] >> 4) - 0x08
            reldisp = mem[pc+2]
            reltarget = _resolve_rel(new_pc, reldisp)

            inst = Instruction(name + " [hl].{bit},{reltarget}",
                               opcode=mem[pc+0],
                               operands=(mem[pc+1], mem[pc+2]),
                               bit=bit,
                               reltarget=reltarget,
                               flow_type=FlowTypes.ConditionalJump,)
            return inst
        else:
            msg = "Illegal byte 0x%02x follows opcode 0x31 at 0x%04x" % (mem[pc+1], pc)
            raise IllegalInstructionError(msg)

    elif mem[pc+0] == 0x61:
        bit = _bit(mem[pc+1])
        reg = _reg(mem[pc+1])
        if mem[pc+1] == 0x80:
            inst = Instruction('adjba',
                               opcode=mem[pc+0],
                               operands=(mem[pc+1],),
                               flow_type=FlowTypes.Continue,)
            return inst
        elif mem[pc+1] == 0x90:
            inst = Instruction('adjbs',
                               opcode=mem[pc+0],
                               operands=(mem[pc+1],),
                               flow_type=FlowTypes.Continue,)
            return inst
        elif mem[pc+1] == 0xd0:
            inst = Instruction('sel rb0',
                               opcode=mem[pc+0],
                               operands=(mem[pc+1],),
                               flow_type=FlowTypes.Continue,)
            return inst
        elif mem[pc+1] == 0xd8:
            inst = Instruction('sel rb1',
                               opcode=mem[pc+0],
                               operands=(mem[pc+1],),
                               flow_type=FlowTypes.Continue,)
            return inst
        elif mem[pc+1] == 0xf0:
            inst = Instruction('sel rb2',
                               opcode=mem[pc+0],
                               operands=(mem[pc+1],),
                               flow_type=FlowTypes.Continue,)
            return inst
        elif mem[pc+1] == 0xf8:
            inst = Instruction('sel rb3',
                               opcode=mem[pc+0],
                               operands=(mem[pc+1],),
                               flow_type=FlowTypes.Continue,)
            return inst
        elif mem[pc+1] in range(0x00, 0x80):
            index = mem[pc+1] >> 4
            name = ('add', 'sub', 'addc', 'subc',
                    'cmp', 'and', 'or', 'xor')[index]

            mode = mem[pc+1] & 0x0f
            modetpl = "{reg},a" if mode in range(0x00, 0x08) else "a,{reg}"
            inst = Instruction(name + " " + modetpl,
                               opcode=mem[pc+0],
                               operands=(mem[pc+1],),
                               reg=reg,
                               flow_type=FlowTypes.Continue,)
            return inst
        elif mem[pc+1] in (0x89, 0x99, 0xa9, 0xb9, 0xc9, 0xd9, 0xe9, 0xf9):
            inst = Instruction('mov1 a.{bit},cy',
                               opcode=mem[pc+0],
                               operands=(mem[pc+1],),
                               bit=bit,
                               flow_type=FlowTypes.Continue,)
            return inst
        elif mem[pc+1] in (0x8a, 0x9a, 0xaa, 0xba, 0xca, 0xda, 0xea, 0xfa):
            inst = Instruction('set1 a.{bit}',
                               opcode=mem[pc+0],
                               operands=(mem[pc+1],),
                               bit=bit,
                               flow_type=FlowTypes.Continue,)
            return inst
        elif mem[pc+1] in (0x8b, 0x9b, 0xab, 0xbb, 0xcb, 0xdb, 0xeb, 0xfb):
            inst = Instruction('clr1 a.{bit}',
                               opcode=mem[pc+0],
                               operands=(mem[pc+1],),
                               bit=bit,
                               flow_type=FlowTypes.Continue,)
            return inst
        elif mem[pc+1] in (0x8c, 0x9c, 0xac, 0xbc, 0xcc, 0xdc, 0xec, 0xfc):
            inst = Instruction('mov1 cy,a.{bit}',
                               opcode=mem[pc+0],
                               operands=(mem[pc+1],),
                               bit=bit,
                               flow_type=FlowTypes.Continue,)
            return inst
        elif mem[pc+1] in (0x8d, 0x9d, 0xad, 0xbd, 0xcd, 0xdd, 0xed, 0xfd):
            inst = Instruction('and1 cy,a.{bit}',
                               opcode=mem[pc+0],
                               operands=(mem[pc+1],),
                               bit=bit,
                               flow_type=FlowTypes.Continue,)
            return inst
        elif mem[pc+1] in (0x8e, 0x9e, 0xae, 0xbe, 0xce, 0xde, 0xee, 0xfe):
            inst = Instruction('or1 cy,a.{bit}',
                               opcode=mem[pc+0],
                               operands=(mem[pc+1],),
                               bit=bit,
                               flow_type=FlowTypes.Continue,)
            return inst
        elif mem[pc+1] in (0x8f, 0x9f, 0xaf, 0xbf, 0xcf, 0xdf, 0xef, 0xff):
            inst = Instruction('xor1 cy,a.{bit}',
                               opcode=mem[pc+0],
                               operands=(mem[pc+1],),
                               bit=bit,
                               flow_type=FlowTypes.Continue,)
            return inst
        else:
            msg = "Illegal byte 0x%02x follows opcode 0x61 at 0x%04x" % (mem[pc+1], pc)
            raise IllegalInstructionError(msg)

    elif mem[pc+0] == 0x71:
        if mem[pc+1] == 0x00:
            inst = Instruction('stop',
                               opcode=mem[pc+0],
                               operands=(mem[pc+1],),
                               flow_type=FlowTypes.Stop,)
            return inst
        elif mem[pc+1] == 0x10:
            inst = Instruction('halt',
                               opcode=mem[pc+0],
                               operands=(mem[pc+1],),
                               flow_type=FlowTypes.Stop,)
            return inst
        elif mem[pc+1] in (0x82, 0x92, 0xa2, 0xb2, 0xc2, 0xd2, 0xe2, 0xf2):
            bit = (mem[pc+1] >> 4) - 8
            inst = Instruction('set1 [hl].{bit}',
                               opcode=mem[pc+0],
                               operands=(mem[pc+1],),
                               bit=bit,
                               flow_type=FlowTypes.Continue,)
            return inst
        elif mem[pc+1] in (0x83, 0x93, 0xa3, 0xb3, 0xc3, 0xd3, 0xe3, 0xf3):
            bit = (mem[pc+1] >> 4) - 8
            inst = Instruction('clr1 [hl].{bit}',
                               opcode=mem[pc+0],
                               operands=(mem[pc+1],),
                               bit=bit,
                               flow_type=FlowTypes.Continue,)
            return inst
        elif (mem[pc+1] >> 4) in range(8, 0x0f+1) and (mem[pc+1] & 0x0f) in (0x4, 0x5, 0x6, 0x7):
            bit = (mem[pc+1] >> 4) - 8
            index = (mem[pc+1] & 0x0f) - 4
            name = ('mov1', 'and1', 'or1', 'xor1')[index]
            inst = Instruction('%s cy,[hl].{bit}' % name,
                               opcode=mem[pc+0],
                               operands=(mem[pc+1],),
                               bit=bit,
                               flow_type=FlowTypes.Continue,)
            return inst
        elif (mem[pc+1] >> 4) in range(8, 0x0f+1) and (mem[pc+1] & 0x0f) == 1:
            bit = (mem[pc+1] >> 4) - 8
            inst = Instruction('mov1 [hl].{bit},cy',
                               opcode=mem[pc+0],
                               operands=(mem[pc+1],),
                               bit=bit,
                               flow_type=FlowTypes.Continue,)
            return inst
        elif (mem[pc+1] >> 4) < 8 and (mem[pc+1] & 0x0f) in (0x0a, 0x0b):
            bit = (mem[pc+1] >> 4)
            name = 'set1' if (mem[pc+1] & 0x0f) == 0x0a else 'clr1'
            sfr = _sfr(mem[pc+2])
            inst = Instruction(name + ' {sfr}.{bit}',
                               opcode=mem[pc+0],
                               operands=(mem[pc+1], mem[pc+2]),
                               sfr=sfr,
                               bit=bit,
                               flow_type=FlowTypes.Continue,)
            return inst
        elif (mem[pc+1] >> 4) < 8 and (mem[pc+1] & 0x0f) == 0x09:
            bit = (mem[pc+1] >> 4)
            sfr = _sfr(mem[pc+2])
            inst = Instruction('mov1 {sfr}.{bit},cy',
                               opcode=mem[pc+0],
                               operands=(mem[pc+1], mem[pc+2]),
                               sfr=sfr,
                               bit=bit,
                               flow_type=FlowTypes.Continue,)
            return inst
        elif (mem[pc+1] >> 4) < 8 and (mem[pc+1] & 0x0f) in range(0x0c, 0x0f+1):
            bit = (mem[pc+1] >> 4)
            sfr = _sfr(mem[pc+2])
            index = (mem[pc+1] & 0x0f) - 0x0c
            name = ('mov1', 'and1', 'or1', 'xor1')[index]
            inst = Instruction(name + ' cy,{sfr}.{bit}',
                               opcode=mem[pc+0],
                               operands=(mem[pc+1], mem[pc+2]),
                               sfr=sfr,
                               bit=bit,
                               flow_type=FlowTypes.Continue,)
            return inst
        elif (mem[pc+1] >> 4) < 8 and (mem[pc+1] & 0x0f) == 1:
            bit = (mem[pc+1] >> 4)
            saddr = _saddr(mem[pc+2])
            if saddr == 0xff1e:
                inst = Instruction('mov1 psw.{bit},cy',
                                   opcode=mem[pc+0],
                                   operands=(mem[pc+1], mem[pc+2]),
                                   bit=bit,
                                   flow_type=FlowTypes.Continue,)
                return inst
            else:
                inst = Instruction('mov1 {saddr}.{bit},cy',
                                   opcode=mem[pc+0],
                                   operands=(mem[pc+1], mem[pc+2]),
                                   saddr=saddr,
                                   bit=bit,
                                   flow_type=FlowTypes.Continue,)
                return inst
        elif (mem[pc+1] >> 4) < 8 and (mem[pc+1] & 0x0f) in (0x4, 0x5, 0x6, 0x7):
            bit = (mem[pc+1] >> 4)
            inst = (mem[pc+1] & 0x0f) - 4
            instname = ('mov1', 'and1', 'or1', 'xor1')[inst]
            saddr = _saddr(mem[pc+2])
            if saddr == 0xff1e:
                inst = Instruction(instname + ' cy,psw.{bit}',
                                   opcode=mem[pc+0],
                                   operands=(mem[pc+1], mem[pc+2]),
                                   bit=bit,
                                   flow_type=FlowTypes.Continue,)
                return inst
            else:
                inst = Instruction(instname + ' cy,{saddr}.{bit}',
                                   opcode=mem[pc+0],
                                   operands=(mem[pc+1], mem[pc+2]),
                                   saddr=saddr,
                                   bit=bit,
                                   flow_type=FlowTypes.Continue,)
                return inst
        else:
            msg = "Illegal byte 0x%02x follows opcode 0x71 at 0x%04x" % (mem[pc+1], pc)
            raise IllegalInstructionError(msg)

    else:
        msg = "Illegal opcode 0x%02x at 0x%04x" % (mem[pc], pc)
        raise IllegalInstructionError(msg)


def _reg(opcode):
    r = opcode & 0b111
    return ('x', 'a', 'c', 'b', 'e', 'd', 'l', 'h')[r]

def _regpair(opcode):
    rp = (opcode >> 1) & 0b11
    return ('ax', 'bc', 'de', 'hl')[rp]

def _bit(opcode):
    return (opcode & 0b01110000) >> 4

def _saddr(low):
    saddr = 0xfe00 + low
    if low < 0x20:
        saddr += 0x100
    return saddr

def _saddrp(low):
    saddrp = _saddr(low)
    if saddrp & 1 != 0:
        raise IllegalInstructionError("saddrp must be an even address")
    return _saddr(low)

def _addr16p(low, high):
    addr16p = low + (high << 8)
    if addr16p & 1 != 0:
        raise IllegalInstructionError("addr16p must be an even address")
    return addr16p

def _sfr(low):
    sfr = 0xff00 + low
    return sfr

def _sfrp(low):
    sfrp = _sfr(low)
    if sfrp & 1 != 0:
        raise IllegalInstructionError("sfrp must be an even address")
    return sfrp

def _resolve_rel(pc, displacement):
    if displacement & 0x80:
        displacement = -((displacement ^ 0xFF) + 1)
    return (pc + displacement) & 0xffff



class Instruction(object):
    def __init__(self, template, saddrp=None, saddr=None, reltarget=None, addr5target=None,
                                 addr5=None, addr11=None, addr16=None, addr16p=None,
                                 offset=None, bit=None, imm8=None, imm16=None,
                                 sfr=None, sfrp=None, reg=None, regpair=None,
                                 flow_type=None, opcode=None, operands=()):
        self.template = template
        self.saddrp = saddrp
        self.saddr = saddr
        self.reltarget = reltarget
        self.addr5target = addr5target
        self.addr5 = addr5
        self.addr11 = addr11
        self.addr16 = addr16
        self.addr16p = addr16p
        self.offset = offset
        self.bit = bit
        self.imm8 = imm8
        self.imm16 = imm16
        self.reg = reg
        self.regpair = regpair
        self.sfr = sfr
        self.sfrp = sfrp
        self.flow_type = flow_type
        self.opcode = opcode
        self.operands = operands

    def __len__(self):
        return 1 + len(self.operands)

    def __str__(self):
        return self.to_string()

    def to_string(self, symbols=None):
        if symbols is None:
            symbols = {}  # address: (name, comment)
        disasm = self.template
        if self.saddrp is not None:
            disasm = disasm.replace('{saddrp}', self._format_ext_address(self.saddrp, symbols))
        if self.saddr is not None:
            disasm = disasm.replace('{saddr}', self._format_ext_address(self.saddr, symbols))
        if self.reltarget is not None:
            disasm = disasm.replace('{reltarget}', self._format_ext_address(self.reltarget, symbols))
        if self.addr5 is not None:
            disasm = disasm.replace('{addr5}', '[0x%04x]' % self.addr5)
        if self.addr11 is not None:
            disasm = disasm.replace('{addr11}', '!' + self._format_ext_address(self.addr11, symbols))
        if self.addr16 is not None:
            disasm = disasm.replace('{addr16}', '!' + self._format_ext_address(self.addr16, symbols))
        if self.addr16p is not None:
            disasm = disasm.replace('{addr16p}', '!' + self._format_ext_address(self.addr16p, symbols))
        if self.offset is not None:
            disasm = disasm.replace('{offset}', '0x%02x' % self.offset)
        if self.bit is not None:
            disasm = disasm.replace('{bit}', '%d' % self.bit)
        if self.imm8 is not None:
            disasm = disasm.replace('{imm8}', '#' + '0x%02x' % self.imm8)
        if self.imm16 is not None:
            disasm = disasm.replace('{imm16}', '#' + self._format_imm16(self.imm16, symbols))
        if self.reg is not None:
            disasm = disasm.replace('{reg}', self.reg)
        if self.regpair is not None:
            disasm = disasm.replace('{regpair}', self.regpair)
        if self.sfr is not None:
            disasm = disasm.replace('{sfr}', self._format_ext_address(self.sfr, symbols))
        if self.sfrp is not None:
            disasm = disasm.replace('{sfrp}', self._format_ext_address(self.sfrp, symbols))
        return disasm

    def _format_imm16(self, imm16, symbols):
        if imm16 < 0x007f: # skip vector area
            pass
        elif imm16 in symbols:
            name, comment = symbols[imm16]
            return name
        return '0x%04x' % imm16

    def _format_ext_address(self, address, symbols):
        if address in symbols:
            name, comment = symbols[address]
            return name
        return '0x%04x' % address

    @property
    def all_bytes(self):
        return [self.opcode] + list(self.operands)

    @property
    def referenced_addresses(self):
        '''Return all addresses that are read, written, or branched
        by the instruction.  For indirect or relative addresses, only
        the target is returned.'''
        addresses = []
        names = ('saddrp', 'saddr', 'reltarget', 'addr11', 'addr16', 'addr16p', 'sfr', 'sfrp')
        for name in names:
            address = getattr(self, name, None)
            if address is not None:
                addresses.append(address)
        return addresses

    @property
    def target_address(self):
        '''Return the branch target address, or None if instruction cannot branch'''
        # direct addresses
        if self.addr16 is not None:
            return self.addr16
        if self.addr11 is not None:
            return self.addr11
        # indirect addresses
        if self.addr5target is not None:
            return self.addr5target
        # relative addresses
        if self.reltarget is not None:
            return self.reltarget
        return None


class IllegalInstructionError(Exception):
    pass


class FlowTypes(object):
    Continue = 0
    Stop = 1
    UnconditionalJump = 2
    IndirectUnconditionalJump = 3
    ConditionalJump = 4
    SubroutineCall = 5
    SubroutineReturn = 6

