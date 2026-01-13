#!/usr/bin/env python3
"""
EASY MUSIC ORGANIZER
Simple, smart organization using all gathered intelligence
Understands: 322 = 3:22 duration, series patterns, etc.
"""

import csv
from pathlib import Path
import shutil
import re

def parse_duration_from_filename(filename: str) -> str:
    """Extract duration from filename patterns like 322 = 3:22"""
    
    # Look for patterns like: song322, song-322, song_322
    match = re.search(r'(\d{3,4})(?:\.mp3|$|-|_)', filename)
    
    if match:
        num = match.group(1)
        
        if len(num) == 3:
            # 322 = 3:22
            minutes = num[0]
            seconds = num[1:3]
            return f"{minutes}:{seconds}"
        elif len(num) == 4:
            # 1022 = 10:22
            minutes = num[:2]
            seconds = num[2:4]
            return f"{minutes}:{seconds}"
    
    return ""

def identify_series(filename: str) -> str:
    """Identify which series this song belongs to"""
    
    name_lower = filename.lower()
    
    # Series patterns
    series_patterns = {
        'Bite in the Night': ['bite', 'bitin'],
        'Blues in the Moonlit Nights': ['blues', 'moonlit', 'moonlight'],
        'Feather Fang': ['feather', 'fang'],
        'Book of Memory': ['bookOmemory', 'book'],
        'Heart Songs': ['heart cover', 'heart_cover'],
        'Sammy\'s Serenade': ['sammy', 'serenade'],
        'Alley Songs': ['alley', 'hide'],
        'Junkyard Symphony': ['junkyard', 'scraps', 'refuse'],
        'Heartbeats in the Dark': ['heartbeat'],
        'Workshop Worries': ['workshop'],
        'Petals Fall': ['petal', 'fall'],
        'Kings and Queens': ['kings', 'queens', 'litter'],
        'Echoes': ['echoes'],
        'Descriptive Origins': ['descriptive'],
    }
    
    for series, keywords in series_patterns.items():
        if any(kw in name_lower for kw in keywords):
            return series
    
    return 'Misc Songs'

def get_version_info(filename: str) -> dict:
    """Extract version information from filename"""
    
    info = {
        'is_remix': False,
        'is_remastered': False,
        'is_live': False,
        'is_edit': False,
        'version_number': '',
        'duration_tag': ''
    }
    
    name_lower = filename.lower()
    
    if 'remix' in name_lower:
        info['is_remix'] = True
    if 'remaster' in name_lower:
        info['is_remastered'] = True
    if 'live' in name_lower:
        info['is_live'] = True
    if 'edit' in name_lower:
        info['is_edit'] = True
    
    # Get duration tag
    duration = parse_duration_from_filename(filename)
    if duration:
        info['duration_tag'] = duration
    
    return info

def generate_clean_name(filename: str, series: str, version_info: dict) -> str:
    """Generate clean, organized filename"""
    
    stem = Path(filename).stem
    
    # Start with series
    parts = [series]
    
    # Add duration tag if present
    if version_info['duration_tag']:
        parts.append(f"({version_info['duration_tag']})")
    
    # Add version info
    version_tags = []
    if version_info['is_remastered']:
        version_tags.append('Remastered')
    if version_info['is_remix']:
        version_tags.append('Remix')
    if version_info['is_live']:
        version_tags.append('Live')
    if version_info['is_edit']:
        version_tags.append('Edit')
    
    if version_tags:
        parts.append(f"[{' '.join(version_tags)}]")
    
    return ' - '.join(parts) + '.mp3'

