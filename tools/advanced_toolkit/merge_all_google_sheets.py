#!/usr/bin/env python3
"""
Merge ALL Google Sheets + Local Data
Comprehensive integration of all data sources
"""

import csv
from pathlib import Path
from collections import defaultdict
from difflib import SequenceMatcher

def normalize_title(title: str) -> str:
    """Normalize for matching"""
    if not title:
        return ""
    return title.lower().replace('_', ' ').replace('-', ' ').strip()

def load_all_data_sources():
    """Load everything"""
    
    print("\n" + "=" * 80)
    print("  LOADING ALL DATA SOURCES")
    print("=" * 80 + "\n")
    
    sources = {}
    
    # Google Sheet 1
    sheet1 = Path.home() / 'Music/GOOGLE_SHEET_SUNO_DATA.csv'
    if sheet1.exists():
        with open(sheet1, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            sources['google_sheet_1'] = list(reader)
        print(f"? Google Sheet 1: {len(sources['google_sheet_1'])} rows")
    
    # Google Sheet 2
    sheet2 = Path.home() / 'Music/GOOGLE_SHEET_2_SUNO_DATA.csv'
    if sheet2.exists():
        with open(sheet2, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            sources['google_sheet_2'] = list(reader)
        print(f"? Google Sheet 2: {len(sources['google_sheet_2'])} rows")
    
    # Local files
    local_csv = Path.home() / 'Downloads/YOUR_SUNO_SONGS_COMPLETE - MASTER_MERGED_DATA (1).csv'
    if local_csv.exists():
        with open(local_csv, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            sources['local_files'] = [row for row in reader if row.get('filename')]
        print(f"? Local files: {len(sources['local_files'])} files")
    
    # Suno master catalog
    suno_master = Path.home() / 'Music/nocTurneMeLoDieS/SUNO/suno-sept/songs_master_combined.csv'
    if suno_master.exists():
        with open(suno_master, 'r', encoding='utf-8', errors='ignore') as f:
            reader = csv.DictReader(f)
            sources['suno_catalog'] = list(reader)
        print(f"? Suno catalog: {len(sources['suno_catalog'])} songs")
    
    print()
    return sources

def build_unified_database(sources: dict):
    """Build unified database of all songs"""
    
    print("=" * 80)
    print("  BUILDING UNIFIED DATABASE")
    print("=" * 80 + "\n")
    
    unified = {}
    
    # Process Google Sheet 1
    if 'google_sheet_1' in sources:
        for row in sources['google_sheet_1']:
            title = row.get('SongTitle', '') or row.get('Title', '')
            if title:
                title_norm = normalize_title(title)
                if title_norm not in unified:
                    unified[title_norm] = {
                        'title': title,
                        'in_google_sheet_1': True,
                        'google_1_data': row,
                        'in_google_sheet_2': False,
                        'in_suno_catalog': False,
                        'local_files': [],
                        'cover_url': row.get('CoverUrl', ''),
                        'song_url': row.get('SongURL', ''),
                        'genre': row.get('Genre', ''),
                    }
    
    # Process Google Sheet 2
    if 'google_sheet_2' in sources:
        for row in sources['google_sheet_2']:
            title = row.get('SongTitle', '') or row.get('Title', '') or row.get('title', '')
            if title:
                title_norm = normalize_title(title)
                if title_norm not in unified:
                    unified[title_norm] = {
                        'title': title,
                        'in_google_sheet_1': False,
                        'in_google_sheet_2': True,
                        'google_2_data': row,
                        'in_suno_catalog': False,
                        'local_files': [],
                    }
                else:
                    unified[title_norm]['in_google_sheet_2'] = True
                    unified[title_norm]['google_2_data'] = row
    
    # Process Suno catalog
    if 'suno_catalog' in sources:
        for row in sources['suno_catalog']:
            title = row.get('SongTitle', '')
            if title:
                title_norm = normalize_title(title)
                if title_norm in unified:
                    unified[title_norm]['in_suno_catalog'] = True
    
    # Process local files
    if 'local_files' in sources:
        for row in sources['local_files']:
            filename = row.get('filename', '')
            title = row.get('title', '')
            
            if not filename:
                continue
            
            # Try to match by title
            if title:
                title_norm = normalize_title(title)
                if title_norm in unified:
                    unified[title_norm]['local_files'].append(filename)
                else:
                    # Create entry for local-only file
                    unified[title_norm] = {
                        'title': title,
                        'in_google_sheet_1': False,
                        'in_google_sheet_2': False,
                        'in_suno_catalog': False,
                        'local_files': [filename],
                        'local_data': row,
                    }
            else:
                # No title - try filename
                filename_norm = normalize_title(filename)
                if filename_norm not in unified:
                    unified[filename_norm] = {
                        'title': '',
                        'in_google_sheet_1': False,
                        'in_google_sheet_2': False,
                        'in_suno_catalog': False,
                        'local_files': [filename],
                        'local_data': row,
                    }
    
    print(f"? Unified database: {len(unified)} unique entries\n")
    
    return unified

def analyze_unified(unified: dict):
    """Analyze the unified database"""
    
    print("=" * 80)
    print("  UNIFIED ANALYSIS")
    print("=" * 80 + "\n")
    
    stats = {
        'in_both_sheets': 0,
        'in_sheet_1_only': 0,
        'in_sheet_2_only': 0,
        'have_local_file': 0,
        'confirmed_suno': 0,
        'complete_sets': 0,  # Have file + sheet data
    }
    
    for entry in unified.values():
        if entry['in_google_sheet_1'] and entry['in_google_sheet_2']:
            stats['in_both_sheets'] += 1
        elif entry['in_google_sheet_1']:
            stats['in_sheet_1_only'] += 1
        elif entry['in_google_sheet_2']:
            stats['in_sheet_2_only'] += 1
        
        if entry['local_files']:
            stats['have_local_file'] += 1
        
        if entry['in_suno_catalog']:
            stats['confirmed_suno'] += 1
        
        if entry['local_files'] and (entry['in_google_sheet_1'] or entry['in_google_sheet_2']):
            stats['complete_sets'] += 1
    
    print("Statistics:")
    print(f"  Total unique songs/files: {len(unified)}")
    print(f"  In both Google Sheets: {stats['in_both_sheets']}")
    print(f"  In Sheet 1 only: {stats['in_sheet_1_only']}")
    print(f"  In Sheet 2 only: {stats['in_sheet_2_only']}")
    print(f"  Have local file: {stats['have_local_file']}")
    print(f"  Confirmed in Suno catalog: {stats['confirmed_suno']}")
    print(f"  Complete sets (file + sheet): {stats['complete_sets']}")
    print()
    
    return stats

def save_master_unified(unified: dict):
    """Save master unified CSV"""
    
    output = Path.home() / 'Music/MASTER_UNIFIED_ALL_SOURCES.csv'
    
    print("=" * 80)
    print("  SAVING MASTER UNIFIED DATABASE")
    print("=" * 80 + "\n")
    
    with open(output, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow([
            'Title', 
            'In Google Sheet 1', 'In Google Sheet 2', 'In Suno Catalog',
            'Have Local File', 'Local Filenames',
            'Cover URL', 'Song URL', 'Genre',
            'Status', 'Recommendation'
        ])
        
        for entry in sorted(unified.values(), key=lambda x: x.get('title', '')):
            # Determine status
            if entry['local_files'] and (entry['in_google_sheet_1'] or entry['in_google_sheet_2']):
                status = 'COMPLETE'
                recommendation = 'Have file + metadata - ready to use'
            elif entry['in_google_sheet_1'] or entry['in_google_sheet_2']:
                status = 'NEED_DOWNLOAD'
                recommendation = 'Download from Suno'
            elif entry['local_files']:
                status = 'LOCAL_ONLY'
                recommendation = 'Review - may be video/podcast/other'
            else:
                status = 'UNKNOWN'
                recommendation = 'Review'
            
            writer.writerow([
                entry.get('title', ''),
                'YES' if entry['in_google_sheet_1'] else '',
                'YES' if entry['in_google_sheet_2'] else '',
                'YES' if entry['in_suno_catalog'] else '',
                'YES' if entry['local_files'] else '',
                '; '.join(entry['local_files']) if entry['local_files'] else '',
                entry.get('cover_url', ''),
                entry.get('song_url', ''),
                entry.get('genre', ''),
                status,
                recommendation
            ])
    
    print(f"? Saved to: {output}\n")
    
    return output

def main():
    print("\n" + "??" * 40)
    print("  MERGE ALL GOOGLE SHEETS + LOCAL DATA")
    print("  Complete Integration")
    print("??" * 40)
    
    # Load everything
    sources = load_all_data_sources()
    
    # Build unified database
    unified = build_unified_database(sources)
    
    # Analyze
    stats = analyze_unified(unified)
    
    # Save master file
    output = save_master_unified(unified)
    
    print("=" * 80)
    print("  ? MASTER INTEGRATION COMPLETE")
    print("=" * 80 + "\n")
    
    print(f"Master file: {output}")
    print(f"\nThis merges:")
    print(f"  ? Google Sheet 1 (466 rows)")
    print(f"  ? Google Sheet 2 (if different)")
    print(f"  ? Local files (341 files)")
    print(f"  ? Suno catalog")
    print(f"\nFilter by 'Status' column:")
    print(f"  COMPLETE ? Have file + metadata")
    print(f"  NEED_DOWNLOAD ? In sheets, need to download")
    print(f"  LOCAL_ONLY ? Have file, review if music or other")
    print(f"\nOpen: open {output}")

if __name__ == '__main__':
    main()
