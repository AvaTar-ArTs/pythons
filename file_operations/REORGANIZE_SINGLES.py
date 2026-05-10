#!/usr/bin/env python3
"""from datetime import datetime
from pathlib import Path
import json
import shutil
Reorganize Singles folder - move files back to their proper albums
Based on song titles, themes, and Suno data analysis

Total: 58 files
- 38 files to move to albums
- 12 files keep in Singles (covers/misc)
- 8 files need manual review
"""

nocturne_dir = Path("/Users/steven/Music/nocTurneMeLoDieS")
singles_dir = nocturne_dir / "Singles"

# Reorganization map
MOVES = {
    "Bite_in_the_Night": ["AUDIO - Touch of a calming night by Lygia _ Suno.mp3"],
    "Book_of_Memory": [
        "PeTaLs_FaLL_Banjo.mp3",
        "PeTals_FaLL_Remasteredflutr.mp3",
        "Petals_Fall copy.mp3",
        "Petals_Fall_RooTs_ReMain301.mp3",
        "Petals_fall_yet_roots_remain.mp3",
        "petals_fall_duo-344.mp3",
        "PeTasLs.mp3",
    ],
    "Love_In_Imperfection": ["love_imperfection.mp3"],
    "Feather_Fang": ["I_Became_Beast_Remix.mp3", "iBecame_Etherial_Duo_Ritual.mp3"],
    "Tapestry_Of_Tyranny": [
        "Graves_Before_Throne.mp3",
        "Graves_Before_Throne_Ballad_Remix.mp3",
        "Graves_Before_Throne_Rock_short.mp3",
    ],
    "Shadow_Messages": ["DarkWeb_Violin_Duo.mp3", "Darkest.mp3"],
    "Heartbeats": [
        "Heartbreak_hope_and_memories-og_Remastered.mp3",
        "Head_and_Heats_Onfire - Ai Billie.mp3",
        "Heads - Billie.mp3",
    ],
    "Epic_Fantasy_Battle_Ballade": ["fantasy_ballade_LyricRemix.mp3"],
    "Enchanted_Woods": ["golden_roots2.mp3"],
    "Murray_Kyle_-_Standing_On_One_Side": [
        "Standing_on_One_Side_mixd.mp3",
        "Standing_on_One_Side_mixd_Remix.mp3",
    ],
    "Echoes_Moonlight": ["Whispers_Of_The_Night229.mp3"],
    "Rituals": ["The_Jungle_Shaman.mp3", "FeLLowCeLlo.mp3", "Trinity.mp3"],
    "Philosophical": ["think-spoken.mp3", "wtching-you.mp3"],
    "Stormchild": ["Rhythms_Circle.mp3", "Circles.mp3", "acoustice-circles.mp3"],
    "Heavenly_Hands": ["Mother.mp3"],
    "Workshop_Series": [
        "Spiral_Architect.mp3",
        "Spiral_Architect_dup1.mp3",
        "Spiral_Architects.mp3",
    ],
    "RocketMan-Covers": ["Adele - Heads.mp3", "Adele - Heads and Hearts.mp3"],
    "Storytelling": [
        "itchy.mp3",
        "iTchy_iSLe659.mp3",
        "iTchy_iSLe759.mp3",
        "Pals - Trickster.mp3",
    ],
    "Rituals": [
        "The_Jungle_Shaman.mp3",
        "FeLLowCeLlo.mp3",
        "Trinity.mp3",
        "Micro.mp3",
        "Mystical_Mushroom_Realm - Micro.mp3",
    ],
}

# Files to move to main nocTurneMeLoDieS folder (root)
MOVE_TO_ROOT = ["All_I_Wanna_Do.mp3", "Call_for_More.mp3"]

# Files to keep in Singles (covers/misc only)
KEEP_IN_SINGLES = [
    "Infraction - Dance With Me.mp3",
    "Justin-Marcellus - Dilation_Cyberpunkdaram.mp3",
    "Kbong - In Session.mp3",
    "Metelkin_Viktor - for snoop in cyberpunk.mp3",
    "Rise-To-Power - Christoffer-Moe-Ditlevsen.mp3",
    "Super_Crooks_OP_ALPHA_-_TOWA_TEI_with_Taprikk_Sweezee_Netflix_Anime_6Sby8-UDIa4.mp3",
    "AvaTar_ArTs - Trickycoh.mp3",
    "Through_and_Through - Amulets.mp3",
    "Music2video - Imagenet Song.mp3",
    "Nope-only_pic.mp3",
    "Misc_Songs - _Remix.mp3",
    "Misc Songs_296.mp3",
]


