#!/usr/bin/env python3
"""
Focused script to rename UUID-named directories and group related songs
into themed collections using metadata from the SUNO CSV file.
"""

import os
import re
from collections import defaultdict
from pathlib import Path


def extract_uuid_to_title_mapping(csv_file_path):
    """
    Extract UUID to title mappings from the CSV file.
    """
    uuid_mapping = {}

    with open(csv_file_path, encoding="utf-8") as file:
        content = file.read()

    # Pattern to match UUID and title in the CSV
    # Looking for: UUID,,,,title, or similar patterns

    lines = content.split("\n")
    for line in lines:
        # Match UUID at the beginning of the line followed by commas and a title
        match = re.search(r"^([a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12}),", line)
        if match:
            uuid = match.group(1)
            # Extract the title field (typically in the 5th position after splitting by comma)
            parts = line.split(",")
            if len(parts) >= 5:
                title = parts[4].strip("\"' ")
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


def rename_uuid_directories_and_group(root_dir, uuid_mapping, song_groups):
    """
    Rename UUID directories to proper titles and group related songs.
    """
    renamed_items = []

    # First, collect all UUID-named directories
    uuid_dirs = []
    for item in Path(root_dir).iterdir():
        if item.is_dir():
            dir_name = item.name

            # Check if the directory name looks like a UUID (with underscores)
            uuid_pattern = r"^[a-f0-9]{8}_[a-f0-9]{4}_[a-f0-9]{4}_[a-f0-9]{4}_[a-f0-9]{12}$"

            if re.match(uuid_pattern, dir_name.lower()):
                uuid_dirs.append(item)

    # Process each UUID directory
    for item in uuid_dirs:
        dir_name = item.name
        lookup_key = dir_name.lower()

        if lookup_key in uuid_mapping:
            proper_title = uuid_mapping[lookup_key]
            base_song_name = get_song_family_name(proper_title)

            # Determine the target directory based on grouping
            if len(song_groups.get(base_song_name, [])) > 1:
                # This song has variations, so group it in a themed collection
                target_dir = Path(root_dir) / base_song_name
            else:
                # This song has no variations, use its proper title as directory
                target_dir = Path(root_dir) / proper_title

            # Create target directory if it doesn't exist
            target_dir.mkdir(exist_ok=True)

            # Move the entire directory to the target location
            new_path = target_dir / proper_title
            counter = 1
            while new_path.exists():
                new_path = target_dir / f"{proper_title}_{counter}"
                counter += 1

            try:
                # If the target is different from current, move it
                if new_path != item:
                    # If we're moving into a group directory, we might need to handle differently
                    # Just rename the directory within the same parent for now
                    temp_path = item.parent / f"temp_{dir_name}"
                    item.rename(temp_path)

                    # Now rename to the final name
                    temp_path.rename(new_path)

                    print(f"Renamed directory: '{item.name}' -> '{new_path.name}'")
                    renamed_items.append((str(item), str(new_path), "directory"))
            except OSError as e:
                print(f"Failed to rename directory '{item.name}': {e}")
        else:
            print(f"No mapping found for UUID directory: {dir_name}")

    return renamed_items


def process_albums_directory(albums_dir):
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

    # Load UUID to title mapping
    csv_file_path = "/Users/steven/Music/nocTurneMeLoDieS/DATA/CSV/suno-csv/SUNO_ULTIMATE_MASTER_20251226_101830.csv"
    print("Loading UUID to title mappings...")
    uuid_mapping = extract_uuid_to_title_mapping(csv_file_path)
    print(f"Loaded {len(uuid_mapping)} UUID mappings")

    # Group related songs
    print("Grouping related songs...")
    song_groups = group_related_songs(uuid_mapping)
    print(f"Created {len(song_groups)} song groups")

    # Show some examples of grouped songs
    print("\nExample song groups:")
    count = 0
    for group_name, songs in song_groups.items():
        if len(songs) > 1:  # Only show groups with multiple songs
            print(f"  {group_name}: {[title for _, title in songs[:3]]}")  # Show first 3
            count += 1
            if count >= 5:  # Limit to 5 examples
                break

    # Process UUID directories
    renamed_items = rename_uuid_directories_and_group(albums_dir, uuid_mapping, song_groups)

    # Summary
    dir_count = len(renamed_items)

    print("\nSummary:")
    print(f"- Processed {dir_count} UUID directories")

    # Also process any remaining UUID directories that weren't handled
    remaining_uuid_dirs = []
    for item in Path(albums_dir).iterdir():
        if item.is_dir():
            dir_name = item.name
            uuid_pattern = r"^[a-f0-9]{8}_[a-f0-9]{4}_[a-f0-9]{4}_[a-f0-9]{4}_[a-f0-9]{12}$"
            if re.match(uuid_pattern, dir_name.lower()):
                remaining_uuid_dirs.append(item)

    if remaining_uuid_dirs:
        print(f"- Found {len(remaining_uuid_dirs)} remaining UUID directories that could not be mapped")
        for item in remaining_uuid_dirs[:5]:  # Show first 5
            print(f"  - {item.name}")

    print("\nProcess completed!")


def main():
    # Define paths
    albums_dir = "/Users/steven/Music/nocTurneMeLoDieS/MUSIC_ORGANIZED/ALBUMS/"

    # Check if albums directory exists
    if not os.path.exists(albums_dir):
        print(f"Albums directory not found: {albums_dir}")
        return

    # Process the albums directory
    process_albums_directory(albums_dir)


if __name__ == "__main__":
    main()
