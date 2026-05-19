#!/usr/bin/env python3
"""
Focused Album-Based Organization for nocTurneMeLoDieS
Moves content to album-based structure where each album contains all versions of the same song
"""

import re
import shutil
from pathlib import Path


def create_album_structure():
    """Create the album-based organizational structure"""
    base_path = Path("/Users/steven/Music/nocTurneMeLoDieS")

    # Create main album directory
    album_dir = base_path / "ALBUMS_FOCUSSED"
    album_dir.mkdir(exist_ok=True)

    # Create album directories for main collections
    album_subdirs = [
        "Bite_In_The_Night",
        "In_This_Alley_Where_I_Hide",
        "Willow_Whispers",
        "Summer_Love",
        "Heroes_Rise_Villains_Overthrow",
        "Junkyard_Symphony",
        "Beautiful_Mess",
        "Echoes_of_Yesterday",
        "The_Sound_of_Ancestors",
        "Sammys_Serenade",
        "Witches_Road",
        "Love_is_Rubbish",
        "From_Ashes_I_Will_Rise",
        "Dusty_Rhymes",
        "Enchanted_Woods_Song_Adventure",
        "Heartbeats_in_the_Dark",
        "Love_in_Imperfection",
        "Petals_Fall",
        "Chamber_of_Silence",
        "The_Enchanted_Children",
        "The_Jungle_Shaman",
        "The_Names_of_God",
        "The_Patchwork_Prophecy",
        "The_Seven_Work_Refusals",
        "The_Shadow",
        "The_Soul_Below",
        "The_Spirits_Are_Near",
        "There's_A_Feeling",
        "Think_Spoken",
        "Thinketh",
        "Threaded_Through_The_Veil",
        "Touch_of_a_Calming_Night",
        "Trinity",
        "Unbroken_Stars",
        "Vine_of_the_Void",
        "Wasting_Time",
        "What_The_Stars_See",
        "Where_I'm_Redeemed",
        "Where_Shadows_Play",
        "Witches_Road",
        "Workshop_Worries",
        "All_Other_Albums",
    ]

    for subdir in album_subdirs:
        (album_dir / subdir).mkdir(exist_ok=True)

    print(f"Created album structure in: {album_dir}")
    return album_dir


def normalize_album_name(name):
    """Normalize album names to identify the same album across different versions"""
    # Remove file extensions and common version indicators
    if name.lower().endswith((".mp3", ".wav", ".flac", ".m4a")):
        name = Path(name).stem

    # Remove version numbers and common descriptors
    name = re.sub(r"v\d+", "", name, flags=re.IGNORECASE)
    name = re.sub(r"_?\d+(_\d+)?$", "", name)  # Remove trailing numbers
    name = re.sub(r"_remaster(ed|ing)?", "", name, flags=re.IGNORECASE)
    name = re.sub(r"_?live", "", name, flags=re.IGNORECASE)
    name = re.sub(r"_acoustic", "", name, flags=re.IGNORECASE)
    name = re.sub(r"_instrumental", "", name, flags=re.IGNORECASE)
    name = re.sub(r"_demo", "", name, flags=re.IGNORECASE)
    name = re.sub(r"_edit", "", name, flags=re.IGNORECASE)
    name = re.sub(r"_remix", "", name, flags=re.IGNORECASE)
    name = re.sub(r"_cut", "", name, flags=re.IGNORECASE)
    name = re.sub(r"_og", "", name, flags=re.IGNORECASE)
    name = re.sub(r"_best", "", name, flags=re.IGNORECASE)
    name = re.sub(r"_stadium", "", name, flags=re.IGNORECASE)
    name = re.sub(r"_lady", "", name, flags=re.IGNORECASE)
    name = re.sub(r"_feelers?", "", name, flags=re.IGNORECASE)
    name = re.sub(r"_chill", "", name, flags=re.IGNORECASE)
    name = re.sub(r"_feels?", "", name, flags=re.IGNORECASE)
    name = re.sub(r"_indie", "", name, flags=re.IGNORECASE)
    name = re.sub(r"_folk", "", name, flags=re.IGNORECASE)
    name = re.sub(r"_trashy", "", name, flags=re.IGNORECASE)
    name = re.sub(r"_scraps?", "", name, flags=re.IGNORECASE)
    name = re.sub(r"_symphony", "", name, flags=re.IGNORECASE)
    name = re.sub(r"_junkyard", "", name, flags=re.IGNORECASE)
    name = re.sub(r"_alley", "", name, flags=re.IGNORECASE)
    name = re.sub(r"_love", "", name, flags=re.IGNORECASE)
    name = re.sub(r"_willow", "", name, flags=re.IGNORECASE)
    name = re.sub(r"_heroes?", "", name, flags=re.IGNORECASE)
    name = re.sub(r"_rise", "", name, flags=re.IGNORECASE)
    name = re.sub(r"_villains?", "", name, flags=re.IGNORECASE)
    name = re.sub(r"_overthrow", "", name, flags=re.IGNORECASE)

    # Clean up special characters and spaces
    name = re.sub(r"[-_]+", " ", name)
    name = re.sub(r"\s+", " ", name)
    name = name.strip()

    # Standardize known album names
    name = name.lower()
    if "bite" in name and "night" in name:
        return "Bite_In_The_Night"
    elif "alley" in name and "hide" in name:
        return "In_This_Alley_Where_I_Hide"
    elif "willow" in name and "whisp" in name:
        return "Willow_Whispers"
    elif "summer" in name and "love" in name:
        return "Summer_Love"
    elif "hero" in name and "villain" in name:
        return "Heroes_Rise_Villains_Overthrow"
    elif "junk" in name and "symphony" in name:
        return "Junkyard_Symphony"
    elif "beautiful" in name and "mess" in name:
        return "Beautiful_Mess"
    elif "echoes" in name and "yester" in name:
        return "Echoes_of_Yesterday"
    elif "sound" in name and "ancestor" in name:
        return "The_Sound_of_Ancestors"
    elif "sammy" in name and "serenade" in name:
        return "Sammys_Serenade"
    elif "witch" in name and "road" in name:
        return "Witches_Road"
    elif "love" in name and "rubbish" in name:
        return "Love_is_Rubbish"
    elif "ashes" in name and "rise" in name:
        return "From_Ashes_I_Will_Rise"
    elif "dusty" in name and "rhyme" in name:
        return "Dusty_Rhymes"
    elif "enchanted" in name and "woods" in name:
        return "Enchanted_Woods_Song_Adventure"
    elif "heartbeat" in name and "dark" in name:
        return "Heartbeats_in_the_Dark"
    elif "love" in name and "imperfection" in name:
        return "Love_in_Imperfection"
    elif "petals" in name and "fall" in name:
        return "Petals_Fall"
    elif "chamber" in name and "silence" in name:
        return "Chamber_of_Silence"
    elif "enchanted" in name and "children" in name:
        return "The_Enchanted_Children"
    elif "jungle" in name and "shaman" in name:
        return "The_Jungle_Shaman"
    elif "names" in name and "god" in name:
        return "The_Names_of_God"
    elif "patchwork" in name and "prophecy" in name:
        return "The_Patchwork_Prophecy"
    elif "seven" in name and "work" in name:
        return "The_Seven_Work_Refusals"
    elif "shadow" in name and "the" in name:
        return "The_Shadow"
    elif "soul" in name and "below" in name:
        return "The_Soul_Below"
    elif "spirits" in name and "near" in name:
        return "The_Spirits_Are_Near"
    elif "threaded" in name and "veil" in name:
        return "Threaded_Through_The_Veil"
    elif "touch" in name and "calming" in name:
        return "Touch_of_a_Calming_Night"
    elif "waste" in name and "time" in name:
        return "Wasting_Time"
    elif "stars" in name and "see" in name:
        return "What_The_Stars_See"
    elif "redeem" in name:
        return "Where_I'm_Redeemed"
    elif "shadows" in name and "play" in name:
        return "Where_Shadows_Play"
    elif "workshop" in name and "worries" in name:
        return "Workshop_Worries"
    else:
        # For other cases, clean up the name
        name = re.sub(r"[^\w\s]", " ", name)
        name = re.sub(r"\s+", "_", name.strip())
        return name.title()


