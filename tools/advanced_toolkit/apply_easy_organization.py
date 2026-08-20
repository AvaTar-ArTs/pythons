#!/usr/bin/env python3
"""
Apply Easy Organization
Actually create folders and move/rename files based on the plan
"""

import csv
from pathlib import Path
import shutil

def main():
    print("\n" + "??" * 40)
    print("  APPLYING EASY ORGANIZATION")
    print("  Creating series folders and organizing songs")
    print("??" * 40 + "\n")
    
    home = Path.home()
    plan_csv = home / 'Music/EASY_ORGANIZATION_PLAN.csv'
    
    if not plan_csv.exists():
        print("? EASY_ORGANIZATION_PLAN.csv not found")
        print("Run easy_organize_all.py first")
        return
    
    # Load plan
    print("Loading organization plan...\n")
    
    plan = []
    with open(plan_csv, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        plan = list(reader)
    
    print(f"? Loaded {len(plan)} files to organize\n")
    
    # Create series folders
    base_dir = home / 'Music/nocTurneMeLoDieS/FINAL_ORGANIZED/YOUR_SUNO_SONGS'
    
    series_folders = set(row['Target_Folder'] for row in plan)
    
    print(f"Creating {len(series_folders)} series folders...\n")
    
    for folder_name in sorted(series_folders):
        folder_path = base_dir / folder_name
        folder_path.mkdir(exist_ok=True)
        print(f"  ? {folder_name}/")
    
    print()
    
    # Apply organization
    print("=" * 80)
    print("  ORGANIZING FILES")
    print("=" * 80 + "\n")
    
    results = {
        'moved': 0,
        'renamed': 0,
        'skipped': 0,
        'failed': 0
    }
    
    by_series = {}
    
    for i, item in enumerate(plan):
        if (i + 1) % 50 == 0:
            print(f"  Processing {i + 1}/{len(plan)}...")
        
        current_path = Path(item['Current_Path'])
        target_folder = base_dir / item['Target_Folder']
        suggested_name = item['Suggested_Name']
        
        if not current_path.exists():
            results['skipped'] += 1
            continue
        
        # Determine target path
        target_path = target_folder / suggested_name
        
        # Handle conflicts
        if target_path.exists() and target_path != current_path:
            # Add number suffix
            counter = 1
            stem = target_path.stem
            while target_path.exists():
                target_path = target_folder / f"{stem} {counter}.mp3"
                counter += 1
        
        try:
            # Move/rename file
            if current_path != target_path:
                shutil.move(str(current_path), str(target_path))
                
                series = item['Series']
                if series not in by_series:
                    by_series[series] = 0
                by_series[series] += 1
                
                if str(current_path.parent) != str(target_folder):
                    results['moved'] += 1
                else:
                    results['renamed'] += 1
        
        except Exception as e:
            results['failed'] += 1
            print(f"  ? Failed: {current_path.name}")
    
    print()
    print("=" * 80)
    print("  ? ORGANIZATION COMPLETE")
    print("=" * 80 + "\n")
    
    print(f"Files moved: {results['moved']}")
    print(f"Files renamed: {results['renamed']}")
    print(f"Skipped (not found): {results['skipped']}")
    print(f"Failed: {results['failed']}")
    print()
    
    print("Songs organized by series:")
    for series in sorted(by_series.keys()):
        count = by_series[series]
        print(f"  ? {series}: {count} songs")
    
    print()
    print(f"All organized in: {base_dir}")
    print()
    print("Your music is now organized by series!")
    print("Each series has all versions, remixes, live recordings together.")
    print()
    print(f"Open: open '{base_dir}'")

if __name__ == '__main__':
    main()
