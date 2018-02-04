    org 0

    nop                     ;00
    not1 cy                 ;01
    ;movw ax,!0abcdh        ;           RA78K0 error E2317: Even expression expected
    movw ax,!0abceh         ;02 CE AB
    ;MOVW !0abcdh,AX        ;           RA78K0 error E2317: Even expression expected
    MOVW !0abceh,AX         ;03 CE AB
label0:
    DBNZ 0fe20h,$label0     ;04 20 FD   DBNZ saddr,$addr16
    xch a,[de]              ;05
                            ;06         06 is Illegal
    XCH A,[HL]              ;07
    ADD A,!0abcdh           ;08 CD AB
    ADD A,[HL+0abh]         ;09 AB
    SET1 0fe20h.0           ;0A 20      saddr
    SET1 PSW.0              ;0A 1E
    CLR1 0fe20h.0           ;0B 20      saddr
    CLR1 PSW.0              ;0B 1E
    callf !0800h            ;0C 00      0c = callf 0800h-08ffh
    callf !08ffh            ;0C FF
    ADD A,#0abh             ;0D AB
    ADD A,0fe20h            ;0E 20      ADD A,saddr     (saddr = FE20H to FF1FH)
    ADD A,[HL]              ;0F
    MOVW AX,#0abcdh         ;10 CD AB
    MOV 0fe20h,#0abh        ;11 20 AB   saddr
    MOV PSW,#0abh           ;11 1E AB
    MOVW BC,#0abcdh         ;12 CD AB
    MOV 0fffeh, #0abh       ;13 FE AB   MOV sfr, #byte  (sfr = FF00H to FFFFH)
    MOVW DE,#0abcdh         ;14 CD AB
                            ;15         15 is Illegal
    MOVW HL,#0abcdh         ;16 CD AB
                            ;17         17 is Illegal
    SUB A,!0abcdh           ;18 CD AB
    SUB A,[HL+0abh]         ;19 AB
    SET1 0fe20h.1           ;1A 20      saddr
    SET1 PSW.1              ;1A 1E
    CLR1 0fe20h.1           ;1B 20      saddr
    CLR1 PSW.1              ;1B 1E
    callf !0900h            ;1C 00      1c = callf 0900h-09ffh
    callf !09ffh            ;1C FF
    SUB A,#0abh             ;1D AB
    SUB A,0fe20h            ;1E 20      SUB A,saddr     (saddr = FE20H to FF1FH)
    SUB A,[HL]              ;1F
    SET1 CY                 ;20
    CLR1 CY                 ;21
    PUSH PSW                ;22
    POP PSW                 ;23
    ROR A,1                 ;24
    RORC A,1                ;25
    ROL A,1                 ;26
    ROLC A,1                ;27
    ADDC A,!0abcdh          ;28 CD AB
    ADDC A,[HL+0abh]        ;29 AB
    SET1 0fe20h.2           ;2A 20      saddr
    SET1 PSW.2              ;2A 1E
    CLR1 0fe20h.2           ;2B 20      saddr
    CLR1 PSW.2              ;2B 1E
    callf !0a00h            ;2C 00      2c = callf 0a00h-0affh
    callf !0affh            ;2C FF
    ADDC A,#0abh            ;2D AB
    ADDC A,0fe20h           ;2E 20      ADDC A,0fe20h   (saddr = FE20H to FF1FH)
    ADDC A,[HL]             ;2F
    XCH A,X                 ;30
                            ;31         TODO
    XCH A,C                 ;32
    XCH A,B                 ;33
    XCH A,E                 ;34
    XCH A,D                 ;35
    XCH A,L                 ;36
    XCH A,H                 ;37
    SUBC A,!0abcdh          ;38 CD AB
    SUBC A,[HL+0abh]        ;39 AB
    SET1 0fe20h.3           ;3A 20      saddr
    SET1 PSW.3              ;3A 1E
    CLR1 0fe20h.3           ;3B 20      saddr
    CLR1 PSW.3              ;3B 1E
    callf !0b00h            ;3C 00      3c = callf 0b00h-0bffh
    callf !0bffh            ;3C FF
    SUBC A,#0abh            ;3D AB
    SUBC A,0fe20h           ;3E 20      SUBC A,saddr    (saddr = FE20H to FF1FH)
    SUBC A,[HL]             ;3F
    INC X                   ;40
    INC A                   ;41
    INC C                   ;42
    INC B                   ;43
    INC E                   ;44
    INC D                   ;45
    INC L                   ;46
    INC H                   ;47
    CMP A,!0abcdh           ;48 CD AB
    CMP A,[HL+0abh]         ;49 AB
    SET1 0fe20h.4           ;4A 20      saddr
    SET1 PSW.4              ;4A 1E
    CLR1 0fe20h.4           ;4B 20      saddr
    CLR1 PSW.4              ;4B 1E
    callf !0c00h            ;4C 00      4c = callf 0c00h-0cffh
    callf !0cffh            ;4C FF
    CMP A,#0abh             ;4D AB
    CMP A,0fe20h            ;4E 20      CMP A,0fe20h    (saddr = FE20H to FF1FH)
    CMP A,[HL]              ;4F
    DEC X                   ;50
    DEC A                   ;51
    DEC C                   ;52
    DEC B                   ;53
    DEC E                   ;54
    DEC D                   ;55
    DEC L                   ;56
    DEC H                   ;57
    AND A,!0abcdh           ;58 CD AB
    AND A,[HL+0abh]         ;59 AB
    SET1 0fe20h.5           ;5A 20      saddr
    SET1 PSW.5              ;5A 1E
    CLR1 0fe20h.5           ;5B 20      saddr
    CLR1 PSW.5              ;5B 1E
    callf !0d00h            ;5C 00      5c = callf 0d00h-0dffh
    callf !0dffh            ;5C FF
    AND A,#0abh             ;5D AB
    AND A,0fe20h            ;5E 20       AND A,saddr   (saddr = FE20H to FF1FH)
    AND A,[HL]              ;5F
    MOV A,X                 ;60
                            ;61         TODO
    MOV A,C                 ;62
    MOV A,B                 ;63
    MOV A,E                 ;64
    MOV A,D                 ;65
    MOV A,L                 ;66
    MOV A,H                 ;67
    OR A,!0abcdh            ;68 CD AB
    OR A,[HL+0abh]          ;69 AB
    SET1 0fe20h.6           ;6A 20      saddr
    SET1 PSW.6              ;6A 1E
    CLR1 0fe20h.6           ;6B 20      saddr
    CLR1 PSW.6              ;6B 1E
    callf !0e00h            ;6C 00      6c = callf 0e00h-0effh
    callf !0effh            ;6C FF
    OR A,#0abh              ;6D AB
    OR A,0fe20h             ;6E 20      OR A,saddr     (saddr = FE20H to FF1FH)
    OR A,[HL]               ;6F
    MOV X,A                 ;70
                            ;71         TODO
    MOV C,A                 ;72
    MOV B,A                 ;73
    MOV E,A                 ;74
    MOV D,A                 ;75
    MOV L,A                 ;76
    MOV H,A                 ;77
    XOR A,!0abcdh           ;78 CD AB
    XOR A,[HL+0abh]         ;79 AB
    SET1 0fe20h.7           ;7A 20      saddr
    SET1 PSW.7              ;7A 1E      TODO duplicate opcodes!
    EI                      ;7A 1E      TODO duplicate opcodes!
    CLR1 0fe20h.7           ;7B 20      saddr
    CLR1 PSW.7              ;7B 1E      TODO duplicate opcodes!
    DI                      ;7B 1E      TODO duplicate opcodes!
    callf !0f00h            ;7C 00      7c = callf 0f00h-0fffh
    callf !0fffh            ;7C FF
    XOR A,#0abh             ;7D AB
    XOR A,0fe20h            ;7E 20      XOR A,saddr     (saddr = FE20H to FF1FH)
    XOR A,[HL]              ;7F
    INCW AX                 ;80
    INC 0fe20h              ;81 20      INC saddr       (saddr = FE20H to FF1FH)
    INCW BC                 ;82
    XCH A,0fe20h            ;83 20      XCH A,saddr     (saddr = FE20H to FF1FH)
    INCW DE                 ;84
    MOV A,[DE]              ;85
    INCW HL                 ;86
    MOV A,[HL]              ;87
    ADD 0fe20h,#0abh        ;88 20 AB   ADD saddr,#byte (saddr = FE20H to FF1FH)
    MOVW AX,0fe20h          ;89 20      saddrp
    MOVW AX,SP              ;89 1C
