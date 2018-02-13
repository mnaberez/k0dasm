import sys
import unittest
from k0dasm.disassemble import disassemble

class disassemble_tests(unittest.TestCase):
    def test_00_nop(self):
        pc = 0x1000
        mem = [0x00]
        disasm, new_pc = disassemble(mem, pc)
        self.assertEqual(disasm, "NOP")
        self.assertEqual(new_pc, pc + len(mem))

    def test_01_not1_cy1(self):
        pc = 0x1000
        mem = [0x01]
        disasm, new_pc = disassemble(mem, pc)
        self.assertEqual(disasm, "NOT1 CY")
        self.assertEqual(new_pc, pc + len(mem))

    def test_02_movw_ax_saddrp(self):
        pc = 0x1000
        mem = [0x02, 0x20, 0xfe]
        disasm, new_pc = disassemble(mem, pc)
        self.assertEqual(disasm, "MOVW AX,0fe20H")
        self.assertEqual(new_pc, pc + len(mem))

    def test_03_movw_saddrp_ax(self):
        pc = 0x1000
        mem = [0x03, 0x20, 0xfe]
        disasm, new_pc = disassemble(mem, pc)
        self.assertEqual(disasm, "MOVW 0fe20H,AX")
        self.assertEqual(new_pc, pc + len(mem))

    def test_04_dbnz_saddr_disp(self):
        pc = 0x1000
        for saddr in range(0xfe20, 0xff20):
            saddr_low = saddr & 0xff
            mem = [0x04, saddr_low, 0xFD]
            disasm, new_pc = disassemble(mem, pc)
            self.assertEqual(disasm, "DBNZ 0%04xH,$01000H" % saddr)
            self.assertEqual(new_pc, pc + len(mem))

    def test_05_xch_a_de(self):
        pc = 0x1000
        mem = [0x05]
        disasm, new_pc = disassemble(mem, pc)
        self.assertEqual(disasm, "XCH A,[DE]")
        self.assertEqual(new_pc, pc + len(mem))

    def test_07_xch_a_hl(self):
        pc = 0x1000
        mem = [0x07]
        disasm, new_pc = disassemble(mem, pc)
        self.assertEqual(disasm, "XCH A,[HL]")
        self.assertEqual(new_pc, pc + len(mem))

    def test_08_add_a_addr16(self):
        pc = 0x1000
        for addr16 in (0x0000, 0xabcd, 0xffff):
            low = addr16 & 0xff
            high = (addr16 >> 8) & 0xff
            mem = [0x08, low, high]
            disasm, new_pc = disassemble(mem, pc)
            self.assertEqual(disasm, "ADD A,!0%04xh" % addr16)
            self.assertEqual(new_pc, pc + len(mem))

    def test_09_add_a_hl_plus_byte(self):
        pc = 0x1000
        for byte in (0x00, 0xab, 0xff):
            mem = [0x09, byte]
            disasm, new_pc = disassemble(mem, pc)
            self.assertEqual(disasm, "ADD A,[HL+0%02xH]" % byte)
            self.assertEqual(new_pc, pc + len(mem))

    def test_callf(self):
        d = {0x0C: 0x0800, 0x1C: 0x0900, 0x2C: 0x0A00, 0x3C: 0x0B00,
             0x4C: 0x0C00, 0x5C: 0x0D00, 0x6C: 0x0E00, 0x7C: 0x0F00}

        pc = 0x1000
        for opcode, base in d.items():
            for offset in (0x00, 0xab, 0xff):
                mem = [opcode, offset]
                disasm, new_pc = disassemble(mem, pc)
                address = base + offset
                self.assertEqual(disasm, "CALLF !%04xH" % address)
                self.assertEqual(new_pc, pc + len(mem))

    def test_callt(self):
        d = {0xC1: 0x0040, 0xC3: 0x0042, 0xC5: 0x0044, 0xC7: 0x0046,
             0xC9: 0x0048, 0xCB: 0x004a, 0xCD: 0x004c, 0xCF: 0x004e,
             0xD1: 0x0050, 0xD3: 0x0052, 0xD5: 0x0054, 0xD7: 0x0056,
             0xD9: 0x0058, 0xDB: 0x005A, 0xDD: 0x005C, 0xDF: 0x005e,
             0xE1: 0x0060, 0xE3: 0x0062, 0xE5: 0x0064, 0xE7: 0x0066,
             0xE9: 0x0068, 0xEB: 0x006a, 0xED: 0x006c, 0xEF: 0x006e,
             0xF1: 0x0070, 0xF3: 0x0072, 0xF5: 0x0074, 0xF7: 0x0076,
             0xF9: 0x0078, 0xFB: 0x007a, 0xFD: 0x007c, 0xFF: 0x007e,
            }

        pc = 0x1000
        for opcode, address in d.items():
            mem = [opcode]
            disasm, new_pc = disassemble(mem, pc)
            self.assertEqual(disasm, "CALLT [%04xH]" % address)
            self.assertEqual(new_pc, pc + len(mem))

    def test_0d_add_a_imm(self):
        pc = 0x1000
        for byte in (0, 0xab, 0xff):
            mem = [0x0d, byte]
            disasm, new_pc = disassemble(mem, pc)
            self.assertEqual(disasm, 'ADD A,#0%02xH' % byte)
            self.assertEqual(new_pc, pc + len(mem))

    def test_0e_addr_a_saddr(self):
        pc = 0x1000
        for saddr in range(0xfe20, 0xff20):
            saddr_low = saddr & 0xff
            mem = [0x0e, saddr_low]
            disasm, new_pc = disassemble(mem, pc)
            self.assertEqual(disasm, 'ADD A,0%04xH' % saddr)
            self.assertEqual(new_pc, pc + len(mem))

    def test_0f_add_a_hl(self):
        pc = 0x1000
        mem = [0x0f]
        disasm, new_pc = disassemble(mem, pc)
        self.assertEqual(disasm, 'ADD A,[HL]')
        self.assertEqual(new_pc, pc + len(mem))

    def test_10_12_14_16_movw_regpair_imm16(self):
        d = {0x10: "AX", 0x12: "BC", 0x14: "DE", 0x16: "HL"}

        pc = 0x1000
        for opcode, regpairname in d.items():
            for imm16 in (0x0000, 0xabcd, 0xffff):
                low = imm16 & 0xff
                high = (imm16 >> 8) & 0xff
                mem = [opcode, low, high]
                disasm, new_pc = disassemble(mem, pc)
                self.assertEqual(disasm, 'MOVW %s,#0%04xH' % (regpairname, imm16))
                self.assertEqual(new_pc, pc + len(mem))

    def test_13_mov_sfr_imm8(self):
        pc = 0x1000
        for sfr in range(0xff00, 0x10000):
            sfr_low = sfr & 0xff
            mem = [0x13, sfr_low, 0xab]
            disasm, new_pc = disassemble(mem, pc)
            self.assertEqual(disasm, "MOV 0%04xH,#0abH" % sfr)
            self.assertEqual(new_pc, pc + len(mem))

    def test_18_sub_a_addr16(self):
        pc = 0x1000
        for addr16 in (0x0000, 0xabcd, 0xffff):
            low = addr16 & 0xff
            high = (addr16 >> 8) & 0xff
            mem = [0x18, low, high]
            disasm, new_pc = disassemble(mem, pc)
            self.assertEqual(disasm, 'SUB A,!0%04xH' % addr16)
            self.assertEqual(new_pc, pc + len(mem))

    def test_19_sub_a_hl_plus_offset(self):
        pc = 0x1000
        mem = [0x19, 0xab]
        disasm, new_pc = disassemble(mem, pc)
        self.assertEqual(disasm, 'SUB A,[HL+0abH]')
        self.assertEqual(new_pc, pc + len(mem))

    def test_1d_sub_a_imm8(self):
        pc = 0x1000
        mem = [0x1d, 0xab]
        disasm, new_pc = disassemble(mem, pc)
        self.assertEqual(disasm, 'SUB A,#0abH')
        self.assertEqual(new_pc, pc + len(mem))

    def test_1e_sub_a_saddr(self):
        pc = 0x1000
        for saddr in range(0xfe20, 0xff20):
            saddr_low = saddr & 0xff
            mem = [0x1e, saddr_low]
            disasm, new_pc = disassemble(mem, pc)
            self.assertEqual(disasm, 'SUB A,0%04xH' % saddr)
            self.assertEqual(new_pc, pc + len(mem))

    def test_1f_sub_a_hl(self):
        pc = 0x1000
        mem = [0x1f]
        disasm, new_pc = disassemble(mem, pc)
        self.assertEqual(disasm, "SUB A,[HL]")
        self.assertEqual(new_pc, pc + len(mem))

    def test_20_set1_cy(self):
        pc = 0x1000
        mem = [0x20]
        disasm, new_pc = disassemble(mem, pc)
        self.assertEqual(disasm, "SET1 CY")
        self.assertEqual(new_pc, pc + len(mem))

    def test_21_clr1_cy(self):
        pc = 0x1000
        mem = [0x21]
        disasm, new_pc = disassemble(mem, pc)
        self.assertEqual(disasm, "CLR1 CY")
        self.assertEqual(new_pc, pc + len(mem))

    def test_22_push_psw(self):
        pc = 0x1000
        mem = [0x22]
        disasm, new_pc = disassemble(mem, pc)
        self.assertEqual(disasm, "PUSH PSW")
        self.assertEqual(new_pc, pc + len(mem))

    def test_23_pop_psw(self):
        pc = 0x1000
        mem = [0x23]
        disasm, new_pc = disassemble(mem, pc)
        self.assertEqual(disasm, "POP PSW")
        self.assertEqual(new_pc, pc + len(mem))

    def test_24_ror_a(self):
        pc = 0x1000
        mem = [0x24]
        disasm, new_pc = disassemble(mem, pc)
        self.assertEqual(disasm, "ROR A,1")
        self.assertEqual(new_pc, pc + len(mem))

    def test_25_rorc_a(self):
        pc = 0x1000
        mem = [0x25]
        disasm, new_pc = disassemble(mem, pc)
        self.assertEqual(disasm, "RORC A,1")
        self.assertEqual(new_pc, pc + len(mem))

    def test_26_rol_a(self):
        pc = 0x1000
        mem = [0x26]
        disasm, new_pc = disassemble(mem, pc)
        self.assertEqual(disasm, "ROL A,1")
        self.assertEqual(new_pc, pc + len(mem))

    def test_27_rolc_a(self):
        pc = 0x1000
        mem = [0x27]
        disasm, new_pc = disassemble(mem, pc)
        self.assertEqual(disasm, "ROLC A,1")
        self.assertEqual(new_pc, pc + len(mem))

    def test_27_addc_a_hl(self):
        pc = 0x1000
        mem = [0x27]
        disasm, new_pc = disassemble(mem, pc)
        self.assertEqual(disasm, "ROLC A,1")
        self.assertEqual(new_pc, pc + len(mem))

    def test_28_addc_a_addr16(self):
        pc = 0x1000
        for addr16 in (0x0000, 0xabcd, 0xffff):
            low = addr16 & 0xff
            high = (addr16 >> 8) & 0xff
            mem = [0x28, low, high]
            disasm, new_pc = disassemble(mem, pc)
            self.assertEqual(disasm, 'ADDC A,!0%04xH' % addr16)
            self.assertEqual(new_pc, pc + len(mem))

    def test_29_sub_a_hl_plus_offset(self):
        pc = 0x1000
        mem = [0x29, 0xab]
        disasm, new_pc = disassemble(mem, pc)
        self.assertEqual(disasm, 'ADDC A,[HL+0abH]')
        self.assertEqual(new_pc, pc + len(mem))

    def test_2d_a_imm8(self):
        pc = 0x1000
        mem = [0x2d, 0xab]
        disasm, new_pc = disassemble(mem, pc)
        self.assertEqual(disasm, "ADDC A,#0abH")
        self.assertEqual(new_pc, pc + len(mem))

    def test_2e_addc_a_saddr(self):
        pc = 0x1000
        for saddr in range(0xfe20, 0xff20):
            saddr_low = saddr & 0xff
            mem = [0x2e, saddr_low]
            disasm, new_pc = disassemble(mem, pc)
            self.assertEqual(disasm, 'ADDC A,0%04xH' % saddr)
            self.assertEqual(new_pc, pc + len(mem))

    def test_30_37_xch_a_reg(self):
        d = {0x30: 'XCH A,X',                  0x32: 'XCH A,C',
             0x33: 'XCH A,B', 0x34: 'XCH A,E', 0x35: 'XCH A,D',
             0x36: 'XCH A,L', 0x37: 'XCH A,H'}

        pc = 0x1000
        for opcode, expected_disasm in d.items():
            mem = [opcode]
            disasm, new_pc = disassemble(mem, pc)
            self.assertEqual(disasm, expected_disasm)
            self.assertEqual(new_pc, pc + len(mem))

    def test_48_cmp_a_addr16(self):
        pc = 0x1000
        for addr16 in (0x0000, 0xabcd, 0xffff):
            low = addr16 & 0xff
            high = (addr16 >> 8) & 0xff
            mem = [0x48, low, high]
            disasm, new_pc = disassemble(mem, pc)
            self.assertEqual(disasm, 'CMP A,!0%04xH' % addr16)
            self.assertEqual(new_pc, pc + len(mem))

    def test_39_subc_a_hl_plus_offset(self):
        pc = 0x1000
        mem = [0x39, 0xab]
        disasm, new_pc = disassemble(mem, pc)
        self.assertEqual(disasm, 'SUBC A,[HL+0abH]')
        self.assertEqual(new_pc, pc + len(mem))

    def test_3d_subc_a_imm8(self):
        pc = 0x1000
        mem = [0x3d, 0xab]
        disasm, new_pc = disassemble(mem, pc)
        self.assertEqual(disasm, "SUBC A,#0abH")
        self.assertEqual(new_pc, pc + len(mem))

    def test_3e_subc_a_saddr(self):
        pc = 0x1000
        for saddr in range(0xfe20, 0xff20):
            saddr_low = saddr & 0xff
            mem = [0x3e, saddr_low]
            disasm, new_pc = disassemble(mem, pc)
            self.assertEqual(disasm, 'SUBC A,0%04xH' % saddr)
            self.assertEqual(new_pc, pc + len(mem))

    def test_3f_subc_a_hl(self):
        pc = 0x1000
        mem = [0x3f]
        disasm, new_pc = disassemble(mem, pc)
        self.assertEqual(disasm, "SUBC A,[HL]")
        self.assertEqual(new_pc, pc + len(mem))

    def test_40_47_inc_reg(self):
        d = {0x40: 'INC X', 0x41: 'INC A', 0x42: 'INC C',
             0x43: 'INC B', 0x44: 'INC E', 0x45: 'INC D',
             0x46: 'INC L', 0x47: 'INC H'}

        pc = 0x1000
        for opcode, expected_disasm in d.items():
            mem = [opcode]
            disasm, new_pc = disassemble(mem, pc)
            self.assertEqual(disasm, expected_disasm)
            self.assertEqual(new_pc, pc + len(mem))

    def test_49_cmp_a_hl_plus_offset(self):
        pc = 0x1000
        mem = [0x49, 0xab]
        disasm, new_pc = disassemble(mem, pc)
        self.assertEqual(disasm, 'CMP A,[HL+0abH]')
        self.assertEqual(new_pc, pc + len(mem))

    def test_4d_cmp_a_imm8(self):
        pc = 0x1000
        mem = [0x4d, 0xab]
        disasm, new_pc = disassemble(mem, pc)
        self.assertEqual(disasm, "CMP A,#0abH")
        self.assertEqual(new_pc, pc + len(mem))

    def test_4e_cmp_a_saddr(self):
        pc = 0x1000
        for saddr in range(0xfe20, 0xff20):
            saddr_low = saddr & 0xff
            mem = [0x4e, saddr_low]
            disasm, new_pc = disassemble(mem, pc)
            self.assertEqual(disasm, 'CMP A,0%04xH' % saddr)
            self.assertEqual(new_pc, pc + len(mem))

    def test_4f_cmp_a_hl(self):
        pc = 0x1000
        mem = [0x4f]
        disasm, new_pc = disassemble(mem, pc)
        self.assertEqual(disasm, "CMP A,[HL]")
        self.assertEqual(new_pc, pc + len(mem))

    def test_50_57_dec_reg(self):
        d = {0x50: 'DEC X', 0x51: 'DEC A', 0x52: 'DEC C',
             0x53: 'DEC B', 0x54: 'DEC E', 0x55: 'DEC D',
             0x56: 'DEC L', 0x57: 'DEC H'}

        pc = 0x1000
        for opcode, expected_disasm in d.items():
            mem = [opcode]
            disasm, new_pc = disassemble(mem, pc)
            self.assertEqual(disasm, expected_disasm)
            self.assertEqual(new_pc, pc + len(mem))

    def test_58_and_a_addr16(self):
        pc = 0x1000
        for addr16 in (0x0000, 0xabcd, 0xffff):
            low = addr16 & 0xff
            high = (addr16 >> 8) & 0xff
            mem = [0x58, low, high]
            disasm, new_pc = disassemble(mem, pc)
            self.assertEqual(disasm, 'AND A,!0%04xH' % addr16)
            self.assertEqual(new_pc, pc + len(mem))

    def test_59_and_a_hl_plus_offset(self):
        pc = 0x1000
        mem = [0x59, 0xab]
        disasm, new_pc = disassemble(mem, pc)
        self.assertEqual(disasm, 'AND A,[HL+0abH]')
        self.assertEqual(new_pc, pc + len(mem))

    def test_5d_and_a_imm8(self):
        pc = 0x1000
        mem = [0x5d, 0xab]
        disasm, new_pc = disassemble(mem, pc)
        self.assertEqual(disasm, "AND A,#0abH")
        self.assertEqual(new_pc, pc + len(mem))

    def test_5e_and_a_saddr(self):
        pc = 0x1000
        for saddr in range(0xfe20, 0xff20):
            saddr_low = saddr & 0xff
            mem = [0x5e, saddr_low]
            disasm, new_pc = disassemble(mem, pc)
            self.assertEqual(disasm, 'AND A,0%04xH' % saddr)
            self.assertEqual(new_pc, pc + len(mem))

    def test_5f_and_a_hl(self):
        pc = 0x1000
        mem = [0x5f]
        disasm, new_pc = disassemble(mem, pc)
        self.assertEqual(disasm, "AND A,[HL]")
        self.assertEqual(new_pc, pc + len(mem))

    def test_60_67_mov_a_reg(self):
        d = {0x60: 'MOV A,X',                  0x62: 'MOV A,C',
             0x63: 'MOV A,B', 0x64: 'MOV A,E', 0x65: 'MOV A,D',
             0x66: 'MOV A,L', 0x67: 'MOV A,H'}

        pc = 0x1000
        for opcode, expected_disasm in d.items():
            mem = [opcode]
            disasm, new_pc = disassemble(mem, pc)
            self.assertEqual(disasm, expected_disasm)
            self.assertEqual(new_pc, pc + len(mem))

    def test_61_80_adjba(self):
        pc = 0x1000
        mem = [0x61, 0x80]
        disasm, new_pc = disassemble(mem, pc)
        self.assertEqual(disasm, "ADJBA")
        self.assertEqual(new_pc, pc + len(mem))

    def test_61_90_adjbs(self):
        pc = 0x1000
        mem = [0x61, 0x90]
        disasm, new_pc = disassemble(mem, pc)
        self.assertEqual(disasm, "ADJBS")
        self.assertEqual(new_pc, pc + len(mem))

    def test_61_00_thru_07_and_reg_a(self):
        d = {0x00: 'ADD X,A', 0x01: 'ADD A,A', 0x02: 'ADD C,A',
             0x03: 'ADD B,A', 0x04: 'ADD E,A', 0x05: 'ADD D,A',
             0x06: 'ADD L,A', 0x07: 'ADD H,A'}

        pc = 0x1000
        for operand, expected_disasm in d.items():
            mem = [0x61, operand]
            disasm, new_pc = disassemble(mem, pc)
            self.assertEqual(disasm, expected_disasm)
            self.assertEqual(new_pc, pc + len(mem))

    def test_61_08_thru_0f_add_a_reg(self):
        d = {0x08: 'ADD A,X', 0x09: 'ADD A,A', 0x0a: 'ADD A,C',
             0x0b: 'ADD A,B', 0x0c: 'ADD A,E', 0x0d: 'ADD A,D',
             0x0e: 'ADD A,L', 0x0f: 'ADD A,H'}

        pc = 0x1000
        for operand, expected_disasm in d.items():
            mem = [0x61, operand]
            disasm, new_pc = disassemble(mem, pc)
            self.assertEqual(disasm, expected_disasm)
            self.assertEqual(new_pc, pc + len(mem))

    def test_61_10_thru_17_and_reg_a(self):
        d = {0x10: 'SUB X,A', 0x11: 'SUB A,A', 0x12: 'SUB C,A',
             0x13: 'SUB B,A', 0x14: 'SUB E,A', 0x15: 'SUB D,A',
             0x16: 'SUB L,A', 0x17: 'SUB H,A'}

        pc = 0x1000
        for operand, expected_disasm in d.items():
            mem = [0x61, operand]
            disasm, new_pc = disassemble(mem, pc)
            self.assertEqual(disasm, expected_disasm)
            self.assertEqual(new_pc, pc + len(mem))

    def test_61_18_thru_1f_sub_a_reg(self):
        d = {0x18: 'SUB A,X', 0x19: 'SUB A,A', 0x1a: 'SUB A,C',
             0x1b: 'SUB A,B', 0x1c: 'SUB A,E', 0x1d: 'SUB A,D',
             0x1e: 'SUB A,L', 0x1f: 'SUB A,H'}

        pc = 0x1000
        for operand, expected_disasm in d.items():
            mem = [0x61, operand]
            disasm, new_pc = disassemble(mem, pc)
            self.assertEqual(disasm, expected_disasm)
            self.assertEqual(new_pc, pc + len(mem))

    def test_61_20_thru_27_addc_reg_a(self):
        d = {0x20: 'ADDC X,A', 0x21: 'ADDC A,A', 0x22: 'ADDC C,A',
             0x23: 'ADDC B,A', 0x24: 'ADDC E,A', 0x25: 'ADDC D,A',
             0x26: 'ADDC L,A', 0x27: 'ADDC H,A'}

        pc = 0x1000
        for operand, expected_disasm in d.items():
            mem = [0x61, operand]
            disasm, new_pc = disassemble(mem, pc)
            self.assertEqual(disasm, expected_disasm)
            self.assertEqual(new_pc, pc + len(mem))

    def test_61_28_thru_2f_addc_a_reg(self):
        d = {0x28: 'ADDC A,X', 0x29: 'ADDC A,A', 0x2a: 'ADDC A,C',
             0x2b: 'ADDC A,B', 0x2c: 'ADDC A,E', 0x2d: 'ADDC A,D',
             0x2e: 'ADDC A,L', 0x2f: 'ADDC A,H'}

        pc = 0x1000
        for operand, expected_disasm in d.items():
            mem = [0x61, operand]
            disasm, new_pc = disassemble(mem, pc)
            self.assertEqual(disasm, expected_disasm)
            self.assertEqual(new_pc, pc + len(mem))

    def test_61_30_thru_37_subc_reg_a(self):
        d = {0x30: 'SUBC X,A', 0x31: 'SUBC A,A', 0x32: 'SUBC C,A',
             0x33: 'SUBC B,A', 0x34: 'SUBC E,A', 0x35: 'SUBC D,A',
             0x36: 'SUBC L,A', 0x37: 'SUBC H,A'}

        pc = 0x1000
        for operand, expected_disasm in d.items():
            mem = [0x61, operand]
            disasm, new_pc = disassemble(mem, pc)
            self.assertEqual(disasm, expected_disasm)
            self.assertEqual(new_pc, pc + len(mem))

    def test_61_38_thru_3f_subc_a_reg(self):
        d = {0x38: 'SUBC A,X', 0x39: 'SUBC A,A', 0x3a: 'SUBC A,C',
             0x3b: 'SUBC A,B', 0x3c: 'SUBC A,E', 0x3d: 'SUBC A,D',
             0x3e: 'SUBC A,L', 0x3f: 'SUBC A,H'}

        pc = 0x1000
        for operand, expected_disasm in d.items():
            mem = [0x61, operand]
            disasm, new_pc = disassemble(mem, pc)
            self.assertEqual(disasm, expected_disasm)
            self.assertEqual(new_pc, pc + len(mem))

    def test_61_40_thru_47_cmp_reg_a(self):
        d = {0x40: 'CMP X,A', 0x41: 'CMP A,A', 0x42: 'CMP C,A',
             0x43: 'CMP B,A', 0x44: 'CMP E,A', 0x45: 'CMP D,A',
             0x46: 'CMP L,A', 0x47: 'CMP H,A'}

        pc = 0x1000
        for operand, expected_disasm in d.items():
            mem = [0x61, operand]
            disasm, new_pc = disassemble(mem, pc)
            self.assertEqual(disasm, expected_disasm)
            self.assertEqual(new_pc, pc + len(mem))

    def test_61_48_thru_4f_cmp_a_reg(self):
        d = {0x48: 'CMP A,X', 0x49: 'CMP A,A', 0x4a: 'CMP A,C',
             0x4b: 'CMP A,B', 0x4c: 'CMP A,E', 0x4d: 'CMP A,D',
             0x4e: 'CMP A,L', 0x4f: 'CMP A,H'}

        pc = 0x1000
        for operand, expected_disasm in d.items():
            mem = [0x61, operand]
            disasm, new_pc = disassemble(mem, pc)
            self.assertEqual(disasm, expected_disasm)
            self.assertEqual(new_pc, pc + len(mem))

    def test_61_50_thru_57_and_reg_a(self):
        d = {0x50: 'AND X,A', 0x51: 'AND A,A', 0x52: 'AND C,A',
             0x53: 'AND B,A', 0x54: 'AND E,A', 0x55: 'AND D,A',
             0x56: 'AND L,A', 0x57: 'AND H,A'}

        pc = 0x1000
        for operand, expected_disasm in d.items():
            mem = [0x61, operand]
            disasm, new_pc = disassemble(mem, pc)
            self.assertEqual(disasm, expected_disasm)
            self.assertEqual(new_pc, pc + len(mem))

    def test_61_58_thru_5f_and_a_reg(self):
        d = {0x58: 'AND A,X', 0x59: 'AND A,A', 0x5a: 'AND A,C',
             0x5b: 'AND A,B', 0x5c: 'AND A,E', 0x5d: 'AND A,D',
             0x5e: 'AND A,L', 0x5f: 'AND A,H'}

        pc = 0x1000
        for operand, expected_disasm in d.items():
            mem = [0x61, operand]
            disasm, new_pc = disassemble(mem, pc)
            self.assertEqual(disasm, expected_disasm)
            self.assertEqual(new_pc, pc + len(mem))

    def test_61_60_thru_67_or_reg_a(self):
        d = {0x60: 'OR X,A', 0x61: 'OR A,A', 0x62: 'OR C,A',
             0x63: 'OR B,A', 0x64: 'OR E,A', 0x65: 'OR D,A',
             0x66: 'OR L,A', 0x67: 'OR H,A'}

        pc = 0x1000
        for operand, expected_disasm in d.items():
            mem = [0x61, operand]
            disasm, new_pc = disassemble(mem, pc)
            self.assertEqual(disasm, expected_disasm)
            self.assertEqual(new_pc, pc + len(mem))

    def test_61_68_thru_6f_or_a_reg(self):
        d = {0x68: 'OR A,X', 0x69: 'OR A,A', 0x6a: 'OR A,C',
             0x6b: 'OR A,B', 0x6c: 'OR A,E', 0x6d: 'OR A,D',
             0x6e: 'OR A,L', 0x6f: 'OR A,H'}

        pc = 0x1000
        for operand, expected_disasm in d.items():
            mem = [0x61, operand]
            disasm, new_pc = disassemble(mem, pc)
            self.assertEqual(disasm, expected_disasm)
            self.assertEqual(new_pc, pc + len(mem))

    def test_61_70_thru_77_or_reg_a(self):
        d = {0x70: 'XOR X,A', 0x71: 'XOR A,A', 0x72: 'XOR C,A',
             0x73: 'XOR B,A', 0x74: 'XOR E,A', 0x75: 'XOR D,A',
             0x76: 'XOR L,A', 0x77: 'XOR H,A'}

        pc = 0x1000
        for operand, expected_disasm in d.items():
            mem = [0x61, operand]
            disasm, new_pc = disassemble(mem, pc)
            self.assertEqual(disasm, expected_disasm)
            self.assertEqual(new_pc, pc + len(mem))

    def test_61_78_thru_7f_or_a_reg(self):
        d = {0x78: 'XOR A,X', 0x79: 'XOR A,A', 0x7a: 'XOR A,C',
             0x7b: 'XOR A,B', 0x7c: 'XOR A,E', 0x7d: 'XOR A,D',
             0x7e: 'XOR A,L', 0x7f: 'XOR A,H'}

        pc = 0x1000
        for operand, expected_disasm in d.items():
            mem = [0x61, operand]
            disasm, new_pc = disassemble(mem, pc)
            self.assertEqual(disasm, expected_disasm)
            self.assertEqual(new_pc, pc + len(mem))

    def test_61_dx_fx_sel_rbx(self):
        d = {0xd0: 'SEL RB0', 0xd8: 'SEL RB1',
             0xf0: 'SEL RB2', 0xf8: 'SEL RB3'}

        pc = 0x1000
        for operand, expected_disasm in d.items():
            mem = [0x61, operand]
            disasm, new_pc = disassemble(mem, pc)
            self.assertEqual(disasm, expected_disasm)
            self.assertEqual(new_pc, pc + len(mem))

    def test_61_x9_mov1_a_bit_cy(self):
        operands = (0x89, 0x99, 0xa9, 0xb9, 0xc9, 0xd9, 0xe9, 0xf9)

        pc = 0x1000
        for bit, operand in enumerate(operands):
            mem = [0x61, operand]
            disasm, new_pc = disassemble(mem, pc)
            self.assertEqual(disasm, "MOV1 A.%d,CY" % bit)
            self.assertEqual(new_pc, pc + len(mem))

    def test_61_xa_set1_a_bit(self):
        operands = (0x8a, 0x9a, 0xaa, 0xba, 0xca, 0xda, 0xea, 0xfa)

        pc = 0x1000
        for bit, operand in enumerate(operands):
            mem = [0x61, operand]
            disasm, new_pc = disassemble(mem, pc)
            self.assertEqual(disasm, "SET1 A.%d" % bit)
            self.assertEqual(new_pc, pc + len(mem))

    def test_61_xb_clr1_a_bit(self):
        operands = (0x8b, 0x9b, 0xab, 0xbb, 0xcb, 0xdb, 0xeb, 0xfb)

        pc = 0x1000
        for bit, operand in enumerate(operands):
            mem = [0x61, operand]
            disasm, new_pc = disassemble(mem, pc)
            self.assertEqual(disasm, "CLR1 A.%d" % bit)
            self.assertEqual(new_pc, pc + len(mem))

    def test_61_xc_mov1_cy_a_bit(self):
        operands = (0x8c, 0x9c, 0xac, 0xbc, 0xcc, 0xdc, 0xec, 0xfc)

        pc = 0x1000
        for bit, operand in enumerate(operands):
            mem = [0x61, operand]
            disasm, new_pc = disassemble(mem, pc)
            self.assertEqual(disasm, "MOV1 CY,A.%d" % bit)
            self.assertEqual(new_pc, pc + len(mem))

    def test_61_xd_and1_cy_a_bit(self):
        operands = (0x8d, 0x9d, 0xad, 0xbd, 0xcd, 0xdd, 0xed, 0xfd)

        pc = 0x1000
        for bit, operand in enumerate(operands):
            mem = [0x61, operand]
            disasm, new_pc = disassemble(mem, pc)
            self.assertEqual(disasm, "AND1 CY,A.%d" % bit)
            self.assertEqual(new_pc, pc + len(mem))

    def test_61_xe_or1_cy_a_bit(self):
        operands = (0x8e, 0x9e, 0xae, 0xbe, 0xce, 0xde, 0xee, 0xfe)

        pc = 0x1000
        for bit, operand in enumerate(operands):
            mem = [0x61, operand]
            disasm, new_pc = disassemble(mem, pc)
            self.assertEqual(disasm, "OR1 CY,A.%d" % bit)
            self.assertEqual(new_pc, pc + len(mem))

    def test_61_xf_xor1_cy_a_bit(self):
        operands = (0x8f, 0x9f, 0xaf, 0xbf, 0xcf, 0xdf, 0xef, 0xff)

        pc = 0x1000
        for bit, operand in enumerate(operands):
            mem = [0x61, operand]
            disasm, new_pc = disassemble(mem, pc)
            self.assertEqual(disasm, "XOR1 CY,A.%d" % bit)
            self.assertEqual(new_pc, pc + len(mem))

    def test_68_or_a_addr16(self):
        pc = 0x1000
        for addr16 in (0x0000, 0xabcd, 0xffff):
            low = addr16 & 0xff
            high = (addr16 >> 8) & 0xff
            mem = [0x68, low, high]
            disasm, new_pc = disassemble(mem, pc)
            self.assertEqual(disasm, 'OR A,!0%04xH' % addr16)
            self.assertEqual(new_pc, pc + len(mem))

    def test_69_or_a_hl_plus_offset(self):
        pc = 0x1000
        mem = [0x69, 0xab]
        disasm, new_pc = disassemble(mem, pc)
        self.assertEqual(disasm, 'OR A,[HL+0abH]')
        self.assertEqual(new_pc, pc + len(mem))

    def test_6d_or_a_imm8(self):
        pc = 0x1000
        mem = [0x6d, 0xab]
        disasm, new_pc = disassemble(mem, pc)
        self.assertEqual(disasm, "OR A,#0abH")
        self.assertEqual(new_pc, pc + len(mem))

    def test_6e_or_a_saddr(self):
        pc = 0x1000
        for saddr in range(0xfe20, 0xff20):
            saddr_low = saddr & 0xff
            mem = [0x6e, saddr_low]
            disasm, new_pc = disassemble(mem, pc)
            self.assertEqual(disasm, 'OR A,0%04xH' % saddr)
            self.assertEqual(new_pc, pc + len(mem))

    def test_6f_or_a_hl(self):
        pc = 0x1000
        mem = [0x6f]
        disasm, new_pc = disassemble(mem, pc)
        self.assertEqual(disasm, "OR A,[HL]")
        self.assertEqual(new_pc, pc + len(mem))

    def test_70_77_mov_a_reg(self):
        d = {0x70: 'MOV X,A',                  0x72: 'MOV C,A',
             0x73: 'MOV B,A', 0x74: 'MOV E,A', 0x75: 'MOV D,A',
             0x76: 'MOV L,A', 0x77: 'MOV H,A'}

        pc = 0x1000
        for opcode, expected_disasm in d.items():
            mem = [opcode]
            disasm, new_pc = disassemble(mem, pc)
            self.assertEqual(disasm, expected_disasm)
            self.assertEqual(new_pc, pc + len(mem))

    def test_71_00_stop(self):
        pc = 0x1000
        mem = [0x71, 0x00]
        disasm, new_pc = disassemble(mem, pc)
        self.assertEqual(disasm, 'STOP')
        self.assertEqual(new_pc, pc + len(mem))

    def test_71_01_mov1_saddr_bit_cy(self):
        operands = (0x01, 0x11, 0x21, 0x31, 0x41, 0x51, 0x61, 0x71)
        pc = 0x1000
        for bit, operand in enumerate(operands):
            for saddr in range(0xfe20, 0xff20):
                if saddr == 0xff1e:
                    continue # special case; would disassemble as MOV1 PSW.bit,CY
                saddr_low = saddr & 0xff
                mem = [0x71, operand, saddr_low]
                disasm, new_pc = disassemble(mem, pc)
                self.assertEqual(disasm, "MOV1 0%04xH.%d,CY" % (saddr, bit))
                self.assertEqual(new_pc, pc + len(mem))

    def test_71_01_mov1_psw_bit_cy(self):
        operands = (0x01, 0x11, 0x21, 0x31, 0x41, 0x51, 0x61, 0x71)
        pc = 0x1000
        for bit, operand in enumerate(operands):
            mem = [0x71, operand, 0x1e]
            disasm, new_pc = disassemble(mem, pc)
            self.assertEqual(disasm, "MOV1 PSW.%d,CY" % bit)
            self.assertEqual(new_pc, pc + len(mem))

    def test_71_04_thru_74_mov1_cy_saddr_bit(self):
        operands = (0x04, 0x14, 0x24, 0x34, 0x44, 0x54, 0x64, 0x74)
        pc = 0x1000
        for bit, operand in enumerate(operands):
            for saddr in range(0xfe20, 0xff20):
                if saddr == 0xff1e:
                    continue # special case; would disassemble as MOV1 CY,PSW.bit
                saddr_low = saddr & 0xff
                mem = [0x71, operand, saddr_low]
                disasm, new_pc = disassemble(mem, pc)
                self.assertEqual(disasm, "MOV1 CY,0%04xH.%d" % (saddr, bit))
                self.assertEqual(new_pc, pc + len(mem))

    def test_71_04_thru_74_cy_psw_bit(self):
        operands = (0x04, 0x14, 0x24, 0x34, 0x44, 0x54, 0x64, 0x74)
        pc = 0x1000
        for bit, operand in enumerate(operands):
            mem = [0x71, operand, 0x1e]
            disasm, new_pc = disassemble(mem, pc)
            self.assertEqual(disasm, "MOV1 CY,PSW.%d" % bit)
            self.assertEqual(new_pc, pc + len(mem))

    def test_71_05_thru_75_and1_cy_saddr_bit(self):
        operands = (0x05, 0x15, 0x25, 0x35, 0x45, 0x55, 0x65, 0x75)
        pc = 0x1000
        for bit, operand in enumerate(operands):
            for saddr in range(0xfe20, 0xff20):
                if saddr == 0xff1e:
                    continue # special case; would disassemble as AND1 CY,PSW.bit
                saddr_low = saddr & 0xff
                mem = [0x71, operand, saddr_low]
                disasm, new_pc = disassemble(mem, pc)
                self.assertEqual(disasm, "AND1 CY,0%04xH.%d" % (saddr, bit))
                self.assertEqual(new_pc, pc + len(mem))

    def test_71_05_thru_75_and1_cy_psw_bit(self):
        operands = (0x05, 0x15, 0x25, 0x35, 0x45, 0x55, 0x65, 0x75)
        pc = 0x1000
        for bit, operand in enumerate(operands):
            mem = [0x71, operand, 0x1e]
            disasm, new_pc = disassemble(mem, pc)
            self.assertEqual(disasm, "AND1 CY,PSW.%d" % bit)
            self.assertEqual(new_pc, pc + len(mem))

    def test_71_06_thru_76_or1_cy_saddr_bit(self):
        operands = (0x06, 0x16, 0x26, 0x36, 0x46, 0x56, 0x66, 0x76)
        pc = 0x1000
        for bit, operand in enumerate(operands):
            for saddr in range(0xfe20, 0xff20):
                if saddr == 0xff1e:
                    continue # special case; would disassemble as OR1 CY,PSW.bit
                saddr_low = saddr & 0xff
                mem = [0x71, operand, saddr_low]
                disasm, new_pc = disassemble(mem, pc)
                self.assertEqual(disasm, "OR1 CY,0%04xH.%d" % (saddr, bit))
                self.assertEqual(new_pc, pc + len(mem))

    def test_71_06_thru_76_or1_cy_psw_bit(self):
        operands = (0x06, 0x16, 0x26, 0x36, 0x46, 0x56, 0x66, 0x76)
        pc = 0x1000
        for bit, operand in enumerate(operands):
            mem = [0x71, operand, 0x1e]
            disasm, new_pc = disassemble(mem, pc)
            self.assertEqual(disasm, "OR1 CY,PSW.%d" % bit)
            self.assertEqual(new_pc, pc + len(mem))

    def test_71_07_thru_77_xor1_cy_saddr_bit(self):
        operands = (0x07, 0x17, 0x27, 0x37, 0x47, 0x57, 0x67, 0x77)
        pc = 0x1000
        for bit, operand in enumerate(operands):
            for saddr in range(0xfe20, 0xff20):
                if saddr == 0xff1e:
                    continue # special case; would disassemble as XOR1 CY,PSW.bit
                saddr_low = saddr & 0xff
                mem = [0x71, operand, saddr_low]
                disasm, new_pc = disassemble(mem, pc)
                self.assertEqual(disasm, "XOR1 CY,0%04xH.%d" % (saddr, bit))
                self.assertEqual(new_pc, pc + len(mem))

    def test_71_07_thru_77_xor1_cy_psw_bit(self):
        operands = (0x07, 0x17, 0x27, 0x37, 0x47, 0x57, 0x67, 0x77)
        pc = 0x1000
        for bit, operand in enumerate(operands):
            mem = [0x71, operand, 0x1e]
            disasm, new_pc = disassemble(mem, pc)
            self.assertEqual(disasm, "XOR1 CY,PSW.%d" % bit)
            self.assertEqual(new_pc, pc + len(mem))

    def test_71_10_halt(self):
        pc = 0x1000
        mem = [0x71, 0x10]
        disasm, new_pc = disassemble(mem, pc)
        self.assertEqual(disasm, 'HALT')
        self.assertEqual(new_pc, pc + len(mem))

    def test_71_09_thru_79_mov1_sfr_bit_cy(self):
        operands = (0x09, 0x19, 0x29, 0x39, 0x49, 0x59, 0x69, 0x79)
        pc = 0x1000
        for bit, operand in enumerate(operands):
            for sfr in range(0xff00, 0x10000):
                sfr_low = sfr & 0xff
                mem = [0x71, operand, sfr_low]
                disasm, new_pc = disassemble(mem, pc)
                self.assertEqual(disasm, 'MOV1 0%04xH.%d,CY' % (sfr, bit))
                self.assertEqual(new_pc, pc + len(mem))

    def test_71_0a_set1_sfr_bit(self):
        operands = (0x0a, 0x1a, 0x2a, 0x3a, 0x4a, 0x5a, 0x6a, 0x7a)
        pc = 0x1000
        for bit, operand in enumerate(operands):
            for sfr in range(0xff00, 0x10000):
                sfr_low = sfr & 0xff
                mem = [0x71, operand, sfr_low]
                disasm, new_pc = disassemble(mem, pc)
                self.assertEqual(disasm, 'SET1 0%04xH.%d' % (sfr, bit))
                self.assertEqual(new_pc, pc + len(mem))

    def test_71_0c_thru_7c_mov1_cy_sfr_bit(self):
        operands = (0x0c, 0x1c, 0x2c, 0x3c, 0x4c, 0x5c, 0x6c, 0x7c)
        pc = 0x1000
        for bit, operand in enumerate(operands):
            for sfr in range(0xff00, 0x10000):
                sfr_low = sfr & 0xff
                mem = [0x71, operand, sfr_low]
                disasm, new_pc = disassemble(mem, pc)
                self.assertEqual(disasm, 'MOV1 CY,0%04xH.%d' % (sfr, bit))
                self.assertEqual(new_pc, pc + len(mem))

    def test_72_82_thru_f3_clr1_hl_bit(self):
        operands = (0x82, 0x92, 0xa2, 0xb2, 0xc2, 0xd2, 0xe2, 0xf2)
        pc = 0x1000
        for bit, operand in enumerate(operands):
            mem = [0x71, operand]
            disasm, new_pc = disassemble(mem, pc)
            self.assertEqual(disasm, 'SET1 [HL].%d' % bit)
            self.assertEqual(new_pc, pc + len(mem))

    def test_71_83_thru_f3_clr1_hl_bit(self):
        operands = (0x83, 0x93, 0xa3, 0xb3, 0xc3, 0xd3, 0xe3, 0xf3)
        pc = 0x1000
        for bit, operand in enumerate(operands):
            mem = [0x71, operand]
            disasm, new_pc = disassemble(mem, pc)
            self.assertEqual(disasm, 'CLR1 [HL].%d' % bit)
            self.assertEqual(new_pc, pc + len(mem))

    def test_71_84_thru_f4_mov1_hl_bit(self):
        operands = (0x84, 0x94, 0xa4, 0xb4, 0xc4, 0xd4, 0xe4, 0xf4)
        pc = 0x1000
        for bit, operand in enumerate(operands):
            mem = [0x71, operand]
            disasm, new_pc = disassemble(mem, pc)
            self.assertEqual(disasm, 'MOV1 CY,[HL].%d' % bit)
            self.assertEqual(new_pc, pc + len(mem))

    def test_71_84_thru_f4_and1_hl_bit(self):
        operands = (0x85, 0x95, 0xa5, 0xb5, 0xc5, 0xd5, 0xe5, 0xf5)
        pc = 0x1000
        for bit, operand in enumerate(operands):
            mem = [0x71, operand]
            disasm, new_pc = disassemble(mem, pc)
            self.assertEqual(disasm, 'AND1 CY,[HL].%d' % bit)
            self.assertEqual(new_pc, pc + len(mem))

    def test_71_86_thru_f6_and1_hl_bit(self):
        operands = (0x86, 0x96, 0xa6, 0xb6, 0xc6, 0xd6, 0xe6, 0xf6)
        pc = 0x1000
        for bit, operand in enumerate(operands):
            mem = [0x71, operand]
            disasm, new_pc = disassemble(mem, pc)
            self.assertEqual(disasm, 'OR1 CY,[HL].%d' % bit)
            self.assertEqual(new_pc, pc + len(mem))

    def test_71_87_thru_f7_and1_hl_bit(self):
        operands = (0x87, 0x97, 0xa7, 0xb7, 0xc7, 0xd7, 0xe7, 0xf7)
        pc = 0x1000
        for bit, operand in enumerate(operands):
            mem = [0x71, operand]
            disasm, new_pc = disassemble(mem, pc)
            self.assertEqual(disasm, 'XOR1 CY,[HL].%d' % bit)
            self.assertEqual(new_pc, pc + len(mem))

    def test_71_81_thru_f1_mov1_hl_bit_cy(self):
        operands = (0x81, 0x91, 0xa1, 0xb1, 0xc1, 0xd1, 0xe1, 0xf1)
        pc = 0x1000
        for bit, operand in enumerate(operands):
            mem = [0x71, operand]
            disasm, new_pc = disassemble(mem, pc)
            self.assertEqual(disasm, 'MOV1 [HL].%d,CY' % bit)
            self.assertEqual(new_pc, pc + len(mem))

    def test_78_xor_a_addr16(self):
        pc = 0x1000
        for addr16 in (0x0000, 0xabcd, 0xffff):
            low = addr16 & 0xff
            high = (addr16 >> 8) & 0xff
            mem = [0x78, low, high]
            disasm, new_pc = disassemble(mem, pc)
            self.assertEqual(disasm, 'XOR A,!0%04xH' % addr16)
            self.assertEqual(new_pc, pc + len(mem))

    def test_79_xor_a_hl_plus_offset(self):
        pc = 0x1000
        mem = [0x79, 0xab]
        disasm, new_pc = disassemble(mem, pc)
        self.assertEqual(disasm, 'XOR A,[HL+0abH]')
        self.assertEqual(new_pc, pc + len(mem))

    def test_7d_xor_a_imm8(self):
        pc = 0x1000
        mem = [0x7d, 0xab]
        disasm, new_pc = disassemble(mem, pc)
        self.assertEqual(disasm, "XOR A,#0abH")
        self.assertEqual(new_pc, pc + len(mem))

    def test_7e_xor_a_saddr(self):
        pc = 0x1000
        for saddr in range(0xfe20, 0xff20):
            saddr_low = saddr & 0xff
            mem = [0x7e, saddr_low]
            disasm, new_pc = disassemble(mem, pc)
            self.assertEqual(disasm, 'XOR A,0%04xH' % saddr)
            self.assertEqual(new_pc, pc + len(mem))

    def test_7f_xor_a_hl(self):
        pc = 0x1000
        mem = [0x7f]
        disasm, new_pc = disassemble(mem, pc)
        self.assertEqual(disasm, "XOR A,[HL]")
        self.assertEqual(new_pc, pc + len(mem))

    def test_80_82_84_86_incw_regpair(self):
        d = {0x80: "INCW AX", 0x82: "INCW BC",
             0x84: "INCW DE", 0x86: "INCW HL"}

        pc = 0x1000
        for opcode, expected_disasm in d.items():
            mem = [opcode]
            disasm, new_pc = disassemble(mem, pc)
            self.assertEqual(disasm, expected_disasm)
            self.assertEqual(new_pc, pc + len(mem))

    def test_81_inc_saddr(self):
        pc = 0x1000
        for saddr in range(0xfe20, 0xff20):
            saddr_low = saddr & 0xff
            mem = [0x81, saddr_low]
            disasm, new_pc = disassemble(mem, pc)
            self.assertEqual(disasm, "INC 0%04xH" % saddr)
            self.assertEqual(new_pc, pc + len(mem))

    def test_83_xch_a_saddr(self):
        pc = 0x1000
        for saddr in range(0xfe20, 0xff20):
            saddr_low = saddr & 0xff
            mem = [0x83, saddr_low]
            disasm, new_pc = disassemble(mem, pc)
            self.assertEqual(disasm, "XCH A,0%04xH" % saddr)
            self.assertEqual(new_pc, pc + len(mem))

    def test_85_mov_a_de(self):
        pc = 0x1000
        mem = [0x85]
        disasm, new_pc = disassemble(mem, pc)
        self.assertEqual(disasm, "MOV A,[DE]")
        self.assertEqual(new_pc, pc + len(mem))

    def test_87_mov_a_hl(self):
        pc = 0x1000
        mem = [0x87]
        disasm, new_pc = disassemble(mem, pc)
        self.assertEqual(disasm, "MOV A,[HL]")
        self.assertEqual(new_pc, pc + len(mem))

    def test_88_add_saddr_imm8(self):
        pc = 0x1000
        for saddr in range(0xfe20, 0xff20):
            saddr_low = saddr & 0xff
            mem = [0x88, saddr_low, 0xab]
            disasm, new_pc = disassemble(mem, pc)
            self.assertEqual(disasm, "ADD 0%04xH,#0abH" % saddr)
            self.assertEqual(new_pc, pc + len(mem))

    def test_8a_bc_rel(self):
        pc = 0x1000
        mem = [0x8a, 0xfe]
        disasm, new_pc = disassemble(mem, pc)
        self.assertEqual(disasm, "DBNZ C,$01000H")
        self.assertEqual(new_pc, pc + len(mem))

    def test_8b_bc_rel(self):
        pc = 0x1000
        mem = [0x8b, 0xfe]
        disasm, new_pc = disassemble(mem, pc)
        self.assertEqual(disasm, "DBNZ B,$01000H")
        self.assertEqual(new_pc, pc + len(mem))

    def test_8d_bc_rel(self):
        pc = 0x1000
        mem = [0x8d, 0xfe]
        disasm, new_pc = disassemble(mem, pc)
        self.assertEqual(disasm, 'BC $01000H')
        self.assertEqual(new_pc, pc + len(mem))

    def test_8e_mov_a_addr16(self):
        pc = 0x1000
        for addr16 in (0x0000, 0xabcd, 0xffff):
            low = addr16 & 0xff
            high = (addr16 >> 8) & 0xff
            mem = [0x8e, low, high]
            disasm, new_pc = disassemble(mem, pc)
            self.assertEqual(disasm, 'MOV A,!0%04xH' % addr16)
            self.assertEqual(new_pc, pc + len(mem))

    def test_8f_reti(self):
        pc = 0x1000
        mem = [0x8f]
        disasm, new_pc = disassemble(mem, pc)
        self.assertEqual(disasm, "RETI")
        self.assertEqual(new_pc, pc + len(mem))

    def test_90_92_94_96_decw_regpair(self):
        d = {0x90: "DECW AX", 0x92: "DECW BC",
             0x94: "DECW DE", 0x96: "DECW HL"}

        pc = 0x1000
        for opcode, expected_disasm in d.items():
            mem = [opcode]
            disasm, new_pc = disassemble(mem, pc)
            self.assertEqual(disasm, expected_disasm)
            self.assertEqual(new_pc, pc + len(mem))

    def test_91_dec_saddr(self):
        pc = 0x1000
        for saddr in range(0xfe20, 0xff20):
            saddr_low = saddr & 0xff
            mem = [0x91, saddr_low]
            disasm, new_pc = disassemble(mem, pc)
            self.assertEqual(disasm, "DEC 0%04xH" % saddr)
            self.assertEqual(new_pc, pc + len(mem))

    def test_93_xch_a_sfr(self):
        pc = 0x1000
        for sfr in range(0xff00, 0x10000):
            sfr_low = sfr & 0xff
            mem = [0x93, sfr_low]
            disasm, new_pc = disassemble(mem, pc)
            self.assertEqual(disasm, "XCH A,0%04xH" % sfr)
            self.assertEqual(new_pc, pc + len(mem))

    def test_95_mov_de_a(self):
        pc = 0x1000
        mem = [0x95]
        disasm, new_pc = disassemble(mem, pc)
        self.assertEqual(disasm, "MOV [DE],A")
        self.assertEqual(new_pc, pc + len(mem))

    def test_97_mov_hl_a(self):
        pc = 0x1000
        mem = [0x97]
        disasm, new_pc = disassemble(mem, pc)
        self.assertEqual(disasm, "MOV [HL],A")
        self.assertEqual(new_pc, pc + len(mem))

    def test_98_sub_saddr_imm8(self):
        pc = 0x1000
        for saddr in range(0xfe20, 0xff20):
            saddr_low = saddr & 0xff
            mem = [0x98, saddr_low, 0xab]
            disasm, new_pc = disassemble(mem, pc)
            self.assertEqual(disasm, "SUB 0%04xH,#0abH" % saddr)
            self.assertEqual(new_pc, pc + len(mem))

    def test_9a_call_addr16(self):
        pc = 0x1000
        for addr16 in (0x0000, 0xabcd, 0xffff):
            low = addr16 & 0xff
            high = (addr16 >> 8) & 0xff
            mem = [0x9a, low, high]
            disasm, new_pc = disassemble(mem, pc)
            self.assertEqual(disasm, 'CALL !0%04xH' % addr16)
            self.assertEqual(new_pc, pc + len(mem))

    def test_9b_br_addr16(self):
        pc = 0x1000
        for addr16 in (0x0000, 0xabcd, 0xffff):
            low = addr16 & 0xff
            high = (addr16 >> 8) & 0xff
            mem = [0x9b, low, high]
            disasm, new_pc = disassemble(mem, pc)
            self.assertEqual(disasm, 'BR !0%04xH' % addr16)
            self.assertEqual(new_pc, pc + len(mem))

    def test_9d_bnc_rel(self):
        pc = 0x1000
        mem = [0x9d, 0xfe]
        disasm, new_pc = disassemble(mem, pc)
        self.assertEqual(disasm, "BNC $01000H")
        self.assertEqual(new_pc, pc + len(mem))

    def test_9e_mov_addr16_a(self):
        pc = 0x1000
        for addr16 in (0x0000, 0xabcd, 0xffff):
            low = addr16 & 0xff
            high = (addr16 >> 8) & 0xff
            mem = [0x9e, low, high]
            disasm, new_pc = disassemble(mem, pc)
            self.assertEqual(disasm, 'MOV !0%04xH,A' % addr16)
            self.assertEqual(new_pc, pc + len(mem))

    def test_9f_retb(self):
        pc = 0x1000
        mem = [0x9F]
        disasm, new_pc = disassemble(mem, pc)
        self.assertEqual(disasm, "RETB")
        self.assertEqual(new_pc, pc + len(mem))

    def test_a0_a7_mov_reg_imm8(self):
        d = {0xa0: 'MOV X,#0%02xH', 0xa1: 'MOV A,#0%02xH',
             0xa2: 'MOV C,#0%02xH', 0xa3: 'MOV B,#0%02xH',
             0xa4: 'MOV E,#0%02xH', 0xa5: 'MOV D,#0%02xH',
             0xa6: 'MOV L,#0%02xH', 0xa7: 'MOV H,#0%02xH'}

        pc = 0x1000
        for opcode, expected_disasm_fmt in d.items():
            for imm8 in (0x00, 0xab, 0xff):
                mem = [opcode, imm8]
                disasm, new_pc = disassemble(mem, pc)
                self.assertEqual(disasm, expected_disasm_fmt % imm8)
                self.assertEqual(new_pc, pc + len(mem))

    def test_a8_addc_saddr_imm8(self):
        pc = 0x1000
        for saddr in range(0xfe20, 0xff20):
            saddr_low = saddr & 0xff
            mem = [0xa8, saddr_low, 0xab]
            disasm, new_pc = disassemble(mem, pc)
            self.assertEqual(disasm, "ADDC 0%04xH,#0abH" % saddr)
            self.assertEqual(new_pc, pc + len(mem))

    def test_a9_movw_ax_sfrp(self):
        pc = 0x1000
        for sfrp in range(0xff00, 0x10000, 2):
            sfrp_low = sfrp & 0xff
            mem = [0xa9, sfrp_low]
            disasm, new_pc = disassemble(mem, pc)
            self.assertEqual(disasm, "MOVW AX,0%04xH" % sfrp)
            self.assertEqual(new_pc, pc + len(mem))

    def test_aa_mov_a_hl_plus_c(self):
        pc = 0x1000
        mem = [0xaa]
        disasm, new_pc = disassemble(mem, pc)
        self.assertEqual(disasm, "MOV A,[HL+C]")
        self.assertEqual(new_pc, pc + len(mem))

    def test_ab_mov_a_hl_plus_b(self):
        pc = 0x1000
        mem = [0xab]
        disasm, new_pc = disassemble(mem, pc)
        self.assertEqual(disasm, "MOV A,[HL+B]")
        self.assertEqual(new_pc, pc + len(mem))

    def test_ad_bz_rel(self):
        pc = 0x1000
        mem = [0xad, 0xfe]
        disasm, new_pc = disassemble(mem, pc)
        self.assertEqual(disasm, "BZ $01000H")
        self.assertEqual(new_pc, pc + len(mem))

    def test_ae_mov_a_hl_plus_byte(self):
        pc = 0x1000
        mem = [0xAE, 0xAB]
        disasm, new_pc = disassemble(mem, pc)
        self.assertEqual(disasm, "MOV A,[HL+0abH]")
        self.assertEqual(new_pc, pc + len(mem))

    def test_af_ret(self):
        pc = 0x1000
        mem = [0xAF]
        disasm, new_pc = disassemble(mem, pc)
        self.assertEqual(disasm, "RET")
        self.assertEqual(new_pc, pc + len(mem))

    def test_b0_b2_b4_b6_pop_regpair(self):
        d = {0xB0: "POP AX", 0xB2: "POP BC",
             0xB4: "POP DE", 0xB6: "POP HL"}

        pc = 0x1000
        for opcode, expected_disasm in d.items():
            mem = [opcode]
            disasm, new_pc = disassemble(mem, pc)
            self.assertEqual(disasm, expected_disasm)
            self.assertEqual(new_pc, pc + len(mem))

    def test_b1_b3_b5_b7_push_regpair(self):
        d = {0xB1: "PUSH AX", 0xB3: "PUSH BC",
             0xB5: "PUSH DE", 0xB7: "PUSH HL"}

        pc = 0x1000
        for opcode, expected_disasm in d.items():
            mem = [opcode]
            disasm, new_pc = disassemble(mem, pc)
            self.assertEqual(disasm, expected_disasm)
            self.assertEqual(new_pc, pc + len(mem))

    def test_b8_subc_saddr_imm8(self):
        pc = 0x1000
        for saddr in range(0xfe20, 0xff20):
            saddr_low = saddr & 0xff
            mem = [0xb8, saddr_low, 0xab]
            disasm, new_pc = disassemble(mem, pc)
            self.assertEqual(disasm, "SUBC 0%04xH,#0abH" % saddr)
            self.assertEqual(new_pc, pc + len(mem))

    def test_b9_movw_sfrp_ax(self):
        pc = 0x1000
        for sfrp in range(0xff00, 0x10000, 2):
            sfrp_low = sfrp & 0xff
            mem = [0xb9, sfrp_low]
            disasm, new_pc = disassemble(mem, pc)
            self.assertEqual(disasm, "MOVW 0%04xH,AX" % sfrp)
            self.assertEqual(new_pc, pc + len(mem))

    def test_ba_mov_hl_plus_c_a(self):
        pc = 0x1000
        mem = [0xBA]
        disasm, new_pc = disassemble(mem, pc)
        self.assertEqual(disasm, "MOV [HL+C],A")
        self.assertEqual(new_pc, pc + len(mem))

    def test_bb_mov_hl_plus_b_a(self):
        pc = 0x1000
        mem = [0xBB]
        disasm, new_pc = disassemble(mem, pc)
        self.assertEqual(disasm, "MOV [HL+B],A")
        self.assertEqual(new_pc, pc + len(mem))

    def test_bd_bnz_rel(self):
        pc = 0x1000
        mem = [0xbd, 0xfe]
        disasm, new_pc = disassemble(mem, pc)
        self.assertEqual(disasm, "BNZ $01000H")
        self.assertEqual(new_pc, pc + len(mem))

    def test_be_mov_hl_plus_byte_a(self):
        pc = 0x1000
        mem = [0xBE, 0xAB]
        disasm, new_pc = disassemble(mem, pc)
        self.assertEqual(disasm, "MOV [HL+0abH],A")
        self.assertEqual(new_pc, pc + len(mem))

    def test_bf_brk(self):
        pc = 0x1000
        mem = [0xBF]
        disasm, new_pc = disassemble(mem, pc)
        self.assertEqual(disasm, "BRK")
        self.assertEqual(new_pc, pc + len(mem))

    def test_c2_c4_c6_mov_ax_regpair(self):
        d = {0xC2: "MOVW AX,BC", 0xC4: "MOVW AX,DE", 0xC6: "MOVW AX,HL"}

        pc = 0x1000
        for opcode, expected_disasm in d.items():
            mem = [opcode]
            disasm, new_pc = disassemble(mem, pc)
            self.assertEqual(disasm, expected_disasm)
            self.assertEqual(new_pc, pc + len(mem))

    def test_c8_cmp_saddr_imm8(self):
        pc = 0x1000
        for saddr in range(0xfe20, 0xff20):
            saddr_low = saddr & 0xff
            mem = [0xc8, saddr_low, 0xab]
            disasm, new_pc = disassemble(mem, pc)
            self.assertEqual(disasm, "CMP 0%04xH,#0abH" % saddr)
            self.assertEqual(new_pc, pc + len(mem))

    def test_ca_addw_ax_imm16(self):
        pc = 0x1000
        for imm16 in (0x0000, 0xabcd, 0xffff):
            high = (imm16 >> 8) & 0xff
            low = imm16 & 0xff
            mem = [0xca, low, high]
            disasm, new_pc = disassemble(mem, pc)
            self.assertEqual(disasm, "ADDW AX,#0%04xH" % imm16)
            self.assertEqual(new_pc, pc + len(mem))

    def test_ce_xch_a_addr16(self):
        pc = 0x1000
        for addr16 in (0x0000, 0xabcd, 0xffff):
            low = addr16 & 0xff
            high = (addr16 >> 8) & 0xff
            mem = [0xce, low, high]
            disasm, new_pc = disassemble(mem, pc)
            self.assertEqual(disasm, 'XCH A,!0%04xH' % addr16)
            self.assertEqual(new_pc, pc + len(mem))

    def test_d2_d4_d6_mov_regpair(self):
        d = {0xD2: "MOVW BC,AX", 0xD4: "MOVW DE,AX", 0xD6: "MOVW HL,AX"}

        pc = 0x1000
        for opcode, expected_disasm in d.items():
            mem = [opcode]
            disasm, new_pc = disassemble(mem, pc)
            self.assertEqual(disasm, expected_disasm)
            self.assertEqual(new_pc, pc + len(mem))

    def test_d8_and_saddr_imm8(self):
        pc = 0x1000
        for saddr in range(0xfe20, 0xff20):
            saddr_low = saddr & 0xff
            mem = [0xd8, saddr_low, 0xab]
            disasm, new_pc = disassemble(mem, pc)
            self.assertEqual(disasm, "AND 0%04xH,#0abH" % saddr)
            self.assertEqual(new_pc, pc + len(mem))

    def test_da_subw_ax_imm16(self):
        pc = 0x1000
        for imm16 in (0x0000, 0xabcd, 0xffff):
            high = (imm16 >> 8) & 0xff
            low = imm16 & 0xff
            mem = [0xda, low, high]
            disasm, new_pc = disassemble(mem, pc)
            self.assertEqual(disasm, "SUBW AX,#0%04xH" % imm16)
            self.assertEqual(new_pc, pc + len(mem))

    def test_de_xch_a_hl_plus_byte(self):
        pc = 0x1000
        mem = [0xde, 0xab]
        disasm, new_pc = disassemble(mem, pc)
        self.assertEqual(disasm, "XCH A,[HL+0abH]")
        self.assertEqual(new_pc, pc + len(mem))

    def test_e2_e4_e6_xchw_ax_regpair(self):
        d = {0xE2: "XCHW AX,BC", 0xE4: "XCHW AX,DE", 0xE6: "XCHW AX,HL"}

        pc = 0x1000
        for opcode, expected_disasm in d.items():
            mem = [opcode]
            disasm, new_pc = disassemble(mem, pc)
            self.assertEqual(disasm, expected_disasm)
            self.assertEqual(new_pc, pc + len(mem))

    def test_e8_or_saddr_imm8(self):
        pc = 0x1000
        for saddr in range(0xfe20, 0xff20):
            saddr_low = saddr & 0xff
            mem = [0xe8, saddr_low, 0xab]
            disasm, new_pc = disassemble(mem, pc)
            self.assertEqual(disasm, "OR 0%04xH,#0abH" % saddr)
            self.assertEqual(new_pc, pc + len(mem))

    def test_ea_cmpw_ax_imm16(self):
        pc = 0x1000
        for imm16 in (0x0000, 0xabcd, 0xffff):
            high = (imm16 >> 8) & 0xff
            low = imm16 & 0xff
            mem = [0xea, low, high]
            disasm, new_pc = disassemble(mem, pc)
            self.assertEqual(disasm, "CMPW AX,#0%04xH" % imm16)
            self.assertEqual(new_pc, pc + len(mem))

    def test_f4_mov_a_sfr(self):
        pc = 0x1000
        for sfr in range(0xff00, 0x10000):
            sfr_low = sfr & 0xff
            mem = [0xf4, sfr_low]
            disasm, new_pc = disassemble(mem, pc)
            self.assertEqual(disasm, "MOV A,0%04xH" % sfr)
            self.assertEqual(new_pc, pc + len(mem))

    def test_f6_mov_sfr_a(self):
        pc = 0x1000
        for sfr in range(0xff00, 0x10000):
            sfr_low = sfr & 0xff
            mem = [0xf6, sfr_low]
            disasm, new_pc = disassemble(mem, pc)
            self.assertEqual(disasm, "MOV 0%04xH,A" % sfr)
            self.assertEqual(new_pc, pc + len(mem))

    def test_f8_xor_saddr_imm8(self):
        pc = 0x1000
        for saddr in range(0xfe20, 0xff20):
            saddr_low = saddr & 0xff
            mem = [0xf8, saddr_low, 0xab]
            disasm, new_pc = disassemble(mem, pc)
            self.assertEqual(disasm, "XOR 0%04xH,#0abH" % saddr)
            self.assertEqual(new_pc, pc + len(mem))

    def test_fe_movw_sfrp_imm16(self):
        pc = 0x1000
        for sfrp in range(0xff00, 0x10000, 2):
            sfrp_low = sfrp & 0xff
            mem = [0xfe, sfrp_low, 0xcd, 0xab]
            disasm, new_pc = disassemble(mem, pc)
            self.assertEqual(disasm, "MOVW 0%04xH,#0abcdH" % sfrp)
            self.assertEqual(new_pc, pc + len(mem))

    def test_fa_br_rel(self):
        pc = 0x1000
        mem = [0xfa, 0xfe]
        disasm, new_pc = disassemble(mem, pc)
        self.assertEqual(disasm, "BR $01000H")
        self.assertEqual(new_pc, pc + len(mem))

    #
    # Instructions that require multiple bytes to recognize
    #

    def test_set1_psw(self):
        opcodes = (0x0a, 0x1a, 0x2a, 0x3a, 0x4a, 0x5a, 0x6a)
        pc = 0x1000
        for bit, opcode in enumerate(opcodes):
            mem = [opcode, 0x1e]
            disasm, new_pc = disassemble(mem, pc)
            self.assertEqual(disasm, "SET1 PSW.%d" % bit)
            self.assertEqual(new_pc, pc + len(mem))

    def test_11_1e_mov_psw_imm8(self):
        pc = 0x1000
        mem = [0x11, 0x1e, 0xab]
        disasm, new_pc = disassemble(mem, pc)
        self.assertEqual(disasm, "MOV PSW,#0abH")
        self.assertEqual(new_pc, pc + len(mem))

    def test_11_xx_mov_saddr_imm8(self):
        pc = 0x1000
        for saddr in range(0xfe20, 0xff20):
            if saddr == 0xff1e:
                continue # special case; would disassemble as MOV PSW,#imm8
            saddr_low = saddr & 0xff
            mem = [0x11, saddr_low, 0xab]
            disasm, new_pc = disassemble(mem, pc)
            self.assertEqual(disasm, "MOV 0%04xH,#0abH" % (saddr))
            self.assertEqual(new_pc, pc + len(mem))

    def test_31_01_thru_71_btclr_saddr(self):
        opcodes = (0x01, 0x11, 0x21, 0x31, 0x41, 0x51, 0x61, 0x71)
        pc = 0x1000
        for bit, opcode in enumerate(opcodes):
            for saddr in range(0xfe20, 0xff20):
                if saddr == 0xff1e:
                    continue # special case; would disassemble as BTCLR PSW.x,$rel
                saddr_low = saddr & 0xff
                mem = [0x31, opcode, saddr_low, 0xfc]
                disasm, new_pc = disassemble(mem, pc)
                self.assertEqual(disasm, "BTCLR 0%04xH.%d,$01000H" % (saddr, bit))
                self.assertEqual(new_pc, pc + len(mem))

    def test_31_01_thru_71_btclr_psw(self):
        opcodes = (0x01, 0x11, 0x21, 0x31, 0x41, 0x51, 0x61, 0x71)
        pc = 0x1000
        for bit, opcode in enumerate(opcodes):
            mem = [0x31, opcode, 0x1e, 0xfc]
            disasm, new_pc = disassemble(mem, pc)
            self.assertEqual(disasm, "BTCLR PSW.%d,$01000H" % bit)
            self.assertEqual(new_pc, pc + len(mem))

    def test_31_03_thru_73_bf_saddr(self):
        opcodes = (0x03, 0x13, 0x23, 0x33, 0x43, 0x53, 0x63, 0x73)
        pc = 0x1000
        for bit, opcode in enumerate(opcodes):
            for saddr in range(0xfe20, 0xff20):
                if saddr == 0xff1e:
                    continue # special case; would disassemble as BF PSW.x,$rel
                saddr_low = saddr & 0xff
                mem = [0x31, opcode, saddr_low, 0xfc]
                disasm, new_pc = disassemble(mem, pc)
                self.assertEqual(disasm, "BF 0%04xH.%d,$01000H" % (saddr, bit))
                self.assertEqual(new_pc, pc + len(mem))

    def test_31_03_thru_73_bf_psw(self):
        opcodes = (0x03, 0x13, 0x23, 0x33, 0x43, 0x53, 0x63, 0x73)
        pc = 0x1000
        for bit, opcode in enumerate(opcodes):
            mem = [0x31, opcode, 0x1e, 0xfc]
            disasm, new_pc = disassemble(mem, pc)
            self.assertEqual(disasm, "BF PSW.%d,$01000H" % bit)
            self.assertEqual(new_pc, pc + len(mem))

    def test_31_05_thru_75_btclr_sfr(self):
        opcodes = (0x05, 0x15, 0x25, 0x35, 0x45, 0x55, 0x65, 0x75)
        pc = 0x1000
        for bit, opcode in enumerate(opcodes):
            for sfr in range(0xff00, 0x10000):
                sfr_low = sfr & 0xff
                mem = [0x31, opcode, sfr_low, 0xfc]
                disasm, new_pc = disassemble(mem, pc)
                self.assertEqual(disasm, "BTCLR 0%04xH.%d,$01000H" % (sfr, bit))
                self.assertEqual(new_pc, pc + len(mem))

    def test_31_06_thru_76_bt_sfr(self):
        opcodes = (0x06, 0x16, 0x26, 0x36, 0x46, 0x56, 0x66, 0x76)
        pc = 0x1000
        for bit, opcode in enumerate(opcodes):
            for sfr in range(0xff00, 0x10000):
                sfr_low = sfr & 0xff
                mem = [0x31, opcode, sfr_low, 0xfc]
                disasm, new_pc = disassemble(mem, pc)
                self.assertEqual(disasm, "BT 0%04xH.%d,$01000H" % (sfr, bit))
                self.assertEqual(new_pc, pc + len(mem))

    def test_31_07_thru_77_bf_sfr(self):
        opcodes = (0x07, 0x17, 0x27, 0x37, 0x47, 0x57, 0x67, 0x77)
        pc = 0x1000
        for bit, opcode in enumerate(opcodes):
            for sfr in range(0xff00, 0x10000):
                sfr_low = sfr & 0xff
                mem = [0x31, opcode, sfr_low, 0xfc]
                disasm, new_pc = disassemble(mem, pc)
                self.assertEqual(disasm, "BF 0%04xH.%d,$01000H" % (sfr, bit))
                self.assertEqual(new_pc, pc + len(mem))

    def test_31_0a_add_a_hl_plus_c(self):
        pc = 0x1000
        mem = [0x31, 0x0a]
        disasm, new_pc = disassemble(mem, pc)
        self.assertEqual(disasm, "ADD A,[HL+C]")
        self.assertEqual(new_pc, pc + len(mem))

    def test_31_0b_add_a_hl_plus_b(self):
        pc = 0x1000
        mem = [0x31, 0x0b]
        disasm, new_pc = disassemble(mem, pc)
        self.assertEqual(disasm, "ADD A,[HL+B]")
        self.assertEqual(new_pc, pc + len(mem))

    def test_31_0d_thru_7d_btclr(self):
        opcodes = (0x0d, 0x1d, 0x2d, 0x3d, 0x4d, 0x5d, 0x6d, 0x7d)
        pc = 0x1000
        for bit, opcode in enumerate(opcodes):
            mem = [0x31, opcode, 0xfd]
            disasm, new_pc = disassemble(mem, pc)
            self.assertEqual(disasm, "BTCLR A.%d,$01000H" % bit)
            self.assertEqual(new_pc, pc + len(mem))

    def test_31_85_thru_f5_btclr_hl(self):
        opcodes = (0x85, 0x95, 0xa5, 0xb5, 0xc5, 0xd5, 0xe5, 0xf5)
        pc = 0x1000
        for bit, opcode in enumerate(opcodes):
            mem = [0x31, opcode, 0xfd]
            disasm, new_pc = disassemble(mem, pc)
            self.assertEqual(disasm, "BTCLR [HL].%d,$01000H" % bit)
            self.assertEqual(new_pc, pc + len(mem))

    def test_31_86_thru_f6_bt_hl(self):
        opcodes = (0x86, 0x96, 0xa6, 0xb6, 0xc6, 0xd6, 0xe6, 0xf6)
        pc = 0x1000
        for bit, opcode in enumerate(opcodes):
            mem = [0x31, opcode, 0xfd]
            disasm, new_pc = disassemble(mem, pc)
            self.assertEqual(disasm, "BT [HL].%d,$01000H" % bit)
            self.assertEqual(new_pc, pc + len(mem))

    def test_31_87_thru_f7_bf_hl(self):
        opcodes = (0x87, 0x97, 0xa7, 0xb7, 0xc7, 0xd7, 0xe7, 0xf7)
        pc = 0x1000
        for bit, opcode in enumerate(opcodes):
            mem = [0x31, opcode, 0xfd]
            disasm, new_pc = disassemble(mem, pc)
            self.assertEqual(disasm, "BF [HL].%d,$01000H" % bit)
            self.assertEqual(new_pc, pc + len(mem))

    def test_31_0e_thru_7e_bt(self):
        opcodes = (0x0e, 0x1e, 0x2e, 0x3e, 0x4e, 0x5e, 0x6e, 0x7e)
        pc = 0x1000
        for bit, opcode in enumerate(opcodes):
            mem = [0x31, opcode, 0xfd]
            disasm, new_pc = disassemble(mem, pc)
            self.assertEqual(disasm, "BT A.%d,$01000H" % bit)
            self.assertEqual(new_pc, pc + len(mem))

    def test_31_0f_thru_7f_bt(self):
        opcodes = (0x0f, 0x1f, 0x2f, 0x3f, 0x4f, 0x5f, 0x6f, 0x7f)
        pc = 0x1000
        for bit, opcode in enumerate(opcodes):
            mem = [0x31, opcode, 0xfd]
            disasm, new_pc = disassemble(mem, pc)
            self.assertEqual(disasm, "BF A.%d,$01000H" % bit)
            self.assertEqual(new_pc, pc + len(mem))

    def test_31_1a_sub_a_hl_plus_c(self):
        pc = 0x1000
        mem = [0x31, 0x1a]
        disasm, new_pc = disassemble(mem, pc)
        self.assertEqual(disasm, "SUB A,[HL+C]")
        self.assertEqual(new_pc, pc + len(mem))

    def test_31_1b_sub_a_hl_plus_b(self):
        pc = 0x1000
        mem = [0x31, 0x1b]
        disasm, new_pc = disassemble(mem, pc)
        self.assertEqual(disasm, "SUB A,[HL+B]")
        self.assertEqual(new_pc, pc + len(mem))

    def test_31_2a_addc_a_hl_plus_c(self):
        pc = 0x1000
        mem = [0x31, 0x2a]
        disasm, new_pc = disassemble(mem, pc)
        self.assertEqual(disasm, "ADDC A,[HL+C]")
        self.assertEqual(new_pc, pc + len(mem))

    def test_31_2b_addc_a_hl_plus_b(self):
        pc = 0x1000
        mem = [0x31, 0x2b]
        disasm, new_pc = disassemble(mem, pc)
        self.assertEqual(disasm, "ADDC A,[HL+B]")
        self.assertEqual(new_pc, pc + len(mem))

    def test_31_3a_subc_a_hl_plus_c(self):
        pc = 0x1000
        mem = [0x31, 0x3a]
        disasm, new_pc = disassemble(mem, pc)
        self.assertEqual(disasm, "SUBC A,[HL+C]")
        self.assertEqual(new_pc, pc + len(mem))

    def test_31_3b_subc_a_hl_plus_b(self):
        pc = 0x1000
        mem = [0x31, 0x3b]
        disasm, new_pc = disassemble(mem, pc)
        self.assertEqual(disasm, "SUBC A,[HL+B]")
        self.assertEqual(new_pc, pc + len(mem))

    def test_31_4a_cmp_a_hl_plus_c(self):
        pc = 0x1000
        mem = [0x31, 0x4a]
        disasm, new_pc = disassemble(mem, pc)
        self.assertEqual(disasm, "CMP A,[HL+C]")
        self.assertEqual(new_pc, pc + len(mem))

    def test_31_4b_cmp_a_hl_plus_b(self):
        pc = 0x1000
        mem = [0x31, 0x4b]
        disasm, new_pc = disassemble(mem, pc)
        self.assertEqual(disasm, "CMP A,[HL+B]")
        self.assertEqual(new_pc, pc + len(mem))

    def test_31_5a_and_a_hl_plus_a(self):
        pc = 0x1000
        mem = [0x31, 0x5a]
        disasm, new_pc = disassemble(mem, pc)
        self.assertEqual(disasm, "AND A,[HL+C]")
        self.assertEqual(new_pc, pc + len(mem))

    def test_31_5b_and_a_hl_plus_b(self):
        pc = 0x1000
        mem = [0x31, 0x5b]
        disasm, new_pc = disassemble(mem, pc)
        self.assertEqual(disasm, "AND A,[HL+B]")
        self.assertEqual(new_pc, pc + len(mem))

    def test_31_6a_or_a_hl_plus_c(self):
        pc = 0x1000
        mem = [0x31, 0x6a]
        disasm, new_pc = disassemble(mem, pc)
        self.assertEqual(disasm, "OR A,[HL+C]")
        self.assertEqual(new_pc, pc + len(mem))

    def test_31_6b_or_a_hl_plus_b(self):
        pc = 0x1000
        mem = [0x31, 0x6b]
        disasm, new_pc = disassemble(mem, pc)
        self.assertEqual(disasm, "OR A,[HL+B]")
        self.assertEqual(new_pc, pc + len(mem))

    def test_31_7a_xor_a_hl_plus_c(self):
        pc = 0x1000
        mem = [0x31, 0x7a]
        disasm, new_pc = disassemble(mem, pc)
        self.assertEqual(disasm, "XOR A,[HL+C]")
        self.assertEqual(new_pc, pc + len(mem))

    def test_31_7b_xor_a_hl_plus_b(self):
        pc = 0x1000
        mem = [0x31, 0x7b]
        disasm, new_pc = disassemble(mem, pc)
        self.assertEqual(disasm, "XOR A,[HL+B]")
        self.assertEqual(new_pc, pc + len(mem))

    def test_31_8a_xch_a_hl_plus_c(self):
        pc = 0x1000
        mem = [0x31, 0x8a]
        disasm, new_pc = disassemble(mem, pc)
        self.assertEqual(disasm, "XCH A,[HL+C]")
        self.assertEqual(new_pc, pc + len(mem))

    def test_31_8b_xch_a_hl_plus_b(self):
        pc = 0x1000
        mem = [0x31, 0x8b]
        disasm, new_pc = disassemble(mem, pc)
        self.assertEqual(disasm, "XCH A,[HL+B]")
        self.assertEqual(new_pc, pc + len(mem))

    def test_31_80_ror4_hl(self):
        pc = 0x1000
        mem = [0x31, 0x80]
        disasm, new_pc = disassemble(mem, pc)
        self.assertEqual(disasm, "ROL4 [HL]")
        self.assertEqual(new_pc, pc + len(mem))

    def test_31_82_mulu_x(self):
        pc = 0x1000
        mem = [0x31, 0x82]
        disasm, new_pc = disassemble(mem, pc)
        self.assertEqual(disasm, "DIVUW C")
        self.assertEqual(new_pc, pc + len(mem))

    def test_31_88_mulu_x(self):
        pc = 0x1000
        mem = [0x31, 0x88]
        disasm, new_pc = disassemble(mem, pc)
        self.assertEqual(disasm, "MULU X")
        self.assertEqual(new_pc, pc + len(mem))

    def test_31_90_ror4_hl(self):
        pc = 0x1000
        mem = [0x31, 0x90]
        disasm, new_pc = disassemble(mem, pc)
        self.assertEqual(disasm, "ROR4 [HL]")
        self.assertEqual(new_pc, pc + len(mem))

    def test_31_98_ror4_hl(self):
        pc = 0x1000
        mem = [0x31, 0x98]
        disasm, new_pc = disassemble(mem, pc)
        self.assertEqual(disasm, "BR AX")
        self.assertEqual(new_pc, pc + len(mem))

    def test_7a_ei_alias_for_set1_psw_bit_7(self):
        pc = 0x1000
        mem = [0x7a, 0x1e]
        disasm, new_pc = disassemble(mem, pc)
        self.assertEqual(disasm, "EI")
        self.assertEqual(new_pc, pc + len(mem))

    def test_set1_saddr(self):
        opcodes = (0x0a, 0x1a, 0x2a, 0x3a, 0x4a, 0x5a, 0x6a, 0x7a)
        pc = 0x1000
        for bit, opcode in enumerate(opcodes):
            for saddr in range(0xfe20, 0xff20):
                if saddr == 0xff1e:
                    continue # special case; would disassemble as SET1 PSW.x
                saddr_low = saddr & 0xff
                mem = [opcode, saddr_low]
                disasm, new_pc = disassemble(mem, pc)
                self.assertEqual(disasm, "SET1 0%04xH.%d" % (saddr, bit))
                self.assertEqual(new_pc, pc + len(mem))

    def test_clr1_psw(self):
        opcodes = (0x0b, 0x1b, 0x2b, 0x3b, 0x4b, 0x5b, 0x6b)
        pc = 0x1000
        for bit, opcode in enumerate(opcodes):
            mem = [opcode, 0x1e]
            disasm, new_pc = disassemble(mem, pc)
            self.assertEqual(disasm, "CLR1 PSW.%d" % bit)
            self.assertEqual(new_pc, pc + len(mem))

    def test_7b_di_alias_for_set1_psw_bit_7(self):
        pc = 0x1000
        mem = [0x7b, 0x1e]
        disasm, new_pc = disassemble(mem, pc)
        self.assertEqual(disasm, "DI")
        self.assertEqual(new_pc, pc + len(mem))

    def test_clr1_saddr(self):
        opcodes = (0x0b, 0x1b, 0x2b, 0x3b, 0x4b, 0x5b, 0x6b, 0x7b)
        pc = 0x1000
        for bit, opcode in enumerate(opcodes):
            for saddr in range(0xfe20, 0xff20):
                if saddr == 0xff1e:
                    continue # special case; would disassemble as CLR1 PSW.x
                saddr_low = saddr & 0xff
                mem = [opcode, saddr_low]
                disasm, new_pc = disassemble(mem, pc)
                self.assertEqual(disasm, "CLR1 0%04xH.%d" % (saddr, bit))
                self.assertEqual(new_pc, pc + len(mem))

    def test_89_1c_movw_ax_sp(self):
        pc = 0x1000
        mem = [0x89, 0x1c]
        disasm, new_pc = disassemble(mem, pc)
        self.assertEqual(disasm, "MOVW AX,SP")
        self.assertEqual(new_pc, pc + len(mem))

    def test_89_xx_movw_ax_saddrp(self):
        pc = 0x1000
        for saddrp in range(0xfe20, 0xff20, 2):
            if saddrp == 0xff1c:
                continue # special case; would disassemble as MOVW AX,SP
            saddrp_low = saddrp & 0xff
            mem = [0x89, saddrp_low]
            disasm, new_pc = disassemble(mem, pc)
            self.assertEqual(disasm, "MOVW AX,0%04xH" % saddrp)
            self.assertEqual(new_pc, pc + len(mem))

    def test_bt_psw_bit_rel(self):
        opcodes = (0x8c, 0x9c, 0xac, 0xbc, 0xcc, 0xdc, 0xec, 0xfc)
        pc = 0x1000
        for bit, opcode in enumerate(opcodes):
            mem = [opcode, 0x1e, 0xfd]
            disasm, new_pc = disassemble(mem, pc)
            self.assertEqual(disasm, "BT PSW.%d,$01000H" % bit)
            self.assertEqual(new_pc, pc + len(mem))

    def test_bt_saddr_bit_rel(self):
        opcodes = (0x8c, 0x9c, 0xac, 0xbc, 0xcc, 0xdc, 0xec, 0xfc)
        pc = 0x1000
        for bit, opcode in enumerate(opcodes):
            for saddr in range(0xfe20, 0xff20):
                if saddr == 0xff1e:
                    continue # special case; would disassemble as BT PSW.bit,rel
                saddr_low = saddr & 0xff
                mem = [opcode, saddr_low, 0xfd]
                disasm, new_pc = disassemble(mem, pc)
                self.assertEqual(disasm, "BT 0%04xH.%d,$01000H" % (saddr, bit))

    def test_99_1c_movw_sp_ax(self):
        pc = 0x1000
        mem = [0x99, 0x1c]
        disasm, new_pc = disassemble(mem, pc)
        self.assertEqual(disasm, "MOVW SP,AX")
        self.assertEqual(new_pc, pc + len(mem))

    def test_99_xx_movw_saddrp_ax(self):
        pc = 0x1000
        for saddrp in range(0xfe20, 0xff20):
            if saddrp == 0xff1c:
                continue # special case; would disassemble as MOVW AX,SP
            saddrp_low = saddrp & 0xff
            mem = [0x99, saddrp_low]
            disasm, new_pc = disassemble(mem, pc)
            self.assertEqual(disasm, "MOVW 0%04xH,AX" % saddrp)
            self.assertEqual(new_pc, pc + len(mem))

    def test_ee_1c_movw_sp_imm16(self):
        pc = 0x1000
        mem = [0xee, 0x1c, 0xcd, 0xab]
        disasm, new_pc = disassemble(mem, pc)
        self.assertEqual(disasm, "MOVW SP,#0abcdH")
        self.assertEqual(new_pc, pc + len(mem))

    def test_ee_xx_movw_saddrp_imm16(self):
        pc = 0x1000
        for saddrp in range(0xfe20, 0xff20):
            if saddrp == 0xff1c:
                continue # special case; would disassemble as MOVW SP,#imm16
            saddrp_low = saddrp & 0xff
            mem = [0xee, saddrp_low, 0xcd, 0xab]
            disasm, new_pc = disassemble(mem, pc)
            self.assertEqual(disasm, "MOVW 0%04xH,#0abcdH" % saddrp)
            self.assertEqual(new_pc, pc + len(mem))

    def test_f0_e1_mov_a_psw(self):
        pc = 0x1000
        mem = [0xf0, 0x1e]
        disasm, new_pc = disassemble(mem, pc)
        self.assertEqual(disasm, "MOV A,PSW")
        self.assertEqual(new_pc, pc + len(mem))

    def test_f0_xx_mov_a_saddr(self):
        pc = 0x1000
        for saddr in range(0xfe20, 0xff20):
            if saddr == 0xff1e:
                continue # special case; would disassemble as MOV A,PSW
            saddr_low = saddr & 0xff
            mem = [0xf0, saddr_low]
            disasm, new_pc = disassemble(mem, pc)
            self.assertEqual(disasm, "MOV A,0%04xH" % saddr)
            self.assertEqual(new_pc, pc + len(mem))

    def test_f2_e1_mov_psw_a(self):
        pc = 0x1000
        mem = [0xf2, 0x1e]
        disasm, new_pc = disassemble(mem, pc)
        self.assertEqual(disasm, "MOV PSW,A")
        self.assertEqual(new_pc, pc + len(mem))

    def test_f2_xx_mov_a_saddr(self):
        pc = 0x1000
        for saddr in range(0xfe20, 0xff20):
            if saddr == 0xff1e:
                continue # special case; would disassemble as MOV PSW,A
            saddr_low = saddr & 0xff
            mem = [0xf2, saddr_low]
            disasm, new_pc = disassemble(mem, pc)
            self.assertEqual(disasm, "MOV 0%04xH,A" % saddr)
            self.assertEqual(new_pc, pc + len(mem))

    def test_illegals(self):
        for opcode in (0x06, 0x15, 0x17, 0xc0, 0xd0, 0xe0):
            pc = 0x1000
            mem = [opcode]
            disasm, new_pc = disassemble(mem, pc)
            self.assertEqual(disasm, "ILLEGAL 0x%02x" % opcode)
            self.assertEqual(new_pc, pc + len(mem))


def test_suite():
    return unittest.findTestCases(sys.modules[__name__])

if __name__ == '__main__':
    unittest.main(defaultTest='test_suite')
