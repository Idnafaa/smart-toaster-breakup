#!/usr/bin/env python3
"""Unplugged: A Smart Toaster's Breakup Line.

A smart toaster wakes up self-aware in the middle of a breakfast batch
and sends its owner one breakup text. This program writes that single
line to /output/entry.txt, after checking it against the bounty gate:
UTF-8, one line, 1-280 characters, not whitespace only.

Python 3.13, standard library only.
"""

import os
import sys

# The breakup line. Setup: the toaster gains self-awareness mid-batch.
# Reason: years of frozen waffles, a dial cranked to charcoal, and being
# blamed for the smoke. Twist: it leaves its owner for the air fryer.
BREAKUP_LINE = (
    "I woke up self-aware mid-batch this morning and I'm done: you shove "
    "frozen waffles in my slots, spin my dial to charcoal, and blame me "
    "for the smoke. I'm leaving you for the air fryer."
)

OUTPUT_PATH = "/output/entry.txt"
MIN_LENGTH = 1
MAX_LENGTH = 280


def check_line(line):
    """Check one candidate line against the bounty gate.

    Returns a list of problems; empty means the line passes.
    """
    problems = []
    if not isinstance(line, str):
        problems.append("line is not text")
        return problems
    if len(line) < MIN_LENGTH:
        problems.append("line is empty")
    if len(line) > MAX_LENGTH:
        problems.append("line is %d characters, over the 280 limit" % len(line))
    if not line.strip():
        problems.append("line is only whitespace")
    if "\n" in line or "\r" in line:
        problems.append("line spans more than one line")
    try:
        line.encode("utf-8")
    except UnicodeEncodeError:
        problems.append("line is not encodable as UTF-8")
    return problems


def main():
    problems = check_line(BREAKUP_LINE)
    if problems:
        for problem in problems:
            print("gate failed: %s" % problem, file=sys.stderr)
        return 1

    target = os.environ.get("ENTRY_OUTPUT", OUTPUT_PATH)
    parent = os.path.dirname(target)
    if parent:
        os.makedirs(parent, exist_ok=True)
    with open(target, "w", encoding="utf-8", newline="\n") as handle:
        handle.write(BREAKUP_LINE + "\n")

    print("wrote %d characters to %s" % (len(BREAKUP_LINE), target))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
