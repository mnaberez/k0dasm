    .area CODE1 (ABS)
    .org 0

    nop                         ;00             two nops are also reset vector
    nop                         ;00
    not1 cy                     ;01
    movw ax,!0xabce             ;02 ce ab       addr16p
    movw !0xabce,ax             ;03 ce ab       addr16p
label0:
    dbnz @0xfe20,label0         ;04 20 fd       saddr
    xch a,[de]                  ;05
    xch a,[hl]                  ;07
    add a,!0xabcd               ;08 cd ab
    add a,[hl+0xab]             ;09 ab
    set1 @0xfe20.0              ;0a 20          saddr
    set1 psw.0                  ;0a 1e
    clr1 @0xfe20.0              ;0b 20          saddr
    clr1 psw.0                  ;0b 1e
    callf !0x0800               ;0c 00          0c = callf 0800h-08ffh
    callf !0x08ff               ;0c ff
    add a,#0xab                 ;0d ab
    add a,@0xfe20               ;0e 20          saddr
    add a,[hl]                  ;0f
    movw ax,#0xabcd             ;10 cd ab
    mov @0xfe20,#0xab           ;11 20 ab       saddr

;XXX
;    mov psw,#0xab               ;11 1e ab
    .byte 0x11, 0x1e, 0xab

    movw bc,#0xabcd             ;12 cd ab
    mov *0xfffe, #0xab          ;13 fe ab       sfr
    movw de,#0xabcd             ;14 cd ab
    movw hl,#0xabcd             ;16 cd ab
    sub a,!0xabcd               ;18 cd ab
    sub a,[hl+0xab]             ;19 ab
    set1 @0xfe20.1              ;1a 20          saddr
    set1 psw.1                  ;1a 1e
    clr1 @0xfe20.1              ;1b 20          saddr
    clr1 psw.1                  ;1b 1e
    callf !0x0900               ;1c 00          1c = callf 0900h-09ffh
    callf !0x09ff               ;1c ff
    sub a,#0xab                 ;1d ab
    sub a,@0xfe20               ;1e 20          saddr
    sub a,[hl]                  ;1f
    set1 cy                     ;20
    clr1 cy                     ;21

;XXX
;    push psw                   ;22
    .byte 0x22

;XXX
;   pop psw                     ;23
    .byte 0x23

    ror a,1                     ;24
    rorc a,1                    ;25
    rol a,1                     ;26
    rolc a,1                    ;27
    addc a,!0xabcd              ;28 cd ab
    addc a,[hl+0xab]            ;29 ab
    set1 @0xfe20.2              ;2a 20          saddr
    set1 psw.2                  ;2a 1e
    clr1 @0xfe20.2              ;2b 20          saddr
    clr1 psw.2                  ;2b 1e
    callf !0x0a00               ;2c 00          2c = callf 0a00h-0affh
    callf !0x0aff               ;2c ff
    addc a,#0xab                ;2d ab
    addc a,@0xfe20              ;2e 20          saddr
    addc a,[hl]                 ;2f
    xch a,x                     ;30
    xch a,[hl+b]                ;31 8b
    xch a,[hl+c]                ;31 8a
    add a,[hl+b]                ;31 0b
    add a,[hl+c]                ;31 0a
    addc a,[hl+b]               ;31 2b
    addc a,[hl+c]               ;31 2a
    sub a,[hl+b]                ;31 1b
    sub a,[hl+c]                ;31 1a
    subc a,[hl+b]               ;31 3b
    subc a,[hl+c]               ;31 3a
    and a,[hl+b]                ;31 5b
    and a,[hl+c]                ;31 5a
    or a,[hl+b]                 ;31 6b
    or a,[hl+c]                 ;31 6a
    xor a,[hl+b]                ;31 7b
    xor a,[hl+c]                ;31 7a
    cmp a,[hl+b]                ;31 4b
    cmp a,[hl+c]                ;31 4a
    mulu x                      ;31 88
    divuw c                     ;31 82
    ror4 [hl]                   ;31 90
    rol4 [hl]                   ;31 80
    br ax                       ;31 98

label24:
    bt *0xfffe.0,label24        ;31 06 fe fc    sfr
label25:
    bt *0xfffe.1,label25        ;31 16 fe fc    sfr
label26:
    bt *0xfffe.2,label26        ;31 26 fe fc    sfr
label27:
    bt *0xfffe.3,label27        ;31 36 fe fc    sfr
label28:
    bt *0xfffe.4,label28        ;31 46 fe fc    sfr
label29:
    bt *0xfffe.5,label29        ;31 56 fe fc    sfr
label30:
    bt *0xfffe.6,label30        ;31 66 fe fc    sfr
label31:
    bt *0xfffe.7,label31        ;31 76 fe fc    sfr

label32:
    bt a.0,label32              ;31 0e fd
label33:
    bt a.1,label33              ;31 1e fd
label34:
    bt a.2,label34              ;31 2e fd
label35:
    bt a.3,label35              ;31 3e fd
label36:
    bt a.4,label36              ;31 4e fd
label37:
    bt a.5,label37              ;31 5e fd
label38:
    bt a.6,label38              ;31 6e fd
label39:
    bt a.7,label39              ;31 7e fd

label40:
    bt [hl].0,label40           ;31 86 fd
label41:
    bt [hl].1,label41           ;31 96 fd
label42:
    bt [hl].2,label42           ;31 a6 fd
label43:
    bt [hl].3,label43           ;31 b6 fd
