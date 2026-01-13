#!/usr/bin/env python3
"""
Compare Today's Findings with Current Structure
Match discovered songs against existing Vol 1-12 organization
"""

import csv
from pathlib import Path
from difflib import SequenceMatcher
from collections import defaultdict

def normalize_title(title: str) -> str:
    """Normalize for matching"""
    if not title:
        return ""
    return title.lower().replace('_', ' ').replace('-', ' ').strip()

def similarity_score(s1: str, s2: str) -> float:
    """Calculate similarity"""
    return SequenceMatcher(None, normalize_title(s1), normalize_title(s2)).ratio()

def main():
    print("\n" + "??" * 40)
    print("  COMPARE FINDINGS WITH CURRENT STRUCTURE")
    print("  What's new vs what you already have")
    print("??" * 40 + "\n")
    
    home = Path.home()
    
    # Load today's findings
    print("Loading today's findings...\n")
    
    unified_catalog = home / 'Music/nocTurneMeLoDieS/DATA/UNIFIED_MASTER_CATALOG.csv'
    
    if not unified_catalog.exists():
        print("? Unified catalog not found")
        return
    
    findings = []
    with open(unified_catalog, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            # Only YOUR music that is SONG type
            if (row.get('is_your_music') in ['YES', 'True', 'TRUE'] and 
                row.get('content_type') == 'SONG'):
                findings.append(row)
    
    print(f"? Found {len(findings)} of YOUR songs (SONG type only)\n")
    
    # Scan current structure
    print("Scanning your current Vol 1-12 structure...\n")
    
    nocturne_dir = home / 'Music/nocTurneMeLoDieS'
    
    current_songs = []
    
    # Scan all existing albums
    for vol_dir in nocturne_dir.iterdir():
        if not vol_dir.is_dir() or vol_dir.name.startswith('.'):
            continue
        
        # Get all MP3s in this album/volume
        for mp3 in vol_dir.rglob('*.mp3'):
            current_songs.append({
                'filepath': str(mp3),
                'filename': mp3.name,
                'title': mp3.stem,
                'album': vol_dir.name,
                'path_obj': mp3
            })
    
    print(f"? Found {len(current_songs)} songs in current structure\n")
    
    # Compare
    print("Comparing...\n")
    
    # Build lookup by normalized title
    current_lookup = {}
    for song in current_songs:
        title_norm = normalize_title(song['title'])
        current_lookup[title_norm] = song
    
    # Categorize findings
    already_have = []
    new_songs = []
    duplicates = []
    
    for finding in findings:
        title = finding.get('title') or finding.get('filename', '')
        title_norm = normalize_title(title)
        filepath = finding.get('filepath') or finding.get('current_path') or ''
        
        # Check if already in structure
        if title_norm in current_lookup:
            # Check if same file or different
            if str(current_lookup[title_norm]['filepath']) == filepath:
                already_have.append({
                    'title': title,
                    'album': current_lookup[title_norm]['album'],
                    'filepath': filepath,
                    'status': 'ALREADY_ORGANIZED'
                })
            else:
                duplicates.append({
                    'title': title,
                    'existing_path': current_lookup[title_norm]['filepath'],
                    'new_path': filepath,
                    'existing_album': current_lookup[title_norm]['album']
                })
        else:
            # Fuzzy match to catch slight name differences
            best_match = None
            best_score = 0
            
            for existing_title, existing_song in current_lookup.items():
                score = similarity_score(title, existing_title)
                if score > best_score:
                    best_score = score
                    best_match = existing_song
            
            if best_score > 0.85:
                already_have.append({
                    'title': title,
                    'album': best_match['album'],
                    'filepath': filepath,
                    'status': f'ALREADY_HAVE (fuzzy match: {best_score:.0%})'
                })
            else:
                new_songs.append({
                    'title': title,
                    'filepath': filepath,
                    'completeness': finding.get('completeness_score', '0'),
                    'has_lyrics': finding.get('has_lyrics', 'NO'),
                    'in_google_sheet': finding.get('in_google_sheet_1', 'NO'),
                    'status': 'NEW_SONG'
                })
    
    # Results
    print("=" * 80)
    print("  ?? COMPARISON RESULTS")
    print("=" * 80 + "\n")
    
    print(f"Total YOUR songs found today: {len(findings)}")
    print(f"Already in your structure: {len(already_have)}")
    print(f"NEW songs (not in structure): {len(new_songs)}")
    print(f"Duplicates (same song, different file): {len(duplicates)}")
    print()
    
    # Save results
    output = home / 'Music/FINDINGS_VS_CURRENT_STRUCTURE.csv'
    
    with open(output, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow([
            'Title', 'Status', 'Current_Album', 'Filepath',
            'Completeness', 'Has_Lyrics', 'In_Google_Sheet',
            'Recommendation'
        ])
        
        # Already have
        for song in sorted(already_have, key=lambda x: x.get('album', '')):
            writer.writerow([
                song['title'],
                song['status'],
                song.get('album', ''),
                song['filepath'],
                '',
                '',
                '',
                'Already organized'
            ])
        
        # New songs
        for song in sorted(new_songs, key=lambda x: -int(x.get('completeness', 0))):
            # Suggest which volume based on characteristics
            if 'bite' in song['title'].lower():
                suggestion = 'Add to Bite_in_the_Night_Vol_1/ (new series)'
            elif 'blues' in song['title'].lower() or 'moonlit' in song['title'].lower():
                suggestion = 'Add to Blues_in_the_Alley_Vol_3/ or Moonlight_Serenade/'
            elif 'feather' in song['title'].lower() or 'fang' in song['title'].lower():
                suggestion = 'Add to Feather_Fang_Vol_1/ (new series)'
            elif 'book' in song['title'].lower() or 'memory' in song['title'].lower():
                suggestion = 'Add to Book_of_Memory_Vol_1/ (new series)'
            elif int(song.get('completeness', 0)) >= 7:
                suggestion = 'Add to Steven_Chaplinski_Collection_Vol_13/ (high quality)'
            else:
                suggestion = 'Add to Steven_Chaplinski_Collection_Vol_14/ (review first)'
            
            writer.writerow([
                song['title'],
                song['status'],
                'NOT_IN_STRUCTURE',
                song['filepath'],
                song['completeness'],
                song['has_lyrics'],
                song['in_google_sheet'],
                suggestion
            ])
        
        # Duplicates
        for dup in duplicates:
            writer.writerow([
                dup['title'],
                'DUPLICATE',
                dup['existing_album'],
                f"Existing: {dup['existing_path']} | New: {dup['new_path']}",
                '',
                '',
                '',
                'Review - may be different version or remove duplicate'
            ])
    
    print(f"? Comparison saved: {output}\n")
    
    # Show new songs breakdown
    print("=" * 80)
    print("  ?? NEW SONGS BREAKDOWN")
    print("=" * 80 + "\n")
    
    # Group new songs by suggested series
    by_series = defaultdict(list)
    for song in new_songs:
        title_lower = song['title'].lower()
        
        if 'bite' in title_lower:
            by_series['Bite_in_the_Night_Vol_1'].append(song)
        elif 'feather' in title_lower or 'fang' in title_lower:
            by_series['Feather_Fang_Vol_1'].append(song)
        elif 'book' in title_lower or 'memory' in title_lower:
            by_series['Book_of_Memory_Vol_1'].append(song)
        elif 'blues' in title_lower or 'moonlit' in title_lower:
            by_series['Blues_Series'].append(song)
        elif 'heart' in title_lower and 'cover' in title_lower:
            by_series['Heart_Songs_Vol_1'].append(song)
        elif int(song.get('completeness', 0)) >= 7:
            by_series['Steven_Chaplinski_Collection_Vol_13'].append(song)
        else:
            by_series['Steven_Chaplinski_Collection_Vol_14'].append(song)
    
    print("New songs by suggested location:")
    for series in sorted(by_series.keys()):
        songs = by_series[series]
        print(f"  ?? {series}: {len(songs)} songs")
    
    print()
    
    # Summary
    print("=" * 80)
    print("  ? COMPARISON COMPLETE")
    print("=" * 80 + "\n")
    
    print(f"?? Full comparison: {output}\n")
    
    print("Summary:")
    print(f"  ? {len(already_have)} songs already in your structure")
    print(f"  ?? {len(new_songs)} NEW songs to add")
    print(f"  ??  {len(duplicates)} duplicates to review")
    print()
    
    print("Next steps:")
    print("  1. Review FINDINGS_VS_CURRENT_STRUCTURE.csv")
    print("  2. Decide: Create new series volumes OR add to existing")
    print("  3. Run organization script to apply")
    print()
    
    print(f"Open: open '{output}'")

if __name__ == '__main__':
    main()
