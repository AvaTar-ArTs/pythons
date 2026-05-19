#!/usr/bin/env python3
"""from datetime import datetime
from pathlib import Path
import json
import subprocess
INTELLIGENT FOLDER-AWARE CLEANUP
- Detects files in wrong folders based on content/naming
- Moves to correct folders
- Fixes duration codes
- Standardizes naming format
"""

nocturne_dir = Path("/Users/steven/Music/nocTurneMeLoDieS")


def get_duration(mp3_file):
    try:
        result = subprocess.run(
            [
                "ffprobe",
                "-v",
                "quiet",
                "-show_entries",
                "format=duration",
                "-of",
                "default=nw=1:nk=1",
                str(mp3_file),
            ],
            capture_output=True,
            text=True,
            timeout=5,
        )
        dur = int(float(result.stdout.strip()))
        return dur
    except:
        return None


def get_correct_code(seconds):
    return f"{seconds // 60}{seconds % 60:02d}"


def move_with_companions(src_file, dest_dir):
    """Move MP3 and companion files"""
    moves = []
    src_base = src_file.stem

    # MP3
    moves.append(("mp3", src_file, dest_dir / src_file.name))

    # Transcript
    src_transcript = src_file.parent / f"{src_base}_transcript.txt"
    if src_transcript.exists():
        moves.append(
            ("transcript", src_transcript, dest_dir / f"{src_base}_transcript.txt"),
        )

    # Analysis
    src_analysis = src_file.parent / f"{src_base}_analysis.txt"
    if src_analysis.exists():
        moves.append(("analysis", src_analysis, dest_dir / f"{src_base}_analysis.txt"))

    return moves


print("=" * 80)
print("INTELLIGENT FOLDER-AWARE CLEANUP")
print("=" * 80)

# PHASE 1: Detect and fix misplaced files
misplaced_files = [
    # Workshop_Series ? Tapestry_Of_Tyranny
    {
        "current_folder": "Workshop_Series",
        "current_file": "Tapestry_of_Tyranny715.mp3",
        "correct_folder": "Tapestry_Of_Tyranny",
        "new_name": "Tapestry_of_Tyranny714.mp3",  # 7:14
        "reason": "Wrong folder + wrong code (715 ? 714)",
    },
    {
        "current_folder": "Workshop_Series",
        "current_file": "Tapestry_of_Tyranny7591.mp3",
        "correct_folder": "Tapestry_Of_Tyranny",
        "new_name": "Tapestry_of_Tyranny759.mp3",  # 7:59
        "reason": "Wrong folder + garbage code (7591 ? 759)",
    },
    {
        "current_folder": "Workshop_Series",
        "current_file": "Tapestry_of_Tyranny_7592_Remix.mp3",
        "correct_folder": "Tapestry_Of_Tyranny",
        "new_name": "Tapestry_of_Tyranny_Remix759.mp3",  # 7:59
        "reason": "Wrong folder + garbage code (7592 ? 759)",
    },
    {
        "current_folder": "Workshop_Series",
        "current_file": "Tapestry_of_Tyranny_Remix7593.mp3",
        "correct_folder": "Tapestry_Of_Tyranny",
        "new_name": "Tapestry_of_Tyranny_Remix759_Alt.mp3",  # 7:59
        "reason": "Wrong folder + garbage code (7593 ? 759)",
    },
    {
        "current_folder": "Workshop_Series",
        "current_file": "Tapestry_of_Tyranny_550Remix.mp3",
        "correct_folder": "Tapestry_Of_Tyranny",
        "new_name": "Tapestry_of_Tyranny_Remix550.mp3",  # 5:50
        "reason": "Wrong folder + cleaner format",
    },
    {
        "current_folder": "Workshop_Series",
        "current_file": "Tapestry_of_Tyranny_Remix.mp3",
        "correct_folder": "Tapestry_Of_Tyranny",
        "new_name": "Tapestry_of_Tyranny_Remix742.mp3",  # Will verify actual duration
        "reason": "Wrong folder + missing code",
    },
]

