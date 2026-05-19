#!/usr/bin/env python3
"""
Focused script to rename UUID-named directories and group related songs
into themed collections using metadata from the SUNO CSV file.
"""

import os
import re
import shutil
from collections import defaultdict
from pathlib import Path


def extract_uuid_to_title_mapping(csv_file_path):
    """
    Extract UUID to title mappings from the CSV file.
    """
    uuid_mapping = {}

    with open(csv_file_path, encoding="utf-8") as file:
        lines = file.readlines()

    # Skip header line and process each row
    for i, line in enumerate(lines[1:], 1):  # Skip header
        if line.strip():
            parts = line.split(",")
            if len(parts) >= 5:
                uuid = parts[0].strip("\"' ")
                title = parts[4].strip("\"' ")  # The Song Name column

                # Validate UUID format
                if re.match(
                    r"^[a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12}$",
                    uuid,
                    re.IGNORECASE,
                ):
                    if title and len(title) > 1 and not title.isdigit():
                        # Sanitize the title for use as a directory name
                        sanitized_title = sanitize_filename(title)
                        uuid_mapping[uuid.lower()] = sanitized_title
                        # Also add the UUID with underscores (how they appear in directory names)
                        uuid_underscore = uuid.lower().replace("-", "_")
                        uuid_mapping[uuid_underscore] = sanitized_title

    return uuid_mapping


def sanitize_filename(filename):
    """
    Sanitize filename to be filesystem-safe.
    """
    if not filename:
        return "Untitled"

    # Remove invalid characters for filesystem
    sanitized = re.sub(r'[<>:"/\\|?*]', "_", filename)

    # Replace special characters and normalize spaces
    # Keep spaces but replace multiple spaces with single underscore
    sanitized = re.sub(r"\s+", "_", sanitized.strip())

    # Remove leading/trailing underscores and dots
    sanitized = sanitized.strip(" _.")

    # Limit length to avoid filesystem issues
    if len(sanitized) > 200:
        sanitized = sanitized[:200]

    return sanitized


def get_song_family_name(title):
    """
    Extract the base song name to group variations together.
    For example: "Bite in the Night", "Bite in the Night (Remastered)", etc. all belong to "Bite in the Night"
    """
    if not title:
        return "Unknown"

    # Common patterns for variations
    variation_patterns = [
        r"\s*\(?(?:remaster|remastered|live|acoustic|instrumental|demo|edit|remix|version|v\d+)\)?",
        r"\s*[-_]\s*(?:remaster|remastered|live|acoustic|instrumental|demo|edit|remix|version|v\d+)",
        r"\s*[-_]\s*\d+m?\s*x?tra?",  # For patterns like "-4m-xtra"
        r"\s*[-_]\s*\d+",  # For patterns like "-322", "-227" (time stamps or version numbers)
        r"\s*[-_]\s*(?:lady|ballade|indie|grunge|pluck|duo)\s*\d*",  # For patterns like "lady_ballade0227"
        r"\s*[-_]\s*\d{3,4}[a-z]?",  # For patterns like "0227", "322", etc.
    ]

    base_title = title.lower()

    # Remove common variation indicators
    for pattern in variation_patterns:
        base_title = re.sub(pattern, "", base_title, flags=re.IGNORECASE)

    # Clean up extra spaces and punctuation
    base_title = re.sub(r"\s+", " ", base_title.strip()).strip()

    # Capitalize appropriately
    base_title = base_title.strip().title()

    # If the base title is too generic or empty, return the original
    if not base_title or base_title in [
        "V",
        "Version",
        "Remix",
        "Remastered",
        "Live",
        "Acoustic",
        "Duo",
        "Edit",
    ]:
        return title.title()

    return base_title


def group_related_songs(uuid_mapping):
    """
    Group related songs by their base song name.
    """
    song_groups = defaultdict(list)

    for uuid, title in uuid_mapping.items():
        base_name = get_song_family_name(title)
        song_groups[base_name].append((uuid, title))

    return song_groups


