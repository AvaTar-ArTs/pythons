#!/usr/bin/env python3
"""
CSV-Based Organizer
Reads YOUR decisions from CSV and organizes accordingly
"""

import csv
from pathlib import Path
import shutil
from collections import defaultdict

def organize_from_csv(csv_path: Path, dry_run: bool = True):
    """Organize based on CSV file"""
    
    print("\n" + "=" * 80)
    print("  CSV-BASED ORGANIZATION")
    print("  Using YOUR CSV as the source of truth")
    print("=" * 80 + "\n")
    
    if not csv_path.exists():
        print(f"? CSV not found: {csv_path}")
        return
    
    # Load CSV
    files_data = []
    with open(csv_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            files_data.append(row)
    
    print(f"Loaded {len(files_data)} files from CSV\n")
    
    # Analyze what the CSV tells us
    print("Analyzing CSV content...\n")
    
    # Group by artist
    by_artist = defaultdict(list)
    for row in files_data:
        artist = row.get('artist', '') or 'No Artist'
        by_artist[artist].append(row)
    
    print("Files by Artist (from CSV):")
    for artist in sorted(by_artist.keys(), key=lambda x: len(by_artist[x]), reverse=True)[:20]:
        count = len(by_artist[artist])
        print(f"  {artist:30s} {count:3d} files")
    
    print()
    
    # Key insight from old CSV
    avatararts_count = sum(len(files) for artist, files in by_artist.items() 
                          if 'avatar' in artist.lower())
    
    if avatararts_count > 400:
        print(f"? CSV shows {avatararts_count} files marked as AvaTar ArTs variants")
        print("   This CSV marks YOUR originals!\n")
    
    # Check for MY_CATEGORY column (if user added it)
    has_category = 'MY_CATEGORY' in (files_data[0].keys() if files_data else [])
    has_keep = 'KEEP' in (files_data[0].keys() if files_data else [])
    has_action = 'MY_ACTION' in (files_data[0].keys() if files_data else [])
    
    if has_category or has_keep or has_action:
        print("? Found YOUR custom columns!")
        print("   Will use your decisions to organize\n")
    else:
        print("??  No custom columns found")
        print("   Add 'MY_CATEGORY' or 'MY_ACTION' column to CSV")
        print("   Then re-run this script\n")
    
    return files_data

def main():
    import argparse
    
    parser = argparse.ArgumentParser(description='CSV-Based Organizer')
    parser.add_argument('csv_file', nargs='?', 
                       default=str(Path.home() / 'Downloads/YOUR_SUNO_SONGS_COMPLETE - YOUR_SUNO_SONGS_COMPLETE.csv'))
    parser.add_argument('--execute', action='store_true', help='Actually move files')
    
    args = parser.parse_args()
    
    csv_path = Path(args.csv_file)
    files_data = organize_from_csv(csv_path, dry_run=not args.execute)
    
    if files_data:
        print("=" * 80)
        print("  NEXT STEPS")
        print("=" * 80 + "\n")
        print("1. Open the CSV:")
        print(f"   open '{csv_path}'")
        print()
        print("2. Add a column 'MY_CATEGORY' with your decisions:")
        print("   - MUSIC (your songs for streaming)")
        print("   - VIDEO (video content)")  
        print("   - PODCAST (commentary)")
        print("   - CLIPS (short form)")
        print("   - DELETE (don't need)")
        print()
        print("3. Save the CSV")
        print()
        print("4. Run again:")
        print("   python csv_organizer.py --execute")

if __name__ == '__main__':
    main()