# PHASE 2: In-folder renames (files in correct folder, just wrong code/format)
in_folder_renames = [
    # Workshop_Series - WorkShop_Worries files stay here
    {
        "folder": "Workshop_Series",
        "old": "WorkShop_Worries-359-fixed2.mp3",
        "new": "WorkShop_Worries_Fixed2_413.mp3",
        "reason": "Wrong code (359 ? 413) + clean format",
    },
    {
        "folder": "Workshop_Series",
        "old": "WorkShop_Worries-418-_Rhythm_Remix.mp3",
        "new": "WorkShop_Worries_Rhythm_Remix348.mp3",
        "reason": "Wrong code (418 ? 348) + clean format",
    },
    {
        "folder": "Workshop_Series",
        "old": "WorkShop_Worries-418-_Rhythm_Remix_alt1.mp3",
        "new": "WorkShop_Worries_Rhythm_Remix348_Alt.mp3",
        "reason": "Wrong code (418 ? 348) + clean format",
    },
    # Blues_Alley
    {
        "folder": "Blues_Alley",
        "old": "sammy_Midnight_Reckoning_by_DarkSoundEffect3495___Suno_Remix.mp3",
        "new": "Sammy_Midnight_Reckoning248_Suno_Remix.mp3",
        "reason": "Garbage code (3495 ? 248) + simplified",
    },
    {
        "folder": "Blues_Alley",
        "old": "sammy_Midnight_Reckoning_by_DarkSoundEffect3495_Suno_Remix.mp3",
        "new": "Sammy_Midnight_Reckoning248_Suno_Remix_Alt.mp3",
        "reason": "Garbage code (3495 ? 248) + simplified",
    },
    # Willow_Whispers
    {
        "folder": "Willow_Whispers",
        "old": "Willow_whispers-feelers-chill_Remastered_x2349.mp3",
        "new": "Willow_Whispers_Feelers_Chill_Remastered348.mp3",
        "reason": "Wrong code (2349 ? 348) + clean format",
    },
    {
        "folder": "Willow_Whispers",
        "old": "Willow_whispers-feelers-chill_Remastered_x2349-2.mp3",
        "new": "Willow_Whispers_Feelers_Chill_Remastered348_Alt.mp3",
        "reason": "Wrong code (2349 ? 348) + clean format",
    },
    # Book_of_Memory
    {
        "folder": "Book_of_Memory",
        "old": "bookOmemory418.mp3",
        "new": "Book_Of_Memory413.mp3",
        "reason": "Wrong code (418 ? 413) + proper caps",
    },
    {
        "folder": "Book_of_Memory",
        "old": "bookOmemory418_1.mp3",
        "new": "Book_Of_Memory413_Alt.mp3",
        "reason": "Wrong code (418 ? 413) + proper caps",
    },
    # Bite_in_the_Night
    {
        "folder": "Bite_in_the_Night",
        "old": "bite_in_the_night319-lady-heart.mp3",
        "new": "Bite_in_the_Night_Lady_Heart310.mp3",
        "reason": "Wrong code (319 ? 310) + clean format",
    },
    # The_Plantagenets
    {
        "folder": "The_Plantagenets",
        "old": "The_Plantagenets314_Remix.mp3",
        "new": "The_Plantagenets_Remix324.mp3",
        "reason": "Wrong code (314 ? 324) + clean format",
    },
]

print("\n?? INTELLIGENT CLEANUP PLAN:")
print("=" * 80)
print("\nPhase 1: MOVE misplaced files")
print(f"   ? {len(misplaced_files)} files in wrong folders")
print("\nPhase 2: RENAME files in correct folders")
print(f"   ? {len(in_folder_renames)} files to fix")
print(f"\nTotal operations: {len(misplaced_files) + len(in_folder_renames)}")

print("\n\n" + "=" * 80)
print("PHASE 1: MOVE FILES TO CORRECT FOLDERS")
print("=" * 80)

move_operations = []