def process_albums_directory(albums_dir, uuid_mapping, song_groups):
    """
    Process the ALBUMS directory to identify and fix UUID-named directories.
    """
    print("Processing ALBUMS directory...")

    # Find all UUID-named directories in the albums directory
    uuid_dirs = []
    for item in Path(albums_dir).iterdir():
        if item.is_dir():
            dir_name = item.name

            # Check if the directory name looks like a UUID (with underscores)
            uuid_pattern = r"^[a-f0-9]{8}_[a-f0-9]{4}_[a-f0-9]{4}_[a-f0-9]{4}_[a-f0-9]{12}$"

            if re.match(uuid_pattern, dir_name.lower()):
                uuid_dirs.append(item)

    print(f"Found {len(uuid_dirs)} UUID-named directories to process")

    # Process each UUID directory
    processed_count = 0
    for item in uuid_dirs:
        dir_name = item.name
        lookup_key = dir_name.lower()

        if lookup_key in uuid_mapping:
            proper_title = uuid_mapping[lookup_key]
            base_song_name = get_song_family_name(proper_title)

            # Determine the target directory based on grouping
            if len(song_groups.get(base_song_name, [])) > 1:
                # This song has variations, so group it in a themed collection
                target_collection_dir = Path(albums_dir) / base_song_name
            else:
                # This song has no variations, use its proper title as directory
                target_collection_dir = Path(albums_dir) / proper_title

            # Create target collection directory if it doesn't exist
            target_collection_dir.mkdir(exist_ok=True)

            # Create a subdirectory named after the specific version
            target_subdir = target_collection_dir / proper_title

            # Handle duplicate names by appending a number
            counter = 1
            while target_subdir.exists():
                target_subdir = target_collection_dir / f"{proper_title}_{counter}"
                counter += 1

            try:
                # Move the UUID directory to the target location
                shutil.move(str(item), str(target_subdir))

                print(f"Moved: '{item.name}' -> '{target_subdir.relative_to(albums_dir)}'")
                processed_count += 1
            except OSError as e:
                print(f"Failed to move directory '{item.name}': {e}")
        else:
            print(f"No mapping found for UUID directory: {dir_name}")

    print(f"\nProcessed {processed_count} UUID directories")


def process_non_uuid_directories(albums_dir, uuid_mapping, song_groups):
    """
    Process non-UUID directories that might need to be grouped together.
    """
    print("\nProcessing non-UUID directories for grouping...")

    # Group directories by their base song name
    dir_groups = defaultdict(list)

    for item in Path(albums_dir).iterdir():
        if item.is_dir():
            dir_name = item.name

            # Skip if it's a UUID directory (already processed)
            uuid_pattern = r"^[a-f0-9]{8}_[a-f0-9]{4}_[a-f0-9]{4}_[a-f0-9]{4}_[a-f0-9]{12}$"
            if re.match(uuid_pattern, dir_name.lower()):
                continue

            # Get the base song name for grouping
            base_name = get_song_family_name(dir_name)

            # Only group if this base name has multiple versions in our mapping
            if len(song_groups.get(base_name, [])) > 1:
                dir_groups[base_name].append(item)

    print(f"Found {len(dir_groups)} potential song groups to consolidate")

    # Process each group
    consolidated_count = 0
    for base_name, dirs in dir_groups.items():
        if len(dirs) > 1:
            # Create a main collection directory
            collection_dir = Path(albums_dir) / base_name

            # If the collection directory doesn't exist, create it
            if not collection_dir.exists():
                collection_dir.mkdir(exist_ok=True)

            # Move all directories in this group into the collection directory
            for dir_item in dirs:
                if dir_item != collection_dir:  # Don't move the collection dir into itself
                    target_subdir = collection_dir / dir_item.name

                    # Handle duplicates
                    counter = 1
                    while target_subdir.exists():
                        target_subdir = collection_dir / f"{dir_item.name}_{counter}"
                        counter += 1

                    try:
                        if target_subdir != dir_item:
                            shutil.move(str(dir_item), str(target_subdir))
                            print(f"Grouped: '{dir_item.name}' -> '{target_subdir.relative_to(albums_dir)}'")
                            consolidated_count += 1
                    except OSError as e:
                        print(f"Failed to move directory '{dir_item.name}': {e}")

    print(f"Consolidated {consolidated_count} directories into song groups")


def main():
    # Define paths
    albums_dir = "/Users/steven/Music/nocTurneMeLoDieS/MUSIC_ORGANIZED/ALBUMS/"
    csv_file_path = "/Users/steven/Music/nocTurneMeLoDieS/DATA/CSV/suno-csv/SUNO_ULTIMATE_MASTER_20251226_101830.csv"

    # Check if directories exist
    if not os.path.exists(albums_dir):
        print(f"Albums directory not found: {albums_dir}")
        return

    if not os.path.exists(csv_file_path):
        print(f"CSV file not found: {csv_file_path}")
        return

    # Load UUID to title mapping
    print("Loading UUID to title mappings...")
    uuid_mapping = extract_uuid_to_title_mapping(csv_file_path)
    print(f"Loaded {len(uuid_mapping)} UUID mappings")

    # Group related songs
    print("Grouping related songs...")
    song_groups = group_related_songs(uuid_mapping)
    print(f"Created {len(song_groups)} song groups")

    # Show some examples of grouped songs
    print("\nExample song groups with multiple versions:")
    count = 0
    for group_name, songs in song_groups.items():
        if len(songs) > 1:  # Only show groups with multiple songs
            print(f"  {group_name}: {len(songs)} versions")
            for _, title in songs[:3]:  # Show first 3 titles
                print(f"    - {title}")
            if len(songs) > 3:
                print(f"    - ... and {len(songs) - 3} more")
            count += 1
            if count >= 10:  # Limit to 10 examples
                break

    # Process UUID directories first
    process_albums_directory(albums_dir, uuid_mapping, song_groups)

    # Then process non-UUID directories for grouping
    process_non_uuid_directories(albums_dir, uuid_mapping, song_groups)

    print("\nOrganization process completed!")


if __name__ == "__main__":
    main()
