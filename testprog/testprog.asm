    org 0

    nop                 ;00
    not1 cy             ;01
    ;movw ax,!0abcdh    ;           RA78K0 error E2317: Even expression expected
    movw ax,!0abceh     ;02 CE AB
    ;MOVW !0abcdh,AX    ;           RA78K0 error E2317: Even expression expected
    MOVW !0abceh,AX     ;03 CE AB
    ;DBNZ saddr,$addr16 ;4          TODO
    xch a,[de]          ;05
                        ;06         06 is Illegal
    XCH A,[HL]          ;07
    ADD A,!0abcdh       ;08 CD AB
    ADD A,[HL+0abh]     ;09 AB
    ;callf !0           ;0c         TODO
    ADD A,#0abh         ;0D AB
    ADD A,0fe20h        ;0E 20      ADD A,saddr     (saddr = FE20H to FF1FH)
    ADD A,[HL]          ;0F
    MOVW AX,#0abcdh     ;10 CD AB
                        ;11         TODO
    MOVW BC,#0abcdh     ;12 CD AB
    MOV 0fffeh, #0abh   ;13 FE AB   MOV sfr, #byte  (sfr = FF00H to FFFFH)
    MOVW DE,#0abcdh     ;14 CD AB
                        ;15         15 is Illegal
    MOVW HL,#0abcdh     ;16 CD AB
                        ;17         17 is Illegal
    SUB A,!0abcdh       ;18 CD AB
    SUB A,[HL+0abh]     ;19 AB
                        ;1A         TODO
                        ;1B         TODO
    ;0x1c: 'CALLF !1'   ;1C         TODO
    SUB A,#0abh         ;1D AB
    SUB A,0fe20h        ;1E 20      SUB A,saddr     (saddr = FE20H to FF1FH)
    SUB A,[HL]          ;1F
    SET1 CY             ;20
    CLR1 CY             ;21
    PUSH PSW            ;22
    POP PSW             ;23
    ROR A,1             ;24
    RORC A,1            ;25
    ROL A,1             ;26
    ROLC A,1            ;27
    ADDC A,!0abcdh      ;28 CD AB
    ADDC A,[HL+0abh]    ;29 AB
    ;0x2c: 'CALLF !2'   ;           TODO
    ADDC A,#0abh        ;2D AB
    ADDC A,0fe20h       ;2E 20      ADDC A,0fe20h   (saddr = FE20H to FF1FH)
    ADDC A,[HL]         ;2F
    XCH A,X             ;30
                        ;31         TODO
    XCH A,C             ;32
    XCH A,B             ;33
    XCH A,E             ;34
    XCH A,D             ;35
    XCH A,L             ;36
    XCH A,H             ;37
    SUBC A,!0abcdh      ;38 CD AB
    SUBC A,[HL+0abh]    ;39 AB
                        ;3A         TODO
                        ;3B         TODO
    ; 0x3c: 'CALLF !3'              TODO
    SUBC A,#0abh        ;3D AB
    SUBC A,0fe20h       ;3E 20      SUBC A,saddr    (saddr = FE20H to FF1FH)
    SUBC A,[HL]         ;3F
    INC X               ;40
    INC A               ;41
    INC C               ;42
    INC B               ;43
    INC E               ;44
    INC D               ;45
    INC L               ;46
    INC H               ;47
    CMP A,!0abcdh       ;48 CD AB
    CMP A,[HL+0abh]     ;49 AB
                        ;4A         TODO
                        ;4B         TODO
    ;CALLF !4           ;4C         TODO
    CMP A,#0abh         ;4D AB
    CMP A,0fe20h        ;4E 20      CMP A,0fe20h    (saddr = FE20H to FF1FH)
    CMP A,[HL]          ;4F
    DEC X               ;50
    DEC A               ;51
    DEC C               ;52
    DEC B               ;53
    DEC E               ;54
    DEC D               ;55
    DEC L               ;56
    DEC H               ;57
    AND A,!0abcdh       ;58 CD AB
    AND A,[HL+0abh]     ;59 AB
                        ;5A         TODO
                        ;5B         TODO
    ; 0x5c: 'CALLF !5'  TODO
    AND A,#0abh         ;5D AB
    AND A,0fe20h        ;5E 20       AND A,saddr   (saddr = FE20H to FF1FH)
    AND A,[HL]          ;5F
    MOV A,X             ;60
                        ;61         TODO
    MOV A,C             ;62
    MOV A,B             ;63
    MOV A,E             ;64
    MOV A,D             ;65
    MOV A,L             ;66
    MOV A,H             ;67
    OR A,!0abcdh        ;68 CD AB
    OR A,[HL+0abh]      ;69 AB
                        ;6A         TODO
                        ;6B         TODO
    ; 0x6c: 'CALLF !6'  ;6C
    OR A,#0abh          ;6D AB
    OR A,0fe20h         ;6E 20      OR A,saddr     (saddr = FE20H to FF1FH)
    OR A,[HL]           ;6F
    MOV X,A             ;70
                        ;71         TODO
    MOV C,A             ;72
    MOV B,A             ;73
    MOV E,A             ;74
    MOV D,A             ;75
    MOV L,A             ;76
    MOV H,A             ;77
    XOR A,!0abcdh       ;78 CD AB
    XOR A,[HL+0abh]     ;79 AB
                        ;7a         TODO
                        ;7b         TODO
    ; 0x7c: 'CALLF !7'              TODO
    XOR A,#0abh         ;7D AB
    XOR A,0fe20h        ;7E 20      XOR A,saddr     (saddr = FE20H to FF1FH)
    XOR A,[HL]          ;7F
    INCW AX             ;80
    INC 0fe20h          ;81 20      INC saddr       (saddr = FE20H to FF1FH)
    INCW BC             ;82
    XCH A,0fe20h        ;83 20      XCH A,saddr     (saddr = FE20H to FF1FH)
    INCW DE             ;84
    MOV A,[DE]          ;85
    INCW HL             ;86
    MOV A,[HL]          ;87
    ADD 0fe20h,#0abh    ;88 20 AB   ADD saddr,#byte (saddr = FE20H to FF1FH)
    ; 0x8a: DBNZ C,$addr16          TODO
    ; 0x8b: 'DBNZ B,$addr16'        TODO
    ; 0x8c:                         TODO
    ; 0x8d: 'BC $addr16'            TODO
    MOV A,!0abcdh       ;8E CD AB
    RETI                ;8F
    DECW AX             ;90
    DEC 0fe20h          ;91 20      DEC saddr       (saddr = FE20H to FF1FH)
    DECW BC             ;92
    XCH A,0fffeh        ;93 FE      XCH A,sfr       (sfr = FF00H to FFFFH)
    DECW DE             ;94
    MOV [DE],A          ;95
    DECW HL             ;96
    MOV [HL],A          ;97
    SUB 0fe20h,#0abh    ;98 20 AB   SUB saddr,#byte (saddr = FE20H to FF1FH)
    CALL !0abcdh        ;9A CD AB
    BR !0abcdh          ;9B CD AB
                        ;9C         TODO
    ; 0x9d: 'BNC $addr16'           TODO
    MOV !0abcdh,A       ;9E CD AB
    RETB                ;9F
    MOV X,#0abh         ;A0 AB
    MOV A,#0abh         ;A1 AB
    MOV C,#0abh         ;A2 AB
    MOV B,#0abh         ;A3 AB
    MOV E,#0abh         ;A4 AB
    MOV D,#0abh         ;A5 AB
    MOV L,#0abh         ;A6 AB
    MOV H,#0abh         ;A7 AB
    ADDC 0fe20h,#0abh   ;A8 20 AB   ADDC saddr,#byte (saddr = FE20H to FF1FH)
    MOVW AX,0fffeh      ;A9 FE      MOVW AX,sfrp    (sfrp = FF00H to FFFFH, evens only)
    ;MOVW AX,0ffffh     ;           TODO RA78K0 error E2317: Even expression expected
    MOV A,[HL+C]        ;AA
    MOV A,[HL+B]        ;AB
    ; 0xad: 'BZ $addr16'            TODO
    MOV A,[HL+0abh]     ;AE AB
    RET                 ;AF
    POP AX              ;B0
    PUSH AX             ;B1
    POP BC              ;B2
    PUSH BC             ;B3
    POP DE              ;B4
    PUSH DE             ;B5
    POP HL              ;B6
    PUSH HL             ;B7
    SUBC 0fe20h,#0abh   ;B8 20 AB   SUBC saddr,#byte (saddr = FE20H to FF1FH)
    MOVW 0fffeh,AX      ;B9 FE      MOVW sfrp,AX (sfrp = FF00H to FFFFH, evens only)
    ;MOVW 0ffffh,AX     ;           TODO RA78K0 error E2317: Even expression expected
    MOV [HL+C],A        ;BA
    MOV [HL+B],A        ;BB
    ; 0xbd: 'BNZ $addr16'           TODO
    MOV [HL+0abh],A     ;BE AB
    BRK
    ; 0xc0: 'MOVW AX,AX'             TODO RA78K0 error E2202: Illegal operand
    ; 0xc1: 'CALLT [0]'              TODO RA78K0 error E2313: Operand out of range (addr5)
    MOVW AX,BC          ;C2
    ; 0xc3: 'CALLT [1]'             TODO
    MOVW AX,DE          ;C4
    ; 0xc5: 'CALLT [2]'             TODO
    MOVW AX,HL          ;C6
    ; 0xc7: 'CALLT [3]'             TODO
    CMP 0fe20h,#0abh    ;C8 20 AB   CMP saddr,#byte (saddr = FE20H to FF1FH)
    ; 0xc9: 'CALLT [4]'             TODO
    ADDW AX,#0abcdh     ;CA CD AB
    ; 0xcb: 'CALLT [5]'             TODO
    ; 0xcd: 'CALLT [6]'             TODO
    XCH A,!0abcdh       ;CE CD AB
    ; 0xcf: 'CALLT [7]'             TODO
    ; 0xd0: 'MOVW AX,AX'            TODO RA78K0 error E2202: Illegal operand
    ; 0xd1: 'CALLT [8]'             TODO
    MOVW BC,AX          ;D2
    ; 0xd3: 'CALLT [9]'             TODO
    MOVW DE,AX          ;D4
    ; 0xd5: 'CALLT [10]'            TODO
    MOVW HL,AX          ;D6
    ; 0xd7: 'CALLT [11]'            TODO
    AND 0fe20h,#0abh    ;D8 20 AB   AND saddr,#byte (saddr = FE20H to FF1FH)
    ; 0xd9: 'CALLT [12]'            TODO
    SUBW AX,#0abcdh     ;DA CD AB
    ; 0xdb: 'CALLT [13]'            TODO
    ; 0xdd: 'CALLT [14]'            TODO
    XCH A,[HL+0abh]     ;DE AB
    ; 0xdf: 'CALLT [15]'            TODO
    ; 0xe0: 'XCHW AX,AX'            TODO RA78K0 error E2202: Illegal operand
    ; 0xe1: 'CALLT [16]'            TODO
    XCHW AX,BC          ;E2
    ; 0xe3: 'CALLT [17]'            TODO
    XCHW AX,DE          ;E4
    ; 0xe5: 'CALLT [18]'            TODO
    XCHW AX,HL          ;E6
    ; 0xe7: 'CALLT [19]'            TODO
    OR 0fe20h,#0abh     ;E8 20 AB
    ; 0xe9: 'CALLT [20]'            TODO
    CMPW AX,#0abcdh     ;EA CD AB
    ;0xeb: 'CALLT [21]'             TODO
    ;0xed: 'CALLT [22]'             TODO
    ;0xef: 'CALLT [23]'             TODO
    ;0xf1: 'CALLT [24]'             TODO
    ;0xf3: 'CALLT [25]'             TODO
    MOV A,0fffeh        ;F4 FF      MOV A,sfr (sfr = FF00H to FFFFH)
    ; 0xf5: 'CALLT [26]'            TODO
    ; 0xf6: 'MOV sfr,A'             TODO
    MOV 0fffeh,A        ;F6 FE      MOV sfr,A (sfr = FF00H to FFFFH)
    ; 0xf7: 'CALLT [27]'            TODO
    XOR 0fe20h,#0abh    ;F8 20 AB   XOR saddr,#byte (saddr = FE20H to FF1FH)
    ; 0xf9: 'CALLT [28]'            TODO
    ; 0xfa: 'BR $addr16'            TODO
    ; 0xfb: 'CALLT [29]'            TODO
    ; 0xfd: 'CALLT [30]'            TODO
    MOVW 0fffeh,#0abcdh ;FE FE CD AB    MOVW sfrp,#word (sfrp = FF00H to FFFFH, evens only)
    ;MOVW 0ffffh,#0abcdh ;FE FE CD AB   TODO RA78K0 error E2317: Even expression expected
    ; 0xff: 'CALLT [31]'            TODO


    end
