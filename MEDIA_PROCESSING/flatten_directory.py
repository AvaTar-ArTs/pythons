#!/usr/bin/env python3
"""
Flatten directory structure by moving all files from subdirectories to root.
Handles filename conflicts by appending parent directory name.
"""

import shutil
from pathlib import Path


def flatten_directory(root_dir):
    """Move all files from subdirectories to root directory."""
    root_path = Path(root_dir)

    # Track files to move and handle conflicts
    files_to_move = []
    existing_files = set()

    # Get all existing files in root (excluding directories and this script)
    for item in root_path.iterdir():
        if item.is_file() and item.name != "flatten_directory.py":
            existing_files.add(item.name)

    # Walk through all subdirectories
    for subdir in root_path.iterdir():
        if subdir.is_dir() and subdir.name != "__pycache__":
            # Get relative path for naming conflicts
            subdir.relative_to(root_path)

            # Find all files in this subdirectory (recursively)
            for file_path in subdir.rglob("*"):
                if file_path.is_file():
                    # Skip this script if it exists in subdir
                    if file_path.name == "flatten_directory.py":
                        continue

                    # Check for conflicts
                    target_name = file_path.name
                    if target_name in existing_files:
                        # Create unique name using parent directory
                        parent_name = file_path.parent.name
                        stem = file_path.stem
                        suffix = file_path.suffix
                        target_name = f"{stem}_{parent_name}{suffix}"
                        # If still conflicts, add more path components
                        counter = 1
                        while target_name in existing_files:
                            target_name = f"{stem}_{parent_name}_{counter}{suffix}"
                            counter += 1

                    target_path = root_path / target_name
                    files_to_move.append((file_path, target_path))
                    existing_files.add(target_name)

    # Move all files
    moved_count = 0
    for source, target in files_to_move:
        try:
            print(f"Moving: {source.relative_to(root_path)} -> {target.name}")
            shutil.move(str(source), str(target))
            moved_count += 1
        except Exception as e:
            print(f"Error moving {source}: {e}")

    # Remove empty directories
    removed_dirs = []
    for subdir in root_path.iterdir():
        if subdir.is_dir() and subdir.name != "__pycache__":
            try:
                # Try to remove if empty
                subdir.rmdir()
                removed_dirs.append(subdir.name)
            except OSError:
                # Directory not empty, try to remove recursively
                try:
                    shutil.rmtree(subdir)
                    removed_dirs.append(subdir.name)
                    print(f"Removed directory: {subdir.name}")
                except Exception as e:
                    print(f"Could not remove {subdir}: {e}")

    print("\n✅ Flattening complete!")
    print(f"   Moved {moved_count} files")
    print(f"   Removed {len(removed_dirs)} directories")

    return moved_count, removed_dirs


if __name__ == "__main__":
    root_directory = Path(__file__).parent
    flatten_directory(root_directory)
