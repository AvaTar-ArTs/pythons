#!/usr/bin/env python3
"""
Add Downloads Content to Song Bundles
Copy matched content from Downloads into existing song bundles
"""

import csv
from pathlib import Path
import shutil

def copy_file_safely(src: Path, dst: Path) -> bool:
    """Copy file with conflict handling"""
    try:
        if not src.exists():
            return False
        
        # If destination exists, add number
        if dst.exists():
            stem = dst.stem
            suffix = dst.suffix
            counter = 1
            while dst.exists():
                dst = dst.parent / f"{stem}_{counter}{suffix}"
                counter += 1
        
        shutil.copy2(src, dst)
        return True
    except Exception as e:
        return False

def main():
    print("\n" + "??" * 40)
    print("  ADD DOWNLOADS CONTENT TO SONG BUNDLES")
    print("  Consolidate Downloads matches into bundles")
    print("??" * 40 + "\n")
    
    home = Path.home()
    bundles_root = home / 'Music/nocTurneMeLoDieS/SONG_BUNDLES'
    matched_csv = home / 'Music/DOWNLOADS_MATCHED_CONTENT.csv'
    
    if not matched_csv.exists():
        print("? DOWNLOADS_MATCHED_CONTENT.csv not found")
        print("Run scan_downloads_for_content.py first")
        return
    
    if not bundles_root.exists():
        print("? SONG_BUNDLES directory not found")
        print("Run consolidate_song_bundles.py first")
        return
    
    # Load matched content
    print("Loading matched Downloads content...\n")
    
    matched_items = []
    with open(matched_csv, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        matched_items = list(reader)
    
    print(f"? Found {len(matched_items)} matched items\n")
    
    # Group by song
    by_song = {}
    for item in matched_items:
        song_title = item.get('Song_Title', '')
        if song_title not in by_song:
            by_song[song_title] = []
        by_song[song_title].append(item)
    
    print(f"? Content for {len(by_song)} songs\n")
    
    print("=" * 80)
    print("  ADDING CONTENT TO BUNDLES")
    print("=" * 80 + "\n")
    
    results = {
        'updated': 0,
        'created': 0,
        'files_added': 0,
        'skipped': 0
    }
    
    for song_title, items in sorted(by_song.items()):
        print(f"{song_title}")
        
        # Find or create bundle folder
        # Try to find existing bundle
        bundle_path = None
        for bundle_dir in bundles_root.iterdir():
            if bundle_dir.is_dir() and song_title.lower() in bundle_dir.name.lower():
                bundle_path = bundle_dir
                break
        
        # If not found, create new bundle
        if not bundle_path:
            # Sanitize folder name
            folder_name = song_title.replace('/', '_').replace('\\', '_')
            folder_name = folder_name[:100]  # Limit length
            bundle_path = bundles_root / f"Unknown - {folder_name}"
            bundle_path.mkdir(exist_ok=True)
            results['created'] += 1
            print(f"  ? Created new bundle")
        else:
            results['updated'] += 1
        
        # Add files to bundle
        files_added = 0
        
        for item in items:
            content_type = item.get('Content_Type', '')
            filepath = item.get('Filepath', '')
            
            if not filepath or not Path(filepath).exists():
                results['skipped'] += 1
                continue
            
            src = Path(filepath)
            
            # Determine prefix based on content type
            if content_type == 'AUDIO':
                prefix = 'AUDIO'
            elif content_type == 'LYRICS':
                prefix = 'LYRICS'
            elif content_type == 'PROMPT':
                prefix = 'PROMPT'
            elif content_type == 'IMAGE':
                prefix = 'IMAGE'
            else:
                prefix = 'DOC'
            
            dst = bundle_path / f"{prefix} - {src.name}"
            
            if copy_file_safely(src, dst):
                files_added += 1
                results['files_added'] += 1
        
        if files_added > 0:
            print(f"  ? Added {files_added} files")
        
        print()
    
    # Summary
    print("=" * 80)
    print("  ? DOWNLOADS CONTENT ADDED")
    print("=" * 80 + "\n")
    
    print(f"Bundles updated: {results['updated']}")
    print(f"Bundles created: {results['created']}")
    print(f"Files added: {results['files_added']}")
    print(f"Files skipped: {results['skipped']}")
    print()
    
    print(f"All bundles are in: {bundles_root}\n")
    print(f"Open: open '{bundles_root}'")

if __name__ == '__main__':
    main()