label44:
    bt [hl].4,label44           ;31 c6 fd
label45:
    bt [hl].5,label45           ;31 d6 fd
label46:
    bt [hl].6,label46           ;31 e6 fd
label47:
    bt [hl].7,label47           ;31 f6 fd

label48:
    bf 0xfe20.0,label48         ;31 03 20 fc    saddr
label49:
    bf 0xfe20.1,label49         ;31 13 20 fc    saddr
label50:
    bf 0xfe20.2,label50         ;31 23 20 fc    saddr
label51:
    bf 0xfe20.3,label51         ;31 33 20 fc    saddr
label52:
    bf 0xfe20.4,label52         ;31 43 20 fc    saddr
label53:
    bf 0xfe20.5,label53         ;31 53 20 fc    saddr
label54:
    bf 0xfe20.6,label54         ;31 63 20 fc    saddr
label55:
    bf 0xfe20.7,label55         ;31 73 20 fc    saddr

label56:
    bf *0xfffe.0,label56        ;31 07 fe fc    sfr
label57:
    bf *0xfffe.1,label57        ;31 17 fe fc    sfr
label58:
    bf *0xfffe.2,label58        ;31 27 fe fc    sfr
label59:
    bf *0xfffe.3,label59        ;31 37 fe fc    sfr
label60:
    bf *0xfffe.4,label60        ;31 47 fe fc    sfr
label61:
    bf *0xfffe.5,label61        ;31 57 fe fc    sfr
label62:
    bf *0xfffe.6,label62        ;31 67 fe fc    sfr
label63:
    bf *0xfffe.7,label63        ;31 77 fe fc    sfr

label64:
    bf a.0,label64              ;31 0f fd
label65:
    bf a.1,label65              ;31 1f fd
label66:
    bf a.2,label66              ;31 2f fd
label67:
    bf a.3,label67              ;31 3f fd
label68:
    bf a.4,label68              ;31 4f fd
label69:
    bf a.5,label69              ;31 5f fd
label70:
    bf a.6,label70              ;31 6f fd
label71:
    bf a.7,label71              ;31 7f fd

label72:
    bf psw.0,label72            ;31 03 1e fc
label73:
    bf psw.1,label73            ;31 13 1e fc
label74:
    bf psw.2,label74            ;31 23 1e fc
label75:
    bf psw.3,label75            ;31 33 1e fc
label76:
    bf psw.4,label76            ;31 43 1e fc
label77:
    bf psw.5,label77            ;31 53 1e fc
label78:
    bf psw.6,label78            ;31 63 1e fc
label79:
    bf psw.7,label79            ;31 73 1e fc

label80:
    bf [hl].0,label80           ;31 87 fd
label81:
    bf [hl].1,label81           ;31 97 fd
label82:
    bf [hl].2,label82           ;31 a7 fd
label83:
    bf [hl].3,label83           ;31 b7 fd
label84:
    bf [hl].4,label84           ;31 c7 fd
label85:
    bf [hl].5,label85           ;31 d7 fd
label86:
    bf [hl].6,label86           ;31 e7 fd
label87:
    bf [hl].7,label87           ;31 f7 fd

label88:
    btclr @0xfe20.0,label88     ;31 01 20 fc    saddr
label89:
    btclr @0xfe20.1,label89     ;31 11 20 fc    saddr
label90:
    btclr @0xfe20.2,label90     ;31 21 20 fc    saddr
label91:
    btclr @0xfe20.3,label91     ;31 31 20 fc    saddr
label92:
    btclr @0xfe20.4,label92     ;31 41 20 fc    saddr
label93:
    btclr @0xfe20.5,label93     ;31 51 20 fc    saddr
label94:
    btclr @0xfe20.6,label94     ;31 61 20 fc    saddr
label95:
    btclr @0xfe20.7,label95     ;31 71 20 fc    saddr

label96:
    btclr *0xfffe.0,label96     ;31 05 fe fc    sfr
label97:
    btclr *0xfffe.1,label97     ;31 15 fe fc    sfr
label98:
    btclr *0xfffe.2,label98     ;31 25 fe fc    sfr
label99:
    btclr *0xfffe.3,label99     ;31 35 fe fc    sfr
label100:
    btclr *0xfffe.4,label100    ;31 45 fe fc    sfr
label101:
    btclr *0xfffe.5,label101    ;31 55 fe fc    sfr
label102:
    btclr *0xfffe.6,label102    ;31 65 fe fc    sfr
label103:
    btclr *0xfffe.7,label103    ;31 75 fe fc    sfr

label104:
    btclr a.0,label104          ;31 0d fd
label105:
    btclr a.1,label105          ;31 1d fd
label106:
    btclr a.2,label106          ;31 2d fd
label107:
    btclr a.3,label107          ;31 3d fd
label108:
    btclr a.4,label108          ;31 4d fd
label109:
    btclr a.5,label109          ;31 5d fd
label110:
    btclr a.6,label110          ;31 6d fd
label111:
    btclr a.7,label111          ;31 7d fd

label112:
    btclr psw.0,label112       ;31 01 1e fc
label113:
    btclr psw.1,label113       ;31 11 1e fc
label114:
    btclr psw.2,label114       ;31 21 1e fc
label115:
    btclr psw.3,label115       ;31 31 1e fc
label116:
    btclr psw.4,label116       ;31 41 1e fc
label117:
    btclr psw.5,label117       ;31 51 1e fc
label118:
    btclr psw.6,label118       ;31 61 1e fc
