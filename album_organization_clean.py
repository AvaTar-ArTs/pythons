#!/usr/bin/env python3
"""
Music Collection Album Organizer
Groups similar-titled MP3s into album-based collections
"""

import csv
import re
import shutil
import unicodedata
from collections import defaultdict
from pathlib import Path


def normalize_title(title):
    """Normalize title for comparison purposes"""
    # Remove file extension
    if title.lower().endswith(".mp3"):
        title = title[:-4]

    # Convert to lowercase and normalize unicode
    title = title.lower()
    title = unicodedata.normalize("NFKD", title)

    # Remove common version indicators and extra info
    title = re.sub(r"\([^)]*\)", "", title)  # Remove parentheses content
    title = re.sub(r"\[[^\]]*\]", "", title)  # Remove brackets content

    # Remove version numbers and common descriptors
    title = re.sub(r"v\d+", "", title)
    title = re.sub(r"_?\d+(_\d+)?$", "", title)  # Remove trailing numbers
    title = re.sub(r"_remaster(ed|ing)?", "", title)
    title = re.sub(r"_?live", "", title)
    title = re.sub(r"_acoustic", "", title)
    title = re.sub(r"_instrumental", "", title)
    title = re.sub(r"_demo", "", title)
    title = re.sub(r"_edit", "", title)
    title = re.sub(r"_remix", "", title)
    title = re.sub(r"_cut", "", title)
    title = re.sub(r"_og", "", title)
    title = re.sub(r"_best", "", title)
    title = re.sub(r"_stadium", "", title)
    title = re.sub(r"_lady", "", title)
    title = re.sub(r"_feelers?", "", title)
    title = re.sub(r"_chill", "", title)
    title = re.sub(r"_feels?", "", title)
    title = re.sub(r"_indie", "", title)
    title = re.sub(r"_folk", "", title)
    title = re.sub(r"_trashy", "", title)
    title = re.sub(r"_scraps?", "", title)
    title = re.sub(r"_symphony", "", title)
    title = re.sub(r"_junkyard", "", title)
    title = re.sub(r"_alley", "", title)
    title = re.sub(r"_love", "", title)
    title = re.sub(r"_willow", "", title)
    title = re.sub(r"_heroes?", "", title)
    title = re.sub(r"_rise", "", title)
    title = re.sub(r"_villains?", "", title)
    title = re.sub(r"_overthrow", "", title)

    # Clean up special characters and spaces
    title = re.sub(r"[-_]+", " ", title)
    title = re.sub(r"\s+", " ", title)
    title = title.strip()

    return title


def group_files_by_normalized_title(source_dir):
    """Group files by their normalized titles"""
    groups = defaultdict(list)

    # Walk through source directory to find all MP3 files
    for mp3_file in Path(source_dir).rglob("*.mp3"):
        normalized_title = normalize_title(mp3_file.name)
        groups[normalized_title].append(mp3_file)

    return groups


