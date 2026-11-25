"""Unified instruction/data memory and the execution loop."""
import math

from codec import decode_at
from instructions import ADDRESS_LIMIT, OP_LOAD, OP_READ, OP_SQRT, OP_WRITE


class Machine:
    """Execute sequential instructions in 1024 numeric memory cells."""

    def __init__(self, program):
        """Load program bytes into the beginning of unified memory."""
        if len(program) > ADDRESS_LIMIT:
            raise ValueError("Program exceeds unified memory capacity")
        self.memory = [0] * ADDRESS_LIMIT
        self.memory[:len(program)] = program
        self.end = len(program)
        self.position = 0
        self.executed = 0

    def address(self, value):
        """Check an indirect pointer before indexing memory."""
        if type(value) not in (int, float) or not math.isfinite(value):
            raise ValueError(f"Invalid memory pointer: {value}")
        if int(value) != value or not 0 <= value < ADDRESS_LIMIT:
            raise ValueError(f"Memory pointer outside 0..1023: {value}")
        return int(value)

    def execute(self, instruction):
        """Execute a memory operation or square root of an indirect value."""
        a, b, c = instruction.a, instruction.b, instruction.c
        if a == OP_LOAD:
            self.memory[b] = c
        elif a == OP_READ:
            pointer = self.address(self.memory[b])
            self.memory[c] = self.memory[pointer]
        elif a == OP_WRITE:
            self.memory[b] = self.memory[c]
        elif a == OP_SQRT:
            self.memory[b] = self.square_root(self.memory[c])
        else:
            raise ValueError(f"Unsupported opcode: {a}")

    def square_root(self, pointer):
        """Read an indirect operand and reject invalid real square roots."""
        value = self.memory[self.address(pointer)]
        if not math.isfinite(value) or value < 0:
            raise ValueError(f"sqrt requires a finite nonnegative value: {value}")
        return math.sqrt(value)

    def run(self):
        """Fetch each instruction from current memory until program end."""
        while self.position < self.end:
            try:
                instruction, following = decode_at(
                    self.memory, self.position, self.end
                )
                self.execute(instruction)
            except ValueError as error:
                raise ValueError(
                    f"PC={self.position}: {error}"
                ) from error
            self.position = following
            self.executed += 1
        return self.memory

    def dump(self, start, end):
        """Return an inclusive address range in JSON-compatible form."""
        if not 0 <= start <= end < ADDRESS_LIMIT:
            raise ValueError("Dump range must satisfy 0 <= start <= end < 1024")
        return {
            "start": start, "end": end,
            "memory": {str(i): self.memory[i] for i in range(start, end + 1)},
        }
