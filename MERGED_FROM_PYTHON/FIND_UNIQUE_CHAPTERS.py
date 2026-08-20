#!/usr/bin/env python3
"""
Find UNIQUE chapters - remove duplicates with _2, _1_2, etc.
"""

from pathlib import Path
from mutagen import File as MutagenFile
from collections import defaultdict

BASE = Path("/Users/steven/Documents/Audiobooks/As_A_Man_Thinketh")

print("=" * 80)
print("?? FINDING UNIQUE AUDIOBOOK CHAPTERS")
print("=" * 80)
print()

# Scan all MP3s recursively
all_files = list(BASE.rglob("*.mp3"))

print(f"Found {len(all_files)} total MP3 files")
print()

# Group by base name (without _2, _1_2, etc.)
import re


def get_base_name(filename):
    """Remove version suffixes like _2, _1_2, part1_2, etc."""
    name = filename.replace(".mp3", "")
    # Remove AUDIO - prefix
    name = re.sub(r"^AUDIO\s*-\s*", "", name)
    # Remove _2, _1_2, _part1_2, etc.
    name = re.sub(r"_\d+(_\d+)?$", "", name)
    # Remove part1, part2, part3
    name = re.sub(r"_part\d+$", "", name)
    return name


chapters = defaultdict(list)

for f in all_files:
    base = get_base_name(f.name)

    # Get duration
    try:
        audio = MutagenFile(f)
        duration = int(audio.info.length) if audio and hasattr(audio, "info") else 0
    except:
        duration = 0

    size_mb = round(f.stat().st_size / (1024 * 1024), 2)

    chapters[base].append({"file": f, "duration": duration, "size": size_mb})

print(f"Unique chapters: {len(chapters)}")
print()

# Show each chapter and its versions
for chapter, versions in sorted(chapters.items()):
    print(f"{chapter}:")
    print(f"  {len(versions)} versions")

    # Group by duration to find true duplicates
    by_duration = defaultdict(list)
    for v in versions:
        by_duration[v["duration"]].append(v)

    if len(by_duration) > 1:
        print(f"  ??  Multiple durations: {list(by_duration.keys())}")

    # Show first of each duration
    for dur, files in by_duration.items():
        mins = dur // 60
        secs = dur % 60
        print(f"    ? {mins}:{secs:02d} ({len(files)} copies)")
    print()

# Summary
print("=" * 80)
print(f"TOTAL UNIQUE CHAPTERS: {len(chapters)}")
print(f"TOTAL FILES (including duplicates): {len(all_files)}")
print(f"DUPLICATES TO REMOVE: {len(all_files) - len(chapters)}")
print("=" * 80)
print()