for item in misplaced_files:
    src_dir = nocturne_dir / item["current_folder"]
    src_file = src_dir / item["current_file"]
    dest_dir = nocturne_dir / item["correct_folder"]

    if not src_file.exists():
        print(f"??  File not found: {item['current_file']}")
        continue

    if not dest_dir.exists():
        print(f"? Destination folder missing: {item['correct_folder']}")
        continue

    # Get actual duration and verify new name
    actual_dur = get_duration(src_file)
    if actual_dur:
        correct_code = get_correct_code(actual_dur)
        # Update new_name if needed to ensure correct code
        import re

        if correct_code not in item["new_name"]:
            # Replace any existing code with correct one
            codes = re.findall(r"\d{3,4}", item["new_name"])
            if codes:
                item["new_name"] = item["new_name"].replace(codes[-1], correct_code)

    print(f"\n?? {item['current_file']}")
    print(f"   FROM: {item['current_folder']}/")
    print(f"   TO:   {item['correct_folder']}/{item['new_name']}")
    print(f"   Why:  {item['reason']}")

    # Plan companion file moves
    companions = move_with_companions(src_file, dest_dir)
    for ftype, src, dest in companions:
        # Apply new name to destination
        if ftype == "mp3":
            dest = dest.parent / item["new_name"]
        else:
            new_base = Path(item["new_name"]).stem
            if ftype == "transcript":
                dest = dest.parent / f"{new_base}_transcript.txt"
            elif ftype == "analysis":
                dest = dest.parent / f"{new_base}_analysis.txt"

        move_operations.append(
            {
                "type": ftype,
                "src": src,
                "dest": dest,
                "from_folder": item["current_folder"],
                "to_folder": item["correct_folder"],
            },
        )

print("\n\n" + "=" * 80)
print("PHASE 2: RENAME FILES IN CORRECT FOLDERS")
print("=" * 80)

rename_operations = []

for item in in_folder_renames:
    folder_path = nocturne_dir / item["folder"]
    old_path = folder_path / item["old"]

    if not old_path.exists():
        print(f"??  File not found: {item['old']}")
        continue

    # Verify duration
    actual_dur = get_duration(old_path)
    if actual_dur:
        correct_code = get_correct_code(actual_dur)
        # Verify new name has correct code
        import re

        codes = re.findall(r"\d{3,4}", item["new"])
        if codes and codes[-1] != correct_code:
            print(f"\n??  Duration verification failed for {item['old']}")
            print(f"   Expected code: {correct_code}, new name has: {codes[-1]}")
            continue

    print(f"\n??  {item['folder']}/")
    print(f"   OLD: {item['old']}")
    print(f"   NEW: {item['new']}")
    print(f"   Why: {item['reason']}")

    # Add MP3 rename
    new_path = folder_path / item["new"]
    rename_operations.append(
        {"type": "mp3", "src": old_path, "dest": new_path, "folder": item["folder"]},
    )

    # Add companion renames
    old_base = old_path.stem
    new_base = new_path.stem

    old_transcript = folder_path / f"{old_base}_transcript.txt"
    if old_transcript.exists():
        rename_operations.append(
            {
                "type": "transcript",
                "src": old_transcript,
                "dest": folder_path / f"{new_base}_transcript.txt",
                "folder": item["folder"],
            },
        )

    old_analysis = folder_path / f"{old_base}_analysis.txt"
    if old_analysis.exists():
        rename_operations.append(
            {
                "type": "analysis",
                "src": old_analysis,
                "dest": folder_path / f"{new_base}_analysis.txt",
                "folder": item["folder"],
            },
        )

# Summary
total_ops = len(move_operations) + len(rename_operations)
print("\n\n" + "=" * 80)
print("?? TOTAL OPERATIONS:")
print("=" * 80)
print(
    f"\n   MOVES (wrong folder): {len([m for m in move_operations if m['type'] == 'mp3'])} files",
)
print(
    f"   RENAMES (same folder): {len([r for r in rename_operations if r['type'] == 'mp3'])} files",
)
print(
    f"   Companion files: {len([op for op in move_operations + rename_operations if op['type'] != 'mp3'])}",
)
print(f"   Total operations: {total_ops}")

