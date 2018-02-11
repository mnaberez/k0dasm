    org 0

    nop                         ;00
    not1 cy                     ;01
    movw ax,0fe20h              ;02 CE AB       saddrp
    MOVW 0fe20h,AX              ;03 CE AB       saddrp
label0:
    DBNZ 0fe20h,$label0         ;04 20 FD       saddr
    xch a,[de]                  ;05
    XCH A,[HL]                  ;07
    ADD A,!0abcdh               ;08 CD AB
    ADD A,[HL+0abh]             ;09 AB
    SET1 0fe20h.0               ;0A 20          saddr
    SET1 PSW.0                  ;0A 1E
    CLR1 0fe20h.0               ;0B 20          saddr
    CLR1 PSW.0                  ;0B 1E
    callf !0800h                ;0C 00          0c = callf 0800h-08ffh
    callf !08ffh                ;0C FF
    ADD A,#0abh                 ;0D AB
    ADD A,0fe20h                ;0E 20          saddr
    ADD A,[HL]                  ;0F
    MOVW AX,#0abcdh             ;10 CD AB
    MOV 0fe20h,#0abh            ;11 20 AB       saddr
    MOV PSW,#0abh               ;11 1E AB
    MOVW BC,#0abcdh             ;12 CD AB
    MOV 0fffeh, #0abh           ;13 FE AB       sfr
    MOVW DE,#0abcdh             ;14 CD AB
    MOVW HL,#0abcdh             ;16 CD AB
    SUB A,!0abcdh               ;18 CD AB
    SUB A,[HL+0abh]             ;19 AB
    SET1 0fe20h.1               ;1A 20          saddr
    SET1 PSW.1                  ;1A 1E
    CLR1 0fe20h.1               ;1B 20          saddr
    CLR1 PSW.1                  ;1B 1E
    callf !0900h                ;1C 00          1c = callf 0900h-09ffh
    callf !09ffh                ;1C FF
    SUB A,#0abh                 ;1D AB
    SUB A,0fe20h                ;1E 20          saddr
    SUB A,[HL]                  ;1F
    SET1 CY                     ;20
    CLR1 CY                     ;21
    PUSH PSW                    ;22
    POP PSW                     ;23
    ROR A,1                     ;24
    RORC A,1                    ;25
    ROL A,1                     ;26
    ROLC A,1                    ;27
    ADDC A,!0abcdh              ;28 CD AB
    ADDC A,[HL+0abh]            ;29 AB
    SET1 0fe20h.2               ;2A 20          saddr
    SET1 PSW.2                  ;2A 1E
    CLR1 0fe20h.2               ;2B 20          saddr
    CLR1 PSW.2                  ;2B 1E
    callf !0a00h                ;2C 00          2c = callf 0a00h-0affh
    callf !0affh                ;2C FF
    ADDC A,#0abh                ;2D AB
    ADDC A,0fe20h               ;2E 20          saddr
    ADDC A,[HL]                 ;2F
    XCH A,X                     ;30
    XCH A,[HL+B]                ;31 8B
    XCH A,[HL+C]                ;31 8A
    ADD A,[HL+B]                ;31 0B
    ADD A,[HL+C]                ;31 0A
    ADDC A,[HL+B]               ;31 2B
    ADDC A,[HL+C]               ;31 2A
    SUB A,[HL+B]                ;31 1B
    SUB A,[HL+C]                ;31 1A
    SUBC A,[HL+B]               ;31 3B
    SUBC A,[HL+C]               ;31 3A
    AND A,[HL+B]                ;31 5B
    AND A,[HL+C]                ;31 5A
    OR A,[HL+B]                 ;31 6B
    OR A,[HL+C]                 ;31 6A
    XOR A,[HL+B]                ;31 7B
    XOR A,[HL+C]                ;31 7A
    CMP A,[HL+B]                ;31 4B
    CMP A,[HL+C]                ;31 4A
    MULU X                      ;31 88
    DIVUW C                     ;31 82
    ROR4 [HL]                   ;31 90
    ROL4 [HL]                   ;31 80
    BR AX                       ;31 98

label24:
    BT 0fffeh.0,$label24        ;31 06 FE FC    sfr
label25:
    BT 0fffeh.1,$label25        ;31 16 FE FC    sfr
label26:
    BT 0fffeh.2,$label26        ;31 26 FE FC    sfr
label27:
    BT 0fffeh.3,$label27        ;31 36 FE FC    sfr
label28:
    BT 0fffeh.4,$label28        ;31 46 FE FC    sfr
label29:
    BT 0fffeh.5,$label29        ;31 56 FE FC    sfr
label30:
    BT 0fffeh.6,$label30        ;31 66 FE FC    sfr
label31:
    BT 0fffeh.7,$label31        ;31 76 FE FC    sfr

label32:
    BT A.0,$label32             ;31 0E FD
label33:
    BT A.1,$label33             ;31 1E FD
label34:
    BT A.2,$label34             ;31 2E FD
label35:
    BT A.3,$label35             ;31 3E FD
label36:
    BT A.4,$label36             ;31 4E FD
label37:
    BT A.5,$label37             ;31 5E FD
label38:
    BT A.6,$label38             ;31 6E FD
label39:
    BT A.7,$label39             ;31 7E FD

label40:
    BT [HL].0,$label40          ;31 86 FD
label41:
    BT [HL].1,$label41          ;31 96 FD
