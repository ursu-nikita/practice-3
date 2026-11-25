"""Assembler command-line interface."""
import argparse
from pathlib import Path
import sys

from parser import parse_program
from codec import encode


def main(argv=None):
    """Translate a complete source and save its machine code."""
    parser = argparse.ArgumentParser(description="Variant 24 assembler")
    parser.add_argument("source", type=Path)
    parser.add_argument("output", type=Path)
    parser.add_argument("--test", action="store_true")
    args = parser.parse_args(argv)
    try:
        source = args.source.read_text(encoding="utf-8-sig")
        instructions = parse_program(source)
        data = b"".join(encode(item) for item in instructions)
        if args.source.resolve() == args.output.resolve():
            raise ValueError("Source and output must be different files")
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_bytes(data)
        if args.test:
            for instruction in instructions:
                print(instruction.fields())
                encoded = encode(instruction)
                print(", ".join(f"0x{byte:02X}" for byte in encoded))
        print(f"Instructions: {len(instructions)}")
        return 0
    except (OSError, ValueError) as error:
        print(f"Assembly error: {error}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
