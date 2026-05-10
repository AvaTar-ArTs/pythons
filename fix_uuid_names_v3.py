#!/usr/bin/env python3
"""
Comprehensive script to rename UUID-named directories and files to proper song titles
using the metadata from the CSV files.
"""

import csv
import os
import re
from pathlib import Path


def load_uuid_mapping(csv_file_path):
    """
    Load UUID to title mapping from CSV file.
    Creates mappings for both hyphen and underscore formats.
    """
    uuid_mapping = {}

    with open(csv_file_path, newline="", encoding="utf-8") as csvfile:
        reader = csv.DictReader(csvfile)

        for row in reader:
            # Extract UUID from id column
            uuid = row.get("id", "").strip()

            # Extract title from title column
            title = row.get("title", "").strip()

            # Extract mp3_filename if available
            mp3_filename = row.get("mp3_filename", "").strip()

            if uuid and (title or mp3_filename):
                # Clean up the title to make it filesystem-friendly
                clean_title = sanitize_filename(title if title else mp3_filename.replace(".mp3", ""))

                # Store the UUID with hyphens
                uuid_mapping[uuid.lower()] = clean_title

                # Also store the underscore version of the UUID (used in directory names)
                underscore_uuid = uuid.lower().replace("-", "_")
                uuid_mapping[underscore_uuid] = clean_title

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


def rename_uuid_directories(root_dir, uuid_mapping):
    """
    Rename directories with UUID names to proper titles.
    """
    renamed_dirs = []

    for item in Path(root_dir).iterdir():
        if item.is_dir():
            dir_name = item.name

            # Check if the directory name looks like a UUID (with underscores or hyphens)
            uuid_pattern = r"^[a-f0-9]{8}[_-][a-f0-9]{4}[_-][a-f0-9]{4}[_-][a-f0-9]{4}[_-][a-f0-9]{12}$"

            if re.match(uuid_pattern, dir_name.lower()):
                # Normalize the directory name to lowercase
                lookup_key = dir_name.lower()

                # Try to find a match in the mapping
                if lookup_key in uuid_mapping:
                    new_name = uuid_mapping[lookup_key]
                else:
                    # If not found, try converting underscores to hyphens
                    lookup_key_hyphen = dir_name.lower().replace("_", "-")
                    if lookup_key_hyphen in uuid_mapping:
                        new_name = uuid_mapping[lookup_key_hyphen]
                    elif lookup_key.replace("-", "_") in uuid_mapping:
                        new_name = uuid_mapping[lookup_key.replace("-", "_")]
                    else:
                        print(f"No mapping found for UUID directory: {dir_name}")
                        continue

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
                    renamed_dirs.append((str(item), str(new_path)))
                except OSError as e:
                    print(f"Failed to rename directory '{item.name}': {e}")

    return renamed_dirs


def rename_uuid_files(root_dir, uuid_mapping):
    """
    Rename files with UUID names to proper titles.
    """
    renamed_files = []

    # Walk through all subdirectories
    for root, dirs, files in os.walk(root_dir):
        for file in files:
            if file.lower().endswith((".mp3", ".wav", ".flac", ".m4a")):
                # Check if the filename looks like a UUID
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
                                renamed_files.append((str(old_path), str(new_path)))
                            except OSError as e:
                                print(f"Failed to rename file '{file}': {e}")
                        else:
                            print(f"No mapping found for UUID file: {file}")

    return renamed_files


def main():
    # Define paths
    csv_file_path = "/Users/steven/Music/nocTurneMeLoDieS/DATA/CSV/NOCTURNEMELODIES_ULTIMATE_MASTER.csv"
    music_root_dir = "/Users/steven/Music/nocTurneMeLoDieS/MUSIC_ORGANIZED"

    # Check if CSV file exists
    if not os.path.exists(csv_file_path):
        print(f"CSV file not found: {csv_file_path}")
        return

    # Load UUID to title mapping
    print("Loading UUID to title mapping...")
    uuid_mapping = load_uuid_mapping(csv_file_path)
    print(f"Loaded {len(uuid_mapping)} UUID mappings")

    # Rename directories with UUID names
    print("\nRenaming UUID-named directories...")
    renamed_dirs = rename_uuid_directories(music_root_dir, uuid_mapping)

    # Rename files with UUID names
    print("\nRenaming UUID-named files...")
    renamed_files = rename_uuid_files(music_root_dir, uuid_mapping)

    # Summary
    print("\nSummary:")
    print(f"- Renamed {len(renamed_dirs)} directories")
    print(f"- Renamed {len(renamed_files)} files")

    print("\nProcess completed!")


if __name__ == "__main__":
    main()
