#!/usr/bin/env python3
"""
Check for empty files and directories.
"""

import sys
from pathlib import Path
from collections import defaultdict


def check_empty(root_path):
    """Find empty files and directories."""
    print("=" * 80)
    print("EMPTY FILES & DIRECTORIES CHECK")
    print("=" * 80)
    
    root_path = Path(root_path)
    if not root_path.exists():
        print(f"❌ Error: Directory not found: {root_path}")
        return False
    
    print(f"\n📂 Checking: {root_path}")
    
    empty_files = []
    empty_dirs = []
    total_size = 0
    
    # Check files
    print(f"\n📋 Scanning files...")
    for file_path in root_path.rglob('*'):
        if file_path.is_file():
            try:
                size = file_path.stat().st_size
                if size == 0:
                    empty_files.append(file_path)
                total_size += size
            except Exception:
                pass
    
    # Check directories
    print(f"📁 Scanning directories...")
    for dir_path in root_path.rglob('*'):
        if dir_path.is_dir():
            try:
                if not any(dir_path.iterdir()):
                    empty_dirs.append(dir_path)
            except Exception:
                pass
    
    print(f"\n📊 RESULTS")
    print(f"=" * 80)
    
    print(f"\n📭 EMPTY FILES: {len(empty_files)}")
    if empty_files:
        # Group by extension
        by_ext = defaultdict(list)
        for f in empty_files:
            ext = f.suffix.lower() or '(no extension)'
            by_ext[ext].append(f)
        
        print(f"\n   By file type:")
        for ext, files in sorted(by_ext.items(), key=lambda x: len(x[1]), reverse=True):
            print(f"     {ext:20s} {len(files):4d} files")
        
        print(f"\n   Sample empty files:")
        for file_path in sorted(empty_files)[:20]:
            rel_path = file_path.relative_to(root_path)
            print(f"     - {rel_path}")
        if len(empty_files) > 20:
            print(f"     ... and {len(empty_files) - 20} more")
    else:
        print("   ✅ No empty files found")
    
    print(f"\n📁 EMPTY DIRECTORIES: {len(empty_dirs)}")
    if empty_dirs:
        # Group by depth
        by_depth = defaultdict(list)
        for d in empty_dirs:
            depth = len(str(d.relative_to(root_path)).split('/'))
            by_depth[depth].append(d)
        
        print(f"\n   By depth level:")
        for depth in sorted(by_depth.keys()):
            print(f"     Depth {depth}: {len(by_depth[depth])} directories")
        
        print(f"\n   Sample empty directories:")
        for dir_path in sorted(empty_dirs)[:30]:
            rel_path = dir_path.relative_to(root_path)
            print(f"     - {rel_path}")
        if len(empty_dirs) > 30:
            print(f"     ... and {len(empty_dirs) - 30} more")
    else:
        print("   ✅ No empty directories found")
    
    # Summary
    print(f"\n" + "=" * 80)
    print("SUMMARY")
    print("=" * 80)
    print(f"\n  Empty files: {len(empty_files)}")
    print(f"  Empty directories: {len(empty_dirs)}")
    print(f"  Total items to clean: {len(empty_files) + len(empty_dirs)}")
    
    if empty_files or empty_dirs:
        print(f"\n💡 Use --remove to delete empty files and directories")
    
    return {
        'empty_files': empty_files,
        'empty_dirs': empty_dirs
    }


def remove_empty(root_path, empty_files, empty_dirs, dry_run=True):
    """Remove empty files and directories."""
    print(f"\n" + "=" * 80)
    print("REMOVING EMPTY FILES & DIRECTORIES")
    print("=" * 80)
    
    if dry_run:
        print(f"\n⚠️  DRY RUN MODE - No files will be deleted")
        print(f"   Use --execute to actually remove")
    
    removed_files = 0
    removed_dirs = 0
    errors = []
    
    # Remove empty files
    if empty_files:
        print(f"\n🗑️  Removing {len(empty_files)} empty files...")
        for file_path in empty_files:
            if not dry_run:
                try:
                    file_path.unlink()
                    removed_files += 1
                except Exception as e:
                    errors.append(f"{file_path.relative_to(root_path)}: {e}")
            else:
                removed_files += 1
        
        if not dry_run:
            print(f"   ✓ Removed {removed_files} empty files")
        else:
            print(f"   [DRY RUN] Would remove {removed_files} empty files")
    
    # Remove empty directories (deepest first)
    if empty_dirs:
        # Sort by depth (deepest first) so we can remove nested empty dirs
        sorted_dirs = sorted(empty_dirs, key=lambda d: len(str(d.relative_to(root_path)).split('/')), reverse=True)
        
        print(f"\n🗑️  Removing {len(sorted_dirs)} empty directories...")
        for dir_path in sorted_dirs:
            if not dry_run:
                try:
                    dir_path.rmdir()
                    removed_dirs += 1
                except Exception as e:
                    # Directory might not be empty anymore or already removed
                    pass
            else:
                removed_dirs += 1
        
        if not dry_run:
            print(f"   ✓ Removed {removed_dirs} empty directories")
        else:
            print(f"   [DRY RUN] Would remove {removed_dirs} empty directories")
    
    if errors:
        print(f"\n⚠️  Errors ({len(errors)}):")
        for error in errors[:5]:
            print(f"   - {error}")
    
    return removed_files, removed_dirs


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python check_empty.py <directory> [--remove] [--execute]")
        print("\nExample:")
        print("  python check_empty.py /path/to/dir          # Check only")
        print("  python check_empty.py /path/to/dir --remove # Dry run removal")
        print("  python check_empty.py /path/to/dir --remove --execute # Actually remove")
        sys.exit(1)
    
    root_path = sys.argv[1]
    should_remove = '--remove' in sys.argv
    dry_run = '--execute' not in sys.argv
    
    results = check_empty(root_path)
    
    if should_remove and results:
        remove_empty(Path(root_path), results['empty_files'], results['empty_dirs'], dry_run)
        
        if not dry_run:
            print(f"\n✅ Cleanup complete!")
