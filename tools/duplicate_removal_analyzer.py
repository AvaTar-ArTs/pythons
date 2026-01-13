#!/usr/bin/env python3
"""
Duplicate Removal Analyzer
Analyzes home directory Python analysis CSV and identifies files that can be removed
"""

import csv
import re
from collections import defaultdict, Counter
from pathlib import Path
from typing import List, Dict, Tuple, Set
import hashlib

def load_csv_data(filename: str) -> List[Dict]:
    """Load data from CSV file"""
    with open(filename, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        return list(reader)

def find_identical_files(data: List[Dict]) -> List[List[Dict]]:
    """Find files with identical content (same hash)"""
    hash_groups = defaultdict(list)

    for row in data:
        file_hash = row.get('hash', '')
        if file_hash and file_hash != '':
            hash_groups[file_hash].append(row)

    # Return only groups with multiple files
    return [group for group in hash_groups.values() if len(group) > 1]

def find_versioned_files(data: List[Dict]) -> List[List[Dict]]:
    """Find versioned files (numbered variants, copies, backups)"""
    versioned_groups = defaultdict(list)

    version_patterns = [
        r'[_\-\s][v]?(\d+)$',  # file_v1.py, file-2.py, file 3.py
        r'[_\-\s]copy\d*$',    # file_copy.py, file-copy1.py
        r'[_\-\s]bak\d*$',     # file_bak.py, file.bak1
        r'[_\-\s]old\d*$',     # file_old.py
        r'[_\-\s]new\d*$',     # file_new.py
        r'[_\-\s]\(\d+\)$',    # file (1).py
    ]

    for row in data:
        filename = row['filename'].lower()

        # Check if file matches version patterns
        for pattern in version_patterns:
            if re.search(pattern, filename):
                # Extract base name (remove version suffix)
                base_name = re.sub(pattern, '', filename)
                versioned_groups[base_name].append(row)
                break

    return [group for group in versioned_groups.values() if len(group) > 1]

def find_similar_functionality(data: List[Dict]) -> List[List[Dict]]:
    """Find files with similar functionality that could be merged"""
    functionality_groups = defaultdict(list)

    # Group by purpose and parent folder
    for row in data:
        purpose = row['primary_purpose']
        parent = row['parent_folder']

        # Create grouping key
        if purpose and parent:
            key = f"{purpose}__{parent}"
            functionality_groups[key].append(row)

    # Return groups with multiple files that have similar names
    similar_groups = []
    for group in functionality_groups.values():
        if len(group) > 1:
            # Check if they have similar base names
            base_names = []
            for item in group:
                filename = item['filename'].lower()
                # Remove common suffixes and extensions
                base = re.sub(r'\d+$|\(\d+\)$|_copy\d*$|_bak\d*$|\.py$', '', filename)
                base_names.append(base)

            # If most files share similar base names, they're likely duplicates
            if len(set(base_names)) <= len(base_names) // 2:  # At least 50% similarity
                similar_groups.append(group)

    return similar_groups

def find_large_duplicate_groups(data: List[Dict]) -> List[List[Dict]]:
    """Find groups of files that are clearly duplicates based on naming patterns"""
    duplicate_groups = defaultdict(list)

    for row in data:
        filename = row['filename'].lower()
        parent = row['parent_folder']

        # Look for clear duplicate patterns
        patterns = [
            (r'^(.+?)_(\d+)\.py$', r'\1'),  # file_1.py, file_2.py
            (r'^(.+?)_copy(\d*)\.py$', r'\1'),  # file_copy.py, file_copy1.py
            (r'^(.+?)\s*\((\d+)\)\.py$', r'\1'),  # file (1).py, file (2).py
            (r'^(.+?)_bak(\d*)\.py$', r'\1'),  # file_bak.py
            (r'^(.+?)_old(\d*)\.py$', r'\1'),  # file_old.py
        ]

        for pattern, replacement in patterns:
            match = re.match(pattern, filename)
            if match:
                base_name = re.sub(pattern, replacement, filename)
                key = f"{parent}__{base_name}"
                duplicate_groups[key].append(row)
                break

    return [group for group in duplicate_groups.values() if len(group) > 1]

def analyze_duplicates_for_removal(duplicate_groups: List[List[Dict]]) -> List[Dict]:
    """Analyze duplicate groups and recommend which files to keep/remove"""
    removal_recommendations = []

    for group in duplicate_groups:
        if len(group) < 2:
            continue

        # Sort by preference (keep newer, larger, more complete files)
        sorted_group = sorted(group, key=lambda x: (
            -int(x.get('file_size', 0)),  # Prefer larger files
            -int(x.get('line_count', 0)),  # Prefer more complete files
            x['filepath']  # Alphabetical fallback
        ))

        # Keep the best one, mark others for removal
        keep_file = sorted_group[0]
        remove_files = sorted_group[1:]

        for remove_file in remove_files:
            removal_recommendations.append({
                'file_to_remove': remove_file['filepath'],
                'filename': remove_file['filename'],
                'reason': 'Duplicate of better file',
                'keep_file': keep_file['filepath'],
                'keep_filename': keep_file['filename'],
                'duplicate_type': 'Content/Version Duplicate',
                'file_size': remove_file['file_size'],
                'primary_purpose': remove_file['primary_purpose'],
                'parent_folder': remove_file['parent_folder'],
                'confidence': 'High'
            })

    return removal_recommendations

def analyze_similar_for_merge(similar_groups: List[List[Dict]]) -> List[Dict]:
    """Analyze similar functionality groups for potential merging"""
    merge_recommendations = []

    for group in similar_groups:
        if len(group) < 3:  # Only consider groups with 3+ similar files
            continue

        # Group by base functionality
        base_names = defaultdict(list)
        for item in group:
            filename = item['filename'].lower()
            # Extract base name
            base = re.sub(r'\d+$|\(\d+\)$|_copy\d*$|_bak\d*$|\.py$', '', filename)
            base_names[base].append(item)

        for base_name, files in base_names.items():
            if len(files) >= 3:  # Only merge if 3+ similar files
                # Sort by size and completeness
                sorted_files = sorted(files, key=lambda x: (
                    -int(x.get('file_size', 0)),
                    -int(x.get('line_count', 0))
                ))

                keep_file = sorted_files[0]
                merge_candidates = sorted_files[1:]

                for candidate in merge_candidates:
                    merge_recommendations.append({
                        'file_to_merge': candidate['filepath'],
                        'filename': candidate['filename'],
                        'merge_strategy': 'Consolidate into unified module',
                        'target_file': keep_file['filepath'],
                        'target_filename': keep_file['filename'],
                        'merge_type': 'Similar Functionality',
                        'file_size': candidate['file_size'],
                        'primary_purpose': candidate['primary_purpose'],
                        'parent_folder': candidate['parent_folder'],
                        'confidence': 'Medium',
                        'merge_benefit': f'Consolidate {len(merge_candidates)} similar files'
                    })

    return merge_recommendations

def create_removal_csv(recommendations: List[Dict], filename: str):
    """Create CSV file with removal recommendations"""
    if not recommendations:
        print(f"No recommendations to save for {filename}")
        return

    fieldnames = [
        'action_type', 'file_path', 'filename', 'reason', 'target_file', 'target_filename',
        'duplicate_type', 'merge_type', 'file_size', 'primary_purpose', 'parent_folder',
        'confidence', 'merge_benefit'
    ]

    with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        for rec in recommendations:
            row = {
                'action_type': 'Remove' if 'file_to_remove' in rec else 'Merge',
                'file_path': rec.get('file_to_remove', rec.get('file_to_merge', '')),
                'filename': rec.get('filename', ''),
                'reason': rec.get('reason', ''),
                'target_file': rec.get('keep_file', rec.get('target_file', '')),
                'target_filename': rec.get('keep_filename', rec.get('target_filename', '')),
                'duplicate_type': rec.get('duplicate_type', ''),
                'merge_type': rec.get('merge_type', ''),
                'file_size': rec.get('file_size', ''),
                'primary_purpose': rec.get('primary_purpose', ''),
                'parent_folder': rec.get('parent_folder', ''),
                'confidence': rec.get('confidence', ''),
                'merge_benefit': rec.get('merge_benefit', ''),
            }
            writer.writerow(row)

    print(f"Created {filename} with {len(recommendations)} recommendations")

def main():
    """Main analysis function"""
    print("🔍 Analyzing duplicates for removal recommendations...")

    # Load the analysis data
    data = load_csv_data('home_directory_python_analysis.csv')
    print(f"Loaded {len(data)} files for analysis")

    # Find different types of duplicates
    print("📋 Identifying duplicate patterns...")

    identical_groups = find_identical_files(data)
    print(f"   • Identical content groups: {len(identical_groups)}")

    versioned_groups = find_versioned_files(data)
    print(f"   • Versioned file groups: {len(versioned_groups)}")

    similar_groups = find_similar_functionality(data)
    print(f"   • Similar functionality groups: {len(similar_groups)}")

    large_duplicate_groups = find_large_duplicate_groups(data)
    print(f"   • Large duplicate groups: {len(large_duplicate_groups)}")

    # Analyze for removal recommendations
    print("🗑️ Analyzing removal recommendations...")

    # Combine all duplicate groups
    all_duplicate_groups = identical_groups + versioned_groups + large_duplicate_groups

    removal_recommendations = analyze_duplicates_for_removal(all_duplicate_groups)
    print(f"   • Files recommended for removal: {len(removal_recommendations)}")

    merge_recommendations = analyze_similar_for_merge(similar_groups)
    print(f"   • Files recommended for merging: {len(merge_recommendations)}")

    # Create CSV files
    print("💾 Creating CSV reports...")

    create_removal_csv(removal_recommendations, 'files_to_remove.csv')
    create_removal_csv(merge_recommendations, 'files_to_merge.csv')

    # Summary statistics
    total_files_to_remove = len(removal_recommendations)
    total_files_to_merge = len(merge_recommendations)

    print("\n📊 Summary:")
    print(f"   • Files to remove: {total_files_to_remove}")
    print(f"   • Files to merge: {total_files_to_merge}")
    print(f"   • Total potential cleanup: {total_files_to_remove + total_files_to_merge} files")

    if total_files_to_remove > 0:
        print(f"   • Estimated space savings: ~{sum(int(r.get('file_size', 0)) for r in removal_recommendations if r.get('file_size', '').isdigit()) // 1024} KB")

    # Show top removal reasons
    removal_reasons = Counter(r['reason'] for r in removal_recommendations)
    if removal_reasons:
        print("\n🎯 Top removal reasons:")
        for reason, count in removal_reasons.most_common(3):
            print(f"   • {reason}: {count} files")

if __name__ == '__main__':
    main()