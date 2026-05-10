#!/usr/bin/env python3
"""
Keep ONE of each chapter, delete duplicates
For chapters with multiple durations, keep ONE of each duration
"""

from pathlib import Path
from mutagen import File as MutagenFile
from collections import defaultdict
import re

BASE = Path("/Users/steven/Documents/Audiobooks/As_A_Man_Thinketh")

print("=" * 80)
print("???  REMOVING DUPLICATE CHAPTERS")
print("=" * 80)
print()


def get_base_name(filename):
    """Remove version suffixes"""
    name = filename.replace(".mp3", "")
    name = re.sub(r"^AUDIO\s*-\s*", "", name)
    name = re.sub(r"_\d+(_\d+)?$", "", name)
    name = re.sub(r"_part\d+$", "", name)
    return name


# Scan all MP3s
all_files = list(BASE.rglob("*.mp3"))
chapters = defaultdict(list)

for f in all_files:
    base = get_base_name(f.name)

    try:
        audio = MutagenFile(f)
        duration = int(audio.info.length) if audio and hasattr(audio, "info") else 0
    except:
        duration = 0

    chapters[base].append({"file": f, "duration": duration})

print(f"Found {len(all_files)} files")
print(f"Unique chapters: {len(chapters)}")
print()

# For each chapter, keep FIRST of each duration, delete rest
kept = 0
deleted = 0

for chapter, versions in sorted(chapters.items()):
    # Group by duration
    by_duration = defaultdict(list)
    for v in versions:
        by_duration[v["duration"]].append(v["file"])

    # Keep first of each duration
    for duration, files in by_duration.items():
        if files:
            keep = files[0]
            kept += 1

            # Delete the rest
            for dup in files[1:]:
                try:
                    dup.unlink()
                    deleted += 1
                except Exception as e:
                    print(f"  ??  Error deleting {dup.name}: {e}")

print()
print(f"? Kept: {kept} unique files")
print(f"???  Deleted: {deleted} duplicates")
print()

# Now organize the remaining files properly
print("=" * 80)
print("?? ORGANIZING INTO CHAPTERS")
print("=" * 80)
print()

# Clean up - move all remaining files to root
import shutil

remaining = list(BASE.rglob("*.mp3"))
print(f"Remaining files: {len(remaining)}")

for f in remaining:
    if f.parent != BASE:
        dest = BASE / f.name
        print(f"  {f.name} ? root/")
        shutil.move(str(f), str(dest))

# Remove empty folders
for d in BASE.iterdir():
    if d.is_dir() and d.name != "DOCS":
        try:
            d.rmdir()
            print(f"  Removed empty: {d.name}/")
        except:
            pass

print()
print("? All chapters at root level")
print()
