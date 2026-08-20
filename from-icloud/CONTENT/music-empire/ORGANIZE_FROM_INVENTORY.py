#!/usr/bin/env python3
"""
Organize 13,007 files using inventory
"""

import csv
import shutil
from pathlib import Path

workspace = Path.home() / 'workspace' / 'music-empire'
target = Path.home() / 'Music' / 'nocTurneMeLoDieS' / 'FINAL_ORGANIZED'

# Create structure
suno_dir = target / 'YOUR_SUNO_SONGS'
other_dir = target / 'OTHER_MUSIC'
suno_dir.mkdir(parents=True, exist_ok=True)
other_dir.mkdir(parents=True, exist_ok=True)

print("🧹 ORGANIZING FROM INVENTORY")
print("=" * 70)

# Load inventory
inventory_file = workspace / 'COMPLETE_FILE_INVENTORY.csv'

stats = {'suno': 0, 'other': 0, 'dupes': 0, 'errors': 0}
seen_hashes = set()

with open(inventory_file, 'r') as f:
    reader = csv.DictReader(f)
    files = list(reader)
    total = len(files)
    
    print(f"\n📊 Processing {total} files in batches...\n")
    
    for i, row in enumerate(files):
        try:
            source = Path(row['path'])
            
            if not source.exists():
                continue
            
            # Skip duplicates
            file_hash = row['hash']
            if file_hash in seen_hashes:
                stats['dupes'] += 1
                continue
            seen_hashes.add(file_hash)
            
            # Determine category
            in_catalog = row['in_catalog'] == 'YES'
            filename_lower = source.name.lower()
            
            is_suno = in_catalog or any(word in filename_lower for word in 
                                       ['suno', 'nocturne', 'avatararts', 'moonlit', 'junk'])
            
            if is_suno:
                dest_dir = suno_dir
                stats['suno'] += 1
            else:
                dest_dir = other_dir
                stats['other'] += 1
            
            # Copy
            dest = dest_dir / source.name
            counter = 1
            while dest.exists():
                dest = dest_dir / f"{source.stem}_{counter}{source.suffix}"
                counter += 1
            
            shutil.copy2(source, dest)
            
            if (i + 1) % 100 == 0:
                print(f"   [{i+1}/{total}] Suno: {stats['suno']} | Other: {stats['other']} | Dupes: {stats['dupes']}")
        
        except Exception as e:
            stats['errors'] += 1

print(f"\n{'=' * 70}")
print("🎊 DONE!")
print("=" * 70)
print(f"\n✅ Your Suno songs: {stats['suno']}")
print(f"📦 Other music: {stats['other']}")
print(f"🔄 Duplicates skipped: {stats['dupes']}")
print(f"❌ Errors: {stats['errors']}")
print(f"\n📁 Organized at: {target}")
