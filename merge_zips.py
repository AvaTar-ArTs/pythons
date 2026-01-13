#!/usr/bin/env python3
"""
Merge multiple ZIP files into a single ZIP file.
Handles conflicts by keeping the first occurrence.
"""

import sys
import zipfile
from pathlib import Path
from collections import defaultdict
import os


def merge_zips(input_zips, output_zip, conflict_strategy='skip'):
    """
    Merge multiple ZIP files into one.
    
    Args:
        input_zips: List of input ZIP file paths
        output_zip: Output ZIP file path
        conflict_strategy: 'skip' (keep first), 'overwrite' (keep last), 'rename' (add number)
    """
    print("=" * 80)
    print("ZIP FILES MERGER")
    print("=" * 80)
    
    # Validate input files
    valid_zips = []
    for zip_path in input_zips:
        path = Path(zip_path)
        if not path.exists():
            print(f"⚠️  Warning: File not found: {zip_path}")
            continue
        if not zipfile.is_zipfile(path):
            print(f"⚠️  Warning: Not a valid ZIP file: {zip_path}")
            continue
        valid_zips.append(path)
    
    if not valid_zips:
        print("\n❌ No valid ZIP files found to merge.")
        return False
    
    print(f"\n📦 Merging {len(valid_zips)} ZIP files:")
    total_size = 0
    for zip_path in valid_zips:
        size = zip_path.stat().st_size
        total_size += size
        print(f"  - {zip_path.name} ({size/1024/1024:.2f} MB)")
    
    print(f"\n  Total input size: {total_size/1024/1024:.2f} MB ({total_size/1024/1024/1024:.2f} GB)")
    
    # Track files to detect conflicts
    seen_files = {}
    file_stats = defaultdict(int)
    conflicts = []
    
    output_path = Path(output_zip)
    if output_path.exists():
        print(f"\n⚠️  Warning: Output file exists: {output_zip}")
        response = input("  Overwrite? (y/N): ").strip().lower()
        if response != 'y':
            print("  Cancelled.")
            return False
    
    print(f"\n📝 Creating merged ZIP: {output_zip}")
    
    try:
        with zipfile.ZipFile(output_path, 'w', zipfile.ZIP_DEFLATED, compresslevel=6) as out_zip:
            for zip_idx, zip_path in enumerate(valid_zips, 1):
                print(f"\n  Processing {zip_idx}/{len(valid_zips)}: {zip_path.name}...")
                
                try:
                    with zipfile.ZipFile(zip_path, 'r') as in_zip:
                        file_list = in_zip.namelist()
                        print(f"    Found {len(file_list)} files")
                        
                        for file_idx, filename in enumerate(file_list, 1):
                            if file_idx % 100 == 0:
                                print(f"    Processing file {file_idx}/{len(file_list)}...", end='\r')
                            
                            # Check for conflicts
                            original_filename = filename
                            if filename in seen_files:
                                conflicts.append({
                                    'file': filename,
                                    'first': seen_files[filename],
                                    'duplicate': zip_path.name
                                })
                                
                                if conflict_strategy == 'skip':
                                    continue  # Skip duplicate
                                elif conflict_strategy == 'overwrite':
                                    # Will overwrite by writing again
                                    pass
                                elif conflict_strategy == 'rename':
                                    # Rename the duplicate
                                    base, ext = os.path.splitext(filename)
                                    counter = 1
                                    new_name = f"{base}_{counter}{ext}"
                                    while new_name in seen_files:
                                        counter += 1
                                        new_name = f"{base}_{counter}{ext}"
                                    filename = new_name
                            
                            # Read and write file data
                            try:
                                file_info = in_zip.getinfo(original_filename)
                                
                                # Read and write file data
                                file_data = in_zip.read(original_filename)
                                out_zip.writestr(file_info, file_data)
                                
                                if filename not in seen_files:
                                    seen_files[filename] = zip_path.name
                                
                                file_stats[zip_path.name] += 1
                                
                            except Exception as e:
                                print(f"\n    ⚠️  Error reading {original_filename}: {e}")
                                continue
                        
                        print(f"    ✓ Added {file_stats[zip_path.name]} files")
                        
                except Exception as e:
                    print(f"\n  ❌ Error processing {zip_path.name}: {e}")
                    continue
        
        # Get final stats
        with zipfile.ZipFile(output_path, 'r') as final_zip:
            final_size = output_path.stat().st_size
            final_files = len(final_zip.namelist())
        
        print("\n" + "=" * 80)
        print("MERGE COMPLETE")
        print("=" * 80)
        print(f"\n✅ Created: {output_zip}")
        print(f"   Output size: {final_size/1024/1024:.2f} MB ({final_size/1024/1024/1024:.2f} GB)")
        print(f"   Total files: {final_files}")
        print(f"   Files from each source:")
        for zip_name, count in file_stats.items():
            print(f"     - {zip_name}: {count} files")
        
        if conflicts:
            print(f"\n⚠️  Found {len(conflicts)} file conflicts (duplicates):")
            for conflict in conflicts[:10]:
                print(f"     - {conflict['file']}")
                print(f"       First in: {conflict['first']}")
                print(f"       Also in: {conflict['duplicate']}")
            if len(conflicts) > 10:
                print(f"     ... and {len(conflicts) - 10} more conflicts")
        else:
            print("\n✅ No file conflicts detected - all files are unique!")
        
        return True
        
    except Exception as e:
        print(f"\n❌ Error creating merged ZIP: {e}")
        if output_path.exists():
            output_path.unlink()
        return False


if __name__ == '__main__':
    if len(sys.argv) < 3:
        print("Usage: python merge_zips.py <output.zip> <input1.zip> <input2.zip> [input3.zip] ...")
        print("\nExample:")
        print("  python merge_zips.py merged.zip file1.zip file2.zip file3.zip")
        print("\nConflict strategies:")
        print("  --skip (default): Skip duplicate files, keep first occurrence")
        print("  --overwrite: Overwrite with last occurrence")
        print("  --rename: Rename duplicates with _1, _2, etc.")
        sys.exit(1)
    
    output_zip = sys.argv[1]
    input_zips = sys.argv[2:]
    
    # Check for conflict strategy
    conflict_strategy = 'skip'
    if '--overwrite' in input_zips:
        conflict_strategy = 'overwrite'
        input_zips.remove('--overwrite')
    elif '--rename' in input_zips:
        conflict_strategy = 'rename'
        input_zips.remove('--rename')
    
    success = merge_zips(input_zips, output_zip, conflict_strategy)
    sys.exit(0 if success else 1)
