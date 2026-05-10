#!/usr/bin/env python3
"""from datetime import datetime
from pathlib import Path
import csv
import os
import shutil
Standardize folder names and clean up loose files in root directory.
"""

MUSIC_DIR = Path("/Users/steven/Music/nocTurneMeLoDieS")
LOG_FILE = (
    MUSIC_DIR
    / "DATA"
    / f"folder_standardization_log_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
)

# Folder renames
FOLDER_RENAMES = {
    "Feather Fang Spirit Sang": "Feather_Fang_Spirit_Sang",
    "Heartbeats_in_the_Dark2_Remastered_1": "Heartbeats_in_the_Dark2_Remastered",
    "Kings and Queens of Litter": "Kings_and_Queens_of_Litter",
    "PeTals": "Petals",
    "Sammy's Moonlit Blues": "Sammys_Moonlit_Blues",
    "bookOmemory": "Book_of_Memory",
    "in This aLLey Where i HiDe": "In_This_Alley_Where_I_Hide",
}


def create_singles_folder():
    """Ensure Singles folder exists."""
    singles_folder = MUSIC_DIR / "Singles"
    singles_folder.mkdir(exist_ok=True)
    return singles_folder


def move_loose_mp3s():
    """Move loose MP3 files from root to Singles folder."""
    singles_folder = create_singles_folder()
    moved_files = []

    # Find all MP3s in root
    root_mp3s = list(MUSIC_DIR.glob("*.mp3")) + list(MUSIC_DIR.glob("*.MP3"))

    for mp3_file in root_mp3s:
        try:
            destination = singles_folder / mp3_file.name

            # If file already exists in Singles, rename with suffix
            if destination.exists():
                base = destination.stem
                ext = destination.suffix
                counter = 1
                while destination.exists():
                    destination = singles_folder / f"{base}_{counter}{ext}"
                    counter += 1

            shutil.move(str(mp3_file), str(destination))
            moved_files.append(
                {
                    "type": "file_move",
                    "original": str(mp3_file.relative_to(MUSIC_DIR)),
                    "new": str(destination.relative_to(MUSIC_DIR)),
                    "status": "SUCCESS",
                },
            )
            print(f"  Moved: {mp3_file.name} ? Singles/")

        except Exception as e:
            moved_files.append(
                {
                    "type": "file_move",
                    "original": str(mp3_file.relative_to(MUSIC_DIR)),
                    "new": "",
                    "status": f"ERROR: {e}",
                },
            )
            print(f"  Error moving {mp3_file.name}: {e}")

    return moved_files


def rename_folders():
    """Rename folders to standardized names."""
    renamed_folders = []

    for old_name, new_name in FOLDER_RENAMES.items():
        old_path = MUSIC_DIR / old_name
        new_path = MUSIC_DIR / new_name

        if not old_path.exists():
            print(f"  Skip: {old_name} (doesn't exist)")
            renamed_folders.append(
                {
                    "type": "folder_rename",
                    "original": old_name,
                    "new": new_name,
                    "status": "SKIPPED (not found)",
                },
            )
            continue

        if new_path.exists():
            print(f"  Skip: {old_name} (target already exists: {new_name})")
            renamed_folders.append(
                {
                    "type": "folder_rename",
                    "original": old_name,
                    "new": new_name,
                    "status": "SKIPPED (target exists)",
                },
            )
            continue

        try:
            old_path.rename(new_path)
            renamed_folders.append(
                {
                    "type": "folder_rename",
                    "original": old_name,
                    "new": new_name,
                    "status": "SUCCESS",
                },
            )
            print(f"  ? Renamed: {old_name} ? {new_name}")

        except Exception as e:
            renamed_folders.append(
                {
                    "type": "folder_rename",
                    "original": old_name,
                    "new": new_name,
                    "status": f"ERROR: {e}",
                },
            )
            print(f"  ? Error renaming {old_name}: {e}")

    return renamed_folders


def main():
    print("=" * 80)
    print("FOLDER STANDARDIZATION & ROOT CLEANUP")
    print("=" * 80)
    print()

    all_changes = []

    # Step 1: Move loose MP3s to Singles
    print("STEP 1: Moving loose MP3 files to Singles/")
    print("-" * 80)
    moved_files = move_loose_mp3s()
    all_changes.extend(moved_files)
    print(f"? Moved {len(moved_files)} files to Singles/\n")

    # Step 2: Rename folders
    print("STEP 2: Standardizing folder names")
    print("-" * 80)
    renamed_folders = rename_folders()
    all_changes.extend(renamed_folders)
    print(
        f"? Renamed {len([r for r in renamed_folders if r['status'] == 'SUCCESS'])} folders\n",
    )

    # Save log
    if all_changes:
        LOG_FILE.parent.mkdir(exist_ok=True)
        with open(LOG_FILE, "w", encoding="utf-8", newline="") as f:
            fieldnames = ["type", "original", "new", "status"]
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(all_changes)

        print(f"Log saved to: {LOG_FILE.relative_to(MUSIC_DIR)}")

    # Summary
    print("\n" + "=" * 80)
    print("SUMMARY")
    print("=" * 80)

    file_moves = [c for c in all_changes if c["type"] == "file_move"]
    folder_renames = [c for c in all_changes if c["type"] == "folder_rename"]

    successful_moves = len([f for f in file_moves if f["status"] == "SUCCESS"])
    successful_renames = len([f for f in folder_renames if f["status"] == "SUCCESS"])

    print(f"Files moved to Singles/: {successful_moves}")
    print(f"Folders renamed: {successful_renames}")
    print(f"Total changes: {successful_moves + successful_renames}")
    print()
    print("? Standardization complete!")

    if successful_renames > 0:
        print(
            "\n? IMPORTANT: You should now regenerate the master catalog to reflect new folder names.",
        )
        print("   Run: python3 SCRIPTS/create_enhanced_master_catalog.py")


if __name__ == "__main__":
    main()
