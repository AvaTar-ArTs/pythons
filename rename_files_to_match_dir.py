#!/usr/bin/env python3
"""
Script to rename files inside the renamed directories to match the directory name.
"""

from pathlib import Path


def rename_files_to_match_directory(parent_dir):
    """
    Rename files inside directories to match the directory name.
    """
    renamed_files = []

    for item in Path(parent_dir).iterdir():
        if item.is_dir():
            # Get the directory name (which is now the proper title)
            dir_name = item.name

            # Look for audio files inside the directory
            for file in item.iterdir():
                if file.is_file() and file.suffix.lower() in [
                    ".mp3",
                    ".wav",
                    ".flac",
                    ".m4a",
                ]:
                    # Create new filename based on directory name
                    new_filename = f"{dir_name}{file.suffix}"

                    # Handle duplicate names by appending a number
                    new_path = file.parent / new_filename
                    counter = 1
                    while new_path.exists() and new_path != file:
                        new_path = file.parent / f"{dir_name}_{counter}{file.suffix}"
                        counter += 1

                    # Perform the rename
                    try:
                        file.rename(new_path)
                        print(f"Renamed file: '{file.name}' -> '{new_path.name}'")
                        renamed_files.append((str(file), str(new_path)))
                    except OSError as e:
                        print(f"Failed to rename file '{file.name}': {e}")

    return renamed_files


def main():
    # Define path
    parent_dir = "/Users/steven/Music/nocTurneMeLoDieS/MUSIC_ORGANIZED/ALBUMS"

    # Rename files inside directories to match directory names
    print(f"Renaming files inside directories in {parent_dir}...")
    renamed_files = rename_files_to_match_directory(parent_dir)

    # Summary
    print("\nSummary:")
    print(f"- Renamed {len(renamed_files)} files")

    print("\nProcess completed!")


if __name__ == "__main__":
    main()