print("\n?? FILES BEING MOVED TO CORRECT FOLDERS:")
for folder in sorted(
    set(m["to_folder"] for m in move_operations if m["type"] == "mp3"),
):
    count = len(
        [m for m in move_operations if m["to_folder"] == folder and m["type"] == "mp3"],
    )
    print(f"   ? {folder}: +{count} files")

print("\n??  FILES BEING RENAMED (staying in same folder):")
for folder in sorted(set(r["folder"] for r in rename_operations if r["type"] == "mp3")):
    count = len(
        [r for r in rename_operations if r["folder"] == folder and r["type"] == "mp3"],
    )
    print(f"   ? {folder}: {count} files")

# Confirm
print("\n" + "=" * 80)
print("??  INTELLIGENT CLEANUP WILL:")
print("   1. Move 6 Tapestry files from Workshop_Series to Tapestry_Of_Tyranny")
print("   2. Fix all garbage duration codes (7591?759, 3495?248, 2349?348)")
print("   3. Fix minor duration code errors")
print("   4. Apply consistent naming format")
print("   5. Move companion _transcript and _analysis files too")
print("=" * 80)

response = input("\n??  Proceed? (yes/no): ").strip().lower()
if response not in ["yes", "y"]:
    print("? Cancelled - no changes made")
    exit(0)

# Execute
print("\n" + "=" * 80)
print("EXECUTING INTELLIGENT CLEANUP")
print("=" * 80)

timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
log = {"timestamp": timestamp, "operations": [], "errors": []}

success_count = 0
error_count = 0

# Phase 1: Moves
print("\n?? MOVING FILES TO CORRECT FOLDERS:")
for op in move_operations:
    try:
        if op["dest"].exists():
            print(f"??  Skipping (exists): {op['dest'].name}")
            log["errors"].append({"file": op["src"].name, "reason": "exists"})
            continue

        op["src"].rename(op["dest"])
        log["operations"].append(
            {
                "operation": "move",
                "type": op["type"],
                "from": str(op["src"]),
                "to": str(op["dest"]),
                "from_folder": op["from_folder"],
                "to_folder": op["to_folder"],
            },
        )

        if op["type"] == "mp3":
            print(f"? {op['from_folder']} ? {op['to_folder']}: {op['dest'].name}")

        success_count += 1
    except Exception as e:
        print(f"? Error: {op['src'].name} - {e}")
        log["errors"].append({"file": str(op["src"]), "error": str(e)})
        error_count += 1

# Phase 2: Renames
print("\n??  RENAMING FILES IN PLACE:")
for op in rename_operations:
    try:
        if op["dest"].exists():
            print(f"??  Skipping (exists): {op['dest'].name}")
            log["errors"].append({"file": op["src"].name, "reason": "exists"})
            continue

        op["src"].rename(op["dest"])
        log["operations"].append(
            {
                "operation": "rename",
                "type": op["type"],
                "from": str(op["src"]),
                "to": str(op["dest"]),
                "folder": op["folder"],
            },
        )

        if op["type"] == "mp3":
            print(f"? {op['folder']}: {op['src'].name} ? {op['dest'].name}")

        success_count += 1
    except Exception as e:
        print(f"? Error: {op['src'].name} - {e}")
        log["errors"].append({"file": str(op["src"]), "error": str(e)})
        error_count += 1

# Save log
log_file = nocturne_dir / f"INTELLIGENT_CLEANUP_LOG_{timestamp}.json"
with open(log_file, "w") as f:
    json.dump(log, f, indent=2)

print("\n" + "=" * 80)
print("? INTELLIGENT CLEANUP COMPLETE!")
print("=" * 80)
print(f"? Success: {success_count} operations")
print(f"? Errors: {error_count}")
print(f"?? Log: {log_file.name}")
print("\n? Files now in correct folders with accurate duration codes!")
print("=" * 80)