label1:
    DBNZ C,$label1          ;8A FE
label2:
    DBNZ B,$label2          ;8B FE
label8:
    BT 0fe20h.0,$label8     ;8C 20 FD   saddr.0,$addr16
label9:
    BT PSW.0,$label9        ;8C 1E FD
label3:
    BC $label3              ;8D FE
    MOV A,!0abcdh           ;8E CD AB
    RETI                    ;8F
    DECW AX                 ;90
    DEC 0fe20h              ;91 20      DEC saddr       (saddr = FE20H to FF1FH)
    DECW BC                 ;92
    XCH A,0fffeh            ;93 FE      XCH A,sfr       (sfr = FF00H to FFFFH)
    DECW DE                 ;94
    MOV [DE],A              ;95
    DECW HL                 ;96
    MOV [HL],A              ;97
    SUB 0fe20h,#0abh        ;98 20 AB   SUB saddr,#byte (saddr = FE20H to FF1FH)
    MOVW 0fe20h,AX          ;99 20      saddrp,AX
    MOVW SP,AX              ;99 1C
    CALL !0abcdh            ;9A CD AB
    BR !0abcdh              ;9B CD AB
label10:
    BT 0fe20h.1,$label10    ;9C 20 FD  saddr.1,$addr16
label11:
    BT PSW.1,$label11       ;9C 1E FD
