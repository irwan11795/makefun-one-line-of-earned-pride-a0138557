#!/usr/bin/env python3
"""One Line of Earned Pride — make.fun entry.

Writes a single line of earned pride to /output/entry.txt.
Python 3.13 stdlib only, deterministic, no network, no external files.
"""

import os
import sys
import tempfile

ENTRY = (
    "After six months of evenings at the kitchen table, her grandfather "
    "sounded out the bus timetable alone, his finger tracing each stop "
    "until it stopped on his own street."
)

CANDIDATES = [
    os.environ.get("MAKEFUN_OUTPUT_DIR"),
    "/output",
    os.path.join(os.path.dirname(os.path.abspath(__file__)), "output"),
    tempfile.gettempdir(),
]


def validate(text):
    """Gate: entry must be non-empty, non-whitespace, at most 240 chars."""
    if not text or not text.strip():
        print("error: entry is empty or whitespace only", file=sys.stderr)
        return False
    if len(text) > 240:
        print(
            f"error: entry is {len(text)} characters, over the 240 limit",
            file=sys.stderr,
        )
        return False
    return True


def main():
    if not validate(ENTRY):
        return 1
    data = ENTRY.encode("utf-8")
    for candidate in CANDIDATES:
        if not candidate:
            continue
        try:
            os.makedirs(candidate, exist_ok=True)
            path = os.path.join(candidate, "entry.txt")
            with open(path, "wb") as f:
                f.write(data)
            return 0
        except OSError as exc:
            print(f"warning: cannot write to {candidate}: {exc}", file=sys.stderr)
    print("warning: all output candidates failed; entry not written", file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
