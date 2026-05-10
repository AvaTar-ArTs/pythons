#!/usr/bin/env python3
"""
Final script to rename UUID-named directories in ALBUMS to proper song titles
using the metadata from the SUNO CSV file.
"""

import os
import re
from pathlib import Path


def parse_suno_csv_for_mappings(csv_file_path):
    """
    Parse the SUNO CSV file to extract UUID to title mappings.
    Focus on the specific format: UUID,,,,title,
    """
    uuid_mapping = {}

    with open(csv_file_path, encoding="utf-8") as file:
        content = file.read()

    # Pattern to match: UUID followed by exactly 4 commas and then a title
    pattern = r'([a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12}),,,,([^,\n"]+?),(?:,|$)'
    matches = re.findall(pattern, content, re.IGNORECASE)

    for uuid, title_candidate in matches:
        # Clean up the title candidate
        title_candidate = re.sub(r'^"|"$', "", title_candidate.strip())
        title_candidate = re.sub(r"^\'|\'$", "", title_candidate.strip())

        # Only add if it looks like a real title (not a URL, timestamp, or ID)
        if (
            title_candidate
            and len(title_candidate) > 2
            and not title_candidate.startswith("http")
            and not title_candidate.startswith("https")
            and not title_candidate.isdigit()
            and not re.match(r"^[a-f0-9-]{36,}$", title_candidate)
            and not title_candidate.startswith("fetch")
            and not title_candidate.startswith("2025-")
            and not title_candidate.startswith("image_")
            and not title_candidate.endswith(".mp3")
            and not title_candidate.endswith(".jpeg")
            and not title_candidate.endswith(".png")
            and not title_candidate.endswith(".jpg")
            and title_candidate.lower() != "jpeg"
            and title_candidate.lower() != "png"
            and title_candidate.lower() != "jpg"
            and not title_candidate.startswith("Title:")
            and not title_candidate.startswith("Aspect Ratio:")
            and not title_candidate.startswith("https://cdn")
            and not title_candidate.startswith("https://suno.com/s/")
            and not title_candidate.startswith("https://suno.com/song/")
        ):
            clean_title = sanitize_filename(title_candidate)
            uuid_mapping[uuid.lower()] = clean_title
            uuid_mapping[uuid.lower().replace("-", "_")] = clean_title

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


def rename_uuid_directories(albums_dir, uuid_mapping):
    """
    Rename directories with UUID names to proper titles in the ALBUMS directory.
    """
    renamed_items = []

    # Process directories in the albums directory
    for item in Path(albums_dir).iterdir():
        if item.is_dir():
            dir_name = item.name

            # Check if the directory name looks like a UUID (with underscores)
            uuid_pattern = r"^[a-f0-9]{8}_[a-f0-9]{4}_[a-f0-9]{4}_[a-f0-9]{4}_[a-f0-9]{12}$"

            if re.match(uuid_pattern, dir_name.lower()):
                # Normalize the directory name to lowercase
                lookup_key = dir_name.lower()

                # Try to find a match in the mapping
                new_name = None
                if lookup_key in uuid_mapping:
                    new_name = uuid_mapping[lookup_key]
                else:
                    # If not found, try converting underscores to hyphens
                    lookup_key_hyphen = dir_name.lower().replace("_", "-")
                    if lookup_key_hyphen in uuid_mapping:
                        new_name = uuid_mapping[lookup_key_hyphen]
                    elif lookup_key.replace("-", "_") in uuid_mapping:
                        new_name = uuid_mapping[lookup_key.replace("-", "_")]

                if new_name:
                    # Handle duplicate names by appending a number
                    new_path = item.parent / new_name
                    counter = 1
                    while new_path.exists() and new_path != item:
                        new_path = item.parent / f"{new_name}_{counter}"
                        counter += 1

                    # Perform the rename
                    try:
                        item.rename(new_path)
                        print(f"Renamed directory: '{item.name}' -> '{new_path.name}'")
                        renamed_items.append((str(item), str(new_path), "directory"))
                    except OSError as e:
                        print(f"Failed to rename directory '{item.name}': {e}")
                else:
                    print(f"No mapping found for UUID directory: {dir_name}")

    return renamed_items


def main():
    # Define paths
    csv_file_path = "/Users/steven/Music/nocTurneMeLoDieS/DATA/CSV/suno-csv/SUNO_ULTIMATE_MASTER_20251226_101830.csv"
    albums_dir = "/Users/steven/Music/nocTurneMeLoDieS/MUSIC_ORGANIZED/ALBUMS"

    # Check if CSV file exists
    if not os.path.exists(csv_file_path):
        print(f"CSV file not found: {csv_file_path}")
        return

    # Load UUID to title mapping
    print("Parsing CSV file for UUID to title mappings...")
    uuid_mapping = parse_suno_csv_for_mappings(csv_file_path)
    print(f"Loaded {len(uuid_mapping)} UUID mappings")

    # Show some sample mappings
    print("\nSample mappings loaded:")
    count = 0
    for uuid, title in list(uuid_mapping.items())[:5]:  # Show first 5 mappings
        print(f"  {uuid} -> {title}")
        count += 1

    # Rename directories with UUID names
    print(f"\nRenaming UUID-named directories in {albums_dir}...")
    renamed_items = rename_uuid_directories(albums_dir, uuid_mapping)

    # Summary
    dir_count = len(renamed_items)

    print("\nSummary:")
    print(f"- Renamed {dir_count} directories")

    print("\nProcess completed!")


if __name__ == "__main__":
    main()