label4:
    BNC $label4             ;9D FE
    MOV !0abcdh,A           ;9E CD AB
    RETB                    ;9F
    MOV X,#0abh             ;A0 AB
    MOV A,#0abh             ;A1 AB
    MOV C,#0abh             ;A2 AB
    MOV B,#0abh             ;A3 AB
    MOV E,#0abh             ;A4 AB
    MOV D,#0abh             ;A5 AB
    MOV L,#0abh             ;A6 AB
    MOV H,#0abh             ;A7 AB
    ADDC 0fe20h,#0abh       ;A8 20 AB   ADDC saddr,#byte (saddr = FE20H to FF1FH)
    MOVW AX,0fffeh          ;A9 FE      MOVW AX,sfrp    (sfrp = FF00H to FFFFH, evens only)
    ;MOVW AX,0ffffh         ;           TODO RA78K0 error E2317: Even expression expected
    MOV A,[HL+C]            ;AA
    MOV A,[HL+B]            ;AB
label12:
    BT 0fe20h.2,$label12    ;AC 20 FD    BT saddr.2,$addr16
label13:
    BT PSW.2,$label13       ;AC 1E FD
label5:
    bz $label5              ;AD FE
    MOV A,[HL+0abh]         ;AE AB
    RET                     ;AF
    POP AX                  ;B0
    PUSH AX                 ;B1
    POP BC                  ;B2
    PUSH BC                 ;B3
    POP DE                  ;B4
    PUSH DE                 ;B5
    POP HL                  ;B6
    PUSH HL                 ;B7
    SUBC 0fe20h,#0abh       ;B8 20 AB   SUBC saddr,#byte (saddr = FE20H to FF1FH)
    MOVW 0fffeh,AX          ;B9 FE      MOVW sfrp,AX (sfrp = FF00H to FFFFH, evens only)
    ;MOVW 0ffffh,AX         ;           TODO RA78K0 error E2317: Even expression expected
    MOV [HL+C],A            ;BA
    MOV [HL+B],A            ;BB
label14:
    BT 0fe20h.3,$label14    ;BC 20 FD  saddr.3,$addr16
label15:
    BT PSW.3,$label15       ;BC 1E FD
