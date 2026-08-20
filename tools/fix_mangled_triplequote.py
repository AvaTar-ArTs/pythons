#!/usr/bin/env python3
r"""Un-mangle triple-quoted strings corrupted by a shell-quoting codemod bug.

A bad codemod passed source through shell single-quoting and turned every
Python triple-quote (`\"\"\"`) into the 4-char sequence `'\''` (apostrophe,
backslash, apostrophe, apostrophe). That breaks multi-line strings, docstrings,
and f-strings ("'(' was never closed" / "unterminated string literal").

This tool replaces that exact artifact with `\"\"\"`, but ONLY when doing so
makes the file parse (safety guard against a legitimate `'\''` literal).

Usage:
    fix_mangled_triplequote.py --check FILE...
    fix_mangled_triplequote.py FILE...
"""
from __future__ import annotations

import ast
import sys

ARTIFACT = r"'\''"
REPLACEMENT = '"""'


def main(argv: list[str]) -> int:
    check = "--check" in argv
    files = [a for a in argv if a != "--check"]
    for path in files:
        src = open(path, encoding="utf-8").read()
        if ARTIFACT not in src:
            print(f"{path}: no-artifact")
            continue
        fixed = src.replace(ARTIFACT, REPLACEMENT)
        try:
            ast.parse(fixed)
        except SyntaxError as e:
            print(f"{path}: SKIP (still broken after fix -> L{e.lineno}: {e.msg})")
            continue
        print(f"{path}: fixed ({src.count(ARTIFACT)} artifacts)")
        if not check:
            with open(path, "w", encoding="utf-8") as f:
                f.write(fixed)
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
