#!/usr/bin/env python3
"""
Integrate User Updates
Merge user's edits from Downloads CSV back into unified catalog
"""

import csv
from pathlib import Path

def normalize_path(path: str) -> str:
    """Normalize path for matching"""
    if not path:
        return ""
    return str(Path(path).resolve())

def main():
    print("\n" + "??" * 40)
    print("  INTEGRATING USER UPDATES")
    print("  Merging your edits back into unified catalog")
    print("??" * 40 + "\n")
    
    home = Path.home()
    
    # User's edited file
    user_updates = home / 'Downloads/ENHANCED_MP3_CATALOG - ENHANCED_MP3_CATALOG.csv'
    
    # Our unified catalog
    unified_catalog = home / 'Music/UNIFIED_MASTER_CATALOG.csv'
    
    if not user_updates.exists():
        print(f"? User updates file not found: {user_updates}")
        return
    
    if not unified_catalog.exists():
        print(f"? Unified catalog not found: {unified_catalog}")
        return
    
    print("Loading your updates...\n")
    
    # Load user updates
    user_data = {}
    user_columns = []
    
    with open(user_updates, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        user_columns = reader.fieldnames
        for row in reader:
            filepath = normalize_path(row.get('filepath') or row.get('current_path') or '')
            if filepath:
                user_data[filepath] = row
    
    print(f"? Loaded {len(user_data)} entries from your updates")
    print(f"  Columns: {', '.join(user_columns[:10])}...")
    print()
    
    # Load unified catalog
    print("Loading unified catalog...\n")
    
    unified_data = []
    unified_columns = []
    
    with open(unified_catalog, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        unified_columns = reader.fieldnames
        unified_data = list(reader)
    
    print(f"? Loaded {len(unified_data)} entries from unified catalog\n")
    
    # Merge user updates
    print("Merging your updates...\n")
    
    updates_applied = 0
    new_entries = 0
    
    # Update existing entries
    for entry in unified_data:
        filepath = normalize_path(entry.get('filepath', ''))
        
        if filepath in user_data:
            user_row = user_data[filepath]
            
            # Update fields that user may have changed
            important_fields = [
                'should_transcribe', 'transcribed', 'notes',
                'title', 'artist', 'album', 'genre',
                'content_type', 'is_music'
            ]
            
            for field in important_fields:
                if field in user_row and user_row[field]:
                    # User's value takes precedence
                    if field == 'is_music':
                        # Map is_music to is_your_music
                        entry['is_your_music'] = 'YES' if user_row[field] == 'True' else 'NO'
                    else:
                        entry[field] = user_row[field]
                    updates_applied += 1
    
    # Add new entries from user file
    for filepath, user_row in user_data.items():
        # Check if this file is in unified catalog
        if not any(normalize_path(e.get('filepath', '')) == filepath for e in unified_data):
            # New entry - add it
            new_entry = {col: '' for col in unified_columns}
            
            # Fill from user data
            new_entry['filepath'] = user_row.get('filepath') or user_row.get('current_path') or ''
            new_entry['filename'] = user_row.get('filename') or user_row.get('current_filename') or ''
            new_entry['title'] = user_row.get('title') or ''
            new_entry['artist'] = user_row.get('artist') or ''
            new_entry['album'] = user_row.get('album') or ''
            new_entry['genre'] = user_row.get('genre') or ''
            new_entry['duration_seconds'] = user_row.get('duration_seconds') or user_row.get('duration') or ''
            new_entry['file_size_mb'] = user_row.get('file_size_mb') or ''
            new_entry['content_type'] = user_row.get('content_type') or ''
            new_entry['is_your_music'] = 'YES' if user_row.get('is_music') == 'True' else 'NO'
            new_entry['should_transcribe'] = user_row.get('should_transcribe') or 'REVIEW'
            new_entry['transcribed'] = user_row.get('transcribed') or 'NO'
            new_entry['notes'] = user_row.get('notes') or ''
            new_entry['in_existing_catalog'] = 'YES'
            new_entry['in_new_analysis'] = 'NO'
            new_entry['in_deep_scan'] = 'NO'
            
            unified_data.append(new_entry)
            new_entries += 1
    
    # Save updated unified catalog
    output = home / 'Music/UNIFIED_MASTER_CATALOG.csv'
    backup = home / 'Music/UNIFIED_MASTER_CATALOG_BACKUP.csv'
    
    # Backup original
    if output.exists():
        import shutil
        shutil.copy2(output, backup)
        print(f"? Backed up original to: {backup}\n")
    
    print("Saving updated unified catalog...\n")
    
    with open(output, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=unified_columns)
        writer.writeheader()
        writer.writerows(unified_data)
    
    print(f"? Saved to: {output}\n")
    
    # Summary
    print("=" * 80)
    print("  ? USER UPDATES INTEGRATED")
    print("=" * 80 + "\n")
    
    print(f"Total entries: {len(unified_data)}")
    print(f"Updates applied: {updates_applied} field changes")
    print(f"New entries added: {new_entries}")
    print()
    
    print("Your edits have been merged into the unified catalog!")
    print()
    print(f"Open updated catalog: open '{output}'")

if __name__ == '__main__':
    main()
