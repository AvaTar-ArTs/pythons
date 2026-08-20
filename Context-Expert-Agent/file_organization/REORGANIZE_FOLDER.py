#!/usr/bin/env python3
"""from datetime import datetime
from pathlib import Path
import json
import shutil
Reorganize Love_Is_Rubbish folder:
1. Move misplaced songs to proper folders
2. Rename remaining Love_is_Rubbish versions to standard format
3. Handle companion transcript/analysis files

Based on deep transcript analysis - see SONG_CATEGORIZATION.md
"""


# Configuration
NOCTURNE_DIR = Path("/Users/steven/Music/nocTurneMeLoDieS")
CURRENT_DIR = NOCTURNE_DIR / "Love_Is_Rubbish"
SINGLES_DIR = NOCTURNE_DIR / "Singles"
SAMMYS_BLUES_DIR = NOCTURNE_DIR / "Sammys_Blues"

# Songs to move OUT of this folder
MOVES = {
    # Live Fast Eat Trash songs ? Singles
    "Live_fast_Eat_Trash.mp3": ("Singles", "Live_Fast_Eat_Trash343.mp3"),
    "Live_fast_Eat_Trash_alt1.mp3": ("Singles", "Live_Fast_Eat_Trash343_Alt.mp3"),
    "rubbish.mp3": (
        "Singles",
        "Live_Fast_Eat_Trash249.mp3",
    ),  # Same song, different duration
    "rubbish0.mp3": ("Singles", "Live_Fast_Eat_Trash249_Alt.mp3"),
    # Trash Revolution ? Singles
    "Trash_Revolution.mp3": ("Singles", "Trash_Revolution229.mp3"),
    "Trash_Revolution_alt1.mp3": ("Singles", "Trash_Revolution229_Alt.mp3"),
    # Sammy's Blues song ? Sammys_Blues folder
    "rubbish-manga.mp3": (
        "Sammys_Blues",
        "Sammys_Blues254.mp3",
    ),  # Check actual title/duration
}

# Love is Rubbish renames (stay in this folder)
LOVE_IS_RUBBISH_RENAMES = {
    # Base versions
    "Love_is_Rubbish_and_Rubbish_is_Love-239.mp3": "Love_is_Rubbish239.mp3",
    "LoVe_is_RuBBisH_and_RuBBiSh_is_LoVe247.mp3": "Love_is_Rubbish247.mp3",
    "rubbish-love-disarray-244.mp3": "Love_is_Rubbish244.mp3",
    "rubbish-love-disarray-244_1.mp3": "Love_is_Rubbish244_Alt.mp3",
    "rubbish-love-disarray-309.mp3": "Love_is_Rubbish309.mp3",
    "rubbish-love-disarray-309_1.mp3": "Love_is_Rubbish309_Alt.mp3",
    # Remix versions
    "Love_is_rubbish_Lets_Get_Trashy_BanjoBandit238Remix.mp3": "Love_is_Rubbish238_BanjoBandit_Remix.mp3",
    "Love_is_rubbish_Lets_Get_Trashy_BanjoBandit308.mp3": "Love_is_Rubbish308_BanjoBandit.mp3",
    "Love_is_rubbish_Lets_Get_Trashy_BanjoBandit308_Remix.mp3": "Love_is_Rubbish308_BanjoBandit_Remix.mp3",
    "Love_is_rubbish_Lets_Get_Trashy_BanjoBandit308_Remix_Edit.mp3": "Love_is_Rubbish308_BanjoBandit_Remix_Edit.mp3",
    "Love_is_rubbish_Lets_Get_Trashy_Banjo_Remix259.mp3": "Love_is_Rubbish259_Banjo_Remix.mp3",
    "Love_is_rubbish_Lets_Get_Trashy_plucky_indieRemix257.mp3": "Love_is_Rubbish257_Plucky_Indie_Remix.mp3",
    "Love_is_rubbish_Lets_Get_Trashy_FeRaLFiddle254.mp3": "Love_is_Rubbish254_Feral_Fiddle.mp3",
    "Love_is_rubbish_Lets_Get_Trashy_rustyfunk317.mp3": "Love_is_Rubbish317_Rusty_Funk.mp3",
    "Love_is_rubbish_Lets_Get_Trashy_Remix234.mp3": "Love_is_Rubbish234_Remix.mp3",
    "Love_is_rubbish_Lets_Get_Trashy_Remix244.mp3": "Love_is_Rubbish244_Remix.mp3",
    "Love_is_rubbish_Lets_Get_Trashy_Remix318.mp3": "Love_is_Rubbish318_Remix.mp3",
    "Love_is_rubbish_Lets_Get_Trashy_Remix329.mp3": "Love_is_Rubbish329_Remix.mp3",
    "Love_is_rubbish_Lets_Get_Trashy_Remix304.mp3": "Love_is_Rubbish304_Remix.mp3",
    "Love_is_rubbish_Lets_Get_Trashy_Remix304-folk.mp3": "Love_is_Rubbish304_Folk_Remix.mp3",
    "Love_is_rubbish_Lets_Get_Trashy_Remix304-acoustic-FOLK-rock.mp3": "Love_is_Rubbish304_Acoustic_Folk_Rock.mp3",
    "Love_is_rubbish_Lets_Get_Trashy.mp3": "Love_is_Rubbish.mp3",  # Main version
    "Love_is_rubbish_Lets_Get_Trashy_Remastered.mp3": "Love_is_Rubbish_Remastered.mp3",
}


