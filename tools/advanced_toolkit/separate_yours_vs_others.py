#!/usr/bin/env python3
"""
Separate YOUR Music vs Others' Music
- YOUR music: Goes in themed series volumes (Bite, Feather, Blues, etc.)
- OTHERS' music: Goes in And_Also_Special_Guest/ with "Artist - Song.mp3" format
"""

import csv
from pathlib import Path
import shutil

def main():
    print("\n" + "??" * 40)
    print("  SEPARATE YOUR MUSIC VS OTHERS")
    print("  Different structure for each")
    print("??" * 40 + "\n")
    
    home = Path.home()
    nocturne_dir = home / 'Music/nocTurneMeLoDieS'
    unified_catalog = nocturne_dir / 'DATA/UNIFIED_MASTER_CATALOG.csv'
    
    if not unified_catalog.exists():
        print(f"? Unified catalog not found")
        return
    
    # Load all songs
    print("Loading catalog...\n")
    
    all_songs = []
    with open(unified_catalog, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        all_songs = list(reader)
    
    print(f"? Loaded {len(all_songs)} total files\n")
    
    # Separate
    print("Separating YOUR music vs OTHERS...\n")
    
    your_songs = []
    others_songs = []
    
    for song in all_songs:
        # Only process SONG type (skip clips, audiobooks, etc.)
        if song.get('content_type') != 'SONG':
            continue
        
        if song.get('is_your_music') in ['YES', 'True', 'TRUE']:
            your_songs.append(song)
        else:
            others_songs.append(song)
    
    print(f"? YOUR music (AvaTar ArTs): {len(your_songs)} songs")
    print(f"? OTHERS' music (guest artists): {len(others_songs)} songs\n")
    
    # Show breakdown
    print("=" * 80)
    print("  ?? ORGANIZATION PLAN")
    print("=" * 80 + "\n")
    
    print("YOUR MUSIC ? Themed Series Volumes:")
    print("  ? Bite_in_the_Night_Vol_1/")
    print("  ? Feather_Fang_Vol_1/")
    print("  ? Blues_in_the_Alley_Vol_3/")
    print("  ? Petals_Fall_Vol_1/")
    print("  ? etc.")
    print("  Format: Just song title.mp3 or numbered")
    print()
    
    print("OTHERS' MUSIC ? And_Also_Special_Guest/:")
    print("  Format: Artist - Song Title.mp3")
    print("  Structure: files/, metadata/, images/, prompts/, README.md")
    print()
    
    # Create And_Also_Special_Guest structure
    print("=" * 80)
    print("  CREATING GUEST ARTISTS FOLDER")
    print("=" * 80 + "\n")
    
    guest_dir = nocturne_dir / 'And_Also_Special_Guest'
    guest_dir.mkdir(exist_ok=True)
    
    files_dir = guest_dir / 'files'
    files_dir.mkdir(exist_ok=True)
    (guest_dir / 'metadata').mkdir(exist_ok=True)
    (guest_dir / 'images').mkdir(exist_ok=True)
    (guest_dir / 'prompts').mkdir(exist_ok=True)
    
    print(f"? Created: And_Also_Special_Guest/\n")
    
    # Create README
    readme = guest_dir / 'README.md'
    with open(readme, 'w') as f:
        f.write("# And Also Special Guest\n\n")
        f.write("**Music by guest artists and other musicians**\n\n")
        f.write(f"**Total Songs:** {len(others_songs)}\n\n")
        f.write("Format: `Artist - Song Title.mp3`\n\n")
    
    # Copy OTHERS' music (sample first 20)
    print("Copying guest artists' music (sample)...\n")
    
    copied = 0
    
    for song in others_songs[:20]:  # Sample first 20
        filepath = song.get('filepath') or song.get('current_path') or ''
        
        if not filepath or not Path(filepath).exists():
            continue
        
        src = Path(filepath)
        artist = song.get('artist', 'Unknown Artist')
        title = song.get('title', src.stem)
        
        # Format: Artist - Song Title.mp3
        new_filename = f"{artist} - {title}.mp3"
        dst = files_dir / new_filename
        
        if dst.exists():
            continue
        
        try:
            shutil.copy2(src, dst)
            print(f"  ? {new_filename}")
            copied += 1
        except Exception:
            pass
    
    print(f"\n? Copied {copied} guest artists' songs (sample)\n")
    
    # Summary
    print("=" * 80)
    print("  ? STRUCTURE CLARIFIED")
    print("=" * 80 + "\n")
    
    print("YOUR MUSIC (AvaTar ArTs):")
    print(f"  ? {len(your_songs)} songs")
    print("  ? Goes in: Bite_in_the_Night_Vol_1/, Blues_Vol_3/, etc.")
    print("  ? Format: Song title (NO artist prefix)")
    print()
    
    print("OTHERS' MUSIC (Guest Artists):")
    print(f"  ? {len(others_songs)} songs")
    print("  ? Goes in: And_Also_Special_Guest/")
    print("  ? Format: Artist - Song Title.mp3")
    print(f"  ? Sample copied: {copied} songs")
    print()
    
    print(f"Check: open '{guest_dir}'")

if __name__ == '__main__':
    main()
