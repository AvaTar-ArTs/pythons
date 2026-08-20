#!/usr/bin/env python3
"""
Remove files with 'merge' or 'diff' in their names.
"""

import sys
from pathlib import Path


def remove_merge_diff_files(root_path, dry_run=True):
    """Find and remove files with 'merge' or 'diff' in name."""
    print("=" * 80)
    print("REMOVE MERGE & DIFF FILES")
    print("=" * 80)
    
    root_path = Path(root_path)
    if not root_path.exists():
        print(f"❌ Error: Directory not found: {root_path}")
        return False
    
    print(f"\n📂 Searching in: {root_path}")
    
    # Find all files
    merge_files = []
    diff_files = []
    
    for file_path in root_path.rglob('*'):
        if file_path.is_file():
            name_lower = file_path.name.lower()
            if 'merge' in name_lower:
                merge_files.append(file_path)
            if 'diff' in name_lower:
                diff_files.append(file_path)
    
    # Remove duplicates (files with both merge and diff)
    all_files = list(set(merge_files + diff_files))
    
    print(f"\n📋 Found files:")
    print(f"   With 'merge' in name: {len(merge_files)}")
    print(f"   With 'diff' in name: {len(diff_files)}")
    print(f"   Total unique files: {len(all_files)}")
    
    if all_files:
        print(f"\n   Files to remove:")
        for file_path in sorted(all_files):
            rel_path = file_path.relative_to(root_path)
            size = file_path.stat().st_size / 1024 / 1024
            print(f"     - {rel_path} ({size:.2f} MB)")
        
        if not dry_run:
            print(f"\n🗑️  Removing {len(all_files)} files...")
            removed_count = 0
            errors = []
            
            for file_path in all_files:
                try:
                    file_path.unlink()
                    removed_count += 1
                except Exception as e:
                    errors.append(f"{file_path.relative_to(root_path)}: {e}")
            
            print(f"   ✓ Removed {removed_count} files")
            if errors:
                print(f"   ⚠️  Errors ({len(errors)}):")
                for error in errors[:5]:
                    print(f"     - {error}")
        else:
            print(f"\n   [DRY RUN] Would remove {len(all_files)} files")
            print(f"   Use --execute to actually remove files")
    else:
        print(f"\n   ✅ No files with 'merge' or 'diff' in name found")
    
    return all_files


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python remove_merge_diff.py <directory> [--execute]")
        print("\nExample:")
        print("  python remove_merge_diff.py /path/to/dir          # Dry run")
        print("  python remove_merge_diff.py /path/to/dir --execute # Actually remove")
        sys.exit(1)
    
    root_path = sys.argv[1]
    dry_run = '--execute' not in sys.argv
    
    print(f"Mode: {'DRY RUN' if dry_run else 'EXECUTE'}")
    if dry_run:
        print("⚠️  DRY RUN MODE - No files will be deleted")
        print("   Use --execute flag to actually remove files\n")
    
    removed = remove_merge_diff_files(root_path, dry_run)
    
    if not dry_run and removed:
        print(f"\n✅ Cleanup complete! Removed {len(removed)} files")