label42:
    BT [HL].2,$label42          ;31 A6 FD
label43:
    BT [HL].3,$label43          ;31 B6 FD
label44:
    BT [HL].4,$label44          ;31 C6 FD
label45:
    BT [HL].5,$label45          ;31 D6 FD
label46:
    BT [HL].6,$label46          ;31 E6 FD
label47:
    BT [HL].7,$label47          ;31 F6 FD

label48:
    BF 0fe20h.0,$label48        ;31 03 20 FC    saddr
label49:
    BF 0fe20h.1,$label49        ;31 13 20 FC    saddr
label50:
    BF 0fe20h.2,$label50        ;31 23 20 FC    saddr
label51:
    BF 0fe20h.3,$label51        ;31 33 20 FC    saddr
label52:
    BF 0fe20h.4,$label52        ;31 43 20 FC    saddr
label53:
    BF 0fe20h.5,$label53        ;31 53 20 FC    saddr
label54:
    BF 0fe20h.6,$label54        ;31 63 20 FC    saddr
label55:
    BF 0fe20h.7,$label55        ;31 73 20 FC    saddr

label56:
    BF 0fffeh.0,$label56        ;31 07 FE FC    sfr
label57:
    BF 0fffeh.1,$label57        ;31 17 FE FC    sfr
label58:
    BF 0fffeh.2,$label58        ;31 27 FE FC    sfr
label59:
    BF 0fffeh.3,$label59        ;31 37 FE FC    sfr
label60:
    BF 0fffeh.4,$label60        ;31 47 FE FC    sfr
label61:
    BF 0fffeh.5,$label61        ;31 57 FE FC    sfr
label62:
    BF 0fffeh.6,$label62        ;31 67 FE FC    sfr
label63:
    BF 0fffeh.7,$label63        ;31 77 FE FC    sfr

label64:
    BF A.0,$label64             ;31 0F FD
label65:
    BF A.1,$label65             ;31 1F FD
label66:
    BF A.2,$label66             ;31 2F FD
label67:
    BF A.3,$label67             ;31 3F FD
label68:
    BF A.4,$label68             ;31 4F FD
label69:
    BF A.5,$label69             ;31 5F FD
label70:
    BF A.6,$label70             ;31 6F FD
label71:
    BF A.7,$label71             ;31 7F FD

label72:
    BF PSW.0,$label72           ;31 03 1E FC
label73:
    BF PSW.1,$label73           ;31 13 1E FC
label74:
    BF PSW.2,$label74           ;31 23 1E FC
label75:
    BF PSW.3,$label75           ;31 33 1E FC
label76:
    BF PSW.4,$label76           ;31 43 1E FC
label77:
    BF PSW.5,$label77           ;31 53 1E FC
label78:
    BF PSW.6,$label78           ;31 63 1E FC
label79:
    BF PSW.7,$label79           ;31 73 1E FC

label80:
    BF [HL].0,$label80          ;31 87 FD
label81:
    BF [HL].1,$label81          ;31 97 FD
label82:
    BF [HL].2,$label82          ;31 A7 FD
label83:
    BF [HL].3,$label83          ;31 B7 FD
label84:
    BF [HL].4,$label84          ;31 C7 FD
label85:
    BF [HL].5,$label85          ;31 D7 FD
label86:
    BF [HL].6,$label86          ;31 E7 FD
label87:
    BF [HL].7,$label87          ;31 F7 FD

label88:
    BTCLR 0fe20h.0,$label88     ;31 01 20 FC    saddr
label89:
    BTCLR 0fe20h.1,$label89     ;31 11 20 FC    saddr
label90:
    BTCLR 0fe20h.2,$label90     ;31 21 20 FC    saddr
label91:
    BTCLR 0fe20h.3,$label91     ;31 31 20 FC    saddr
label92:
    BTCLR 0fe20h.4,$label92     ;31 41 20 FC    saddr
label93:
    BTCLR 0fe20h.5,$label93     ;31 51 20 FC    saddr
label94:
    BTCLR 0fe20h.6,$label94     ;31 61 20 FC    saddr
label95:
    BTCLR 0fe20h.7,$label95     ;31 71 20 FC    saddr

label96:
    BTCLR 0fffeh.0,$label96     ;31 05 FE FC    sfr
label97:
    BTCLR 0fffeh.1,$label97     ;31 15 FE FC    sfr
label98:
    BTCLR 0fffeh.2,$label98     ;31 25 FE FC    sfr
label99:
    BTCLR 0fffeh.3,$label99     ;31 35 FE FC    sfr
label100:
    BTCLR 0fffeh.4,$label100    ;31 45 FE FC    sfr
label101:
    BTCLR 0fffeh.5,$label101    ;31 55 FE FC    sfr
label102:
    BTCLR 0fffeh.6,$label102    ;31 65 FE FC    sfr
label103:
    BTCLR 0fffeh.7,$label103    ;31 75 FE FC    sfr

label104:
    BTCLR A.0,$label104         ;31 0D FD
label105:
    BTCLR A.1,$label105         ;31 1D FD
label106:
    BTCLR A.2,$label106         ;31 2D FD
label107:
    BTCLR A.3,$label107         ;31 3D FD
label108:
    BTCLR A.4,$label108         ;31 4D FD
label109:
    BTCLR A.5,$label109         ;31 5D FD
label110:
    BTCLR A.6,$label110         ;31 6D FD
