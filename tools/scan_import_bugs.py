#!/usr/bin/env python3
"""Scan for syntax errors and module-level use-before-import. Exit 1 if any found."""
from __future__ import annotations

import ast
import sys
import warnings

warnings.filterwarnings("ignore")


def scan(path: str):
    try:
        src = open(path, encoding="utf-8", errors="replace").read()
    except OSError:
        return None
    try:
        tree = ast.parse(src)
    except SyntaxError as e:
        return ("SYNTAX", e.lineno, str(e.msg))

    import_line: dict[str, int] = {}

    def note(name: str, lineno: int) -> None:
        # earliest import line wins (ast.walk is breadth-first, so a shallow
        # module-level import can otherwise mask a deeper, earlier one)
        if name not in import_line or lineno < import_line[name]:
            import_line[name] = lineno

    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for a in node.names:
                note((a.asname or a.name).split(".")[0], node.lineno)
        elif isinstance(node, ast.ImportFrom):
            for a in node.names:
                note(a.asname or a.name, node.lineno)

    hits = []
    for stmt in tree.body:
        if isinstance(stmt, (ast.Import, ast.ImportFrom)):
            continue
        for n in ast.walk(stmt):
            if isinstance(n, ast.Name) and isinstance(n.ctx, ast.Load):
                if n.id in import_line and n.lineno < import_line[n.id]:
                    hits.append((n.id, n.lineno, import_line[n.id]))
    return ("USE_BEFORE_IMPORT", sorted(set(hits))) if hits else None


def main(argv):
    syntax, ube = [], []
    for path in argv:
        r = scan(path)
        if not r:
            continue
        if r[0] == "SYNTAX":
            syntax.append((path, r[1], r[2]))
        else:
            ube.append((path, r[1]))
    for p, ln, msg in syntax:
        print(f"SYNTAX  {p}:{ln}  {msg}")
    for p, hits in ube:
        for name, use, imp in hits[:3]:
            print(f"UBI     {p}: '{name}' used@L{use} imported@L{imp}")
    print(f"\n== {len(syntax)} syntax, {len(ube)} use-before-import ==")
    return 1 if (syntax or ube) else 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
