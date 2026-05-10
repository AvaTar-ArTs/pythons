#!/usr/bin/env python3
"""
Intelligent Merge - Use existing scan data from ~/
Merge ALL previous scans with current analysis
"""

import csv
import json
from pathlib import Path
from collections import defaultdict

def merge_all_existing_data():
    """Merge all existing scan/analysis data"""
    
    print("\n" + "=" * 80)
    print("  INTELLIGENT MERGE - Using ALL Existing Data")
    print("=" * 80 + "\n")
    
    home = Path.home()
    
    # All existing data sources
    data_sources = {
        # Current analysis
        'your_songs_current': home / 'Music/YOUR_SUNO_SONGS_COMPLETE.csv',
        'merged_analysis': home / 'Music/MERGED_ANALYSIS.csv',
        'complete_analysis': home / 'Music/nocTurneMeLoDieS/COMPLETE_ANALYSIS.csv',
        
        # Previous scans
        'general_scan': home / 'workspace/csvs-consolidated/general_scan_results.csv',
        'python_inventory': home / 'Documents/inventory/python_inventory.csv',
        'script_inventory': home / 'Documents/inventory/script_inventory.csv',
        
        # Content analysis
        'content_aware': home / 'content_aware_analysis.json',
        'content_type': home / 'content_type_classification.json',
        
        # Suno catalogs
        'suno_master': home / 'Music/nocTurneMeLoDieS/SUNO/suno-sept/songs_master_combined.csv',
        'file_inventory': home / 'workspace/music-empire/COMPLETE_FILE_INVENTORY.csv',
    }
    
    loaded_data = {}
    
    print("Loading existing data sources...\n")
    
    for name, path in data_sources.items():
        if not path.exists():
            continue
        
        print(f"  {name}...")
        
        if path.suffix == '.json':
            try:
                with open(path) as f:
                    loaded_data[name] = json.load(f)
                print(f"    ? Loaded JSON")
            except Exception as e:
                print(f"    ??  Error: {e}")
        
        elif path.suffix == '.csv':
            try:
                with open(path, 'r', encoding='utf-8', errors='ignore') as f:
                    reader = csv.DictReader(f)
                    rows = list(reader)
                    loaded_data[name] = rows
                print(f"    ? Loaded {len(rows)} rows")
            except Exception as e:
                print(f"    ??  Error: {e}")
    
    print()
    return loaded_data

def build_complete_picture(loaded_data: dict):
    """Build complete picture from all data"""
    
    print("=" * 80)
    print("  BUILDING COMPLETE PICTURE")
    print("=" * 80 + "\n")
    
    # Index all files
    all_files = {}
    
    # From current YOUR_SUNO_SONGS
    if 'your_songs_current' in loaded_data:
        for row in loaded_data['your_songs_current']:
            filename = row.get('filename', '')
            if filename:
                all_files[filename] = {
                    'filename': filename,
                    'title': row.get('title', ''),
                    'artist': row.get('artist', ''),
                    'duration': row.get('duration', 0),
                    'location': 'YOUR_SUNO_SONGS',
                    'source': 'current'
                }
    
    # From content-aware analysis
    if 'content_aware' in loaded_data:
        ca_data = loaded_data['content_aware']
        for location, info in ca_data.items():
            if isinstance(info, dict) and 'sample_audio' in info:
                for sample in info['sample_audio']:
                    filename = sample.get('file', '')
                    if filename and filename not in all_files:
                        all_files[filename] = {
                            'filename': filename,
                            'title': sample.get('title', ''),
                            'artist': sample.get('artist', ''),
                            'location': location,
                            'source': 'content_aware_scan'
                        }
    
    # From Suno master catalog
    suno_catalog_titles = set()
    if 'suno_master' in loaded_data:
        for row in loaded_data['suno_master']:
            title = row.get('SongTitle', '')
            if title:
                suno_catalog_titles.add(title.lower().strip())
    
    # Mark which are in catalog
    for filename, info in all_files.items():
        title = info.get('title') or ''
        title_normalized = title.lower().strip() if title else ''
        info['in_suno_catalog'] = title_normalized in suno_catalog_titles if title_normalized else False
    
    print(f"Total unique files indexed: {len(all_files)}")
    print(f"Suno catalog songs: {len(suno_catalog_titles)}")
    print()
    
    return all_files, suno_catalog_titles

def create_master_csv(all_files: dict):
    """Create master CSV with everything"""
    
    output = Path.home() / 'Music/MASTER_MERGED_DATA.csv'
    
    print("=" * 80)
    print("  CREATING MASTER CSV")
    print("=" * 80 + "\n")
    
    with open(output, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=[
            'filename', 'title', 'artist', 'duration', 
            'location', 'in_suno_catalog', 'source'
        ])
        writer.writeheader()
        
        for info in sorted(all_files.values(), key=lambda x: x.get('filename', '')):
            writer.writerow({
                'filename': info.get('filename', ''),
                'title': info.get('title', ''),
                'artist': info.get('artist', ''),
                'duration': info.get('duration', ''),
                'location': info.get('location', ''),
                'in_suno_catalog': 'YES' if info.get('in_suno_catalog') else 'NO',
                'source': info.get('source', '')
            })
    
    print(f"? Master CSV saved to: {output}\n")
    
    # Summary
    in_catalog = sum(1 for f in all_files.values() if f.get('in_suno_catalog'))
    
    print("Summary:")
    print(f"  Total files: {len(all_files)}")
    print(f"  In Suno catalog: {in_catalog}")
    print(f"  Not in catalog: {len(all_files) - in_catalog}")
    print()
    
    return output

def main():
    print("\n" + "??" * 40)
    print("  INTELLIGENT MERGE - All Existing Data")
    print("??" * 40)
    
    # Load all existing data
    loaded_data = merge_all_existing_data()
    
    # Build complete picture
    all_files, catalog = build_complete_picture(loaded_data)
    
    # Create master CSV
    output = create_master_csv(all_files)
    
    print("=" * 80)
    print("  ? INTELLIGENT MERGE COMPLETE")
    print("=" * 80 + "\n")
    
    print(f"Master CSV: {output}")
    print(f"\nThis merges ALL previous scans and analysis!")
    print(f"\nOpen it: open {output}")

if __name__ == '__main__':
    main()
