#!/usr/bin/env python3
"""
Apply Your Exact Structure
Match the And_Also_Special_Guest format:
- files/, images/, metadata/, prompts/
- Filenames: Artist - Song Title.mp3 (NO track numbers)
- README.md for info
"""

import csv
from pathlib import Path
import shutil

def main():
    print("\n" + "?" * 40)
    print("  APPLY YOUR EXACT STRUCTURE")
    print("  Format: Artist - Song Title.mp3")
    print("?" * 40 + "\n")
    
    home = Path.home()
    nocturne_dir = home / 'Music/nocTurneMeLoDieS'
    comparison_csv = home / 'Music/FINDINGS_VS_CURRENT_STRUCTURE.csv'
    
    if not comparison_csv.exists():
        print("? Comparison CSV not found")
        return
    
    # Load NEW songs
    print("Loading NEW songs...\n")
    
    new_songs = []
    with open(comparison_csv, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row.get('Status') == 'NEW_SONG':
                new_songs.append(row)
    
    print(f"? Found {len(new_songs)} NEW songs\n")
    
    # Categorize by series
    series_songs = {
        'Bite_in_the_Night_Vol_1': [],
        'Feather_Fang_Vol_1': [],
        'Book_of_Memory_Vol_1': [],
        'Heart_Songs_Vol_1': [],
        'Petals_Fall_Vol_1': [],
        'Workshop_Worries_Vol_1': [],
        'Blues_in_the_Alley_Vol_3': []
    }
    
    for song in new_songs:
        title = song.get('Title', '').lower()
        rec = song.get('Recommendation', '').lower()
        
        if 'bite' in rec and 'vol_1' in rec:
            series_songs['Bite_in_the_Night_Vol_1'].append(song)
        elif 'feather' in rec and 'vol_1' in rec:
            series_songs['Feather_Fang_Vol_1'].append(song)
        elif 'book' in rec and 'memory' in rec:
            series_songs['Book_of_Memory_Vol_1'].append(song)
        elif 'blues_in_the_alley_vol_3' in rec:
            series_songs['Blues_in_the_Alley_Vol_3'].append(song)
        elif 'heart' in title and 'cover' in title:
            series_songs['Heart_Songs_Vol_1'].append(song)
        elif 'petal' in title or 'fall' in title:
            series_songs['Petals_Fall_Vol_1'].append(song)
        elif 'workshop' in title:
            series_songs['Workshop_Worries_Vol_1'].append(song)
    
    # Process each series
    print("=" * 80)
    print("  POPULATING SERIES VOLUMES")
    print("=" * 80 + "\n")
    
    for series_name, songs in series_songs.items():
        if not songs:
            continue
        
        print(f"{series_name}: {len(songs)} songs")
        
        series_dir = nocturne_dir / series_name
        
        # Ensure structure exists
        files_dir = series_dir / 'files'
        files_dir.mkdir(parents=True, exist_ok=True)
        (series_dir / 'metadata').mkdir(exist_ok=True)
        (series_dir / 'images').mkdir(exist_ok=True)
        (series_dir / 'prompts').mkdir(exist_ok=True)
        
        # Create README
        readme = series_dir / 'README.md'
        with open(readme, 'w') as f:
            f.write(f"# {series_name.replace('_', ' ')}\n\n")
            f.write(f"**Songs:** {len(songs)}\n")
            f.write(f"**Artist:** AvaTar ArTs\n\n")
            f.write("## Tracks\n\n")
            for i, song in enumerate(songs, 1):
                f.write(f"{i}. {song.get('Title', 'Unknown')}\n")
        
        # Copy files - Format: Artist - Song Title.mp3 (NO track numbers!)
        for song in songs:
            filepath = song.get('Filepath', '')
            
            if not filepath or not Path(filepath).exists():
                print(f"  ??  Not found: {song.get('Title')}")
                continue
            
            src = Path(filepath)
            artist = song.get('Artist', 'AvaTar ArTs')
            title = song.get('Title', src.stem)
            
            # Format: Artist - Song Title.mp3
            new_filename = f"{artist} - {title}.mp3"
            dst = files_dir / new_filename
            
            # Handle conflicts
            if dst.exists():
                counter = 2
                while dst.exists():
                    new_filename = f"{artist} - {title} ({counter}).mp3"
                    dst = files_dir / new_filename
                    counter += 1
            
            try:
                shutil.copy2(src, dst)
                print(f"  ? {new_filename}")
            except Exception as e:
                print(f"  ? Failed: {title}")
        
        print()
    
    # Summary
    print("=" * 80)
    print("  ? SERIES VOLUMES POPULATED")
    print("=" * 80 + "\n")
    
    print("Created structure matching And_Also_Special_Guest:")
    print()
    for series_name, songs in series_songs.items():
        if songs:
            print(f"? {series_name}/")
            print(f"  ??? files/     ({len(songs)} songs)")
            print(f"  ??? metadata/")
            print(f"  ??? images/")
            print(f"  ??? prompts/")
            print(f"  ??? README.md")
            print()
    
    print(f"All in: {nocturne_dir}")
    print()
    print("Filename format: Artist - Song Title.mp3")
    print("(NO track numbers, matching your And_Also_Special_Guest format)")
    print()
    print(f"Open: open '{nocturne_dir}'")

if __name__ == '__main__':
    main()
