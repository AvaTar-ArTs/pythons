#!/usr/bin/env python3
"""
Analyze Both Music Folders
Compare ~/Music vs ~/music and suggest unified structure
"""

import csv
from pathlib import Path
from collections import defaultdict

def analyze_folder(base_path: Path) -> dict:
    """Analyze a music folder structure"""
    
    if not base_path.exists():
        return {'exists': False}
    
    result = {
        'exists': True,
        'path': str(base_path),
        'top_level_folders': [],
        'top_level_files': 0,
        'total_mp3s': 0,
        'total_folders': 0,
        'by_album': {}
    }
    
    # Get top-level items
    for item in base_path.iterdir():
        if item.name.startswith('.'):
            continue
        
        if item.is_dir():
            mp3_count = len(list(item.rglob('*.mp3')))
            result['top_level_folders'].append({
                'name': item.name,
                'mp3_count': mp3_count
            })
            result['by_album'][item.name] = mp3_count
        elif item.suffix.lower() == '.mp3':
            result['top_level_files'] += 1
    
    result['total_mp3s'] = len(list(base_path.rglob('*.mp3')))
    result['total_folders'] = len(result['top_level_folders'])
    
    return result

def main():
    print("\n" + "??" * 40)
    print("  ANALYZE BOTH MUSIC FOLDERS")
    print("  ~/Music vs ~/music comparison")
    print("??" * 40 + "\n")
    
    home = Path.home()
    
    # Analyze both locations
    print("Analyzing music folders...\n")
    
    music_upper = analyze_folder(home / 'Music')
    music_lower = analyze_folder(home / 'music')
    music_nocturne = analyze_folder(home / 'Music/nocTurneMeLoDieS')
    
    # Report findings
    print("=" * 80)
    print("  ?? FOLDER COMPARISON")
    print("=" * 80 + "\n")
    
    if music_upper['exists']:
        print("~/Music/")
        print(f"  Total MP3s: {music_upper['total_mp3s']:,}")
        print(f"  Top-level folders: {music_upper['total_folders']}")
        print(f"  Top-level MP3s: {music_upper['top_level_files']}")
        print()
    
    if music_lower['exists']:
        print("~/music/ (lowercase)")
        print(f"  Total MP3s: {music_lower['total_mp3s']:,}")
        print(f"  Top-level folders: {music_lower['total_folders']}")
        print(f"  Top-level MP3s: {music_lower['top_level_files']}")
        print()
    
    if music_nocturne['exists']:
        print("~/Music/nocTurneMeLoDieS/")
        print(f"  Total MP3s: {music_nocturne['total_mp3s']:,}")
        print(f"  Top-level folders: {music_nocturne['total_folders']}")
        print(f"  Top-level MP3s: {music_nocturne['top_level_files']}")
        print()
    
    # Show structure
    print("=" * 80)
    print("  ?? CURRENT STRUCTURE")
    print("=" * 80 + "\n")
    
    if music_nocturne['exists']:
        print("~/Music/nocTurneMeLoDieS/ structure:")
        print("\nLargest albums (top 20):")
        
        sorted_albums = sorted(
            music_nocturne['by_album'].items(),
            key=lambda x: x[1],
            reverse=True
        )[:20]
        
        for name, count in sorted_albums:
            print(f"  ? {name:<50} {count:>4} MP3s")
        
        if len(music_nocturne['by_album']) > 20:
            print(f"\n  ... and {len(music_nocturne['by_album']) - 20} more folders")
    
    print()
    
    if music_lower['exists'] and music_lower['total_folders'] > 0:
        print("~/music/ structure:")
        print("\nAlbums/folders:")
        
        sorted_albums = sorted(
            music_lower['by_album'].items(),
            key=lambda x: x[1],
            reverse=True
        )[:15]
        
        for name, count in sorted_albums:
            print(f"  ? {name:<50} {count:>4} MP3s")
    
    print()
    
    # Suggestions
    print("=" * 80)
    print("  ?? STRUCTURE SUGGESTIONS")
    print("=" * 80 + "\n")
    
    print("Your current setup:")
    print("  ? Organized by artist/album folders")
    print("  ? Volume-based collections (Vol. 1-12)")
    print("  ? Themed series (Blues in the Alley, Junkyard Symphony)")
    print()
    
    print("Recommended structure to match your existing:")
    print()
    print("~/Music/nocTurneMeLoDieS/")
    print("  ??? Steven_Chaplinski_Collection_Vol_[1-12]/   ? Your main collections")
    print("  ??? Blues_in_the_Alley_Vol_[1-2]/              ? Series with volumes")
    print("  ??? Junkyard_Symphony_Vol_[1-3]/               ? Series with volumes")
    print("  ??? Moonlight_Serenade/                        ? Single series")
    print("  ??? Echoes_&_Whispers/                         ? Single series")
    print("  ??? Heroes_Rise/                               ? Single series")
    print("  ??? avatararts/                                ? Container for subprojects")
    print("  ?   ??? files/")
    print("  ?   ??? images/")
    print("  ?   ??? metadata/")
    print("  ?   ??? prompts/")
    print("  ??? SUNO/                                      ? Metadata repository")
    print()
    
    print("Suggested improvements:")
    print("  1. ? Continue volume-based organization (Vol. 1-12)")
    print("  2. ? Group series into volumes when > 20 songs")
    print("  3. ?? Keep avatararts/ as project workspace")
    print("  4. ?? Clean up empty folders")
    print("  5. ?? Move loose MP3s into appropriate volumes")
    print()
    
    # Save detailed report
    output = home / 'Music/BOTH_FOLDERS_ANALYSIS.csv'
    
    with open(output, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['Location', 'Folder_Name', 'MP3_Count', 'Type', 'Recommendation'])
        
        # ~/Music/nocTurneMeLoDieS folders
        if music_nocturne['exists']:
            for name, count in sorted(music_nocturne['by_album'].items(), key=lambda x: -x[1]):
                if 'Collection_Vol' in name:
                    folder_type = 'VOLUME_COLLECTION'
                    rec = 'Keep - good organization'
                elif 'Vol.' in name or 'Vol_' in name:
                    folder_type = 'SERIES_VOLUME'
                    rec = 'Keep - series organization'
                elif count > 10:
                    folder_type = 'LARGE_ALBUM'
                    rec = 'Keep - substantial content'
                elif count > 3:
                    folder_type = 'ALBUM'
                    rec = 'Keep or merge into volume'
                elif count > 0:
                    folder_type = 'SMALL_ALBUM'
                    rec = 'Consider merging into related volume'
                else:
                    folder_type = 'EMPTY'
                    rec = 'Review - may be able to remove'
                
                writer.writerow([
                    'nocTurneMeLoDieS',
                    name,
                    count,
                    folder_type,
                    rec
                ])
        
        # ~/music folders
        if music_lower['exists']:
            for name, count in sorted(music_lower['by_album'].items(), key=lambda x: -x[1]):
                writer.writerow([
                    'music (lowercase)',
                    name,
                    count,
                    'UNKNOWN',
                    'Review and possibly merge'
                ])
    
    print(f"? Detailed analysis saved: {output}\n")
    
    print(f"Open: open '{output}'")

if __name__ == '__main__':
    main()
