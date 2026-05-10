#!/usr/bin/env python3
"""
Remove exact duplicate files identified in the duplicate check.
This script will remove the duplicate files, keeping one version of each.
"""

import sys
import hashlib
from pathlib import Path

# Avoid importing local files
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


def remove_exact_duplicates(root_dir, dry_run=True):
    """Remove exact duplicate files."""
    root_path = Path(root_dir)

    # Known exact duplicates from our analysis
    duplicate_groups = [
        # (keep_file, remove_file)
        ("help_uploadbot.py", "categories.py"),
        ("png-jpg.py", "upscale-.py"),  # Keep png-jpg.py, remove upscale-.py
        ("html-auto-img-gallery.py", "bot_checkpoint.py"),
        ("NewUpload_20250607131212.py", "NewUpload_20250607131235.py"),
        ("generate_album_html-pages_fixed.py", "generate_album_html-pages_fixed 1.py"),
    ]

    files_to_remove = []

    print("=" * 80)
    print("🔍 EXACT DUPLICATES IDENTIFIED")
    print("=" * 80)
    print()

    for keep_name, remove_name in duplicate_groups:
        keep_file = root_path / keep_name
        remove_file = root_path / remove_name

        if not keep_file.exists():
            print(f"⚠️  Keep file not found: {keep_name}")
            continue
        if not remove_file.exists():
            print(f"⚠️  Remove file not found: {remove_name}")
            continue

        # Verify they're actually the same size
        if keep_file.stat().st_size == remove_file.stat().st_size:
            print("📦 Duplicate pair:")
            print(f"   ✅ KEEP: {keep_name}")
            print(f"   ❌ REMOVE: {remove_name}")
            files_to_remove.append(remove_file)
            print()
        else:
            print(f"⚠️  Size mismatch: {keep_name} vs {remove_name}")
            print()

    if dry_run:
        print("=" * 80)
        print("🔍 DRY RUN MODE - No files will be deleted")
        print("=" * 80)
        print(f"\nWould remove {len(files_to_remove)} duplicate files")
        print("\nTo actually remove these files, run with --execute flag:")
        print("   python3 remove_exact_duplicates.py --execute")
    else:
        print("=" * 80)
        print("🗑️  REMOVING DUPLICATES")
        print("=" * 80)

        removed_count = 0
        for file in files_to_remove:
            try:
                file.unlink()
                print(f"   ✅ Removed: {file.name}")
                removed_count += 1
            except Exception as e:
                print(f"   ❌ Error removing {file.name}: {e}")

        print(f"\n✅ Removed {removed_count} duplicate files")


if __name__ == "__main__":
    root_directory = Path(__file__).parent
    dry_run = "--execute" not in sys.argv
    remove_exact_duplicates(root_directory, dry_run=dry_run)