label111:
    BTCLR A.7,$label111         ;31 7D FD

label112:
    BTCLR PSW.0,$label112       ;31 01 1E FC
label113:
    BTCLR PSW.1,$label113       ;31 11 1E FC
label114:
    BTCLR PSW.2,$label114       ;31 21 1E FC
label115:
    BTCLR PSW.3,$label115       ;31 31 1E FC
label116:
    BTCLR PSW.4,$label116       ;31 41 1E FC
label117:
    BTCLR PSW.5,$label117       ;31 51 1E FC
label118:
    BTCLR PSW.6,$label118       ;31 61 1E FC
label119:
    BTCLR PSW.7,$label119       ;31 71 1E FC

label120:
    BTCLR [HL].0,$label120      ;31 85 FD
label121:
    BTCLR [HL].1,$label121      ;31 95 FD
label122:
    BTCLR [HL].2,$label122      ;31 A5 FD
label123:
    BTCLR [HL].3,$label123      ;31 B5 FD
label124:
    BTCLR [HL].4,$label124      ;31 C5 FD
label125:
    BTCLR [HL].5,$label125      ;31 D5 FD
label126:
    BTCLR [HL].6,$label126      ;31 E5 FD
label127:
    BTCLR [HL].7,$label127      ;31 F5 FD

    XCH A,C                     ;32
    XCH A,B                     ;33
    XCH A,E                     ;34
    XCH A,D                     ;35
    XCH A,L                     ;36
    XCH A,H                     ;37
    SUBC A,!0abcdh              ;38 CD AB
    SUBC A,[HL+0abh]            ;39 AB
    SET1 0fe20h.3               ;3A 20          saddr
    SET1 PSW.3                  ;3A 1E
    CLR1 0fe20h.3               ;3B 20          saddr
    CLR1 PSW.3                  ;3B 1E
    callf !0b00h                ;3C 00          3c = callf 0b00h-0bffh
    callf !0bffh                ;3C FF
    SUBC A,#0abh                ;3D AB
    SUBC A,0fe20h               ;3E 20          saddr
    SUBC A,[HL]                 ;3F
    INC X                       ;40
    INC A                       ;41
    INC C                       ;42
    INC B                       ;43
    INC E                       ;44
    INC D                       ;45
    INC L                       ;46
    INC H                       ;47
    CMP A,!0abcdh               ;48 CD AB
    CMP A,[HL+0abh]             ;49 AB
    SET1 0fe20h.4               ;4A 20          saddr
    SET1 PSW.4                  ;4A 1E
    CLR1 0fe20h.4               ;4B 20          saddr
    CLR1 PSW.4                  ;4B 1E
    callf !0c00h                ;4C 00          4c = callf 0c00h-0cffh
    callf !0cffh                ;4C FF
    CMP A,#0abh                 ;4D AB
    CMP A,0fe20h                ;4E 20          saddr
    CMP A,[HL]                  ;4F
    DEC X                       ;50
    DEC A                       ;51
    DEC C                       ;52
    DEC B                       ;53
    DEC E                       ;54
    DEC D                       ;55
    DEC L                       ;56
    DEC H                       ;57
    AND A,!0abcdh               ;58 CD AB
    AND A,[HL+0abh]             ;59 AB
    SET1 0fe20h.5               ;5A 20          saddr
    SET1 PSW.5                  ;5A 1E
    CLR1 0fe20h.5               ;5B 20          saddr
    CLR1 PSW.5                  ;5B 1E
    callf !0d00h                ;5C 00          5c = callf 0d00h-0dffh
    callf !0dffh                ;5C FF
    AND A,#0abh                 ;5D AB
    AND A,0fe20h                ;5E 20          saddr
    AND A,[HL]                  ;5F
    MOV A,X                     ;60

    ADJBA                       ;61 80
    ADJBS                       ;61 90

    SEL RB0                     ;61 D0
    SEL RB1                     ;61 D8
    SEL RB2                     ;61 F0
    SEL RB3                     ;61 F8

    MOV1 CY,A.0                 ;61 8C
    MOV1 CY,A.1                 ;61 9C
    MOV1 CY,A.2                 ;61 AC
    MOV1 CY,A.3                 ;61 BC
    MOV1 CY,A.4                 ;61 CC
    MOV1 CY,A.5                 ;61 DC
    MOV1 CY,A.6                 ;61 EC
    MOV1 CY,A.7                 ;61 FC

    MOV1 A.0,CY                 ;61 89
    MOV1 A.1,CY                 ;61 99
    MOV1 A.2,CY                 ;61 A9
    MOV1 A.3,CY                 ;61 B9
    MOV1 A.4,CY                 ;61 C9
    MOV1 A.5,CY                 ;61 D9
    MOV1 A.6,CY                 ;61 E9
    MOV1 A.7,CY                 ;61 F9

    AND1 CY,A.0                 ;61 8D
    AND1 CY,A.1                 ;61 9D
    AND1 CY,A.2                 ;61 AD
    AND1 CY,A.3                 ;61 BD
    AND1 CY,A.4                 ;61 CD
    AND1 CY,A.5                 ;61 DD
    AND1 CY,A.6                 ;61 ED
    AND1 CY,A.7                 ;61 FD

    OR1 CY,A.0                  ;61 8E
    OR1 CY,A.1                  ;61 9E
    OR1 CY,A.2                  ;61 AE
    OR1 CY,A.3                  ;61 BE
    OR1 CY,A.4                  ;61 CE
    OR1 CY,A.5                  ;61 DE
    OR1 CY,A.6                  ;61 EE
    OR1 CY,A.7                  ;61 FE

    XOR1 CY,A.0                 ;61 8F
    XOR1 CY,A.1                 ;61 9F
    XOR1 CY,A.2                 ;61 AF
    XOR1 CY,A.3                 ;61 BF
    XOR1 CY,A.4                 ;61 CF
    XOR1 CY,A.5                 ;61 DF
    XOR1 CY,A.6                 ;61 EF
    XOR1 CY,A.7                 ;61 FF

    SET1 A.0                    ;61 8A
    SET1 A.1                    ;61 9A
    SET1 A.2                    ;61 AA
    SET1 A.3                    ;61 BA
    SET1 A.4                    ;61 CA
    SET1 A.5                    ;61 DA
    SET1 A.6                    ;61 EA
    SET1 A.7                    ;61 FA

    CLR1 A.0                    ;61 8B
    CLR1 A.1                    ;61 9B
    CLR1 A.2                    ;61 AB
    CLR1 A.3                    ;61 BB
    CLR1 A.4                    ;61 CB
    CLR1 A.5                    ;61 DB
    CLR1 A.6                    ;61 EB
    CLR1 A.7                    ;61 FB

    ADD A,X                     ;61 08
    ADD A,A                     ;61 01
    ADD A,C                     ;61 0A
    ADD A,B                     ;61 0B
    ADD A,E                     ;61 0C
    ADD A,D                     ;61 0D
    ADD A,L                     ;61 0E
    ADD A,H                     ;61 0F

    ADD X,A                     ;61 00
    ADD A,A                     ;61 01
    ADD C,A                     ;61 02
    ADD B,A                     ;61 03
    ADD E,A                     ;61 04
    ADD D,A                     ;61 05
    ADD L,A                     ;61 06
    ADD H,A                     ;61 07

    ADDC A,X                    ;61 28
    ADDC A,A                    ;61 21
    ADDC A,C                    ;61 2A
    ADDC A,B                    ;61 2B
    ADDC A,E                    ;61 2C
    ADDC A,D                    ;61 2D
    ADDC A,L                    ;61 2E
    ADDC A,H                    ;61 2F

    ADDC X,A                    ;61 20
    ADDC A,A                    ;61 21
    ADDC C,A                    ;61 22
    ADDC B,A                    ;61 23
    ADDC E,A                    ;61 24
    ADDC D,A                    ;61 25
    ADDC L,A                    ;61 26
    ADDC H,A                    ;61 27

    SUB A,X                     ;61 18
    SUB A,A                     ;61 11
    SUB A,C                     ;61 1A
    SUB A,B                     ;61 1B
    SUB A,E                     ;61 1C
    SUB A,D                     ;61 1D
    SUB A,L                     ;61 1E
    SUB A,H                     ;61 1F

    SUB X,A                     ;61 10
    SUB A,A                     ;61 11
    SUB C,A                     ;61 12
    SUB B,A                     ;61 13
    SUB E,A                     ;61 14
    SUB D,A                     ;61 15
    SUB L,A                     ;61 16
    SUB H,A                     ;61 17

    SUBC A,X                    ;61 38
    SUBC A,A                    ;61 31
    SUBC A,C                    ;61 3A
    SUBC A,B                    ;61 3B
    SUBC A,E                    ;61 3C
    SUBC A,D                    ;61 3D
    SUBC A,L                    ;61 3E
    SUBC A,H                    ;61 3F

    SUBC X,A                    ;61 30
    SUBC A,A                    ;61 31
    SUBC C,A                    ;61 32
    SUBC B,A                    ;61 33
    SUBC E,A                    ;61 34
    SUBC D,A                    ;61 35
    SUBC L,A                    ;61 36
    SUBC H,A                    ;61 37

    AND X,A                     ;61 50
    AND A,A                     ;61 51
    AND C,A                     ;61 52
    AND B,A                     ;61 53
    AND E,A                     ;61 54
    AND D,A                     ;61 55
    AND L,A                     ;61 56
    AND H,A                     ;61 57

    AND A,X                     ;61 58
    AND A,A                     ;61 51
    AND A,C                     ;61 5A
    AND A,B                     ;61 5B
    AND A,E                     ;61 5C
    AND A,D                     ;61 5D
    AND A,L                     ;61 5E
    AND A,H                     ;61 5F

    OR A,X                      ;61 68
    OR A,A                      ;61 61
    OR A,C                      ;61 6A
    OR A,B                      ;61 6B
    OR A,E                      ;61 6C
    OR A,D                      ;61 6D
    OR A,L                      ;61 6E
    OR A,H                      ;61 6F

    OR X,A                      ;61 60
    OR A,A                      ;61 61
    OR C,A                      ;61 62
    OR B,A                      ;61 63
    OR E,A                      ;61 64
    OR D,A                      ;61 65
    OR L,A                      ;61 66
    OR H,A                      ;61 67

    XOR A,X                     ;61 78
    XOR A,A                     ;61 71
    XOR A,C                     ;61 7A
    XOR A,B                     ;61 7B
    XOR A,E                     ;61 7C
    XOR A,D                     ;61 7D
    XOR A,L                     ;61 7E
    XOR A,H                     ;61 7F

    XOR X,A                     ;61 70
    XOR A,A                     ;61 71
    XOR C,A                     ;61 72
    XOR B,A                     ;61 73
    XOR E,A                     ;61 74
    XOR D,A                     ;61 75
    XOR L,A                     ;61 76
    XOR H,A                     ;61 77

    CMP A,X                     ;61 48
    CMP A,A                     ;61 41
    CMP A,C                     ;61 4A
    CMP A,B                     ;61 4B
    CMP A,E                     ;61 4C
    CMP A,D                     ;61 4D
    CMP A,L                     ;61 4E
    CMP A,H                     ;61 4F

    CMP X,A                     ;61 40
    CMP A,A                     ;61 41
    CMP C,A                     ;61 42
    CMP B,A                     ;61 43
    CMP E,A                     ;61 44
    CMP D,A                     ;61 45
    CMP L,A                     ;61 46
    CMP H,A                     ;61 47

    MOV A,C                     ;62
    MOV A,B                     ;63
    MOV A,E                     ;64
    MOV A,D                     ;65
    MOV A,L                     ;66
    MOV A,H                     ;67
    OR A,!0abcdh                ;68 CD AB
    OR A,[HL+0abh]              ;69 AB
    SET1 0fe20h.6               ;6A 20          saddr
    SET1 PSW.6                  ;6A 1E
    CLR1 0fe20h.6               ;6B 20          saddr
    CLR1 PSW.6                  ;6B 1E
    callf !0e00h                ;6C 00          6c = callf 0e00h-0effh
    callf !0effh                ;6C FF
    OR A,#0abh                  ;6D AB
    OR A,0fe20h                 ;6E 20          saddr
    OR A,[HL]                   ;6F
    MOV X,A                     ;70

    MOV1 CY,0fe20h.0            ;71 04 20       saddr
    MOV1 CY,0fe20h.1            ;71 14 20       saddr
    MOV1 CY,0fe20h.2            ;71 24 20       saddr
    MOV1 CY,0fe20h.3            ;71 34 20       saddr
    MOV1 CY,0fe20h.4            ;71 44 20       saddr
    MOV1 CY,0fe20h.5            ;71 54 20       saddr
    MOV1 CY,0fe20h.6            ;71 64 20       saddr
    MOV1 CY,0fe20h.7            ;71 74 20       saddr

    MOV1 CY,0fffeh.0            ;71 0C FE       sfr
    MOV1 CY,0fffeh.1            ;71 1C FE       sfr
    MOV1 CY,0fffeh.2            ;71 2C FE       sfr
    MOV1 CY,0fffeh.3            ;71 3C FE       sfr
    MOV1 CY,0fffeh.4            ;71 4C FE       sfr
    MOV1 CY,0fffeh.5            ;71 5C FE       sfr
    MOV1 CY,0fffeh.6            ;71 6C FE       sfr
    MOV1 CY,0fffeh.7            ;71 7C FE       sfr

    MOV1 CY,PSW.0               ;71 04 1E
    MOV1 CY,PSW.1               ;71 14 1E
    MOV1 CY,PSW.2               ;71 24 1E
    MOV1 CY,PSW.3               ;71 34 1E
    MOV1 CY,PSW.4               ;71 44 1E
    MOV1 CY,PSW.5               ;71 54 1E
    MOV1 CY,PSW.6               ;71 64 1E
    MOV1 CY,PSW.7               ;71 74 1E

    MOV1 CY,[HL].0              ;71 84
    MOV1 CY,[HL].1              ;71 94
    MOV1 CY,[HL].2              ;71 A4
    MOV1 CY,[HL].3              ;71 B4
    MOV1 CY,[HL].4              ;71 C4
    MOV1 CY,[HL].5              ;71 D4
    MOV1 CY,[HL].6              ;71 E4
    MOV1 CY,[HL].7              ;71 F4

    MOV1 0fe20h.0,CY            ;71 01 20       saddr
    MOV1 0fe20h.1,CY            ;71 11 20       saddr
    MOV1 0fe20h.2,CY            ;71 21 20       saddr
    MOV1 0fe20h.3,CY            ;71 31 20       saddr
    MOV1 0fe20h.4,CY            ;71 41 20       saddr
    MOV1 0fe20h.5,CY            ;71 51 20       saddr
    MOV1 0fe20h.6,CY            ;71 61 20       saddr
    MOV1 0fe20h.7,CY            ;71 71 20       saddr

    MOV1 0fffeh.0,CY            ;71 09 FE       sfr
    MOV1 0fffeh.1,CY            ;71 19 FE       sfr
    MOV1 0fffeh.2,CY            ;71 29 FE       sfr
    MOV1 0fffeh.3,CY            ;71 39 FE       sfr
    MOV1 0fffeh.4,CY            ;71 49 FE       sfr
    MOV1 0fffeh.5,CY            ;71 59 FE       sfr
    MOV1 0fffeh.6,CY            ;71 69 FE       sfr
    MOV1 0fffeh.7,CY            ;71 79 FE       sfr

    MOV1 PSW.0,CY               ;71 01 1E
    MOV1 PSW.1,CY               ;71 11 1E
    MOV1 PSW.2,CY               ;71 21 1E
    MOV1 PSW.3,CY               ;71 31 1E
    MOV1 PSW.4,CY               ;71 41 1E
    MOV1 PSW.5,CY               ;71 51 1E
    MOV1 PSW.6,CY               ;71 61 1E
    MOV1 PSW.7,CY               ;71 71 1E

    MOV1 [HL].0,CY              ;71 81
    MOV1 [HL].1,CY              ;71 91
    MOV1 [HL].2,CY              ;71 A1
    MOV1 [HL].3,CY              ;71 B1
    MOV1 [HL].4,CY              ;71 C1
    MOV1 [HL].5,CY              ;71 D1
    MOV1 [HL].6,CY              ;71 E1
    MOV1 [HL].7,CY              ;71 F1

    AND1 CY,0fe20h.0            ;71 05 20       saddr
    AND1 CY,0fe20h.1            ;71 15 20       saddr
    AND1 CY,0fe20h.2            ;71 25 20       saddr
    AND1 CY,0fe20h.3            ;71 35 20       saddr
    AND1 CY,0fe20h.4            ;71 45 20       saddr
    AND1 CY,0fe20h.5            ;71 55 20       saddr
    AND1 CY,0fe20h.6            ;71 65 20       saddr
    AND1 CY,0fe20h.7            ;71 75 20       saddr

    AND1 CY,0fffeh.0            ;71 0D FE       sfr
    AND1 CY,0fffeh.1            ;71 1D FE       sfr
    AND1 CY,0fffeh.2            ;71 2D FE       sfr
    AND1 CY,0fffeh.3            ;71 3D FE       sfr
    AND1 CY,0fffeh.4            ;71 4D FE       sfr
    AND1 CY,0fffeh.5            ;71 5D FE       sfr
    AND1 CY,0fffeh.6            ;71 6D FE       sfr
    AND1 CY,0fffeh.7            ;71 7D FE       sfr

    AND1 CY,PSW.0               ;71 05 1E
    AND1 CY,PSW.1               ;71 15 1E
    AND1 CY,PSW.2               ;71 25 1E
    AND1 CY,PSW.3               ;71 35 1E
    AND1 CY,PSW.4               ;71 45 1E
    AND1 CY,PSW.5               ;71 55 1E
    AND1 CY,PSW.6               ;71 65 1E
    AND1 CY,PSW.7               ;71 75 1E

    AND1 CY,[HL].0              ;71 85
    AND1 CY,[HL].1              ;71 95
    AND1 CY,[HL].2              ;71 A5
    AND1 CY,[HL].3              ;71 B5
    AND1 CY,[HL].4              ;71 C5
    AND1 CY,[HL].5              ;71 D5
    AND1 CY,[HL].6              ;71 E5
    AND1 CY,[HL].7              ;71 F5

    OR1 CY,0fe20h.0             ;71 06 20       saddr
    OR1 CY,0fe20h.1             ;71 16 20       saddr
    OR1 CY,0fe20h.2             ;71 26 20       saddr
    OR1 CY,0fe20h.3             ;71 36 20       saddr
    OR1 CY,0fe20h.4             ;71 46 20       saddr
    OR1 CY,0fe20h.5             ;71 56 20       saddr
    OR1 CY,0fe20h.6             ;71 66 20       saddr
    OR1 CY,0fe20h.7             ;71 76 20       saddr

    OR1 CY,0fffeh.0             ;71 0E FE       sfr
    OR1 CY,0fffeh.1             ;71 1E FE       sfr
    OR1 CY,0fffeh.2             ;71 2E FE       sfr
    OR1 CY,0fffeh.3             ;71 3E FE       sfr
    OR1 CY,0fffeh.4             ;71 4E FE       sfr
    OR1 CY,0fffeh.5             ;71 5E FE       sfr
    OR1 CY,0fffeh.6             ;71 6E FE       sfr
    OR1 CY,0fffeh.7             ;71 7E FE       sfr

    OR1 CY,PSW.0                ;71 06 1E
    OR1 CY,PSW.1                ;71 16 1E
    OR1 CY,PSW.2                ;71 26 1E
    OR1 CY,PSW.3                ;71 36 1E
    OR1 CY,PSW.4                ;71 46 1E
    OR1 CY,PSW.5                ;71 56 1E
    OR1 CY,PSW.6                ;71 66 1E
    OR1 CY,PSW.7                ;71 76 1E

    OR1 CY,[HL].0               ;71 86
    OR1 CY,[HL].1               ;71 96
    OR1 CY,[HL].2               ;71 A6
    OR1 CY,[HL].3               ;71 B6
    OR1 CY,[HL].4               ;71 C6
    OR1 CY,[HL].5               ;71 D6
    OR1 CY,[HL].6               ;71 E6
    OR1 CY,[HL].7               ;71 F6

    XOR1 CY,0fe20h.0            ;71 07 20       saddr
    XOR1 CY,0fe20h.1            ;71 17 20       saddr
    XOR1 CY,0fe20h.2            ;71 27 20       saddr
    XOR1 CY,0fe20h.3            ;71 37 20       saddr
    XOR1 CY,0fe20h.4            ;71 47 20       saddr
    XOR1 CY,0fe20h.5            ;71 57 20       saddr
    XOR1 CY,0fe20h.6            ;71 67 20       saddr
    XOR1 CY,0fe20h.7            ;71 77 20       saddr

    XOR1 CY,0fffeh.0            ;71 0F FE       sfr
    XOR1 CY,0fffeh.1            ;71 1F FE       sfr
    XOR1 CY,0fffeh.2            ;71 2F FE       sfr
    XOR1 CY,0fffeh.3            ;71 3F FE       sfr
    XOR1 CY,0fffeh.4            ;71 4F FE       sfr
    XOR1 CY,0fffeh.5            ;71 5F FE       sfr
    XOR1 CY,0fffeh.6            ;71 6F FE       sfr
    XOR1 CY,0fffeh.7            ;71 7F FE       sfr

    XOR1 CY,PSW.0               ;71 07 1E
    XOR1 CY,PSW.1               ;71 17 1E
    XOR1 CY,PSW.2               ;71 27 1E
    XOR1 CY,PSW.3               ;71 37 1E
    XOR1 CY,PSW.4               ;71 47 1E
    XOR1 CY,PSW.5               ;71 57 1E
    XOR1 CY,PSW.6               ;71 67 1E
    XOR1 CY,PSW.7               ;71 77 1E

    XOR1 CY,[HL].0              ;71 87
    XOR1 CY,[HL].1              ;71 97
    XOR1 CY,[HL].2              ;71 A7
    XOR1 CY,[HL].3              ;71 B7
    XOR1 CY,[HL].4              ;71 C7
    XOR1 CY,[HL].5              ;71 D7
    XOR1 CY,[HL].6              ;71 E7
    XOR1 CY,[HL].7              ;71 F7

    SET1 0fffeh.0               ;71 0A FE       sfr
    SET1 0fffeh.1               ;71 1A FE       sfr
    SET1 0fffeh.2               ;71 2A FE       sfr
    SET1 0fffeh.3               ;71 3A FE       sfr
    SET1 0fffeh.4               ;71 4A FE       sfr
    SET1 0fffeh.5               ;71 5A FE       sfr
    SET1 0fffeh.6               ;71 6A FE       sfr
    SET1 0fffeh.7               ;71 7A FE       sfr

    SET1 [HL].0                 ;71 82
    SET1 [HL].1                 ;71 92
    SET1 [HL].2                 ;71 A2
    SET1 [HL].3                 ;71 B2
    SET1 [HL].4                 ;71 C2
    SET1 [HL].5                 ;71 D2
    SET1 [HL].6                 ;71 E2
    SET1 [HL].7                 ;71 F2

    CLR1 0fffeh.0               ;71 0B FE       sfr
    CLR1 0fffeh.1               ;71 1B FE       sfr
    CLR1 0fffeh.2               ;71 2B FE       sfr
    CLR1 0fffeh.3               ;71 3B FE       sfr
    CLR1 0fffeh.4               ;71 4B FE       sfr
    CLR1 0fffeh.5               ;71 5B FE       sfr
    CLR1 0fffeh.6               ;71 6B FE       sfr
    CLR1 0fffeh.7               ;71 7B FE       sfr

    CLR1 [HL].0                 ;71 83
    CLR1 [HL].1                 ;71 93
    CLR1 [HL].2                 ;71 A3
    CLR1 [HL].3                 ;71 B3
    CLR1 [HL].4                 ;71 C3
    CLR1 [HL].5                 ;71 D3
    CLR1 [HL].6                 ;71 E3
    CLR1 [HL].7                 ;71 F3

    HALT                        ;71 10
    STOP                        ;71 00

    MOV C,A                     ;72
    MOV B,A                     ;73
    MOV E,A                     ;74
    MOV D,A                     ;75
    MOV L,A                     ;76
    MOV H,A                     ;77
    XOR A,!0abcdh               ;78 CD AB
    XOR A,[HL+0abh]             ;79 AB
    SET1 0fe20h.7               ;7A 20          saddr
    SET1 PSW.7                  ;7A 1E
    EI                          ;7A 1E          alias for SET1 PSW.7
    CLR1 0fe20h.7               ;7B 20          saddr
    CLR1 PSW.7                  ;7B 1E
    DI                          ;7B 1E          alias for CLR1 PSW.7
    callf !0f00h                ;7C 00          7c = callf 0f00h-0fffh
    callf !0fffh                ;7C FF
    XOR A,#0abh                 ;7D AB
    XOR A,0fe20h                ;7E 20          saddr
    XOR A,[HL]                  ;7F
    INCW AX                     ;80
    INC 0fe20h                  ;81 20          saddr
    INCW BC                     ;82
    XCH A,0fe20h                ;83 20          saddr
    INCW DE                     ;84
    MOV A,[DE]                  ;85
    INCW HL                     ;86
    MOV A,[HL]                  ;87
    ADD 0fe20h,#0abh            ;88 20 AB       saddr
    MOVW AX,0fe20h              ;89 20          saddrp
    MOVW AX,SP                  ;89 1C
