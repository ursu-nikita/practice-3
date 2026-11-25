"""ALU square-root behavior and indirect-address validation."""
import math
import unittest

from test_machine import machine_for


class SquareRootTests(unittest.TestCase):
    """Check exact, fractional and invalid operands."""

    def test_roots(self):
        for value in (0, 1, 2, 9, 32767):
            with self.subTest(value=value):
                machine = machine_for(
                    f"mem[512]={value}\nmem[700]=512\n"
                    "mem[600]=sqrt(mem[mem[700]])"
                )
                memory = machine.run()
                self.assertAlmostEqual(memory[600], math.sqrt(value))
                self.assertEqual(memory[512], value)

    def test_in_place_root(self):
        machine = machine_for(
            "mem[512]=16\nmem[700]=512\n"
            "mem[512]=sqrt(mem[mem[700]])"
        )
        self.assertEqual(machine.run()[512], 4.0)

    def test_invalid_values(self):
        for value in (-1, float("inf"), float("nan")):
            with self.subTest(value=value):
                machine = machine_for(
                    "mem[700]=512\nmem[600]=sqrt(mem[mem[700]])"
                )
                machine.memory[512] = value
                with self.assertRaisesRegex(ValueError, "sqrt requires"):
                    machine.run()

    def test_fractional_and_negative_pointer(self):
        for value in (1.5, -1, float("nan")):
            machine = machine_for("mem[600]=sqrt(mem[mem[700]])")
            machine.memory[700] = value
            with self.assertRaises(ValueError):
                machine.run()


if __name__ == "__main__":
    unittest.main()
