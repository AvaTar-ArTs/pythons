#!/usr/bin/env python3
"""
Analyze remaining files after consolidation.

Categorizes and summarizes what's left at root level.
"""

from collections import defaultdict
from pathlib import Path

PROJECT = Path(__file__).parent


def analyze_remaining():
    """Analyze remaining root files."""
    stats = defaultdict(int)
    categories = defaultdict(list)
    py_files = []
    md_files = []

    for f in PROJECT.iterdir():
        if not f.is_file() or f.name.startswith(".") or f.name in ["README.md"]:
            continue

        stats["total"] += 1
        suffix = f.suffix.lower()

        # Count by type
        if suffix == ".pyc":
            stats["pyc"] += 1
            categories["Python bytecode"].append(f.name)
        elif suffix == ".py":
            stats["py"] += 1
            py_files.append(f.name)
        elif suffix == ".md":
            stats["md"] += 1
            md_files.append(f.name)
        elif suffix in [".csv", ".json", ".txt"]:
            stats["data"] += 1
            categories["Data files"].append(f.name)
        elif suffix in [".html", ".xml"]:
            stats["web"] += 1
            categories["Web files"].append(f.name)
        elif suffix in [".gz", ".tar", ".zip"]:
            stats["archives"] += 1
            categories["Archives"].append(f.name)
        elif suffix == ".sh":
            stats["scripts"] += 1
            categories["Shell scripts"].append(f.name)
        else:
            stats["other"] += 1
            categories["Other"].append(f.name)

    print("Remaining Files Analysis")
    print("=" * 50)
    print(f"Total remaining files: {stats['total']}")
    print()

    print("By file type:")
    print(f"  Python scripts: {stats['py']}")
    print(f"  Markdown docs: {stats['md']}")
    print(f"  Compiled .pyc: {stats['pyc']}")
    print(f"  Data files: {stats['data']}")
    print(f"  Web files: {stats['web']}")
    print(f"  Archives: {stats['archives']}")
    print(f"  Shell scripts: {stats['scripts']}")
    print(f"  Other: {stats['other']}")
    print()

    print("Python scripts to categorize:")
    print(f"  Total: {len(py_files)}")
    print("  Sample:", py_files[:5], "..." if len(py_files) > 5 else "")
    print()

    print("Markdown docs to organize:")
    print(f"  Total: {len(md_files)}")
    print("  Sample:", md_files[:5], "..." if len(md_files) > 5 else "")
    print()

    print("Other categories:")
    for category, files in categories.items():
        if category not in ["Python scripts", "Markdown docs"]:
            print(f"  {category}: {len(files)} files")


if __name__ == "__main__":
    analyze_remaining()
