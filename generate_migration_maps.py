#!/usr/bin/env python3
"""
📋 Generate Migration Maps: Old Path → New Path
Creates CSV files showing file movements from current to organized structure
"""

import csv
import json
from pathlib import Path
from typing import Dict, List
from collections import defaultdict
import re


def load_analysis_csv(csv_file: Path) -> List[Dict]:
    """Load the analysis CSV file"""
    rows = []
    with open(csv_file, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        rows = list(reader)
    return rows


def determine_new_path(file_data: Dict, base_path: str = "~/Documents/CsV") -> str:
    """Determine new organized path for a file"""
    category = file_data.get('Category', 'Misc').strip()

    # Map category names to folder names (simplified, flat structure)
    category_map = {
        'AI/ML': 'AI-ML',
        'Data Analysis': 'Data-Analysis',
        'Media Content': 'Media',
        'Automation Scripts': 'Automation',
        'Portfolio Work': 'Portfolio',
        'Web Development': 'Web-Dev',
        'Documentation': 'Docs',
        'Configuration': 'Config',
        'Testing': 'Testing'
    }

    folder_name = category_map.get(category, 'Misc')

    # Get filename
    old_path = file_data.get('File Path', '')
    filename = Path(old_path).name if old_path else 'unknown'

    # New path: base/category/filename
    new_path = f"{base_path}/{folder_name}/{filename}"

    return new_path


def generate_migration_csv(analysis_csv: Path, output_dir: Path, base_path: str = "~/Documents/CsV"):
    """Generate migration CSV mapping old paths to new paths"""

    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    # Load analysis data
    print(f"📊 Loading analysis from: {analysis_csv}")
    file_data_list = load_analysis_csv(analysis_csv)
    print(f"   Found {len(file_data_list)} files to map")

    # Prepare migration data
    migrations = []
    by_category = defaultdict(list)
    errors = []

    for file_data in file_data_list:
        old_path = file_data.get('File Path', '').strip()
        if not old_path:
            continue

        try:
            new_path = determine_new_path(file_data, base_path)
            category = file_data.get('Category', 'Unknown')
            priority = file_data.get('Priority', '0')

            migration = {
                'Old Path': old_path,
                'New Path': new_path,
                'Filename': Path(old_path).name,
                'Category': category,
                'Priority': priority,
                'Description': file_data.get('Description', ''),
                'Status': 'Pending'  # Will be updated after migration
            }

            migrations.append(migration)
            by_category[category].append(migration)

        except Exception as e:
            errors.append({'File': old_path, 'Error': str(e)})

    # Sort migrations by priority (highest first)
    migrations.sort(key=lambda x: float(x.get('Priority', 0)), reverse=True)

    # Generate main migration CSV (all files)
    main_csv = output_dir / "migration_map_all_files.csv"
    print(f"\n📝 Generating main migration map...")
    with open(main_csv, 'w', newline='', encoding='utf-8') as f:
        fieldnames = ['Old Path', 'New Path', 'Filename', 'Category', 'Priority', 'Description', 'Status']
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(migrations)

    print(f"   ✅ Created: {main_csv.name} ({len(migrations)} files)")

    # Generate category-specific CSV files
    print(f"\n📂 Generating category-specific migration maps...")
    category_csvs = {}

    for category, files in sorted(by_category.items()):
        # Clean category name for filename
        safe_category = category.replace('/', '-').replace(' ', '-')
        category_csv = output_dir / f"migration_map_{safe_category}.csv"

        # Sort by priority
        files_sorted = sorted(files, key=lambda x: float(x.get('Priority', 0)), reverse=True)

        with open(category_csv, 'w', newline='', encoding='utf-8') as f:
            fieldnames = ['Old Path', 'New Path', 'Filename', 'Priority', 'Description', 'Status']
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            # Only write the fields we want (remove Category from dict)
            for file_data in files_sorted:
                row = {k: file_data.get(k, '') for k in fieldnames}
                writer.writerow(row)

        category_csvs[category] = category_csv.name
        print(f"   ✅ {category}: {category_csv.name} ({len(files_sorted)} files)")

    # Generate summary CSV
    summary_csv = output_dir / "migration_summary.csv"
    print(f"\n📊 Generating summary...")
    with open(summary_csv, 'w', newline='', encoding='utf-8') as f:
        fieldnames = ['Category', 'File Count', 'CSV File']
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()

        for category in sorted(by_category.keys()):
            safe_category = category.replace('/', '-').replace(' ', '-')
            writer.writerow({
                'Category': category,
                'File Count': len(by_category[category]),
                'CSV File': f"migration_map_{safe_category}.csv"
            })

    print(f"   ✅ Created: {summary_csv.name}")

    # Generate errors CSV if any
    if errors:
        errors_csv = output_dir / "migration_errors.csv"
        with open(errors_csv, 'w', newline='', encoding='utf-8') as f:
            fieldnames = ['File', 'Error']
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(errors)
        print(f"   ⚠️  Errors: {errors_csv.name} ({len(errors)} files)")

    # Print statistics
    print(f"\n" + "=" * 70)
    print(f"📈 MIGRATION STATISTICS")
    print("=" * 70)
    print(f"Total files mapped: {len(migrations)}")
    print(f"Categories: {len(by_category)}")
    print(f"\nFiles by category:")
    for category, files in sorted(by_category.items(), key=lambda x: len(x[1]), reverse=True):
        print(f"  {category:25} {len(files):4} files")

    print(f"\n💾 Migration CSV files created in: {output_dir}")
    print(f"   - Main map: migration_map_all_files.csv")
    print(f"   - Summary: migration_summary.csv")
    print(f"   - Category maps: {len(category_csvs)} files")

    return {
        'main_csv': main_csv,
        'summary_csv': summary_csv,
        'category_csvs': category_csvs,
        'total_files': len(migrations),
        'by_category': {cat: len(files) for cat, files in by_category.items()}
    }


def generate_directory_structure_csv(output_dir: Path, base_path: str = "~/Documents/CsV"):
    """Generate CSV showing the new directory structure"""

    structure = [
        {'Path': f"{base_path}/AI-ML", 'Description': 'AI/ML files (310 files)', 'Action': 'Create directory'},
        {'Path': f"{base_path}/Data-Analysis", 'Description': 'Data Analysis files (85 files)', 'Action': 'Create directory'},
        {'Path': f"{base_path}/Media", 'Description': 'Media Content files (66 files)', 'Action': 'Create directory'},
        {'Path': f"{base_path}/Automation", 'Description': 'Automation Scripts (20 files)', 'Action': 'Create directory'},
        {'Path': f"{base_path}/Portfolio", 'Description': 'Portfolio Work (11 files)', 'Action': 'Create directory'},
        {'Path': f"{base_path}/Web-Dev", 'Description': 'Web Development files (3 files)', 'Action': 'Create directory'},
        {'Path': f"{base_path}/Docs", 'Description': 'Documentation files (2 files)', 'Action': 'Create directory'},
        {'Path': f"{base_path}/Config", 'Description': 'Configuration files (2 files)', 'Action': 'Create directory'},
        {'Path': f"{base_path}/Testing", 'Description': 'Testing files (1 file)', 'Action': 'Create directory'},
        {'Path': f"{base_path}/Misc", 'Description': 'Miscellaneous files', 'Action': 'Create directory'},
    ]

    structure_csv = output_dir / "new_directory_structure.csv"
    with open(structure_csv, 'w', newline='', encoding='utf-8') as f:
        fieldnames = ['Path', 'Description', 'Action']
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(structure)

    print(f"   ✅ Directory structure: {structure_csv.name}")
    return structure_csv


def main():
    import argparse

    parser = argparse.ArgumentParser(description='Generate migration maps (old path → new path)')
    parser.add_argument('analysis_csv', type=Path,
                       help='Analysis CSV file with file paths and categories')
    parser.add_argument('--output', type=Path, default=Path('~/analysis_reports').expanduser(),
                       help='Output directory for migration CSV files')
    parser.add_argument('--base-path', default='~/Documents/CsV',
                       help='Base path for new organized structure')

    args = parser.parse_args()

    if not args.analysis_csv.exists():
        print(f"❌ Analysis CSV not found: {args.analysis_csv}")
        return

    print("=" * 70)
    print("📋 GENERATING MIGRATION MAPS (Old Path → New Path)")
    print("=" * 70)
    print()

    # Generate migration maps
    result = generate_migration_csv(args.analysis_csv, args.output, args.base_path)

    # Generate directory structure CSV
    print(f"\n🏗️  Generating directory structure CSV...")
    generate_directory_structure_csv(args.output, args.base_path)

    print("\n" + "=" * 70)
    print("✅ Migration maps generation complete!")
    print("=" * 70)
    print("\n📋 Next steps:")
    print("  1. Review migration_map_all_files.csv")
    print("  2. Review category-specific CSV files")
    print("  3. Review new_directory_structure.csv")
    print("  4. Use these CSVs to organize your files")


if __name__ == '__main__':
    main()

