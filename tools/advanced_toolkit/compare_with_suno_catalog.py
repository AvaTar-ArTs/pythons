#!/usr/bin/env python3
"""
Compare YOUR_SUNO_SONGS files with Suno catalog CSVs
Find which songs you have vs what's in your Suno account
"""

import csv
from pathlib import Path
from collections import defaultdict

def load_suno_catalog(csv_path: Path) -> dict:
    """Load Suno catalog CSV"""
    catalog = {}
    
    try:
        with open(csv_path, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                # Get title from various possible column names
                title = (row.get('title') or row.get('Title') or 
                        row.get('song_title') or row.get('name') or '').strip()
                
                if title:
                    catalog[title.lower()] = row
        
        return catalog
    except Exception as e:
        print(f"Error loading {csv_path.name}: {e}")
        return {}

def load_current_files(csv_path: Path) -> dict:
    """Load current YOUR_SUNO_SONGS files"""
    current = {}
    
    with open(csv_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            filename = row.get('filename', '')
            title = row.get('title', '').strip()
            
            if filename:
                current[filename] = {
                    'title': title,
                    'title_lower': title.lower() if title else '',
                    **row
                }
    
    return current

def compare_catalogs():
    """Compare current files with Suno catalog"""
    
    print("\n" + "=" * 80)
    print("  COMPARE WITH SUNO CATALOG")
    print("=" * 80 + "\n")
    
    # Load Suno catalogs
    suno_csvs = [
        Path.home() / 'Music/nocTurneMeLoDieS/SUNO/suno-sept/songs_master_combined.csv',
        Path.home() / 'Music/nocTurneMeLoDieS/SUNO/suno-sept/songs_master_unique.csv',
        Path.home() / 'workspace/music-empire/COMPLETE_FILE_INVENTORY.csv',
    ]
    
    print("Loading Suno catalogs...")
    all_catalog_songs = {}
    
    for suno_csv in suno_csvs:
        if suno_csv.exists():
            print(f"  Loading {suno_csv.name}...")
            catalog = load_suno_catalog(suno_csv)
            all_catalog_songs.update(catalog)
            print(f"    Found {len(catalog)} songs")
    
    print(f"\nTotal unique songs in Suno catalogs: {len(all_catalog_songs)}\n")
    
    # Load current files
    current_csv = Path.home() / 'Music/YOUR_SUNO_SONGS_COMPLETE.csv'
    current_files = load_current_files(current_csv)
    
    print(f"Current files in YOUR_SUNO_SONGS: {len(current_files)}\n")
    
    # Compare
    print("=" * 80)
    print("  MATCHING")
    print("=" * 80 + "\n")
    
    matched = []
    unmatched_files = []
    
    for filename, file_info in current_files.items():
        title_lower = file_info['title_lower']
        
        if title_lower and title_lower in all_catalog_songs:
            matched.append((filename, title_lower, all_catalog_songs[title_lower]))
        else:
            unmatched_files.append((filename, file_info))
    
    print(f"? MATCHED: {len(matched)} files found in Suno catalog")
    print(f"? UNMATCHED: {len(unmatched_files)} files NOT in catalog")
    print()
    
    # Show samples
    if matched:
        print("Sample matched files:")
        for filename, title, catalog_entry in matched[:10]:
            print(f"  ? {filename}")
            print(f"    Title: {title}")
        print()
    
    if unmatched_files:
        print("Sample unmatched files (may be video/podcast/other):")
        for filename, file_info in unmatched_files[:20]:
            print(f"  ? {filename}")
            if file_info['title']:
                print(f"    Title: {file_info['title']}")
            print(f"    Duration: {file_info['duration_formatted']}")
        
        if len(unmatched_files) > 20:
            print(f"  ... and {len(unmatched_files) - 20} more")
    
    # Analysis
    print("\n" + "=" * 80)
    print("  ANALYSIS")
    print("=" * 80 + "\n")
    
    print(f"Your Suno catalog: {len(all_catalog_songs)} unique songs")
    print(f"Files you have: {len(current_files)} files")
    print(f"Matched: {len(matched)} files are confirmed Suno songs")
    print(f"Unmatched: {len(unmatched_files)} files are:")
    print(f"  ? Video content")
    print(f"  ? Podcast content")
    print(f"  ? Files without titles")
    print(f"  ? Other content")
    print()
    
    # What you're missing
    catalog_titles = set(all_catalog_songs.keys())
    current_titles = set(f['title_lower'] for f in current_files.values() if f['title_lower'])
    
    missing_from_catalog = catalog_titles - current_titles
    
    print(f"Songs in catalog you DON'T have downloaded: {len(missing_from_catalog)}")
    print()
    
    # Save comparison
    output = Path.home() / 'Music/SUNO_COMPARISON.csv'
    
    with open(output, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['Filename', 'Title', 'Status', 'Duration', 'Notes'])
        
        for filename, title, catalog_entry in matched:
            writer.writerow([filename, title, 'IN_CATALOG', current_files[filename]['duration_formatted'], 'Confirmed Suno song'])
        
        for filename, file_info in unmatched_files:
            writer.writerow([filename, file_info['title'], 'NOT_IN_CATALOG', file_info['duration_formatted'], 'Review - may be video/podcast'])
    
    print(f"? Comparison saved to: {output}")
    print()
    
    print("=" * 80)
    print("  SUMMARY")
    print("=" * 80 + "\n")
    
    print(f"? {len(matched)} files are confirmed Suno music")
    print(f"? {len(unmatched_files)} files need review (likely video/podcast)")
    print(f"?? {len(missing_from_catalog)} songs in catalog not yet downloaded")

if __name__ == '__main__':
    compare_catalogs()
