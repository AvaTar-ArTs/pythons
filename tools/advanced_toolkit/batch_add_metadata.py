#!/usr/bin/env python3
"""
Batch add metadata to audio files
Uses data from master CSV to populate missing tags
"""

import csv
from pathlib import Path
import subprocess
import shutil

def add_metadata_to_file(filepath: str, metadata: dict, dry_run: bool = True) -> bool:
    """Add metadata to audio file using ffmpeg"""
    
    if not Path(filepath).exists():
        return False
    
    # Build metadata arguments
    meta_args = []
    
    if metadata.get('title'):
        meta_args.extend(['-metadata', f"title={metadata['title']}"])
    if metadata.get('artist'):
        meta_args.extend(['-metadata', f"artist={metadata['artist']}"])
    if metadata.get('album'):
        meta_args.extend(['-metadata', f"album={metadata['album']}"])
    if metadata.get('genre'):
        meta_args.extend(['-metadata', f"genre={metadata['genre']}"])
    if metadata.get('comment'):
        meta_args.extend(['-metadata', f"comment={metadata['comment']}"])
    if metadata.get('date'):
        meta_args.extend(['-metadata', f"date={metadata['date']}"])
    
    if not meta_args:
        return False
    
    if dry_run:
        print(f"  Would add to: {Path(filepath).name}")
        for i in range(0, len(meta_args), 2):
            print(f"    {meta_args[i+1]}")
        return True
    
    # Create temp file
    temp_file = str(Path(filepath).with_suffix('.tmp' + Path(filepath).suffix))
    
    try:
        # Run ffmpeg
        cmd = [
            'ffmpeg', '-i', filepath,
            *meta_args,
            '-codec', 'copy',  # Don't re-encode, just copy
            '-y',  # Overwrite
            temp_file
        ]
        
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=30
        )
        
        if result.returncode == 0:
            # Replace original with temp
            shutil.move(temp_file, filepath)
            return True
        else:
            # Clean up temp file
            if Path(temp_file).exists():
                Path(temp_file).unlink()
            return False
    except Exception as e:
        # Clean up temp file
        if Path(temp_file).exists():
            Path(temp_file).unlink()
        return False

def main():
    print("\n" + "??" * 40)
    print("  BATCH METADATA UPDATER")
    print("  Add metadata to files from master CSV")
    print("??" * 40 + "\n")
    
    home = Path.home()
    
    # Load TASK2 results (files that need metadata)
    task2_csv = home / 'Music/TASK2_METADATA_EXTRACTION.csv'
    master_csv = home / 'Music/MASTER_COMPLETE_ALL_FIELDS.csv'
    
    if not task2_csv.exists():
        print("? TASK2_METADATA_EXTRACTION.csv not found")
        print("Run process_all_three_tasks.py first")
        return
    
    # Load files needing metadata
    print("Loading files that need metadata...\n")
    
    need_metadata = []
    with open(task2_csv, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row.get('Priority') in ['HIGH', 'MEDIUM']:
                need_metadata.append(row)
    
    print(f"Found {len(need_metadata)} files needing metadata\n")
    
    # Load master CSV for source data
    print("Loading master CSV for metadata source...\n")
    
    master_data = {}
    with open(master_csv, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            title = row.get('Title', '').lower().strip()
            if title:
                master_data[title] = row
    
    print(f"Loaded {len(master_data)} entries from master CSV\n")
    
    # Match and prepare updates
    print("Preparing metadata updates...\n")
    
    updates = []
    
    for item in need_metadata:
        title = item.get('Title', '').lower().strip()
        filepath = item.get('Filepath', '')
        
        if not filepath:
            continue
        
        # Find in master
        master_entry = master_data.get(title)
        
        if master_entry:
            metadata = {
                'title': master_entry.get('Title', ''),
                'artist': master_entry.get('Artist', ''),
                'genre': master_entry.get('Genre', '') or master_entry.get('Style', ''),
                'comment': master_entry.get('Mood', '') or master_entry.get('Description', ''),
                'album': 'Suno Creations',  # Default album
            }
            
            # Only include if we have something to add
            if any(metadata.values()):
                updates.append({
                    'filepath': filepath,
                    'filename': item.get('Filename', ''),
                    'metadata': metadata,
                    'missing': item.get('Missing_Fields', ''),
                    'priority': item.get('Priority', '')
                })
    
    print(f"Prepared {len(updates)} updates\n")
    
    # Show sample
    print("=" * 80)
    print("  SAMPLE UPDATES (First 10)")
    print("=" * 80 + "\n")
    
    for i, update in enumerate(updates[:10]):
        print(f"{i+1}. {update['filename']}")
        print(f"   Missing: {update['missing']}")
        print(f"   Will add:")
        for key, value in update['metadata'].items():
            if value:
                print(f"     {key}: {value}")
        print()
    
    if len(updates) > 10:
        print(f"... and {len(updates) - 10} more\n")
    
    # Ask user
    print("=" * 80)
    print("  DRY RUN MODE")
    print("=" * 80 + "\n")
    
    print("This is a DRY RUN - no files will be modified.\n")
    print("To apply updates, edit this script and set dry_run=False\n")
    
    # Dry run
    success = 0
    for update in updates[:20]:  # Sample first 20
        if add_metadata_to_file(update['filepath'], update['metadata'], dry_run=True):
            success += 1
    
    print(f"\n? Would update {success} files successfully\n")
    
    # Save update plan
    output = home / 'Music/METADATA_UPDATE_PLAN.csv'
    
    with open(output, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow([
            'Filename', 'Filepath', 'Priority',
            'Missing_Fields',
            'Will_Add_Title', 'Will_Add_Artist', 'Will_Add_Genre',
            'Will_Add_Album', 'Will_Add_Comment'
        ])
        
        for update in updates:
            meta = update['metadata']
            writer.writerow([
                update['filename'],
                update['filepath'],
                update['priority'],
                update['missing'],
                meta.get('title', ''),
                meta.get('artist', ''),
                meta.get('genre', ''),
                meta.get('album', ''),
                meta.get('comment', ''),
            ])
    
    print(f"? Saved update plan to: {output}\n")
    
    print("=" * 80)
    print("  SUMMARY")
    print("=" * 80 + "\n")
    
    print(f"Files ready for metadata update: {len(updates)}")
    print(f"Update plan saved to: {output}")
    print()
    print("To actually apply the metadata:")
    print("  1. Review METADATA_UPDATE_PLAN.csv")
    print("  2. Edit batch_add_metadata.py and set dry_run=False")
    print("  3. Run again to apply changes")
    print()
    print(f"Open plan: open '{output}'")

if __name__ == '__main__':
    main()
