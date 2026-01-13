#!/usr/bin/env python3
"""
Duplicate File Finder
Finds exact duplicates across key directories using MD5 hashing
"""
import hashlib
from pathlib import Path
from collections import defaultdict
import csv
from datetime import datetime

def hash_file(filepath):
    """Generate MD5 hash of file"""
    hasher = hashlib.md5()
    try:
        with open(filepath, 'rb') as f:
            # Read in chunks for large files
            for chunk in iter(lambda: f.read(8192), b''):
                hasher.update(chunk)
        return hasher.hexdigest()
    except Exception as e:
        print(f"Error hashing {filepath}: {e}")
        return None

def find_duplicates(search_dirs, extensions=['*.py']):
    """Find duplicate files across directories"""
    hashes = defaultdict(list)

    print(f"Scanning {len(search_dirs)} directories for duplicates...")

    for search_dir in search_dirs:
        if not search_dir.exists():
            print(f"Skipping {search_dir} (doesn't exist)")
            continue

        print(f"  Scanning {search_dir}...")

        for ext in extensions:
            for file_path in search_dir.rglob(ext):
                if file_path.is_file():
                    file_hash = hash_file(file_path)
                    if file_hash:
                        hashes[file_hash].append({
                            'path': str(file_path),
                            'size': file_path.stat().st_size,
                            'modified': file_path.stat().st_mtime
                        })

    # Filter to only duplicates (2+ files with same hash)
    duplicates = {h: files for h, files in hashes.items() if len(files) > 1}

    return duplicates

def main():
    home = Path.home()

    # Directories to scan
    search_dirs = [
        home / 'AVATARARTS',
        home / 'GitHub',
        home / 'pythons',
        home / 'pythons-sort',
        home / 'scripts',
        home / 'Documents'
    ]

    # Find duplicates
    duplicates = find_duplicates(search_dirs, extensions=['*.py', '*.csv', '*.json'])

    # Calculate statistics
    total_duplicates = sum(len(files) - 1 for files in duplicates.values())
    wasted_space = sum((len(files) - 1) * files[0]['size'] for files in duplicates.values())

    # Generate text report
    report_file = home / 'AVATARARTS' / f'DUPLICATE_FILES_REPORT_{datetime.now().strftime("%Y%m%d_%H%M%S")}.txt'

    with open(report_file, 'w') as f:
        f.write("=" * 80 + "\n")
        f.write("DUPLICATE FILE REPORT\n")
        f.write("=" * 80 + "\n")
        f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")

        f.write(f"Total duplicate sets: {len(duplicates)}\n")
        f.write(f"Total redundant files: {total_duplicates}\n")
        f.write(f"Wasted space: {wasted_space / 1024 / 1024:.2f} MB\n\n")

        f.write("=" * 80 + "\n")
        f.write("DUPLICATE SETS (sorted by number of copies)\n")
        f.write("=" * 80 + "\n\n")

        for hash_val, files in sorted(duplicates.items(), key=lambda x: len(x[1]), reverse=True):
            f.write(f"Hash: {hash_val}\n")
            f.write(f"Copies: {len(files)}\n")
            f.write(f"Size: {files[0]['size'] / 1024:.2f} KB\n")
            f.write(f"Wasted: {(len(files) - 1) * files[0]['size'] / 1024:.2f} KB\n")
            f.write("Files:\n")
            for file_info in sorted(files, key=lambda x: x['modified']):
                f.write(f"  - {file_info['path']}\n")
            f.write("\n")

    # Generate CSV report
    csv_file = home / 'AVATARARTS' / f'DUPLICATE_FILES_{datetime.now().strftime("%Y%m%d_%H%M%S")}.csv'

    with open(csv_file, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['hash', 'copies', 'size_bytes', 'wasted_bytes', 'paths'])

        for hash_val, files in sorted(duplicates.items(), key=lambda x: len(x[1]), reverse=True):
            paths = ';'.join([f['path'] for f in files])
            writer.writerow([
                hash_val,
                len(files),
                files[0]['size'],
                (len(files) - 1) * files[0]['size'],
                paths
            ])

    print(f"\n{'=' * 80}")
    print("DUPLICATE FILE ANALYSIS COMPLETE")
    print(f"{'=' * 80}")
    print(f"Total duplicate sets: {len(duplicates)}")
    print(f"Total redundant files: {total_duplicates}")
    print(f"Wasted space: {wasted_space / 1024 / 1024:.2f} MB")
    print(f"\nReports saved:")
    print(f"  - {report_file}")
    print(f"  - {csv_file}")
    print(f"{'=' * 80}")

if __name__ == '__main__':
    main()
