"""Independent byte-for-byte checks against the assignment."""
from pathlib import Path
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from codec import decode_at, encode
from instructions import Instruction

REFERENCE = [
    ((195, 164, 243), bytes.fromhex("C3 A4 CC 03 00")),
    ((6, 222, 704), bytes.fromhex("06 DE 00 0B")),
    ((104, 12, 29), bytes.fromhex("68 0C 74 00")),
    ((80, 491, 586), bytes.fromhex("50 EB 29 09")),
]


class CodecTests(unittest.TestCase):
    """Verify reference bytes, round trips and binary validation."""

    def test_reference_bytes(self):
        for fields, expected in REFERENCE:
            with self.subTest(fields=fields):
                instruction = Instruction(*fields)
                self.assertEqual(encode(instruction), expected)
                decoded, end = decode_at(expected, 0, len(expected))
                self.assertEqual(decoded, instruction)
                self.assertEqual(end, len(expected))

    def test_field_boundaries(self):
        for opcode, constant in ((195, 32767), (6, 1023),
                                 (104, 1023), (80, 1023)):
            instruction = Instruction(opcode, 1023, constant)
            data = encode(instruction)
            self.assertEqual(decode_at(data, 0, len(data))[0], instruction)

    def test_malformed_binary(self):
        for data in (b"\xff", b"\x06", bytes.fromhex("06 00 00 F0")):
            with self.subTest(data=data):
                with self.assertRaises(ValueError):
                    decode_at(data, 0, len(data))


if __name__ == "__main__":
    unittest.main()
