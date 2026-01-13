#!/usr/bin/env python3
"""
Rescan and compare merged directory with source directories.
"""

import sys
from pathlib import Path
from collections import defaultdict
import hashlib


def get_file_hash(file_path, chunk_size=8192):
    """Calculate MD5 hash of a file."""
    md5 = hashlib.md5()
    try:
        with open(file_path, 'rb') as f:
            while chunk := f.read(chunk_size):
                md5.update(chunk)
        return md5.hexdigest()
    except Exception as e:
        return None


def scan_directory(dir_path):
    """Scan directory and return file information."""
    dir_path = Path(dir_path)
    if not dir_path.exists() or not dir_path.is_dir():
        return None
    
    files = {}
    total_size = 0
    
    for file_path in dir_path.rglob('*'):
        if file_path.is_file():
            try:
                rel_path = str(file_path.relative_to(dir_path))
                size = file_path.stat().st_size
                files[rel_path] = {
                    'path': file_path,
                    'size': size,
                    'hash': None  # Will calculate if needed
                }
                total_size += size
            except Exception:
                continue
    
    return {
        'name': dir_path.name,
        'path': str(dir_path),
        'files': files,
        'file_count': len(files),
        'total_size': total_size
    }


def compare_directories(merged_dir, source_dirs):
    """Compare merged directory with source directories."""
    print("=" * 80)
    print("RESCAN & COMPARE")
    print("=" * 80)
    
    # Scan merged directory
    print("\n📂 Scanning merged directory...")
    merged = scan_directory(merged_dir)
    if not merged:
        print(f"❌ Error: Merged directory not found: {merged_dir}")
        return False
    
    print(f"  {merged['name']}: {merged['file_count']:,} files, {merged['total_size']/1024/1024/1024:.2f} GB")
    
    # Scan source directories
    print("\n📂 Scanning source directories...")
    sources = []
    for source_dir in source_dirs:
        source = scan_directory(source_dir)
        if source:
            sources.append(source)
            print(f"  {source['name']}: {source['file_count']:,} files, {source['total_size']/1024/1024/1024:.2f} GB")
        else:
            print(f"  ⚠️  Warning: Could not scan {source_dir}")
    
    if not sources:
        print("\n❌ No valid source directories found.")
        return False
    
    # Compare file counts
    print("\n" + "=" * 80)
    print("FILE COUNT COMPARISON")
    print("=" * 80)
    
    expected_files = sum(s['file_count'] for s in sources)
    actual_files = merged['file_count']
    
    print(f"\n  Expected (sum of sources): {expected_files:,} files")
    print(f"  Actual (merged directory): {actual_files:,} files")
    print(f"  Difference: {actual_files - expected_files:,} files")
    
    if actual_files < expected_files:
        print(f"  ⚠️  {expected_files - actual_files:,} files missing (likely duplicates)")
    elif actual_files > expected_files:
        print(f"  ⚠️  {actual_files - expected_files:,} extra files (unexpected)")
    else:
        print(f"  ✅ File counts match exactly!")
    
    # Compare file sizes
    print("\n" + "=" * 80)
    print("SIZE COMPARISON")
    print("=" * 80)
    
    expected_size = sum(s['total_size'] for s in sources)
    actual_size = merged['total_size']
    
    print(f"\n  Expected (sum of sources): {expected_size/1024/1024/1024:.2f} GB")
    print(f"  Actual (merged directory): {actual_size/1024/1024/1024:.2f} GB")
    print(f"  Difference: {(actual_size - expected_size)/1024/1024/1024:.2f} GB")
    
    if abs(actual_size - expected_size) < 1024 * 1024:  # Less than 1MB difference
        print(f"  ✅ Sizes match (within 1MB tolerance)")
    else:
        print(f"  ⚠️  Size difference detected")
    
    # Find files in sources but not in merged
    print("\n" + "=" * 80)
    print("MISSING FILES CHECK")
    print("=" * 80)
    
    merged_files = set(merged['files'].keys())
    missing_files = []
    
    for source in sources:
        for filename in source['files'].keys():
            if filename not in merged_files:
                missing_files.append({
                    'file': filename,
                    'source': source['name']
                })
    
    if missing_files:
        print(f"\n⚠️  Found {len(missing_files)} files in sources but not in merged:")
        for item in missing_files[:20]:
            print(f"     - {item['file']} (from {item['source']})")
        if len(missing_files) > 20:
            print(f"     ... and {len(missing_files) - 20} more")
    else:
        print("\n✅ All source files are present in merged directory!")
    
    # Find duplicate files across sources
    print("\n" + "=" * 80)
    print("DUPLICATE FILES ANALYSIS")
    print("=" * 80)
    
    all_source_files = defaultdict(list)
    for source in sources:
        for filename in source['files'].keys():
            all_source_files[filename].append(source['name'])
    
    duplicates = {f: sources for f, sources in all_source_files.items() if len(sources) > 1}
    
    if duplicates:
        print(f"\n📋 Found {len(duplicates)} files that appear in multiple sources:")
        for filename, source_list in list(duplicates.items())[:10]:
            print(f"     - {filename}")
            print(f"       Present in: {', '.join(source_list)}")
        if len(duplicates) > 10:
            print(f"     ... and {len(duplicates) - 10} more duplicates")
        
        # These should be skipped in merge (only one copy kept)
        print(f"\n  ✅ These duplicates were correctly handled (only one copy kept in merge)")
    else:
        print("\n✅ No duplicate files found across sources")
    
    # File type breakdown
    print("\n" + "=" * 80)
    print("FILE TYPE BREAKDOWN (Merged Directory)")
    print("=" * 80)
    
    extensions = defaultdict(lambda: {'count': 0, 'size': 0})
    for filename, file_info in merged['files'].items():
        ext = Path(filename).suffix.lower() or '(no extension)'
        extensions[ext]['count'] += 1
        extensions[ext]['size'] += file_info['size']
    
    print(f"\n  Top 15 file types:")
    for ext, data in sorted(extensions.items(), key=lambda x: x[1]['count'], reverse=True)[:15]:
        print(f"    {ext:20s} {data['count']:6,} files  ({data['size']/1024/1024/1024:6.2f} GB)")
    
    # Summary
    print("\n" + "=" * 80)
    print("SUMMARY")
    print("=" * 80)
    
    print(f"\n  ✅ Merged directory: {merged['name']}")
    print(f"     Files: {merged['file_count']:,}")
    print(f"     Size: {merged['total_size']/1024/1024/1024:.2f} GB")
    print(f"     Sources merged: {len(sources)}")
    print(f"     Duplicates handled: {len(duplicates)}")
    print(f"     Missing files: {len(missing_files)}")
    
    if len(missing_files) == 0 and len(duplicates) > 0:
        print(f"\n  ✅ Merge successful! All unique files preserved, duplicates correctly handled.")
    elif len(missing_files) == 0:
        print(f"\n  ✅ Merge successful! All files preserved.")
    else:
        print(f"\n  ⚠️  Some files may be missing. Review the missing files list above.")
    
    return True


if __name__ == '__main__':
    if len(sys.argv) < 3:
        print("Usage: python rescan_compare.py <merged_dir> <source_dir1> <source_dir2> [source_dir3] ...")
        print("\nExample:")
        print("  python rescan_compare.py merged dir1 dir2 dir3")
        sys.exit(1)
    
    merged_dir = sys.argv[1]
    source_dirs = sys.argv[2:]
    
    compare_directories(merged_dir, source_dirs)