label1:
    DBNZ C,$label1              ;8A FE
label2:
    DBNZ B,$label2              ;8B FE
label8:
    BT 0fe20h.0,$label8         ;8C 20 FD       saddr
label9:
    BT PSW.0,$label9            ;8C 1E FD
label3:
    BC $label3                  ;8D FE
    MOV A,!0abcdh               ;8E CD AB
    RETI                        ;8F
    DECW AX                     ;90
    DEC 0fe20h                  ;91 20          saddr
    DECW BC                     ;92
    XCH A,0fffeh                ;93 FE          sfr
    DECW DE                     ;94
    MOV [DE],A                  ;95
    DECW HL                     ;96
    MOV [HL],A                  ;97
    SUB 0fe20h,#0abh            ;98 20 AB       saddr
    MOVW 0fe20h,AX              ;99 20          saddrp
    MOVW SP,AX                  ;99 1C
    CALL !0abcdh                ;9A CD AB
    BR !0abcdh                  ;9B CD AB
label10:
    BT 0fe20h.1,$label10        ;9C 20 FD       saddr
label11:
    BT PSW.1,$label11           ;9C 1E FD
label4:
    BNC $label4                 ;9D FE
    MOV !0abcdh,A               ;9E CD AB
    RETB                        ;9F
    MOV X,#0abh                 ;A0 AB
    MOV A,#0abh                 ;A1 AB
    MOV C,#0abh                 ;A2 AB
    MOV B,#0abh                 ;A3 AB
    MOV E,#0abh                 ;A4 AB
    MOV D,#0abh                 ;A5 AB
    MOV L,#0abh                 ;A6 AB
    MOV H,#0abh                 ;A7 AB
    ADDC 0fe20h,#0abh           ;A8 20 AB       saddr
    MOVW AX,0fffeh              ;A9 FE          sfrp
    MOV A,[HL+C]                ;AA
    MOV A,[HL+B]                ;AB
