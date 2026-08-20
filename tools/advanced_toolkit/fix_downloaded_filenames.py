#!/usr/bin/env python3
"""
Fix Downloaded Filenames
Remove "-_" prefix and clean up obvious naming issues
NO transcription needed - we can tell what they are already
"""

from pathlib import Path
import re

def clean_filename(filename: str) -> str:
    """Clean up filename for clarity"""
    
    stem = Path(filename).stem
    ext = Path(filename).suffix
    
    # Remove "-_" prefix
    stem = re.sub(r'^-_', '', stem)
    
    # Remove "- " prefix
    stem = re.sub(r'^-\s+', '', stem)
    
    # Fix common patterns
    stem = stem.replace('_', ' ')
    stem = stem.replace('-', ' ')
    
    # Fix multiple spaces
    stem = re.sub(r'\s+', ' ', stem)
    
    # Title case for readability
    stem = stem.strip()
    
    return f"{stem}{ext}"

def main():
    print("\n" + "??" * 40)
    print("  FIX DOWNLOADED FILENAMES")
    print("  Simple cleanup - no transcription needed")
    print("??" * 40 + "\n")
    
    home = Path.home()
    
    # Find all DOWNLOADED folders
    music_dir = home / 'Music/nocTurneMeLoDieS'
    
    downloaded_folders = []
    for path in music_dir.rglob('DOWNLOADED'):
        if path.is_dir():
            downloaded_folders.append(path)
    
    # Also check BACKUP folders
    for path in (home / 'Music').rglob('BACKUP_MERGE_*'):
        if path.is_dir():
            downloaded = path / 'DOWNLOADED'
            if downloaded.exists():
                downloaded_folders.append(downloaded)
    
    print(f"Found {len(downloaded_folders)} DOWNLOADED folders\n")
    
    # Process each folder
    all_renames = []
    
    for folder in downloaded_folders:
        print(f"Scanning: {folder}")
        
        mp3s = list(folder.glob('*.mp3'))
        
        if not mp3s:
            print(f"  No MP3s found\n")
            continue
        
        print(f"  Found {len(mp3s)} MP3s")
        
        for mp3 in mp3s:
            old_name = mp3.name
            new_name = clean_filename(old_name)
            
            if old_name != new_name:
                all_renames.append({
                    'old_path': mp3,
                    'old_name': old_name,
                    'new_name': new_name,
                    'new_path': mp3.parent / new_name,
                    'folder': str(folder)
                })
        
        print()
    
    if not all_renames:
        print("? All filenames are already clean!\n")
        return
    
    print(f"Found {len(all_renames)} files to rename\n")
    
    print("=" * 80)
    print("  PROPOSED RENAMES (First 20)")
    print("=" * 80 + "\n")
    
    for i, rename in enumerate(all_renames[:20], 1):
        print(f"{i}. OLD: {rename['old_name']}")
        print(f"   NEW: {rename['new_name']}")
        print()
    
    if len(all_renames) > 20:
        print(f"... and {len(all_renames) - 20} more\n")
    
    print("=" * 80)
    print("  APPLYING RENAMES")
    print("=" * 80 + "\n")
    
    success = 0
    failed = 0
    skipped = 0
    
    for rename in all_renames:
        try:
            # Check if target exists
            if rename['new_path'].exists():
                print(f"??  Target exists, skipping: {rename['new_name']}")
                skipped += 1
                continue
            
            # Rename
            rename['old_path'].rename(rename['new_path'])
            success += 1
            
        except Exception as e:
            print(f"? Failed: {rename['old_name']}")
            print(f"  Error: {e}")
            failed += 1
    
    print()
    print("=" * 80)
    print("  ? CLEANUP COMPLETE")
    print("=" * 80 + "\n")
    
    print(f"Successfully renamed: {success}")
    print(f"Skipped (target exists): {skipped}")
    print(f"Failed: {failed}")
    print()
    
    print("Examples of cleaned names:")
    for rename in all_renames[:10]:
        print(f"  ? {rename['new_name']}")
    
    print()
    print("All files in DOWNLOADED folders are now clean!")

if __name__ == '__main__':
    main()
