"""End-to-end tests through the assembler and interpreter CLIs."""
import json
import math
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
DATASETS = {
    "vector_squares": [0, 1, 4, 9, 16, 25, 36, 49, 64],
    "vector_fractional": [2, 3, 5, 7, 10, 11, 13, 17, 19],
    "vector_large": [81, 100, 121, 144, 169, 196, 225, 256, 289],
}


class VectorTests(unittest.TestCase):
    """Check nine-element results from real generated machine code."""

    def test_three_datasets(self):
        with tempfile.TemporaryDirectory() as directory:
            binary = Path(directory) / "program.bin"
            dump = Path(directory) / "dump.json"
            for name, values in DATASETS.items():
                with self.subTest(name=name):
                    self.run_example(name, binary, dump)
                    actual = json.loads(dump.read_text())["memory"]
                    self.assertEqual(list(actual),
                                     [str(i) for i in range(512, 521)])
                    for i, value in enumerate(values):
                        self.assertAlmostEqual(actual[str(512 + i)],
                                               math.sqrt(value))

    def run_example(self, name, binary, dump):
        """Invoke both programs with isolated output files."""
        subprocess.run(
            [sys.executable, str(ROOT / "src/assembler.py"),
             str(ROOT / "examples" / f"{name}.asm"), str(binary)],
            check=True, capture_output=True,
        )
        subprocess.run(
            [sys.executable, str(ROOT / "src/interpreter.py"),
             str(binary), str(dump), "--start", "512", "--end", "520"],
            check=True, capture_output=True,
        )

    def test_cli_errors(self):
        with tempfile.TemporaryDirectory() as directory:
            binary = Path(directory) / "broken.bin"
            dump = Path(directory) / "dump.json"
            binary.write_bytes(b"\xff")
            result = subprocess.run(
                [sys.executable, str(ROOT / "src/interpreter.py"),
                 str(binary), str(dump)], capture_output=True, text=True,
            )
            self.assertEqual(result.returncode, 1)
            self.assertIn("Unknown opcode", result.stderr)
            self.assertFalse(dump.exists())


if __name__ == "__main__":
    unittest.main()