label119:
    btclr psw.7,label119       ;31 71 1e fc

label120:
    btclr [hl].0,label120      ;31 85 fd
label121:
    btclr [hl].1,label121      ;31 95 fd
label122:
    btclr [hl].2,label122      ;31 a5 fd
label123:
    btclr [hl].3,label123      ;31 b5 fd
label124:
    btclr [hl].4,label124      ;31 c5 fd
label125:
    btclr [hl].5,label125      ;31 d5 fd
label126:
    btclr [hl].6,label126      ;31 e5 fd
label127:
    btclr [hl].7,label127      ;31 f5 fd

    xch a,c                     ;32
    xch a,b                     ;33
    xch a,e                     ;34
    xch a,d                     ;35

;XXX
;    xch a,l                     ;36
    .byte 0x36

;XXX
;    xch a,h                     ;37
    .byte 0x37

    subc a,!0xabcd              ;38 cd ab
    subc a,[hl+0xab]            ;39 ab
    set1 @0xfe20.3              ;3a 20          saddr
    set1 psw.3                  ;3a 1e
    clr1 @0xfe20.3              ;3b 20          saddr
    clr1 psw.3                  ;3b 1e
    callf !0x0b00               ;3c 00          3c = callf 0b00h-0bffh
    callf !0x0bff               ;3c ff
    subc a,#0xab                ;3d ab
    subc a,@0xfe20              ;3e 20          saddr
    subc a,[hl]                 ;3f
    inc x                       ;40
    inc a                       ;41
    inc c                       ;42
    inc b                       ;43
    inc e                       ;44
    inc d                       ;45

;XXX
;   inc l                       ;46
    .byte 0x46

;XXX
;   inc h                       ;47
    .byte 0x47

    cmp a,!0xabcd               ;48 cd ab
    cmp a,[hl+0xab]             ;49 ab
    set1 @0xfe20.4               ;4a 20          saddr
    set1 psw.4                  ;4a 1e
    clr1 @0xfe20.4               ;4b 20          saddr
    clr1 psw.4                  ;4b 1e
    callf !0xc00                ;4c 00          4c = callf 0c00h-0cffh
    callf !0xcff                ;4c ff
    cmp a,#0xab                 ;4d ab
    cmp a,0xfe20                ;4e 20          saddr
    cmp a,[hl]                  ;4f
    dec x                       ;50
    dec a                       ;51
    dec c                       ;52
    dec b                       ;53
    dec e                       ;54
    dec d                       ;55

;XXX
;   dec l                       ;56
    .byte 0x56

;XXX
;   dec h                       ;57
    .byte 0x57

    and a,!0xabcd               ;58 cd ab
    and a,[hl+0xab]             ;59 ab
    set1 @0xfe20.5              ;5a 20          saddr
    set1 psw.5                  ;5a 1e
    clr1 @0xfe20.5              ;5b 20          saddr
    clr1 psw.5                  ;5b 1e
    callf !0xd00                ;5c 00          5c = callf 0d00h-0dffh
    callf !0xdff                ;5c ff
    and a,#0xab                 ;5d ab
    and a,0xfe20                ;5e 20          saddr
    and a,[hl]                  ;5f
    mov a,x                     ;60

    adjba                       ;61 80
    adjbs                       ;61 90

    sel rb0                     ;61 d0
    sel rb1                     ;61 d8
    sel rb2                     ;61 f0
    sel rb3                     ;61 f8

    mov1 cy,a.0                 ;61 8c
    mov1 cy,a.1                 ;61 9c
    mov1 cy,a.2                 ;61 ac
    mov1 cy,a.3                 ;61 bc
    mov1 cy,a.4                 ;61 cc
    mov1 cy,a.5                 ;61 dc
    mov1 cy,a.6                 ;61 ec
    mov1 cy,a.7                 ;61 fc

    mov1 a.0,cy                 ;61 89
    mov1 a.1,cy                 ;61 99
    mov1 a.2,cy                 ;61 a9
    mov1 a.3,cy                 ;61 b9
    mov1 a.4,cy                 ;61 c9
    mov1 a.5,cy                 ;61 d9
    mov1 a.6,cy                 ;61 e9
    mov1 a.7,cy                 ;61 f9

    and1 cy,a.0                 ;61 8d
    and1 cy,a.1                 ;61 9d
    and1 cy,a.2                 ;61 ad
    and1 cy,a.3                 ;61 bd
    and1 cy,a.4                 ;61 cd
    and1 cy,a.5                 ;61 dd
    and1 cy,a.6                 ;61 ed
    and1 cy,a.7                 ;61 fd

    or1 cy,a.0                  ;61 8e
    or1 cy,a.1                  ;61 9e
    or1 cy,a.2                  ;61 ae
    or1 cy,a.3                  ;61 be
    or1 cy,a.4                  ;61 ce
    or1 cy,a.5                  ;61 de
    or1 cy,a.6                  ;61 ee
    or1 cy,a.7                  ;61 fe

    xor1 cy,a.0                 ;61 8f
    xor1 cy,a.1                 ;61 9f
    xor1 cy,a.2                 ;61 af
    xor1 cy,a.3                 ;61 bf
    xor1 cy,a.4                 ;61 cf
    xor1 cy,a.5                 ;61 df
    xor1 cy,a.6                 ;61 ef
    xor1 cy,a.7                 ;61 ff

    set1 a.0                    ;61 8a
    set1 a.1                    ;61 9a
    set1 a.2                    ;61 aa
    set1 a.3                    ;61 ba
    set1 a.4                    ;61 ca
    set1 a.5                    ;61 da
    set1 a.6                    ;61 ea
    set1 a.7                    ;61 fa

    clr1 a.0                    ;61 8b
    clr1 a.1                    ;61 9b
    clr1 a.2                    ;61 ab
    clr1 a.3                    ;61 bb
    clr1 a.4                    ;61 cb
    clr1 a.5                    ;61 db
    clr1 a.6                    ;61 eb
    clr1 a.7                    ;61 fb

    add a,x                     ;61 08
    add a,a                     ;61 01
    add a,c                     ;61 0a
    add a,b                     ;61 0b
    add a,e                     ;61 0c
    add a,d                     ;61 0d

