#!/usr/bin/env python3
"""
Quick Python File Inventory Scanner
Scans all Python files across 5 locations and generates basic statistics.
"""

import csv
import hashlib
import os
import sys
from datetime import datetime
from pathlib import Path
from collections import defaultdict


def count_lines(filepath):
    """Count lines of code, skipping empty lines and comments."""
    try:
        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
            lines = f.readlines()
            total = len(lines)
            code_lines = sum(1 for line in lines if line.strip() and not line.strip().startswith('#'))
            return total, code_lines
    except Exception:
        return 0, 0


def get_file_hash(filepath):
    """Generate MD5 hash for duplicate detection."""
    try:
        with open(filepath, 'rb') as f:
            return hashlib.md5(f.read()).hexdigest()
    except Exception:
        return ""


def scan_location(location_path, location_name):
    """Scan a location for all Python files."""
    results = []
    location = Path(location_path).expanduser()

    if not location.exists():
        print(f"⚠️  {location_name}: Path does not exist - {location}")
        return results

    print(f"📂 Scanning {location_name}: {location}")

    # Find all .py files
    py_files = list(location.rglob("*.py"))
    print(f"   Found {len(py_files)} Python files")

    for i, filepath in enumerate(py_files, 1):
        if i % 500 == 0:
            print(f"   Processing {i}/{len(py_files)}...")

        try:
            stat = filepath.stat()
            total_lines, code_lines = count_lines(filepath)
            file_hash = get_file_hash(filepath)

            # Get relative path from location root
            try:
                rel_path = filepath.relative_to(location)
            except ValueError:
                rel_path = filepath

            results.append({
                'location': location_name,
                'relative_path': str(rel_path),
                'full_path': str(filepath),
                'filename': filepath.name,
                'size_bytes': stat.st_size,
                'size_kb': round(stat.st_size / 1024, 2),
                'total_lines': total_lines,
                'code_lines': code_lines,
                'last_modified': datetime.fromtimestamp(stat.st_mtime).isoformat(),
                'md5_hash': file_hash,
            })
        except Exception as e:
            print(f"   ⚠️  Error processing {filepath.name}: {e}")

    return results


def generate_statistics(all_files):
    """Generate summary statistics."""
    stats = {
        'total_files': len(all_files),
        'total_size_mb': sum(f['size_bytes'] for f in all_files) / (1024 * 1024),
        'total_lines': sum(f['total_lines'] for f in all_files),
        'total_code_lines': sum(f['code_lines'] for f in all_files),
        'by_location': defaultdict(lambda: {
            'count': 0,
            'size_mb': 0,
            'lines': 0,
            'code_lines': 0
        })
    }

    for f in all_files:
        loc = f['location']
        stats['by_location'][loc]['count'] += 1
        stats['by_location'][loc]['size_mb'] += f['size_bytes'] / (1024 * 1024)
        stats['by_location'][loc]['lines'] += f['total_lines']
        stats['by_location'][loc]['code_lines'] += f['code_lines']

    # Find duplicates by hash
    hash_groups = defaultdict(list)
    for f in all_files:
        if f['md5_hash']:
            hash_groups[f['md5_hash']].append(f)

    stats['duplicate_groups'] = {k: v for k, v in hash_groups.items() if len(v) > 1}
    stats['duplicate_file_count'] = sum(len(v) - 1 for v in stats['duplicate_groups'].values())

    return stats


def main():
    """Main execution."""
    print("\n" + "="*70)
    print("🐍 PYTHON FILE INVENTORY SCANNER")
    print("="*70 + "\n")

    # Define locations
    locations = [
        ("~/GitHub", "GitHub"),
        ("~/AVATARARTS", "AVATARARTS"),
        ("~/pythons", "pythons"),
        ("~/pythons-sort", "pythons-sort"),
        ("~/scripts", "scripts"),
    ]

    # Scan all locations
    all_files = []
    for path, name in locations:
        files = scan_location(path, name)
        all_files.extend(files)
        print(f"   ✓ {name}: {len(files)} files\n")

    # Generate statistics
    print("📊 Generating statistics...")
    stats = generate_statistics(all_files)

    # Output CSV
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_csv = f"PYTHON_INVENTORY_{timestamp}.csv"

    with open(output_csv, 'w', newline='', encoding='utf-8') as f:
        fieldnames = ['location', 'relative_path', 'full_path', 'filename',
                     'size_bytes', 'size_kb', 'total_lines', 'code_lines',
                     'last_modified', 'md5_hash']
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(all_files)

    print(f"✓ CSV written: {output_csv}\n")

    # Print summary
    print("="*70)
    print("📈 SUMMARY STATISTICS")
    print("="*70)
    print(f"\n{'Total Files:':<30} {stats['total_files']:,}")
    print(f"{'Total Size:':<30} {stats['total_size_mb']:.2f} MB")
    print(f"{'Total Lines:':<30} {stats['total_lines']:,}")
    print(f"{'Total Code Lines:':<30} {stats['total_code_lines']:,}")
    print(f"{'Duplicate Files (exact):':<30} {stats['duplicate_file_count']:,}")
    print(f"{'Duplicate Groups:':<30} {len(stats['duplicate_groups']):,}")

    print("\n" + "-"*70)
    print("BY LOCATION:")
    print("-"*70)
    print(f"{'Location':<20} {'Files':>10} {'Size (MB)':>12} {'Lines':>12} {'Code Lines':>12}")
    print("-"*70)

    for loc, data in sorted(stats['by_location'].items(),
                           key=lambda x: x[1]['count'], reverse=True):
        print(f"{loc:<20} {data['count']:>10,} {data['size_mb']:>12.2f} "
              f"{data['lines']:>12,} {data['code_lines']:>12,}")

    # Output duplicate summary
    if stats['duplicate_groups']:
        dup_csv = f"PYTHON_DUPLICATES_{timestamp}.csv"
        with open(dup_csv, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['md5_hash', 'file_count', 'locations', 'filenames', 'file_paths'])

            for hash_val, files in sorted(stats['duplicate_groups'].items(),
                                          key=lambda x: len(x[1]), reverse=True):
                locations_str = ', '.join(set(f['location'] for f in files))
                filenames = ', '.join(f['filename'] for f in files)
                paths = '\n'.join(f['full_path'] for f in files)
                writer.writerow([hash_val, len(files), locations_str, filenames, paths])

        print(f"\n✓ Duplicate report: {dup_csv}")

    print("\n" + "="*70)
    print("✓ Inventory complete!")
    print("="*70 + "\n")

    return output_csv, stats


if __name__ == "__main__":
    main()
