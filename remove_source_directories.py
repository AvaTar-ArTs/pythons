#!/usr/bin/env python3
"""
Remove source directories after verifying merge is complete.
"""

import os
import shutil
from pathlib import Path
from datetime import datetime

SOURCE_DIRS = [
    "/Users/steven/.claude-worktrees/pythons",
    "/Users/steven/pythons-merged-backup",
    "/Users/steven/pythons-sort",
]

TARGET_DIR = "/Users/steven/pythons"

def get_directory_size(path):
    """Get number of files and total size in bytes."""
    if not os.path.exists(path):
        return 0, 0

    count = 0
    total_size = 0
    for root, dirs, files in os.walk(path):
        for file in files:
            filepath = os.path.join(root, file)
            try:
                size = os.path.getsize(filepath)
                count += 1
                total_size += size
            except (OSError, IOError):
                pass
    return count, total_size

def remove_directories():
    """Remove source directories after merge."""
    print("🗑️  Directory Removal Tool")
    print("=" * 60)
    print(f"Target directory (will be preserved): {TARGET_DIR}\n")

    # Check target exists
    if not os.path.exists(TARGET_DIR):
        print(f"❌ Error: Target directory does not exist: {TARGET_DIR}")
        return

    # Show what will be removed
    print("📋 Directories to be removed:")
    dirs_to_remove = []
    total_files = 0
    total_size = 0

    for dir_path in SOURCE_DIRS:
        if os.path.exists(dir_path):
            count, size = get_directory_size(dir_path)
            total_files += count
            total_size += size
            dirs_to_remove.append((dir_path, count, size))
            print(f"  ✓ {dir_path}")
            print(f"    Files: {count:,}, Size: {size/1024/1024:.2f} MB")
        else:
            print(f"  ✗ {dir_path} (does not exist)")

    if not dirs_to_remove:
        print("\n✅ All source directories have already been removed!")
        return

    print(f"\n📊 Summary:")
    print(f"  Total files: {total_files:,}")
    print(f"  Total size: {total_size/1024/1024:.2f} MB")
    print(f"  Directories: {len(dirs_to_remove)}")

    # Confirm
    print("\n⚠️  WARNING: This will permanently delete the source directories!")
    print("   Make sure all files have been successfully merged to ~/pythons.")
    response = input("\nProceed with removal? (type 'yes' to confirm): ").strip().lower()

    if response != 'yes':
        print("❌ Removal cancelled by user.")
        return

    # Remove directories
    print("\n🗑️  Removing directories...")
    removed = 0
    errors = 0

    for dir_path, count, size in dirs_to_remove:
        try:
            print(f"  Removing {dir_path}...")
            shutil.rmtree(dir_path)
            removed += 1
            print(f"    ✅ Removed ({count:,} files)")
        except Exception as e:
            print(f"    ❌ Error removing {dir_path}: {e}")
            errors += 1

    # Summary
    print(f"\n✅ Removal complete!")
    print(f"  Successfully removed: {removed}/{len(dirs_to_remove)} directories")
    if errors > 0:
        print(f"  Errors: {errors}")

    # Verify target still exists
    if os.path.exists(TARGET_DIR):
        count, size = get_directory_size(TARGET_DIR)
        print(f"\n📁 Target directory status:")
        print(f"  {TARGET_DIR}")
        print(f"  Files: {count:,}")
        print(f"  Size: {size/1024/1024:.2f} MB")
        print(f"\n✨ All files are now consolidated in ~/pythons!")

if __name__ == "__main__":
    try:
        remove_directories()
    except KeyboardInterrupt:
        print("\n\n⚠️  Interrupted by user.")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
