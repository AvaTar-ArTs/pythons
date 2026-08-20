#!/usr/bin/env python3
"""
Find Duplicate Scripts
Identifies duplicate Python scripts by content hash and filename patterns.

Usage:
    python find_duplicate_scripts.py [--delete] [--pattern]
"""

import argparse
import hashlib
from pathlib import Path
from collections import defaultdict
import re


def file_hash(file_path):
    """Calculate MD5 hash of file content."""
    hash_md5 = hashlib.md5()
    try:
        with open(file_path, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hash_md5.update(chunk)
        return hash_md5.hexdigest()
    except Exception as e:
        print(f"Error reading {file_path}: {e}")
        return None


def find_duplicate_patterns(root_dir):
    """Find files with duplicate patterns in names."""
    patterns = [
        r'\(1\)',  # (1), (2), etc.
        r'_1\.py$',  # _1.py, _2.py, etc.
        r'_copy\.py$',  # _copy.py
        r' copy\.py$',  #  copy.py
        r'_v\d+\.py$',  # _v1.py, _v2.py (if same base)
    ]

    duplicates = defaultdict(list)

    for py_file in Path(root_dir).rglob('*.py'):
        name = py_file.name
        for pattern in patterns:
            if re.search(pattern, name):
                # Extract base name
                base_name = re.sub(pattern, '', name)
                if base_name:
                    duplicates[base_name].append(py_file)

    return duplicates


def find_content_duplicates(root_dir):
    """Find duplicate files by content hash."""
    hashes = defaultdict(list)

    print("Calculating file hashes...")
    for py_file in Path(root_dir).rglob('*.py'):
        file_hash_val = file_hash(py_file)
        if file_hash_val:
            hashes[file_hash_val].append(py_file)

    # Filter to only groups with duplicates
    duplicates = {h: files for h, files in hashes.items() if len(files) > 1}
    return duplicates


def main():
    parser = argparse.ArgumentParser(
        description='Find duplicate Python scripts'
    )
    parser.add_argument(
        '--root',
        type=str,
        default='/Users/steven/pythons',
        help='Root directory to scan (default: /Users/steven/pythons)'
    )
    parser.add_argument(
        '--pattern',
        action='store_true',
        help='Find duplicates by filename patterns (e.g., (1), _1, copy)'
    )
    parser.add_argument(
        '--content',
        action='store_true',
        help='Find duplicates by content hash'
    )
    parser.add_argument(
        '--delete',
        action='store_true',
        help='Delete duplicate files (keeps first occurrence)'
    )
    parser.add_argument(
        '--all',
        action='store_true',
        help='Run both pattern and content checks'
    )

    args = parser.parse_args()

    root_path = Path(args.root)
    if not root_path.exists():
        print(f"Error: Root directory {root_path} does not exist")
        return 1

    run_pattern = args.pattern or args.all
    run_content = args.content or args.all

    if not run_pattern and not run_content:
        print("Please specify --pattern, --content, or --all")
        return 1

    print(f"Scanning {root_path} for duplicate scripts...\n")

    # Pattern-based duplicates
    if run_pattern:
        print("=" * 60)
        print("FILENAME PATTERN DUPLICATES")
        print("=" * 60)

        pattern_dups = find_duplicate_patterns(root_path)

        if pattern_dups:
            total_files = sum(len(files) for files in pattern_dups.values())
            print(f"\nFound {len(pattern_dups)} base files with pattern duplicates")
            print(f"Total files: {total_files}\n")

            for base_name, files in sorted(pattern_dups.items()):
                if len(files) > 1:
                    print(f"\n{base_name} ({len(files)} variants):")
                    for f in sorted(files):
                        print(f"  - {f}")

                    if args.delete:
                        # Keep the first (usually the original), delete others
                        original = files[0]
                        for dup in files[1:]:
                            try:
                                dup.unlink()
                                print(f"    ✓ Deleted {dup.name}")
                            except Exception as e:
                                print(f"    ✗ Error deleting {dup.name}: {e}")
        else:
            print("No pattern-based duplicates found.")

    # Content-based duplicates
    if run_content:
        print("\n" + "=" * 60)
        print("CONTENT-BASED DUPLICATES")
        print("=" * 60)

        content_dups = find_content_duplicates(root_path)

        if content_dups:
            total_dups = sum(len(files) - 1 for files in content_dups.values())
            print(f"\nFound {len(content_dups)} groups of duplicate content")
            print(f"Total duplicate files: {total_dups}\n")

            for hash_val, files in sorted(content_dups.items(), key=lambda x: len(x[1]), reverse=True):
                print(f"\nDuplicate group (hash: {hash_val[:8]}...) - {len(files)} files:")
                for f in sorted(files):
                    print(f"  - {f}")

                if args.delete:
                    # Keep the first, delete others
                    original = files[0]
                    for dup in files[1:]:
                        try:
                            dup.unlink()
                            print(f"    ✓ Deleted {dup.name}")
                        except Exception as e:
                            print(f"    ✗ Error deleting {dup.name}: {e}")
        else:
            print("No content-based duplicates found.")

    if args.delete:
        print("\n✓ Duplicate removal complete")
    else:
        print("\n[DRY RUN] Use --delete to actually remove duplicates")

    return 0


if __name__ == '__main__':
    exit(main())

