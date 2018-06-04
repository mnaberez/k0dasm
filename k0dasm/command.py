import sys

from k0dasm.disassemble import disassemble
from k0dasm.memory import Memory
from k0dasm.trace import Tracer
from k0dasm.listing import Printer
from k0dasm.symbols import SymbolTable, D78F0831Y_SYMBOLS

def main():
    with open(sys.argv[1], 'rb') as f:
        rom = bytearray(f.read())
    memory = Memory(rom)

    start_address = 0
    entry_points = [0x09e6,
                    0x12e3,
                    0x26c9, 0x26d6, 0x26e4, 0x26f9, 0x48f1, 0x4914, 0x4960, 0x68b0,
                    0x26b6,
                    0x275c, 0x274e, 0x2706,
                    0x2784, 0x278c, 0x2790, 0x27b0, 0x27cf, 0x27e6, 0x2821, 0x281c,
                    0x6934, 0x695e, 0x69f8, 0x6a0a, 0x6a10, 0x6a2f, 0x6a5c, 0x6a64,
                    0x71c6, 0x71cf, 0x7176, 0x717f, 0x7188, 0x7191, 0x719a, 0x719c,
                    0x719e, 0x71a7, 0x71b0, 0x7142, 0x710b,
                    0x6b66, 0x67b9, 0x6b73, 0x8085, 0x8090,
                    0x6af5, 0x6b00, 0x6b0f, 0x6b18, 0x6b21, 0x6a5c, 0x6a8d, 0x6a9b,
                    0x6a9c, 0x6ab7, 0x6aca, 0x6b48, 0x6b5c, 0x6b3e, 0x6b21, 0x6b2a, 0x6b33,
                    0x6bb4,
                    0x6b9d, 0x6bb4, 0x6bc2, 0x6bcb,
                    0x7142, 0x7151, 0x716b,
                    0x6bf0, 0x6bf9, 0x6c10, 0x6c29, 0x6c3f, 0x6c58, 0x6c6a, 0x6c76,
                    0x6c82, 0x6c8e, 0x6c9a, 0x6ca2, 0x6cac,
                    0x6a7a, 0x71da, 0x71e3, 0x71f2, 0x7224, 0x7249, 0x7294, 0x72de,
                    0x72e9, 0x7303, 0x733e, 0x7351, 0x7387, 0x73a3, 0x73bf, 0x73cd,
                    0x7405, 0x744c, 0x749d, 0x74d5, 0x74e3, 0x7529, 0x752f, 0x7575,
                    0x7579, 0x75bf, 0x75c5, 0x760c, 0x7612, 0x7659, 0x765f, 0x766a,
                    0x7675,
                    ]