;XXX
;   add a,l                     ;61 0e
    .byte 0x61, 0x0e

;XXX
;   add a,h                     ;61 0f
    .byte 0x61, 0x0f

    add x,a                     ;61 00
    add a,a                     ;61 01
    add c,a                     ;61 02
    add b,a                     ;61 03
    add e,a                     ;61 04
    add d,a                     ;61 05

;XXX
;    add l,a                     ;61 06
    .byte 0x61, 0x06

;XXX
;    add h,a                     ;61 07
    .byte 0x61, 0x07

    addc a,x                    ;61 28
    addc a,a                    ;61 21
    addc a,c                    ;61 2a
    addc a,b                    ;61 2b
    addc a,e                    ;61 2c
    addc a,d                    ;61 2d

;XXX
;   addc a,l                    ;61 2e
    .byte 0x61, 0x2e

;XXX
;   addc a,h                    ;61 2f
    .byte 0x61, 0x2f

    addc x,a                    ;61 20
    addc a,a                    ;61 21
    addc c,a                    ;61 22
    addc b,a                    ;61 23
    addc e,a                    ;61 24
    addc d,a                    ;61 25

;XXX
;   addc l,a                    ;61 26
    .byte 0x61, 0x26

;XXX
;   addc h,a                    ;61 27
    .byte 0x61, 0x27

    sub a,x                     ;61 18
    sub a,a                     ;61 11
    sub a,c                     ;61 1a
    sub a,b                     ;61 1b
    sub a,e                     ;61 1c
    sub a,d                     ;61 1d

;XXX
;   sub a,l                     ;61 1e
    .byte 0x61, 0x1e

;XXX
;   sub a,h                     ;61 1f
    .byte 0x61, 0x1f

    sub x,a                     ;61 10
    sub a,a                     ;61 11
    sub c,a                     ;61 12
    sub b,a                     ;61 13
    sub e,a                     ;61 14
    sub d,a                     ;61 15

;XXX
;    sub l,a                     ;61 16
    .byte 0x61, 0x16

;XXX
;    sub h,a                     ;61 17
    .byte 0x61, 0x17

    subc a,x                    ;61 38
    subc a,a                    ;61 31
    subc a,c                    ;61 3a
    subc a,b                    ;61 3b
    subc a,e                    ;61 3c
    subc a,d                    ;61 3d

;XXX
;    subc a,l                    ;61 3e
    .byte 0x61, 0x3e

;XXX
;    subc a,h                    ;61 3f
    .byte 0x61, 0x3f

    subc x,a                    ;61 30
    subc a,a                    ;61 31
    subc c,a                    ;61 32
    subc b,a                    ;61 33
    subc e,a                    ;61 34
    subc d,a                    ;61 35

;XXX
;   subc l,a                    ;61 36
    .byte 0x61, 0x36

;XXX
;   subc h,a                    ;61 37
    .byte 0x61, 0x37

    and x,a                     ;61 50
    and a,a                     ;61 51
    and c,a                     ;61 52
    and b,a                     ;61 53
    and e,a                     ;61 54
    and d,a                     ;61 55

;XXX
;    and l,a                     ;61 56
    .byte 0x61, 0x56

;XXX
;   and h,a                     ;61 57
    .byte 0x61, 0x57

    and a,x                     ;61 58
    and a,a                     ;61 51
    and a,c                     ;61 5a
    and a,b                     ;61 5b
    and a,e                     ;61 5c
    and a,d                     ;61 5d

;XXX
;    and a,l                     ;61 5e
    .byte 0x61, 0x5e

;XXX
;    and a,h                     ;61 5f
    .byte 0x61, 0x5f

    or a,x                      ;61 68
    or a,a                      ;61 61
    or a,c                      ;61 6a
    or a,b                      ;61 6b
    or a,e                      ;61 6c
    or a,d                      ;61 6d

;XXX
;    or a,l                      ;61 6e
    .byte 0x61, 0x6e

;XXX
;   or a,h                      ;61 6f
    .byte 0x61, 0x6f

    or x,a                      ;61 60
    or a,a                      ;61 61
    or c,a                      ;61 62
    or b,a                      ;61 63
    or e,a                      ;61 64
    or d,a                      ;61 65

;XXX
;    or l,a                      ;61 66
    .byte 0x61, 0x66

;XXX
;    or h,a                      ;61 67
    .byte 0x61, 0x67

    xor a,x                     ;61 78
    xor a,a                     ;61 71
    xor a,c                     ;61 7a
    xor a,b                     ;61 7b
    xor a,e                     ;61 7c
    xor a,d                     ;61 7d

;XXX
;   xor a,l                     ;61 7e
    .byte 0x61, 0x7e

