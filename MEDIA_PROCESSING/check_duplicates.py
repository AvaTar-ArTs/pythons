#!/usr/bin/env python3
"""
Check for duplicate files in the directory by:
1. Filename patterns (similar names)
2. Content hashing (exact duplicates)
3. File size comparison
"""

import sys
import hashlib
from pathlib import Path
from collections import defaultdict
from difflib import SequenceMatcher

# Avoid importing local files that might conflict with stdlib
# Remove current directory from path temporarily
if str(Path(__file__).parent) in sys.path:
    sys.path.remove(str(Path(__file__).parent))


def calculate_file_hash(filepath):
    """Calculate MD5 hash of file content."""
    hash_md5 = hashlib.md5()
    try:
        with open(filepath, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hash_md5.update(chunk)
        return hash_md5.hexdigest()
    except Exception:
        return None


def similarity(a, b):
    """Calculate similarity ratio between two strings."""
    return SequenceMatcher(None, a, b).ratio()


def check_duplicates(root_dir):
    """Check for duplicate files."""
    root_path = Path(root_dir)

    # Get all Python files
    all_files = [f for f in root_path.iterdir() if f.is_file() and f.suffix == ".py"]

    print(f"🔍 Analyzing {len(all_files)} Python files for duplicates...\n")

    # 1. Check for similar filenames
    print("=" * 80)
    print("📝 SIMILAR FILENAMES (Potential duplicates by name)")
    print("=" * 80)

    similar_groups = []
    processed = set()

    for i, file1 in enumerate(all_files):
        if file1.name in processed:
            continue
        group = [file1]
        name1 = file1.stem.lower()

        for file2 in all_files[i + 1 :]:
            if file2.name in processed:
                continue
            name2 = file2.stem.lower()

            # Check for high similarity or common patterns
            sim = similarity(name1, name2)
            if sim > 0.7 or (name1 in name2 or name2 in name1):
                group.append(file2)
                processed.add(file2.name)

        if len(group) > 1:
            similar_groups.append(group)
            processed.add(file1.name)

    for group in similar_groups:
        print(f"\n📦 Similar names ({len(group)} files):")
        for f in sorted(group):
            size = f.stat().st_size
            print(f"   • {f.name} ({size:,} bytes)")

    # 2. Check for exact content duplicates (by hash)
    print("\n" + "=" * 80)
    print("🔐 EXACT CONTENT DUPLICATES (Same hash)")
    print("=" * 80)

    hash_to_files = defaultdict(list)

    print("Calculating file hashes...")
    for file in all_files:
        file_hash = calculate_file_hash(file)
        if file_hash:
            hash_to_files[file_hash].append(file)

    exact_duplicates = {
        h: files for h, files in hash_to_files.items() if len(files) > 1
    }

    if exact_duplicates:
        print(f"\nFound {len(exact_duplicates)} groups of exact duplicates:\n")
        for i, (file_hash, files) in enumerate(exact_duplicates.items(), 1):
            print(f"Group {i} ({len(files)} identical files):")
            for f in sorted(files):
                size = f.stat().st_size
                print(f"   • {f.name} ({size:,} bytes)")
            print(f"   Hash: {file_hash[:16]}...")
            print()
    else:
        print("\n✅ No exact content duplicates found!")

    # 3. Check for files with same size (potential duplicates)
    print("=" * 80)
    print("📊 FILES WITH SAME SIZE (Potential duplicates)")
    print("=" * 80)

    size_to_files = defaultdict(list)
    for file in all_files:
        size = file.stat().st_size
        size_to_files[size].append(file)

    same_size_groups = {
        s: files for s, files in size_to_files.items() if len(files) > 1 and s > 0
    }

    if same_size_groups:
        print(
            f"\nFound {len(same_size_groups)} groups of files with identical sizes:\n"
        )
        for size, files in sorted(same_size_groups.items(), key=lambda x: -len(x[1]))[
            :20
        ]:  # Top 20
            if len(files) > 1:
                print(f"Size: {size:,} bytes ({len(files)} files):")
                for f in sorted(files):
                    print(f"   • {f.name}")
                print()
    else:
        print("\n✅ No files with identical sizes found!")

    # Summary
    print("=" * 80)
    print("📈 SUMMARY")
    print("=" * 80)
    print(f"Total files analyzed: {len(all_files)}")
    print(f"Similar filename groups: {len(similar_groups)}")
    print(f"Exact duplicate groups: {len(exact_duplicates)}")
    print(f"Same-size groups: {len(same_size_groups)}")

    # Generate recommendations
    if exact_duplicates or similar_groups:
        print("\n" + "=" * 80)
        print("💡 RECOMMENDATIONS")
        print("=" * 80)
        if exact_duplicates:
            print(
                "⚠️  Exact duplicates found - consider removing duplicates and keeping one version"
            )
        if similar_groups:
            print(
                "⚠️  Similar filenames found - review to see if they're actual duplicates"
            )
        print("\nYou may want to:")
        print("  1. Review exact duplicates and remove redundant copies")
        print("  2. Compare similar-named files to see if they're duplicates")
        print("  3. Consolidate functionality into fewer files")


if __name__ == "__main__":
    root_directory = Path(__file__).parent
    check_duplicates(root_directory)
