#!/usr/bin/env python3
"""
Version Comparison Tool
Shows differences between script versions to help decide which to keep
"""

import difflib
from pathlib import Path
import sys


def compare_files(file1, file2):
    """Compare two files and show differences"""
    try:
        with open(file1, "r", errors="ignore") as f:
            lines1 = f.readlines()
        with open(file2, "r", errors="ignore") as f:
            lines2 = f.readlines()
    except Exception as e:
        print(f"Error reading files: {e}")
        return

    # Generate diff
    diff = list(
        difflib.unified_diff(
            lines1,
            lines2,
            fromfile=str(file1.name),
            tofile=str(file2.name),
            lineterm="",
        )
    )

    if not diff:
        print(f"? Files are identical!")
        return

    # Count changes
    additions = sum(
        1 for line in diff if line.startswith("+") and not line.startswith("+++")
    )
    deletions = sum(
        1 for line in diff if line.startswith("-") and not line.startswith("---")
    )

    print(f"\n?? Changes: +{additions} lines, -{deletions} lines")
    print("=" * 70)

    # Show first 50 lines of diff
    for line in diff[:50]:
        if line.startswith("+++") or line.startswith("---"):
            print(f"\033[1m{line}\033[0m")  # Bold
        elif line.startswith("+"):
            print(f"\033[32m{line}\033[0m")  # Green
        elif line.startswith("-"):
            print(f"\033[31m{line}\033[0m")  # Red
        elif line.startswith("@@"):
            print(f"\033[36m{line}\033[0m")  # Cyan
        else:
            print(line)

    if len(diff) > 50:
        print(f"\n... ({len(diff) - 50} more lines of diff)")


def compare_family(base_dir, pattern):
    """Compare all versions of a script family"""
    versions = sorted(base_dir.glob(pattern))

    if len(versions) < 2:
        print(f"Found {len(versions)} files matching {pattern}")
        return

    print(f"\n?? Found {len(versions)} versions:")
    print("=" * 70)

    for i, v in enumerate(versions, 1):
        stats = v.stat()
        print(
            f"{i}. {v.name:<40} {stats.st_size:>8,} bytes  "
            f"{sum(1 for _ in open(v, errors='ignore')):>4} lines"
        )

    print("\n" + "=" * 70)
    print("Comparing versions...")

    # Compare each version with the next
    for i in range(len(versions) - 1):
        print(f"\n{'=' * 70}")
        print(f"COMPARING: {versions[i].name} ?  {versions[i+1].name}")
        print("=" * 70)
        compare_files(versions[i], versions[i + 1])


def analyze_content(filepath):
    """Analyze what a script does"""
    try:
        with open(filepath, "r", errors="ignore") as f:
            content = f.read()

        # Extract docstring
        lines = content.split("\n")
        docstring = []
        in_docstring = False

        for line in lines[:50]:  # First 50 lines
            if '"""' in line or "'''" in line:
                in_docstring = not in_docstring
                docstring.append(line)
            elif in_docstring:
                docstring.append(line)
            elif line.strip().startswith("#") and len(line.strip()) > 2:
                docstring.append(line)

        # Find imports
        imports = [
            line for line in lines if line.strip().startswith(("import ", "from "))
        ]

        # Find functions/classes
        functions = [line for line in lines if line.strip().startswith("def ")]
        classes = [line for line in lines if line.strip().startswith("class ")]

        print(f"\n?? {filepath.name}")
        print("=" * 70)

        if docstring:
            print("\n?? Documentation:")
            for line in docstring[:10]:
                print(f"  {line}")

        if imports:
            print(f"\n?? Imports: ({len(imports)})")
            for imp in imports[:10]:
                print(f"  {imp.strip()}")

        if functions:
            print(f"\n?? Functions: ({len(functions)})")
            for func in functions[:10]:
                print(f"  {func.strip()}")

        if classes:
            print(f"\n???  Classes: ({len(classes)})")
            for cls in classes:
                print(f"  {cls.strip()}")

    except Exception as e:
        print(f"Error analyzing {filepath}: {e}")


def main():
    if len(sys.argv) < 2:
        print("Usage:")
        print("  python3 compare_versions.py upload")
        print("  python3 compare_versions.py youtube/upload*.py")
        print("  python3 compare_versions.py --analyze youtube/upload_30.py")
        return

    if sys.argv[1] == "--analyze":
        if len(sys.argv) < 3:
            print("Please specify a file to analyze")
            return
        analyze_content(Path(sys.argv[2]))
        return

    # Find matching files
    pattern = sys.argv[1]

    if "/" in pattern:
        # Full path given
        base_dir = Path(pattern).parent
        pattern = Path(pattern).name
    else:
        # Search current directory
        base_dir = Path("/Users/steven/documents/python")
        # Find in all subdirectories
        all_matches = list(base_dir.rglob(f"{pattern}*.py"))

        if not all_matches:
            print(f"No files found matching: {pattern}")
            return

        # Group by parent directory
        by_dir = {}
        for m in all_matches:
            by_dir.setdefault(m.parent, []).append(m)

        if len(by_dir) > 1:
            print(f"Found {len(all_matches)} files in {len(by_dir)} directories:")
            for d, files in by_dir.items():
                print(f"\n{d.relative_to(base_dir)}/: {len(files)} files")

            print("\nSpecify directory:")
            print(f"  python3 compare_versions.py youtube/{pattern}")
            return

        base_dir = list(by_dir.keys())[0]
        pattern = f"{pattern}*.py"

    compare_family(base_dir, pattern)


if __name__ == "__main__":
    main()