;XXX
;   xor a,h                     ;61 7f
    .byte 0x61, 0x7f

    xor x,a                     ;61 70
    xor a,a                     ;61 71
    xor c,a                     ;61 72
    xor b,a                     ;61 73
    xor e,a                     ;61 74
    xor d,a                     ;61 75

;XXX
;    xor l,a                     ;61 76
    .byte 0x61, 0x76

;XXX
;    xor h,a                     ;61 77
    .byte 0x61, 0x77

    cmp a,x                     ;61 48
    cmp a,a                     ;61 41
    cmp a,c                     ;61 4a
    cmp a,b                     ;61 4b
    cmp a,e                     ;61 4c
    cmp a,d                     ;61 4d

;XXX
;    cmp a,l                     ;61 4e
    .byte 0x61, 0x4e

;XXX
;    cmp a,h                     ;61 4f
    .byte 0x61, 0x4f

    cmp x,a                     ;61 40
    cmp a,a                     ;61 41
    cmp c,a                     ;61 42
    cmp b,a                     ;61 43
    cmp e,a                     ;61 44
    cmp d,a                     ;61 45

;XXX
;    cmp l,a                     ;61 46
    .byte 0x61, 0x46

;XXX
;    cmp h,a                     ;61 47
    .byte 0x61, 0x47

    mov a,c                     ;62
    mov a,b                     ;63
    mov a,e                     ;64
    mov a,d                     ;65

;XXX
;   mov a,l                     ;66
    .byte 0x66

