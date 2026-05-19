#!/usr/bin/env python3
"""
Reorganize ~/pythons by removing numeric prefixes (01_, 02_, 03_, etc.)
Cleans up directory and file names
"""

import os
import shutil
from pathlib import Path
import re

def remove_numeric_prefix(name):
    """
    Remove numeric prefixes like 01_, 02_, 03_ from directory/file names
    """
    # Match pattern like "01_NAME" or "01_NAME.txt"
    match = re.match(r'^(\d+)_(.+)$', name)
    if match:
        return match.group(2)
    return name

def reorganize_directory(root_dir, dry_run=True):
    """
    Reorganize directory by removing numeric prefixes
    """
    root = Path(root_dir).expanduser().resolve()

    if not root.exists():
        print(f"❌ Directory does not exist: {root}")
        return

    stats = {
        'directories_renamed': 0,
        'files_renamed': 0,
        'conflicts': 0,
        'errors': 0
    }

    conflicts = []

    print(f"\n🔄 Reorganizing: {root}")
    print(f"   Mode: {'DRY RUN' if dry_run else 'LIVE'}")
    print(f"   Action: Removing numeric prefixes (01_, 02_, etc.)")
    print("=" * 70)

    # First pass: collect all renames to check for conflicts
    renames = []

    # Process directories and files - sort by depth (deepest first) so parent renames don't break child paths
    all_items = []
    for item in root.rglob('*'):
        if not item.exists():
            continue
        # Skip .git and __pycache__
        if '.git' in item.parts or '__pycache__' in item.parts:
            continue
        all_items.append(item)

    # Sort by depth (deepest first) and reverse path (so children before parents)
    all_items.sort(key=lambda x: (-len(x.parts), str(x)[::-1]))

    for item in all_items:
        rel_path = item.relative_to(root)
        original_name = item.name

        # Check if name has numeric prefix
        new_name = remove_numeric_prefix(original_name)

        if new_name != original_name:
            new_path = item.parent / new_name

            # Check for conflicts
            if new_path.exists() and new_path != item:
                conflicts.append({
                    'type': 'directory' if item.is_dir() else 'file',
                    'old': str(rel_path),
                    'new': str(new_path.relative_to(root)),
                    'conflict_with': str(new_path.relative_to(root))
                })
                stats['conflicts'] += 1
            else:
                renames.append({
                    'item': item,
                    'old_name': original_name,
                    'new_name': new_name,
                    'old_path': rel_path,
                    'new_path': new_path,
                    'is_dir': item.is_dir(),
                    'depth': len(item.parts)
                })

    # Show conflicts first
    if conflicts:
        print(f"\n⚠️  CONFLICTS FOUND ({len(conflicts)}):")
        for conflict in conflicts[:10]:
            print(f"   {conflict['old']} → {conflict['new']} (conflicts with existing)")
        if len(conflicts) > 10:
            print(f"   ... and {len(conflicts) - 10} more conflicts")
        print()

    # Sort renames by depth (deepest first) so parent renames don't break child paths
    renames.sort(key=lambda x: -x.get('depth', 0))

    # Separate directories and files for display
    dir_renames = [r for r in renames if r['is_dir']]
    file_renames = [r for r in renames if not r['is_dir']]

    print(f"\n📁 Directories to rename ({len(dir_renames)}):")
    for rename in dir_renames[:20]:
        old_path_str = str(rename['old_path'])
        print(f"   {old_path_str:50} → {rename['new_name']}")
    if len(dir_renames) > 20:
        print(f"   ... and {len(dir_renames) - 20} more directories")

    print(f"\n📄 Files to rename ({len(file_renames)}):")
    for rename in file_renames[:20]:
        old_path_str = str(rename['old_path'])
        print(f"   {old_path_str:50} → {rename['new_name']}")
    if len(file_renames) > 20:
        print(f"   ... and {len(file_renames) - 20} more files")

    # Execute renames (deepest first)
    if not dry_run:
        print(f"\n🔄 Executing renames (deepest first)...")
        for rename in renames:
            try:
                # Re-check path since parents may have been renamed
                if not rename['item'].exists():
                    continue
                rename['item'].rename(rename['new_path'])
                if rename['is_dir']:
                    stats['directories_renamed'] += 1
                else:
                    stats['files_renamed'] += 1
            except Exception as e:
                if stats['errors'] < 5:
                    print(f"      ❌ Error renaming {rename['old_path']}: {e}")
                stats['errors'] += 1

    # Print summary
    print("\n" + "=" * 70)
    print("📊 REORGANIZATION SUMMARY:")
    print(f"   Directories renamed:    {stats['directories_renamed']}")
    print(f"   Files renamed:          {stats['files_renamed']}")
    print(f"   Conflicts:              {stats['conflicts']}")
    print(f"   Errors:                 {stats['errors']}")
    print("=" * 70)

    return stats

if __name__ == "__main__":
    import sys

    target_dir = "/Users/steven/pythons"

    # Default to dry-run unless --execute is passed
    dry_run = "--execute" not in sys.argv

    if dry_run:
        print("🔍 DRY RUN MODE - No files will be modified")
        print("   Pass --execute to perform actual reorganization\n")
    else:
        print("⚠️  LIVE MODE - Files will be renamed!")
        print("   Executing reorganization...\n")

    stats = reorganize_directory(target_dir, dry_run=dry_run)

    if dry_run:
        print("\n💡 Run with --execute to perform the actual reorganization")

