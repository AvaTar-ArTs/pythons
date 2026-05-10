#!/usr/bin/env python3
"""
Test script to verify UUID mapping and directory matching
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


def test_uuid_directories_and_files(root_dir, uuid_mapping):
    """
    Test: Check directories and files with UUID names to see if they match mappings.
    """
    print("Testing directories and files for UUID matches...")

    # Process directories first
    for item in Path(root_dir).iterdir():
        if item.is_dir():
            dir_name = item.name

            # Check if the directory name looks like a UUID (with underscores)
            uuid_pattern = r"^[a-f0-9]{8}_[a-f0-9]{4}_[a-f0-9]{4}_[a-f0-9]{4}_[a-f0-9]{12}$"

            if re.match(uuid_pattern, dir_name.lower()):
                print(f"Found UUID directory: {dir_name}")

                # Normalize the directory name to lowercase
                lookup_key = dir_name.lower()

                # Try to find a match in the mapping
                if lookup_key in uuid_mapping:
                    print(f"  -> Found mapping: {uuid_mapping[lookup_key]}")
                else:
                    # If not found, try converting underscores to hyphens
                    lookup_key_hyphen = dir_name.lower().replace("_", "-")
                    if lookup_key_hyphen in uuid_mapping:
                        print(f"  -> Found mapping with hyphens: {uuid_mapping[lookup_key_hyphen]}")
                    elif lookup_key.replace("-", "_") in uuid_mapping:
                        print(f"  -> Found mapping with underscores: {uuid_mapping[lookup_key.replace('-', '_')]}")
                    else:
                        print(f"  -> No mapping found for: {lookup_key}")


def main():
    # Define paths
    csv_file_path = "/Users/steven/Music/nocTurneMeLoDieS/DATA/CSV/suno-csv/SUNO_ULTIMATE_MASTER_20251226_101830.csv"
    music_root_dir = "/Users/steven/Music/nocTurneMeLoDieS/MUSIC_ORGANIZED/ALBUMS"

    # Check if CSV file exists
    if not os.path.exists(csv_file_path):
        print(f"CSV file not found: {csv_file_path}")
        return

    # Load UUID to title mapping
    print("Parsing CSV file for UUID to title mappings...")
    uuid_mapping = parse_suno_csv_for_mappings(csv_file_path)
    print(f"Loaded {len(uuid_mapping)} UUID mappings")

    # Test directories and files with UUID names
    print("\nTesting UUID-named directories...")
    test_uuid_directories_and_files(music_root_dir, uuid_mapping)

    print("\nProcess completed!")


if __name__ == "__main__":
    main()
