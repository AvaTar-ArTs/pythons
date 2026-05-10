#!/usr/bin/env python3
"""
Rename files using CSV metadata to replace UUID-based names with proper song titles
"""

import csv
import re
import shutil
from datetime import datetime
from pathlib import Path


def load_song_metadata():
    """Load song metadata from CSV files to map UUIDs to proper titles"""
    base_path = Path("/Users/steven/Music/nocTurneMeLoDieS")
    metadata = {}

    # Find all CSV files that contain song metadata
    csv_files = list(base_path.rglob("*.csv"))

    for csv_file in csv_files:
        try:
            with open(csv_file, encoding="utf-8") as f:
                # Check if this CSV contains song metadata
                sample = f.read(1024)
                f.seek(0)

                if any(keyword in sample.lower() for keyword in ["id", "title", "song", "audio_url", "url"]):
                    reader = csv.DictReader(f)
                    for row in reader:
                        if "id" in row and "title" in row:
                            song_id = row["id"].strip()
                            title = row["title"].strip()
                            if song_id and title:
                                # Clean the title for use as a filename
                                clean_title = re.sub(r"[^\w\s-]", "_", title)
                                clean_title = re.sub(r"\s+", "_", clean_title.strip())
                                metadata[song_id] = clean_title
                        elif "uuid" in row and "title" in row:
                            song_id = row["uuid"].strip()
                            title = row["title"].strip()
                            if song_id and title:
                                # Clean the title for use as a filename
                                clean_title = re.sub(r"[^\w\s-]", "_", title)
                                clean_title = re.sub(r"\s+", "_", clean_title.strip())
                                metadata[song_id] = clean_title
        except Exception as e:
            print(f"Could not read CSV {csv_file}: {e}")
            continue

    return metadata


def normalize_filename(name):
    """Normalize a filename to extract potential UUID"""
    # Remove file extension
    stem = Path(name).stem

    # Look for UUID patterns in the filename
    uuid_patterns = [
        r"([0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12})",
        r"([0-9a-f]{8}[0-9a-f]{4}[0-9a-f]{4}[0-9a-f]{4}[0-9a-f]{12})",
        r"([0-9a-f]{8}[_-][0-9a-f]{4}[_-][0-9a-f]{4}[_-][0-9a-f]{4}[_-][0-9a-f]{12})",
    ]

    for pattern in uuid_patterns:
        match = re.search(pattern, stem, re.IGNORECASE)
        if match:
            return match.group(1).lower().replace("-", "").replace("_", "")

    return None


