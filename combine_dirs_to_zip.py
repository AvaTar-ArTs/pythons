#!/usr/bin/env python3
"""
Combine multiple directories into a single ZIP file.
"""

import sys
import zipfile
from pathlib import Path
from collections import defaultdict
import os


def add_directory_to_zip(zip_file, dir_path, base_path=None, seen_files=None, file_stats=None):
    """Recursively add directory contents to ZIP file."""
    if seen_files is None:
        seen_files = {}
    if file_stats is None:
        file_stats = defaultdict(int)
    
    dir_path = Path(dir_path)
    if base_path is None:
        base_path = dir_path
    
    if not dir_path.exists():
        return seen_files, file_stats
    
    conflicts = []
    files_added = 0
    
    for item in dir_path.rglob('*'):
        if item.is_file():
            # Get relative path from base directory
            try:
                rel_path = item.relative_to(base_path)
                arcname = str(rel_path)
                
                # Check for conflicts
                if arcname in seen_files:
                    conflicts.append({
                        'file': arcname,
                        'first': seen_files[arcname],
                        'duplicate': str(base_path)
                    })
                    # Skip duplicates (keep first occurrence)
                    continue
                
                # Read and add file
                try:
                    with open(item, 'rb') as f:
                        file_data = f.read()
                    
                    zip_file.writestr(arcname, file_data)
                    seen_files[arcname] = str(base_path)
                    file_stats[str(base_path)] += 1
                    files_added += 1
                    
                except Exception as e:
                    print(f"    ⚠️  Error reading {arcname}: {e}")
                    continue
                    
            except ValueError:
                # File is outside base path (shouldn't happen)
                continue
    
    return seen_files, file_stats, conflicts, files_added


def combine_dirs_to_zip(input_dirs, output_zip):
    """Combine multiple directories into a single ZIP file."""
    print("=" * 80)
    print("DIRECTORY COMBINER")
    print("=" * 80)
    
    # Validate input directories
    valid_dirs = []
    total_size = 0
    for dir_path in input_dirs:
        path = Path(dir_path)
        if not path.exists():
            print(f"⚠️  Warning: Directory not found: {dir_path}")
            continue
        if not path.is_dir():
            print(f"⚠️  Warning: Not a directory: {dir_path}")
            continue
        valid_dirs.append(path)
        
        # Calculate total size
        dir_size = sum(f.stat().st_size for f in path.rglob('*') if f.is_file())
        total_size += dir_size
        file_count = sum(1 for f in path.rglob('*') if f.is_file())
        print(f"  - {path.name}: {file_count} files, {dir_size/1024/1024:.2f} MB")
    
    if not valid_dirs:
        print("\n❌ No valid directories found to combine.")
        return False
    
    print(f"\n  Total input size: {total_size/1024/1024:.2f} MB ({total_size/1024/1024/1024:.2f} GB)")
    
    output_path = Path(output_zip)
    if output_path.exists():
        print(f"\n⚠️  Warning: Output file exists: {output_zip}")
        print("  Removing existing file...")
        output_path.unlink()
    
    print(f"\n📝 Creating combined ZIP: {output_zip}")
    
    seen_files = {}
    file_stats = defaultdict(int)
    all_conflicts = []
    
    try:
        with zipfile.ZipFile(output_path, 'w', zipfile.ZIP_DEFLATED, compresslevel=6) as out_zip:
            for dir_idx, dir_path in enumerate(valid_dirs, 1):
                print(f"\n  Processing {dir_idx}/{len(valid_dirs)}: {dir_path.name}...")
                
                seen_files, file_stats, conflicts, files_added = add_directory_to_zip(
                    out_zip, dir_path, dir_path, seen_files, file_stats
                )
                
                all_conflicts.extend(conflicts)
                print(f"    ✓ Added {files_added} files")
                if conflicts:
                    print(f"    ⚠️  Skipped {len(conflicts)} duplicate files")
        
        # Get final stats
        final_size = output_path.stat().st_size
        with zipfile.ZipFile(output_path, 'r') as final_zip:
            final_files = len(final_zip.namelist())
        
        print("\n" + "=" * 80)
        print("COMBINE COMPLETE")
        print("=" * 80)
        print(f"\n✅ Created: {output_zip}")
        print(f"   Output size: {final_size/1024/1024:.2f} MB ({final_size/1024/1024/1024:.2f} GB)")
        print(f"   Total files: {final_files}")
        print(f"   Files from each source:")
        for dir_name, count in file_stats.items():
            print(f"     - {Path(dir_name).name}: {count} files")
        
        if all_conflicts:
            print(f"\n⚠️  Found {len(all_conflicts)} file conflicts (duplicates):")
            for conflict in all_conflicts[:10]:
                print(f"     - {conflict['file']}")
                print(f"       First in: {Path(conflict['first']).name}")
                print(f"       Also in: {Path(conflict['duplicate']).name}")
            if len(all_conflicts) > 10:
                print(f"     ... and {len(all_conflicts) - 10} more conflicts")
        else:
            print("\n✅ No file conflicts detected - all files are unique!")
        
        return True
        
    except Exception as e:
        print(f"\n❌ Error creating combined ZIP: {e}")
        import traceback
        traceback.print_exc()
        if output_path.exists():
            output_path.unlink()
        return False


if __name__ == '__main__':
    if len(sys.argv) < 3:
        print("Usage: python combine_dirs_to_zip.py <output.zip> <dir1> <dir2> [dir3] ...")
        print("\nExample:")
        print("  python combine_dirs_to_zip.py merged.zip dir1 dir2 dir3")
        sys.exit(1)
    
    output_zip = sys.argv[1]
    input_dirs = sys.argv[2:]
    
    success = combine_dirs_to_zip(input_dirs, output_zip)
    sys.exit(0 if success else 1)
