#!/usr/bin/env python3
"""
Duplicate Detection, Merge Analysis, and Deduplication Tool
Finds duplicates, identifies merge opportunities, shows differences
"""

import os
import hashlib
import json
from pathlib import Path
from collections import defaultdict
import subprocess

def calculate_file_hash(filepath):
    """Calculate MD5 hash of file"""
    try:
        hash_md5 = hashlib.md5()
        with open(filepath, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hash_md5.update(chunk)
        return hash_md5.hexdigest()
    except:
        return None

def get_dir_signature(dirpath):
    """Get signature of directory (name + file count + total size)"""
    try:
        file_count = sum(1 for f in Path(dirpath).rglob('*') if f.is_file())
        result = subprocess.run(['du', '-sk', dirpath], capture_output=True, text=True)
        if result.returncode == 0:
            size_kb = int(result.stdout.split()[0])
            return f"{Path(dirpath).name}_{file_count}_{size_kb}"
    except:
        pass
    return None

def get_dir_content_hash(dirpath):
    """Calculate content hash of directory based on all files inside"""
    file_hashes = []
    try:
        for filepath in Path(dirpath).rglob('*'):
            if filepath.is_file():
                file_hash = calculate_file_hash(str(filepath))
                if file_hash:
                    # Include relative path and hash
                    rel_path = filepath.relative_to(dirpath)
                    file_hashes.append(f"{rel_path}:{file_hash}")
    except:
        pass

    # Sort to ensure consistent ordering
    file_hashes.sort()
    # Create combined hash
    combined = '\n'.join(file_hashes)
    if combined:
        return hashlib.md5(combined.encode()).hexdigest()
    return None

def find_duplicate_directories(root_path):
    """Find directories with similar names that might be duplicates - CONTENT BASED"""
    root = Path(root_path)
    potential_duplicates = []

    print("Scanning for duplicate directories by CONTENT...")

    # Find all directories
    all_dirs = []
    for dirpath in root.rglob('*'):
        if dirpath.is_dir() and not dirpath.name.startswith('.'):
            all_dirs.append(dirpath)

    print(f"Found {len(all_dirs)} directories. Analyzing content...")

    # Group by normalized name first (for efficiency)
    name_groups = defaultdict(list)
    for dirpath in all_dirs:
        name_lower = dirpath.name.lower()
        normalized = name_lower.replace(' ', '-').replace('_', '-')
        normalized = normalized.replace('copy', '').replace('duplicate', '')
        normalized = normalized.strip('-')
        name_groups[normalized].append(dirpath)

    # For groups with multiple entries, compare actual content
    processed = 0
    for normalized, dirs in name_groups.items():
        if len(dirs) > 1:
            processed += 1
            if processed % 10 == 0:
                print(f"  Processing group {processed}/{len([g for g in name_groups.values() if len(g) > 1])}...")

            # Calculate content hash for each directory
            dir_info = []
            content_hashes = {}

            for d in dirs:
                size = get_dir_size(str(d))
                content_hash = get_dir_content_hash(str(d))

                info = {
                    'path': str(d.relative_to(root)),
                    'size_bytes': size,
                    'content_hash': content_hash
                }
                dir_info.append(info)

                # Group by content hash
                if content_hash:
                    if content_hash not in content_hashes:
                        content_hashes[content_hash] = []
                    content_hashes[content_hash].append(info)

            # Find directories with identical content hashes
            for content_hash, matching_dirs in content_hashes.items():
                if len(matching_dirs) > 1:
                    sizes = [d['size_bytes'] for d in matching_dirs]
                    size_ratio = min(sizes) / max(sizes) if max(sizes) > 0 else 0

                    potential_duplicates.append({
                        'normalized_name': normalized,
                        'directories': matching_dirs,
                        'similarity': 1.0 if content_hash else size_ratio,  # 100% if same hash
                        'content_hash': content_hash
                    })

    return potential_duplicates

def find_duplicate_files(root_path):
    """Find duplicate files by hash - COMPARE ALL FILES"""
    root = Path(root_path)
    file_hashes = defaultdict(list)

    print("Scanning ALL files for duplicates by content hash...")

    # Get ALL files (not just samples)
    all_files = []
    for filepath in root.rglob('*'):
        if filepath.is_file() and not filepath.name.startswith('.'):
            try:
                size = filepath.stat().st_size
                if size < 500 * 1024 * 1024:  # Files under 500MB (increased limit)
                    all_files.append((filepath, size))
            except:
                pass

    # Sort by size (check smaller files first)
    all_files.sort(key=lambda x: x[1])

    print(f"Checking {len(all_files)} files for duplicates by content...")

    # Process in batches to show progress
    batch_size = 500
    for i in range(0, len(all_files), batch_size):
        batch = all_files[i:i+batch_size]
        if i % (batch_size * 5) == 0:
            print(f"  Processed {i}/{len(all_files)} files...")

        for filepath, size in batch:
            file_hash = calculate_file_hash(str(filepath))
            if file_hash:
                file_hashes[file_hash].append({
                    'path': str(filepath.relative_to(root)),
                    'size': size
                })

    # Find duplicates
    duplicates = {h: files for h, files in file_hashes.items() if len(files) > 1}

    print(f"Found {len(duplicates)} groups of duplicate files by content")

    return duplicates

def get_dir_size(path):
    """Get directory size in bytes"""
    try:
        result = subprocess.run(['du', '-sk', path], capture_output=True, text=True)
        if result.returncode == 0:
            size_kb = int(result.stdout.split()[0])
            return size_kb * 1024
    except:
        pass
    return 0

def analyze_similar_folders(root_path):
    """Find folders that might be similar/duplicates based on analysis data"""
    analysis_file = Path(root_path) / 'directory_analysis.json'

    if not analysis_file.exists():
        return []

    with open(analysis_file) as f:
        data = json.load(f)

    flat_structure = data.get('flat_structure', [])

    # Group by normalized name
    name_groups = defaultdict(list)
    for item in flat_structure:
        name_lower = item['name'].lower()
        normalized = name_lower.replace(' ', '-').replace('_', '-')
        normalized = normalized.replace('copy', '').replace('duplicate', '').strip('-')
        name_groups[normalized].append(item)

    # Find similar folders
    similar_folders = []
    for normalized, items in name_groups.items():
        if len(items) > 1:
            # Filter by similar size
            sizes = [item['size_bytes'] for item in items]
            if max(sizes) > 0:
                size_ratio = min(sizes) / max(sizes)
                if size_ratio > 0.7:  # 70% similar
                    similar_folders.append({
                        'name': normalized,
                        'items': items,
                        'similarity': size_ratio,
                        'total_waste_mb': (sum(sizes) - max(sizes)) / (1024*1024)
                    })

    return similar_folders

def create_merge_plan(similar_folders, duplicates):
    """Create plan for merging and deduplication"""
    merge_plan = []

    # Handle similar folders
    for group in similar_folders:
        items = sorted(group['items'], key=lambda x: x['size_bytes'], reverse=True)
        keep = items[0]  # Keep largest
        remove = items[1:]  # Remove others

        merge_plan.append({
            'type': 'folder_duplicate',
            'action': 'merge',
            'keep': keep['path'],
            'remove': [item['path'] for item in remove],
            'waste_mb': group['total_waste_mb'],
            'similarity': group['similarity']
        })

    # Handle duplicate files
    total_file_waste = 0
    for file_hash, files in duplicates.items():
        if len(files) > 1:
            files_sorted = sorted(files, key=lambda x: x['size'])
            keep = files_sorted[0]  # Keep first
            remove = files_sorted[1:]

            waste = sum(f['size'] for f in remove)
            total_file_waste += waste

            merge_plan.append({
                'type': 'file_duplicate',
                'action': 'remove',
                'keep': keep['path'],
                'remove': [f['path'] for f in remove],
                'waste_mb': waste / (1024*1024),
                'hash': file_hash
            })

    return merge_plan, total_file_waste / (1024*1024)

def main():
    root_path = Path('.')

    print("="*80)
    print("DUPLICATE DETECTION & DEDUPLICATION ANALYSIS")
    print("="*80)
    print()

    # Find duplicate directories
    print("1. Finding duplicate directories...")
    dup_dirs = find_duplicate_directories(root_path)

    print(f"\nFound {len(dup_dirs)} potential duplicate directory groups")
    print("-" * 80)

    total_waste_mb = 0
    for dup_group in sorted(dup_dirs, key=lambda x: max(d['size_bytes'] for d in x['directories']), reverse=True)[:20]:
        dirs = dup_group['directories']
        sizes = [d['size_bytes'] / (1024*1024) for d in dirs]
        waste = sum(sizes) - max(sizes)
        total_waste_mb += waste

        print(f"\n{dup_group['normalized_name']}:")
        print(f"  Similarity: {dup_group['similarity']*100:.1f}%")
        print(f"  Potential waste: {waste:.1f} MB")
        for d in dirs:
            size_mb = d['size_bytes'] / (1024*1024)
            print(f"    - {d['path']:60} {size_mb:8.1f} MB")

    # Find similar folders from analysis
    print("\n" + "="*80)
    print("2. Analyzing similar folders from structure analysis...")
    similar = analyze_similar_folders(root_path)

    print(f"\nFound {len(similar)} similar folder groups")
    print("-" * 80)

    for group in sorted(similar, key=lambda x: x['total_waste_mb'], reverse=True)[:20]:
        print(f"\n{group['name']}:")
        print(f"  Similarity: {group['similarity']*100:.1f}%")
        print(f"  Total waste: {group['total_waste_mb']:.1f} MB")
        for item in sorted(group['items'], key=lambda x: x['size_bytes'], reverse=True):
            size_mb = item['size_bytes'] / (1024*1024)
            print(f"    - {item['path']:60} {size_mb:8.1f} MB")
        total_waste_mb += group['total_waste_mb']

    # Find duplicate files
    print("\n" + "="*80)
    print("3. Finding duplicate files...")
    dup_files = find_duplicate_files(root_path)

    print(f"\nFound {len(dup_files)} duplicate file groups")

    file_waste_mb = 0
    for file_hash, files in list(dup_files.items())[:20]:
        waste = sum(f['size'] for f in files[1:]) / (1024*1024)
        file_waste_mb += waste
        print(f"\nHash: {file_hash[:16]}... ({len(files)} copies, {waste:.2f} MB waste)")
        for f in files:
            print(f"    - {f['path']}")

    # Create merge plan
    print("\n" + "="*80)
    print("4. Creating merge/deduplication plan...")
    merge_plan, total_file_waste = create_merge_plan(similar, dup_files)

    # Save results
    results = {
        'duplicate_directories': dup_dirs,
        'similar_folders': similar,
        'duplicate_files': {h: files for h, files in list(dup_files.items())[:100]},
        'merge_plan': merge_plan,
        'summary': {
            'total_duplicate_dirs': len(dup_dirs),
            'total_similar_folders': len(similar),
            'total_duplicate_files': len(dup_files),
            'estimated_waste_mb': total_waste_mb + total_file_waste,
            'merge_actions': len(merge_plan)
        }
    }

    with open('dedupe_analysis.json', 'w') as f:
        json.dump(results, f, indent=2)

    print("\n" + "="*80)
    print("SUMMARY")
    print("="*80)
    print(f"Duplicate directory groups: {len(dup_dirs)}")
    print(f"Similar folder groups: {len(similar)}")
    print(f"Duplicate file groups: {len(dup_files)}")
    print(f"Estimated total waste: {total_waste_mb + total_file_waste:.1f} MB")
    print(f"Merge actions recommended: {len(merge_plan)}")
    print(f"\nDetailed analysis saved to: dedupe_analysis.json")
    print("="*80)

if __name__ == "__main__":
    main()

