#!/usr/bin/env python3
"""
Create merge plan from duplicates CSV
"""
import csv
from pathlib import Path
from collections import defaultdict

CSV_FILE = Path("/Users/steven/Documents/Archives/duplicate_analysis/duplicates_report.csv")
MERGE_PLAN = Path("/Users/steven/Documents/Archives/duplicate_analysis/merge_plan.csv")
SUMMARY = Path("/Users/steven/Documents/Archives/duplicate_analysis/merge_summary.txt")

# Ignore these patterns (system files, configs, cache)
IGNORE = [
    '.DS_Store', '.gitignore', '.editorconfig', '.dockerignore', 
    '.env', 'README.md', 'LICENSE', 'CMakeLists.txt', '.gitkeep',
    '.pyc', '__pycache__', '.dist-info', '.egg-info', 'INSTALLER',
    'METADATA', 'RECORD', 'WHEEL', 'top_level.txt', 'REQUESTED',
    '.venv', 'node_modules', '.git'
]

def is_important(filename, filepath_str):
    """Check if this is an important duplicate (not system file)"""
    filename_lower = filename.lower()
    filepath_lower = str(filepath_str).lower()
    
    # Check if any ignore pattern matches
    for ignore in IGNORE:
        if ignore in filename_lower or ignore in filepath_lower:
            return False
    
    # Important files: archives, executables, large files
    important_extensions = ['.zip', '.tar', '.gz', '.tar.gz', '.7z', '.rar',
                           '.dmg', '.pkg', '.app', '.exe', '.deb', '.rpm']
    if any(filename_lower.endswith(ext) for ext in important_extensions):
        return True
    
    # Files larger than 1MB are likely important (check from CSV size_mb field)
    # This will be checked in main() using the CSV data
    
    return False

def main():
    # Read CSV
    groups = defaultdict(list)
    with open(CSV_FILE, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            groups[row['group_id']].append(row)
    
    # Filter important groups
    important = []
    for group_id, rows in groups.items():
        if len(rows) <= 1:
            continue
        # Check if any file is important (by name/ext) OR if any file is > 1MB
        has_important = any(is_important(r['file_name'], r['file_path']) for r in rows)
        has_large_file = any(float(r.get('size_mb', 0)) > 1.0 for r in rows)
        if has_important or has_large_file:
            important.append((group_id, rows))
    
    # Create merge plan
    merge_rows = []
    total_size_savings = 0
    total_files_to_remove = 0
    
    for group_id, rows in important:
        # Sort: KEEP first, then by size (largest first)
        rows_sorted = sorted(rows, key=lambda x: (
            x['action'] != 'KEEP',
            -float(x['size_mb'])
        ))
        
        keep = [r for r in rows_sorted if r['action'] == 'KEEP']
        remove = [r for r in rows_sorted if r['action'] == 'REMOVE']
        
        if keep and remove:
            keep_file = keep[0]
            size_savings = sum(float(r['size_mb']) for r in remove)
            
            merge_rows.append({
                'group_id': group_id,
                'group_type': rows[0]['group_type'],
                'keep_file': keep_file['file_path'],
                'keep_name': keep_file['file_name'],
                'keep_size_mb': keep_file['size_mb'],
                'keep_date': keep_file['modified'],
                'remove_count': len(remove),
                'size_savings_mb': round(size_savings, 2),
                'remove_files': '; '.join([f"{r['file_name']} ({r['size_mb']}MB)" for r in remove])
            })
            
            total_size_savings += size_savings
            total_files_to_remove += len(remove)
    
    # Sort by size savings
    merge_rows.sort(key=lambda x: float(x['size_savings_mb']), reverse=True)
    
    # Write merge plan CSV
    if merge_rows:
        fieldnames = ['group_id', 'group_type', 'keep_file', 'keep_name', 'keep_size_mb',
                     'keep_date', 'remove_count', 'size_savings_mb', 'remove_files']
        with open(MERGE_PLAN, 'w', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(merge_rows)
    
    # Write summary
    with open(SUMMARY, 'w') as f:
        f.write("=" * 70 + "\n")
        f.write("DUPLICATE MERGE PLAN\n")
        f.write("=" * 70 + "\n\n")
        f.write(f"Total duplicate groups: {len(important)}\n")
        f.write(f"Files to remove: {total_files_to_remove}\n")
        f.write(f"Space savings: {total_size_savings:.2f} MB\n\n")
        f.write("TOP 20 LARGEST DUPLICATE GROUPS:\n")
        f.write("-" * 70 + "\n")
        
        for i, row in enumerate(merge_rows[:20], 1):
            f.write(f"\n{i}. {row['keep_name']}\n")
            f.write(f"   Keep: {row['keep_file']}\n")
            f.write(f"   Size: {row['keep_size_mb']} MB | Date: {row['keep_date']}\n")
            f.write(f"   Remove {row['remove_count']} files ({row['size_savings_mb']} MB)\n")
            f.write(f"   Files: {row['remove_files'][:100]}...\n" if len(row['remove_files']) > 100 else f"   Files: {row['remove_files']}\n")
    
    print("✅ MERGE PLAN CREATED")
    print("=" * 70)
    print(f"📊 Summary:")
    print(f"   Groups to merge: {len(important)}")
    print(f"   Files to remove: {total_files_to_remove}")
    print(f"   Space savings: {total_size_savings:.2f} MB")
    print(f"\n📄 Files created:")
    print(f"   {MERGE_PLAN}")
    print(f"   {SUMMARY}")
    print(f"\n💡 Next: Review merge_plan.csv and merge_summary.txt")

if __name__ == "__main__":
    main()
