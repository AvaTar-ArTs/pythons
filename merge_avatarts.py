#!/usr/bin/env python3
"""
Merge /Users/steven/AVATARARTS into ~/pythons with flattening logic
Applies similar flattening as pythons-sort merge
"""

import os
import shutil
from pathlib import Path
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
        return None

def flatten_avatarts_path(rel_path):
    """
    Flatten AVATARARTS paths by removing intermediate directories:
    AVATARARTS/00_ACTIVE/DEVELOPMENT/UTILITIES_TOOLS/tools/media/image
    → tools/media/image

    Common patterns to flatten:
    - Remove AVATARARTS prefix (already relative)
    - Remove 00_ACTIVE/DEVELOPMENT/UTILITIES_TOOLS/
    - Remove code-projects/CODE_PROJECTS/ duplicates
    """
    parts = list(rel_path.parts)

    # Remove common intermediate directories
    patterns_to_remove = [
        ('00_ACTIVE', 'DEVELOPMENT', 'UTILITIES_TOOLS'),
        ('00_ACTIVE', 'DEVELOPMENT'),
        ('code-projects', 'CODE_PROJECTS'),
        ('04_WEBSITES', 'ai-sites', 'active', 'ORGANIZED'),
    ]

    for pattern in patterns_to_remove:
        if len(pattern) <= len(parts):
            for i in range(len(parts) - len(pattern) + 1):
                if parts[i:i+len(pattern)] == list(pattern):
                    # Remove the pattern
                    parts = parts[:i] + parts[i+len(pattern):]
                    break

    # Remove standalone intermediate directories
    intermediate_dirs = {'00_ACTIVE', 'DEVELOPMENT', 'UTILITIES_TOOLS', 'CODE_PROJECTS'}
    parts = [p for p in parts if p not in intermediate_dirs]

    return Path(*parts) if parts else Path('.')

def merge_avatarts(source_dir, target_dir, dry_run=True):
    """
    Merge AVATARARTS into target directory with flattening
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
    print(f"   Flattening: Removing intermediate directories")
    print("=" * 70)

    # Walk through source directory
    for root, dirs, files in os.walk(source):
        src_path = Path(root)
        rel_path = src_path.relative_to(source)

        # Skip .git and __pycache__ directories
        if '.git' in rel_path.parts or '__pycache__' in rel_path.parts:
            continue

        # Filter out .git and __pycache__ from dirs
        dirs[:] = [d for d in dirs if d not in ('.git', '__pycache__')]

        # Flatten the path
        flattened_path = flatten_avatarts_path(rel_path)

        # Skip if flattened to empty
        if str(flattened_path) == '.' or not flattened_path.parts:
            continue

        dst_dir = target / flattened_path

        # Create destination directory structure
        if not dry_run:
            dst_dir.mkdir(parents=True, exist_ok=True)
        else:
            if not dst_dir.exists():
                if stats['copied'] < 10:  # Only show first few
                    print(f"📁 Would create directory: {dst_dir}")

        # Process files
        for file in files:
            src_file = src_path / file
            dst_file = dst_dir / file

            # Skip hidden files
            if file.startswith('.'):
                continue

            # Only process Python files
            if src_file.suffix.lower() not in {'.py', '.pyw', '.ipynb'}:
                continue

            try:
                # Check if file exists in target
                if dst_file.exists():
                    # Files with same name exist - check if identical
                    src_hash = get_file_hash(src_file)
                    dst_hash = get_file_hash(dst_file)

                    if src_hash and dst_hash and src_hash == dst_hash:
                        # Identical files - skip
                        stats['skipped_identical'] += 1
                        continue
                    else:
                        # Different content - create versioned name
                        base_name = file.rsplit('.', 1)
                        if len(base_name) == 2:
                            name, ext = base_name
                            versioned_name = f"{name}_from_AVATARARTS.{ext}"
                        else:
                            versioned_name = f"{file}_from_AVATARARTS"

                        dst_file = dst_dir / versioned_name
                        stats['versioned'] += 1
                        if stats['versioned'] <= 5:
                            print(f"📝 Versioned: {rel_path / file} → {versioned_name}")
                else:
                    # New file - copy it
                    stats['copied'] += 1
                    if stats['copied'] <= 10:
                        print(f"✅ Would copy: {flattened_path / file}")

                # Actually copy the file
                if not dry_run:
                    shutil.copy2(src_file, dst_file)

            except Exception as e:
                stats['errors'] += 1
                if stats['errors'] <= 5:
                    print(f"❌ Error processing {src_file}: {e}")

    # Print summary
    print("\n" + "=" * 70)
    print("📊 MERGE SUMMARY:")
    print(f"   Files copied:           {stats['copied']}")
    print(f"   Files skipped (same):   {stats['skipped_identical']}")
    print(f"   Files versioned:        {stats['versioned']}")
    print(f"   Errors:                 {stats['errors']}")
    print("=" * 70)

    return stats

if __name__ == "__main__":
    import sys

    source_dir = "/Users/steven/AVATARARTS"
    target_dir = "/Users/steven/pythons"

    # Default to dry-run unless --execute is passed
    dry_run = "--execute" not in sys.argv

    if dry_run:
        print("🔍 DRY RUN MODE - No files will be modified")
        print("   Pass --execute to perform actual merge\n")
    else:
        print("⚠️  LIVE MODE - Files will be copied!")
        print("   Executing merge...\n")

    stats = merge_avatarts(source_dir, target_dir, dry_run=dry_run)

    if dry_run:
        print("\n💡 Run with --execute to perform the actual merge")