;XXX
;   mov a,h                     ;67
    .byte 0x67

    or a,!0xabcd                ;68 cd ab
    or a,[hl+0xab]              ;69 ab
    set1 @0xfe20.6              ;6a 20          saddr
    set1 psw.6                  ;6a 1e
    clr1 @0xfe20.6              ;6b 20          saddr
    clr1 psw.6                  ;6b 1e
    callf !0xe00                ;6c 00          6c = callf 0e00h-0effh
    callf !0xeff                ;6c ff
    or a,#0xab                  ;6d ab
    or a,@0xfe20                ;6e 20          saddr
    or a,[hl]                   ;6f
    mov x,a                     ;70

    mov1 cy,@0xfe20.0            ;71 04 20       saddr
    mov1 cy,@0xfe20.1            ;71 14 20       saddr
    mov1 cy,@0xfe20.2            ;71 24 20       saddr
    mov1 cy,@0xfe20.3            ;71 34 20       saddr
    mov1 cy,@0xfe20.4            ;71 44 20       saddr
    mov1 cy,@0xfe20.5            ;71 54 20       saddr
    mov1 cy,@0xfe20.6            ;71 64 20       saddr
    mov1 cy,@0xfe20.7            ;71 74 20       saddr

    mov1 cy,*0xfffe.0            ;71 0c fe       sfr
    mov1 cy,*0xfffe.1            ;71 1c fe       sfr
    mov1 cy,*0xfffe.2            ;71 2c fe       sfr
    mov1 cy,*0xfffe.3            ;71 3c fe       sfr
    mov1 cy,*0xfffe.4            ;71 4c fe       sfr
    mov1 cy,*0xfffe.5            ;71 5c fe       sfr
    mov1 cy,*0xfffe.6            ;71 6c fe       sfr
    mov1 cy,*0xfffe.7            ;71 7c fe       sfr

    mov1 cy,psw.0               ;71 04 1e
    mov1 cy,psw.1               ;71 14 1e
    mov1 cy,psw.2               ;71 24 1e
    mov1 cy,psw.3               ;71 34 1e
    mov1 cy,psw.4               ;71 44 1e
    mov1 cy,psw.5               ;71 54 1e
    mov1 cy,psw.6               ;71 64 1e
    mov1 cy,psw.7               ;71 74 1e

    mov1 cy,[hl].0              ;71 84
    mov1 cy,[hl].1              ;71 94
    mov1 cy,[hl].2              ;71 a4
    mov1 cy,[hl].3              ;71 b4
    mov1 cy,[hl].4              ;71 c4
    mov1 cy,[hl].5              ;71 d4
    mov1 cy,[hl].6              ;71 e4
    mov1 cy,[hl].7              ;71 f4

    mov1 @0xfe20.0,cy            ;71 01 20       saddr
    mov1 @0xfe20.1,cy            ;71 11 20       saddr
    mov1 @0xfe20.2,cy            ;71 21 20       saddr
    mov1 @0xfe20.3,cy            ;71 31 20       saddr
    mov1 @0xfe20.4,cy            ;71 41 20       saddr
    mov1 @0xfe20.5,cy            ;71 51 20       saddr
    mov1 @0xfe20.6,cy            ;71 61 20       saddr
    mov1 @0xfe20.7,cy            ;71 71 20       saddr

    mov1 *0xfffe.0,cy            ;71 09 fe       sfr
    mov1 *0xfffe.1,cy            ;71 19 fe       sfr
    mov1 *0xfffe.2,cy            ;71 29 fe       sfr
    mov1 *0xfffe.3,cy            ;71 39 fe       sfr
    mov1 *0xfffe.4,cy            ;71 49 fe       sfr
    mov1 *0xfffe.5,cy            ;71 59 fe       sfr
    mov1 *0xfffe.6,cy            ;71 69 fe       sfr
    mov1 *0xfffe.7,cy            ;71 79 fe       sfr

    mov1 psw.0,cy               ;71 01 1e
    mov1 psw.1,cy               ;71 11 1e
    mov1 psw.2,cy               ;71 21 1e
    mov1 psw.3,cy               ;71 31 1e
    mov1 psw.4,cy               ;71 41 1e
    mov1 psw.5,cy               ;71 51 1e
    mov1 psw.6,cy               ;71 61 1e
    mov1 psw.7,cy               ;71 71 1e

    mov1 [hl].0,cy              ;71 81
    mov1 [hl].1,cy              ;71 91
    mov1 [hl].2,cy              ;71 a1
    mov1 [hl].3,cy              ;71 b1
    mov1 [hl].4,cy              ;71 c1
    mov1 [hl].5,cy              ;71 d1
    mov1 [hl].6,cy              ;71 e1
    mov1 [hl].7,cy              ;71 f1

    and1 cy,@0xfe20.0           ;71 05 20       saddr
    and1 cy,@0xfe20.1           ;71 15 20       saddr
    and1 cy,@0xfe20.2           ;71 25 20       saddr
    and1 cy,@0xfe20.3           ;71 35 20       saddr
    and1 cy,@0xfe20.4           ;71 45 20       saddr
    and1 cy,@0xfe20.5           ;71 55 20       saddr
    and1 cy,@0xfe20.6           ;71 65 20       saddr
    and1 cy,@0xfe20.7           ;71 75 20       saddr

    and1 cy,*0xfffe.0           ;71 0d fe       sfr
    and1 cy,*0xfffe.1           ;71 1d fe       sfr
    and1 cy,*0xfffe.2           ;71 2d fe       sfr
    and1 cy,*0xfffe.3           ;71 3d fe       sfr
    and1 cy,*0xfffe.4           ;71 4d fe       sfr
    and1 cy,*0xfffe.5           ;71 5d fe       sfr
    and1 cy,*0xfffe.6           ;71 6d fe       sfr
    and1 cy,*0xfffe.7           ;71 7d fe       sfr

    and1 cy,psw.0               ;71 05 1e
    and1 cy,psw.1               ;71 15 1e
    and1 cy,psw.2               ;71 25 1e
    and1 cy,psw.3               ;71 35 1e
    and1 cy,psw.4               ;71 45 1e
    and1 cy,psw.5               ;71 55 1e
    and1 cy,psw.6               ;71 65 1e
    and1 cy,psw.7               ;71 75 1e

    and1 cy,[hl].0              ;71 85
    and1 cy,[hl].1              ;71 95
    and1 cy,[hl].2              ;71 a5
    and1 cy,[hl].3              ;71 b5
    and1 cy,[hl].4              ;71 c5
    and1 cy,[hl].5              ;71 d5
    and1 cy,[hl].6              ;71 e5
    and1 cy,[hl].7              ;71 f5

    or1 cy,@0xfe20.0            ;71 06 20       saddr
    or1 cy,@0xfe20.1            ;71 16 20       saddr
    or1 cy,@0xfe20.2            ;71 26 20       saddr
    or1 cy,@0xfe20.3            ;71 36 20       saddr
    or1 cy,@0xfe20.4            ;71 46 20       saddr
    or1 cy,@0xfe20.5            ;71 56 20       saddr
    or1 cy,@0xfe20.6            ;71 66 20       saddr
    or1 cy,@0xfe20.7            ;71 76 20       saddr

    or1 cy,*0xfffe.0             ;71 0e fe       sfr
    or1 cy,*0xfffe.1             ;71 1e fe       sfr
    or1 cy,*0xfffe.2             ;71 2e fe       sfr
    or1 cy,*0xfffe.3             ;71 3e fe       sfr
    or1 cy,*0xfffe.4             ;71 4e fe       sfr
    or1 cy,*0xfffe.5             ;71 5e fe       sfr
    or1 cy,*0xfffe.6             ;71 6e fe       sfr
    or1 cy,*0xfffe.7             ;71 7e fe       sfr

    or1 cy,psw.0                ;71 06 1e
    or1 cy,psw.1                ;71 16 1e
    or1 cy,psw.2                ;71 26 1e
    or1 cy,psw.3                ;71 36 1e
    or1 cy,psw.4                ;71 46 1e
    or1 cy,psw.5                ;71 56 1e
    or1 cy,psw.6                ;71 66 1e
    or1 cy,psw.7                ;71 76 1e

    or1 cy,[hl].0               ;71 86
    or1 cy,[hl].1               ;71 96
    or1 cy,[hl].2               ;71 a6
    or1 cy,[hl].3               ;71 b6
    or1 cy,[hl].4               ;71 c6
    or1 cy,[hl].5               ;71 d6
    or1 cy,[hl].6               ;71 e6
    or1 cy,[hl].7               ;71 f6

    xor1 cy,@0xfe20.0           ;71 07 20       saddr
    xor1 cy,@0xfe20.1           ;71 17 20       saddr
    xor1 cy,@0xfe20.2           ;71 27 20       saddr
    xor1 cy,@0xfe20.3           ;71 37 20       saddr
    xor1 cy,@0xfe20.4           ;71 47 20       saddr
    xor1 cy,@0xfe20.5           ;71 57 20       saddr
    xor1 cy,@0xfe20.6           ;71 67 20       saddr
    xor1 cy,@0xfe20.7           ;71 77 20       saddr

    xor1 cy,*0xfffe.0           ;71 0f fe       sfr
    xor1 cy,*0xfffe.1           ;71 1f fe       sfr
    xor1 cy,*0xfffe.2           ;71 2f fe       sfr
    xor1 cy,*0xfffe.3           ;71 3f fe       sfr
    xor1 cy,*0xfffe.4           ;71 4f fe       sfr
    xor1 cy,*0xfffe.5           ;71 5f fe       sfr
    xor1 cy,*0xfffe.6           ;71 6f fe       sfr
    xor1 cy,*0xfffe.7           ;71 7f fe       sfr

    xor1 cy,psw.0               ;71 07 1e
    xor1 cy,psw.1               ;71 17 1e
    xor1 cy,psw.2               ;71 27 1e
    xor1 cy,psw.3               ;71 37 1e
    xor1 cy,psw.4               ;71 47 1e
    xor1 cy,psw.5               ;71 57 1e
    xor1 cy,psw.6               ;71 67 1e
    xor1 cy,psw.7               ;71 77 1e

    xor1 cy,[hl].0              ;71 87
    xor1 cy,[hl].1              ;71 97
    xor1 cy,[hl].2              ;71 a7
    xor1 cy,[hl].3              ;71 b7
    xor1 cy,[hl].4              ;71 c7
    xor1 cy,[hl].5              ;71 d7
    xor1 cy,[hl].6              ;71 e7
    xor1 cy,[hl].7              ;71 f7

    set1 *0xfffe.0              ;71 0a fe       sfr
    set1 *0xfffe.1              ;71 1a fe       sfr
    set1 *0xfffe.2              ;71 2a fe       sfr
    set1 *0xfffe.3              ;71 3a fe       sfr
    set1 *0xfffe.4              ;71 4a fe       sfr
    set1 *0xfffe.5              ;71 5a fe       sfr
    set1 *0xfffe.6              ;71 6a fe       sfr
    set1 *0xfffe.7              ;71 7a fe       sfr

    set1 [hl].0                 ;71 82
    set1 [hl].1                 ;71 92
    set1 [hl].2                 ;71 a2
    set1 [hl].3                 ;71 b2
    set1 [hl].4                 ;71 c2
    set1 [hl].5                 ;71 d2
    set1 [hl].6                 ;71 e2
    set1 [hl].7                 ;71 f2

    clr1 *0xfffe.0              ;71 0b fe       sfr
    clr1 *0xfffe.1              ;71 1b fe       sfr
    clr1 *0xfffe.2              ;71 2b fe       sfr
    clr1 *0xfffe.3              ;71 3b fe       sfr
    clr1 *0xfffe.4              ;71 4b fe       sfr
    clr1 *0xfffe.5              ;71 5b fe       sfr
    clr1 *0xfffe.6              ;71 6b fe       sfr
    clr1 *0xfffe.7              ;71 7b fe       sfr

    clr1 [hl].0                 ;71 83
    clr1 [hl].1                 ;71 93
    clr1 [hl].2                 ;71 a3
    clr1 [hl].3                 ;71 b3
    clr1 [hl].4                 ;71 c3
    clr1 [hl].5                 ;71 d3
    clr1 [hl].6                 ;71 e3
    clr1 [hl].7                 ;71 f3

    halt                        ;71 10
    stop                        ;71 00

    mov c,a                     ;72
    mov b,a                     ;73
    mov e,a                     ;74
    mov d,a                     ;75