label6:
    bnz $label6             ;BD FE
    MOV [HL+0abh],A         ;BE AB
    BRK
    ; 0xc0: 'MOVW AX,AX'             TODO RA78K0 error E2202: Illegal operand
    callt [0040H]           ;C1
    MOVW AX,BC              ;C2
    callt [0042H]           ;C3
    MOVW AX,DE              ;C4
    callt [0044H]           ;C5
    MOVW AX,HL              ;C6
    callt [0046H]           ;C7
    CMP 0fe20h,#0abh        ;C8 20 AB   CMP saddr,#byte (saddr = FE20H to FF1FH)
    callt [0048H]           ;C9
    ADDW AX,#0abcdh         ;CA CD AB
    callt [004aH]           ;CB
label16:
    BT 0fe20h.4,$label16    ;CC 20 FD saddr.4,$addr16
label17:
    BT PSW.4,$label17       ;CC 1E FD
    callt [004cH]           ;CD
    XCH A,!0abcdh           ;CE CD AB
    callt [004eH]           ;CF
    ; 0xd0: 'MOVW AX,AX'            TODO RA78K0 error E2202: Illegal operand
    callt [0050H]           ;D1
    MOVW BC,AX              ;D2
    callt [0052H]           ;D3
    MOVW DE,AX              ;D4
    callt [0054H]           ;D5
    MOVW HL,AX              ;D6
    callt [0056H]           ;D7
    AND 0fe20h,#0abh        ;D8 20 AB   AND saddr,#byte (saddr = FE20H to FF1FH)
    callt [0058H]           ;D9
    SUBW AX,#0abcdh         ;DA CD AB
    callt [005AH]           ;DB
label20:
    BT 0fe20h.5,$label20    ;DC 20 FD    BT saddr.5,$addr16
label21:
    BT PSW.5,$label21       ;DC 1E FD
    callt [005CH]           ;DD
    XCH A,[HL+0abh]         ;DE AB
    callt [005eh]           ;DF

    ; 0xe0: 'XCHW AX,AX'            TODO RA78K0 error E2202: Illegal operand

    callt [0060h]           ;E1
    XCHW AX,BC              ;E2
    callt [0062h]           ;E3
    XCHW AX,DE              ;E4
    callt [0064h]           ;E5
    XCHW AX,HL              ;E6
    callt [0066h]           ;E7
    OR 0fe20h,#0abh         ;E8 20 AB
    callt [0068h]           ;E9
    CMPW AX,#0abcdh         ;EA CD AB
    callt [006ah]           ;EB
label22:
    BT 0fe20h.6,$label22    ;EC 20 FD   BT saddr.6,$addr16
label23:
    BT PSW.6,$label23       ;EC 1E FD
    callt [006ch]           ;ED
    MOVW 0fe20h,#0abcdh     ;EE 20 CD AB    MOVW saddrp,#word
    MOVW SP,#0abcdh         ;EE 1C CD AB
    callt [006eh]           ;EF
    mov a,0fe20h            ;F0 20      saddr
    mov a,psw               ;F0 1E
    callt [0070h]           ;F1
    MOV 0fe20h,A            ;F2 20      saddr
    MOV PSW,A               ;F2 1E
    callt [0072h]           ;F3
    MOV A,0fffeh            ;F4 FF      MOV A,sfr (sfr = FF00H to FFFFH)
    callt [0074h]           ;F5
    MOV 0fffeh,A            ;F6 FE      MOV sfr,A (sfr = FF00H to FFFFH)
    callt [0076h]           ;F7
    XOR 0fe20h,#0abh        ;F8 20 AB   XOR saddr,#byte (saddr = FE20H to FF1FH)
    callt [0078h]           ;F9
label7:
    br $label7              ;FA FE
    callt [007ah]           ;FB
label18:
    BT 0fe20h.7,$label18    ;FC 20 FD  BT saddr.7,$addr16
label19:
    BT PSW.7,$label19       ;FC 1E FD
    callt [007ch]           ;FD
    MOVW 0fffeh,#0abcdh     ;FE FE CD AB    MOVW sfrp,#word (sfrp = FF00H to FFFFH, evens only)
    ;MOVW 0ffffh,#0abcdh    ;FE FE CD AB   TODO RA78K0 error E2317: Even expression expected
    callt [007eh]           ;FF

    end
