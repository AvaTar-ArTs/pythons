#!/usr/bin/env python3
"""
Fix Bundle Folder Names
Clean up inconsistent naming in song bundles
"""

from pathlib import Path
import re

def title_case_smart(text: str) -> str:
    """Smart title case that preserves certain patterns"""
    # Words that should stay lowercase (unless first word)
    lowercase_words = {'a', 'an', 'the', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'by', 'from', 'with'}
    
    # Split by spaces
    words = text.split()
    
    result = []
    for i, word in enumerate(words):
        # Keep special patterns
        if word in ['LIVE', 'CuT', 'og', 'v4', 'v3', 'MP3', 'MP4']:
            result.append(word)
        # First word or not in lowercase list
        elif i == 0 or word.lower() not in lowercase_words:
            result.append(word.capitalize())
        else:
            result.append(word.lower())
    
    return ' '.join(result)

def clean_song_title(title: str) -> str:
    """Clean up song title"""
    # Fix common issues
    title = title.strip()
    
    # Fix weird capitalization patterns
    title = re.sub(r'aLLey', 'Alley', title)
    title = re.sub(r'([a-z])([A-Z])', r'\1 \2', title)  # Fix camelCase
    
    # Fix specific patterns
    replacements = {
        'PeTals FaLL': 'Petals Fall',
        'in This aLLey Where i HiDe': 'In This Alley Where I Hide',
        'in the Alley where Hope Flies': 'In the Alley Where Hope Flies',
        'in_this_alley_where_i_Hide LIVE_-_CuT-og': 'In This Alley Where I Hide (Live Cut Original)',
        'Junkyard symphony from hearts': 'Junkyard Symphony From Hearts',
        'WorkShop Worries': 'Workshop Worries',
        'DescriptiveOrigins': 'Descriptive Origins',
    }
    
    for old, new in replacements.items():
        if old in title:
            title = title.replace(old, new)
    
    return title

def determine_artist(folder_name: str, song_title: str) -> str:
    """Determine the correct artist"""
    
    # Check if it's clearly the user's music
    user_indicators = [
        'remastered', 'blues', 'heartbeats', 'alley', 'junkyard', 
        'kings and queens', 'petals', 'serenade', 'workshop', 'echoes',
        'circles', 'descriptive'
    ]
    
    song_lower = song_title.lower()
    
    # If clearly user's music
    if any(indicator in song_lower for indicator in user_indicators):
        return 'AvaTar ArTs'
    
    # If it's a UUID or number
    if re.match(r'^[a-f0-9-]{36}$|^\d+$', song_title):
        return 'AvaTar ArTs'
    
    # Default to AvaTar ArTs for "Unknown"
    if 'unknown' in folder_name.lower():
        return 'AvaTar ArTs'
    
    return 'AvaTar ArTs'

def get_new_folder_name(old_name: str) -> str:
    """Generate new clean folder name"""
    
    # Remove special characters that shouldn't be in folder names
    if old_name == '_BUNDLES_INDEX.txt':
        return old_name
    
    # Parse current name
    if ' - ' in old_name:
        parts = old_name.split(' - ', 1)
        artist = parts[0].strip()
        song_title = parts[1].strip()
    else:
        artist = ''
        song_title = old_name.strip()
    
    # Fix missing or wrong artist
    if not artist or artist == '' or artist == 'Unknown':
        artist = determine_artist(old_name, song_title)
    
    # Clean up song title
    song_title = clean_song_title(song_title)
    
    # Build new name
    new_name = f"{artist} - {song_title}"
    
    return new_name

def main():
    print("\n" + "??" * 40)
    print("  FIX BUNDLE FOLDER NAMES")
    print("  Clean up inconsistent naming")
    print("??" * 40 + "\n")
    
    bundles_root = Path.home() / 'Music/nocTurneMeLoDieS/SONG_BUNDLES'
    
    if not bundles_root.exists():
        print("? SONG_BUNDLES directory not found")
        return
    
    # Find all folders that need renaming
    renames = []
    
    for item in sorted(bundles_root.iterdir()):
        if item.name.startswith('.'):
            continue
        
        old_name = item.name
        new_name = get_new_folder_name(old_name)
        
        if old_name != new_name:
            renames.append({
                'old': item,
                'old_name': old_name,
                'new_name': new_name,
                'new_path': bundles_root / new_name
            })
    
    if not renames:
        print("? All bundle names are already clean!\n")
        return
    
    print(f"Found {len(renames)} folders to rename\n")
    
    print("=" * 80)
    print("  PROPOSED RENAMES")
    print("=" * 80 + "\n")
    
    for i, rename in enumerate(renames, 1):
        print(f"{i}. OLD: {rename['old_name']}")
        print(f"   NEW: {rename['new_name']}")
        print()
    
    print("=" * 80)
    print("  APPLYING RENAMES")
    print("=" * 80 + "\n")
    
    success = 0
    failed = 0
    
    for rename in renames:
        try:
            # Check if target already exists
            if rename['new_path'].exists():
                print(f"??  Skipping {rename['old_name']}")
                print(f"   Target already exists: {rename['new_name']}")
                failed += 1
            else:
                rename['old'].rename(rename['new_path'])
                print(f"? {rename['old_name']}")
                print(f"  ? {rename['new_name']}")
                success += 1
        except Exception as e:
            print(f"? Failed: {rename['old_name']}")
            print(f"  Error: {e}")
            failed += 1
        print()
    
    print("=" * 80)
    print("  ? BUNDLE RENAMING COMPLETE")
    print("=" * 80 + "\n")
    
    print(f"Successfully renamed: {success}")
    print(f"Failed/Skipped: {failed}")
    print()
    
    print(f"All bundles: open '{bundles_root}'")

if __name__ == '__main__':
    main()
