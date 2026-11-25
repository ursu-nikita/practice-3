"""Assembler command-line interface."""
import argparse
from pathlib import Path
import sys

from parser import parse_program


def main(argv=None):
    """Read assembly text and print its intermediate representation."""
    parser = argparse.ArgumentParser(description="Variant 24 assembler")
    parser.add_argument("source", type=Path)
    parser.add_argument("output", type=Path)
    parser.add_argument("--test", action="store_true")
    args = parser.parse_args(argv)
    try:
        source = args.source.read_text(encoding="utf-8-sig")
        instructions = parse_program(source)
        if args.test:
            for instruction in instructions:
                print(instruction.fields())
        print(f"Instructions: {len(instructions)}")
        return 0
    except (OSError, ValueError) as error:
        print(f"Assembly error: {error}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
