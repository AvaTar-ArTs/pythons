#!/usr/bin/env python3
"""
Find Duplicates by Filename and Size
More aggressive duplicate detection - finds files with same name and size.
"""

import csv
from pathlib import Path
from collections import defaultdict
from datetime import datetime

def find_duplicates_by_name_size(workspace_root: Path):
    """Find duplicates by matching filename and size."""
    
    print("🔍 Scanning for duplicates by filename and size...")
    
    file_groups = defaultdict(list)
    
    # Scan all files
    for file_path in workspace_root.rglob('*'):
        if not file_path.is_file():
            continue
        
        # Skip system files
        if file_path.name.startswith('.'):
            continue
        
        try:
            stat = file_path.stat()
            size = stat.st_size
            
            # Group by filename and size
            key = (file_path.name, size)
            file_groups[key].append({
                'path': str(file_path.relative_to(workspace_root)),
                'full_path': str(file_path),
                'size': size,
                'size_mb': size / (1024 * 1024)
            })
        except Exception:
            continue
    
    # Find groups with duplicates
    duplicates = []
    for (filename, size), files in file_groups.items():
        if len(files) > 1:
            # Sort by path depth (prefer shallower)
            files_sorted = sorted(files, key=lambda x: x['path'].count('/'))
            
            keep_file = files_sorted[0]
            duplicate_files = files_sorted[1:]
            
            total_waste = sum(f['size'] for f in duplicate_files)
            
            duplicates.append({
                'filename': filename,
                'size_mb': size / (1024 * 1024),
                'keep_path': keep_file['path'],
                'duplicate_count': len(duplicate_files),
                'waste_mb': total_waste / (1024 * 1024),
                'duplicates': duplicate_files
            })
    
    # Sort by waste (largest first)
    duplicates.sort(key=lambda x: x['waste_mb'], reverse=True)
    
    print(f"   Found {len(duplicates)} duplicate groups")
    print(f"   Total duplicate files: {sum(d['duplicate_count'] for d in duplicates)}")
    print(f"   Total waste: {sum(d['waste_mb'] for d in duplicates) / 1024:.2f} GB")
    
    return duplicates

def generate_mapping_csv(duplicates, workspace_root: Path):
    """Generate mapping CSV."""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_csv = workspace_root / f"DUPLICATES_BY_NAME_SIZE_{timestamp}.csv"
    
    print(f"\n💾 Generating mapping CSV: {output_csv.name}")
    
    mappings = []
    
    for dup_group in duplicates:
        keep_path = dup_group['keep_path']
        for dup_file in dup_group['duplicates']:
            mappings.append({
                'original_path': dup_file['path'],
                'new_path': keep_path,
                'filename': dup_group['filename'],
                'size_mb': f"{dup_group['size_mb']:.2f}",
                'waste_mb': f"{dup_group['waste_mb']:.2f}"
            })
    
    with open(output_csv, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=['original_path', 'new_path', 'filename', 'size_mb', 'waste_mb'])
        writer.writeheader()
        writer.writerows(mappings)
    
    print(f"✅ CSV created: {output_csv}")
    print(f"   Total mappings: {len(mappings):,}")
    
    # Show top duplicates
    print(f"\n📊 Top 20 duplicate groups by waste:")
    for i, dup in enumerate(duplicates[:20], 1):
        print(f"   {i:2d}. {dup['filename']}")
        print(f"       {dup['duplicate_count']} duplicates, {dup['waste_mb']:.2f} MB waste")
        print(f"       Keep: {dup['keep_path']}")
    
    return output_csv

def main():
    """Main execution."""
    print("=" * 80)
    print("DUPLICATE FINDER - BY FILENAME AND SIZE")
    print("=" * 80)
    print()
    
    workspace_root = Path("/Users/steven/AVATARARTS")
    
    # Find duplicates
    duplicates = find_duplicates_by_name_size(workspace_root)
    
    if not duplicates:
        print("\n✅ No duplicates found!")
        return
    
    # Generate mapping CSV
    mapping_csv = generate_mapping_csv(duplicates, workspace_root)
    
    print(f"\n{'='*80}")
    print("✅ ANALYSIS COMPLETE")
    print(f"{'='*80}")
    print(f"\n📄 Mapping CSV: {mapping_csv.name}")
    print(f"💡 Use this CSV to remove duplicates")
    print()

if __name__ == "__main__":
    main()