def organize_albums():
    """Organize music files into album-based structure"""
    base_path = Path("/Users/steven/Music/nocTurneMeLoDieS")
    album_base_path = create_album_structure()

    # Find all MP3 files
    all_mp3_files = list(base_path.rglob("*.mp3"))

    # Track moved files
    moved_files = 0
    failed_moves = 0

    print(f"Found {len(all_mp3_files)} MP3 files to organize...")

    for mp3_file in all_mp3_files:
        # Skip files already in the new album structure
        if str(album_base_path) in str(mp3_file):
            continue

        # Get the normalized album name from the file
        album_name = normalize_album_name(mp3_file.name)

        # Determine target directory
        target_dir = album_base_path / album_name
        if not target_dir.exists():
            target_dir = album_base_path / "All_Other_Albums"

        # Create target directory if it doesn't exist
        target_dir.mkdir(exist_ok=True)

        # Handle potential filename conflicts
        target_file = target_dir / mp3_file.name
        counter = 1
        while target_file.exists():
            stem = mp3_file.stem
            suffix = mp3_file.suffix
            target_file = target_dir / f"{stem}_{counter}{suffix}"
            counter += 1

        try:
            # Move the file
            shutil.move(str(mp3_file), str(target_file))
            print(f"  Moved: {mp3_file.name} -> {album_name}/")
            moved_files += 1
        except Exception as e:
            print(f"  Failed to move {mp3_file.name}: {str(e)}")
            failed_moves += 1

    # Also move directories that match album names
    all_dirs = [d for d in base_path.iterdir() if d.is_dir() and d.name != "ALBUMS_FOCUSSED"]

    for dir_path in all_dirs:
        # Skip certain system directories
        if dir_path.name in [".git", ".DS_Store", "__pycache__", ".claude"]:
            continue

        # Get the normalized album name from the directory
        album_name = normalize_album_name(dir_path.name)

        # Determine target directory
        target_dir = album_base_path / album_name
        if not target_dir.exists():
            target_dir = album_base_path / "All_Other_Albums"

        # Create target directory if it doesn't exist
        target_dir.mkdir(exist_ok=True)

        # Handle potential directory name conflicts
        target_path = target_dir / dir_path.name
        counter = 1
        while target_path.exists():
            target_path = target_dir / f"{dir_path.name}_{counter}"
            counter += 1

        try:
            # Move the directory
            shutil.move(str(dir_path), str(target_path))
            print(f"  Moved directory: {dir_path.name} -> {album_name}/")
            moved_files += 1
        except Exception as e:
            print(f"  Failed to move directory {dir_path.name}: {str(e)}")
            failed_moves += 1

    print("\nOrganization completed!")
    print(f"- Files moved: {moved_files}")
    print(f"- Failed moves: {failed_moves}")
    print(f"- Album structure created at: {album_base_path}")


if __name__ == "__main__":
    organize_albums()
