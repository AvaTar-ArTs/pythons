#!/usr/bin/env python3
"""
Process Final CSV - Focus only on remaining files
Based on YOUR_SUNO_SONGS_COMPLETE - MASTER_MERGED_DATA (1).csv
"""

import csv
from pathlib import Path
from collections import defaultdict
import shutil

def analyze_final_csv():
    """Analyze the final CSV file"""
    
    csv_path = Path.home() / 'Downloads/YOUR_SUNO_SONGS_COMPLETE - MASTER_MERGED_DATA (1).csv'
    
    print("\n" + "=" * 80)
    print("  PROCESSING FINAL CSV")
    print("  Focusing ONLY on files in this list")
    print("=" * 80 + "\n")
    
    if not csv_path.exists():
        print(f"? CSV not found: {csv_path}")
        return
    
    # Load CSV
    with open(csv_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        rows = list(reader)
    
    print(f"? Loaded {len(rows)} files from CSV\n")
    
    # Check columns
    if rows:
        print(f"Columns: {', '.join(rows[0].keys())}\n")
    
    # Analyze
    stats = {
        'total': len(rows),
        'by_artist': defaultdict(int),
        'by_duration': defaultdict(int),
        'with_metadata': 0,
        'without_metadata': 0,
    }
    
    for row in rows:
        # Count by artist
        artist = row.get('artist', '') or 'No Artist'
        stats['by_artist'][artist] += 1
        
        # Count by duration
        try:
            duration = float(row.get('duration', 0))
            if duration < 30:
                stats['by_duration']['SHORT'] += 1
            elif duration <= 360:
                stats['by_duration']['SONG'] += 1
            else:
                stats['by_duration']['LONG'] += 1
        except:
            stats['by_duration']['UNKNOWN'] += 1
        
        # Metadata quality
        if row.get('title') or row.get('artist'):
            stats['with_metadata'] += 1
        else:
            stats['without_metadata'] += 1
    
    # Show results
    print("=" * 80)
    print("  ANALYSIS OF FINAL CSV")
    print("=" * 80 + "\n")
    
    print(f"Total files: {stats['total']}\n")
    
    print("By Duration:")
    for dur_type, count in sorted(stats['by_duration'].items()):
        print(f"  {dur_type:10s} {count:4d} files")
    
    print(f"\nMetadata Quality:")
    print(f"  With metadata: {stats['with_metadata']}")
    print(f"  Without metadata: {stats['without_metadata']}")
    
    print(f"\nTop Artists:")
    for artist, count in sorted(stats['by_artist'].items(), key=lambda x: x[1], reverse=True)[:15]:
        print(f"  {artist:30s} {count:3d} files")
    
    return rows

def create_action_plan(rows):
    """Create action plan based on CSV"""
    
    print("\n" + "=" * 80)
    print("  RECOMMENDED ACTIONS")
    print("=" * 80 + "\n")
    
    # Check if user added decision columns
    if rows:
        has_my_category = 'MY_CATEGORY' in rows[0].keys()
        has_my_action = 'MY_ACTION' in rows[0].keys()
        has_keep = 'KEEP' in rows[0].keys()
        
        if has_my_category or has_my_action or has_keep:
            print("? Found YOUR decision columns!")
            print("   Ready to execute based on your choices\n")
            
            # Count by category
            if has_my_category:
                categories = defaultdict(int)
                for row in rows:
                    cat = row.get('MY_CATEGORY', 'UNSET')
                    categories[cat] += 1
                
                print("Your categories:")
                for cat, count in sorted(categories.items()):
                    print(f"  {cat:20s} {count:3d} files")
            
            print("\nRun with --execute to organize based on YOUR choices!")
            
        else:
            print("??  No decision columns found yet\n")
            print("To organize, add one of these columns to the CSV:")
            print("  ? MY_CATEGORY (MUSIC, VIDEO, PODCAST, CLIP, DELETE)")
            print("  ? MY_ACTION (KEEP, MOVE, DELETE)")
            print("  ? KEEP (YES, NO)")
            print()
            print("Then save and run: python process_final_csv.py --execute")

def main():
    import argparse
    
    parser = argparse.ArgumentParser(description='Process Final CSV')
    parser.add_argument('--execute', action='store_true', help='Execute organization')
    
    args = parser.parse_args()
    
    rows = analyze_final_csv()
    
    if rows:
        create_action_plan(rows)

if __name__ == '__main__':
    main()
