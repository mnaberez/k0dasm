
class Memory(object):
    def __init__(self, rom):
        self.contents = bytearray(rom) + bytearray(0x10000 - len(rom))
        self.instructions = {}
        self.types = {}
        self.annotations = {}

        for address in range(len(self.contents)):
            self.instructions[address] = None
            self.types[address] = LocationTypes.Unknown
            self.annotations[address] = set()

    def __len__(self):
        return len(self.contents)

    def __getitem__(self, address):
        if isinstance(address, slice):
            rng = _slice_to_range(address)
            return bytearray([ self.contents[a] for a in rng ])
        return self.contents[address]

    def read_byte(self, address):
        return self.contents[address]

    def read_word(self, address):
        high = self.contents[(address + 1) & 0xFFFF]
        low = self.contents[address]
        return (high << 8) + low

    # Instruction Storage

    def set_instruction(self, address, inst):
        inst_len = len(inst)

        # ensure the memory locations are only assigned to one instruction
        for i in range(inst_len):
            addr = (address + i) & 0xFFFF
            if not self.is_unknown(addr):
                msg = "Attempt to overwrite non-unknown at %04x"
                raise Exception(msg % addr)

        # store instruction and mark its locations
        self.instructions[address] = inst
        for i in range(inst_len):
            addr = (address + i) & 0xFFFF
            if addr == address:
                loc_type = LocationTypes.InstructionStart
            else:
                loc_type = LocationTypes.InstructionContinuation
            self.types[addr] = loc_type

    def get_instruction(self, address):
        return self.instructions[address]

    def iter_instructions(self, address=0):
        for a in range(address, len(self.contents)):
            if self.types[a] == LocationTypes.InstructionStart:
                yield a, self.instructions[a]

    # Vector Storage

    def set_vector(self, address):
        self.types[address] = LocationTypes.VectorStart
        self.types[(address + 1) & 0xFFFF] = LocationTypes.VectorContinuation

    def get_vector(self, address):
        high = self.contents[address]
        low = self.contents[(address + 1) & 0xFFFF]
        return (high << 8) + low

    def iter_vectors(self, address=0):
        for a in range(address, len(self.contents)):
            if self.types[a] == LocationTypes.VectorStart:
                yield a, self.get_vector(a)

    # Data Storage

    def set_data(self, address):
        self.types[address] = LocationTypes.Data

    # Location Types

    def is_unknown(self, address, length=1):
        for i in range(length):
            if self.types[(address + i) & 0xFFFF] != LocationTypes.Unknown:
                return False
        return True

    def is_data(self, address):
        return self.types[address] == LocationTypes.Data

    def is_instruction_start(self, address):
        return self.types[address] == LocationTypes.InstructionStart

    def is_instruction_continuation(self, address):
        return self.types[address] == LocationTypes.InstructionContinuation

    def is_vector_start(self, address):
        return self.types[address] == LocationTypes.VectorStart

    def is_vector_continuation(self, address):
        return self.types[address] == LocationTypes.VectorContinuation

    # Location Types (single- or multi-byte inquiry)

    def is_single_byte_or_start_of_multibyte(self, address):
        return not self.is_continuation_of_multibyte_type(address)

    def is_continuation_of_multibyte_type(self, address):
        return self.types[address] in (
            LocationTypes.InstructionContinuation,
            LocationTypes.VectorContinuation,
            )

    # Location Annotations

    def annotate_entry_point(self, address):
        self.annotations[address].add(LocationAnnotations.EntryPoint)

    def annotate_jump_target(self, address):
        self.annotations[address].add(LocationAnnotations.JumpTarget)

    def annotate_call_target(self, address):
        self.annotations[address].add(LocationAnnotations.CallTarget)

    def annotate_illegal_instruction(self, address):
        self.annotations[address].add(LocationAnnotations.IllegalInstruction)

    def is_entry_point(self, address):
        return LocationAnnotations.EntryPoint in self.annotations[address]

    def is_jump_target(self, address):
        return LocationAnnotations.JumpTarget in self.annotations[address]

    def is_call_target(self, address):
        return LocationAnnotations.CallTarget in self.annotations[address]

    def is_illegal_instruction(self, address):
        return LocationAnnotations.IllegalInstruction in self.annotations[address]


class LocationTypes(object):
    '''A memory location has exactly one type'''
    Unknown = 0
    Data = 1
    InstructionStart = 2
    InstructionContinuation = 3
    VectorStart = 4
    VectorContinuation = 5


class LocationAnnotations(object):
    '''A memory location can have zero or more annotations'''
    EntryPoint = 0
    JumpTarget = 1
    CallTarget = 2
    IllegalInstruction = 3


def _slice_to_range(slc):
    start, stop, step = slc.start, slc.stop, slc.step
    if start is None:
        start = 0
    if step is None:
        step = 1
    return range(start, stop, step)