def main():
    print("\n" + "?" * 40)
    print("  EASY MUSIC ORGANIZER")
    print("  Simple smart organization")
    print("?" * 40 + "\n")
    
    home = Path.home()
    
    # Scan YOUR_SUNO_SONGS and DOWNLOADED folders
    music_dir = home / 'Music/nocTurneMeLoDieS/FINAL_ORGANIZED/YOUR_SUNO_SONGS'
    
    if not music_dir.exists():
        print(f"? Directory not found: {music_dir}")
        return
    
    print(f"Scanning: {music_dir}\n")
    
    # Find all MP3s
    all_mp3s = list(music_dir.rglob('*.mp3'))
    
    print(f"Found {len(all_mp3s)} MP3 files\n")
    
    # Analyze and organize
    print("Analyzing files...\n")
    
    organization_plan = {}
    
    for mp3 in all_mp3s:
        series = identify_series(mp3.name)
        version_info = get_version_info(mp3.name)
        
        if series not in organization_plan:
            organization_plan[series] = []
        
        organization_plan[series].append({
            'current_path': mp3,
            'current_name': mp3.name,
            'series': series,
            'version_info': version_info,
            'suggested_name': generate_clean_name(mp3.name, series, version_info),
            'current_folder': mp3.parent.name
        })
    
    # Show organization plan
    print("=" * 80)
    print("  ORGANIZATION PLAN")
    print("=" * 80 + "\n")
    
    for series in sorted(organization_plan.keys()):
        songs = organization_plan[series]
        print(f"\n{series} ({len(songs)} songs):")
        
        for song in sorted(songs, key=lambda x: x['current_name'])[:5]:
            print(f"  ? {song['current_name']}")
            if song['version_info']['duration_tag']:
                print(f"    Duration tag: {song['version_info']['duration_tag']}")
            if song['current_name'] != song['suggested_name']:
                print(f"    ? Suggested: {song['suggested_name']}")
        
        if len(songs) > 5:
            print(f"  ... and {len(songs) - 5} more")
    
    print()
    print("=" * 80)
    print("  RECOMMENDED STRUCTURE")
    print("=" * 80 + "\n")
    
    print("Create folders in YOUR_SUNO_SONGS/:")
    for series in sorted(organization_plan.keys()):
        count = len(organization_plan[series])
        folder_name = series.replace(' ', '_').replace("'", '')
        print(f"  ? {folder_name}/ ({count} songs)")
    
    print()
    
    # Save organization plan
    output = home / 'Music/EASY_ORGANIZATION_PLAN.csv'
    
    with open(output, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow([
            'Series', 'Current_Name', 'Suggested_Name', 
            'Current_Folder', 'Target_Folder',
            'Duration_Tag', 'Is_Remix', 'Is_Remastered', 'Is_Live',
            'Current_Path', 'Action'
        ])
        
        for series, songs in sorted(organization_plan.items()):
            target_folder = series.replace(' ', '_').replace("'", '')
            
            for song in songs:
                writer.writerow([
                    series,
                    song['current_name'],
                    song['suggested_name'],
                    song['current_folder'],
                    target_folder,
                    song['version_info']['duration_tag'],
                    'YES' if song['version_info']['is_remix'] else 'NO',
                    'YES' if song['version_info']['is_remastered'] else 'NO',
                    'YES' if song['version_info']['is_live'] else 'NO',
                    str(song['current_path']),
                    'MOVE to series folder' if song['current_folder'] != target_folder else 'RENAME only'
                ])
    
    print(f"? Organization plan saved: {output}\n")
    
    print("=" * 80)
    print("  ? EASY ORGANIZATION READY")
    print("=" * 80 + "\n")
    
    print("Next steps:")
    print("  1. Review the plan:")
    print(f"     open '{output}'")
    print()
    print("  2. Apply organization (I can create this):")
    print("     python3 ~/advanced_toolkit/apply_easy_organization.py")
    print()
    print("  3. Or do manually in Finder:")
    print("     - Create series folders")
    print("     - Drag songs into appropriate series")
    print("     - Clean names will help you see what's what!")
    print()
    
    print(f"Open plan: open '{output}'")

if __name__ == '__main__':
    main()
