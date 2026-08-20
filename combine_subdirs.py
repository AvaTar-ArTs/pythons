#!/usr/bin/env python3
"""
Combine two subdirectories, merging their contents.
"""

import sys
import shutil
from pathlib import Path
from collections import defaultdict


def combine_subdirectories(source1, source2, output_dir=None):
    """Combine two directories into one."""
    print("=" * 80)
    print("SUBDIRECTORY COMBINER")
    print("=" * 80)
    
    source1_path = Path(source1)
    source2_path = Path(source2)
    
    # Validate directories
    if not source1_path.exists() or not source1_path.is_dir():
        print(f"❌ Error: Directory not found: {source1}")
        return False
    
    if not source2_path.exists() or not source2_path.is_dir():
        print(f"❌ Error: Directory not found: {source2}")
        return False
    
    # Determine output directory
    if output_dir is None:
        # Use the first source as the output (merge into it)
        output_path = source1_path
        merge_into_first = True
    else:
        output_path = Path(output_dir)
        merge_into_first = False
    
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
    
    files1, size1 = scan_dir(source1_path)
    files2, size2 = scan_dir(source2_path)
    
    print(f"  {source1_path.name}: {len(files1):,} files, {size1/1024/1024:.2f} MB")
    print(f"  {source2_path.name}: {len(files2):,} files, {size2/1024/1024:.2f} MB")
    
    # Find duplicates
    duplicates = []
    for filename in files2.keys():
        if filename in files1:
            duplicates.append(filename)
    
    print(f"\n  Duplicate files found: {len(duplicates)}")
    if duplicates:
        print(f"  (These will be skipped - keeping files from first directory)")
        for dup in duplicates[:10]:
            print(f"    - {dup}")
        if len(duplicates) > 10:
            print(f"    ... and {len(duplicates) - 10} more")
    
    # Merge strategy
    if merge_into_first:
        print(f"\n📝 Merging into: {source1_path}")
        print(f"   (Files from {source2_path.name} will be copied to {source1_path.name})")
    else:
        if output_path.exists():
            print(f"\n⚠️  Warning: Output directory exists: {output_dir}")
            print("  Removing existing directory...")
            shutil.rmtree(output_path)
        output_path.mkdir(parents=True, exist_ok=True)
        print(f"\n📝 Creating merged directory: {output_dir}")
    
    # Copy files
    files_copied = 0
    files_skipped = 0
    
    # First, copy all files from source1 (if creating new output)
    if not merge_into_first:
        print(f"\n  Copying files from {source1_path.name}...")
        for filename, file_info in files1.items():
            source_file = file_info['path']
            dest_file = output_path / filename
            dest_file.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(source_file, dest_file)
            files_copied += 1
            if files_copied % 100 == 0:
                print(f"    Copied {files_copied} files...", end='\r')
    
    # Then, copy unique files from source2
    print(f"\n  Copying unique files from {source2_path.name}...")
    for filename, file_info in files2.items():
        if filename in duplicates:
            files_skipped += 1
            continue
        
        source_file = file_info['path']
        if merge_into_first:
            dest_file = source1_path / filename
        else:
            dest_file = output_path / filename
        
        dest_file.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source_file, dest_file)
        files_copied += 1
        
        if files_copied % 100 == 0:
            print(f"    Copied {files_copied} files...", end='\r')
    
    print(f"\n    ✓ Copied {files_copied} files")
    if files_skipped > 0:
        print(f"    ⚠️  Skipped {files_skipped} duplicate files")
    
    # Final stats
    final_path = source1_path if merge_into_first else output_path
    final_files = sum(1 for f in final_path.rglob('*') if f.is_file())
    final_size = sum(f.stat().st_size for f in final_path.rglob('*') if f.is_file())
    
    print("\n" + "=" * 80)
    print("COMBINE COMPLETE")
    print("=" * 80)
    print(f"\n✅ Combined directory: {final_path}")
    print(f"   Total files: {final_files:,}")
    print(f"   Total size: {final_size/1024/1024:.2f} MB ({final_size/1024/1024/1024:.2f} GB)")
    print(f"   Files from {source1_path.name}: {len(files1):,}")
    print(f"   Files from {source2_path.name}: {len(files2) - len(duplicates):,} (unique)")
    print(f"   Duplicates skipped: {len(duplicates)}")
    
    # Optionally remove the second directory if merged into first
    if merge_into_first:
        print(f"\n💡 Note: {source2_path.name} still exists. Remove it? (y/N): ", end='')
        try:
            response = input().strip().lower()
            if response == 'y':
                shutil.rmtree(source2_path)
                print(f"  ✓ Removed {source2_path.name}")
        except:
            pass
    
    return True


if __name__ == '__main__':
    if len(sys.argv) < 3:
        print("Usage: python combine_subdirs.py <dir1> <dir2> [output_dir]")
        print("\nExample:")
        print("  python combine_subdirs.py dir1 dir2")
        print("  python combine_subdirs.py dir1 dir2 merged_output")
        sys.exit(1)
    
    source1 = sys.argv[1]
    source2 = sys.argv[2]
    output_dir = sys.argv[3] if len(sys.argv) > 3 else None
    
    success = combine_subdirectories(source1, source2, output_dir)
    sys.exit(0 if success else 1)