def rename_files_with_metadata():
    """Rename files using metadata from CSVs"""
    base_path = Path("/Users/steven/Music/nocTurneMeLoDieS")

    print("Loading song metadata from CSV files...")
    song_metadata = load_song_metadata()
    print(f"Loaded metadata for {len(song_metadata)} songs")

    # Find all MP3 files that might need renaming
    mp3_files = list(base_path.rglob("*.mp3"))

    renamed_count = 0
    failed_count = 0
    skipped_count = 0

    print(f"Found {len(mp3_files)} MP3 files to process")

    for mp3_file in mp3_files:
        # Skip files in the new organized structure that already have good names
        if "MUSIC_ORGANIZED" in str(mp3_file):
            continue

        # Extract potential UUID from filename
        potential_uuid = normalize_filename(mp3_file.name)

        if potential_uuid and len(potential_uuid) == 32:  # Valid UUID length
            # Look for this UUID in our metadata
            found_match = False
            for uuid_key, title in song_metadata.items():
                clean_uuid_key = uuid_key.lower().replace("-", "").replace("_", "")
                if clean_uuid_key == potential_uuid:
                    # Found a match, rename the file
                    original_path = mp3_file
                    new_name = f"{title}{mp3_file.suffix}"

                    # Handle potential naming conflicts
                    counter = 1
                    new_path = mp3_file.parent / new_name
                    while new_path.exists():
                        new_name = f"{title}_{counter}{mp3_file.suffix}"
                        new_path = mp3_file.parent / new_name
                        counter += 1

                    try:
                        # Rename the file
                        shutil.move(str(original_path), str(new_path))
                        print(f"✓ Renamed: {mp3_file.name} -> {new_name}")
                        renamed_count += 1
                        found_match = True
                        break
                    except Exception as e:
                        print(f"✗ Failed to rename {mp3_file.name}: {str(e)}")
                        failed_count += 1
                        break

            if not found_match:
                print(f"- No metadata match found for UUID in: {mp3_file.name}")
                skipped_count += 1
        else:
            # Check if filename contains "Untitled" or other generic names that might have UUID parts
            if "Untitled" in mp3_file.name or "_" in mp3_file.name:
                # Try to find a UUID pattern in the name even if it's not a perfect match
                name_part = mp3_file.stem
                # Look for patterns like "Untitled_B56eaca9" where the second part might be a UUID
                parts = name_part.split("_")
                if len(parts) >= 2:
                    potential_uuid_part = parts[-1]  # Take the last part after underscores
                    # Check if it looks like a partial UUID
                    if len(potential_uuid_part) >= 6 and re.match(r"^[0-9a-f]+$", potential_uuid_part, re.IGNORECASE):
                        # Look for this partial UUID in our metadata
                        found_match = False
                        for uuid_key, title in song_metadata.items():
                            if potential_uuid_part.lower() in uuid_key.lower():
                                # Found a partial match, rename the file
                                original_path = mp3_file
                                new_name = f"{title}{mp3_file.suffix}"

                                # Handle potential naming conflicts
                                counter = 1
                                new_path = mp3_file.parent / new_name
                                while new_path.exists():
                                    new_name = f"{title}_{counter}{mp3_file.suffix}"
                                    new_path = mp3_file.parent / new_name
                                    counter += 1

                                try:
                                    shutil.move(str(original_path), str(new_path))
                                    print(f"✓ Renamed (partial UUID match): {mp3_file.name} -> {new_name}")
                                    renamed_count += 1
                                    found_match = True
                                    break
                                except Exception as e:
                                    print(f"✗ Failed to rename {mp3_file.name}: {str(e)}")
                                    failed_count += 1
                                    break

                        if not found_match:
                            skipped_count += 1
                    else:
                        skipped_count += 1
                else:
                    skipped_count += 1
            else:
                skipped_count += 1

    # Create summary report
    report_path = base_path / "DOCUMENTATION" / "filename_rename_report.md"
    report_path.parent.mkdir(parents=True, exist_ok=True)

    with open(report_path, "w") as f:
        f.write("# nocTurneMeLoDieS - Filename Rename Report\n\n")
        f.write(f"**Date**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        f.write(f"- **Files renamed**: {renamed_count}\n")
        f.write(f"- **Files failed to rename**: {failed_count}\n")
        f.write(f"- **Files skipped**: {skipped_count}\n\n")
        f.write("## Process Summary\n\n")
        f.write(
            "This script processed MP3 files with UUID-based names and renamed them using metadata from CSV files.\n"
        )
        f.write("Files were matched based on their UUID portions and renamed to proper song titles.\n\n")
        f.write("## Benefits Achieved\n\n")
        f.write("- Replaced cryptic UUID-based filenames with meaningful song titles\n")
        f.write("- Maintained proper organization while improving file naming\n")
        f.write("- Made it easier to identify songs by their filenames\n")

    print(f"\n{'=' * 60}")
    print("FILENAME RENAMING COMPLETED!")
    print(f"{'=' * 60}")
    print(f"Files renamed: {renamed_count}")
    print(f"Files failed: {failed_count}")
    print(f"Files skipped: {skipped_count}")
    print(f"Report saved to: {report_path}")

    return {
        "renamed": renamed_count,
        "failed": failed_count,
        "skipped": skipped_count,
        "report_path": str(report_path),
    }


def rename_directories_with_metadata():
    """Also rename directories that still have UUID names"""
    base_path = Path("/Users/steven/Music/nocTurneMeLoDieS")

    print("\nRenaming directories with UUID names...")

    # Find directories that still have UUID names
    uuid_dirs = []
    for item in base_path.rglob("*"):
        if item.is_dir():
            dir_name = item.name
            # Check if directory name looks like it contains a UUID
            uuid_pattern = re.compile(
                r"[0-9a-f]{8}[-_]?[0-9a-f]{4}[-_]?[0-9a-f]{4}[-_]?[0-9a-f]{4}[-_]?[0-9a-f]{12}|[0-9a-f]{32}",
                re.IGNORECASE,
            )

            if uuid_pattern.search(dir_name) or ("Untitled" in dir_name and "_" in dir_name):
                uuid_dirs.append(item)

    print(f"Found {len(uuid_dirs)} directories with UUID-like names")

    # Load metadata for directory renaming
    song_metadata = load_song_metadata()

    renamed_dirs = 0
    failed_dirs = 0

    for uuid_dir in uuid_dirs:
        dir_name = uuid_dir.name

        # Extract potential UUID from directory name
        potential_uuid = normalize_filename(dir_name)

        if potential_uuid and len(potential_uuid) == 32:  # Valid UUID length
            # Look for this UUID in our metadata
            found_match = False
            for uuid_key, title in song_metadata.items():
                clean_uuid_key = uuid_key.lower().replace("-", "").replace("_", "")
                if clean_uuid_key == potential_uuid:
                    # Found a match, rename the directory
                    original_path = uuid_dir
                    new_name = title

                    # Handle potential naming conflicts
                    counter = 1
                    new_path = uuid_dir.parent / new_name
                    while new_path.exists():
                        new_name = f"{title}_{counter}"
                        new_path = uuid_dir.parent / new_name
                        counter += 1

                    try:
                        shutil.move(str(original_path), str(new_path))
                        print(f"✓ Renamed directory: {uuid_dir.name} -> {new_name}")
                        renamed_dirs += 1
                        found_match = True
                        break
                    except Exception as e:
                        print(f"✗ Failed to rename directory {uuid_dir.name}: {str(e)}")
                        failed_dirs += 1
                        break

            if not found_match:
                print(f"- No metadata match found for directory: {uuid_dir.name}")
        else:
            # Check for partial UUID matches in directory names
            parts = dir_name.split("_")
            if len(parts) >= 2:
                potential_uuid_part = parts[-1]  # Take the last part after underscores
                # Check if it looks like a partial UUID
                if len(potential_uuid_part) >= 6 and re.match(r"^[0-9a-f]+$", potential_uuid_part, re.IGNORECASE):
                    # Look for this partial UUID in our metadata
                    found_match = False
                    for uuid_key, title in song_metadata.items():
                        if potential_uuid_part.lower() in uuid_key.lower():
                            # Found a partial match, rename the directory
                            original_path = uuid_dir
                            new_name = title

                            # Handle potential naming conflicts
                            counter = 1
                            new_path = uuid_dir.parent / new_name
                            while new_path.exists():
                                new_name = f"{title}_{counter}"
                                new_path = uuid_dir.parent / new_name
                                counter += 1

                            try:
                                shutil.move(str(original_path), str(new_path))
                                print(f"✓ Renamed directory (partial UUID match): {uuid_dir.name} -> {new_name}")
                                renamed_dirs += 1
                                found_match = True
                                break
                            except Exception as e:
                                print(f"✗ Failed to rename directory {uuid_dir.name}: {str(e)}")
                                failed_dirs += 1
                                break

                    if not found_match:
                        print(f"- No partial metadata match found for directory: {uuid_dir.name}")

    print(f"\nDirectory renaming completed: {renamed_dirs} renamed, {failed_dirs} failed")
    return renamed_dirs, failed_dirs


if __name__ == "__main__":
    # First rename files
    file_results = rename_files_with_metadata()

    # Then rename directories
    dir_results = rename_directories_with_metadata()

    print("\nOverall Results:")
    print(
        f"- Files: {file_results['renamed']} renamed, {file_results['failed']} failed, {file_results['skipped']} skipped"
    )
    print(f"- Directories: {dir_results[0]} renamed, {dir_results[1]} failed")
    print(f"- Total items renamed: {file_results['renamed'] + dir_results[0]}")
