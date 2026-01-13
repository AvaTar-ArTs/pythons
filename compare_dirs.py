#!/usr/bin/env python3
"""
Compare two directories to find differences, duplicates, and unique files.
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


def compare_directories(dir1, dir2, check_content=False):
    """Compare two directories."""
    print("=" * 80)
    print("DIRECTORY COMPARISON")
    print("=" * 80)
    
    # Scan both directories
    print(f"\n📂 Scanning directories...")
    
    dir1_info = scan_directory(dir1)
    dir2_info = scan_directory(dir2)
    
    if not dir1_info:
        print(f"❌ Error: Directory not found: {dir1}")
        return False
    
    if not dir2_info:
        print(f"❌ Error: Directory not found: {dir2}")
        return False
    
    print(f"  {dir1_info['name']}: {dir1_info['file_count']:,} files, {dir1_info['total_size']/1024/1024/1024:.2f} GB")
    print(f"  {dir2_info['name']}: {dir2_info['file_count']:,} files, {dir2_info['total_size']/1024/1024/1024:.2f} GB")
    
    # Compare file counts
    print("\n" + "=" * 80)
    print("FILE COUNT COMPARISON")
    print("=" * 80)
    
    print(f"\n  {dir1_info['name']}: {dir1_info['file_count']:,} files")
    print(f"  {dir2_info['name']}: {dir2_info['file_count']:,} files")
    print(f"  Difference: {abs(dir1_info['file_count'] - dir2_info['file_count']):,} files")
    
    # Compare sizes
    print("\n" + "=" * 80)
    print("SIZE COMPARISON")
    print("=" * 80)
    
    print(f"\n  {dir1_info['name']}: {dir1_info['total_size']/1024/1024/1024:.2f} GB")
    print(f"  {dir2_info['name']}: {dir2_info['total_size']/1024/1024/1024:.2f} GB")
    size_diff = dir1_info['total_size'] - dir2_info['total_size']
    print(f"  Difference: {abs(size_diff)/1024/1024/1024:.2f} GB")
    
    # Find common files
    print("\n" + "=" * 80)
    print("COMMON FILES ANALYSIS")
    print("=" * 80)
    
    files1 = set(dir1_info['files'].keys())
    files2 = set(dir2_info['files'].keys())
    
    common_files = files1 & files2
    only_in_dir1 = files1 - files2
    only_in_dir2 = files2 - files1
    
    print(f"\n  Files in both directories: {len(common_files):,}")
    print(f"  Files only in {dir1_info['name']}: {len(only_in_dir1):,}")
    print(f"  Files only in {dir2_info['name']}: {len(only_in_dir2):,}")
    
    # Check for size differences in common files
    if common_files:
        size_mismatches = []
        for filename in common_files:
            size1 = dir1_info['files'][filename]['size']
            size2 = dir2_info['files'][filename]['size']
            if size1 != size2:
                size_mismatches.append({
                    'file': filename,
                    'size1': size1,
                    'size2': size2
                })
        
        if size_mismatches:
            print(f"\n  ⚠️  Found {len(size_mismatches)} files with different sizes:")
            for item in size_mismatches[:10]:
                print(f"     - {item['file']}")
                print(f"       {dir1_info['name']}: {item['size1']:,} bytes")
                print(f"       {dir2_info['name']}: {item['size2']:,} bytes")
            if len(size_mismatches) > 10:
                print(f"     ... and {len(size_mismatches) - 10} more")
        else:
            print(f"\n  ✅ All common files have the same size")
    
    # Content comparison (if requested)
    if check_content and common_files:
        print("\n" + "=" * 80)
        print("CONTENT COMPARISON (HASH CHECK)")
        print("=" * 80)
        print("\n  Calculating file hashes (this may take a while)...")
        
        content_mismatches = []
        checked = 0
        for filename in list(common_files)[:100]:  # Limit to first 100 for performance
            checked += 1
            if checked % 10 == 0:
                print(f"    Checking {checked}/{min(100, len(common_files))} files...", end='\r')
            
            file1_path = dir1_info['files'][filename]['path']
            file2_path = dir2_info['files'][filename]['path']
            
            hash1 = get_file_hash(file1_path)
            hash2 = get_file_hash(file2_path)
            
            if hash1 and hash2 and hash1 != hash2:
                content_mismatches.append(filename)
        
        print(f"\n    Checked {checked} common files")
        if content_mismatches:
            print(f"  ⚠️  Found {len(content_mismatches)} files with different content:")
            for filename in content_mismatches[:10]:
                print(f"     - {filename}")
            if len(content_mismatches) > 10:
                print(f"     ... and {len(content_mismatches) - 10} more")
        else:
            print(f"  ✅ All checked files have identical content")
    
    # Show sample unique files
    print("\n" + "=" * 80)
    print("UNIQUE FILES")
    print("=" * 80)
    
    if only_in_dir1:
        print(f"\n  Files only in {dir1_info['name']} ({len(only_in_dir1):,} files):")
        for filename in sorted(only_in_dir1)[:15]:
            size = dir1_info['files'][filename]['size']
            print(f"     - {filename} ({size/1024/1024:.2f} MB)")
        if len(only_in_dir1) > 15:
            print(f"     ... and {len(only_in_dir1) - 15} more")
    
    if only_in_dir2:
        print(f"\n  Files only in {dir2_info['name']} ({len(only_in_dir2):,} files):")
        for filename in sorted(only_in_dir2)[:15]:
            size = dir2_info['files'][filename]['size']
            print(f"     - {filename} ({size/1024/1024:.2f} MB)")
        if len(only_in_dir2) > 15:
            print(f"     ... and {len(only_in_dir2) - 15} more")
    
    # File type breakdown
    print("\n" + "=" * 80)
    print("FILE TYPE BREAKDOWN")
    print("=" * 80)
    
    def get_extensions(files_dict):
        extensions = defaultdict(lambda: {'count': 0, 'size': 0})
        for filename, file_info in files_dict.items():
            ext = Path(filename).suffix.lower() or '(no extension)'
            extensions[ext]['count'] += 1
            extensions[ext]['size'] += file_info['size']
        return extensions
    
    ext1 = get_extensions(dir1_info['files'])
    ext2 = get_extensions(dir2_info['files'])
    
    print(f"\n  {dir1_info['name']} - Top 10 file types:")
    for ext, data in sorted(ext1.items(), key=lambda x: x[1]['count'], reverse=True)[:10]:
        print(f"    {ext:20s} {data['count']:6,} files  ({data['size']/1024/1024/1024:6.2f} GB)")
    
    print(f"\n  {dir2_info['name']} - Top 10 file types:")
    for ext, data in sorted(ext2.items(), key=lambda x: x[1]['count'], reverse=True)[:10]:
        print(f"    {ext:20s} {data['count']:6,} files  ({data['size']/1024/1024/1024:6.2f} GB)")
    
    # Summary
    print("\n" + "=" * 80)
    print("SUMMARY")
    print("=" * 80)
    
    print(f"\n  Directory 1: {dir1_info['name']}")
    print(f"    Path: {dir1_info['path']}")
    print(f"    Files: {dir1_info['file_count']:,}")
    print(f"    Size: {dir1_info['total_size']/1024/1024/1024:.2f} GB")
    
    print(f"\n  Directory 2: {dir2_info['name']}")
    print(f"    Path: {dir2_info['path']}")
    print(f"    Files: {dir2_info['file_count']:,}")
    print(f"    Size: {dir2_info['total_size']/1024/1024/1024:.2f} GB")
    
    print(f"\n  Comparison:")
    print(f"    Common files: {len(common_files):,}")
    print(f"    Unique to dir1: {len(only_in_dir1):,}")
    print(f"    Unique to dir2: {len(only_in_dir2):,}")
    
    similarity = (len(common_files) / max(len(files1), len(files2)) * 100) if max(len(files1), len(files2)) > 0 else 0
    print(f"    Similarity: {similarity:.1f}%")
    
    return True


if __name__ == '__main__':
    if len(sys.argv) < 3:
        print("Usage: python compare_dirs.py <dir1> <dir2> [--check-content]")
        print("\nExample:")
        print("  python compare_dirs.py dir1 dir2")
        print("  python compare_dirs.py dir1 dir2 --check-content")
        sys.exit(1)
    
    dir1 = sys.argv[1]
    dir2 = sys.argv[2]
    check_content = '--check-content' in sys.argv
    
    compare_directories(dir1, dir2, check_content)
