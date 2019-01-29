import sys
import unittest

from k0dasm.disassemble import disassemble, FlowTypes, IllegalInstructionError


class disassemble_tests(unittest.TestCase):
    def test_00_nop(self):
        mem = [0x00]
        inst = disassemble(mem, pc=0)
        self.assertEqual(str(inst), "nop")
        self.assertEqual(len(inst), len(mem))
        self.assertEqual(inst.flow_type, FlowTypes.Continue)

    def test_01_not1_cy1(self):
        mem = [0x01]
        inst = disassemble(mem, pc=0)
        self.assertEqual(str(inst), "not1 cy")
        self.assertEqual(len(inst), len(mem))
        self.assertEqual(inst.flow_type, FlowTypes.Continue)

    def test_02_movw_ax_addr16p(self):
        mem = [0x02, 0xce, 0xab]
        inst = disassemble(mem, pc=0)
        self.assertEqual(str(inst), "movw ax,!0xabce")
        self.assertEqual(len(inst), len(mem))
        self.assertEqual(inst.flow_type, FlowTypes.Continue)

    def test_02_movw_ax_addr16p_raises_for_odd_address(self):
        mem = [0x02, 0xcd, 0xab]
        with self.assertRaises(IllegalInstructionError):
            disassemble(mem, pc=0)

    def test_02_movw_ax_saddrp_raises_for_out_of_range_address(self):
        mem = [0x02, 0x19, 0xfe]
        with self.assertRaises(IllegalInstructionError):
            disassemble(mem, pc=0)

    def test_03_movw_addr16p_ax(self):
        mem = [0x03, 0xce, 0xab]
        inst = disassemble(mem, pc=0)
        self.assertEqual(str(inst), "movw !0xabce,ax")
        self.assertEqual(len(inst), len(mem))
        self.assertEqual(inst.flow_type, FlowTypes.Continue)

    def test_03_movw_saddrp_ax_raises_for_odd_address(self):
        mem = [0x03, 0xcd, 0xab]
        with self.assertRaises(IllegalInstructionError):
            disassemble(mem, pc=0)

    def test_03_movw_saddrp_ax_raises_for_out_of_range_address(self):
        mem = [0x03, 0x19, 0xfe]
        with self.assertRaises(IllegalInstructionError):
            disassemble(mem, pc=0)

    def test_04_dbnz_saddr_disp(self):
        for saddr in range(0xfe20, 0xff20):
            saddr_low = saddr & 0xff
            mem = bytearray(0x2000)
            code = [0x04, saddr_low, 0xFD]
            for address, c in enumerate(code, 0x1000):
                mem[address] = c
            inst = disassemble(mem, pc=0x1000)
            self.assertEqual(str(inst), "dbnz 0x%04x,0x1000" % saddr)
            self.assertEqual(len(inst), len(code))
            self.assertEqual(inst.flow_type, FlowTypes.ConditionalJump)

    def test_05_xch_a_de(self):
        mem = [0x05]
        inst = disassemble(mem, pc=0)
        self.assertEqual(str(inst), "xch a,[de]")
        self.assertEqual(len(inst), len(mem))
        self.assertEqual(inst.flow_type, FlowTypes.Continue)

    def test_07_xch_a_hl(self):
        mem = [0x07]
        inst = disassemble(mem, pc=0)
        self.assertEqual(str(inst), "xch a,[hl]")
        self.assertEqual(len(inst), len(mem))
        self.assertEqual(inst.flow_type, FlowTypes.Continue)

    def test_08_add_a_addr16(self):
        for addr16 in (0x0000, 0xabcd, 0xffff):
            low = addr16 & 0xff
            high = (addr16 >> 8) & 0xff
            mem = [0x08, low, high]
            inst = disassemble(mem, pc=0)
            self.assertEqual(str(inst), "add a,!0x%04x" % addr16)
            self.assertEqual(len(inst), len(mem))
            self.assertEqual(inst.flow_type, FlowTypes.Continue)

    def test_09_add_a_hl_plus_byte(self):
        for byte in (0x00, 0xab, 0xff):
            mem = [0x09, byte]
            inst = disassemble(mem, pc=0)
            self.assertEqual(str(inst), "add a,[hl+0x%02x]" % byte)
            self.assertEqual(len(inst), len(mem))
            self.assertEqual(inst.flow_type, FlowTypes.Continue)

    def test_callf(self):
        d = {0x0C: 0x0800, 0x1C: 0x0900, 0x2C: 0x0A00, 0x3C: 0x0B00,
             0x4C: 0x0C00, 0x5C: 0x0D00, 0x6C: 0x0E00, 0x7C: 0x0F00}

        for opcode, base in d.items():
            for offset in (0x00, 0xab, 0xff):
                mem = [opcode, offset]
                inst = disassemble(mem, pc=0)
                address = base + offset
                self.assertEqual(str(inst), "callf !0x%04x" % address)
                self.assertEqual(len(inst), len(mem))
                self.assertEqual(inst.flow_type, FlowTypes.SubroutineCall)

    def test_callt(self):
        vectors_by_opcode = {0xC1: 0x0040, 0xC3: 0x0042, 0xC5: 0x0044, 0xC7: 0x0046,
                             0xC9: 0x0048, 0xCB: 0x004a, 0xCD: 0x004c, 0xCF: 0x004e,
                             0xD1: 0x0050, 0xD3: 0x0052, 0xD5: 0x0054, 0xD7: 0x0056,
                             0xD9: 0x0058, 0xDB: 0x005A, 0xDD: 0x005C, 0xDF: 0x005e,
                             0xE1: 0x0060, 0xE3: 0x0062, 0xE5: 0x0064, 0xE7: 0x0066,
                             0xE9: 0x0068, 0xEB: 0x006a, 0xED: 0x006c, 0xEF: 0x006e,
                             0xF1: 0x0070, 0xF3: 0x0072, 0xF5: 0x0074, 0xF7: 0x0076,
                             0xF9: 0x0078, 0xFB: 0x007a, 0xFD: 0x007c, 0xFF: 0x007e,
                            }

        for opcode, vector in vectors_by_opcode.items():
            mem = bytearray(0xF000)
            mem[0x1000] = opcode

            target = (vector << 8) + opcode  # unique address to store in callt vector
            mem[vector] = target & 0xFF
            mem[vector+1] = target >> 8

            inst = disassemble(mem, pc=0x1000)
            self.assertEqual(str(inst), "callt [0x%04x]" % vector)
            self.assertEqual(len(inst), 1)
            self.assertEqual(inst.flow_type, FlowTypes.SubroutineCall)
            self.assertEqual(inst.addr5target, target)

    def test_0d_add_a_imm(self):
        for byte in (0, 0xab, 0xff):
            mem = [0x0d, byte]
            inst = disassemble(mem, pc=0)
            self.assertEqual(str(inst), 'add a,#0x%02x' % byte)
            self.assertEqual(len(inst), len(mem))
            self.assertEqual(inst.flow_type, FlowTypes.Continue)

    def test_0e_addr_a_saddr(self):
        for saddr in range(0xfe20, 0xff20):
            saddr_low = saddr & 0xff
            mem = [0x0e, saddr_low]
            inst = disassemble(mem, pc=0)
            self.assertEqual(str(inst), 'add a,0x%04x' % saddr)
            self.assertEqual(len(inst), len(mem))
            self.assertEqual(inst.flow_type, FlowTypes.Continue)

    def test_0f_add_a_hl(self):
        mem = [0x0f]
        inst = disassemble(mem, pc=0)
        self.assertEqual(str(inst), 'add a,[hl]')
        self.assertEqual(len(inst), len(mem))
        self.assertEqual(inst.flow_type, FlowTypes.Continue)

    def test_10_12_14_16_movw_regpair_imm16(self):
        d = {0x10: "ax", 0x12: "bc", 0x14: "de", 0x16: "hl"}

        for opcode, regpairname in d.items():
            for imm16 in (0x0000, 0xabcd, 0xffff):
                low = imm16 & 0xff
                high = (imm16 >> 8) & 0xff
                mem = [opcode, low, high]
                inst = disassemble(mem, pc=0)
                self.assertEqual(str(inst), 'movw %s,#0x%04x' % (regpairname, imm16))
                self.assertEqual(len(inst), len(mem))
                self.assertEqual(inst.flow_type, FlowTypes.Continue)

    def test_13_mov_sfr_imm8(self):
        for sfr in range(0xff00, 0x10000):
            sfr_low = sfr & 0xff
            mem = [0x13, sfr_low, 0xab]
            inst = disassemble(mem, pc=0)
            self.assertEqual(str(inst), "mov 0x%04x,#0xab" % sfr)
            self.assertEqual(len(inst), len(mem))
            self.assertEqual(inst.flow_type, FlowTypes.Continue)

    def test_18_sub_a_addr16(self):
        for addr16 in (0x0000, 0xabcd, 0xffff):
            low = addr16 & 0xff
            high = (addr16 >> 8) & 0xff
            mem = [0x18, low, high]
            inst = disassemble(mem, pc=0)
            self.assertEqual(str(inst), 'sub a,!0x%04x' % addr16)
            self.assertEqual(len(inst), len(mem))
            self.assertEqual(inst.flow_type, FlowTypes.Continue)

    def test_19_sub_a_hl_plus_offset(self):
        mem = [0x19, 0xab]
        inst = disassemble(mem, pc=0)
        self.assertEqual(str(inst), 'sub a,[hl+0xab]')
        self.assertEqual(len(inst), len(mem))
        self.assertEqual(inst.flow_type, FlowTypes.Continue)

    def test_1d_sub_a_imm8(self):
        mem = [0x1d, 0xab]
        inst = disassemble(mem, pc=0)
        self.assertEqual(str(inst), 'sub a,#0xab')
        self.assertEqual(len(inst), len(mem))
        self.assertEqual(inst.flow_type, FlowTypes.Continue)

    def test_1e_sub_a_saddr(self):
        for saddr in range(0xfe20, 0xff20):
            saddr_low = saddr & 0xff
            mem = [0x1e, saddr_low]
            inst = disassemble(mem, pc=0)
            self.assertEqual(str(inst), 'sub a,0x%04x' % saddr)
            self.assertEqual(len(inst), len(mem))
            self.assertEqual(inst.flow_type, FlowTypes.Continue)

    def test_1f_sub_a_hl(self):
        mem = [0x1f]
        inst = disassemble(mem, pc=0)
        self.assertEqual(str(inst), "sub a,[hl]")
        self.assertEqual(len(inst), len(mem))
        self.assertEqual(inst.flow_type, FlowTypes.Continue)

    def test_20_set1_cy(self):
        mem = [0x20]
        inst = disassemble(mem, pc=0)
        self.assertEqual(str(inst), "set1 cy")
        self.assertEqual(len(inst), len(mem))
        self.assertEqual(inst.flow_type, FlowTypes.Continue)

    def test_21_clr1_cy(self):
        mem = [0x21]
        inst = disassemble(mem, pc=0)
        self.assertEqual(str(inst), "clr1 cy")
        self.assertEqual(len(inst), len(mem))
        self.assertEqual(inst.flow_type, FlowTypes.Continue)

    def test_22_push_psw(self):
        mem = [0x22]
        inst = disassemble(mem, pc=0)
        self.assertEqual(str(inst), "push psw")
        self.assertEqual(len(inst), len(mem))
        self.assertEqual(inst.flow_type, FlowTypes.Continue)

    def test_23_pop_psw(self):
        mem = [0x23]
        inst = disassemble(mem, pc=0)
        self.assertEqual(str(inst), "pop psw")
        self.assertEqual(len(inst), len(mem))
        self.assertEqual(inst.flow_type, FlowTypes.Continue)

    def test_24_ror_a(self):
        mem = [0x24]
        inst = disassemble(mem, pc=0)
        self.assertEqual(str(inst), "ror a,1")
        self.assertEqual(len(inst), len(mem))
        self.assertEqual(inst.flow_type, FlowTypes.Continue)

    def test_25_rorc_a(self):
        mem = [0x25]
        inst = disassemble(mem, pc=0)
        self.assertEqual(str(inst), "rorc a,1")
        self.assertEqual(len(inst), len(mem))
        self.assertEqual(inst.flow_type, FlowTypes.Continue)

    def test_26_rol_a(self):
        mem = [0x26]
        inst = disassemble(mem, pc=0)
        self.assertEqual(str(inst), "rol a,1")
        self.assertEqual(len(inst), len(mem))
        self.assertEqual(inst.flow_type, FlowTypes.Continue)

    def test_27_rolc_a(self):
        mem = [0x27]
        inst = disassemble(mem, pc=0)
        self.assertEqual(str(inst), "rolc a,1")
        self.assertEqual(len(inst), len(mem))
        self.assertEqual(inst.flow_type, FlowTypes.Continue)

    def test_27_addc_a_hl(self):
        mem = [0x27]
        inst = disassemble(mem, pc=0)
        self.assertEqual(str(inst), "rolc a,1")
        self.assertEqual(len(inst), len(mem))
        self.assertEqual(inst.flow_type, FlowTypes.Continue)

    def test_28_addc_a_addr16(self):
        for addr16 in (0x0000, 0xabcd, 0xffff):
            low = addr16 & 0xff
            high = (addr16 >> 8) & 0xff
            mem = [0x28, low, high]
            inst = disassemble(mem, pc=0)
            self.assertEqual(str(inst), 'addc a,!0x%04x' % addr16)
            self.assertEqual(len(inst), len(mem))
            self.assertEqual(inst.flow_type, FlowTypes.Continue)

    def test_29_sub_a_hl_plus_offset(self):
        mem = [0x29, 0xab]
        inst = disassemble(mem, pc=0)
        self.assertEqual(str(inst), 'addc a,[hl+0xab]')
        self.assertEqual(len(inst), len(mem))
        self.assertEqual(inst.flow_type, FlowTypes.Continue)

    def test_2d_a_imm8(self):
        mem = [0x2d, 0xab]
        inst = disassemble(mem, pc=0)
        self.assertEqual(str(inst), "addc a,#0xab")
        self.assertEqual(len(inst), len(mem))
        self.assertEqual(inst.flow_type, FlowTypes.Continue)

    def test_2e_addc_a_saddr(self):
        for saddr in range(0xfe20, 0xff20):
            saddr_low = saddr & 0xff
            mem = [0x2e, saddr_low]
            inst = disassemble(mem, pc=0)
            self.assertEqual(str(inst), 'addc a,0x%04x' % saddr)
            self.assertEqual(len(inst), len(mem))
            self.assertEqual(inst.flow_type, FlowTypes.Continue)

    def test_30_37_xch_a_reg(self):
        d = {0x30: 'xch a,x',                  0x32: 'xch a,c',
             0x33: 'xch a,b', 0x34: 'xch a,e', 0x35: 'xch a,d',
             0x36: 'xch a,l', 0x37: 'xch a,h'}

        for opcode, expected_inst in d.items():
            mem = [opcode]
            inst = disassemble(mem, pc=0)
            self.assertEqual(str(inst), expected_inst)
            self.assertEqual(len(inst), len(mem))
            self.assertEqual(inst.flow_type, FlowTypes.Continue)

    def test_38_subc_a_addr16(self):
        for addr16 in (0x0000, 0xabcd, 0xffff):
            low = addr16 & 0xff
            high = (addr16 >> 8) & 0xff
            mem = [0x38, low, high]
            inst = disassemble(mem, pc=0)
            self.assertEqual(str(inst), "subc a,!0x%04x" % addr16)
            self.assertEqual(len(inst), len(mem))
            self.assertEqual(inst.flow_type, FlowTypes.Continue)

    def test_39_subc_a_hl_plus_offset(self):
        mem = [0x39, 0xab]
        inst = disassemble(mem, pc=0)
        self.assertEqual(str(inst), 'subc a,[hl+0xab]')
        self.assertEqual(len(inst), len(mem))
        self.assertEqual(inst.flow_type, FlowTypes.Continue)

    def test_3d_subc_a_imm8(self):
        mem = [0x3d, 0xab]
        inst = disassemble(mem, pc=0)
        self.assertEqual(str(inst), "subc a,#0xab")
        self.assertEqual(len(inst), len(mem))
        self.assertEqual(inst.flow_type, FlowTypes.Continue)

    def test_3e_subc_a_saddr(self):
        for saddr in range(0xfe20, 0xff20):
            saddr_low = saddr & 0xff
            mem = [0x3e, saddr_low]
            inst = disassemble(mem, pc=0)
            self.assertEqual(str(inst), 'subc a,0x%04x' % saddr)
            self.assertEqual(len(inst), len(mem))
            self.assertEqual(inst.flow_type, FlowTypes.Continue)

    def test_3f_subc_a_hl(self):
        mem = [0x3f]
        inst = disassemble(mem, pc=0)
        self.assertEqual(str(inst), "subc a,[hl]")
        self.assertEqual(len(inst), len(mem))
        self.assertEqual(inst.flow_type, FlowTypes.Continue)

    def test_40_47_inc_reg(self):
        d = {0x40: 'inc x', 0x41: 'inc a', 0x42: 'inc c',
             0x43: 'inc b', 0x44: 'inc e', 0x45: 'inc d',
             0x46: 'inc l', 0x47: 'inc h'}

        for opcode, expected_inst in d.items():
            mem = [opcode]
            inst = disassemble(mem, pc=0)
            self.assertEqual(str(inst), expected_inst)
            self.assertEqual(len(inst), len(mem))
            self.assertEqual(inst.flow_type, FlowTypes.Continue)

    def test_48_cmp_a_addr16(self):
        for addr16 in (0x0000, 0xabcd, 0xffff):
            low = addr16 & 0xff
            high = (addr16 >> 8) & 0xff
            mem = [0x48, low, high]
            inst = disassemble(mem, pc=0)
            self.assertEqual(str(inst), 'cmp a,!0x%04x' % addr16)
            self.assertEqual(len(inst), len(mem))
            self.assertEqual(inst.flow_type, FlowTypes.Continue)

    def test_49_cmp_a_hl_plus_offset(self):
        mem = [0x49, 0xab]
        inst = disassemble(mem, pc=0)
        self.assertEqual(str(inst), 'cmp a,[hl+0xab]')
        self.assertEqual(len(inst), len(mem))
        self.assertEqual(inst.flow_type, FlowTypes.Continue)

    def test_4d_cmp_a_imm8(self):
        mem = [0x4d, 0xab]
        inst = disassemble(mem, pc=0)
        self.assertEqual(str(inst), "cmp a,#0xab")
        self.assertEqual(len(inst), len(mem))
        self.assertEqual(inst.flow_type, FlowTypes.Continue)

    def test_4e_cmp_a_saddr(self):
        for saddr in range(0xfe20, 0xff20):
            saddr_low = saddr & 0xff
            mem = [0x4e, saddr_low]
            inst = disassemble(mem, pc=0)
            self.assertEqual(str(inst), 'cmp a,0x%04x' % saddr)
            self.assertEqual(len(inst), len(mem))
            self.assertEqual(inst.flow_type, FlowTypes.Continue)

    def test_4f_cmp_a_hl(self):
        mem = [0x4f]
        inst = disassemble(mem, pc=0)
        self.assertEqual(str(inst), "cmp a,[hl]")
        self.assertEqual(len(inst), len(mem))
        self.assertEqual(inst.flow_type, FlowTypes.Continue)

    def test_50_57_dec_reg(self):
        d = {0x50: 'dec x', 0x51: 'dec a', 0x52: 'dec c',
             0x53: 'dec b', 0x54: 'dec e', 0x55: 'dec d',
             0x56: 'dec l', 0x57: 'dec h'}

        for opcode, expected_inst in d.items():
            mem = [opcode]
            inst = disassemble(mem, pc=0)
            self.assertEqual(str(inst), expected_inst)
            self.assertEqual(len(inst), len(mem))
            self.assertEqual(inst.flow_type, FlowTypes.Continue)

    def test_58_and_a_addr16(self):
        for addr16 in (0x0000, 0xabcd, 0xffff):
            low = addr16 & 0xff
            high = (addr16 >> 8) & 0xff
            mem = [0x58, low, high]
            inst = disassemble(mem, pc=0)
            self.assertEqual(str(inst), 'and a,!0x%04x' % addr16)
            self.assertEqual(len(inst), len(mem))
            self.assertEqual(inst.flow_type, FlowTypes.Continue)

    def test_59_and_a_hl_plus_offset(self):
        mem = [0x59, 0xab]
        inst = disassemble(mem, pc=0)
        self.assertEqual(str(inst), 'and a,[hl+0xab]')
        self.assertEqual(len(inst), len(mem))
        self.assertEqual(inst.flow_type, FlowTypes.Continue)

    def test_5d_and_a_imm8(self):
        mem = [0x5d, 0xab]
        inst = disassemble(mem, pc=0)
        self.assertEqual(str(inst), "and a,#0xab")
        self.assertEqual(len(inst), len(mem))
        self.assertEqual(inst.flow_type, FlowTypes.Continue)

    def test_5e_and_a_saddr(self):
        for saddr in range(0xfe20, 0xff20):
            saddr_low = saddr & 0xff
            mem = [0x5e, saddr_low]
            inst = disassemble(mem, pc=0)
            self.assertEqual(str(inst), 'and a,0x%04x' % saddr)
            self.assertEqual(len(inst), len(mem))
            self.assertEqual(inst.flow_type, FlowTypes.Continue)

    def test_5f_and_a_hl(self):
        mem = [0x5f]
        inst = disassemble(mem, pc=0)
        self.assertEqual(str(inst), "and a,[hl]")
        self.assertEqual(len(inst), len(mem))

    def test_60_67_mov_a_reg(self):
        d = {0x60: 'mov a,x',                  0x62: 'mov a,c',
             0x63: 'mov a,b', 0x64: 'mov a,e', 0x65: 'mov a,d',
             0x66: 'mov a,l', 0x67: 'mov a,h'}

        for opcode, expected_inst in d.items():
            mem = [opcode]
            inst = disassemble(mem, pc=0)
            self.assertEqual(str(inst), expected_inst)
            self.assertEqual(len(inst), len(mem))
            self.assertEqual(inst.flow_type, FlowTypes.Continue)

    def test_61_80_adjba(self):
        mem = [0x61, 0x80]
        inst = disassemble(mem, pc=0)
        self.assertEqual(str(inst), "adjba")
        self.assertEqual(len(inst), len(mem))
        self.assertEqual(inst.flow_type, FlowTypes.Continue)

    def test_61_90_adjbs(self):
        mem = [0x61, 0x90]
        inst = disassemble(mem, pc=0)
        self.assertEqual(str(inst), "adjbs")
        self.assertEqual(len(inst), len(mem))
        self.assertEqual(inst.flow_type, FlowTypes.Continue)

    def test_61_00_thru_07_and_reg_a(self):
        d = {0x00: 'add x,a', 0x01: 'add a,a', 0x02: 'add c,a',
             0x03: 'add b,a', 0x04: 'add e,a', 0x05: 'add d,a',
             0x06: 'add l,a', 0x07: 'add h,a'}

        for operand, expected_inst in d.items():
            mem = [0x61, operand]
            inst = disassemble(mem, pc=0)
            self.assertEqual(str(inst), expected_inst)
            self.assertEqual(len(inst), len(mem))
            self.assertEqual(inst.flow_type, FlowTypes.Continue)

    def test_61_08_thru_0f_add_a_reg(self):
        d = {0x08: 'add a,x', 0x09: 'add a,a', 0x0a: 'add a,c',
             0x0b: 'add a,b', 0x0c: 'add a,e', 0x0d: 'add a,d',
             0x0e: 'add a,l', 0x0f: 'add a,h'}

        for operand, expected_inst in d.items():
            mem = [0x61, operand]
            inst = disassemble(mem, pc=0)
            self.assertEqual(str(inst), expected_inst)
            self.assertEqual(len(inst), len(mem))
            self.assertEqual(inst.flow_type, FlowTypes.Continue)

    def test_61_10_thru_17_and_reg_a(self):
        d = {0x10: 'sub x,a', 0x11: 'sub a,a', 0x12: 'sub c,a',
             0x13: 'sub b,a', 0x14: 'sub e,a', 0x15: 'sub d,a',
             0x16: 'sub l,a', 0x17: 'sub h,a'}

        for operand, expected_inst in d.items():
            mem = [0x61, operand]
            inst = disassemble(mem, pc=0)
            self.assertEqual(str(inst), expected_inst)
            self.assertEqual(len(inst), len(mem))
            self.assertEqual(inst.flow_type, FlowTypes.Continue)

    def test_61_18_thru_1f_sub_a_reg(self):
        d = {0x18: 'sub a,x', 0x19: 'sub a,a', 0x1a: 'sub a,c',
             0x1b: 'sub a,b', 0x1c: 'sub a,e', 0x1d: 'sub a,d',
             0x1e: 'sub a,l', 0x1f: 'sub a,h'}

        for operand, expected_inst in d.items():
            mem = [0x61, operand]
            inst = disassemble(mem, pc=0)
            self.assertEqual(str(inst), expected_inst)
            self.assertEqual(len(inst), len(mem))
            self.assertEqual(inst.flow_type, FlowTypes.Continue)

    def test_61_20_thru_27_addc_reg_a(self):
        d = {0x20: 'addc x,a', 0x21: 'addc a,a', 0x22: 'addc c,a',
             0x23: 'addc b,a', 0x24: 'addc e,a', 0x25: 'addc d,a',
             0x26: 'addc l,a', 0x27: 'addc h,a'}

        for operand, expected_inst in d.items():
            mem = [0x61, operand]
            inst = disassemble(mem, pc=0)
            self.assertEqual(str(inst), expected_inst)
            self.assertEqual(len(inst), len(mem))
            self.assertEqual(inst.flow_type, FlowTypes.Continue)

    def test_61_28_thru_2f_addc_a_reg(self):
        d = {0x28: 'addc a,x', 0x29: 'addc a,a', 0x2a: 'addc a,c',
             0x2b: 'addc a,b', 0x2c: 'addc a,e', 0x2d: 'addc a,d',
             0x2e: 'addc a,l', 0x2f: 'addc a,h'}

        for operand, expected_inst in d.items():
            mem = [0x61, operand]
            inst = disassemble(mem, pc=0)
            self.assertEqual(str(inst), expected_inst)
            self.assertEqual(len(inst), len(mem))
            self.assertEqual(inst.flow_type, FlowTypes.Continue)

    def test_61_30_thru_37_subc_reg_a(self):
        d = {0x30: 'subc x,a', 0x31: 'subc a,a', 0x32: 'subc c,a',
             0x33: 'subc b,a', 0x34: 'subc e,a', 0x35: 'subc d,a',
             0x36: 'subc l,a', 0x37: 'subc h,a'}

        for operand, expected_inst in d.items():
            mem = [0x61, operand]
            inst = disassemble(mem, pc=0)
            self.assertEqual(str(inst), expected_inst)
            self.assertEqual(len(inst), len(mem))
            self.assertEqual(inst.flow_type, FlowTypes.Continue)

    def test_61_38_thru_3f_subc_a_reg(self):
        d = {0x38: 'subc a,x', 0x39: 'subc a,a', 0x3a: 'subc a,c',
             0x3b: 'subc a,b', 0x3c: 'subc a,e', 0x3d: 'subc a,d',
             0x3e: 'subc a,l', 0x3f: 'subc a,h'}

        for operand, expected_inst in d.items():
            mem = [0x61, operand]
            inst = disassemble(mem, pc=0)
            self.assertEqual(str(inst), expected_inst)
            self.assertEqual(len(inst), len(mem))
            self.assertEqual(inst.flow_type, FlowTypes.Continue)

    def test_61_40_thru_47_cmp_reg_a(self):
        d = {0x40: 'cmp x,a', 0x41: 'cmp a,a', 0x42: 'cmp c,a',
             0x43: 'cmp b,a', 0x44: 'cmp e,a', 0x45: 'cmp d,a',
             0x46: 'cmp l,a', 0x47: 'cmp h,a'}

        for operand, expected_inst in d.items():
            mem = [0x61, operand]
            inst = disassemble(mem, pc=0)
            self.assertEqual(str(inst), expected_inst)
            self.assertEqual(len(inst), len(mem))
            self.assertEqual(inst.flow_type, FlowTypes.Continue)

    def test_61_48_thru_4f_cmp_a_reg(self):
        d = {0x48: 'cmp a,x', 0x49: 'cmp a,a', 0x4a: 'cmp a,c',
             0x4b: 'cmp a,b', 0x4c: 'cmp a,e', 0x4d: 'cmp a,d',
             0x4e: 'cmp a,l', 0x4f: 'cmp a,h'}

        for operand, expected_inst in d.items():
            mem = [0x61, operand]
            inst = disassemble(mem, pc=0)
            self.assertEqual(str(inst), expected_inst)
            self.assertEqual(len(inst), len(mem))
            self.assertEqual(inst.flow_type, FlowTypes.Continue)

    def test_61_50_thru_57_and_reg_a(self):
        d = {0x50: 'and x,a', 0x51: 'and a,a', 0x52: 'and c,a',
             0x53: 'and b,a', 0x54: 'and e,a', 0x55: 'and d,a',
             0x56: 'and l,a', 0x57: 'and h,a'}

        for operand, expected_inst in d.items():
            mem = [0x61, operand]
            inst = disassemble(mem, pc=0)
            self.assertEqual(str(inst), expected_inst)
            self.assertEqual(len(inst), len(mem))
            self.assertEqual(inst.flow_type, FlowTypes.Continue)

    def test_61_58_thru_5f_and_a_reg(self):
        d = {0x58: 'and a,x', 0x59: 'and a,a', 0x5a: 'and a,c',
             0x5b: 'and a,b', 0x5c: 'and a,e', 0x5d: 'and a,d',
             0x5e: 'and a,l', 0x5f: 'and a,h'}

        for operand, expected_inst in d.items():
            mem = [0x61, operand]
            inst = disassemble(mem, pc=0)
            self.assertEqual(str(inst), expected_inst)
            self.assertEqual(len(inst), len(mem))
            self.assertEqual(inst.flow_type, FlowTypes.Continue)

    def test_61_60_thru_67_or_reg_a(self):
        d = {0x60: 'or x,a', 0x61: 'or a,a', 0x62: 'or c,a',
             0x63: 'or b,a', 0x64: 'or e,a', 0x65: 'or d,a',
             0x66: 'or l,a', 0x67: 'or h,a'}

        for operand, expected_inst in d.items():
            mem = [0x61, operand]
            inst = disassemble(mem, pc=0)
            self.assertEqual(str(inst), expected_inst)
            self.assertEqual(len(inst), len(mem))
            self.assertEqual(inst.flow_type, FlowTypes.Continue)

    def test_61_68_thru_6f_or_a_reg(self):
        d = {0x68: 'or a,x', 0x69: 'or a,a', 0x6a: 'or a,c',
             0x6b: 'or a,b', 0x6c: 'or a,e', 0x6d: 'or a,d',
             0x6e: 'or a,l', 0x6f: 'or a,h'}

        for operand, expected_inst in d.items():
            mem = [0x61, operand]
            inst = disassemble(mem, pc=0)
            self.assertEqual(str(inst), expected_inst)
            self.assertEqual(len(inst), len(mem))
            self.assertEqual(inst.flow_type, FlowTypes.Continue)

    def test_61_70_thru_77_or_reg_a(self):
        d = {0x70: 'xor x,a', 0x71: 'xor a,a', 0x72: 'xor c,a',
             0x73: 'xor b,a', 0x74: 'xor e,a', 0x75: 'xor d,a',
             0x76: 'xor l,a', 0x77: 'xor h,a'}

        for operand, expected_inst in d.items():
            mem = [0x61, operand]
            inst = disassemble(mem, pc=0)
            self.assertEqual(str(inst), expected_inst)
            self.assertEqual(len(inst), len(mem))
            self.assertEqual(inst.flow_type, FlowTypes.Continue)

    def test_61_78_thru_7f_or_a_reg(self):
        d = {0x78: 'xor a,x', 0x79: 'xor a,a', 0x7a: 'xor a,c',
             0x7b: 'xor a,b', 0x7c: 'xor a,e', 0x7d: 'xor a,d',
             0x7e: 'xor a,l', 0x7f: 'xor a,h'}

        for operand, expected_inst in d.items():
            mem = [0x61, operand]
            inst = disassemble(mem, pc=0)
            self.assertEqual(str(inst), expected_inst)
            self.assertEqual(len(inst), len(mem))
            self.assertEqual(inst.flow_type, FlowTypes.Continue)

    def test_61_dx_fx_sel_rbx(self):
        d = {0xd0: 'sel rb0', 0xd8: 'sel rb1',
             0xf0: 'sel rb2', 0xf8: 'sel rb3'}

        for operand, expected_inst in d.items():
            mem = [0x61, operand]
            inst = disassemble(mem, pc=0)
            self.assertEqual(str(inst), expected_inst)
            self.assertEqual(len(inst), len(mem))
            self.assertEqual(inst.flow_type, FlowTypes.Continue)

    def test_61_x9_mov1_a_bit_cy(self):
        operands = (0x89, 0x99, 0xa9, 0xb9, 0xc9, 0xd9, 0xe9, 0xf9)

        for bit, operand in enumerate(operands):
            mem = [0x61, operand]
            inst = disassemble(mem, pc=0)
            self.assertEqual(str(inst), "mov1 a.%d,cy" % bit)
            self.assertEqual(len(inst), len(mem))
            self.assertEqual(inst.flow_type, FlowTypes.Continue)

    def test_61_xa_set1_a_bit(self):
        operands = (0x8a, 0x9a, 0xaa, 0xba, 0xca, 0xda, 0xea, 0xfa)

        for bit, operand in enumerate(operands):
            mem = [0x61, operand]
            inst = disassemble(mem, pc=0)
            self.assertEqual(str(inst), "set1 a.%d" % bit)
            self.assertEqual(len(inst), len(mem))
            self.assertEqual(inst.flow_type, FlowTypes.Continue)

    def test_61_xb_clr1_a_bit(self):
        operands = (0x8b, 0x9b, 0xab, 0xbb, 0xcb, 0xdb, 0xeb, 0xfb)

        for bit, operand in enumerate(operands):
            mem = [0x61, operand]
            inst = disassemble(mem, pc=0)
            self.assertEqual(str(inst), "clr1 a.%d" % bit)
            self.assertEqual(len(inst), len(mem))
            self.assertEqual(inst.flow_type, FlowTypes.Continue)

    def test_61_xc_mov1_cy_a_bit(self):
        operands = (0x8c, 0x9c, 0xac, 0xbc, 0xcc, 0xdc, 0xec, 0xfc)

        for bit, operand in enumerate(operands):
            mem = [0x61, operand]
            inst = disassemble(mem, pc=0)
            self.assertEqual(str(inst), "mov1 cy,a.%d" % bit)
            self.assertEqual(len(inst), len(mem))
            self.assertEqual(inst.flow_type, FlowTypes.Continue)

    def test_61_xd_and1_cy_a_bit(self):
        operands = (0x8d, 0x9d, 0xad, 0xbd, 0xcd, 0xdd, 0xed, 0xfd)

        for bit, operand in enumerate(operands):
            mem = [0x61, operand]
            inst = disassemble(mem, pc=0)
            self.assertEqual(str(inst), "and1 cy,a.%d" % bit)
            self.assertEqual(len(inst), len(mem))
            self.assertEqual(inst.flow_type, FlowTypes.Continue)

    def test_61_xe_or1_cy_a_bit(self):
        operands = (0x8e, 0x9e, 0xae, 0xbe, 0xce, 0xde, 0xee, 0xfe)

        for bit, operand in enumerate(operands):
            mem = [0x61, operand]
            inst = disassemble(mem, pc=0)
            self.assertEqual(str(inst), "or1 cy,a.%d" % bit)
            self.assertEqual(len(inst), len(mem))
            self.assertEqual(inst.flow_type, FlowTypes.Continue)

    def test_61_xf_xor1_cy_a_bit(self):
        operands = (0x8f, 0x9f, 0xaf, 0xbf, 0xcf, 0xdf, 0xef, 0xff)

        for bit, operand in enumerate(operands):
            mem = [0x61, operand]
            inst = disassemble(mem, pc=0)
            self.assertEqual(str(inst), "xor1 cy,a.%d" % bit)
            self.assertEqual(len(inst), len(mem))
            self.assertEqual(inst.flow_type, FlowTypes.Continue)

    def test_61_raises_for_illegal_second_opcode(self):
        mem = [0x61, 0x81]
        with self.assertRaises(IllegalInstructionError):
            disassemble(mem, pc=0)

    def test_68_or_a_addr16(self):
        for addr16 in (0x0000, 0xabcd, 0xffff):
            low = addr16 & 0xff
            high = (addr16 >> 8) & 0xff
            mem = [0x68, low, high]
            inst = disassemble(mem, pc=0)
            self.assertEqual(str(inst), 'or a,!0x%04x' % addr16)
            self.assertEqual(len(inst), len(mem))
            self.assertEqual(inst.flow_type, FlowTypes.Continue)

    def test_69_or_a_hl_plus_offset(self):
        mem = [0x69, 0xab]
        inst = disassemble(mem, pc=0)
        self.assertEqual(str(inst), 'or a,[hl+0xab]')
        self.assertEqual(len(inst), len(mem))
        self.assertEqual(inst.flow_type, FlowTypes.Continue)

    def test_6d_or_a_imm8(self):
        mem = [0x6d, 0xab]
        inst = disassemble(mem, pc=0)
        self.assertEqual(str(inst), "or a,#0xab")
        self.assertEqual(len(inst), len(mem))
        self.assertEqual(inst.flow_type, FlowTypes.Continue)

    def test_6e_or_a_saddr(self):
        for saddr in range(0xfe20, 0xff20):
            saddr_low = saddr & 0xff
            mem = [0x6e, saddr_low]
            inst = disassemble(mem, pc=0)
            self.assertEqual(str(inst), 'or a,0x%04x' % saddr)
            self.assertEqual(len(inst), len(mem))
            self.assertEqual(inst.flow_type, FlowTypes.Continue)

    def test_6f_or_a_hl(self):
        mem = [0x6f]
        inst = disassemble(mem, pc=0)
        self.assertEqual(str(inst), "or a,[hl]")
        self.assertEqual(len(inst), len(mem))
        self.assertEqual(inst.flow_type, FlowTypes.Continue)

    def test_70_77_mov_a_reg(self):
        d = {0x70: 'mov x,a',                  0x72: 'mov c,a',
             0x73: 'mov b,a', 0x74: 'mov e,a', 0x75: 'mov d,a',
             0x76: 'mov l,a', 0x77: 'mov h,a'}

        for opcode, expected_inst in d.items():
            mem = [opcode]
            inst = disassemble(mem, pc=0)
            self.assertEqual(str(inst), expected_inst)
            self.assertEqual(len(inst), len(mem))
            self.assertEqual(inst.flow_type, FlowTypes.Continue)

    def test_71_00_stop(self):
        mem = [0x71, 0x00]
        inst = disassemble(mem, pc=0)
        self.assertEqual(str(inst), 'stop')
        self.assertEqual(len(inst), len(mem))
        self.assertEqual(inst.flow_type, FlowTypes.Stop)

    def test_71_01_mov1_saddr_bit_cy(self):
        operands = (0x01, 0x11, 0x21, 0x31, 0x41, 0x51, 0x61, 0x71)
        for bit, operand in enumerate(operands):
            for saddr in range(0xfe20, 0xff20):
                if saddr == 0xff1e:
                    continue # special case; would disassemble as MOV1 PSW.bit,CY
                saddr_low = saddr & 0xff
                mem = [0x71, operand, saddr_low]
                inst = disassemble(mem, pc=0)
                self.assertEqual(str(inst), "mov1 0x%04x.%d,cy" % (saddr, bit))
                self.assertEqual(len(inst), len(mem))
                self.assertEqual(inst.flow_type, FlowTypes.Continue)

    def test_71_01_mov1_psw_bit_cy(self):
        operands = (0x01, 0x11, 0x21, 0x31, 0x41, 0x51, 0x61, 0x71)
        for bit, operand in enumerate(operands):
            mem = [0x71, operand, 0x1e]
            inst = disassemble(mem, pc=0)
            self.assertEqual(str(inst), "mov1 psw.%d,cy" % bit)
            self.assertEqual(len(inst), len(mem))
            self.assertEqual(inst.flow_type, FlowTypes.Continue)

    def test_71_04_thru_74_mov1_cy_saddr_bit(self):
        operands = (0x04, 0x14, 0x24, 0x34, 0x44, 0x54, 0x64, 0x74)
        for bit, operand in enumerate(operands):
            for saddr in range(0xfe20, 0xff20):
                if saddr == 0xff1e:
                    continue # special case; would disassemble as MOV1 CY,PSW.bit
                saddr_low = saddr & 0xff
                mem = [0x71, operand, saddr_low]
                inst = disassemble(mem, pc=0)
                self.assertEqual(str(inst), "mov1 cy,0x%04x.%d" % (saddr, bit))
                self.assertEqual(len(inst), len(mem))
                self.assertEqual(inst.flow_type, FlowTypes.Continue)

    def test_71_04_thru_74_cy_psw_bit(self):
        operands = (0x04, 0x14, 0x24, 0x34, 0x44, 0x54, 0x64, 0x74)
        for bit, operand in enumerate(operands):
            mem = [0x71, operand, 0x1e]
            inst = disassemble(mem, pc=0)
            self.assertEqual(str(inst), "mov1 cy,psw.%d" % bit)
            self.assertEqual(len(inst), len(mem))
            self.assertEqual(inst.flow_type, FlowTypes.Continue)

    def test_71_05_thru_75_and1_cy_saddr_bit(self):
        operands = (0x05, 0x15, 0x25, 0x35, 0x45, 0x55, 0x65, 0x75)
        for bit, operand in enumerate(operands):
            for saddr in range(0xfe20, 0xff20):
                if saddr == 0xff1e:
                    continue # special case; would disassemble as AND1 CY,PSW.bit
                saddr_low = saddr & 0xff
                mem = [0x71, operand, saddr_low]
                inst = disassemble(mem, pc=0)
                self.assertEqual(str(inst), "and1 cy,0x%04x.%d" % (saddr, bit))
                self.assertEqual(len(inst), len(mem))
                self.assertEqual(inst.flow_type, FlowTypes.Continue)

    def test_71_05_thru_75_and1_cy_psw_bit(self):
        operands = (0x05, 0x15, 0x25, 0x35, 0x45, 0x55, 0x65, 0x75)
        for bit, operand in enumerate(operands):
            mem = [0x71, operand, 0x1e]
            inst = disassemble(mem, pc=0)
            self.assertEqual(str(inst), "and1 cy,psw.%d" % bit)
            self.assertEqual(len(inst), len(mem))
            self.assertEqual(inst.flow_type, FlowTypes.Continue)

    def test_71_06_thru_76_or1_cy_saddr_bit(self):
        operands = (0x06, 0x16, 0x26, 0x36, 0x46, 0x56, 0x66, 0x76)
        for bit, operand in enumerate(operands):
            for saddr in range(0xfe20, 0xff20):
                if saddr == 0xff1e:
                    continue # special case; would disassemble as OR1 CY,PSW.bit
                saddr_low = saddr & 0xff
                mem = [0x71, operand, saddr_low]
                inst = disassemble(mem, pc=0)
                self.assertEqual(str(inst), "or1 cy,0x%04x.%d" % (saddr, bit))
                self.assertEqual(len(inst), len(mem))
                self.assertEqual(inst.flow_type, FlowTypes.Continue)

    def test_71_06_thru_76_or1_cy_psw_bit(self):
        operands = (0x06, 0x16, 0x26, 0x36, 0x46, 0x56, 0x66, 0x76)
        for bit, operand in enumerate(operands):
            mem = [0x71, operand, 0x1e]
            inst = disassemble(mem, pc=0)
            self.assertEqual(str(inst), "or1 cy,psw.%d" % bit)
            self.assertEqual(len(inst), len(mem))
            self.assertEqual(inst.flow_type, FlowTypes.Continue)

    def test_71_07_thru_77_xor1_cy_saddr_bit(self):
        operands = (0x07, 0x17, 0x27, 0x37, 0x47, 0x57, 0x67, 0x77)
        for bit, operand in enumerate(operands):
            for saddr in range(0xfe20, 0xff20):
                if saddr == 0xff1e:
                    continue # special case; would disassemble as XOR1 CY,PSW.bit
                saddr_low = saddr & 0xff
                mem = [0x71, operand, saddr_low]
                inst = disassemble(mem, pc=0)
                self.assertEqual(str(inst), "xor1 cy,0x%04x.%d" % (saddr, bit))
                self.assertEqual(len(inst), len(mem))
                self.assertEqual(inst.flow_type, FlowTypes.Continue)

    def test_71_07_thru_77_xor1_cy_psw_bit(self):
        operands = (0x07, 0x17, 0x27, 0x37, 0x47, 0x57, 0x67, 0x77)
        for bit, operand in enumerate(operands):
            mem = [0x71, operand, 0x1e]
            inst = disassemble(mem, pc=0)
            self.assertEqual(str(inst), "xor1 cy,psw.%d" % bit)
            self.assertEqual(len(inst), len(mem))
            self.assertEqual(inst.flow_type, FlowTypes.Continue)

    def test_71_10_halt(self):
        mem = [0x71, 0x10]
        inst = disassemble(mem, pc=0)
        self.assertEqual(str(inst), 'halt')
        self.assertEqual(len(inst), len(mem))
        self.assertEqual(inst.flow_type, FlowTypes.Stop)

    def test_71_09_thru_79_mov1_sfr_bit_cy(self):
        operands = (0x09, 0x19, 0x29, 0x39, 0x49, 0x59, 0x69, 0x79)
        for bit, operand in enumerate(operands):
            for sfr in range(0xff00, 0x10000):
                sfr_low = sfr & 0xff
                mem = [0x71, operand, sfr_low]
                inst = disassemble(mem, pc=0)
                self.assertEqual(str(inst), 'mov1 0x%04x.%d,cy' % (sfr, bit))
                self.assertEqual(len(inst), len(mem))
                self.assertEqual(inst.flow_type, FlowTypes.Continue)

    def test_71_0a_set1_sfr_bit(self):
        operands = (0x0a, 0x1a, 0x2a, 0x3a, 0x4a, 0x5a, 0x6a, 0x7a)
        for bit, operand in enumerate(operands):
            for sfr in range(0xff00, 0x10000):
                sfr_low = sfr & 0xff
                mem = [0x71, operand, sfr_low]
                inst = disassemble(mem, pc=0)
                self.assertEqual(str(inst), 'set1 0x%04x.%d' % (sfr, bit))
                self.assertEqual(len(inst), len(mem))
                self.assertEqual(inst.flow_type, FlowTypes.Continue)

    def test_71_0c_thru_7c_mov1_cy_sfr_bit(self):
        operands = (0x0c, 0x1c, 0x2c, 0x3c, 0x4c, 0x5c, 0x6c, 0x7c)
        for bit, operand in enumerate(operands):
            for sfr in range(0xff00, 0x10000):
                sfr_low = sfr & 0xff
                mem = [0x71, operand, sfr_low]
                inst = disassemble(mem, pc=0)
                self.assertEqual(str(inst), 'mov1 cy,0x%04x.%d' % (sfr, bit))
                self.assertEqual(len(inst), len(mem))
                self.assertEqual(inst.flow_type, FlowTypes.Continue)

    def test_72_82_thru_f3_clr1_hl_bit(self):
        operands = (0x82, 0x92, 0xa2, 0xb2, 0xc2, 0xd2, 0xe2, 0xf2)
        for bit, operand in enumerate(operands):
            mem = [0x71, operand]
            inst = disassemble(mem, pc=0)
            self.assertEqual(str(inst), 'set1 [hl].%d' % bit)
            self.assertEqual(len(inst), len(mem))
            self.assertEqual(inst.flow_type, FlowTypes.Continue)

    def test_71_83_thru_f3_clr1_hl_bit(self):
        operands = (0x83, 0x93, 0xa3, 0xb3, 0xc3, 0xd3, 0xe3, 0xf3)
        for bit, operand in enumerate(operands):
            mem = [0x71, operand]
            inst = disassemble(mem, pc=0)
            self.assertEqual(str(inst), 'clr1 [hl].%d' % bit)
            self.assertEqual(len(inst), len(mem))
            self.assertEqual(inst.flow_type, FlowTypes.Continue)

    def test_71_84_thru_f4_mov1_hl_bit(self):
        operands = (0x84, 0x94, 0xa4, 0xb4, 0xc4, 0xd4, 0xe4, 0xf4)
        for bit, operand in enumerate(operands):
            mem = [0x71, operand]
            inst = disassemble(mem, pc=0)
            self.assertEqual(str(inst), 'mov1 cy,[hl].%d' % bit)
            self.assertEqual(len(inst), len(mem))
            self.assertEqual(inst.flow_type, FlowTypes.Continue)

    def test_71_84_thru_f4_and1_hl_bit(self):
        operands = (0x85, 0x95, 0xa5, 0xb5, 0xc5, 0xd5, 0xe5, 0xf5)
        for bit, operand in enumerate(operands):
            mem = [0x71, operand]
            inst = disassemble(mem, pc=0)
            self.assertEqual(str(inst), 'and1 cy,[hl].%d' % bit)
            self.assertEqual(len(inst), len(mem))
            self.assertEqual(inst.flow_type, FlowTypes.Continue)

    def test_71_86_thru_f6_and1_hl_bit(self):
        operands = (0x86, 0x96, 0xa6, 0xb6, 0xc6, 0xd6, 0xe6, 0xf6)
        for bit, operand in enumerate(operands):
            mem = [0x71, operand]
            inst = disassemble(mem, pc=0)
            self.assertEqual(str(inst), 'or1 cy,[hl].%d' % bit)
            self.assertEqual(len(inst), len(mem))
            self.assertEqual(inst.flow_type, FlowTypes.Continue)

    def test_71_87_thru_f7_and1_hl_bit(self):
        operands = (0x87, 0x97, 0xa7, 0xb7, 0xc7, 0xd7, 0xe7, 0xf7)
        for bit, operand in enumerate(operands):
            mem = [0x71, operand]
            inst = disassemble(mem, pc=0)
            self.assertEqual(str(inst), 'xor1 cy,[hl].%d' % bit)
            self.assertEqual(len(inst), len(mem))
            self.assertEqual(inst.flow_type, FlowTypes.Continue)

    def test_71_81_thru_f1_mov1_hl_bit_cy(self):
        operands = (0x81, 0x91, 0xa1, 0xb1, 0xc1, 0xd1, 0xe1, 0xf1)
        for bit, operand in enumerate(operands):
            mem = [0x71, operand]
            inst = disassemble(mem, pc=0)
            self.assertEqual(str(inst), 'mov1 [hl].%d,cy' % bit)
            self.assertEqual(len(inst), len(mem))
            self.assertEqual(inst.flow_type, FlowTypes.Continue)

    def test_71_raises_for_illegal_second_opcode(self):
        mem = [0x71, 0xb0]
        with self.assertRaises(IllegalInstructionError):
            disassemble(mem, pc=0)

    def test_78_xor_a_addr16(self):
        for addr16 in (0x0000, 0xabcd, 0xffff):
            low = addr16 & 0xff
            high = (addr16 >> 8) & 0xff
            mem = [0x78, low, high]
            inst = disassemble(mem, pc=0)
            self.assertEqual(str(inst), 'xor a,!0x%04x' % addr16)
            self.assertEqual(len(inst), len(mem))
            self.assertEqual(inst.flow_type, FlowTypes.Continue)

    def test_79_xor_a_hl_plus_offset(self):
        mem = [0x79, 0xab]
        inst = disassemble(mem, pc=0)
        self.assertEqual(str(inst), 'xor a,[hl+0xab]')
        self.assertEqual(len(inst), len(mem))
        self.assertEqual(inst.flow_type, FlowTypes.Continue)

    def test_7d_xor_a_imm8(self):
        mem = [0x7d, 0xab]
        inst = disassemble(mem, pc=0)
        self.assertEqual(str(inst), "xor a,#0xab")
        self.assertEqual(len(inst), len(mem))
        self.assertEqual(inst.flow_type, FlowTypes.Continue)

    def test_7e_xor_a_saddr(self):
        for saddr in range(0xfe20, 0xff20):
            saddr_low = saddr & 0xff
            mem = [0x7e, saddr_low]
            inst = disassemble(mem, pc=0)
            self.assertEqual(str(inst), 'xor a,0x%04x' % saddr)
            self.assertEqual(len(inst), len(mem))
            self.assertEqual(inst.flow_type, FlowTypes.Continue)

    def test_7f_xor_a_hl(self):
        mem = [0x7f]
        inst = disassemble(mem, pc=0)
        self.assertEqual(str(inst), "xor a,[hl]")
        self.assertEqual(len(inst), len(mem))
        self.assertEqual(inst.flow_type, FlowTypes.Continue)

    def test_80_82_84_86_incw_regpair(self):
        d = {0x80: "incw ax", 0x82: "incw bc",
             0x84: "incw de", 0x86: "incw hl"}

        for opcode, expected_inst in d.items():
            mem = [opcode]
            inst = disassemble(mem, pc=0)
            self.assertEqual(str(inst), expected_inst)
            self.assertEqual(len(inst), len(mem))
            self.assertEqual(inst.flow_type, FlowTypes.Continue)

    def test_81_inc_saddr(self):
        for saddr in range(0xfe20, 0xff20):
            saddr_low = saddr & 0xff
            mem = [0x81, saddr_low]
            inst = disassemble(mem, pc=0)
            self.assertEqual(str(inst), "inc 0x%04x" % saddr)
            self.assertEqual(len(inst), len(mem))
            self.assertEqual(inst.flow_type, FlowTypes.Continue)

    def test_83_xch_a_saddr(self):
        for saddr in range(0xfe20, 0xff20):
            saddr_low = saddr & 0xff
            mem = [0x83, saddr_low]
            inst = disassemble(mem, pc=0)
            self.assertEqual(str(inst), "xch a,0x%04x" % saddr)
            self.assertEqual(len(inst), len(mem))
            self.assertEqual(inst.flow_type, FlowTypes.Continue)

    def test_85_mov_a_de(self):
        mem = [0x85]
        inst = disassemble(mem, pc=0)
        self.assertEqual(str(inst), "mov a,[de]")
        self.assertEqual(len(inst), len(mem))
        self.assertEqual(inst.flow_type, FlowTypes.Continue)

    def test_87_mov_a_hl(self):
        mem = [0x87]
        inst = disassemble(mem, pc=0)
        self.assertEqual(str(inst), "mov a,[hl]")
        self.assertEqual(len(inst), len(mem))
        self.assertEqual(inst.flow_type, FlowTypes.Continue)

    def test_88_add_saddr_imm8(self):
        for saddr in range(0xfe20, 0xff20):
            saddr_low = saddr & 0xff
            mem = [0x88, saddr_low, 0xab]
            inst = disassemble(mem, pc=0)
            self.assertEqual(str(inst), "add 0x%04x,#0xab" % saddr)
            self.assertEqual(len(inst), len(mem))
            self.assertEqual(inst.flow_type, FlowTypes.Continue)

    def test_8a_bc_rel(self):
        mem = bytearray(0x2000)
        code = [0x8a, 0xfe]
        for address, c in enumerate(code, 0x1000):
            mem[address] = c
        inst = disassemble(mem, pc=0x1000)
        self.assertEqual(str(inst), "dbnz c,0x1000")
        self.assertEqual(len(inst), len(code))
        self.assertEqual(inst.flow_type, FlowTypes.ConditionalJump)

    def test_8b_bc_rel(self):
        mem = bytearray(0x2000)
        code = [0x8b, 0xfe]
        for address, c in enumerate(code, 0x1000):
            mem[address] = c
        inst = disassemble(mem, pc=0x1000)
        self.assertEqual(str(inst), "dbnz b,0x1000")
        self.assertEqual(len(inst), len(code))
        self.assertEqual(inst.flow_type, FlowTypes.ConditionalJump)

    def test_8d_bc_rel(self):
        mem = bytearray(0x2000)
        code = [0x8d, 0xfe]
        for address, c in enumerate(code, 0x1000):
            mem[address] = c
        inst = disassemble(mem, pc=0x1000)
        self.assertEqual(str(inst), 'bc 0x1000')
        self.assertEqual(len(inst), len(code))
        self.assertEqual(inst.flow_type, FlowTypes.ConditionalJump)

    def test_8e_mov_a_addr16(self):
        for addr16 in (0x0000, 0xabcd, 0xffff):
            low = addr16 & 0xff
            high = (addr16 >> 8) & 0xff
            mem = [0x8e, low, high]
            inst = disassemble(mem, pc=0)
            self.assertEqual(str(inst), 'mov a,!0x%04x' % addr16)
            self.assertEqual(len(inst), len(mem))
            self.assertEqual(inst.flow_type, FlowTypes.Continue)

    def test_8f_reti(self):
        mem = [0x8f]
        inst = disassemble(mem, pc=0)
        self.assertEqual(str(inst), "reti")
        self.assertEqual(len(inst), len(mem))
        self.assertEqual(inst.flow_type, FlowTypes.SubroutineReturn)

    def test_90_92_94_96_decw_regpair(self):
        d = {0x90: "decw ax", 0x92: "decw bc",
             0x94: "decw de", 0x96: "decw hl"}

        for opcode, expected_inst in d.items():
            mem = [opcode]
            inst = disassemble(mem, pc=0)
            self.assertEqual(str(inst), expected_inst)
            self.assertEqual(len(inst), len(mem))
        self.assertEqual(inst.flow_type, FlowTypes.Continue)

    def test_91_dec_saddr(self):
        for saddr in range(0xfe20, 0xff20):
            saddr_low = saddr & 0xff
            mem = [0x91, saddr_low]
            inst = disassemble(mem, pc=0)
            self.assertEqual(str(inst), "dec 0x%04x" % saddr)
            self.assertEqual(len(inst), len(mem))
            self.assertEqual(inst.flow_type, FlowTypes.Continue)

    def test_93_xch_a_sfr(self):
        for sfr in range(0xff00, 0x10000):
            sfr_low = sfr & 0xff
            mem = [0x93, sfr_low]
            inst = disassemble(mem, pc=0)
            self.assertEqual(str(inst), "xch a,0x%04x" % sfr)
            self.assertEqual(len(inst), len(mem))
            self.assertEqual(inst.flow_type, FlowTypes.Continue)

    def test_95_mov_de_a(self):
        mem = [0x95]
        inst = disassemble(mem, pc=0)
        self.assertEqual(str(inst), "mov [de],a")
        self.assertEqual(len(inst), len(mem))
        self.assertEqual(inst.flow_type, FlowTypes.Continue)

    def test_97_mov_hl_a(self):
        mem = [0x97]
        inst = disassemble(mem, pc=0)
        self.assertEqual(str(inst), "mov [hl],a")
        self.assertEqual(len(inst), len(mem))
        self.assertEqual(inst.flow_type, FlowTypes.Continue)

    def test_98_sub_saddr_imm8(self):
        for saddr in range(0xfe20, 0xff20):
            saddr_low = saddr & 0xff
            mem = [0x98, saddr_low, 0xab]
            inst = disassemble(mem, pc=0)
            self.assertEqual(str(inst), "sub 0x%04x,#0xab" % saddr)
            self.assertEqual(len(inst), len(mem))
            self.assertEqual(inst.flow_type, FlowTypes.Continue)

    def test_9a_call_addr16(self):
        for addr16 in (0x0000, 0xabcd, 0xffff):
            low = addr16 & 0xff
            high = (addr16 >> 8) & 0xff
            mem = [0x9a, low, high]
            inst = disassemble(mem, pc=0)
            self.assertEqual(str(inst), 'call !0x%04x' % addr16)
            self.assertEqual(len(inst), len(mem))
            self.assertEqual(inst.flow_type, FlowTypes.SubroutineCall)

    def test_9b_br_addr16(self):
        for addr16 in (0x0000, 0xabcd, 0xffff):
            low = addr16 & 0xff
            high = (addr16 >> 8) & 0xff
            mem = [0x9b, low, high]
            inst = disassemble(mem, pc=0)
            self.assertEqual(str(inst), 'br !0x%04x' % addr16)
            self.assertEqual(len(inst), len(mem))
            self.assertEqual(inst.flow_type, FlowTypes.UnconditionalJump)

    def test_9d_bnc_rel(self):
        mem = bytearray(0x2000)
        code = [0x9d, 0xfe]
        for address, c in enumerate(code, 0x1000):
            mem[address] = c
        inst = disassemble(mem, pc=0x1000)
        self.assertEqual(str(inst), "bnc 0x1000")
        self.assertEqual(len(inst), len(code))
        self.assertEqual(inst.flow_type, FlowTypes.ConditionalJump)

    def test_9e_mov_addr16_a(self):
        for addr16 in (0x0000, 0xabcd, 0xffff):
            low = addr16 & 0xff
            high = (addr16 >> 8) & 0xff
            mem = [0x9e, low, high]
            inst = disassemble(mem, pc=0)
            self.assertEqual(str(inst), 'mov !0x%04x,a' % addr16)
            self.assertEqual(len(inst), len(mem))
            self.assertEqual(inst.flow_type, FlowTypes.Continue)

    def test_9f_retb(self):
        mem = [0x9F]
        inst = disassemble(mem, pc=0)
        self.assertEqual(str(inst), "retb")
        self.assertEqual(len(inst), len(mem))
        self.assertEqual(inst.flow_type, FlowTypes.SubroutineReturn)

    def test_a0_a7_mov_reg_imm8(self):
        d = {0xa0: 'mov x,#0x%02x', 0xa1: 'mov a,#0x%02x',
             0xa2: 'mov c,#0x%02x', 0xa3: 'mov b,#0x%02x',
             0xa4: 'mov e,#0x%02x', 0xa5: 'mov d,#0x%02x',
             0xa6: 'mov l,#0x%02x', 0xa7: 'mov h,#0x%02x'}

        for opcode, expected_inst_fmt in d.items():
            for imm8 in (0x00, 0xab, 0xff):
                mem = [opcode, imm8]
                inst = disassemble(mem, pc=0)
                self.assertEqual(str(inst), expected_inst_fmt % imm8)
                self.assertEqual(len(inst), len(mem))
                self.assertEqual(inst.flow_type, FlowTypes.Continue)

    def test_a8_addc_saddr_imm8(self):
        for saddr in range(0xfe20, 0xff20):
            saddr_low = saddr & 0xff
            mem = [0xa8, saddr_low, 0xab]
            inst = disassemble(mem, pc=0)
            self.assertEqual(str(inst), "addc 0x%04x,#0xab" % saddr)
            self.assertEqual(len(inst), len(mem))
            self.assertEqual(inst.flow_type, FlowTypes.Continue)

    def test_a9_movw_ax_sfrp(self):
        for sfrp in range(0xff00, 0x10000, 2):
            sfrp_low = sfrp & 0xff
            mem = [0xa9, sfrp_low]
            inst = disassemble(mem, pc=0)
            self.assertEqual(str(inst), "movw ax,0x%04x" % sfrp)
            self.assertEqual(len(inst), len(mem))
            self.assertEqual(inst.flow_type, FlowTypes.Continue)

    def test_a9_movw_ax_sfrp_raises_for_odd_address(self):
        mem = [0xa9, 0x01]
        with self.assertRaises(IllegalInstructionError):
            disassemble(mem, pc=0)

    def test_aa_mov_a_hl_plus_c(self):
        mem = [0xaa]
        inst = disassemble(mem, pc=0)
        self.assertEqual(str(inst), "mov a,[hl+c]")
        self.assertEqual(len(inst), len(mem))
        self.assertEqual(inst.flow_type, FlowTypes.Continue)

    def test_ab_mov_a_hl_plus_b(self):
        mem = [0xab]
        inst = disassemble(mem, pc=0)
        self.assertEqual(str(inst), "mov a,[hl+b]")
        self.assertEqual(len(inst), len(mem))
        self.assertEqual(inst.flow_type, FlowTypes.Continue)

    def test_ad_bz_rel(self):
        mem = bytearray(0x2000)
        code = [0xad, 0xfe]
        for address, c in enumerate(code, 0x1000):
            mem[address] = c
        inst = disassemble(mem, pc=0x1000)
        self.assertEqual(str(inst), "bz 0x1000")
        self.assertEqual(len(inst), len(code))
        self.assertEqual(inst.flow_type, FlowTypes.ConditionalJump)

    def test_ae_mov_a_hl_plus_byte(self):
        mem = [0xAE, 0xAB]
        inst = disassemble(mem, pc=0)
        self.assertEqual(str(inst), "mov a,[hl+0xab]")
        self.assertEqual(len(inst), len(mem))
        self.assertEqual(inst.flow_type, FlowTypes.Continue)

    def test_af_ret(self):
        mem = [0xAF]
        inst = disassemble(mem, pc=0)
        self.assertEqual(str(inst), "ret")
        self.assertEqual(len(inst), len(mem))
        self.assertEqual(inst.flow_type, FlowTypes.SubroutineReturn)

    def test_b0_b2_b4_b6_pop_regpair(self):
        d = {0xb0: "pop ax", 0xb2: "pop bc",
             0xb4: "pop de", 0xb6: "pop hl"}

        for opcode, expected_inst in d.items():
            mem = [opcode]
            inst = disassemble(mem, pc=0)
            self.assertEqual(str(inst), expected_inst)
            self.assertEqual(len(inst), len(mem))
            self.assertEqual(inst.flow_type, FlowTypes.Continue)

    def test_b1_b3_b5_b7_push_regpair(self):
        d = {0xb1: "push ax", 0xb3: "push bc",
             0xb5: "push de", 0xb7: "push hl"}

        for opcode, expected_inst in d.items():
            mem = [opcode]
            inst = disassemble(mem, pc=0)
            self.assertEqual(str(inst), expected_inst)
            self.assertEqual(len(inst), len(mem))
            self.assertEqual(inst.flow_type, FlowTypes.Continue)

    def test_b8_subc_saddr_imm8(self):
        for saddr in range(0xfe20, 0xff20):
            saddr_low = saddr & 0xff
            mem = [0xb8, saddr_low, 0xab]
            inst = disassemble(mem, pc=0)
            self.assertEqual(str(inst), "subc 0x%04x,#0xab" % saddr)
            self.assertEqual(len(inst), len(mem))
            self.assertEqual(inst.flow_type, FlowTypes.Continue)

    def test_b9_movw_sfrp_ax(self):
        for sfrp in range(0xff00, 0x10000, 2):
            sfrp_low = sfrp & 0xff
            mem = [0xb9, sfrp_low]
            inst = disassemble(mem, pc=0)
            self.assertEqual(str(inst), "movw 0x%04x,ax" % sfrp)
            self.assertEqual(len(inst), len(mem))
            self.assertEqual(inst.flow_type, FlowTypes.Continue)

    def test_b9_movw_sfrp_ax_raises_for_odd_address(self):
        mem = [0xb9, 0x01]
        with self.assertRaises(IllegalInstructionError):
            disassemble(mem, pc=0)

    def test_ba_mov_hl_plus_c_a(self):
        mem = [0xBA]
        inst = disassemble(mem, pc=0)
        self.assertEqual(str(inst), "mov [hl+c],a")
        self.assertEqual(len(inst), len(mem))
        self.assertEqual(inst.flow_type, FlowTypes.Continue)

    def test_bb_mov_hl_plus_b_a(self):
        mem = [0xBB]
        inst = disassemble(mem, pc=0)
        self.assertEqual(str(inst), "mov [hl+b],a")
        self.assertEqual(len(inst), len(mem))
        self.assertEqual(inst.flow_type, FlowTypes.Continue)

    def test_bd_bnz_rel(self):
        mem = bytearray(0x2000)
        code = [0xbd, 0xfe]
        for address, c in enumerate(code, 0x1000):
            mem[address] = c
        inst = disassemble(mem, pc=0x1000)
        self.assertEqual(str(inst), "bnz 0x1000")
        self.assertEqual(len(inst), len(code))
        self.assertEqual(inst.flow_type, FlowTypes.ConditionalJump)

    def test_be_mov_hl_plus_byte_a(self):
        mem = [0xBE, 0xAB]
        inst = disassemble(mem, pc=0)
        self.assertEqual(str(inst), "mov [hl+0xab],a")
        self.assertEqual(len(inst), len(mem))
        self.assertEqual(inst.flow_type, FlowTypes.Continue)

    def test_bf_brk(self):
        mem = [0xBF]
        inst = disassemble(mem, pc=0)
        self.assertEqual(str(inst), "brk")
        self.assertEqual(len(inst), len(mem))
        self.assertEqual(inst.flow_type, FlowTypes.Stop)

    def test_c2_c4_c6_mov_ax_regpair(self):
        d = {0xc2: "movw ax,bc", 0xc4: "movw ax,de", 0xc6: "movw ax,hl"}

        for opcode, expected_inst in d.items():
            mem = [opcode]
            inst = disassemble(mem, pc=0)
            self.assertEqual(str(inst), expected_inst)
            self.assertEqual(len(inst), len(mem))
            self.assertEqual(inst.flow_type, FlowTypes.Continue)

    def test_c8_cmp_saddr_imm8(self):
        for saddr in range(0xfe20, 0xff20):
            saddr_low = saddr & 0xff
            mem = [0xc8, saddr_low, 0xab]
            inst = disassemble(mem, pc=0)
            self.assertEqual(str(inst), "cmp 0x%04x,#0xab" % saddr)
            self.assertEqual(len(inst), len(mem))
            self.assertEqual(inst.flow_type, FlowTypes.Continue)

    def test_ca_addw_ax_imm16(self):
        for imm16 in (0x0000, 0xabcd, 0xffff):
            high = (imm16 >> 8) & 0xff
            low = imm16 & 0xff
            mem = [0xca, low, high]
            inst = disassemble(mem, pc=0)
            self.assertEqual(str(inst), "addw ax,#0x%04x" % imm16)
            self.assertEqual(len(inst), len(mem))
            self.assertEqual(inst.flow_type, FlowTypes.Continue)

    def test_ce_xch_a_addr16(self):
        for addr16 in (0x0000, 0xabcd, 0xffff):
            low = addr16 & 0xff
            high = (addr16 >> 8) & 0xff
            mem = [0xce, low, high]
            inst = disassemble(mem, pc=0)
            self.assertEqual(str(inst), 'xch a,!0x%04x' % addr16)
            self.assertEqual(len(inst), len(mem))
            self.assertEqual(inst.flow_type, FlowTypes.Continue)

    def test_d2_d4_d6_mov_regpair(self):
        d = {0xd2: "movw bc,ax", 0xd4: "movw de,ax", 0xd6: "movw hl,ax"}

        for opcode, expected_inst in d.items():
            mem = [opcode]
            inst = disassemble(mem, pc=0)
            self.assertEqual(str(inst), expected_inst)
            self.assertEqual(len(inst), len(mem))
            self.assertEqual(inst.flow_type, FlowTypes.Continue)

    def test_d8_and_saddr_imm8(self):
        for saddr in range(0xfe20, 0xff20):
            saddr_low = saddr & 0xff
            mem = [0xd8, saddr_low, 0xab]
            inst = disassemble(mem, pc=0)
            self.assertEqual(str(inst), "and 0x%04x,#0xab" % saddr)
            self.assertEqual(len(inst), len(mem))
            self.assertEqual(inst.flow_type, FlowTypes.Continue)

    def test_da_subw_ax_imm16(self):
        for imm16 in (0x0000, 0xabcd, 0xffff):
            high = (imm16 >> 8) & 0xff
            low = imm16 & 0xff
            mem = [0xda, low, high]
            inst = disassemble(mem, pc=0)
            self.assertEqual(str(inst), "subw ax,#0x%04x" % imm16)
            self.assertEqual(len(inst), len(mem))
            self.assertEqual(inst.flow_type, FlowTypes.Continue)

    def test_de_xch_a_hl_plus_byte(self):
        mem = [0xde, 0xab]
        inst = disassemble(mem, pc=0)
        self.assertEqual(str(inst), "xch a,[hl+0xab]")
        self.assertEqual(len(inst), len(mem))
        self.assertEqual(inst.flow_type, FlowTypes.Continue)

    def test_e2_e4_e6_xchw_ax_regpair(self):
        d = {0xe2: "xchw ax,bc", 0xe4: "xchw ax,de", 0xe6: "xchw ax,hl"}

        for opcode, expected_inst in d.items():
            mem = [opcode]
            inst = disassemble(mem, pc=0)
            self.assertEqual(str(inst), expected_inst)
            self.assertEqual(len(inst), len(mem))
            self.assertEqual(inst.flow_type, FlowTypes.Continue)

    def test_e8_or_saddr_imm8(self):
        for saddr in range(0xfe20, 0xff20):
            saddr_low = saddr & 0xff
            mem = [0xe8, saddr_low, 0xab]
            inst = disassemble(mem, pc=0)
            self.assertEqual(str(inst), "or 0x%04x,#0xab" % saddr)
            self.assertEqual(len(inst), len(mem))
            self.assertEqual(inst.flow_type, FlowTypes.Continue)

    def test_ea_cmpw_ax_imm16(self):
        for imm16 in (0x0000, 0xabcd, 0xffff):
            high = (imm16 >> 8) & 0xff
            low = imm16 & 0xff
            mem = [0xea, low, high]
            inst = disassemble(mem, pc=0)
            self.assertEqual(str(inst), "cmpw ax,#0x%04x" % imm16)
            self.assertEqual(len(inst), len(mem))
            self.assertEqual(inst.flow_type, FlowTypes.Continue)

    def test_f4_mov_a_sfr(self):
        for sfr in range(0xff00, 0x10000):
            sfr_low = sfr & 0xff
            mem = [0xf4, sfr_low]
            inst = disassemble(mem, pc=0)
            self.assertEqual(str(inst), "mov a,0x%04x" % sfr)
            self.assertEqual(len(inst), len(mem))
            self.assertEqual(inst.flow_type, FlowTypes.Continue)

    def test_f6_mov_sfr_a(self):
        for sfr in range(0xff00, 0x10000):
            sfr_low = sfr & 0xff
            mem = [0xf6, sfr_low]
            inst = disassemble(mem, pc=0)
            self.assertEqual(str(inst), "mov 0x%04x,a" % sfr)
            self.assertEqual(len(inst), len(mem))
            self.assertEqual(inst.flow_type, FlowTypes.Continue)

    def test_f8_xor_saddr_imm8(self):
        for saddr in range(0xfe20, 0xff20):
            saddr_low = saddr & 0xff
            mem = [0xf8, saddr_low, 0xab]
            inst = disassemble(mem, pc=0)
            self.assertEqual(str(inst), "xor 0x%04x,#0xab" % saddr)
            self.assertEqual(len(inst), len(mem))
            self.assertEqual(inst.flow_type, FlowTypes.Continue)

    def test_fe_movw_sfrp_imm16(self):
        for sfrp in range(0xff00, 0x10000, 2):
            sfrp_low = sfrp & 0xff
            mem = [0xfe, sfrp_low, 0xcd, 0xab]
            inst = disassemble(mem, pc=0)
            self.assertEqual(str(inst), "movw 0x%04x,#0xabcd" % sfrp)
            self.assertEqual(len(inst), len(mem))
            self.assertEqual(inst.flow_type, FlowTypes.Continue)

    def test_fe_movw_sfrp_imm16_raises_for_odd_address(self):
        mem = [0xfe, 0x01, 0xcd, 0xab]
        with self.assertRaises(IllegalInstructionError):
            disassemble(mem, pc=0)

    def test_fa_br_rel(self):
        mem = bytearray(0x2000)
        code = [0xfa, 0xfe]
        for address, c in enumerate(code, 0x1000):
            mem[address] = c
        inst = disassemble(mem, pc=0x1000)
        self.assertEqual(str(inst), "br 0x1000")
        self.assertEqual(len(inst), len(code))
        self.assertEqual(inst.flow_type, FlowTypes.UnconditionalJump)

    def test_0a_thru_6a_set1_psw(self):
        opcodes = (0x0a, 0x1a, 0x2a, 0x3a, 0x4a, 0x5a, 0x6a)
        for bit, opcode in enumerate(opcodes):
            mem = [opcode, 0x1e]
            inst = disassemble(mem, pc=0)
            self.assertEqual(str(inst), "set1 psw.%d" % bit)
            self.assertEqual(len(inst), len(mem))
            self.assertEqual(inst.flow_type, FlowTypes.Continue)

    def test_11_1e_mov_psw_imm8(self):
        mem = [0x11, 0x1e, 0xab]
        inst = disassemble(mem, pc=0)
        self.assertEqual(str(inst), "mov psw,#0xab")
        self.assertEqual(len(inst), len(mem))
        self.assertEqual(inst.flow_type, FlowTypes.Continue)

    def test_11_xx_mov_saddr_imm8(self):
        for saddr in range(0xfe20, 0xff20):
            if saddr == 0xff1e:
                continue # special case; would disassemble as MOV PSW,#imm8
            saddr_low = saddr & 0xff
            mem = [0x11, saddr_low, 0xab]
            inst = disassemble(mem, pc=0)
            self.assertEqual(str(inst), "mov 0x%04x,#0xab" % (saddr))
            self.assertEqual(len(inst), len(mem))
            self.assertEqual(inst.flow_type, FlowTypes.Continue)

    def test_31_01_thru_71_btclr_saddr(self):
        opcodes = (0x01, 0x11, 0x21, 0x31, 0x41, 0x51, 0x61, 0x71)
        for bit, opcode in enumerate(opcodes):
            for saddr in range(0xfe20, 0xff20):
                if saddr == 0xff1e:
                    continue # special case; would disassemble as BTCLR PSW.x,$rel
                saddr_low = saddr & 0xff
                mem = bytearray(0x2000)
                code = [0x31, opcode, saddr_low, 0xfc]
                for address, c in enumerate(code, 0x1000):
                    mem[address] = c
                inst = disassemble(mem, pc=0x1000)
                self.assertEqual(str(inst), "btclr 0x%04x.%d,0x1000" % (saddr, bit))
                self.assertEqual(len(inst), len(code))
                self.assertEqual(inst.flow_type, FlowTypes.ConditionalJump)

    def test_31_01_thru_71_btclr_psw(self):
        opcodes = (0x01, 0x11, 0x21, 0x31, 0x41, 0x51, 0x61, 0x71)
        for bit, opcode in enumerate(opcodes):
            mem = bytearray(0x2000)
            code = [0x31, opcode, 0x1e, 0xfc]
            for address, c in enumerate(code, 0x1000):
                mem[address] = c
            inst = disassemble(mem, pc=0x1000)
            self.assertEqual(str(inst), "btclr psw.%d,0x1000" % bit)
            self.assertEqual(len(inst), len(code))
            self.assertEqual(inst.flow_type, FlowTypes.ConditionalJump)

    def test_31_03_thru_73_bf_saddr(self):
        opcodes = (0x03, 0x13, 0x23, 0x33, 0x43, 0x53, 0x63, 0x73)
        for bit, opcode in enumerate(opcodes):
            for saddr in range(0xfe20, 0xff20):
                if saddr == 0xff1e:
                    continue # special case; would disassemble as BF PSW.x,$rel
                saddr_low = saddr & 0xff
                mem = bytearray(0x2000)
                code = [0x31, opcode, saddr_low, 0xfc]
                for address, c in enumerate(code, 0x1000):
                    mem[address] = c
                inst = disassemble(mem, pc=0x1000)
                self.assertEqual(str(inst), "bf 0x%04x.%d,0x1000" % (saddr, bit))
                self.assertEqual(len(inst), len(code))
                self.assertEqual(inst.flow_type, FlowTypes.ConditionalJump)

    def test_31_03_thru_73_bf_psw(self):
        opcodes = (0x03, 0x13, 0x23, 0x33, 0x43, 0x53, 0x63, 0x73)
        for bit, opcode in enumerate(opcodes):
            mem = bytearray(0x2000)
            code = [0x31, opcode, 0x1e, 0xfc]
            for address, c in enumerate(code, 0x1000):
                mem[address] = c
            inst = disassemble(mem, pc=0x1000)
            self.assertEqual(str(inst), "bf psw.%d,0x1000" % bit)
            self.assertEqual(len(inst), len(code))
            self.assertEqual(inst.flow_type, FlowTypes.ConditionalJump)

    def test_31_05_thru_75_btclr_sfr(self):
        opcodes = (0x05, 0x15, 0x25, 0x35, 0x45, 0x55, 0x65, 0x75)
        for bit, opcode in enumerate(opcodes):
            for sfr in range(0xff00, 0x10000):
                sfr_low = sfr & 0xff
                mem = bytearray(0x2000)
                code = [0x31, opcode, sfr_low, 0xfc]
                for address, c in enumerate(code, 0x1000):
                    mem[address] = c
                inst = disassemble(mem, pc=0x1000)
                self.assertEqual(str(inst), "btclr 0x%04x.%d,0x1000" % (sfr, bit))
                self.assertEqual(len(inst), len(code))
                self.assertEqual(inst.flow_type, FlowTypes.ConditionalJump)

    def test_31_06_thru_76_bt_sfr(self):
        opcodes = (0x06, 0x16, 0x26, 0x36, 0x46, 0x56, 0x66, 0x76)
        for bit, opcode in enumerate(opcodes):
            for sfr in range(0xff00, 0x10000):
                sfr_low = sfr & 0xff
                mem = bytearray(0x2000)
                code = [0x31, opcode, sfr_low, 0xfc]
                for address, c in enumerate(code, 0x1000):
                    mem[address] = c
                inst = disassemble(mem, pc=0x1000)
                self.assertEqual(str(inst), "bt 0x%04x.%d,0x1000" % (sfr, bit))
                self.assertEqual(len(inst), len(code))
                self.assertEqual(inst.flow_type, FlowTypes.ConditionalJump)

    def test_31_07_thru_77_bf_sfr(self):
        opcodes = (0x07, 0x17, 0x27, 0x37, 0x47, 0x57, 0x67, 0x77)
        for bit, opcode in enumerate(opcodes):
            for sfr in range(0xff00, 0x10000):
                sfr_low = sfr & 0xff
                mem = bytearray(0x2000)
                code = [0x31, opcode, sfr_low, 0xfc]
                for address, c in enumerate(code, 0x1000):
                    mem[address] = c
                inst = disassemble(mem, pc=0x1000)
                self.assertEqual(str(inst), "bf 0x%04x.%d,0x1000" % (sfr, bit))
                self.assertEqual(len(inst), len(code))
                self.assertEqual(inst.flow_type, FlowTypes.ConditionalJump)

    def test_31_0a_add_a_hl_plus_c(self):
        mem = bytearray(0x2000)
        code = [0x31, 0x0a]
        for address, c in enumerate(code, 0x1000):
            mem[address] = c
        inst = disassemble(mem, pc=0x1000)
        self.assertEqual(str(inst), "add a,[hl+c]")
        self.assertEqual(len(inst), len(code))
        self.assertEqual(inst.flow_type, FlowTypes.Continue)

    def test_31_0b_add_a_hl_plus_b(self):
        mem = bytearray(0x2000)
        code = [0x31, 0x0b]
        for address, c in enumerate(code, 0x1000):
            mem[address] = c
        inst = disassemble(mem, pc=0x1000)
        self.assertEqual(str(inst), "add a,[hl+b]")
        self.assertEqual(len(inst), len(code))
        self.assertEqual(inst.flow_type, FlowTypes.Continue)

    def test_31_0d_thru_7d_btclr(self):
        opcodes = (0x0d, 0x1d, 0x2d, 0x3d, 0x4d, 0x5d, 0x6d, 0x7d)
        for bit, opcode in enumerate(opcodes):
            mem = bytearray(0x2000)
            code = [0x31, opcode, 0xfd]
            for address, c in enumerate(code, 0x1000):
                mem[address] = c
            inst = disassemble(mem, pc=0x1000)
            self.assertEqual(str(inst), "btclr a.%d,0x1000" % bit)
            self.assertEqual(len(inst), len(code))
            self.assertEqual(inst.flow_type, FlowTypes.ConditionalJump)

    def test_31_85_thru_f5_btclr_hl(self):
        opcodes = (0x85, 0x95, 0xa5, 0xb5, 0xc5, 0xd5, 0xe5, 0xf5)
        for bit, opcode in enumerate(opcodes):
            mem = bytearray(0x2000)
            code = [0x31, opcode, 0xfd]
            for address, c in enumerate(code, 0x1000):
                mem[address] = c
            inst = disassemble(mem, pc=0x1000)
            self.assertEqual(str(inst), "btclr [hl].%d,0x1000" % bit)
            self.assertEqual(len(inst), len(code))
            self.assertEqual(inst.flow_type, FlowTypes.ConditionalJump)

    def test_31_86_thru_f6_bt_hl(self):
        opcodes = (0x86, 0x96, 0xa6, 0xb6, 0xc6, 0xd6, 0xe6, 0xf6)
        for bit, opcode in enumerate(opcodes):
            mem = bytearray(0x2000)
            code = [0x31, opcode, 0xfd]
            for address, c in enumerate(code, 0x1000):
                mem[address] = c
            inst = disassemble(mem, pc=0x1000)
            self.assertEqual(str(inst), "bt [hl].%d,0x1000" % bit)
            self.assertEqual(len(inst), len(code))
            self.assertEqual(inst.flow_type, FlowTypes.ConditionalJump)

    def test_31_87_thru_f7_bf_hl(self):
        opcodes = (0x87, 0x97, 0xa7, 0xb7, 0xc7, 0xd7, 0xe7, 0xf7)
        for bit, opcode in enumerate(opcodes):
            mem = bytearray(0x2000)
            code = [0x31, opcode, 0xfd]
            for address, c in enumerate(code, 0x1000):
                mem[address] = c
            inst = disassemble(mem, pc=0x1000)
            self.assertEqual(str(inst), "bf [hl].%d,0x1000" % bit)
            self.assertEqual(len(inst), len(code))
            self.assertEqual(inst.flow_type, FlowTypes.ConditionalJump)

    def test_31_0e_thru_7e_bt(self):
        opcodes = (0x0e, 0x1e, 0x2e, 0x3e, 0x4e, 0x5e, 0x6e, 0x7e)
        for bit, opcode in enumerate(opcodes):
            mem = bytearray(0x2000)
            code = [0x31, opcode, 0xfd]
            for address, c in enumerate(code, 0x1000):
                mem[address] = c
            inst = disassemble(mem, pc=0x1000)
            self.assertEqual(str(inst), "bt a.%d,0x1000" % bit)
            self.assertEqual(len(inst), len(code))
            self.assertEqual(inst.flow_type, FlowTypes.ConditionalJump)

    def test_31_0f_thru_7f_bt(self):
        opcodes = (0x0f, 0x1f, 0x2f, 0x3f, 0x4f, 0x5f, 0x6f, 0x7f)
        for bit, opcode in enumerate(opcodes):
            mem = bytearray(0x2000)
            code = [0x31, opcode, 0xfd]
            for address, c in enumerate(code, 0x1000):
                mem[address] = c
            inst = disassemble(mem, pc=0x1000)
            self.assertEqual(str(inst), "bf a.%d,0x1000" % bit)
            self.assertEqual(len(inst), len(code))
            self.assertEqual(inst.flow_type, FlowTypes.ConditionalJump)

    def test_31_1a_sub_a_hl_plus_c(self):
        mem = [0x31, 0x1a]
        inst = disassemble(mem, pc=0)
        self.assertEqual(str(inst), "sub a,[hl+c]")
        self.assertEqual(len(inst), len(mem))
        self.assertEqual(inst.flow_type, FlowTypes.Continue)

    def test_31_1b_sub_a_hl_plus_b(self):
        mem = [0x31, 0x1b]
        inst = disassemble(mem, pc=0)
        self.assertEqual(str(inst), "sub a,[hl+b]")
        self.assertEqual(len(inst), len(mem))
        self.assertEqual(inst.flow_type, FlowTypes.Continue)

    def test_31_2a_addc_a_hl_plus_c(self):
        mem = [0x31, 0x2a]
        inst = disassemble(mem, pc=0)
        self.assertEqual(str(inst), "addc a,[hl+c]")
        self.assertEqual(len(inst), len(mem))
        self.assertEqual(inst.flow_type, FlowTypes.Continue)

    def test_31_2b_addc_a_hl_plus_b(self):
        mem = [0x31, 0x2b]
        inst = disassemble(mem, pc=0)
        self.assertEqual(str(inst), "addc a,[hl+b]")
        self.assertEqual(len(inst), len(mem))
        self.assertEqual(inst.flow_type, FlowTypes.Continue)

    def test_31_3a_subc_a_hl_plus_c(self):
        mem = [0x31, 0x3a]
        inst = disassemble(mem, pc=0)
        self.assertEqual(str(inst), "subc a,[hl+c]")
        self.assertEqual(len(inst), len(mem))
        self.assertEqual(inst.flow_type, FlowTypes.Continue)

    def test_31_3b_subc_a_hl_plus_b(self):
        mem = [0x31, 0x3b]
        inst = disassemble(mem, pc=0)
        self.assertEqual(str(inst), "subc a,[hl+b]")
        self.assertEqual(len(inst), len(mem))
        self.assertEqual(inst.flow_type, FlowTypes.Continue)

    def test_31_4a_cmp_a_hl_plus_c(self):
        mem = [0x31, 0x4a]
        inst = disassemble(mem, pc=0)
        self.assertEqual(str(inst), "cmp a,[hl+c]")
        self.assertEqual(len(inst), len(mem))
        self.assertEqual(inst.flow_type, FlowTypes.Continue)

    def test_31_4b_cmp_a_hl_plus_b(self):
        mem = [0x31, 0x4b]
        inst = disassemble(mem, pc=0)
        self.assertEqual(str(inst), "cmp a,[hl+b]")
        self.assertEqual(len(inst), len(mem))
        self.assertEqual(inst.flow_type, FlowTypes.Continue)

    def test_31_5a_and_a_hl_plus_a(self):
        mem = [0x31, 0x5a]
        inst = disassemble(mem, pc=0)
        self.assertEqual(str(inst), "and a,[hl+c]")
        self.assertEqual(len(inst), len(mem))
        self.assertEqual(inst.flow_type, FlowTypes.Continue)

    def test_31_5b_and_a_hl_plus_b(self):
        mem = [0x31, 0x5b]
        inst = disassemble(mem, pc=0)
        self.assertEqual(str(inst), "and a,[hl+b]")
        self.assertEqual(len(inst), len(mem))
        self.assertEqual(inst.flow_type, FlowTypes.Continue)

    def test_31_6a_or_a_hl_plus_c(self):
        mem = [0x31, 0x6a]
        inst = disassemble(mem, pc=0)
        self.assertEqual(str(inst), "or a,[hl+c]")
        self.assertEqual(len(inst), len(mem))
        self.assertEqual(inst.flow_type, FlowTypes.Continue)

    def test_31_6b_or_a_hl_plus_b(self):
        mem = [0x31, 0x6b]
        inst = disassemble(mem, pc=0)
        self.assertEqual(str(inst), "or a,[hl+b]")
        self.assertEqual(len(inst), len(mem))
        self.assertEqual(inst.flow_type, FlowTypes.Continue)

    def test_31_7a_xor_a_hl_plus_c(self):
        mem = [0x31, 0x7a]
        inst = disassemble(mem, pc=0)
        self.assertEqual(str(inst), "xor a,[hl+c]")
        self.assertEqual(len(inst), len(mem))
        self.assertEqual(inst.flow_type, FlowTypes.Continue)

    def test_31_7b_xor_a_hl_plus_b(self):
        mem = [0x31, 0x7b]
        inst = disassemble(mem, pc=0)
        self.assertEqual(str(inst), "xor a,[hl+b]")
        self.assertEqual(len(inst), len(mem))
        self.assertEqual(inst.flow_type, FlowTypes.Continue)

    def test_31_8a_xch_a_hl_plus_c(self):
        mem = [0x31, 0x8a]
        inst = disassemble(mem, pc=0)
        self.assertEqual(str(inst), "xch a,[hl+c]")
        self.assertEqual(len(inst), len(mem))
        self.assertEqual(inst.flow_type, FlowTypes.Continue)

    def test_31_8b_xch_a_hl_plus_b(self):
        mem = [0x31, 0x8b]
        inst = disassemble(mem, pc=0)
        self.assertEqual(str(inst), "xch a,[hl+b]")
        self.assertEqual(len(inst), len(mem))
        self.assertEqual(inst.flow_type, FlowTypes.Continue)

    def test_31_80_ror4_hl(self):
        mem = [0x31, 0x80]
        inst = disassemble(mem, pc=0)
        self.assertEqual(str(inst), "rol4 [hl]")
        self.assertEqual(len(inst), len(mem))
        self.assertEqual(inst.flow_type, FlowTypes.Continue)

    def test_31_82_mulu_x(self):
        mem = [0x31, 0x82]
        inst = disassemble(mem, pc=0)
        self.assertEqual(str(inst), "divuw c")
        self.assertEqual(len(inst), len(mem))
        self.assertEqual(inst.flow_type, FlowTypes.Continue)

    def test_31_88_mulu_x(self):
        mem = [0x31, 0x88]
        inst = disassemble(mem, pc=0)
        self.assertEqual(str(inst), "mulu x")
        self.assertEqual(len(inst), len(mem))
        self.assertEqual(inst.flow_type, FlowTypes.Continue)

    def test_31_90_ror4_hl(self):
        mem = [0x31, 0x90]
        inst = disassemble(mem, pc=0)
        self.assertEqual(str(inst), "ror4 [hl]")
        self.assertEqual(len(inst), len(mem))
        self.assertEqual(inst.flow_type, FlowTypes.Continue)

    def test_31_98_ror4_hl(self):
        mem = [0x31, 0x98]
        inst = disassemble(mem, pc=0)
        self.assertEqual(str(inst), "br ax")
        self.assertEqual(len(inst), len(mem))
        self.assertEqual(inst.flow_type, FlowTypes.Continue)

    def test_31_raises_for_illegal_second_opcode(self):
        mem = [0x31, 0x38]
        with self.assertRaises(IllegalInstructionError):
            disassemble(mem, pc=0)

    def test_7a_ei_alias_for_set1_psw_bit_7(self):
        mem = [0x7a, 0x1e]
        inst = disassemble(mem, pc=0)
        self.assertEqual(str(inst), "ei")
        self.assertEqual(len(inst), len(mem))
        self.assertEqual(inst.flow_type, FlowTypes.Continue)

    def test_set1_saddr(self):
        opcodes = (0x0a, 0x1a, 0x2a, 0x3a, 0x4a, 0x5a, 0x6a, 0x7a)
        for bit, opcode in enumerate(opcodes):
            for saddr in range(0xfe20, 0xff20):
                if saddr == 0xff1e:
                    continue # special case; would disassemble as SET1 PSW.x
                saddr_low = saddr & 0xff
                mem = [opcode, saddr_low]
                inst = disassemble(mem, pc=0)
                self.assertEqual(str(inst), "set1 0x%04x.%d" % (saddr, bit))
                self.assertEqual(len(inst), len(mem))
                self.assertEqual(inst.flow_type, FlowTypes.Continue)

    def test_0b_thru_06b_clr1_psw(self):
        opcodes = (0x0b, 0x1b, 0x2b, 0x3b, 0x4b, 0x5b, 0x6b)
        for bit, opcode in enumerate(opcodes):
            mem = [opcode, 0x1e]
            inst = disassemble(mem, pc=0)
            self.assertEqual(str(inst), "clr1 psw.%d" % bit)
            self.assertEqual(len(inst), len(mem))
            self.assertEqual(inst.flow_type, FlowTypes.Continue)

    def test_7b_di_alias_for_set1_psw_bit_7(self):
        mem = [0x7b, 0x1e]
        inst = disassemble(mem, pc=0)
        self.assertEqual(str(inst), "di")
        self.assertEqual(len(inst), len(mem))
        self.assertEqual(inst.flow_type, FlowTypes.Continue)

    def test_0b_thru_7b_clr1_saddr(self):
        opcodes = (0x0b, 0x1b, 0x2b, 0x3b, 0x4b, 0x5b, 0x6b, 0x7b)
        for bit, opcode in enumerate(opcodes):
            for saddr in range(0xfe20, 0xff20):
                if saddr == 0xff1e:
                    continue # special case; would disassemble as CLR1 PSW.x
                saddr_low = saddr & 0xff
                mem = [opcode, saddr_low]
                inst = disassemble(mem, pc=0)
                self.assertEqual(str(inst), "clr1 0x%04x.%d" % (saddr, bit))
                self.assertEqual(len(inst), len(mem))
                self.assertEqual(inst.flow_type, FlowTypes.Continue)

    def test_89_1c_movw_ax_sp(self):
        mem = [0x89, 0x1c]
        inst = disassemble(mem, pc=0)
        self.assertEqual(str(inst), "movw ax,sp")
        self.assertEqual(len(inst), len(mem))
        self.assertEqual(inst.flow_type, FlowTypes.Continue)

    def test_89_xx_movw_ax_saddrp(self):
        for saddrp in range(0xfe20, 0xff20, 2):
            if saddrp == 0xff1c:
                continue # special case; would disassemble as MOVW AX,SP
            saddrp_low = saddrp & 0xff
            mem = [0x89, saddrp_low]
            inst = disassemble(mem, pc=0)
            self.assertEqual(str(inst), "movw ax,0x%04x" % saddrp)
            self.assertEqual(len(inst), len(mem))
            self.assertEqual(inst.flow_type, FlowTypes.Continue)

    def test_89_xx_movw_ax_saddrp_raises_for_odd_address(self):
        mem = [0x89, 0x01]
        with self.assertRaises(IllegalInstructionError):
            disassemble(mem, pc=0)

    def test_bt_psw_bit_rel(self):
        opcodes = (0x8c, 0x9c, 0xac, 0xbc, 0xcc, 0xdc, 0xec, 0xfc)
        for bit, opcode in enumerate(opcodes):
            mem = bytearray(0x2000)
            code = [opcode, 0x1e, 0xfd]
            for address, c in enumerate(code, 0x1000):
                mem[address] = c
            inst = disassemble(mem, pc=0x1000)
            self.assertEqual(str(inst), "bt psw.%d,0x1000" % bit)
            self.assertEqual(len(inst), len(code))
            self.assertEqual(inst.flow_type, FlowTypes.ConditionalJump)

    def test_bt_saddr_bit_rel(self):
        opcodes = (0x8c, 0x9c, 0xac, 0xbc, 0xcc, 0xdc, 0xec, 0xfc)
        for bit, opcode in enumerate(opcodes):
            for saddr in range(0xfe20, 0xff20):
                if saddr == 0xff1e:
                    continue # special case; would disassemble as BT PSW.bit,rel
                saddr_low = saddr & 0xff
                mem = bytearray(0x2000)
                code = [opcode, saddr_low, 0xfd]
                for address, c in enumerate(code, 0x1000):
                    mem[address] = c
                inst = disassemble(mem, pc=0x1000)
                self.assertEqual(str(inst), "bt 0x%04x.%d,0x1000" % (saddr, bit))
                self.assertEqual(inst.flow_type, FlowTypes.ConditionalJump)

    def test_99_1c_movw_sp_ax(self):
        mem = [0x99, 0x1c]
        inst = disassemble(mem, pc=0)
        self.assertEqual(str(inst), "movw sp,ax")
        self.assertEqual(len(inst), len(mem))
        self.assertEqual(inst.flow_type, FlowTypes.Continue)

    def test_99_xx_movw_saddrp_ax(self):
        for saddrp in range(0xfe20, 0xff20, 2):
            if saddrp == 0xff1c:
                continue # special case; would disassemble as MOVW AX,SP
            saddrp_low = saddrp & 0xff
            mem = [0x99, saddrp_low]
            inst = disassemble(mem, pc=0)
            self.assertEqual(str(inst), "movw 0x%04x,ax" % saddrp)
            self.assertEqual(len(inst), len(mem))
            self.assertEqual(inst.flow_type, FlowTypes.Continue)

    def test_99_xx_movw_saddrp_ax_raises_for_odd_address(self):
        mem = [0x99, 0x01]
        with self.assertRaises(IllegalInstructionError):
            disassemble(mem, pc=0)

    def test_ee_1c_movw_sp_imm16(self):
        mem = [0xee, 0x1c, 0xcd, 0xab]
        inst = disassemble(mem, pc=0)
        self.assertEqual(str(inst), "movw sp,#0xabcd")
        self.assertEqual(len(inst), len(mem))
        self.assertEqual(inst.flow_type, FlowTypes.Continue)

    def test_ee_xx_movw_saddrp_imm16(self):
        for saddrp in range(0xfe20, 0xff20, 2):
            if saddrp == 0xff1c:
                continue # special case; would disassemble as MOVW SP,#imm16
            saddrp_low = saddrp & 0xff
            mem = [0xee, saddrp_low, 0xcd, 0xab]
            inst = disassemble(mem, pc=0)
            self.assertEqual(str(inst), "movw 0x%04x,#0xabcd" % saddrp)
            self.assertEqual(len(inst), len(mem))
            self.assertEqual(inst.flow_type, FlowTypes.Continue)

    def test_ee_xx_movw_saddrp_imm16_raise_for_odd_address(self):
        mem = [0xee, 0x01, 0xcd, 0xab]
        with self.assertRaises(IllegalInstructionError):
            disassemble(mem, pc=0)

    def test_f0_e1_mov_a_psw(self):
        mem = [0xf0, 0x1e]
        inst = disassemble(mem, pc=0)
        self.assertEqual(str(inst), "mov a,psw")
        self.assertEqual(len(inst), len(mem))
        self.assertEqual(inst.flow_type, FlowTypes.Continue)

    def test_f0_xx_mov_a_saddr(self):
        for saddr in range(0xfe20, 0xff20):
            if saddr == 0xff1e:
                continue # special case; would disassemble as MOV A,PSW
            saddr_low = saddr & 0xff
            mem = [0xf0, saddr_low]
            inst = disassemble(mem, pc=0)
            self.assertEqual(str(inst), "mov a,0x%04x" % saddr)
            self.assertEqual(len(inst), len(mem))
            self.assertEqual(inst.flow_type, FlowTypes.Continue)

    def test_f2_e1_mov_psw_a(self):
        mem = [0xf2, 0x1e]
        inst = disassemble(mem, pc=0)
        self.assertEqual(str(inst), "mov psw,a")
        self.assertEqual(len(inst), len(mem))
        self.assertEqual(inst.flow_type, FlowTypes.Continue)

    def test_f2_xx_mov_a_saddr(self):
        for saddr in range(0xfe20, 0xff20):
            if saddr == 0xff1e:
                continue # special case; would disassemble as MOV PSW,A
            saddr_low = saddr & 0xff
            mem = [0xf2, saddr_low]
            inst = disassemble(mem, pc=0)
            self.assertEqual(str(inst), "mov 0x%04x,a" % saddr)
            self.assertEqual(len(inst), len(mem))
            self.assertEqual(inst.flow_type, FlowTypes.Continue)

    def test_illegals(self):
        for opcode in (0x06, 0x15, 0x17, 0xc0, 0xd0, 0xe0):
            mem = [opcode]
            with self.assertRaises(IllegalInstructionError):
                disassemble(mem, pc=0)


def test_suite():
    return unittest.findTestCases(sys.modules[__name__])

if __name__ == '__main__':
    unittest.main(defaultTest='test_suite')