def move_with_companions(src_file, dest_dir):
    """Move MP3 and companion files"""
    moves = []
    src_base = src_file.stem

    # MP3
    if src_file.exists():
        dest_file = dest_dir / src_file.name
        moves.append((src_file, dest_file, "mp3"))

    # Transcript
    src_transcript = src_file.parent / f"{src_base}_transcript.txt"
    if src_transcript.exists():
        dest_transcript = dest_dir / f"{src_base}_transcript.txt"
        moves.append((src_transcript, dest_transcript, "transcript"))

    # Analysis
    src_analysis = src_file.parent / f"{src_base}_analysis.txt"
    if src_analysis.exists():
        dest_analysis = dest_dir / f"{src_base}_analysis.txt"
        moves.append((src_analysis, dest_analysis, "analysis"))

    # SRT (subtitle files)
    src_srt = src_file.parent / f"{src_base}.srt"
    if src_srt.exists():
        dest_srt = dest_dir / f"{src_base}.srt"
        moves.append((src_srt, dest_srt, "srt"))

    return moves


print("=" * 80)
print("SINGLES FOLDER REORGANIZATION")
print("=" * 80)

# Check Singles folder exists
if not singles_dir.exists():
    print(f"? Singles folder not found: {singles_dir}")
    exit(1)

# Plan all moves
move_plan = []
missing_files = []
missing_folders = []

for dest_folder, files in MOVES.items():
    dest_dir = nocturne_dir / dest_folder

    # Check if destination exists
    if not dest_dir.exists():
        missing_folders.append(dest_folder)
        continue

    for filename in files:
        src_file = singles_dir / filename
        if not src_file.exists():
            missing_files.append(filename)
            continue

        moves = move_with_companions(src_file, dest_dir)
        for src, dest, file_type in moves:
            move_plan.append((src, dest, dest_folder, file_type))

# Show plan
print("\n?? STATISTICS:")
print(f"   Files to move: {len([m for m in move_plan if m[3] == 'mp3'])}")
print(f"   Companion files: {len([m for m in move_plan if m[3] != 'mp3'])}")
print(f"   Total operations: {len(move_plan)}")
print(f"   Destination folders: {len(MOVES)}")

if missing_folders:
    print(f"\n??  Missing destination folders ({len(missing_folders)}):")
    for folder in missing_folders:
        print(f"   ? {folder}")

if missing_files:
    print(f"\n??  Files not found ({len(missing_files)}):")
    for f in missing_files[:5]:
        print(f"   ? {f}")

print("\n?? DESTINATION BREAKDOWN:")
dest_counts = {}
for _, _, dest, ftype in move_plan:
    if ftype == "mp3":
        dest_counts[dest] = dest_counts.get(dest, 0) + 1

for dest in sorted(dest_counts.keys()):
    print(f"   ? {dest}: +{dest_counts[dest]} files")

print("\n?? FILES STAYING IN SINGLES:")
print(f"   ? {len(KEEP_IN_SINGLES)} cover songs / misc")
print(f"   ? {len(NEEDS_REVIEW)} need manual review")

# Confirm
print("\n" + "=" * 80)
response = input("??  Proceed with reorganization? (yes/no): ").strip().lower()
if response not in ["yes", "y"]:
    print("? Cancelled")
    exit(0)

# Execute moves
print("\n" + "=" * 80)
print("EXECUTING MOVES")
print("=" * 80)

timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
log = {"timestamp": timestamp, "source": str(singles_dir), "moves": [], "errors": []}

success_count = 0
error_count = 0

for src, dest, dest_folder, file_type in move_plan:
    try:
        if dest.exists():
            print(f"??  Target exists, skipping: {dest.name}")
            log["errors"].append(
                {"file": src.name, "reason": "target_exists", "dest": str(dest)},
            )
            continue

        shutil.move(str(src), str(dest))
        log["moves"].append(
            {"file": src.name, "from": "Singles", "to": dest_folder, "type": file_type},
        )

        if file_type == "mp3":
            print(f"? {dest_folder} ? {src.name}")

        success_count += 1
    except Exception as e:
        print(f"? Error moving {src.name}: {e}")
        log["errors"].append({"file": src.name, "error": str(e)})
        error_count += 1

# Create review file for remaining
review_file = singles_dir / "NEEDS_MANUAL_REVIEW.txt"
with open(review_file, "w") as f:
    f.write("Files in Singles that need manual review:\n")
    f.write("=" * 60 + "\n\n")
    for filename in NEEDS_REVIEW:
        f.write(f"? {filename}\n")
    f.write(
        f"\n\nNOTE: {len(KEEP_IN_SINGLES)} files were intentionally kept in Singles\n",
    )
    f.write("(cover songs and misc files)\n")

# Save log
log_file = nocturne_dir / f"SINGLES_REORGANIZE_LOG_{timestamp}.json"
with open(log_file, "w") as f:
    json.dump(log, f, indent=2)

print("\n" + "=" * 80)
print("COMPLETE")
print("=" * 80)
print(f"? Successful moves: {success_count}")
print(f"? Errors: {error_count}")
print(f"?? Log saved: {log_file.name}")
print(f"?? Review file created: {review_file}")

print("\n?? SINGLES FOLDER STATUS:")
remaining = list(singles_dir.glob("*.mp3"))
print(f"   Files remaining: {len(remaining)}")
print(f"   ? {len(KEEP_IN_SINGLES)} intentionally kept (covers/misc)")
print(f"   ? {len(NEEDS_REVIEW)} need manual review")

print("\n" + "=" * 80)
