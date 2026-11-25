"""Memory operations, malformed programs and shared code/data behavior."""
from pathlib import Path
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from codec import encode
from machine import Machine
from parser import parse_program


def machine_for(source):
    """Assemble in memory without creating files."""
    return Machine(b"".join(encode(i) for i in parse_program(source)))


class MachineTests(unittest.TestCase):
    """Check semantics independently of the CLI."""

    def test_copy_array(self):
        path = Path(__file__).resolve().parents[1] / "examples/copy.asm"
        machine = machine_for(path.read_text())
        memory = machine.run()
        self.assertEqual(memory[512:515], [7, 11, 19])
        self.assertEqual(memory[600:603], [7, 11, 19])

    def test_read_has_indirection(self):
        machine = machine_for(
            "mem[700]=512\nmem[512]=42\nmem[600]=mem[mem[700]]"
        )
        self.assertEqual(machine.run()[600], 42)

    def test_invalid_indirect_address(self):
        machine = machine_for("mem[700]=2000\nmem[600]=mem[mem[700]]")
        with self.assertRaisesRegex(ValueError, "PC=5"):
            machine.run()

    def test_self_modifying_code_is_visible(self):
        machine = machine_for("mem[5]=255\nmem[512]=1")
        with self.assertRaisesRegex(ValueError, "Unknown opcode at 5"):
            machine.run()

    def test_dump_and_empty_program(self):
        machine = Machine(b"")
        machine.run()
        self.assertEqual(machine.dump(1023, 1023)["memory"], {"1023": 0})
        with self.assertRaises(ValueError):
            machine.dump(2, 1)
        with self.assertRaises(ValueError):
            Machine(bytes(1025))


if __name__ == "__main__":
    unittest.main()
