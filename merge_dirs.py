#!/usr/bin/env python3
"""
Simply merge multiple directories into one directory.
"""

import sys
import shutil
from pathlib import Path
from collections import defaultdict


def merge_directories(input_dirs, output_dir):
    """Merge multiple directories into one."""
    print("=" * 80)
    print("DIRECTORY MERGER")
    print("=" * 80)
    
    # Validate input directories
    valid_dirs = []
    total_files = 0
    for dir_path in input_dirs:
        path = Path(dir_path)
        if not path.exists():
            print(f"⚠️  Warning: Directory not found: {dir_path}")
            continue
        if not path.is_dir():
            print(f"⚠️  Warning: Not a directory: {dir_path}")
            continue
        valid_dirs.append(path)
        file_count = sum(1 for f in path.rglob('*') if f.is_file())
        total_files += file_count
        print(f"  - {path.name}: {file_count} files")
    
    if not valid_dirs:
        print("\n❌ No valid directories found to merge.")
        return False
    
    print(f"\n  Total files to merge: {total_files}")
    
    output_path = Path(output_dir)
    if output_path.exists():
        print(f"\n⚠️  Warning: Output directory exists: {output_dir}")
        print("  Removing existing directory...")
        shutil.rmtree(output_path)
    
    output_path.mkdir(parents=True, exist_ok=True)
    print(f"\n📝 Merging into: {output_dir}")
    
    seen_files = {}
    file_stats = defaultdict(int)
    conflicts = []
    files_copied = 0
    
    for dir_idx, source_dir in enumerate(valid_dirs, 1):
        print(f"\n  Processing {dir_idx}/{len(valid_dirs)}: {source_dir.name}...")
        
        for source_file in source_dir.rglob('*'):
            if source_file.is_file():
                # Get relative path
                try:
                    rel_path = source_file.relative_to(source_dir)
                    dest_file = output_path / rel_path
                    
                    # Check for conflicts
                    if dest_file.exists():
                        conflicts.append({
                            'file': str(rel_path),
                            'first': seen_files.get(str(rel_path), 'unknown'),
                            'duplicate': source_dir.name
                        })
                        # Skip duplicates (keep first)
                        continue
                    
                    # Create parent directories
                    dest_file.parent.mkdir(parents=True, exist_ok=True)
                    
                    # Copy file
                    shutil.copy2(source_file, dest_file)
                    seen_files[str(rel_path)] = source_dir.name
                    file_stats[source_dir.name] += 1
                    files_copied += 1
                    
                    if files_copied % 100 == 0:
                        print(f"    Copied {files_copied} files...", end='\r')
                        
                except Exception as e:
                    print(f"\n    ⚠️  Error copying {source_file}: {e}")
                    continue
    
    print(f"\n    ✓ Copied {files_copied} files")
    
    # Final stats
    final_files = sum(1 for f in output_path.rglob('*') if f.is_file())
    final_size = sum(f.stat().st_size for f in output_path.rglob('*') if f.is_file())
    
    print("\n" + "=" * 80)
    print("MERGE COMPLETE")
    print("=" * 80)
    print(f"\n✅ Merged into: {output_dir}")
    print(f"   Total files: {final_files}")
    print(f"   Total size: {final_size/1024/1024:.2f} MB ({final_size/1024/1024/1024:.2f} GB)")
    print(f"   Files from each source:")
    for dir_name, count in file_stats.items():
        print(f"     - {Path(dir_name).name}: {count} files")
    
    if conflicts:
        print(f"\n⚠️  Found {len(conflicts)} file conflicts (duplicates skipped):")
        for conflict in conflicts[:10]:
            print(f"     - {conflict['file']}")
        if len(conflicts) > 10:
            print(f"     ... and {len(conflicts) - 10} more")
    else:
        print("\n✅ No file conflicts - all files are unique!")
    
    return True


if __name__ == '__main__':
    if len(sys.argv) < 3:
        print("Usage: python merge_dirs.py <output_dir> <dir1> <dir2> [dir3] ...")
        print("\nExample:")
        print("  python merge_dirs.py merged_dir dir1 dir2 dir3")
        sys.exit(1)
    
    output_dir = sys.argv[1]
    input_dirs = sys.argv[2:]
    
    success = merge_directories(input_dirs, output_dir)
    sys.exit(0 if success else 1)