;XXX
;   mov l,a                     ;76
    .byte 0x76

;XXX
;   mov h,a                     ;77
    .byte 0x77

    xor a,!0xabcd               ;78 cd ab
    xor a,[hl+0xab]             ;79 ab
    set1 @0xfe20.7               ;7a 20          saddr
    set1 psw.7                  ;7a 1e
    ei                          ;7a 1e          alias for set1 psw.7
    clr1 @0xfe20.7               ;7b 20          saddr
    clr1 psw.7                  ;7b 1e
    di                          ;7b 1e          alias for clr1 psw.7
    callf !0x0f00                ;7c 00          7c = callf 0f00h-0fffh
    callf !0x0fff                ;7c ff
    xor a,#0xab                 ;7d ab
    xor a,0xfe20                ;7e 20          saddr
    xor a,[hl]                  ;7f
    incw ax                     ;80
    inc @0xfe20                  ;81 20          saddr
    incw bc                     ;82
    xch a,@0xfe20                ;83 20          saddr
    incw de                     ;84
    mov a,[de]                  ;85
    incw hl                     ;86
    mov a,[hl]                  ;87
    add @0xfe20,#0xab           ;88 20 ab       saddr
    movw ax,@0xfe20              ;89 20          saddrp

;XXX
;     movw ax,sp                  ;89 1c
    .byte 0x89, 0x1c

label1:
    dbnz c,label1              ;8a fe
label2:
    dbnz b,label2              ;8b fe
label8:
    bt @0xfe20.0,label8         ;8c 20 fd       saddr
label9:
    bt psw.0,label9            ;8c 1e fd
label3:
    bc label3                  ;8d fe
    mov a,!0xabcd               ;8e cd ab
    reti                        ;8f
    decw ax                     ;90
    dec 0xfe20                  ;91 20          saddr
    decw bc                     ;92
    xch a,*0xfffe               ;93 fe          sfr
    decw de                     ;94
    mov [de],a                  ;95
    decw hl                     ;96
    mov [hl],a                  ;97
    sub 0xfe20,#0xab            ;98 20 ab       saddr
    movw @0xfe20,ax             ;99 20          saddrp

;XXX
;     movw sp,ax                  ;99 1c
    .byte 0x99, 0x1c

    call !0xabcd                ;9a cd ab
    br !0xabcd                  ;9b cd ab
