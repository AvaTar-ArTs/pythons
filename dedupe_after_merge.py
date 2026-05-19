#!/usr/bin/env python3
"""
Deduplicate files after merge operations
Removes duplicate files based on content hash and keeps the best version
"""

import os
import hashlib
from pathlib import Path
from collections import defaultdict
from typing import Dict, List, Tuple
import json

def calculate_file_hash(filepath: Path) -> str:
    """Calculate MD5 hash of file content"""
    hash_md5 = hashlib.md5()
    try:
        with open(filepath, 'rb') as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hash_md5.update(chunk)
        return hash_md5.hexdigest()
    except Exception as e:
        return ""

def find_duplicates(root_dir: Path) -> Dict[str, List[Path]]:
    """Find duplicate files by content hash"""
    hash_to_files = defaultdict(list)

    print("🔍 Scanning for duplicate files...")

    for root, dirs, files in os.walk(root_dir):
        # Skip .git and __pycache__
        dirs[:] = [d for d in dirs if d not in ('.git', '__pycache__')]

        for file in files:
            if file.startswith('.'):
                continue

            filepath = Path(root) / file
            try:
                file_hash = calculate_file_hash(filepath)
                if file_hash:
                    hash_to_files[file_hash].append(filepath)
            except Exception:
                continue

    # Filter to only hashes with duplicates
    duplicates = {h: files for h, files in hash_to_files.items() if len(files) > 1}

    return duplicates

def choose_best_file(files: List[Path]) -> Tuple[Path, List[Path]]:
    """Choose the best file to keep (prefer shorter paths, non-versioned names)"""
    # Score each file (lower is better)
    scored = []
    for f in files:
        score = 0
        path_str = str(f)

        # Prefer shorter paths
        score += len(path_str.split(os.sep)) * 10

        # Prefer non-versioned names (without "_from_", "_v2", etc.)
        if any(marker in f.name for marker in ['_from_', '_v', '_copy', '_backup']):
            score += 100

        # Prefer files in root/common directories
        if 'tools' in path_str.lower() or 'scripts' in path_str.lower():
            score -= 20

        scored.append((score, f))

    # Sort by score (lower is better)
    scored.sort(key=lambda x: x[0])

    keep = scored[0][1]
    remove = [f for score, f in scored[1:]]

    return keep, remove

def deduplicate(root_dir: Path, dry_run: bool = True) -> Dict:
    """Deduplicate files in directory"""
    root = Path(root_dir)

    print("🔍 DEDUPLICATION PROCESS")
    print("=" * 70)
    print(f"Directory: {root}")
    print(f"Mode: {'DRY RUN' if dry_run else 'LIVE'}")
    print()

    # Find duplicates
    duplicates = find_duplicates(root)

    if not duplicates:
        print("✅ No duplicate files found!")
        return {'duplicates_found': 0, 'files_removed': 0, 'space_freed': 0}

    print(f"📊 Found {len(duplicates)} sets of duplicate files")
    print()

    total_removed = 0
    total_space = 0
    operations = []

    # Process each duplicate set
    for file_hash, files in duplicates.items():
        if len(files) <= 1:
            continue

        keep, remove = choose_best_file(files)

        # Calculate space that will be freed
        file_size = keep.stat().st_size if keep.exists() else 0
        space_to_free = file_size * (len(remove))

        operations.append({
            'hash': file_hash[:8],
            'keep': str(keep.relative_to(root)),
            'remove': [str(f.relative_to(root)) for f in remove],
            'size': file_size,
            'count': len(remove),
            'space_freed': space_to_free
        })

        total_removed += len(remove)
        total_space += space_to_free

        # Show first 10
        if len(operations) <= 10:
            print(f"📁 Duplicate set ({len(files)} files, {file_size:,} bytes each):")
            print(f"   ✅ Keep: {keep.relative_to(root)}")
            for f in remove:
                print(f"   ❌ Remove: {f.relative_to(root)}")
            print()

    if len(operations) > 10:
        print(f"   ... and {len(operations) - 10} more duplicate sets\n")

    # Execute removal
    if not dry_run:
        print("🗑️  Removing duplicate files...")
        removed_count = 0
        for op in operations:
            for file_path in op['remove']:
                full_path = root / file_path
                try:
                    if full_path.exists():
                        full_path.unlink()
                        removed_count += 1
                except Exception as e:
                    print(f"   ⚠️  Error removing {file_path}: {e}")

        print(f"✅ Removed {removed_count} duplicate files")
    else:
        print(f"💡 Would remove {total_removed} duplicate files")

    # Summary
    print("\n" + "=" * 70)
    print("📊 DEDUPLICATION SUMMARY:")
    print(f"   Duplicate sets found:  {len(duplicates)}")
    print(f"   Files to remove:       {total_removed}")
    print(f"   Space to free:         {total_space / (1024*1024):.2f} MB")
    print("=" * 70)

    return {
        'duplicates_found': len(duplicates),
        'files_removed': total_removed if not dry_run else 0,
        'space_freed': total_space,
        'operations': operations
    }

def main():
    """Main execution"""
    import sys

    root_dir = sys.argv[1] if len(sys.argv) > 1 else "/Users/steven/pythons"
    dry_run = "--execute" not in sys.argv

    if dry_run:
        print("🔍 DRY RUN MODE - No files will be deleted")
        print("   Pass --execute to perform actual deduplication\n")
    else:
        print("⚠️  LIVE MODE - Duplicate files will be deleted!")
        print("   Executing deduplication...\n")

    result = deduplicate(Path(root_dir), dry_run=dry_run)

    if dry_run:
        print("\n💡 Run with --execute to perform actual deduplication")
    else:
        print("\n✅ Deduplication complete!")

if __name__ == "__main__":
    main()

