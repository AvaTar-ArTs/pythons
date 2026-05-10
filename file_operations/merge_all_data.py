#!/usr/bin/env python3
"""
Merge, Compare, and Diff ALL CSV data
Combine everything to get the complete picture
"""

import csv
from pathlib import Path
from collections import defaultdict
import hashlib

def load_csv_robust(csv_path: Path) -> list:
    """Load CSV with error handling"""
    rows = []
    
    try:
        with open(csv_path, 'r', encoding='utf-8', errors='ignore') as f:
            reader = csv.DictReader(f)
            for row in reader:
                rows.append(row)
        return rows
    except Exception as e:
        print(f"  Error loading {csv_path.name}: {e}")
        return []

def normalize_title(title: str) -> str:
    """Normalize title for matching"""
    if not title:
        return ""
    return title.lower().replace('_', ' ').replace('-', ' ').strip()

def merge_all_csvs():
    """Merge all available CSVs"""
    
    print("\n" + "=" * 80)
    print("  MERGING ALL CSV DATA")
    print("=" * 80 + "\n")
    
    csvs = {
        'current_files': Path.home() / 'Music/YOUR_SUNO_SONGS_COMPLETE.csv',
        'complete_analysis': Path.home() / 'Music/nocTurneMeLoDieS/COMPLETE_ANALYSIS.csv',
        'suno_master': Path.home() / 'Music/nocTurneMeLoDieS/SUNO/suno-sept/songs_master_combined.csv',
        'suno_unique': Path.home() / 'Music/nocTurneMeLoDieS/SUNO/suno-sept/songs_master_unique.csv',
        'file_inventory': Path.home() / 'workspace/music-empire/COMPLETE_FILE_INVENTORY.csv',
    }
    
    data = {}
    
    for name, path in csvs.items():
        if path.exists():
            print(f"Loading {name}...")
            rows = load_csv_robust(path)
            data[name] = rows
            print(f"  ? {len(rows)} rows\n")
        else:
            print(f"  ??  Not found: {name}\n")
            data[name] = []
    
    return data

def build_unified_index(data: dict) -> dict:
    """Build unified index of all files"""
    
    print("=" * 80)
    print("  BUILDING UNIFIED INDEX")
    print("=" * 80 + "\n")
    
    unified = {}
    
    # From current_files (what you have now)
    for row in data.get('current_files', []):
        filename = row.get('filename', '')
        if filename:
            unified[filename] = {
                'filename': filename,
                'title': row.get('title', ''),
                'artist': row.get('artist', ''),
                'duration': row.get('duration', 0),
                'has_file': True,
                'in_suno_catalog': False,
                'source': 'current_files'
            }
    
    # From Suno catalog (what's in your Suno account)
    catalog_songs = set()
    for row in data.get('suno_master', []):
        song_title = row.get('SongTitle', '')
        if song_title:
            catalog_songs.add(normalize_title(song_title))
    
    # Match current files with catalog
    for filename, info in unified.items():
        title_norm = normalize_title(info['title'])
        if title_norm in catalog_songs:
            info['in_suno_catalog'] = True
    
    print(f"? Indexed {len(unified)} files\n")
    print(f"? Suno catalog has {len(catalog_songs)} songs\n")
    
    # Find matches
    matched = sum(1 for f in unified.values() if f['in_suno_catalog'])
    unmatched = len(unified) - matched
    
    print(f"Matched to Suno catalog: {matched}")
    print(f"Not in Suno catalog: {unmatched}")
    print()
    
    return unified, catalog_songs

def create_diff_report(unified: dict, catalog_songs: set):
    """Create comprehensive diff report"""
    
    print("=" * 80)
    print("  CREATING DIFF REPORT")
    print("=" * 80 + "\n")
    
    # Categorize files
    categories = {
        'confirmed_suno': [],
        'not_in_catalog': [],
        'no_title': [],
    }
    
    for filename, info in unified.items():
        if info['in_suno_catalog']:
            categories['confirmed_suno'].append(info)
        elif not info['title']:
            categories['no_title'].append(info)
        else:
            categories['not_in_catalog'].append(info)
    
    # Show results
    print("CONFIRMED SUNO SONGS (in your catalog):")
    print(f"  {len(categories['confirmed_suno'])} files\n")
    
    print("NOT IN SUNO CATALOG (likely other content):")
    print(f"  {len(categories['not_in_catalog'])} files")
    for info in categories['not_in_catalog'][:10]:
        print(f"    ? {info['filename']}")
        if info['title']:
            print(f"      Title: {info['title']}")
    print()
    
    print("NO METADATA (need review):")
    print(f"  {len(categories['no_title'])} files")
    for info in categories['no_title'][:10]:
        print(f"    ? {info['filename']}")
    print()
    
    # Save merged CSV
    output = Path.home() / 'Music/MERGED_ANALYSIS.csv'
    
    with open(output, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=[
            'filename', 'title', 'artist', 'duration',
            'in_suno_catalog', 'category', 'recommendation'
        ])
        writer.writeheader()
        
        for info in unified.values():
            if info['in_suno_catalog']:
                category = 'SUNO_MUSIC'
                recommendation = 'KEEP - Confirmed Suno song'
            elif not info['title']:
                category = 'NO_METADATA'
                recommendation = 'REVIEW - No metadata'
            else:
                category = 'OTHER_CONTENT'
                recommendation = 'REVIEW - Not in Suno catalog (video/podcast?)'
            
            writer.writerow({
                'filename': info['filename'],
                'title': info['title'],
                'artist': info['artist'],
                'duration': info['duration'],
                'in_suno_catalog': 'YES' if info['in_suno_catalog'] else 'NO',
                'category': category,
                'recommendation': recommendation
            })
    
    print(f"? Merged analysis saved to: {output}\n")
    
    return categories

def main():
    print("\n" + "??" * 40)
    print("  MERGE, COMPARE, DIFF ALL DATA")
    print("??" * 40)
    
    # Load all CSVs
    data = merge_all_csvs()
    
    # Build unified index
    unified, catalog_songs = build_unified_index(data)
    
    # Create diff report
    categories = create_diff_report(unified, catalog_songs)
    
    print("=" * 80)
    print("  SUMMARY")
    print("=" * 80 + "\n")
    
    print(f"Total files analyzed: {len(unified)}")
    print(f"Confirmed Suno songs: {len(categories['confirmed_suno'])}")
    print(f"Other content: {len(categories['not_in_catalog'])}")
    print(f"No metadata: {len(categories['no_title'])}")
    print()
    
    print("Next: Review ~/Music/MERGED_ANALYSIS.csv")
    print("  - in_suno_catalog=YES ? Keep as music")
    print("  - in_suno_catalog=NO ? Review (video/podcast/other)")

if __name__ == '__main__':
    main()
