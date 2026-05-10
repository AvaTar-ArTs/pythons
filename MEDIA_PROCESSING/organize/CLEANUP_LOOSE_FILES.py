#!/usr/bin/env python3
"""
Move loose MP3s and old folders into proper sections
"""

from pathlib import Path
import shutil

BASE = Path("/Users/steven/Documents/Audiobooks/As_A_Man_Thinketh")

print("?? Cleaning up loose files...")
print()

# Get all loose MP3s
loose_files = [f for f in BASE.glob("*.mp3")]

print(f"Found {len(loose_files)} loose MP3 files")

# Move them to appropriate sections
moved = 0
for f in loose_files:
    name = f.name.lower()

    # Determine destination
    if "serenity" in name:
        dest_dir = BASE / "7_Serenity"
    elif "vision" in name or "ideal" in name:
        dest_dir = BASE / "6_Visions_and_Ideals"
    elif "purpose" in name:
        dest_dir = BASE / "4_Thought_and_Purpose"
    elif "effect" in name or "health" in name:
        dest_dir = BASE / "3_Effect_of_Thought"
    elif (
        "divine" in name
        or "mastery" in name
        or "poem" in name
        or "universal" in name
        or "power" in name
    ):
        dest_dir = BASE / "8_Other"
    else:
        dest_dir = BASE / "8_Other"

    dest = dest_dir / f.name
    print(f"  {f.name} ? {dest_dir.name}/")
    shutil.move(str(f), str(dest))
    moved += 1

print()

# Move old folders
old_folders = [
    d
    for d in BASE.iterdir()
    if d.is_dir()
    and not d.name.startswith(("1_", "2_", "3_", "4_", "5_", "6_", "7_", "8_"))
]

print(f"Found {len(old_folders)} old folders to consolidate")

for old_dir in old_folders:
    print(f"\n  Consolidating: {old_dir.name}/")

    # Move all files from old folders into appropriate new sections
    for f in old_dir.glob("*.mp3"):
        name = f.name.lower()

        if "foreword" in old_dir.name.lower():
            dest_dir = BASE / "1_Foreword"
        elif "thought" in old_dir.name.lower() and "character" in old_dir.name.lower():
            dest_dir = BASE / "2_Thought_and_Character"
        else:
            dest_dir = BASE / "8_Other"

        dest = dest_dir / f.name
        print(f"    {f.name} ? {dest_dir.name}/")
        shutil.move(str(f), str(dest))
        moved += 1

    # Remove empty old folder
    try:
        old_dir.rmdir()
        print(f"    Removed: {old_dir.name}/")
    except:
        print(f"    ??  {old_dir.name}/ not empty")

print()
print(f"? Moved {moved} files")
print()
