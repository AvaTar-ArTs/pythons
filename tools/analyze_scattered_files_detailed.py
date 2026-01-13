#!/usr/bin/env python3
"""
Scattered Files Detailed Analysis
Identifies files that exist in multiple locations and determines if they're duplicates
"""

import csv
import hashlib
from collections import defaultdict
from pathlib import Path
from datetime import datetime


def get_file_hash(filepath):
    """Get MD5 hash of file."""
    try:
        with open(filepath, 'rb') as f:
            return hashlib.md5(f.read()).hexdigest()
    except Exception:
        return None


def analyze_scattered_files(inventory_file):
    """Analyze files scattered across multiple locations."""
    print(f"\n{'='*70}")
    print("SCATTERED FILES DETAILED ANALYSIS")
    print(f"{'='*70}\n")

    # Load inventory
    files_by_name = defaultdict(list)

    with open(inventory_file, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            files_by_name[row['filename']].append({
                'location': row['location'],
                'path': row['full_path'],
                'size_kb': float(row['size_kb']),
                'md5': row['md5_hash'],
                'code_lines': int(row['code_lines'])
            })

    # Find scattered files
    scattered = {name: files for name, files in files_by_name.items()
                 if len(files) > 1}

    print(f"Total unique filenames: {len(files_by_name):,}")
    print(f"Files in multiple locations: {len(scattered):,}\n")

    # Categorize scattered files
    categories = {
        'exact_duplicates': [],      # Same content across locations
        'different_content': [],      # Same name, different content
        'package_files': []           # __init__.py, __main__.py (expected)
    }

    for filename, locations in scattered.items():
        # Skip common package files
        if filename in ['__init__.py', '__main__.py', '__pycache__']:
            categories['package_files'].append((filename, locations))
            continue

        # Check if all copies have same hash
        hashes = set(loc['md5'] for loc in locations if loc['md5'])

        if len(hashes) == 1:
            # Exact duplicates
            categories['exact_duplicates'].append((filename, locations))
        else:
            # Different content
            categories['different_content'].append((filename, locations))

    return categories, scattered


def generate_report(categories, scattered):
    """Generate detailed report."""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    # CSV report
    csv_file = f"SCATTERED_FILES_REPORT_{timestamp}.csv"
    with open(csv_file, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['filename', 'location_count', 'category', 'locations',
                        'unique_hashes', 'total_size_kb', 'paths'])

        for category_name, items in categories.items():
            if category_name == 'package_files':
                continue  # Skip package files in report

            for filename, locations in sorted(items, key=lambda x: len(x[1]), reverse=True):
                hashes = set(loc['md5'] for loc in locations if loc['md5'])
                total_size = sum(loc['size_kb'] for loc in locations)
                loc_names = ', '.join(set(loc['location'] for loc in locations))
                paths = ' | '.join(loc['path'] for loc in locations)

                writer.writerow([
                    filename,
                    len(locations),
                    category_name,
                    loc_names,
                    len(hashes),
                    f"{total_size:.2f}",
                    paths
                ])

    # Markdown summary
    md_file = f"SCATTERED_FILES_SUMMARY_{timestamp}.md"
    with open(md_file, 'w', encoding='utf-8') as f:
        f.write("# Scattered Files Analysis\n\n")
        f.write(f"**Generated:** {datetime.now().isoformat()}\n\n")

        # Summary stats
        total_scattered = sum(len(items) for items in categories.values())
        total_exact_dupes = len(categories['exact_duplicates'])
        total_different = len(categories['different_content'])

        f.write("## Summary\n\n")
        f.write(f"- **Total Scattered Files:** {total_scattered}\n")
        f.write(f"- **Exact Duplicates:** {total_exact_dupes} (same content, can be consolidated)\n")
        f.write(f"- **Different Content:** {total_different} (same name, different implementations)\n")
        f.write(f"- **Package Files:** {len(categories['package_files'])} (expected duplicates)\n\n")

        # Exact duplicates section
        f.write("## Exact Duplicates (High Priority)\n\n")
        f.write("These files have identical content across multiple locations. **Action:** Keep one canonical copy, delete others.\n\n")

        sorted_dupes = sorted(categories['exact_duplicates'],
                            key=lambda x: len(x[1]), reverse=True)

        for i, (filename, locations) in enumerate(sorted_dupes[:30], 1):
            location_counts = {}
            for loc in locations:
                location_counts[loc['location']] = location_counts.get(loc['location'], 0) + 1

            f.write(f"### {i}. {filename} ({len(locations)} copies)\n\n")
            f.write("**Locations:**\n")
            for loc_name, count in sorted(location_counts.items(), key=lambda x: x[1], reverse=True):
                f.write(f"- {loc_name}: {count} file(s)\n")

            f.write(f"\n**Size:** {locations[0]['size_kb']:.2f} KB per copy\n")
            f.write(f"**Total waste:** {sum(loc['size_kb'] for loc in locations[1:]):.2f} KB\n\n")

            f.write("**Paths:**\n")
            for loc in locations[:5]:  # Show first 5
                f.write(f"- `{loc['path']}`\n")
            if len(locations) > 5:
                f.write(f"- ... and {len(locations) - 5} more\n")
            f.write("\n---\n\n")

        # Different content section
        f.write("## Different Content (Medium Priority)\n\n")
        f.write("These files share the same name but have different implementations. **Action:** Rename or merge intelligently.\n\n")

        sorted_diff = sorted(categories['different_content'],
                           key=lambda x: len(x[1]), reverse=True)

        for i, (filename, locations) in enumerate(sorted_diff[:20], 1):
            hashes = set(loc['md5'] for loc in locations if loc['md5'])
            location_counts = {}
            for loc in locations:
                location_counts[loc['location']] = location_counts.get(loc['location'], 0) + 1

            f.write(f"### {i}. {filename} ({len(locations)} copies, {len(hashes)} unique versions)\n\n")
            f.write("**Locations:**\n")
            for loc_name, count in sorted(location_counts.items(), key=lambda x: x[1], reverse=True):
                f.write(f"- {loc_name}: {count} file(s)\n")
            f.write("\n")

            # Group by hash
            by_hash = defaultdict(list)
            for loc in locations:
                if loc['md5']:
                    by_hash[loc['md5']].append(loc)

            f.write(f"**Versions:**\n")
            for j, (hash_val, locs) in enumerate(by_hash.items(), 1):
                f.write(f"- Version {j}: {len(locs)} file(s), {locs[0]['code_lines']} lines\n")

            f.write("\n---\n\n")

    print(f"✓ Generated reports:")
    print(f"  - {csv_file}")
    print(f"  - {md_file}\n")

    return csv_file, md_file


def main():
    """Main execution."""
    # Find latest inventory
    inventory_files = sorted(Path('.').glob('PYTHON_INVENTORY_*.csv'), reverse=True)

    if not inventory_files:
        print("❌ No inventory file found. Run quick_python_inventory.py first.")
        return

    inventory_file = inventory_files[0]

    # Analyze
    categories, scattered = analyze_scattered_files(str(inventory_file))

    # Stats
    print(f"📊 BREAKDOWN:\n")
    print(f"Exact Duplicates:   {len(categories['exact_duplicates']):4,} files")
    print(f"Different Content:  {len(categories['different_content']):4,} files")
    print(f"Package Files:      {len(categories['package_files']):4,} files")

    # Calculate waste
    total_waste_kb = 0
    for filename, locations in categories['exact_duplicates']:
        # All copies except one are waste
        total_waste_kb += sum(loc['size_kb'] for loc in locations[1:])

    print(f"\n💾 Space wasted by exact duplicates: {total_waste_kb/1024:.2f} MB\n")

    # Generate reports
    csv_file, md_file = generate_report(categories, scattered)

    # Summary
    print(f"{'='*70}")
    print("NEXT STEPS")
    print(f"{'='*70}\n")
    print("1. Review SCATTERED_FILES_SUMMARY_*.md for consolidation plan")
    print("2. For exact duplicates: keep canonical location, delete others")
    print("3. For different content: investigate and merge/rename as needed")
    print(f"\n✓ See {md_file} for detailed recommendations\n")


if __name__ == "__main__":
    main()
