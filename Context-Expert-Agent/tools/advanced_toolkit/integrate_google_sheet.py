#!/usr/bin/env python3
"""
Integrate Google Sheet Data
Compare Google Sheet with local files and all CSVs
"""

import csv
from pathlib import Path
from collections import defaultdict
from difflib import SequenceMatcher

def normalize_title(title: str) -> str:
    """Normalize title for matching"""
    if not title:
        return ""
    return title.lower().replace('_', ' ').replace('-', ' ').strip()

def load_google_sheet():
    """Load downloaded Google Sheet"""
    
    sheet_path = Path.home() / 'Music/GOOGLE_SHEET_SUNO_DATA.csv'
    
    print("\n" + "=" * 80)
    print("  LOADING GOOGLE SHEET DATA")
    print("=" * 80 + "\n")
    
    if not sheet_path.exists():
        print("? Google Sheet not downloaded yet")
        return []
    
    with open(sheet_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        rows = list(reader)
    
    print(f"? Loaded {len(rows)} rows from Google Sheet")
    
    # Show columns
    if rows:
        print(f"Columns: {', '.join(rows[0].keys())}\n")
    
    return rows

def load_local_files():
    """Load local file list"""
    
    csv_path = Path.home() / 'Downloads/YOUR_SUNO_SONGS_COMPLETE - MASTER_MERGED_DATA (1).csv'
    
    with open(csv_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        rows = [row for row in reader if row.get('filename')]
    
    print(f"? Loaded {len(rows)} local files\n")
    
    return rows

def compare_and_merge(google_data: list, local_data: list):
    """Compare Google Sheet with local files"""
    
    print("=" * 80)
    print("  COMPARING GOOGLE SHEET WITH LOCAL FILES")
    print("=" * 80 + "\n")
    
    # Build indices
    google_index = {}
    for row in google_data:
        # Get title from various possible columns
        title = (row.get('SongTitle') or row.get('Title') or 
                row.get('title') or row.get('Song') or '').strip()
        if title:
            google_index[normalize_title(title)] = row
    
    local_index = {}
    for row in local_data:
        filename = row.get('filename', '')
        title = row.get('title', '')
        
        if filename:
            local_index[filename] = {
                'title': title,
                'title_norm': normalize_title(title) if title else normalize_title(filename),
                **row
            }
    
    print(f"Google Sheet songs: {len(google_index)}")
    print(f"Local files: {len(local_index)}\n")
    
    # Find matches
    matched = []
    in_google_not_local = []
    in_local_not_google = []
    
    # Check local files against Google
    for filename, local_info in local_index.items():
        title_norm = local_info['title_norm']
        
        if title_norm in google_index:
            matched.append({
                'filename': filename,
                'title': local_info['title'],
                'google_data': google_index[title_norm],
                'local_data': local_info
            })
        else:
            in_local_not_google.append(local_info)
    
    # Check Google against local
    local_titles = {local_info['title_norm'] for local_info in local_index.values()}
    
    for title_norm, google_row in google_index.items():
        if title_norm not in local_titles:
            in_google_not_local.append(google_row)
    
    print("=" * 80)
    print("  RESULTS")
    print("=" * 80 + "\n")
    
    print(f"? MATCHED: {len(matched)} files")
    print(f"   (In both Google Sheet and local)")
    print()
    
    print(f"?? IN GOOGLE, NOT LOCAL: {len(in_google_not_local)} songs")
    print(f"   (Songs in your Google Sheet you haven't downloaded)")
    print()
    
    print(f"?? IN LOCAL, NOT GOOGLE: {len(in_local_not_google)} files")
    print(f"   (Files you have but not in Google Sheet)")
    print()
    
    return matched, in_google_not_local, in_local_not_google

def save_master_comparison(matched, in_google_not_local, in_local_not_google):
    """Save master comparison"""
    
    output = Path.home() / 'Music/GOOGLE_SHEET_COMPARISON.csv'
    
    with open(output, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow([
            'Status', 'Filename', 'Title', 'Duration',
            'In Suno Catalog', 'Has Local File', 'In Google Sheet', 'Notes'
        ])
        
        # Matched files
        for match in matched:
            writer.writerow([
                'MATCHED',
                match['filename'],
                match['title'],
                match['local_data'].get('duration', ''),
                match['local_data'].get('in_suno_catalog', ''),
                'YES',
                'YES',
                'Complete - have file and metadata'
            ])
        
        # In Google not local
        for google_row in in_google_not_local[:100]:  # Limit to 100
            title = (google_row.get('SongTitle') or google_row.get('Title') or 
                    google_row.get('title') or '')
            writer.writerow([
                'MISSING_FILE',
                '',
                title,
                google_row.get('Time', ''),
                '',
                'NO',
                'YES',
                'In Google Sheet - need to download'
            ])
        
        # In local not Google
        for local_info in in_local_not_google[:100]:  # Limit to 100
            writer.writerow([
                'NOT_IN_SHEET',
                local_info.get('filename', ''),
                local_info.get('title', ''),
                local_info.get('duration', ''),
                local_info.get('in_suno_catalog', ''),
                'YES',
                'NO',
                'Have file but not in Google Sheet'
            ])
    
    print(f"? Comparison saved to: {output}\n")
    
    return output

def main():
    print("\n" + "??" * 40)
    print("  INTEGRATE GOOGLE SHEET DATA")
    print("  Cross-reference with all local data")
    print("??" * 40)
    
    # Load Google Sheet
    google_data = load_google_sheet()
    
    if not google_data:
        return
    
    # Load local files
    local_data = load_local_files()
    
    # Compare
    matched, in_google, in_local = compare_and_merge(google_data, local_data)
    
    # Save comparison
    output = save_master_comparison(matched, in_google, in_local)
    
    print("=" * 80)
    print("  ? INTEGRATION COMPLETE")
    print("=" * 80 + "\n")
    
    print(f"Results saved to: {output}")
    print(f"\nNow you can see:")
    print(f"  ? Which files match your Google Sheet")
    print(f"  ? Which songs you need to download")
    print(f"  ? Which local files aren't in the sheet")
    print(f"\nOpen it: open {output}")

if __name__ == '__main__':
    main()
