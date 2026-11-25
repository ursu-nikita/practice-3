"""Parse algebraic memory assignments into instruction objects."""
import re

from instructions import Instruction, OP_LOAD, OP_READ, OP_SQRT, OP_WRITE

PATTERNS = (
    (OP_SQRT, r"mem\[(\d+)\]=sqrt\(mem\[mem\[(\d+)\]\]\)"),
    (OP_READ, r"mem\[(\d+)\]=mem\[mem\[(\d+)\]\]"),
    (OP_WRITE, r"mem\[(\d+)\]=mem\[(\d+)\]"),
    (OP_LOAD, r"mem\[(\d+)\]=(\d+)"),
)


def parse_line(line):
    """Parse one expression, ignoring whitespace and trailing comments."""
    expression = re.sub(r"\s+", "", line.split("#", 1)[0])
    if not expression:
        return None
    for opcode, pattern in PATTERNS:
        match = re.fullmatch(pattern, expression)
        if match:
            destination, operand = map(int, match.groups())
            if opcode == OP_READ:
                return Instruction(opcode, operand, destination)
            return Instruction(opcode, destination, operand)
    raise ValueError(f"Invalid expression: {line.strip()}")


def parse_program(source):
    """Translate a complete source with line-numbered diagnostics."""
    instructions = []
    for number, line in enumerate(source.splitlines(), 1):
        try:
            instruction = parse_line(line)
        except ValueError as error:
            raise ValueError(f"Line {number}: {error}") from error
        if instruction is not None:
            instructions.append(instruction)
    return instructions
