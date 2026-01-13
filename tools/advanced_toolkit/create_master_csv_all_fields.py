#!/usr/bin/env python3
"""
Create MASTER CSV with ALL fields from all sources
Every single piece of data in one place
"""

import csv
from pathlib import Path
from collections import defaultdict

def normalize_title(title: str) -> str:
    """Normalize for matching"""
    if not title:
        return ""
    return title.lower().replace('_', ' ').replace('-', ' ').strip()

def safe_get(d: dict, *keys):
    """Get value from dict, trying multiple keys"""
    for key in keys:
        if key in d and d[key]:
            return d[key]
    return ''

def main():
    print("\n" + "??" * 40)
    print("  CREATING MASTER CSV WITH ALL FIELDS")
    print("  Everything in one place")
    print("??" * 40 + "\n")
    
    # Load all data
    print("Loading data sources...")
    
    # Google Sheet 1 (metadata, URLs)
    sheet1_data = {}
    sheet1_path = Path.home() / 'Music/GOOGLE_SHEET_SUNO_DATA.csv'
    if sheet1_path.exists():
        with open(sheet1_path, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                title = safe_get(row, 'SongTitle', 'Title', 'title')
                if title:
                    sheet1_data[normalize_title(title)] = row
        print(f"? Google Sheet 1: {len(sheet1_data)} songs")
    
    # Google Sheet 2 (lyrics!)
    sheet2_data = {}
    sheet2_path = Path.home() / 'Music/GOOGLE_SHEET_2_SUNO_DATA.csv'
    if sheet2_path.exists():
        with open(sheet2_path, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                title = safe_get(row, 'songName', 'SongTitle', 'Title', 'title')
                if title:
                    sheet2_data[normalize_title(title)] = row
        print(f"? Google Sheet 2: {len(sheet2_data)} songs (with lyrics)")
    
    # Local files
    local_data = {}
    local_path = Path.home() / 'Downloads/YOUR_SUNO_SONGS_COMPLETE - MASTER_MERGED_DATA (1).csv'
    if local_path.exists():
        with open(local_path, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                filename = row.get('filename', '')
                title = row.get('title', '')
                if filename:
                    key = normalize_title(title) if title else normalize_title(filename)
                    if key not in local_data:
                        local_data[key] = []
                    local_data[key].append(row)
        print(f"? Local files: {len(local_data)} unique titles/filenames")
    
    # Suno catalog
    suno_data = {}
    suno_path = Path.home() / 'Music/nocTurneMeLoDieS/SUNO/suno-sept/songs_master_combined.csv'
    if suno_path.exists():
        with open(suno_path, 'r', encoding='utf-8', errors='ignore') as f:
            reader = csv.DictReader(f)
            for row in reader:
                title = safe_get(row, 'SongTitle', 'Title')
                if title:
                    suno_data[normalize_title(title)] = row
        print(f"? Suno catalog: {len(suno_data)} songs")
    
    print()
    
    # Build master list
    print("Building master database...")
    
    master_entries = []
    all_keys = set()
    all_keys.update(sheet1_data.keys())
    all_keys.update(sheet2_data.keys())
    all_keys.update(local_data.keys())
    
    for key in sorted(all_keys):
        entry = {}
        
        # Get data from each source
        s1 = sheet1_data.get(key, {})
        s2 = sheet2_data.get(key, {})
        local_files = local_data.get(key, [])
        suno = suno_data.get(key, {})
        
        # Primary identification
        entry['Title'] = safe_get(s1, 'SongTitle', 'Title') or safe_get(s2, 'songName') or (local_files[0].get('title') if local_files else '') or key
        entry['Artist'] = safe_get(s1, 'Artist') or safe_get(s2, 'author') or (local_files[0].get('artist') if local_files else '')
        
        # From Google Sheet 1
        entry['Cover_URL'] = safe_get(s1, 'CoverUrl', 'CoverURL')
        entry['Song_URL'] = safe_get(s1, 'SongURL', 'songLink')
        entry['Genre'] = safe_get(s1, 'Genre')
        entry['Mood'] = safe_get(s1, 'Mood')
        entry['Description'] = safe_get(s1, 'Description')
        entry['Prompt'] = safe_get(s1, 'Prompt')
        entry['Created'] = safe_get(s1, 'Created', 'DateCreated')
        entry['Duration'] = safe_get(s1, 'Duration')
        
        # From Google Sheet 2 (LYRICS!)
        entry['Lyrics'] = safe_get(s2, 'lyrics')
        entry['Style'] = safe_get(s2, 'style')
        entry['Published'] = safe_get(s2, 'published')
        entry['Version'] = safe_get(s2, 'version')
        entry['Playlist'] = safe_get(s2, 'playlist')
        entry['Plays'] = safe_get(s2, 'plays')
        entry['Length'] = safe_get(s2, 'length')
        
        # From local files
        if local_files:
            entry['Have_Local_File'] = 'YES'
            entry['Local_Filenames'] = ' | '.join([f.get('filename', '') for f in local_files])
            entry['File_Size'] = local_files[0].get('size', '')
            entry['File_Duration'] = local_files[0].get('duration', '')
            entry['File_Path'] = local_files[0].get('path', '')
            entry['Content_Type'] = local_files[0].get('content_type', '')
        else:
            entry['Have_Local_File'] = 'NO'
            entry['Local_Filenames'] = ''
            entry['File_Size'] = ''
            entry['File_Duration'] = ''
            entry['File_Path'] = ''
            entry['Content_Type'] = ''
        
        # From Suno catalog
        entry['In_Suno_Catalog'] = 'YES' if suno else 'NO'
        
        # Status
        if entry['Have_Local_File'] == 'YES' and (s1 or s2):
            entry['Status'] = 'COMPLETE'
            entry['Recommendation'] = 'Have file + metadata + lyrics'
        elif s1 or s2:
            entry['Status'] = 'NEED_DOWNLOAD'
            entry['Recommendation'] = 'Download from Suno using Song_URL'
        elif entry['Have_Local_File'] == 'YES':
            entry['Status'] = 'LOCAL_ONLY'
            entry['Recommendation'] = 'Review - may be video/podcast/other content'
        else:
            entry['Status'] = 'UNKNOWN'
            entry['Recommendation'] = 'Review'
        
        master_entries.append(entry)
    
    print(f"? Created {len(master_entries)} master entries\n")
    
    # Save master CSV
    output = Path.home() / 'Music/MASTER_COMPLETE_ALL_FIELDS.csv'
    
    print("Writing master CSV...")
    
    fieldnames = [
        # Identification
        'Title', 'Artist', 'Status', 'Recommendation',
        
        # URLs & Links
        'Song_URL', 'Cover_URL', 'Playlist',
        
        # Metadata
        'Genre', 'Mood', 'Style', 'Description', 'Prompt',
        'Created', 'Published', 'Duration', 'Length', 'Version', 'Plays',
        
        # LYRICS!
        'Lyrics',
        
        # Local file info
        'Have_Local_File', 'Local_Filenames', 'File_Path',
        'File_Size', 'File_Duration', 'Content_Type',
        
        # Catalog
        'In_Suno_Catalog',
    ]
    
    with open(output, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, extrasaction='ignore')
        writer.writeheader()
        writer.writerows(master_entries)
    
    print(f"? Saved to: {output}\n")
    
    # Statistics
    print("=" * 80)
    print("  ?? STATISTICS")
    print("=" * 80 + "\n")
    
    complete = sum(1 for e in master_entries if e['Status'] == 'COMPLETE')
    need_dl = sum(1 for e in master_entries if e['Status'] == 'NEED_DOWNLOAD')
    local_only = sum(1 for e in master_entries if e['Status'] == 'LOCAL_ONLY')
    have_lyrics = sum(1 for e in master_entries if e['Lyrics'])
    have_urls = sum(1 for e in master_entries if e['Song_URL'])
    have_cover = sum(1 for e in master_entries if e['Cover_URL'])
    
    print(f"Total entries: {len(master_entries)}")
    print(f"\nStatus breakdown:")
    print(f"  ? COMPLETE (file + metadata): {complete}")
    print(f"  ?? NEED_DOWNLOAD: {need_dl}")
    print(f"  ?? LOCAL_ONLY: {local_only}")
    print(f"\nContent available:")
    print(f"  ?? Have lyrics: {have_lyrics}")
    print(f"  ?? Have song URLs: {have_urls}")
    print(f"  ???  Have cover art URLs: {have_cover}")
    print()
    
    print("=" * 80)
    print("  ? MASTER CSV COMPLETE")
    print("=" * 80 + "\n")
    
    print(f"?? Master file: {output}")
    print(f"\nIncludes ALL fields from:")
    print(f"  ? Google Sheet 1 (metadata, URLs, prompts)")
    print(f"  ? Google Sheet 2 (FULL LYRICS!)")
    print(f"  ? Local files (paths, sizes, durations)")
    print(f"  ? Suno catalog (verification)")
    print(f"\nOpen: open '{output}'")

if __name__ == '__main__':
    main()