label12:
    BT 0fe20h.2,$label12        ;AC 20 FD       saddr
label13:
    BT PSW.2,$label13           ;AC 1E FD
label5:
    bz $label5                  ;AD FE
    MOV A,[HL+0abh]             ;AE AB
    RET                         ;AF
    POP AX                      ;B0
    PUSH AX                     ;B1
    POP BC                      ;B2
    PUSH BC                     ;B3
    POP DE                      ;B4
    PUSH DE                     ;B5
    POP HL                      ;B6
    PUSH HL                     ;B7
    SUBC 0fe20h,#0abh           ;B8 20 AB       saddr
    MOVW 0fffeh,AX              ;B9 FE          sfrp
    MOV [HL+C],A                ;BA
    MOV [HL+B],A                ;BB
label14:
    BT 0fe20h.3,$label14        ;BC 20 FD       saddr
label15:
    BT PSW.3,$label15           ;BC 1E FD
label6:
    bnz $label6                 ;BD FE
    MOV [HL+0abh],A             ;BE AB
    BRK                         ;BF
    callt [0040H]               ;C1
    MOVW AX,BC                  ;C2
    callt [0042H]               ;C3
    MOVW AX,DE                  ;C4
    callt [0044H]               ;C5
    MOVW AX,HL                  ;C6
    callt [0046H]               ;C7
    CMP 0fe20h,#0abh            ;C8 20 AB       saddr
    callt [0048H]               ;C9
    ADDW AX,#0abcdh             ;CA CD AB
    callt [004aH]               ;CB
