"""Encode and decode variable-sized little-endian instructions."""
from instructions import (
    ADDRESS_BITS, ADDRESS_LIMIT, C_OFFSET, CONSTANT_BITS,
    Instruction, OPCODE_BITS, OP_LOAD, SIZES,
)

BYTE_LIMIT = 1 << OPCODE_BITS


def encode(instruction):
    """Pack A at bit 0, B at bit 8 and C at bit 18."""
    value = (instruction.a | (instruction.b << OPCODE_BITS)
             | (instruction.c << C_OFFSET))
    return value.to_bytes(SIZES[instruction.a], "little")


def decode_at(memory, position, end):
    """Fetch from unified memory and reject malformed instruction bytes."""
    if not 0 <= position < end <= len(memory):
        raise ValueError("Instruction pointer outside program")
    opcode = memory[position]
    if type(opcode) is not int or opcode not in SIZES:
        raise ValueError(f"Unknown opcode at {position}: {opcode}")
    size = SIZES[opcode]
    if position + size > end:
        raise ValueError(f"Truncated instruction at {position}")
    data = memory[position:position + size]
    if any(type(x) is not int or not 0 <= x < BYTE_LIMIT for x in data):
        raise ValueError(f"Non-byte instruction data at {position}")
    value = int.from_bytes(bytes(data), "little")
    c_bits = CONSTANT_BITS if opcode == OP_LOAD else ADDRESS_BITS
    if value >> (C_OFFSET + c_bits):
        raise ValueError(f"Nonzero reserved bits at {position}")
    b = (value >> OPCODE_BITS) & (ADDRESS_LIMIT - 1)
    c = value >> C_OFFSET
    return Instruction(opcode, b, c), position + size
