#!/usr/bin/env python3
"""
Merge source directory into destination directory, then remove source.
"""

import sys
import shutil
from pathlib import Path
from collections import defaultdict


def merge_into_destination(source_dir, dest_dir, remove_source=True):
    """Merge source directory into destination, then optionally remove source."""
    print("=" * 80)
    print("MERGE AND REMOVE")
    print("=" * 80)
    
    source_path = Path(source_dir)
    dest_path = Path(dest_dir)
    
    # Validate directories
    if not source_path.exists() or not source_path.is_dir():
        print(f"❌ Error: Source directory not found: {source_dir}")
        return False
    
    if not dest_path.exists() or not dest_path.is_dir():
        print(f"❌ Error: Destination directory not found: {dest_dir}")
        return False
    
    # Scan both directories
    print(f"\n📂 Scanning directories...")
    
    def scan_dir(dir_path):
        files = {}
        total_size = 0
        for file_path in dir_path.rglob('*'):
            if file_path.is_file():
                try:
                    rel_path = str(file_path.relative_to(dir_path))
                    size = file_path.stat().st_size
                    files[rel_path] = {
                        'path': file_path,
                        'size': size
                    }
                    total_size += size
                except Exception:
                    continue
        return files, total_size
    
    source_files, source_size = scan_dir(source_path)
    dest_files, dest_size = scan_dir(dest_path)
    
    print(f"  Source ({source_path.name}): {len(source_files):,} files, {source_size/1024/1024/1024:.2f} GB")
    print(f"  Destination ({dest_path.name}): {len(dest_files):,} files, {dest_size/1024/1024/1024:.2f} GB")
    
    # Find duplicates
    duplicates = []
    for filename in source_files.keys():
        if filename in dest_files:
            duplicates.append(filename)
    
    print(f"\n  Duplicate files found: {len(duplicates)}")
    if duplicates:
        print(f"  (These will be skipped - keeping files already in destination)")
        for dup in duplicates[:10]:
            print(f"    - {dup}")
        if len(duplicates) > 10:
            print(f"    ... and {len(duplicates) - 10} more")
    
    # Copy unique files
    print(f"\n📝 Copying unique files from {source_path.name} to {dest_path.name}...")
    
    files_copied = 0
    files_skipped = 0
    errors = []
    
    for filename, file_info in source_files.items():
        if filename in duplicates:
            files_skipped += 1
            continue
        
        source_file = file_info['path']
        dest_file = dest_path / filename
        
        try:
            # Create parent directories
            dest_file.parent.mkdir(parents=True, exist_ok=True)
            
            # Copy file
            shutil.copy2(source_file, dest_file)
            files_copied += 1
            
            if files_copied % 100 == 0:
                print(f"    Copied {files_copied} files...", end='\r')
                
        except Exception as e:
            errors.append({'file': filename, 'error': str(e)})
            continue
    
    print(f"\n    ✓ Copied {files_copied} files")
    if files_skipped > 0:
        print(f"    ⚠️  Skipped {files_skipped} duplicate files")
    if errors:
        print(f"    ❌ Errors copying {len(errors)} files")
        for err in errors[:5]:
            print(f"       - {err['file']}: {err['error']}")
    
    # Verify merge
    print(f"\n📊 Verifying merge...")
    final_files, final_size = scan_dir(dest_path)
    print(f"  Final destination: {len(final_files):,} files, {final_size/1024/1024/1024:.2f} GB")
    
    # Remove source directory
    if remove_source:
        print(f"\n🗑️  Removing source directory: {source_path}")
        try:
            shutil.rmtree(source_path)
            print(f"  ✓ Successfully removed {source_path.name}")
        except Exception as e:
            print(f"  ❌ Error removing source directory: {e}")
            return False
    
    # Summary
    print("\n" + "=" * 80)
    print("MERGE COMPLETE")
    print("=" * 80)
    print(f"\n✅ Merged into: {dest_path}")
    print(f"   Files copied: {files_copied:,}")
    print(f"   Duplicates skipped: {files_skipped:,}")
    print(f"   Final file count: {len(final_files):,}")
    print(f"   Final size: {final_size/1024/1024/1024:.2f} GB")
    
    if remove_source:
        print(f"\n✅ Source directory removed: {source_path.name}")
    
    return True


if __name__ == '__main__':
    if len(sys.argv) < 3:
        print("Usage: python merge_and_remove.py <source_dir> <dest_dir> [--keep-source]")
        print("\nExample:")
        print("  python merge_and_remove.py source dest")
        print("  python merge_and_remove.py source dest --keep-source")
        sys.exit(1)
    
    source_dir = sys.argv[1]
    dest_dir = sys.argv[2]
    remove_source = '--keep-source' not in sys.argv
    
    success = merge_into_destination(source_dir, dest_dir, remove_source)
    sys.exit(0 if success else 1)
