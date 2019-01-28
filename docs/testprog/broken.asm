;Instructions broken on as78k0 v5.30

    mov psw,#0xab               ;11 1e ab
    push psw                    ;22
    pop psw                     ;23
    xch a,l                     ;36
    xch a,h                     ;37
    inc l                       ;46
    inc h                       ;47
    dec l                       ;56
    dec h                       ;57
    add a,l                     ;61 0e
    add a,h                     ;61 0f
    add l,a                     ;61 06
    add h,a                     ;61 07
    addc a,l                    ;61 2e
    addc a,h                    ;61 2f
    addc l,a                    ;61 26
    addc h,a                    ;61 27
    sub a,l                     ;61 1e
    sub a,h                     ;61 1f
    sub l,a                     ;61 16
    sub h,a                     ;61 17
    subc a,l                    ;61 3e
    subc a,h                    ;61 3f
    subc l,a                    ;61 36
    subc h,a                    ;61 37
    and l,a                     ;61 56
    and h,a                     ;61 57
    and a,l                     ;61 5e
    and a,h                     ;61 5f
    or a,l                      ;61 6e
    or a,h                      ;61 6f
    or l,a                      ;61 66
    or h,a                      ;61 67
    xor a,l                     ;61 7e
    xor a,h                     ;61 7f
    xor l,a                     ;61 76
    xor h,a                     ;61 77
    cmp a,l                     ;61 4e
    cmp a,h                     ;61 4f
    cmp l,a                     ;61 46
    cmp h,a                     ;61 47
    mov a,l                     ;66
    mov a,h                     ;67
    mov l,a                     ;76
    mov h,a                     ;77
    movw ax,sp                  ;89 1c
    movw sp,ax                  ;99 1c
    mov l,#0xab                 ;a6 ab
    mov h,#0xab                 ;a7 ab
    movw sp,#0xabcd             ;ee 1c cd ab
    mov a,psw                   ;f0 1e
    mov psw,a                   ;f2 1e