label16:
    BT 0fe20h.4,$label16        ;CC 20 FD       saddr
label17:
    BT PSW.4,$label17           ;CC 1E FD
    callt [004cH]               ;CD
    XCH A,!0abcdh               ;CE CD AB
    callt [004eH]               ;CF
    callt [0050H]               ;D1
    MOVW BC,AX                  ;D2
    callt [0052H]               ;D3
    MOVW DE,AX                  ;D4
    callt [0054H]               ;D5
    MOVW HL,AX                  ;D6
    callt [0056H]               ;D7
    AND 0fe20h,#0abh            ;D8 20 AB       saddr
    callt [0058H]               ;D9
    SUBW AX,#0abcdh             ;DA CD AB
    callt [005AH]               ;DB
label20:
    BT 0fe20h.5,$label20        ;DC 20 FD       saddr
label21:
    BT PSW.5,$label21           ;DC 1E FD
    callt [005CH]               ;DD
    XCH A,[HL+0abh]             ;DE AB
    callt [005eh]               ;DF
    callt [0060h]               ;E1
    XCHW AX,BC                  ;E2
    callt [0062h]               ;E3
    XCHW AX,DE                  ;E4
    callt [0064h]               ;E5
    XCHW AX,HL                  ;E6
    callt [0066h]               ;E7
    OR 0fe20h,#0abh             ;E8 20 AB
    callt [0068h]               ;E9
    CMPW AX,#0abcdh             ;EA CD AB
    callt [006ah]               ;EB