def main():
    # Define source and target directories
    source_directory = "/Users/steven/Music/nocTurneMeLoDieS"
    target_directory = "/Users/steven/Music/nocTurneMeLoDieS/MUSIC_ALBUMS_ORGANIZED"

    print("Starting music collection organization...")

    # Create target directories
    major_dir = Path(target_directory) / "MAJOR_COLLECTIONS"
    medium_dir = Path(target_directory) / "MEDIUM_COLLECTIONS"
    small_dir = Path(target_directory) / "SMALL_COLLECTIONS"
    single_dir = Path(target_directory) / "SINGLE_TRACKS"
    support_dir = Path(target_directory) / "SUPPORTING_CONTENT"

    for dir_path in [major_dir, medium_dir, small_dir, single_dir, support_dir]:
        dir_path.mkdir(parents=True, exist_ok=True)

    # Create supporting content subdirectories
    (support_dir / "COVER_ART").mkdir(exist_ok=True)
    (support_dir / "LYRICS").mkdir(exist_ok=True)
    (support_dir / "ANALYSIS").mkdir(exist_ok=True)
    (support_dir / "TRANSCRIPTS").mkdir(exist_ok=True)

    # Group files by normalized title
    file_groups = group_files_by_normalized_title(source_directory)

    # Count total files and groups
    total_files = sum(len(files) for files in file_groups.values())
    print(f"Found {total_files} MP3 files in {len(file_groups)} groups")

    # Process each group
    major_count = 0
    medium_count = 0
    small_count = 0
    single_count = 0

    mapping_log = {}  # Track file movements

    for normalized_title, files in file_groups.items():
        if len(files) >= 20:
            # Major collection (20+ variations)
            album_dir = major_dir / normalized_title.upper().replace(" ", "_")
            major_count += 1
        elif len(files) >= 5:
            # Medium collection (5-19 variations)
            album_dir = medium_dir / normalized_title.upper().replace(" ", "_")
            medium_count += 1
        elif len(files) > 1:
            # Small collection (2-4 variations)
            album_dir = small_dir / normalized_title.upper().replace(" ", "_")
            small_count += 1
        else:
            # Single track
            album_dir = single_dir
            single_count += 1

        # Create album directory if it's a collection
        if len(files) > 1:
            album_dir.mkdir(exist_ok=True)

        # Move/copy each file to its album directory
        for file_path in files:
            # For collections, create a standardized filename
            if len(files) > 1:
                # Create standardized filename based on original
                original_stem = file_path.stem
                original_suffix = file_path.suffix

                # Clean up the filename to make it more standard
                standardized = re.sub(r"[-_]+", "_", original_stem)  # Standardize separators
                standardized = standardized.strip("_")  # Remove leading/trailing separators

                # Add descriptive suffixes based on original indicators
                original_lower = original_stem.lower()
                suffix_parts = []

                if "live" in original_lower:
                    suffix_parts.append("LIVE")
                if "remix" in original_lower:
                    suffix_parts.append("REMIX")
                if "remaster" in original_lower:
                    suffix_parts.append("REMASTERED")
                if "acoustic" in original_lower:
                    suffix_parts.append("ACOUSTIC")
                if "instrumental" in original_lower:
                    suffix_parts.append("INSTRUMENTAL")
                if "demo" in original_lower:
                    suffix_parts.append("DEMO")
                if "v4" in original_lower or "v5" in original_lower:
                    # Extract version number
                    version_match = re.search(r"v(\d+)", original_lower)
                    if version_match:
                        suffix_parts.append(f"VERSION_{version_match.group(1)}")

                if suffix_parts:
                    standardized += "_" + "_".join(suffix_parts)

                # Create final filename
                standard_name = f"{standardized}{original_suffix}"

                # Handle potential filename conflicts in the same album
                target_path = album_dir / standard_name
                counter = 1
                while target_path.exists():
                    name_part = standard_name.rsplit(".", 1)[0]
                    ext_part = standard_name.rsplit(".", 1)[1]
                    target_path = album_dir / f"{name_part}_{counter}.{ext_part}"
                    counter += 1
            else:
                # For single tracks, keep original name but move to single tracks directory
                target_path = single_dir / file_path.name

            # Copy file to new location
            shutil.copy2(file_path, target_path)

            # Log the mapping
            mapping_log[str(file_path)] = str(target_path)

    print("\nOrganization completed!")
    print(f"- Major collections (20+ variations): {major_count}")
    print(f"- Medium collections (5-19 variations): {medium_count}")
    print(f"- Small collections (2-4 variations): {small_count}")
    print(f"- Single tracks: {single_count}")
    print(f"\nNew organization created at: {target_directory}")

    # Save mapping log
    mapping_file = Path(target_directory) / "original_to_new_mapping.csv"
    with open(mapping_file, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["Original_Path", "New_Path"])
        for orig, new in mapping_log.items():
            writer.writerow([orig, new])

    print(f"Mapping log saved to: {mapping_file}")


if __name__ == "__main__":
    main()
