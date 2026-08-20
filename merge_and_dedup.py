#!/usr/bin/env python3
"""Merge Discography0g into DISCO, deduplicate album folders and files."""

import os
import shutil
from pathlib import Path

DISCO = Path("/Users/steven/Music/nocturneMelodies/DISCO")
DISCOG = Path("/Users/steven/Music/nocturneMelodies/Discography0g")

print("=== nocturneMelodies — Merge & Dedup ===\n")
print(f"DISCO:     {sum(1 for _ in DISCO.rglob('*') if _.is_file())} files")
print(f"Discog0g:  {sum(1 for _ in DISCOG.rglob('*') if _.is_file())} files\n")

# Move unique album folders from Discography0g → DISCO
moved = 0
skipped = 0
files_merged = 0
files_skipped = 0

for album_dir in sorted(DISCOG.iterdir()):
    if not album_dir.is_dir():
        continue

    album_name = album_dir.name
    target = DISCO / album_name

    if target.exists():
        # Album exists in both — merge individual files
        for f in album_dir.rglob('*'):
            if f.is_file():
                rel = f.relative_to(album_dir)
                dest = target / rel
                if not dest.exists():
                    dest.parent.mkdir(parents=True, exist_ok=True)
                    shutil.copy2(f, dest)
                    files_merged += 1
                else:
                    files_skipped += 1
        skipped += 1
    else:
        # Unique album — move entire folder
        shutil.move(str(album_dir), str(target))
        moved += 1

print(f"✅ Moved {moved} unique album folders to DISCO")
print(f"📋 Merged {files_merged} files into existing albums")
print(f"⏭️  Skipped {files_skipped} duplicate files (already exist)")
print(f"📦 Skipped {skipped} albums (already in DISCO, merged files)")

# Clean up empty Discography0g
remaining = list(DISCOG.iterdir())
if remaining:
    print(f"\n⚠️  Discography0g still has {len(remaining)} items (non-album files)")
else:
    print(f"\n✅ Discography0g is now empty")

# Final stats
total_files = sum(1 for _ in DISCO.rglob('*') if _.is_file())
total_albums = sum(1 for _ in DISCO.iterdir() if _.is_dir())
print(f"\n=== DISCO FINAL STATE ===")
print(f"  Albums: {total_albums}")
print(f"  Files:  {total_files}")
print(f"  MP3s:   {sum(1 for _ in DISCO.rglob('*.mp3'))}")
print(f"  Covers: {sum(1 for _ in DISCO.rglob('*.jp*'))}")
print(f"  Text:   {sum(1 for _ in DISCO.rglob('*.txt'))}")
