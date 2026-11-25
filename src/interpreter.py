"""Command-line interface for the unified-memory virtual machine."""
import argparse
import json
from pathlib import Path
import sys

from instructions import ADDRESS_LIMIT
from machine import Machine


def main(argv=None):
    """Execute a binary program and save an inclusive JSON memory dump."""
    parser = argparse.ArgumentParser(description="Variant 24 interpreter")
    parser.add_argument("program", type=Path)
    parser.add_argument("dump", type=Path)
    parser.add_argument("--start", type=int, default=0)
    parser.add_argument("--end", type=int, default=ADDRESS_LIMIT - 1)
    args = parser.parse_args(argv)
    try:
        if args.program.resolve() == args.dump.resolve():
            raise ValueError("Program and dump must be different files")
        machine = Machine(args.program.read_bytes())
        machine.dump(args.start, args.end)
        machine.run()
        result = json.dumps(
            machine.dump(args.start, args.end), indent=2, allow_nan=False
        )
        args.dump.parent.mkdir(parents=True, exist_ok=True)
        args.dump.write_text(result + "\n", encoding="utf-8")
        print(f"Executed instructions: {machine.executed}")
        print(f"Memory dump: {args.dump}")
        return 0
    except (OSError, ValueError) as error:
        print(f"Execution error: {error}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