label10:
    bt @0xfe20.1,label10        ;9c 20 fd       saddr
label11:
    bt psw.1,label11           ;9c 1e fd
label4:
    bnc label4                  ;9d fe
    mov !0xabcd,a               ;9e cd ab
    retb                        ;9f
    mov x,#0xab                 ;a0 ab
    mov a,#0xab                 ;a1 ab
    mov c,#0xab                 ;a2 ab
    mov b,#0xab                 ;a3 ab
    mov e,#0xab                 ;a4 ab
    mov d,#0xab                 ;a5 ab

;XXX
;   mov l,#0xab                 ;a6 ab
    .byte 0xa6, 0xab

;XXX
;   mov h,#0xab                 ;a7 ab
    .byte 0xa7, 0xab

    addc @0xfe20,#0xab           ;a8 20 ab       saddr
    movw ax,*0xfffe              ;a9 fe          sfrp
    mov a,[hl+c]                ;aa
    mov a,[hl+b]                ;ab
label12:
    bt @0xfe20.2,label12        ;ac 20 fd       saddr
label13:
    bt psw.2,label13           ;ac 1e fd
label5:
    bz label5                   ;ad fe
    mov a,[hl+0xab]             ;ae ab
    ret                         ;af
    pop ax                      ;b0
    push ax                     ;b1
    pop bc                      ;b2
    push bc                     ;b3
    pop de                      ;b4
    push de                     ;b5
    pop hl                      ;b6
    push hl                     ;b7
    subc @0xfe20,#0xab          ;b8 20 ab       saddr
    movw *0xfffe,ax              ;b9 fe          sfrp
    mov [hl+c],a                ;ba
    mov [hl+b],a                ;bb
label14:
    bt @0xfe20.3,label14        ;bc 20 fd       saddr
label15:
    bt psw.3,label15           ;bc 1e fd
label6:
    bnz label6                 ;bd fe
    mov [hl+0xab],a             ;be ab
    brk                         ;bf
    callt [0x0040]               ;c1
    movw ax,bc                  ;c2
    callt [0x0042]               ;c3
    movw ax,de                  ;c4
    callt [0x0044]               ;c5
    movw ax,hl                  ;c6
    callt [0x0046]               ;c7
    cmp 0xfe20,#0xab            ;c8 20 ab       saddr
    callt [0x0048]               ;c9
    addw ax,#0xabcd             ;ca cd ab
    callt [0x004a]               ;cb
label16:
    bt 0xfe20.4,label16        ;cc 20 fd       saddr
label17:
    bt psw.4,label17           ;cc 1e fd
    callt [0x004c]               ;cd
    xch a,!0xabcd               ;ce cd ab
    callt [0x004e]               ;cf
    callt [0x0050]               ;d1
    movw bc,ax                  ;d2
    callt [0x0052]               ;d3
    movw de,ax                  ;d4
    callt [0x0054]               ;d5
    movw hl,ax                  ;d6
    callt [0x0056]               ;d7
    and @0xfe20,#0xab            ;d8 20 ab       saddr
    callt [0x0058]               ;d9
    subw ax,#0xabcd             ;da cd ab
    callt [0x005a]               ;db
label20:
    bt @0xfe20.5,label20        ;dc 20 fd       saddr
label21:
    bt psw.5,label21            ;dc 1e fd
    callt [0x005c]              ;dd
    xch a,[hl+0xab]             ;de ab
    callt [0x005e]              ;df
    callt [0x0060]              ;e1
    xchw ax,bc                  ;e2
    callt [0x0062]              ;e3
    xchw ax,de                  ;e4
    callt [0x0064]              ;e5
    xchw ax,hl                  ;e6
    callt [0x0066]              ;e7
    or 0xfe20,#0xab             ;e8 20 ab
    callt [0x068]               ;e9
    cmpw ax,#0xabcd             ;ea cd ab
    callt [0x06a]               ;eb
label22:
    bt @0xfe20h.6,label22       ;ec 20 fd       saddr
label23:
    bt psw.6,label23            ;ec 1e fd
    callt [0x06c]               ;ed
    movw @0xfe20,#0xabcd        ;ee 20 cd ab    saddrp

;XXX
;    movw sp,#0xabcd            ;ee 1c cd ab
    .byte 0xee, 0x1c, 0xcd, 0xab

    callt [0x006e]              ;ef
    mov a,@0xfe20               ;f0 20          saddr

;XXX
;    mov a,psw                   ;f0 1e
    .byte 0xf0, 0x1e

    callt [0x0070]              ;f1
    mov 0xfe20,a                ;f2 20          saddr

;XXX
;    mov psw,a                   ;f2 1e
    .byte 0xf2, 0x1e

    callt [0x0072]              ;f3
    mov a,*0x0fffe              ;f4 ff          sfr
    callt [0x0074]              ;f5
    mov *0xfffe,a               ;f6 fe          sfr
    callt [0x0076]              ;f7
    xor @0xfe20,#0xab           ;f8 20 ab       saddr
    callt [0x0078]              ;f9
label7:
   br label7                    ;fa fe
   callt [0x007a]               ;fb
label18:
   bt @0xfe20.7,label18         ;fc 20 fd       saddr
label19:
   bt psw.7,label19             ;fc 1e fd
   callt [0x007c]               ;fd
   movw *0xfffe,#0xabcd         ;fe fe cd ab    sfrp
   callt [0x007e]               ;ff
