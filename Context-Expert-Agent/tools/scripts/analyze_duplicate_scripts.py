#!/usr/bin/env python3
"""
Analyze duplicate Python scripts to determine if they're identical or different
Helps with consolidation decisions
"""

import hashlib
from pathlib import Path
from collections import defaultdict
import difflib

def calculate_file_hash(filepath):
    """Calculate MD5 hash of file content"""
    try:
        with open(filepath, 'rb') as f:
            return hashlib.md5(f.read()).hexdigest()
    except:
        return None

def read_file_content(filepath):
    """Read file content for comparison"""
    try:
        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
            return f.read()
    except:
        return None

def compare_files(file1, file2):
    """Compare two files and return similarity ratio"""
    content1 = read_file_content(file1)
    content2 = read_file_content(file2)

    if content1 is None or content2 is None:
        return 0.0

    if content1 == content2:
        return 1.0

    # Calculate similarity
    similarity = difflib.SequenceMatcher(None, content1, content2).ratio()
    return similarity

def analyze_duplicates(root_dir="/Users/steven/AVATARARTS"):
    root = Path(root_dir)

    # Find all Python files
    python_files = list(root.rglob("*.py"))

    # Group by filename
    by_name = defaultdict(list)
    for py_file in python_files:
        # Skip build artifacts
        if any(x in str(py_file) for x in ['.venv', '_build', '__pycache__', '.git']):
            continue
        by_name[py_file.name].append(py_file)

    # Find duplicates
    duplicates = {name: files for name, files in by_name.items() if len(files) > 1}

    print(f"🔍 Found {len(duplicates)} duplicate script names\n")
    print("=" * 80)

    results = []

    for name, files in sorted(duplicates.items(), key=lambda x: len(x[1]), reverse=True):
        print(f"\n📦 {name} ({len(files)} copies)")
        print("-" * 80)

        # Calculate hashes
        hashes = {}
        for f in files:
            file_hash = calculate_file_hash(f)
            if file_hash:
                if file_hash not in hashes:
                    hashes[file_hash] = []
                hashes[file_hash].append(f)

        # Check if all identical
        if len(hashes) == 1:
            print("  ✅ ALL IDENTICAL - Safe to keep only one")
            rel_paths = [str(f.relative_to(root)) for f in files]
            print(f"  📍 Locations:")
            for path in rel_paths:
                print(f"     - {path}")
            print(f"  💡 Recommendation: Keep {rel_paths[0]}, remove others")
            results.append({
                'name': name,
                'count': len(files),
                'status': 'identical',
                'files': rel_paths,
                'recommendation': f"Keep {rel_paths[0]}, remove others"
            })
        else:
            print(f"  ⚠️  DIFFERENT VERSIONS ({len(hashes)} unique)")
            rel_paths = [str(f.relative_to(root)) for f in files]
            print(f"  📍 Locations:")
            for path in rel_paths:
                size = files[rel_paths.index(path)].stat().st_size
                print(f"     - {path} ({size} bytes)")

            # Compare first two files
            if len(files) >= 2:
                similarity = compare_files(files[0], files[1])
                print(f"  📊 Similarity (first 2): {similarity*100:.1f}%")

                if similarity > 0.95:
                    print(f"  💡 Recommendation: Very similar - likely same script, different versions")
                    print(f"     Review manually to determine which is most current")
                elif similarity > 0.70:
                    print(f"  💡 Recommendation: Similar but different - may be variations")
                    print(f"     Review to see if they can be merged or should be renamed")
                else:
                    print(f"  💡 Recommendation: Different scripts with same name")
                    print(f"     Rename to reflect their different purposes")

            results.append({
                'name': name,
                'count': len(files),
                'status': 'different',
                'files': rel_paths,
                'similarity': similarity if len(files) >= 2 else None
            })

    # Summary
    print("\n" + "=" * 80)
    print("\n📊 SUMMARY")
    print("=" * 80)

    identical = [r for r in results if r['status'] == 'identical']
    different = [r for r in results if r['status'] == 'different']

    print(f"\n✅ Identical scripts (safe to consolidate): {len(identical)}")
    print(f"⚠️  Different scripts (need review): {len(different)}")

    if identical:
        print(f"\n🎯 Quick Wins - Can safely remove duplicates:")
        for r in identical[:10]:
            print(f"   - {r['name']}: {r['count']} copies → keep 1")

    return results

if __name__ == "__main__":
    analyze_duplicates()

