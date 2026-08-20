#!/usr/bin/env python3
"""
Analyze duplicates CSV and create actionable summary
Filters out system files and focuses on real duplicates
"""
import csv
from pathlib import Path
from collections import defaultdict

CSV_FILE = Path("/Users/steven/Documents/Archives/duplicate_analysis/duplicates_report.csv")
OUTPUT_SUMMARY = Path("/Users/steven/Documents/Archives/duplicate_analysis/actionable_summary.csv")
OUTPUT_DETAILED = Path("/Users/steven/Documents/Archives/duplicate_analysis/important_duplicates.csv")

# Files to ignore (system files, common configs)
IGNORE_PATTERNS = [
    '.DS_Store',
    '.gitignore',
    '.editorconfig',
    '.dockerignore',
    '.env',
    '.env.example',
    'README.md',
    'LICENSE',
    'package.json',
    'requirements.txt',
    'setup.py',
    'pyproject.toml',
    '.pre-commit-config.yaml',
    '.github/workflows',
]

def should_ignore(filename, filepath):
    """Check if file should be ignored"""
    for pattern in IGNORE_PATTERNS:
        if pattern in filename or pattern in filepath:
            return True
    return False

def analyze_duplicates():
    """Analyze CSV and create actionable reports"""
    
    # Read all rows
    all_rows = []
    with open(CSV_FILE, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            all_rows.append(row)
    
    # Group by group_id
    groups = defaultdict(list)
    for row in all_rows:
        groups[row['group_id']].append(row)
    
    # Filter to important duplicates
    important_groups = []
    system_groups = []
    
    for group_id, rows in groups.items():
        # Skip single-file groups
        if len(rows) <= 1:
            continue
        
        # Check if all files in group should be ignored
        if all(should_ignore(r['file_name'], r['file_path']) for r in rows):
            system_groups.append((group_id, rows))
        else:
            important_groups.append((group_id, rows))
    
    # Create actionable summary
    actionable_rows = []
    
    for group_id, rows in important_groups:
        # Sort by action (KEEP first)
        rows_sorted = sorted(rows, key=lambda x: (x['action'] == 'REMOVE', float(x['size_mb'])), reverse=True)
        
        keep_file = next((r for r in rows_sorted if r['action'] == 'KEEP'), None)
        remove_files = [r for r in rows_sorted if r['action'] == 'REMOVE']
        
        if keep_file and remove_files:
            total_size = sum(float(r['size_mb']) for r in remove_files)
            
            actionable_rows.append({
                'group_type': rows[0]['group_type'],
                'group_id': group_id,
                'keep_file': keep_file['file_path'],
                'keep_name': keep_file['file_name'],
                'keep_size_mb': keep_file['size_mb'],
                'keep_modified': keep_file['modified'],
                'remove_count': len(remove_files),
                'remove_size_mb': round(total_size, 2),
                'remove_files': ' | '.join([r['file_name'] for r in remove_files[:3]] + 
                                          (['...'] if len(remove_files) > 3 else [])),
            })
    
    # Write actionable summary
    if actionable_rows:
        fieldnames = ['group_type', 'group_id', 'keep_file', 'keep_name', 'keep_size_mb', 
                     'keep_modified', 'remove_count', 'remove_size_mb', 'remove_files']
        with open(OUTPUT_SUMMARY, 'w', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(actionable_rows)
        
        print(f"✅ Actionable summary: {OUTPUT_SUMMARY}")
        print(f"   {len(actionable_rows)} duplicate groups to review")
    
    # Write detailed important duplicates
    important_rows = []
    for group_id, rows in important_groups:
        important_rows.extend(rows)
    
    if important_rows:
        fieldnames = ['group_type', 'group_id', 'file_path', 'file_name', 'size_mb', 
                     'modified', 'action', 'duplicate_count', 'hash']
        with open(OUTPUT_DETAILED, 'w', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(important_rows)
        
        print(f"✅ Detailed report: {OUTPUT_DETAILED}")
        print(f"   {len(important_rows)} files in important duplicate groups")
    
    # Statistics
    total_removable_size = sum(float(r['remove_size_mb']) for r in actionable_rows)
    total_removable_count = sum(int(r['remove_count']) for r in actionable_rows)
    
    print("\n" + "=" * 60)
    print("📊 SUMMARY")
    print("=" * 60)
    print(f"Important duplicate groups: {len(important_groups)}")
    print(f"System file groups (ignored): {len(system_groups)}")
    print(f"\nFiles to remove: {total_removable_count}")
    print(f"Space savings: {total_removable_size:.2f} MB")
    print(f"\nTop 10 largest duplicate groups:")
    
    # Sort by size
    actionable_rows_sorted = sorted(actionable_rows, key=lambda x: float(x['remove_size_mb']), reverse=True)
    for i, row in enumerate(actionable_rows_sorted[:10], 1):
        print(f"  {i}. {row['keep_name']} - {row['remove_size_mb']} MB ({row['remove_count']} duplicates)")
    
    return actionable_rows

if __name__ == "__main__":
    analyze_duplicates()
