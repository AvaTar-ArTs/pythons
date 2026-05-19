#!/usr/bin/env python3
"""
Compare top-level imports in .py files vs requirements.txt package names.
Unique SKU: Gumroad buyers fail on pip install—this audits the gap.
"""

from __future__ import annotations

import argparse
import ast
import re
import sys
from pathlib import Path

# Extend as needed for PyPI name != import name
IMPORT_TO_PKG = {
    "PIL": "Pillow",
    "sklearn": "scikit-learn",
    "yaml": "PyYAML",
    "bs4": "beautifulsoup4",
    "cv2": "opencv-python",
    "dotenv": "python-dotenv",
}


def stdlib() -> set[str]:

    s = getattr(sys, "stdlib_module_names", None)
    if s:
        return set(s)
    return {
        "os",
        "sys",
        "re",
        "json",
        "csv",
        "math",
        "pathlib",
        "argparse",
        "ast",
        "collections",
        "typing",
        "io",
        "subprocess",
    }


def parse_requirements(req_path: Path) -> set[str]:
    if not req_path.is_file():
        return set()
    pkgs: set[str] = set()
    for line in req_path.read_text(encoding="utf-8", errors="replace").splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        # strip extras e.g. pandas>=2
        m = re.match(r"([a-zA-Z0-9_.\-]+)", line)
        if m:
            name = m.group(1).lower()
            # normalize common patterns
            pkgs.add(name.split("[")[0])
    return pkgs


def top_level_imports(py_path: Path) -> set[str]:
    src = py_path.read_text(encoding="utf-8", errors="replace")
    try:
        tree = ast.parse(src)
    except SyntaxError:
        return set()
    found: set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                found.add(alias.name.split(".")[0])
        elif isinstance(node, ast.ImportFrom) and node.module:
            if node.level and node.level > 0:
                continue
            found.add(node.module.split(".")[0])
    return found


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(
        description="Audit imports vs requirements.txt for a project folder."
    )
    p.add_argument(
        "root",
        type=Path,
        help="Root folder to scan for *.py",
    )
    p.add_argument(
        "-r",
        "--requirements",
        type=Path,
        default=None,
        help="requirements.txt path (default: root/requirements.txt)",
    )
    return p.parse_args()


def main() -> int:
    args = parse_args()
    root = args.root
    req_path = args.requirements or (root / "requirements.txt")
    req_pkgs = parse_requirements(req_path)
    lib = stdlib()

    used: set[str] = set()
    for py in root.rglob("*.py"):
        if "__pycache__" in py.parts:
            continue
        used |= top_level_imports(py)

    third = {u for u in used if u and u != "__future__" and u not in lib}
    missing_req: list[str] = []
    for name in sorted(third):
        pkg = IMPORT_TO_PKG.get(name, name).lower()
        # requirements often list canonical name
        if pkg not in req_pkgs and name.lower() not in req_pkgs:
            # loose: any req line starts with name
            if not any(r.startswith(name.lower()) or r.startswith(pkg) for r in req_pkgs):
                missing_req.append(name)

    print(f"requirements.txt: {req_path} ({len(req_pkgs)} packages)")
    print(f"Third-party imports seen: {len(third)}")
    print()
    if missing_req:
        print("Possibly missing from requirements (review manually):")
        for m in missing_req:
            print(f"  - {m} (pip name often: {IMPORT_TO_PKG.get(m, m)})")
    else:
        print("No obvious third-party import without a requirements line (heuristic).")
    print()
    print("Heuristic only—verify with pip install in a clean venv.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
