"""Instruction fields and bit layout of virtual machine variant 24."""
from dataclasses import dataclass

OP_LOAD = 195
OP_READ = 6
OP_WRITE = 104
OP_SQRT = 80
ADDRESS_BITS = 10
CONSTANT_BITS = 15
ADDRESS_LIMIT = 1 << ADDRESS_BITS
CONSTANT_LIMIT = 1 << CONSTANT_BITS
OPCODE_BITS = 8
C_OFFSET = OPCODE_BITS + ADDRESS_BITS
SIZES = {OP_LOAD: 5, OP_READ: 4, OP_WRITE: 4, OP_SQRT: 4}


@dataclass(frozen=True)
class Instruction:
    """The A, B and C fields from the assignment specification."""

    a: int
    b: int
    c: int

    def __post_init__(self):
        """Reject unsupported opcodes and out-of-range unsigned fields."""
        if self.a not in SIZES:
            raise ValueError(f"Unknown opcode: {self.a}")
        if not 0 <= self.b < ADDRESS_LIMIT:
            raise ValueError(f"B must be in 0..{ADDRESS_LIMIT - 1}")
        limit = CONSTANT_LIMIT if self.a == OP_LOAD else ADDRESS_LIMIT
        if not 0 <= self.c < limit:
            raise ValueError(f"C must be in 0..{limit - 1}")

    def fields(self):
        """Format the fields in the same order as the reference tests."""
        return f"A={self.a}, B={self.b}, C={self.c}"
