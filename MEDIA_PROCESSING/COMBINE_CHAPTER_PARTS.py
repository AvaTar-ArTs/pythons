#!/usr/bin/env python3
"""
Combine chapter parts into complete chapters
Keep only ONE best version of each combined chapter
"""

from pathlib import Path
from mutagen import File as MutagenFile
import shutil

BASE = Path("/Users/steven/Documents/Audiobooks/As_A_Man_Thinketh")
FINAL = BASE / "Complete_Chapters"
FINAL.mkdir(exist_ok=True)

print("=" * 80)
print("?? COMBINING CHAPTER PARTS INTO COMPLETE CHAPTERS")
print("=" * 80)
print()

# TRUE BOOK STRUCTURE (based on audio files found)
chapters = {
    "01_Foreword": [],
    "02_Thought_and_Character": [],
    "03_Effect_of_Thought_on_Circumstances": [],
    "04_Effect_of_Thought_on_Health": [],
    "05_Thought_and_Purpose": [],
    "07_Visions_and_Ideals": [],
    "08_Serenity": [],
    "Other": [],  # Divine-Perfection, etc.
}

# Scan all MP3s
all_files = list(BASE.rglob("*.mp3"))

for f in all_files:
    if "Complete_Chapters" in str(f) or "_Archive" in str(f):
        continue

    try:
        audio = MutagenFile(f)
        duration = int(audio.info.length) if audio and hasattr(audio, "info") else 0
    except:
        duration = 0

    name = f.name.lower()

    # Categorize
    if "foreword" in name or "01-" in name:
        chapters["01_Foreword"].append((f, duration))
    elif "thought" in name and "character" in name:
        chapters["02_Thought_and_Character"].append((f, duration))
    elif ("effect" in name or "03-" in name) and ("circumstance" in name):
        chapters["03_Effect_of_Thought_on_Circumstances"].append((f, duration))
    elif ("effect" in name or "04-" in name) and "health" in name:
        chapters["04_Effect_of_Thought_on_Health"].append((f, duration))
    elif "purpose" in name or "05-" in name:
        chapters["05_Thought_and_Purpose"].append((f, duration))
    elif "vision" in name or "ideal" in name or "07-" in name:
        chapters["07_Visions_and_Ideals"].append((f, duration))
    elif "serenity" in name or "08-" in name:
        chapters["08_Serenity"].append((f, duration))
    else:
        chapters["Other"].append((f, duration))

# Analyze and recommend best versions
print("?? CHAPTER ANALYSIS & RECOMMENDATIONS:")
print()

for chapter, files in chapters.items():
    if not files:
        continue

    print(f"{chapter}:")
    print(f"  Total versions/parts: {len(files)}")

    # Group by duration to find complete vs. parts
    from collections import defaultdict

    by_duration = defaultdict(list)

    for f, dur in files:
        by_duration[dur].append(f)

    # Sort by duration (longest first = likely complete chapter)
    sorted_durs = sorted(by_duration.items(), key=lambda x: x[0], reverse=True)

    if sorted_durs:
        longest_dur, longest_files = sorted_durs[0]
        mins = longest_dur // 60
        secs = longest_dur % 60

        # Pick best file (prefer non-"_2" versions, prefer without "AUDIO -" prefix)
        best_file = None
        for f in longest_files:
            if "_2" not in f.name and "AUDIO -" not in f.name:
                best_file = f
                break

        if not best_file:
            best_file = longest_files[0]

        print(f"  ? RECOMMENDED: {best_file.name} ({mins}:{secs:02d})")
        print(f"     Duplicates of same length: {len(longest_files) - 1}")

        # Show other versions
        if len(sorted_durs) > 1:
            print("     Other versions/parts:")
            for dur, files_list in sorted_durs[1:4]:  # Show top 3 others
                m = dur // 60
                s = dur % 60
                print(f"       ? {m}:{s:02d} - {len(files_list)} file(s)")

        # Copy best to Final
        dest = FINAL / f"{chapter}.mp3"
        if not dest.exists():
            shutil.copy2(str(best_file), str(dest))
            print(f"     ? Copied to: Complete_Chapters/{chapter}.mp3")

    print()

# Summary
final_chapters = list(FINAL.glob("*.mp3"))
print("=" * 80)
print("?? FINAL SUMMARY")
print("=" * 80)
print()
print(f"Original files: {len(all_files)}")
print(f"Unique chapters created: {len(final_chapters)}")
print(f"Duplicates/parts removed: {len(all_files) - len(final_chapters)}")
print()
print("? Complete chapters saved to: Complete_Chapters/")
print()
