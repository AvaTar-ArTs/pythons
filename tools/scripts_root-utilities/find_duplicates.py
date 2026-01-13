#!/usr/bin/env python3
"""
Find duplicates, create CSV report, and generate diffs
"""
import os
import hashlib
import csv
from pathlib import Path
from collections import defaultdict
from datetime import datetime
import subprocess

ARCHIVES_DIR = Path("/Users/steven/Documents/Archives")
OUTPUT_DIR = ARCHIVES_DIR / "duplicate_analysis"
CSV_FILE = OUTPUT_DIR / "duplicates_report.csv"
DIFF_DIR = OUTPUT_DIR / "diffs"

def get_file_hash(filepath, chunk_size=8192):
    """Calculate MD5 hash of file"""
    hash_md5 = hashlib.md5()
    try:
        with open(filepath, "rb") as f:
            for chunk in iter(lambda: f.read(chunk_size), b""):
                hash_md5.update(chunk)
        return hash_md5.hexdigest()
    except Exception as e:
        return None

def get_file_size(filepath):
    """Get file size in bytes"""
    try:
        return os.path.getsize(filepath)
    except:
        return 0

def find_duplicates_by_name():
    """Find files with similar names (potential duplicates)"""
    name_groups = defaultdict(list)
    
    # Search in Archives directory
    for file in ARCHIVES_DIR.rglob("*"):
        if file.is_file():
            name = file.name.lower()
            # Extract base name (without version suffixes)
            base_name = name
            for suffix in ['_2025', '-final', '-perfect', '-fixed', '-mine', '_template', '-updated', '-2024']:
                if suffix in base_name:
                    base_name = base_name.split(suffix)[0]
            
            # Group by base name
            name_groups[base_name].append(file)
    
    # Filter to groups with multiple files
    duplicates = {k: v for k, v in name_groups.items() if len(v) > 1}
    return duplicates

def find_duplicates_by_hash():
    """Find files with identical content (exact duplicates)"""
    hash_groups = defaultdict(list)
    
    print("🔍 Calculating file hashes (this may take a while)...")
    file_count = 0
    
    # Only check zip files and common archive types
    extensions = {'.zip', '.tar.gz', '.tar', '.gz'}
    
    for file in ARCHIVES_DIR.rglob("*"):
        if file.is_file() and file.suffix.lower() in extensions:
            file_count += 1
            if file_count % 10 == 0:
                print(f"  Processed {file_count} files...")
            
            file_hash = get_file_hash(file)
            if file_hash:
                hash_groups[file_hash].append(file)
    
    # Filter to groups with multiple files
    exact_duplicates = {k: v for k, v in hash_groups.items() if len(v) > 1}
    return exact_duplicates

def create_diff(file1, file2, diff_file):
    """Create diff between two files (if text-based) or compare metadata"""
    try:
        # For zip files, compare contents
        if file1.suffix == '.zip' and file2.suffix == '.zip':
            result1 = subprocess.run(['unzip', '-l', str(file1)], capture_output=True, text=True, timeout=10)
            result2 = subprocess.run(['unzip', '-l', str(file2)], capture_output=True, text=True, timeout=10)
            
            with open(diff_file, 'w') as f:
                f.write(f"=== {file1.name} ===\n")
                f.write(result1.stdout)
                f.write(f"\n=== {file2.name} ===\n")
                f.write(result2.stdout)
                f.write(f"\n=== DIFF ===\n")
                # Simple comparison
                if result1.stdout == result2.stdout:
                    f.write("Files appear identical\n")
                else:
                    f.write("Files differ in contents\n")
        else:
            # For other files, just compare sizes and dates
            with open(diff_file, 'w') as f:
                f.write(f"File 1: {file1}\n")
                f.write(f"  Size: {get_file_size(file1)} bytes\n")
                f.write(f"  Modified: {datetime.fromtimestamp(file1.stat().st_mtime)}\n")
                f.write(f"\nFile 2: {file2}\n")
                f.write(f"  Size: {get_file_size(file2)} bytes\n")
                f.write(f"  Modified: {datetime.fromtimestamp(file2.stat().st_mtime)}\n")
                f.write(f"\nSize difference: {abs(get_file_size(file1) - get_file_size(file2))} bytes\n")
    except Exception as e:
        with open(diff_file, 'w') as f:
            f.write(f"Error creating diff: {e}\n")

