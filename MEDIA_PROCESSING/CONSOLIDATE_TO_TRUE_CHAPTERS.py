#!/usr/bin/env python3
"""
Consolidate 83 audio files into TRUE 3 chapters based on the official book structure:
1. Foreword (2-3 minutes)
2. Thought and Character (8-10 minutes) 
3. Effect of Thought on Circumstances (12-15 minutes)

Keep BEST version of each, remove duplicates/takes
"""

from pathlib import Path
from mutagen import File as MutagenFile
from collections import defaultdict
import shutil

BASE = Path("/Users/steven/Documents/Audiobooks/As_A_Man_Thinketh")
ARCHIVE = BASE / "_Archive_Multiple_Takes"
FINAL = BASE / "Final_Chapters"

print("=" * 80)
print("?? CONSOLIDATING TO TRUE CHAPTER STRUCTURE")
print("=" * 80)
print()

# Create directories
ARCHIVE.mkdir(exist_ok=True)
FINAL.mkdir(exist_ok=True)

# Scan all MP3s
all_files = list(BASE.rglob("*.mp3"))
print(f"Found {len(all_files)} total MP3 files")
print()

# TRUE CHAPTERS from the book structure
chapters = {
    'foreword': {
        'expected_duration': (120, 180),  # 2-3 minutes
        'files': []
    },
    'thought_and_character': {
        'expected_duration': (480, 600),  # 8-10 minutes
        'files': []
    },
    'effect_of_thought': {
        'expected_duration': (720, 900),  # 12-15 minutes
        'files': []
    },
    'other': {
        'expected_duration': (0, 999999),
        'files': []
    }
}

# Classify files
for f in all_files:
    if '_Archive' in str(f) or 'Final_Chapters' in str(f):
        continue
    
    try:
        audio = MutagenFile(f)
        duration = int(audio.info.length) if audio and hasattr(audio, 'info') else 0
    except:
        duration = 0
    
    name = f.name.lower()
    
    # Categorize
    if 'foreword' in name:
        chapters['foreword']['files'].append((f, duration))
    elif 'thought' in name and 'character' in name:
        chapters['thought_and_character']['files'].append((f, duration))
    elif 'effect' in name or 'circumstance' in name:
        chapters['effect_of_thought']['files'].append((f, duration))
    else:
        chapters['other']['files'].append((f, duration))

# Show analysis
print("CHAPTER ANALYSIS:")
print()

for chapter, data in chapters.items():
    if chapter == 'other':
        continue
        
    files = data['files']
    expected = data['expected_duration']
    
    print(f"{chapter.upper().replace('_', ' ')}:")
    print(f"  Expected: {expected[0]//60}:{expected[0]%60:02d} - {expected[1]//60}:{expected[1]%60:02d}")
    print(f"  Found: {len(files)} versions")
    
    if files:
        # Find version closest to expected duration
        best = None
        for f, dur in files:
            if expected[0] <= dur <= expected[1]:
                if best is None or abs(dur - (expected[0] + expected[1])//2) < abs(best[1] - (expected[0] + expected[1])//2):
                    best = (f, dur)
        
        if best:
            mins = best[1] // 60
            secs = best[1] % 60
            print(f"  ? BEST: {best[0].name} ({mins}:{secs:02d})")
        else:
            # If no perfect match, show all and let user choose
            print(f"  ??  No version in expected range!")
            for f, dur in sorted(files, key=lambda x: x[1]):
                mins = dur // 60
                secs = dur % 60
                print(f"      ? {f.name} ({mins}:{secs:02d})")
    print()

# Show "Other" files
other_files = chapters['other']['files']
if other_files:
    print(f"OTHER FILES ({len(other_files)}):")
    for f, dur in sorted(other_files, key=lambda x: x[1]):
        mins = dur // 60
        secs = dur % 60
        print(f"  ? {f.name} ({mins}:{secs:02d})")
    print()

print("=" * 80)
print("?? SUMMARY")
print("=" * 80)
print()
print(f"Total files: {len(all_files)}")
print(f"Foreword versions: {len(chapters['foreword']['files'])}")
print(f"Thought & Character versions: {len(chapters['thought_and_character']['files'])}")
print(f"Effect of Thought versions: {len(chapters['effect_of_thought']['files'])}")
print(f"Other files: {len(chapters['other']['files'])}")
print()
print("TRUE CHAPTERS: 3")
print(f"TOTAL VERSIONS: {len(all_files)}")
print(f"DUPLICATES TO REMOVE: {len(all_files) - 3}")
print()
