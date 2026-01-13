#!/usr/bin/env python3
"""
Analyze Current Music Structure
Understand existing organization and suggest improvements
"""

import csv
from pathlib import Path
from collections import defaultdict

def analyze_directory_structure(base_path: Path) -> dict:
    """Deep analysis of current directory structure"""
    
    analysis = {
        'folders': {},
        'total_mp3s': 0,
        'depth_analysis': defaultdict(int),
        'folder_types': defaultdict(list),
        'empty_folders': [],
        'single_file_folders': []
    }
    
    def scan_recursive(path: Path, depth: int = 0):
        if not path.is_dir():
            return
        
        mp3_count = len(list(path.glob('*.mp3')))
        all_mp3s = len(list(path.rglob('*.mp3')))
        
        folder_info = {
            'path': str(path),
            'name': path.name,
            'depth': depth,
            'mp3s_direct': mp3_count,
            'mp3s_total': all_mp3s,
            'subfolders': [d.name for d in path.iterdir() if d.is_dir()]
        }
        
        analysis['folders'][str(path)] = folder_info
        analysis['total_mp3s'] += mp3_count
        analysis['depth_analysis'][depth] += 1
        
        # Categorize folder
        if all_mp3s == 0:
            analysis['empty_folders'].append(path.name)
        elif all_mp3s == 1:
            analysis['single_file_folders'].append(path.name)
        
        # Determine folder type
        if depth == 1:  # Top-level folders
            if mp3_count > 0:
                analysis['folder_types']['album'].append(path.name)
            elif any(d.is_dir() for d in path.iterdir()):
                analysis['folder_types']['container'].append(path.name)
        
        # Recurse
        for subdir in path.iterdir():
            if subdir.is_dir() and not subdir.name.startswith('.'):
                scan_recursive(subdir, depth + 1)
    
    scan_recursive(base_path)
    
    return analysis

def main():
    print("\n" + "??" * 40)
    print("  ANALYZE CURRENT MUSIC STRUCTURE")
    print("  Understanding your setup")
    print("??" * 40 + "\n")
    
    home = Path.home()
    base_dir = home / 'Music/nocTurneMeLoDieS'
    
    if not base_dir.exists():
        print(f"? Directory not found: {base_dir}")
        return
    
    print(f"Analyzing: {base_dir}\n")
    
    # Analyze structure
    print("Scanning directory structure...\n")
    analysis = analyze_directory_structure(base_dir)
    
    # Report findings
    print("=" * 80)
    print("  CURRENT STRUCTURE ANALYSIS")
    print("=" * 80 + "\n")
    
    # Top-level folders
    top_level = [f for f in base_dir.iterdir() if f.is_dir() and not f.name.startswith('.')]
    
    print(f"Top-level folders: {len(top_level)}\n")
    
    # Categorize
    albums = []
    containers = []
    special = []
    
    for folder in sorted(top_level):
        mp3s_direct = len(list(folder.glob('*.mp3')))
        mp3s_total = len(list(folder.rglob('*.mp3')))
        subfolders = [d for d in folder.iterdir() if d.is_dir()]
        
        info = {
            'name': folder.name,
            'mp3s_direct': mp3s_direct,
            'mp3s_total': mp3s_total,
            'subfolders': len(subfolders)
        }
        
        if mp3s_direct > 0:
            albums.append(info)
        elif subfolders:
            containers.append(info)
        else:
            special.append(info)
    
    # Print structure
    print("ALBUM FOLDERS (have MP3s directly):")
    for album in sorted(albums, key=lambda x: -x['mp3s_total'])[:20]:
        print(f"  ?? {album['name']:<40} {album['mp3s_total']:>4} MP3s")
    
    if len(albums) > 20:
        print(f"  ... and {len(albums) - 20} more\n")
    else:
        print()
    
    print(f"CONTAINER FOLDERS (have subfolders):")
    for container in sorted(containers, key=lambda x: -x['mp3s_total'])[:15]:
        print(f"  ?? {container['name']:<40} {container['mp3s_total']:>4} MP3s  ({container['subfolders']} subfolders)")
    
    if len(containers) > 15:
        print(f"  ... and {len(containers) - 15} more\n")
    else:
        print()
    
    # Statistics
    print("=" * 80)
    print("  STATISTICS")
    print("=" * 80 + "\n")
    
    print(f"Total folders: {len(analysis['folders'])}")
    print(f"Album folders: {len(albums)}")
    print(f"Container folders: {len(containers)}")
    print(f"Empty folders: {len(analysis['empty_folders'])}")
    print(f"Single-file folders: {len(analysis['single_file_folders'])}")
    print()
    
    print(f"Total MP3s found: {sum(f['mp3s_total'] for f in albums + containers)}")
    print()
    
    # Save detailed report
    output = home / 'Music/CURRENT_STRUCTURE_ANALYSIS.csv'
    
    with open(output, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['Folder_Name', 'Type', 'MP3s_Direct', 'MP3s_Total', 'Subfolders', 'Recommendation'])
        
        for album in albums:
            recommendation = 'Keep as-is' if album['mp3s_total'] > 3 else 'Consider merging with related album'
            writer.writerow([
                album['name'],
                'ALBUM',
                album['mp3s_direct'],
                album['mp3s_total'],
                album['subfolders'],
                recommendation
            ])
        
        for container in containers:
            recommendation = 'Review subfolders' if container['subfolders'] > 10 else 'Good organization'
            writer.writerow([
                container['name'],
                'CONTAINER',
                container['mp3s_direct'],
                container['mp3s_total'],
                container['subfolders'],
                recommendation
            ])
    
    print(f"? Detailed analysis saved: {output}\n")
    
    # Suggestions
    print("=" * 80)
    print("  ?? SUGGESTIONS BASED ON YOUR STRUCTURE")
    print("=" * 80 + "\n")
    
    print("Your current structure has:")
    print(f"  ? {len(albums)} album folders")
    print(f"  ? {len(containers)} container folders with subfolders")
    print()
    
    print("Suggestions:")
    print("  1. Keep container folders (like 'avatararts', 'Audio', etc.)")
    print("  2. Keep album folders with 3+ songs")
    print("  3. Merge small albums (1-2 songs) into related series")
    print("  4. Create clear naming: Artist - Album or Series/Album")
    print()
    
    print(f"Open: open '{output}'")

if __name__ == '__main__':
    main()
