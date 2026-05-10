#!/usr/bin/env python3
'\''
Compare files with identical sizes to check if they're actual duplicates.
"""

import sys
from pathlib import Path
from collections import defaultdict

# Avoid importing local files
if str(Path(__file__).parent) in sys.path:
    sys.path.remove(str(Path(__file__).parent))


def read_file_content(filepath, max_lines=50):
    """Read first N lines of a file for comparison."""
    try:
        with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
            lines = [f.readline() for _ in range(max_lines)]
        return "".join(lines)
    except Exception:
        return None


def compare_files(file1, file2):
    """Compare two files and return similarity info."""
    content1 = read_file_content(file1)
    content2 = read_file_content(file2)

    if content1 is None or content2 is None:
        return None

    # Simple comparison
    if content1 == content2:
        return "IDENTICAL"

    # Count matching lines
    lines1 = content1.split("\n")
    lines2 = content2.split("\n")
    matches = sum(1 for l1, l2 in zip(lines1, lines2) if l1 == l2)
    total = max(len(lines1), len(lines2))
    similarity = (matches / total * 100) if total > 0 else 0

    return f"{similarity:.1f}% similar"


def check_same_size_files(root_dir):
    """Check files with identical sizes.'\''
    root_path = Path(root_dir)
    all_files = [f for f in root_path.iterdir() if f.is_file() and f.suffix == ".py"]

    size_to_files = defaultdict(list)
    for file in all_files:
        size = file.stat().st_size
        size_to_files[size].append(file)

    same_size_groups = {
        s: files for s, files in size_to_files.items() if len(files) > 1 and s > 0
    }

    print("=" * 80)
    print("🔍 DETAILED COMPARISON OF FILES WITH IDENTICAL SIZES")
    print("=" * 80)
    print()

    for size, files in sorted(same_size_groups.items(), key=lambda x: -len(x[1])):
        print(f"📦 Size: {size:,} bytes ({len(files)} files)")
        print("-" * 80)

        # Compare all pairs
        for i, file1 in enumerate(files):
            for file2 in files[i + 1 :]:
                comparison = compare_files(file1, file2)
                if comparison:
                    status = "✅" if comparison == "IDENTICAL" else "⚠️"
                    print(f"   {status} {file1.name} vs {file2.name}: {comparison}")

        print()


if __name__ == "__main__":
    root_directory = Path(__file__).parent
    check_same_size_files(root_directory)
