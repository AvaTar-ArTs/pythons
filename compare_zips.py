#!/usr/bin/env python3
"""
Compare multiple ZIP files to find differences, duplicates, and unique content.
"""

import sys
import zipfile
from pathlib import Path
from collections import defaultdict
from datetime import datetime


def get_zip_info(zip_path):
    """Extract information from a ZIP file."""
    try:
        with zipfile.ZipFile(zip_path, 'r') as zf:
            files = {}
            for info in zf.infolist():
                files[info.filename] = {
                    'size': info.file_size,
                    'compressed_size': info.compress_size,
                    'date': datetime(*info.date_time),
                    'crc': info.CRC
                }
            return {
                'name': zip_path.name,
                'path': str(zip_path),
                'total_files': len(files),
                'total_size': sum(f['size'] for f in files.values()),
                'total_compressed': sum(f['compressed_size'] for f in files.values()),
                'files': files,
                'file_size': zip_path.stat().st_size
            }
    except Exception as e:
        return {
            'name': zip_path.name,
            'path': str(zip_path),
            'error': str(e)
        }


def compare_zips(zip_paths):
    """Compare multiple ZIP files."""
    print("=" * 80)
    print("ZIP FILES COMPARISON")
    print("=" * 80)
    
    # Get info for all ZIPs
    zip_infos = []
    for zip_path in zip_paths:
        path = Path(zip_path)
        if not path.exists():
            print(f"\n⚠️  Warning: File not found: {zip_path}")
            continue
        info = get_zip_info(path)
        zip_infos.append(info)
        if 'error' in info:
            print(f"\n❌ Error reading {info['name']}: {info['error']}")
            continue
    
    if not zip_infos:
        print("\n❌ No valid ZIP files found to compare.")
        return
    
    # Basic statistics
    print(f"\n📦 Found {len(zip_infos)} ZIP files:\n")
    for info in zip_infos:
        if 'error' in info:
            continue
        print(f"  {info['name']}")
        print(f"    Size: {info['file_size']:,} bytes ({info['file_size']/1024/1024:.2f} MB)")
        print(f"    Files inside: {info['total_files']}")
        print(f"    Total uncompressed: {info['total_size']:,} bytes ({info['total_size']/1024/1024:.2f} MB)")
        print(f"    Total compressed: {info['total_compressed']:,} bytes ({info['total_compressed']/1024/1024:.2f} MB)")
        compression_ratio = (1 - info['total_compressed'] / info['total_size']) * 100 if info['total_size'] > 0 else 0
        print(f"    Compression ratio: {compression_ratio:.1f}%")
        print()
    
    # Collect all files from all ZIPs
    all_files = defaultdict(list)  # filename -> list of (zip_name, file_info)
    for info in zip_infos:
        if 'error' in info or 'files' not in info:
            continue
        for filename, file_info in info['files'].items():
            all_files[filename].append((info['name'], file_info))
    
    # Analyze file distribution
    print("=" * 80)
    print("FILE DISTRIBUTION ANALYSIS")
    print("=" * 80)
    
    # Files in all ZIPs
    files_in_all = [f for f, zips in all_files.items() if len(zips) == len(zip_infos)]
    print(f"\n📋 Files present in ALL {len(zip_infos)} ZIPs: {len(files_in_all)}")
    if files_in_all:
        print("   (These files appear in every ZIP file)")
        for filename in sorted(files_in_all)[:10]:
            print(f"     - {filename}")
        if len(files_in_all) > 10:
            print(f"     ... and {len(files_in_all) - 10} more")
    
    # Files in multiple ZIPs
    files_in_multiple = {f: zips for f, zips in all_files.items() if 1 < len(zips) < len(zip_infos)}
    print(f"\n📋 Files present in MULTIPLE (but not all) ZIPs: {len(files_in_multiple)}")
    if files_in_multiple:
        print("   Top files appearing in multiple ZIPs:")
        for filename, zips in sorted(files_in_multiple.items(), key=lambda x: len(x[1]), reverse=True)[:10]:
            zip_names = [z[0] for z in zips]
            print(f"     - {filename} (in {len(zips)} ZIPs: {', '.join(zip_names[:3])}{'...' if len(zip_names) > 3 else ''})")
    
    # Unique files per ZIP
    print(f"\n📋 Unique files per ZIP (files only in that ZIP):")
    for info in zip_infos:
        if 'error' in info or 'files' not in info:
            continue
        unique = [f for f in info['files'].keys() if len(all_files[f]) == 1]
        print(f"  {info['name']}: {len(unique)} unique files")
        if unique:
            for filename in sorted(unique)[:5]:
                print(f"     - {filename}")
            if len(unique) > 5:
                print(f"     ... and {len(unique) - 5} more")
    
    # File size differences
    print("\n" + "=" * 80)
    print("FILE SIZE DIFFERENCES")
    print("=" * 80)
    
    # Find files with different sizes
    size_differences = []
    for filename, zips in all_files.items():
        if len(zips) > 1:
            sizes = {z[0]: z[1]['size'] for z in zips}
            if len(set(sizes.values())) > 1:
                size_differences.append((filename, sizes))
    
    if size_differences:
        print(f"\n⚠️  Found {len(size_differences)} files with different sizes across ZIPs:")
        for filename, sizes in sorted(size_differences, key=lambda x: max(x[1].values()), reverse=True)[:10]:
            print(f"  {filename}")
            for zip_name, size in sorted(sizes.items(), key=lambda x: x[1], reverse=True):
                print(f"    {zip_name}: {size:,} bytes")
    else:
        print("\n✅ All duplicate files have the same size across ZIPs.")
    
    # CRC differences (different content even if same size)
    print("\n" + "=" * 80)
    print("CONTENT DIFFERENCES (CRC CHECK)")
    print("=" * 80)
    
    crc_differences = []
    for filename, zips in all_files.items():
        if len(zips) > 1:
            crcs = {z[0]: z[1]['crc'] for z in zips}
            if len(set(crcs.values())) > 1:
                crc_differences.append((filename, crcs))
    
    if crc_differences:
        print(f"\n⚠️  Found {len(crc_differences)} files with different content (different CRC):")
        for filename, crcs in sorted(crc_differences, key=lambda x: len(x[1]), reverse=True)[:10]:
            print(f"  {filename}")
            for zip_name, crc in sorted(crcs.items()):
                print(f"    {zip_name}: CRC {crc:08X}")
    else:
        print("\n✅ All duplicate files have identical content (same CRC).")
    
    # Summary statistics
    print("\n" + "=" * 80)
    print("SUMMARY STATISTICS")
    print("=" * 80)
    
    total_unique_files = len(all_files)
    total_file_instances = sum(len(zips) for zips in all_files.values())
    
    print(f"\n  Total unique files across all ZIPs: {total_unique_files}")
    print(f"  Total file instances: {total_file_instances}")
    print(f"  Average files per ZIP: {total_file_instances / len(zip_infos):.1f}")
    print(f"  Duplication factor: {total_file_instances / total_unique_files:.2f}x")
    
    # File type breakdown
    print(f"\n  File type breakdown:")
    extensions = defaultdict(int)
    for filename in all_files.keys():
        ext = Path(filename).suffix.lower() or '(no extension)'
        extensions[ext] += 1
    
    for ext, count in sorted(extensions.items(), key=lambda x: x[1], reverse=True)[:10]:
        print(f"    {ext}: {count} files")
    
    print("\n" + "=" * 80)
    print("COMPARISON COMPLETE")
    print("=" * 80)


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python compare_zips.py <zip1> <zip2> [zip3] ...")
        print("\nExample:")
        print("  python compare_zips.py file1.zip file2.zip file3.zip")
        sys.exit(1)
    
    zip_paths = sys.argv[1:]
    compare_zips(zip_paths)
