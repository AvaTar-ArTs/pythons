#!/usr/bin/env python3
"""from pathlib import Path
import re
import shutil

from mutagen.easyid3 import EasyID3
from mutagen.mp3 import MP3
Clean all filenames: Title_artist.mp3
No "01 - Artist - Title" format
No spaces, use underscores
Artist in metadata only
"""

NOCTURNE = Path("/Users/steven/Music/nocTurneMeLoDieS")


def clean_name(text):
    """Clean text for filename: lowercase, no spaces, alphanumeric"""
    if not text:
        return "unknown"
    # Remove special chars, keep alphanumeric and spaces
    text = re.sub(r"[^\w\s-]", "", text)
    # Replace spaces/dashes with underscores
    text = re.sub(r"[-\s]+", "_", text)
    # Lowercase
    text = text.lower().strip("_")
    return text or "unknown"


print("=" * 80)
print("?? CLEANING ALL FILENAMES")
print("=" * 80)
print()
print("Format: Title_artist.mp3")
print("  ? No track numbers")
print("  ? No spaces")
print("  ? Lowercase artist")
print("  ? Artist in metadata only")
print()

# Find all loose MP3s (not in album folders)
loose_mp3s = []
for mp3_file in NOCTURNE.glob("*.mp3"):
    if mp3_file.is_file():
        loose_mp3s.append(mp3_file)

print(f"Found {len(loose_mp3s)} loose MP3 files")
print()

# Analyze and create rename plan
renames = []
skipped = []

print("Analyzing files...")
for mp3_file in loose_mp3s:
    # Read metadata
    try:
        audio = MP3(mp3_file, ID3=EasyID3)
        title = audio.get("title", [None])[0]
        artist = audio.get("artist", [None])[0]
    except:
        title = None
        artist = None

    # If no metadata, try to extract from filename
    if not title:
        # Remove "01 - Artist - " prefix pattern
        name = mp3_file.stem
        # Match pattern: "01 - Artist - Title"
        match = re.match(r"^\d+\s*-\s*(.+?)\s*-\s*(.+)$", name)
        if match:
            artist_from_name = match.group(1)
            title = match.group(2)
            if not artist:
                artist = artist_from_name
        else:
            # Use filename as title
            title = name

    # Create clean filename
    if title:
        title_clean = clean_name(title)
        artist_clean = clean_name(artist) if artist else "unknown"

        new_name = f"{title_clean}_{artist_clean}.mp3"

        # Avoid duplicates
        target = NOCTURNE / new_name
        counter = 1
        while target.exists() and target != mp3_file:
            new_name = f"{title_clean}_{artist_clean}_{counter}.mp3"
            target = NOCTURNE / new_name
            counter += 1

        if mp3_file.name != new_name:
            renames.append((mp3_file, new_name, title, artist))
    else:
        skipped.append(mp3_file)

print(f"? Will rename: {len(renames)} files")
print(f"??  Will skip: {len(skipped)} files (no metadata)")
print()

# Show samples
print("=" * 80)
print("?? SAMPLE RENAMES (first 20):")
print("-" * 80)
for old_file, new_name, title, artist in renames[:20]:
    print(f"Old: {old_file.name[:70]}")
    print(f"New: {new_name}")
    print(f"     Title: {title}")
    print(f"     Artist: {artist}")
    print()

if len(renames) > 20:
    print(f"... and {len(renames) - 20} more")
print()

DRY_RUN = False

if DRY_RUN:
    print("=" * 80)
    print("?? DRY RUN")
    print("=" * 80)
    print()
    print("This will rename all files to clean format:")
    print("  Title_artist.mp3")
    print()
    print("Set DRY_RUN = False to execute")
    print()
else:
    print("=" * 80)
    print("??  EXECUTING RENAME")
    print("=" * 80)
    print()

    renamed = 0
    errors = 0

    for old_file, new_name, title, artist in renames:
        target = NOCTURNE / new_name

        try:
            old_file.rename(target)
            renamed += 1
            if renamed % 20 == 0:
                print(f"  Renamed {renamed} files...")
        except Exception as e:
            print(f"  Error: {old_file.name}: {e}")
            errors += 1

    print()
    print("=" * 80)
    print("? RENAME COMPLETE!")
    print("=" * 80)
    print()
    print(f"Renamed: {renamed} files")
    print(f"Errors: {errors}")
    print()
    print("All filenames now clean: Title_artist.mp3 ?")
    print()