label22:
    BT 0fe20h.6,$label22        ;EC 20 FD       saddr
label23:
    BT PSW.6,$label23           ;EC 1E FD
    callt [006ch]               ;ED
    MOVW 0fe20h,#0abcdh         ;EE 20 CD AB    saddrp
    MOVW SP,#0abcdh             ;EE 1C CD AB
    callt [006eh]               ;EF
    mov a,0fe20h                ;F0 20          saddr
    mov a,psw                   ;F0 1E
    callt [0070h]               ;F1
    MOV 0fe20h,A                ;F2 20          saddr
    MOV PSW,A                   ;F2 1E
    callt [0072h]               ;F3
    MOV A,0fffeh                ;F4 FF          sfr
    callt [0074h]               ;F5
    MOV 0fffeh,A                ;F6 FE          sfr
    callt [0076h]               ;F7
    XOR 0fe20h,#0abh            ;F8 20 AB       saddr
    callt [0078h]               ;F9
label7:
    br $label7                  ;FA FE
    callt [007ah]               ;FB
label18:
    BT 0fe20h.7,$label18        ;FC 20 FD       saddr
label19:
    BT PSW.7,$label19           ;FC 1E FD
    callt [007ch]               ;FD
    MOVW 0fffeh,#0abcdh         ;FE FE CD AB    sfrp
    callt [007eh]               ;FF

    end
