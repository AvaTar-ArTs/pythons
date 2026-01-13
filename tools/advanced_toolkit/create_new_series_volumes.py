#!/usr/bin/env python3
"""
Create New Series Volumes
Based on user's preference: Create themed series, NOT generic Vol_13/14
"""

import csv
from pathlib import Path
import shutil
from difflib import SequenceMatcher

def normalize_title(title: str) -> str:
    """Normalize for matching"""
    if not title:
        return ""
    return title.lower().replace('_', ' ').replace('-', ' ').strip()

def main():
    print("\n" + "??" * 40)
    print("  CREATE NEW SERIES VOLUMES")
    print("  Themed series, NOT generic collections")
    print("??" * 40 + "\n")
    
    home = Path.home()
    comparison_csv = home / 'Music/FINDINGS_VS_CURRENT_STRUCTURE.csv'
    nocturne_dir = home / 'Music/nocTurneMeLoDieS'
    
    if not comparison_csv.exists():
        print("? Comparison CSV not found")
        return
    
    # Load new songs
    print("Loading NEW songs to organize...\n")
    
    new_songs = []
    with open(comparison_csv, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row.get('Status') == 'NEW_SONG':
                new_songs.append(row)
    
    print(f"? Found {len(new_songs)} NEW songs\n")
    
    # Categorize by series
    print("Categorizing by series...\n")
    
    series = {
        'Bite_in_the_Night_Vol_1': [],
        'Feather_Fang_Vol_1': [],
        'Book_of_Memory_Vol_1': [],
        'Heart_Songs_Vol_1': [],
        'Petals_Fall_Vol_1': [],
        'Workshop_Worries_Vol_1': [],
        'Blues_in_the_Alley_Vol_3': [],  # Add to existing Blues series
        'Uncategorized_New': []
    }
    
    for song in new_songs:
        title = song.get('Title', '').lower()
        recommendation = song.get('Recommendation', '')
        
        if 'bite_in_the_night_vol_1' in recommendation.lower():
            series['Bite_in_the_Night_Vol_1'].append(song)
        elif 'feather_fang_vol_1' in recommendation.lower():
            series['Feather_Fang_Vol_1'].append(song)
        elif 'book_of_memory_vol_1' in recommendation.lower():
            series['Book_of_Memory_Vol_1'].append(song)
        elif 'blues' in recommendation.lower():
            series['Blues_in_the_Alley_Vol_3'].append(song)
        elif 'heart' in title and 'cover' in title:
            series['Heart_Songs_Vol_1'].append(song)
        elif 'petal' in title or 'fall' in title:
            series['Petals_Fall_Vol_1'].append(song)
        elif 'workshop' in title or 'worries' in title:
            series['Workshop_Worries_Vol_1'].append(song)
        else:
            series['Uncategorized_New'].append(song)
    
    # Show plan
    print("=" * 80)
    print("  ?? NEW SERIES VOLUMES TO CREATE")
    print("=" * 80 + "\n")
    
    for series_name, songs in series.items():
        if songs:
            print(f"{series_name}: {len(songs)} songs")
            for song in songs[:5]:
                print(f"  ? {song.get('Title', 'Unknown')}")
            if len(songs) > 5:
                print(f"  ... and {len(songs) - 5} more")
            print()
    
    # Create folders and organize
    print("=" * 80)
    print("  CREATING SERIES VOLUMES")
    print("=" * 80 + "\n")
    
    results = {
        'folders_created': 0,
        'files_moved': 0,
        'skipped': 0,
        'failed': 0
    }
    
    for series_name, songs in series.items():
        if not songs or series_name == 'Uncategorized_New':
            continue
        
        # Create folder
        series_dir = nocturne_dir / series_name
        series_dir.mkdir(exist_ok=True)
        
        print(f"? Created: {series_name}/")
        results['folders_created'] += 1
        
        # Create subfolders (match your avatararts style)
        (series_dir / 'files').mkdir(exist_ok=True)
        (series_dir / 'metadata').mkdir(exist_ok=True)
        (series_dir / 'images').mkdir(exist_ok=True)
        (series_dir / 'prompts').mkdir(exist_ok=True)
        
        # Move files
        for i, song in enumerate(songs, 1):
            filepath = song.get('Filepath', '')
            
            if not filepath or not Path(filepath).exists():
                results['skipped'] += 1
                continue
            
            src = Path(filepath)
            
            # Create numbered filename like your existing albums
            new_filename = f"{i:02d} - {song.get('Title', src.stem)}.mp3"
            dst = series_dir / 'files' / new_filename
            
            try:
                # Handle conflicts
                if dst.exists():
                    counter = 1
                    while dst.exists():
                        new_filename = f"{i:02d} - {song.get('Title', src.stem)} ({counter}).mp3"
                        dst = series_dir / 'files' / new_filename
                        counter += 1
                
                shutil.copy2(src, dst)
                results['files_moved'] += 1
                
            except Exception as e:
                print(f"  ? Failed: {src.name}")
                results['failed'] += 1
    
    print()
    
    # Summary
    print("=" * 80)
    print("  ? SERIES VOLUMES CREATED")
    print("=" * 80 + "\n")
    
    print(f"Folders created: {results['folders_created']}")
    print(f"Files organized: {results['files_moved']}")
    print(f"Skipped: {results['skipped']}")
    print(f"Failed: {results['failed']}")
    print()
    
    print("New series created:")
    for series_name, songs in series.items():
        if songs and series_name != 'Uncategorized_New':
            print(f"  ? {series_name}/ - {len(songs)} songs")
    
    print()
    print(f"All in: {nocturne_dir}")
    print()
    print(f"Open: open '{nocturne_dir}'")

if __name__ == '__main__':
    main()