def move_with_companions(old_path, new_dir, new_name):
    """Move MP3 and its companion transcript/analysis files"""
    moves = []
    old_base = old_path.stem
    new_base = Path(new_name).stem

    # MP3
    if old_path.exists():
        moves.append((old_path, new_dir / new_name))

    # Transcript
    old_transcript = old_path.parent / f"{old_base}_transcript.txt"
    if old_transcript.exists():
        moves.append((old_transcript, new_dir / f"{new_base}_transcript.txt"))

    # Analysis
    old_analysis = old_path.parent / f"{old_base}_analysis.txt"
    if old_analysis.exists():
        moves.append((old_analysis, new_dir / f"{new_base}_analysis.txt"))

    return moves


def rename_with_companions(old_path, new_name):
    """Rename MP3 and its companion files"""
    renames = []
    old_base = old_path.stem
    new_base = Path(new_name).stem
    new_path = old_path.parent / new_name

    # MP3
    if old_path.exists():
        renames.append((old_path, new_path))

    # Transcript
    old_transcript = old_path.parent / f"{old_base}_transcript.txt"
    if old_transcript.exists():
        new_transcript = old_path.parent / f"{new_base}_transcript.txt"
        renames.append((old_transcript, new_transcript))

    # Analysis
    old_analysis = old_path.parent / f"{old_base}_analysis.txt"
    if old_analysis.exists():
        new_analysis = old_path.parent / f"{new_base}_analysis.txt"
        renames.append((old_analysis, new_analysis))

    return renames


print("=" * 80)
print("LOVE_IS_RUBBISH FOLDER REORGANIZATION")
print("=" * 80)

# Check directories exist
if not CURRENT_DIR.exists():
    print(f"? Current directory not found: {CURRENT_DIR}")
    exit(1)

# Create Singles if needed
if not SINGLES_DIR.exists():
    print(f"?? Creating Singles directory: {SINGLES_DIR}")
    SINGLES_DIR.mkdir(exist_ok=True)

if not SAMMYS_BLUES_DIR.exists():
    print(f"??  Warning: Sammys_Blues directory not found: {SAMMYS_BLUES_DIR}")
    print("   Will skip moving rubbish-manga.mp3")

# Build move plan
move_plan = []
for old_name, (target_folder, new_name) in MOVES.items():
    old_path = CURRENT_DIR / old_name

    if target_folder == "Singles":
        target_dir = SINGLES_DIR
    elif target_folder == "Sammys_Blues":
        target_dir = SAMMYS_BLUES_DIR
        if not target_dir.exists():
            continue

    moves = move_with_companions(old_path, target_dir, new_name)
    for old, new in moves:
        move_plan.append((old, new, target_folder))

