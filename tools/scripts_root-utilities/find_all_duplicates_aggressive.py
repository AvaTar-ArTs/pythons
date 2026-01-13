#!/usr/bin/env python3
"""
Aggressive Duplicate Finder
Finds duplicates by:
1. Same filename + size (already done)
2. Same filename in multiple locations (scattered)
3. Deep nested folder patterns
"""

import csv
from pathlib import Path
from collections import defaultdict
from datetime import datetime

def find_all_duplicates(workspace_root: Path):
    """Find all types of duplicates."""
    
    print("🔍 Aggressive duplicate scanning...")
    
    # Method 1: Same filename + size
    print("\n1️⃣  Scanning for files with same name and size...")
    name_size_groups = defaultdict(list)
    
    for file_path in workspace_root.rglob('*'):
        if not file_path.is_file() or file_path.name.startswith('.'):
            continue
        
        try:
            stat = file_path.stat()
            key = (file_path.name.lower(), stat.st_size)
            name_size_groups[key].append({
                'path': str(file_path.relative_to(workspace_root)),
                'size': stat.st_size
            })
        except:
            continue
    
    # Method 2: Same filename (any size) - scattered files
    print("2️⃣  Scanning for files with same name (scattered)...")
    name_groups = defaultdict(list)
    
    for file_path in workspace_root.rglob('*'):
        if not file_path.is_file() or file_path.name.startswith('.'):
            continue
        
        try:
            stat = file_path.stat()
            name_groups[file_path.name.lower()].append({
                'path': str(file_path.relative_to(workspace_root)),
                'size': stat.st_size,
                'size_mb': stat.st_size / (1024 * 1024)
            })
        except:
            continue
    
    # Method 3: Check for nested patterns
    print("3️⃣  Checking for nested folder patterns...")
    nested_patterns = defaultdict(list)
    
    for file_path in workspace_root.rglob('*'):
        if not file_path.is_file():
            continue
        
        rel_path = str(file_path.relative_to(workspace_root))
        parts = Path(rel_path).parts
        
        # Look for repeated folder names
        for i in range(len(parts) - 1):
            if parts[i] == parts[i+1]:
                pattern = parts[i]
                nested_patterns[pattern].append({
                    'path': rel_path,
                    'depth': len(parts)
                })
                break
    
    # Process results
    duplicates = []
    
    # Process name+size duplicates
    for (filename, size), files in name_size_groups.items():
        if len(files) > 1:
            files_sorted = sorted(files, key=lambda x: x['path'].count('/'))
            keep = files_sorted[0]
            for dup in files_sorted[1:]:
                duplicates.append({
                    'original_path': dup['path'],
                    'new_path': keep['path'],
                    'filename': filename,
                    'method': 'name_size',
                    'size_mb': size / (1024 * 1024)
                })
    
    # Process scattered files (same name, different sizes might still be duplicates)
    for filename, files in name_groups.items():
        if len(files) > 1:
            # Group by size
            size_groups = defaultdict(list)
            for f in files:
                size_groups[f['size']].append(f)
            
            # For each size group with multiple files, mark as duplicates
            for size, size_files in size_groups.items():
                if len(size_files) > 1:
                    size_files_sorted = sorted(size_files, key=lambda x: x['path'].count('/'))
                    keep = size_files_sorted[0]
                    for dup in size_files_sorted[1:]:
                        duplicates.append({
                            'original_path': dup['path'],
                            'new_path': keep['path'],
                            'filename': filename,
                            'method': 'scattered',
                            'size_mb': size / (1024 * 1024)
                        })
    
    print(f"\n✅ Found {len(duplicates)} duplicate files")
    
    # Calculate waste
    total_waste = sum(d['size_mb'] for d in duplicates)
    print(f"   Total waste: {total_waste / 1024:.2f} GB")
    
    # Show nested patterns
    if nested_patterns:
        print(f"\n⚠️  Found nested folder patterns:")
        for pattern, files in sorted(nested_patterns.items(), key=lambda x: len(x[1]), reverse=True)[:10]:
            print(f"   - {pattern}: {len(files)} files (max depth: {max(f['depth'] for f in files)})")
    
    return duplicates

def generate_csv(duplicates, workspace_root: Path):
    """Generate mapping CSV."""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_csv = workspace_root / f"ALL_DUPLICATES_{timestamp}.csv"
    
    print(f"\n💾 Generating CSV: {output_csv.name}")
    
    with open(output_csv, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=['original_path', 'new_path', 'filename', 'method', 'size_mb'])
        writer.writeheader()
        writer.writerows(duplicates)
    
    print(f"✅ CSV created: {output_csv}")
    print(f"   Total mappings: {len(duplicates):,}")
    
    return output_csv

def main():
    """Main execution."""
    print("=" * 80)
    print("AGGRESSIVE DUPLICATE FINDER")
    print("=" * 80)
    print()
    
    workspace_root = Path("/Users/steven/AVATARARTS")
    
    duplicates = find_all_duplicates(workspace_root)
    
    if duplicates:
        csv_file = generate_csv(duplicates, workspace_root)
        
        print(f"\n{'='*80}")
        print("✅ ANALYSIS COMPLETE")
        print(f"{'='*80}")
        print(f"\n📄 CSV: {csv_file.name}")
        print(f"💡 Run: python3 execute_consolidation_auto.py to remove duplicates")
    else:
        print("\n✅ No duplicates found!")

if __name__ == "__main__":
    main()
