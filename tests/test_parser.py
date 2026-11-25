"""Checks of the algebraic syntax and reference instruction fields."""
from pathlib import Path
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from parser import parse_program


class ParserTests(unittest.TestCase):
    """Verify all instruction syntaxes and input diagnostics."""

    def test_reference_fields(self):
        path = Path(__file__).resolve().parents[1] / "examples/spec.asm"
        result = parse_program(path.read_text())
        fields = [(item.a, item.b, item.c) for item in result]
        self.assertEqual(fields, [
            (195, 164, 243), (6, 222, 704),
            (104, 12, 29), (80, 491, 586),
        ])

    def test_comments_and_spaces(self):
        result = parse_program("# comment\n mem [ 2 ] = 3 # value\n")
        self.assertEqual((result[0].b, result[0].c), (2, 3))

    def test_invalid_syntax_and_fields(self):
        for source in ("mem[1]=-1", "mem[1024]=0", "mem[1]=32768",
                       "mem[1]=sqrt(mem[2])", "unknown"):
            with self.subTest(source=source):
                with self.assertRaisesRegex(ValueError, "Line 1"):
                    parse_program(source)


if __name__ == "__main__":
    unittest.main()
