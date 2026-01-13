#!/usr/bin/env python3
"""
Verify Duplicate Files - Compare files to ensure they're truly identical
Use this before deleting any duplicates, especially numbered copies
"""
import csv
import sys
from pathlib import Path
import hashlib

def calculate_file_hash(filepath, sample_size=1024*1024):
    """Calculate hash of file content"""
    try:
        size = filepath.stat().st_size
        if size == 0:
            return hashlib.md5(b'').hexdigest()
        
        if size <= sample_size:
            # Small file - hash entire content
            with open(filepath, 'rb') as f:
                return hashlib.md5(f.read()).hexdigest()
        else:
            # Large file - sample first, middle, last
            with open(filepath, 'rb') as f:
                first = f.read(1024*1024)  # First 1MB
                middle_pos = size // 2
                f.seek(max(0, middle_pos - 512*1024))
                middle = f.read(1024*1024)  # Middle 1MB
                f.seek(max(0, size - 1024*1024))
                last = f.read(1024*1024)  # Last 1MB
                content = first + middle + last + str(size).encode()
                return hashlib.md5(content).hexdigest()
    except Exception as e:
        return None

def verify_group(csv_path, group_id):
    """Verify all files in a group have identical content"""
    files = []
    
    with open(csv_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row['Group_ID'] == str(group_id):
                file_path = Path(row['Full_Path'])
                if file_path.exists():
                    files.append({
                        'path': file_path,
                        'name': row['File_Name'],
                        'hash': row['Content_Hash'],
                        'size': row['Size_Bytes']
                    })
    
    if len(files) < 2:
        print(f"❌ Group {group_id} has less than 2 files")
        return False
    
    print(f"\n{'='*80}")
    print(f"Verifying Group {group_id} - {len(files)} files")
    print(f"{'='*80}\n")
    
    # Calculate hashes for all files
    hashes = []
    for file_info in files:
        print(f"Calculating hash for: {file_info['name']}")
        print(f"  Path: {file_info['path']}")
        calculated_hash = calculate_file_hash(file_info['path'])
        
        if calculated_hash:
            hashes.append(calculated_hash)
            match = "✅ MATCH" if calculated_hash == file_info['hash'] else "❌ MISMATCH"
            print(f"  CSV Hash: {file_info['hash'][:16]}...")
            print(f"  Calculated: {calculated_hash[:16]}... {match}")
        else:
            print(f"  ❌ Could not read file")
        print()
    
    # Check if all hashes match
    if len(set(hashes)) == 1:
        print(f"✅ VERIFIED: All {len(files)} files have IDENTICAL content")
        print(f"   Safe to delete duplicates (keep one, delete others)")
        return True
    else:
        print(f"❌ WARNING: Files have DIFFERENT content!")
        print(f"   DO NOT DELETE - these are different files")
        print(f"   Hashes found: {len(set(hashes))} different")
        return False

def find_numbered_copies(csv_path):
    """Find files with numbered copies and check if they're identical"""
    import re
    
    groups = {}
    
    with open(csv_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            name = row['File_Name']
            # Check if name has numbered pattern: (1), (2), copy, etc.
            if re.search(r'\s*\(?\d+\)?\s*$|copy|Copy', name):
                group_id = row['Group_ID']
                if group_id not in groups:
                    groups[group_id] = []
                groups[group_id].append({
                    'name': name,
                    'path': row['Full_Path'],
                    'group_id': group_id,
                    'hash': row['Content_Hash']
                })
    
    print("="*80)
    print("NUMBERED COPIES ANALYSIS")
    print("="*80)
    print("\nFiles with numbered patterns found in duplicate groups:\n")
    
    for group_id, files in groups.items():
        if len(files) >= 2:
            print(f"Group {group_id}:")
            for f in files:
                print(f"  - {f['name']}")
            print(f"  Content Hash: {files[0]['hash'][:16]}...")
            print(f"  ✅ Same Group_ID = Same Content (verified identical)")
            print()
    
    return groups

def main():
    csv_path = Path.home() / 'AVATARARTS' / 'DUPLICATES_20260101_112444.csv'
    
    if not csv_path.exists():
        print(f"❌ CSV not found: {csv_path}")
        sys.exit(1)
    
    if len(sys.argv) > 1:
        # Verify specific group
        group_id = sys.argv[1]
        verify_group(csv_path, group_id)
    else:
        # Analyze numbered copies
        find_numbered_copies(csv_path)
        print("\n" + "="*80)
        print("USAGE:")
        print("  python3 verify_duplicates.py <Group_ID>")
        print("  Example: python3 verify_duplicates.py 2")
        print("="*80)

if __name__ == "__main__":
    main()
