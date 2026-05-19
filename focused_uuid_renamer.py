#!/usr/bin/env python3
"""
Focused script to rename UUID-named directories and files to proper song titles
using the metadata from the SUNO CSV file.
"""

import os
import re
from pathlib import Path


def parse_suno_csv_for_mappings(csv_file_path):
    """
    Parse the SUNO CSV file to extract UUID to title mappings.
    Focus on the specific format: UUID,,,,title,,,,,,,,
    """
    uuid_mapping = {}

    with open(csv_file_path, encoding="utf-8") as file:
        content = file.read()

    # Split content into lines
    lines = content.split("\n")

    # Pattern to match: UUID followed by 4 commas and then a title
    # Example: 01bbae67-5f8f-4285-8926-24545afe184e,,,,stitch by stitch4,,,,,,,
    for line in lines:
        if not line.strip():
            continue

        # Match UUID followed by 4 commas and then a title (non-greedy)
        pattern = r'([a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12}),*?,*?,*?,*?([^,\n"]+?)(?:,|$)'
        matches = re.findall(pattern, line, re.IGNORECASE)

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

    # Also try a more specific pattern for the exact format seen in the grep results
    for line in lines:
        if not line.strip():
            continue

        # More specific pattern: UUID,,,,title, (where title is not empty and not a URL)
        pattern = r'([a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12}),,,,([^,\n"]+?),(?:,|$)'
        matches = re.findall(pattern, line, re.IGNORECASE)

        for uuid, title_candidate in matches:
            # Clean up the title candidate
            title_candidate = re.sub(r'^"|"$', "", title_candidate.strip())
            title_candidate = re.sub(r"^\'|\'$", "", title_candidate.strip())

            # Only add if it looks like a real title
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


def rename_uuid_directories_and_files(root_dir, uuid_mapping):
    """
    Rename directories and files with UUID names to proper titles.
    """
    renamed_items = []

    # Process directories first
    for item in Path(root_dir).iterdir():
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

    # Process files in all subdirectories
    for root, dirs, files in os.walk(root_dir):
        for file in files:
            if file.lower().endswith((".mp3", ".wav", ".flac", ".m4a")):
                # Check if the filename looks like a UUID (with hyphens)
                uuid_pattern = r"^[a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12}"

                if re.match(uuid_pattern, file.lower()):
                    # Extract the UUID part (before any extension or additional text)
                    uuid_match = re.match(
                        r"^([a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12})",
                        file.lower(),
                    )

                    if uuid_match:
                        uuid_part = uuid_match.group(1)

                        if uuid_part in uuid_mapping:
                            # Get the proper title and preserve the file extension
                            proper_title = uuid_mapping[uuid_part]
                            file_ext = os.path.splitext(file)[1]

                            new_filename = f"{proper_title}{file_ext}"

                            # Handle duplicate names by appending a number
                            old_path = Path(root) / file
                            new_path = Path(root) / new_filename
                            counter = 1
                            while new_path.exists():
                                new_path = Path(root) / f"{proper_title}_{counter}{file_ext}"
                                counter += 1

                            # Perform the rename
                            try:
                                old_path.rename(new_path)
                                print(f"Renamed file: '{file}' -> '{new_path.name}'")
                                renamed_items.append((str(old_path), str(new_path), "file"))
                            except OSError as e:
                                print(f"Failed to rename file '{file}': {e}")
                        else:
                            print(f"No mapping found for UUID file: {file}")

    return renamed_items


def main():
    # Define paths
    csv_file_path = "/Users/steven/Music/nocTurneMeLoDieS/DATA/CSV/suno-csv/SUNO_ULTIMATE_MASTER_20251226_101830.csv"
    music_root_dir = "/Users/steven/Music/nocTurneMeLoDieS/MUSIC_ORGANIZED"

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

    # Rename directories and files with UUID names
    print("\nRenaming UUID-named directories and files...")
    renamed_items = rename_uuid_directories_and_files(music_root_dir, uuid_mapping)

    # Summary
    dir_count = sum(1 for item in renamed_items if item[2] == "directory")
    file_count = sum(1 for item in renamed_items if item[2] == "file")

    print("\nSummary:")
    print(f"- Renamed {dir_count} directories")
    print(f"- Renamed {file_count} files")

    print("\nProcess completed!")


if __name__ == "__main__":
    main()
