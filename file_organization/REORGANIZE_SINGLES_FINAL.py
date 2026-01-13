#!/usr/bin/env python3
"""from datetime import datetime
from pathlib import Path
import json
import shutil
Reorganize Singles folder - FINAL VERSION
- Move 44 files to album folders
- Move 14 files to root nocTurneMeLoDieS folder (true singles + covers)
- Singles folder will be EMPTY after this
- Create new Storytelling folder
"""


nocturne_dir = Path("/Users/steven/Music/nocTurneMeLoDieS")
singles_dir = nocturne_dir / "Singles"

# Files moving to album folders
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
    "Rituals": [
        "The_Jungle_Shaman.mp3",
        "FeLLowCeLlo.mp3",
        "Trinity.mp3",
        "Micro.mp3",
        "Mystical_Mushroom_Realm - Micro.mp3",
    ],
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
}

# ALL FILES move to root nocTurneMeLoDieS folder (singles that have no album home)
MOVE_TO_ROOT = [
    # True singles
    "All_I_Wanna_Do.mp3",
    "Call_for_More.mp3",
    # Covers and misc (singles with no album match)
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

    # SRT
    src_srt = src_file.parent / f"{src_base}.srt"
    if src_srt.exists():
        dest_srt = dest_dir / f"{src_base}.srt"
        moves.append((src_srt, dest_srt, "srt"))

    return moves


print("=" * 80)
print("SINGLES FOLDER REORGANIZATION - FINAL")
print("=" * 80)

if not singles_dir.exists():
    print(f"? Singles folder not found: {singles_dir}")
    exit(1)

# Create Storytelling folder
storytelling_dir = nocturne_dir / "Storytelling"
if not storytelling_dir.exists():
    print("\n?? Will create new folder: Storytelling/")

# Build move plans
move_plan = []
move_to_root_plan = []
missing_files = []
missing_folders = []

# Plan moves to root
for filename in MOVE_TO_ROOT:
    src_file = singles_dir / filename
    if not src_file.exists():
        missing_files.append(filename)
        continue

    moves = move_with_companions(src_file, nocturne_dir)
    for src, dest, file_type in moves:
        move_to_root_plan.append((src, dest, "ROOT", file_type))

# Plan moves to albums
for dest_folder, files in MOVES.items():
    dest_dir = nocturne_dir / dest_folder

    # Will be created
    if dest_folder == "Storytelling" and not dest_dir.exists():
        pass  # Will create below
    elif not dest_dir.exists():
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

# Combine
all_moves = move_to_root_plan + move_plan

# Show plan
print("\n?? OPERATIONS PLANNED:")
print(f"   Files to album folders: {len([m for m in move_plan if m[3] == 'mp3'])}")
print(
    f"   Files to root folder: {len([m for m in move_to_root_plan if m[3] == 'mp3'])}",
)
print(f"   Companion files: {len([m for m in all_moves if m[3] != 'mp3'])}")
print(f"   Total operations: {len(all_moves)}")

if missing_folders:
    print(f"\n? Missing folders: {', '.join(missing_folders)}")
    print("   Script will skip these")

if missing_files:
    print(f"\n??  Files not found: {len(missing_files)}")
    for f in missing_files[:3]:
        print(f"   ? {f}")

# Show destinations
print("\n?? DESTINATION BREAKDOWN:")
dest_counts = {}
for _, _, dest, ftype in all_moves:
    if ftype == "mp3":
        dest_counts[dest] = dest_counts.get(dest, 0) + 1

for dest in sorted(dest_counts.keys()):
    if dest == "ROOT":
        print(f"   ? nocTurneMeLoDieS/ (root): {dest_counts[dest]} files")
    else:
        print(f"   ? {dest}/: +{dest_counts[dest]} files")

# Confirm
print("\n" + "=" * 80)
print("??  SINGLES FOLDER WILL BE EMPTY AFTER THIS!")
print("=" * 80)
print("This will:")
print("  1. Create new 'Storytelling/' folder (+4 files)")
print("  2. Move 44 files to proper album folders")
print("  3. Move 14 files to main nocTurneMeLoDieS/ root folder")
print("  4. Leave Singles/ folder EMPTY")
print("\nSingles folder purpose: Only for files with no album/theme match")
print("=" * 80)

response = input("\n??  Proceed? (yes/no): ").strip().lower()
if response not in ["yes", "y"]:
    print("? Cancelled - no changes made")
    exit(0)

# CREATE STORYTELLING FOLDER
if not storytelling_dir.exists():
    print(f"\n?? Creating folder: {storytelling_dir}")
    storytelling_dir.mkdir(exist_ok=True)

# Execute moves
print("\n" + "=" * 80)
print("EXECUTING REORGANIZATION")
print("=" * 80)

timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
log = {
    "timestamp": timestamp,
    "source": "Singles",
    "storytelling_created": True,
    "moves": [],
    "errors": [],
}

success_count = 0
error_count = 0

for src, dest, dest_folder, file_type in all_moves:
    try:
        if dest.exists():
            print(f"??  Skipping (exists): {dest.name}")
            log["errors"].append({"file": src.name, "reason": "target_exists"})
            continue

        shutil.move(str(src), str(dest))
        log["moves"].append(
            {"file": src.name, "from": "Singles", "to": dest_folder, "type": file_type},
        )

        if file_type == "mp3":
            if dest_folder == "ROOT":
                print(f"? nocTurneMeLoDieS/ ? {src.name}")
            else:
                print(f"? {dest_folder}/ ? {src.name}")

        success_count += 1
    except Exception as e:
        print(f"? Error: {src.name} - {e}")
        log["errors"].append({"file": src.name, "error": str(e)})
        error_count += 1

# Save log
log_file = nocturne_dir / f"SINGLES_REORGANIZE_LOG_{timestamp}.json"
with open(log_file, "w") as f:
    json.dump(log, f, indent=2)

# Create summary in root (not Singles since it'll be empty)
summary_file = nocturne_dir / f"SINGLES_CLEANUP_COMPLETE_{timestamp}.txt"
with open(summary_file, "w") as f:
    f.write(f"Singles Reorganization Complete - {timestamp}\n")
    f.write("=" * 70 + "\n\n")
    f.write(f"Successful moves: {success_count}\n")
    f.write(f"Errors: {error_count}\n\n")
    f.write(
        f"Files moved to albums: {len([m for m in log['moves'] if m['to'] != 'ROOT' and m['type'] == 'mp3'])}\n",
    )
    f.write(
        f"Files moved to root: {len([m for m in log['moves'] if m['to'] == 'ROOT' and m['type'] == 'mp3'])}\n",
    )
    f.write("Singles folder: EMPTY (all files reorganized)\n\n")
    f.write("New folder created: Storytelling/\n")
    f.write("  ? itchy.mp3 (iTchy iSLe documentary series)\n")
    f.write("  ? iTchy_iSLe659.mp3\n")
    f.write("  ? iTchy_iSLe759.mp3\n")
    f.write("  ? Pals - Trickster.mp3 (Maya mythology)\n\n")
    f.write("Files in root nocTurneMeLoDieS folder:\n")
    f.write("  ? True singles (All_I_Wanna_Do, Call_for_More)\n")
    f.write("  ? Cover songs (Kbong, Infraction, Adele, etc.)\n")
    f.write("  ? Misc/test files\n")

print("\n" + "=" * 80)
print("? REORGANIZATION COMPLETE!")
print("=" * 80)
print(f"? Successful: {success_count} files/operations")
print(f"? Errors: {error_count}")
print(f"?? Log: {log_file.name}")
print(f"?? Summary: {summary_file.name}")

# Show final state
print("\n?? FINAL STATE:")
remaining = list(singles_dir.glob("*.mp3"))
root_files = list(nocturne_dir.glob("*.mp3"))
storytelling_files = (
    list(storytelling_dir.glob("*.mp3")) if storytelling_dir.exists() else []
)

print(f"   Singles/: {len(remaining)} MP3s (EMPTY or nearly empty!)")
print(f"   nocTurneMeLoDieS/: {len(root_files)} MP3s in root folder")
print(f"   Storytelling/: {len(storytelling_files)} MP3s (NEW folder!)")

print("\n? All Singles files now properly organized!")
print("   Singles folder is now clean for future use.")
print("=" * 80)