# Build rename plan
rename_plan = []
for old_name, new_name in LOVE_IS_RUBBISH_RENAMES.items():
    old_path = CURRENT_DIR / old_name
    renames = rename_with_companions(old_path, new_name)
    rename_plan.extend(renames)

# Show plan
print(f"\n?? MOVES to other folders: {len(move_plan)} files")
by_folder = {}
for _, _, folder in move_plan:
    by_folder[folder] = by_folder.get(folder, 0) + 1
for folder, count in by_folder.items():
    print(f"  ? {folder}: {count} files")

print(f"\n??  RENAMES in this folder: {len(rename_plan)} files")
for old, new in rename_plan[:5]:
    print(f"  {old.name} ? {new.name}")
if len(rename_plan) > 5:
    print(f"  ... and {len(rename_plan) - 5} more")

# Confirm
total = len(move_plan) + len(rename_plan)
print(f"\n?? Total operations: {total}")
print("\n??  This will:")
print("  1. Move 'Live Fast Eat Trash' and 'Trash Revolution' songs to Singles/")
print("  2. Move 'rubbish-manga' to Sammys_Blues/ (if folder exists)")
print("  3. Rename all remaining files to Love_is_Rubbish[DUR]_[Type].mp3")
print("  4. Also move/rename companion _transcript.txt and _analysis.txt files")

response = input("\n??  Proceed? (yes/no): ").strip().lower()
if response not in ["yes", "y"]:
    print("? Cancelled")
    exit(0)

# Create log
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
log = {"timestamp": timestamp, "operations": []}

# Execute moves
print("\n" + "=" * 80)
print("MOVING FILES TO PROPER FOLDERS")
print("=" * 80)

for old_path, new_path, folder in move_plan:
    try:
        if new_path.exists():
            print(f"??  Target exists, skipping: {new_path}")
            continue

        shutil.move(str(old_path), str(new_path))
        log["operations"].append(
            {
                "type": "move",
                "from": str(old_path),
                "to": str(new_path),
                "folder": folder,
            },
        )
        print(f"? Moved to {folder}: {old_path.name} ? {new_path.name}")
    except Exception as e:
        print(f"? Error moving {old_path.name}: {e}")

# Execute renames
print("\n" + "=" * 80)
print("RENAMING LOVE_IS_RUBBISH FILES")
print("=" * 80)

for old_path, new_path in rename_plan:
    try:
        if new_path.exists():
            print(f"??  Target exists, skipping: {new_path.name}")
            continue

        old_path.rename(new_path)
        log["operations"].append(
            {"type": "rename", "from": str(old_path), "to": str(new_path)},
        )
        print(f"? {old_path.name} ? {new_path.name}")
    except Exception as e:
        print(f"? Error renaming {old_path.name}: {e}")

# Save log
log_file = CURRENT_DIR / f"REORGANIZE_LOG_{timestamp}.json"
with open(log_file, "w") as f:
    json.dump(log, f, indent=2)

print("\n" + "=" * 80)
print("COMPLETE")
print("=" * 80)
print(f"?? Log saved: {log_file.name}")

# Show final state
remaining = list(CURRENT_DIR.glob("*.mp3"))
print(f"\n?? Remaining MP3s in Love_Is_Rubbish: {len(remaining)}")

non_love = [f for f in remaining if not f.name.startswith("Love_is_Rubbish")]
if non_love:
    print("??  Files that don't match Love_is_Rubbish pattern:")
    for f in non_love:
        print(f"  - {f.name}")

print("\n? Folder reorganization complete!")
print(f"   Singles folder: {len(list(SINGLES_DIR.glob('*.mp3')))} MP3s")
print(f"   Love_Is_Rubbish folder: {len(remaining)} MP3s")

print("\n" + "=" * 80)