def generate_csv_report(name_duplicates, hash_duplicates):
    """Generate CSV report of all duplicates"""
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    DIFF_DIR.mkdir(parents=True, exist_ok=True)
    
    rows = []
    diff_count = 0
    
    # Process name-based duplicates
    for base_name, files in sorted(name_duplicates.items()):
        if len(files) > 1:
            # Sort by modification time (newest first)
            files_sorted = sorted(files, key=lambda f: f.stat().st_mtime, reverse=True)
            
            # Mark which to keep (newest)
            for i, file in enumerate(files_sorted):
                keep = "KEEP" if i == 0 else "REMOVE"
                size_mb = get_file_size(file) / (1024 * 1024)
                modified = datetime.fromtimestamp(file.stat().st_mtime)
                
                rows.append({
                    'group_type': 'name_similar',
                    'group_id': base_name,
                    'file_path': str(file),
                    'file_name': file.name,
                    'size_mb': round(size_mb, 2),
                    'modified': modified.strftime('%Y-%m-%d %H:%M:%S'),
                    'action': keep,
                    'duplicate_count': len(files_sorted),
                    'hash': get_file_hash(file)[:8] if get_file_hash(file) else 'N/A'
                })
            
            # Create diff for first two files
            if len(files_sorted) >= 2:
                diff_file = DIFF_DIR / f"{base_name.replace('/', '_')}_diff.txt"
                create_diff(files_sorted[0], files_sorted[1], diff_file)
                diff_count += 1
    
    # Process hash-based duplicates (exact matches)
    for file_hash, files in sorted(hash_duplicates.items()):
        if len(files) > 1:
            files_sorted = sorted(files, key=lambda f: f.stat().st_mtime, reverse=True)
            
            for i, file in enumerate(files_sorted):
                keep = "KEEP" if i == 0 else "REMOVE"
                size_mb = get_file_size(file) / (1024 * 1024)
                modified = datetime.fromtimestamp(file.stat().st_mtime)
                
                rows.append({
                    'group_type': 'exact_match',
                    'group_id': file_hash[:8],
                    'file_path': str(file),
                    'file_name': file.name,
                    'size_mb': round(size_mb, 2),
                    'modified': modified.strftime('%Y-%m-%d %H:%M:%S'),
                    'action': keep,
                    'duplicate_count': len(files_sorted),
                    'hash': file_hash[:8]
                })
    
    # Write CSV
    if rows:
        fieldnames = ['group_type', 'group_id', 'file_path', 'file_name', 'size_mb', 'modified', 'action', 'duplicate_count', 'hash']
        with open(CSV_FILE, 'w', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(rows)
        
        print(f"\n✅ CSV report created: {CSV_FILE}")
        print(f"   Total duplicate groups: {len(set(r['group_id'] for r in rows))}")
        print(f"   Total files: {len(rows)}")
        print(f"   Diffs created: {diff_count}")
    else:
        print("\n✅ No duplicates found")
    
    return rows

def main():
    print("🔍 Finding Duplicates in Archives")
    print("=" * 60)
    print()
    
    # Find duplicates
    print("1. Finding files with similar names...")
    name_duplicates = find_duplicates_by_name()
    print(f"   Found {len(name_duplicates)} groups with similar names")
    
    print("\n2. Finding files with identical content...")
    hash_duplicates = find_duplicates_by_hash()
    print(f"   Found {len(hash_duplicates)} groups with identical content")
    
    # Generate reports
    print("\n3. Generating CSV report and diffs...")
    rows = generate_csv_report(name_duplicates, hash_duplicates)
    
    # Summary
    print("\n" + "=" * 60)
    print("📊 SUMMARY")
    print("=" * 60)
    
    if rows:
        total_size = sum(r['size_mb'] for r in rows if r['action'] == 'REMOVE')
        print(f"Files to remove: {len([r for r in rows if r['action'] == 'REMOVE'])}")
        print(f"Potential space savings: {total_size:.2f} MB")
        print(f"\n📄 Reports:")
        print(f"   CSV: {CSV_FILE}")
        print(f"   Diffs: {DIFF_DIR}/")
        print(f"\n💡 Next steps:")
        print(f"   1. Review CSV: open {CSV_FILE}")
        print(f"   2. Review diffs in: {DIFF_DIR}/")
        print(f"   3. Decide which files to keep/remove")
    else:
        print("No duplicates found!")

if __name__ == "__main__":
    main()