#sub_0c48 is some kind of indirect call thing

    hardware_vectors = [
        0x0000, # RST
        0x0002, # (unused)
        0x0004, # INTWDT
        0x0004, # INTWDT
        0x0006, # INTP0
        0x0008, # INTP1
        0x000a, # INTP2
        0x000c, # INTP3
        0x000e, # INTP4
        0x0010, # INTP5
        0x0012, # INTP6
        0x0014, # INTP7
        0x0016, # INTSER0
        0x0018, # INTSR0
        0x001a, # INTST0
        0x001c, # INTCSI30
        0x001e, # INTCSI31
        0x0020, # INTIIC0
        0x0022, # INTC2
        0x0024, # INTWTNI0
        0x0026, # INTTM000
        0x0028, # INTTM010
        0x002a, # INTTM001
        0x002c, # INTTM011
        0x002e, # INTAD00
        0x0030, # INTAD01
        0x0032, # (unused)
        0x0034, # INTWTN0
        0x0036, # INTKR
        0x0038, # (unused)
        0x003a, # (unused)
        0x003c, # (unused)
        0x003e,  # BRK_I
    ]
    callt_vectors = list(range(0x40, 0x7f, 2))
    all_vectors = hardware_vectors + callt_vectors

    traceable_range = range(start_address, start_address + len(rom) + 1)
    tracer = Tracer(memory, entry_points, all_vectors, traceable_range)
    tracer.trace(disassemble)

    symbol_table = SymbolTable(D78F0831Y_SYMBOLS)
    symbol_table.generate(memory, start_address) # xxx should pass traceable_range

    symbol_table.symbols.update({

        0x2655: ('kwp_1j003b180b', ''),
        0x2662: ('kwp_1c0035180a', ''),
        0x266f: ('kwp_radio_de2', ''),
        0x267c: ('kwp_radio_delco', ''),
        0x2689: ('kwp_0001', ''),

        0x2696: ('display_test', ''),
        0x26a6: ('display_test_end', ''),

        0x4921: ('charset_fm1', ''),
        0x4928: ('charset_fm2', ''),
        0x492f: ('charset_preset_1', ''),
        0x4936: ('charset_preset_2', ''),
        0x493d: ('charset_preset_3', ''),
        0x4944: ('charset_preset_4', ''),
        0x494b: ('charset_preset_5', ''),
        0x4952: ('charset_preset_6', ''),
        0x4959: ('charset_solid_block', ''),

        0x63ac: ('m', ''),
        0x63ae: ('u1', ''),
        0x63b1: ('u2', ''),
        0x63b4: ('on', ''),
        0x63b7: ('off', ''),
        0x63bb: ('no', ''),
        0x63be: ('e__', ''),
        0x63cb: ('psc', ''),
        0x63cf: ('pscan', ''),
        0x63d5: ('preset_scan', ''),
        0x63e1: ('pset', ''),
        0x63e6: ('scan', ''),
        0x63eb: ('seek_plus', ''),
        0x63f2: ('seek_minus', ''),
        0x63f9: ('vol', ''),
        0x6407: ('fade', ''),
        0x640c: ('fadefront', ''),
        0x6418: ('fadecenter', ''),
        0x6424: ('faderear', ''),
        0x6430: ('bal', ''),
        0x6435: ('bal_left', ''),
        0x6441: ('bal_center', ''),
        0x644d: ('bal_right', ''),
        0x6459: ('bass', ''),
        0x6465: ('mid', ''),
        0x6471: ('treb', ''),
        0x647d: ('treb_out16', ''),
        0x6489: ('max', ''),
        0x6491: ('min', ''),
        0x6499: ('set_onvol', ''),
        0x64a5: ('set_cd_mix', ''),
        0x64b1: ('tape_skip', ''),
        0x64bd: ('rad_de2', ''),
        0x64c9: ('monsoon', ''),
        0x64d5: ('vers_a99cznn', ''),
        0x64e1: ('fern_on', ''),
        0x64ed: ('fern_off', ''),
        0x64f9: ('safe', ''),
        0x6505: ('onethousand', ''),
        0x6511: ('blank', ''),
        0x651d: ('flat', ''),
        0x6527: ('select_eq', ''),
        0x6587: ('normal', ''),
        0x658e: ('loud', ''),
        0x6593: ('diag', ''),
        0x659b: ('none_found', ''),
        0x65a6: ('tape', ''),
        0x65ab: ('tape_play', ''),
        0x65b7: ('tape_ff', ''),
        0x65c3: ('tape_rew', ''),
        0x65cf: ('tapemss_ff', ''),
        0x65db: ('tapemss_rew', ''),
        0x65e7: ('skip_blank', ''),
        0x65f3: ('tape_scan', ''),
        0x65ff: ('tape_metal', ''),
        0x660b: ('tape_load', ''),
        0x6617: ('no_tape', ''),
        0x6623: ('tape_error', ''),
        0x662f: ('ff', ''),
        0x6637: ('right_arrow', ''),
        0x6639: ('rew', ''),
        0x6641: ('left_arrow', ''),
        0x6643: ('cut_tape', ''),
        0x664c: ('disabled', ''),
        0x6655: ('comm_error', ''),
        0x6660: ('broken_tape', ''),
        0x666c: ('tight_tape', ''),
        0x6677: ('wrapped_tape', ''),
        0x6684: ('cd__', ''),
        0x6690: ('cd_no_cd', ''),
        0x669c: ('cd_tr', ''),
        0x66a8: ('playcd_tr', ''),
        0x66b4: ('cue', ''),
        0x66c0: ('rev', ''),
        0x66cc: ('scan_tr', ''),
        0x66d8: ('track', ''),
        0x66df: ('rdm', ''),
        0x66e3: ('random_one', ''),
        0x66ee: ('random_all', ''),
        0x66f9: ('rev2', ''),
        0x66fd: ('fwd', ''),
        0x6701: ('et', ''),
        0x6704: ('eltm', ''),
        0x6709: ('track_scan', ''),
        0x6717: ('disc_scan', ''),
        0x6725: ('check_cd', ''),
        0x672e: ('player_error', ''),
        0x673b: ('focus', ''),
        0x6741: ('cd_door_open', ''),
        0x674e: ('changer_error', ''),
        0x675c: ('magazine', ''),
        0x6765: ('no_magazin', ''),
        0x6771: ('no_changer', ''),
        0x677d: ('no_disc', ''),
        0x6789: ('cd_cd_rom', ''),
        0x6795: ('cd_cd_err', ''),
        0x67a1: ('cd_error', ''),
        0x67ad: ('chk_magazin', ''),

        0xeffe: ('checksum', ''),
    })


    printer = Printer(memory,
                      start_address,
                      traceable_range[-1] - 1,
                      symbol_table
                      )
    printer.print_listing()
