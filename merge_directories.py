#!/usr/bin/env python3
"""
Merge /Users/steven/pythons-sort into /Users/steven/pythons
Handles duplicates intelligently (checks file content, not just names)
"""

import os
import shutil
from pathlib import Path
from collections import defaultdict
import hashlib

def get_file_hash(filepath):
    """Calculate MD5 hash of file content"""
    hash_md5 = hashlib.md5()
    try:
        with open(filepath, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hash_md5.update(chunk)
        return hash_md5.hexdigest()
    except Exception as e:
        print(f"  ⚠️  Error hashing {filepath}: {e}")
        return None

def flatten_path(rel_path):
    """
    Flatten path by removing intermediate directories like:
    archived_content/other_files/audio_video_conversion → audio_video_conversion
    archived_content/something → something (remove archived_content at root)
    """
    parts = list(rel_path.parts)

    # Remove 'archived_content/other_files' prefix
    if 'archived_content' in parts:
        idx = parts.index('archived_content')
        if idx + 1 < len(parts) and parts[idx + 1] == 'other_files':
            # Remove both archived_content and other_files
            parts = parts[:idx] + parts[idx+2:]
        elif idx == 0 and len(parts) > 1:
            # archived_content/xxx -> xxx (remove archived_content at root)
            parts = parts[1:]
        elif idx == 0:
            # Just "archived_content" -> "." (empty, will be skipped)
            return Path('.')

    # Also remove 'other_files' if it's standalone
    while 'other_files' in parts:
        idx = parts.index('other_files')
        parts = parts[:idx] + parts[idx+1:]

    return Path(*parts) if parts else Path('.')

def merge_directories(source_dir, target_dir, dry_run=True):
    """
    Merge source_dir into target_dir with flattened structure
    - Copy files that don't exist in target
    - For duplicates, check content hash
    - If identical, skip
    - If different, create versioned name
    - Flatten paths (remove archived_content/other_files)
    """
    source = Path(source_dir)
    target = Path(target_dir)

    if not source.exists():
        print(f"❌ Source directory does not exist: {source}")
        return

    if not target.exists():
        print(f"📁 Creating target directory: {target}")
        if not dry_run:
            target.mkdir(parents=True, exist_ok=True)

    stats = {
        'copied': 0,
        'skipped_identical': 0,
        'versioned': 0,
        'errors': 0
    }

    print(f"\n🔄 Merging: {source} → {target}")
    print(f"   Mode: {'DRY RUN' if dry_run else 'LIVE'}")
    print(f"   Flattening: Removing archived_content/other_files prefixes")
    print("=" * 60)

    # Walk through source directory
    for root, dirs, files in os.walk(source):
        src_path = Path(root)
        rel_path = src_path.relative_to(source)

        # Skip .git and __pycache__ directories
        if '.git' in rel_path.parts or '__pycache__' in rel_path.parts:
            continue

        # Filter out .git and __pycache__ from dirs to prevent walking into them
        dirs[:] = [d for d in dirs if d not in ('.git', '__pycache__')]

        # Flatten the path
        flattened_path = flatten_path(rel_path)

        # Skip if flattened to empty or just "."
        if str(flattened_path) == '.' or not flattened_path.parts:
            continue

        dst_dir = target / flattened_path

        # Create destination directory structure
        if not dry_run:
            dst_dir.mkdir(parents=True, exist_ok=True)
        else:
            if not dst_dir.exists():
                print(f"📁 Would create directory: {dst_dir}")

        # Process files
        for file in files:
            src_file = src_path / file
            dst_file = dst_dir / file

            # Skip hidden files and common system files
            if file.startswith('.'):
                continue

            try:
                # Check if file exists in target
                if dst_file.exists():
                    # Files with same name exist - check if identical
                    src_hash = get_file_hash(src_file)
                    dst_hash = get_file_hash(dst_file)

                    if src_hash and dst_hash:
                        if src_hash == dst_hash:
                            # Identical files - skip
                            stats['skipped_identical'] += 1
                            if stats['skipped_identical'] <= 5:
                                print(f"⏭️  Skipped (identical): {rel_path / file}")
                            continue
                        else:
                            # Different content - create versioned name
                            base_name = file.rsplit('.', 1)
                            if len(base_name) == 2:
                                name, ext = base_name
                                versioned_name = f"{name}_from_pythons-sort.{ext}"
                            else:
                                versioned_name = f"{file}_from_pythons-sort"

                            dst_file = dst_dir / versioned_name
                            stats['versioned'] += 1
                            print(f"📝 Versioned (different): {rel_path / file} → {versioned_name}")
                    else:
                        # Couldn't hash - create versioned name
                        base_name = file.rsplit('.', 1)
                        if len(base_name) == 2:
                            name, ext = base_name
                            versioned_name = f"{name}_from_pythons-sort.{ext}"
                        else:
                            versioned_name = f"{file}_from_pythons-sort"

                        dst_file = dst_dir / versioned_name
                        stats['versioned'] += 1
                        print(f"📝 Versioned (couldn't verify): {rel_path / file} → {versioned_name}")
                else:
                    # New file - copy it
                    stats['copied'] += 1
                    if stats['copied'] <= 10:
                        print(f"✅ Would copy: {rel_path / file}")

                # Actually copy the file
                if not dry_run:
                    shutil.copy2(src_file, dst_file)

            except Exception as e:
                stats['errors'] += 1
                print(f"❌ Error processing {src_file}: {e}")

    # Print summary
    print("\n" + "=" * 60)
    print("📊 MERGE SUMMARY:")
    print(f"   Files copied:           {stats['copied']}")
    print(f"   Files skipped (same):   {stats['skipped_identical']}")
    print(f"   Files versioned:        {stats['versioned']}")
    print(f"   Errors:                 {stats['errors']}")
    print("=" * 60)

    return stats

if __name__ == "__main__":
    import sys

    source_dir = "/Users/steven/pythons-sort"
    target_dir = "/Users/steven/pythons"

    # Default to dry-run unless --execute is passed
    dry_run = "--execute" not in sys.argv

    if dry_run:
        print("🔍 DRY RUN MODE - No files will be modified")
        print("   Pass --execute to perform actual merge\n")
    else:
        print("⚠️  LIVE MODE - Files will be copied!")
        print("   Executing merge...\n")

    stats = merge_directories(source_dir, target_dir, dry_run=dry_run)

    if dry_run:
        print("\n💡 Run with --execute to perform the actual merge")

