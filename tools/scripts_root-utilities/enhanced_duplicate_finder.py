#!/usr/bin/env python3
"""
Enhanced Duplicate Finder
More aggressive duplicate detection for home directory cleanup
"""

import csv
import re
from collections import defaultdict, Counter
from pathlib import Path

def load_csv_data(filename: str) -> list:
    """Load data from CSV file"""
    with open(filename, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        return list(reader)

def find_more_duplicates(data: list) -> list:
    """Find duplicates using more aggressive patterns"""
    duplicates = []

    # Group by filename to find same-named files in different directories
    filename_groups = defaultdict(list)
    for row in data:
        filename_groups[row['filename']].append(row)

    # Look for files with same name in different locations
    for filename, files in filename_groups.items():
        if len(files) > 1:
            # Sort by file size (keep largest)
            sorted_files = sorted(files, key=lambda x: int(x.get('file_size', 0)), reverse=True)
            keep_file = sorted_files[0]
            for remove_file in sorted_files[1:]:
                duplicates.append({
                    'file_to_remove': remove_file['filepath'],
                    'filename': remove_file['filename'],
                    'reason': f'Same filename as {keep_file["filename"]} - keep larger version',
                    'keep_file': keep_file['filepath'],
                    'keep_filename': keep_file['filename'],
                    'duplicate_type': 'Same Filename Duplicate',
                    'file_size': remove_file['file_size'],
                    'primary_purpose': remove_file['primary_purpose'],
                    'parent_folder': remove_file['parent_folder'],
                    'confidence': 'High'
                })

    # Find files with similar names (differing only by numbers)
    name_patterns = defaultdict(list)
    for row in data:
        filename = row['filename'].lower()
        # Remove numbers and common suffixes
        base_name = re.sub(r'\d+|\(|\)|\.py|_copy|_bak|_old|_new', '', filename)
        name_patterns[base_name].append(row)

    for base_name, files in name_patterns.items():
        if len(files) > 2:  # At least 3 similar files
            # Sort by size and keep the largest
            sorted_files = sorted(files, key=lambda x: int(x.get('file_size', 0)), reverse=True)
            keep_file = sorted_files[0]
            for remove_file in sorted_files[1:]:
                duplicates.append({
                    'file_to_remove': remove_file['filepath'],
                    'filename': remove_file['filename'],
                    'reason': f'Similar to {keep_file["filename"]} - consolidate variants',
                    'keep_file': keep_file['filepath'],
                    'keep_filename': keep_file['filename'],
                    'duplicate_type': 'Similar Name Variant',
                    'file_size': remove_file['file_size'],
                    'primary_purpose': remove_file['primary_purpose'],
                    'parent_folder': remove_file['parent_folder'],
                    'confidence': 'Medium'
                })

    # Find very small files that might be stubs or placeholders
    small_files = [row for row in data if int(row.get('file_size', 0)) < 100]  # Less than 100 bytes
    for small_file in small_files:
        duplicates.append({
            'file_to_remove': small_file['filepath'],
            'filename': small_file['filename'],
            'reason': 'Very small file - likely stub or placeholder',
            'keep_file': '',
            'keep_filename': '',
            'duplicate_type': 'Stub File',
            'file_size': small_file['file_size'],
            'primary_purpose': small_file['primary_purpose'],
            'parent_folder': small_file['parent_folder'],
            'confidence': 'Low'
        })

    return duplicates

def find_empty_or_minimal_files(data: list) -> list:
    """Find empty or minimal files that can be safely removed"""
    minimal_files = []

    for row in data:
        file_size = int(row.get('file_size', 0))
        line_count = int(row.get('line_count', 0))

        # Files that are essentially empty
        if file_size < 50 or line_count < 3:
            minimal_files.append({
                'file_to_remove': row['filepath'],
                'filename': row['filename'],
                'reason': f'Empty/minimal file ({line_count} lines, {file_size} bytes)',
                'keep_file': '',
                'keep_filename': '',
                'duplicate_type': 'Empty File',
                'file_size': row['file_size'],
                'primary_purpose': row['primary_purpose'],
                'parent_folder': row['parent_folder'],
                'confidence': 'High'
            })

    return minimal_files

def find_config_duplicates(data: list) -> list:
    """Find duplicate configuration files"""
    config_files = [row for row in data if 'config' in row['filename'].lower()]
    duplicates = []

    if len(config_files) > 1:
        # Keep the largest config file
        sorted_configs = sorted(config_files, key=lambda x: int(x.get('file_size', 0)), reverse=True)
        keep_file = sorted_configs[0]

        for remove_file in sorted_configs[1:]:
            duplicates.append({
                'file_to_remove': remove_file['filepath'],
                'filename': remove_file['filename'],
                'reason': f'Duplicate config file - keep {keep_file["filename"]}',
                'keep_file': keep_file['filepath'],
                'keep_filename': keep_file['filename'],
                'duplicate_type': 'Config Duplicate',
                'file_size': remove_file['file_size'],
                'primary_purpose': remove_file['primary_purpose'],
                'parent_folder': remove_file['parent_folder'],
                'confidence': 'Medium'
            })

    return duplicates

def create_comprehensive_removal_csv(data: list, filename: str):
    """Create comprehensive CSV with all removal recommendations"""
    all_duplicates = []

    # Find different types of duplicates
    filename_duplicates = find_more_duplicates(data)
    empty_files = find_empty_or_minimal_files(data)
    config_duplicates = find_config_duplicates(data)

    all_duplicates.extend(filename_duplicates)
    all_duplicates.extend(empty_files)
    all_duplicates.extend(config_duplicates)

    if not all_duplicates:
        print(f"No duplicates found to save in {filename}")
        return

    fieldnames = [
        'action_type', 'file_path', 'filename', 'reason', 'target_file', 'target_filename',
        'duplicate_type', 'file_size', 'primary_purpose', 'parent_folder', 'confidence'
    ]

    with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        for dup in all_duplicates:
            row = {
                'action_type': 'Remove',
                'file_path': dup['file_to_remove'],
                'filename': dup['filename'],
                'reason': dup['reason'],
                'target_file': dup.get('keep_file', ''),
                'target_filename': dup.get('keep_filename', ''),
                'duplicate_type': dup['duplicate_type'],
                'file_size': dup['file_size'],
                'primary_purpose': dup['primary_purpose'],
                'parent_folder': dup['parent_folder'],
                'confidence': dup['confidence']
            }
            writer.writerow(row)

    print(f"Created {filename} with {len(all_duplicates)} removal recommendations")

def main():
    """Main analysis function"""
    print("🔍 Enhanced duplicate analysis for home directory cleanup...")

    # Load data
    data = load_csv_data('home_directory_python_analysis.csv')
    print(f"Loaded {len(data)} files for enhanced analysis")

    # Find different types of removable files
    print("🔍 Finding various types of duplicates and removable files...")

    filename_duplicates = find_more_duplicates(data)
    print(f"   • Same filename duplicates: {len(filename_duplicates)}")

    empty_files = find_empty_or_minimal_files(data)
    print(f"   • Empty/minimal files: {len(empty_files)}")

    config_duplicates = find_config_duplicates(data)
    print(f"   • Config file duplicates: {len(config_duplicates)}")

    # Create comprehensive CSV
    print("💾 Creating comprehensive removal recommendations...")
    create_comprehensive_removal_csv(data, 'comprehensive_files_to_remove.csv')

    # Summary
    total_removals = len(filename_duplicates) + len(empty_files) + len(config_duplicates)

    print("\n📊 Enhanced Analysis Summary:")
    print(f"   • Total files recommended for removal: {total_removals}")
    print(f"   • Filename duplicates: {len(filename_duplicates)}")
    print(f"   • Empty/minimal files: {len(empty_files)}")
    print(f"   • Config duplicates: {len(config_duplicates)}")

    # Calculate space savings
    all_files = filename_duplicates + empty_files + config_duplicates
    space_saved = sum(int(f.get('file_size', 0)) for f in all_files if f.get('file_size', '').isdigit())
    print(f"   • Estimated space savings: ~{space_saved // 1024} KB")

    # Show breakdown by confidence
    confidence_levels = Counter(f['confidence'] for f in all_files)
    print("\n🎯 Confidence Levels:")
    for level, count in confidence_levels.most_common():
        print(f"   • {level}: {count} files")

    print("\n✅ Enhanced duplicate analysis complete!")
    print("📄 Check 'comprehensive_files_to_remove.csv' for detailed recommendations")

if __name__ == '__main__':
    main()