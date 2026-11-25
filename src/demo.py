"""Run all stages and preserve generated binaries and JSON results."""
import json
import math
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
DATASETS = {
    "vector_squares": [0, 1, 4, 9, 16, 25, 36, 49, 64],
    "vector_fractional": [2, 3, 5, 7, 10, 11, 13, 17, 19],
    "vector_large": [81, 100, 121, 144, 169, 196, 225, 256, 289],
}


def command(*arguments):
    """Run another project entry point, stopping on any failure."""
    subprocess.run([sys.executable, *arguments], cwd=ROOT, check=True)


def execute_example(name, start, end):
    """Assemble a sample and execute its binary via both public CLIs."""
    binary = f"build/{name}.bin"
    dump = f"build/{name}.json"
    command("src/assembler.py", f"examples/{name}.asm", binary)
    command("src/interpreter.py", binary, dump,
            "--start", str(start), "--end", str(end))
    return json.loads((ROOT / dump).read_text())["memory"]


def main():
    """Demonstrate reference bytes, copying, ALU and three vectors."""
    command("-m", "unittest", "discover", "-s", "tests", "-v")
    print("\nREFERENCE MACHINE BYTES", flush=True)
    command("src/assembler.py", "examples/spec.asm",
            "build/spec.bin", "--test")
    print("\nARRAY COPY", flush=True)
    copied = list(execute_example("copy", 600, 602).values())
    if copied != [7, 11, 19]:
        raise ValueError("Array copying failed")
    print("Copy result:", copied, flush=True)
    print("\nSINGLE SQUARE ROOT", flush=True)
    print(execute_example("sqrt", 600, 600), flush=True)
    for name, values in DATASETS.items():
        print(f"\n{name}: input={values}", flush=True)
        memory = execute_example(name, 512, 520)
        actual = list(memory.values())
        expected = [math.sqrt(value) for value in values]
        if not all(math.isclose(a, b) for a, b in zip(actual, expected)):
            raise ValueError(f"Vector mismatch: {name}")
        print("Output:", actual, flush=True)
    print("\nALL_STAGES_PASSED", flush=True)


if __name__ == "__main__":
    try:
        main()
    except (OSError, ValueError, subprocess.CalledProcessError) as error:
        print(f"Demo failed: {error}", file=sys.stderr)
        raise SystemExit(1)
