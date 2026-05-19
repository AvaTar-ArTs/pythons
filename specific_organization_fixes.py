#!/usr/bin/env python3
"""
Specific script to handle remaining organization issues:
1. Group all "Bite in the Night" variations into a single collection
2. Handle remaining UUID directories that couldn't be mapped
"""

import os
import re
import shutil
from pathlib import Path


def group_bite_in_the_night_variations(albums_dir):
    """
    Specifically group all "Bite in the Night" variations into a single collection.
    """
    print("Grouping 'Bite in the Night' variations...")

    # Find all directories that match "Bite in the Night" patterns
    bite_dirs = []
    for item in Path(albums_dir).iterdir():
        if item.is_dir():
            dir_name = item.name.lower()
            if "bite" in dir_name and "night" in dir_name:
                bite_dirs.append(item)

    print(f"Found {len(bite_dirs)} 'Bite in the Night' related directories:")
    for d in bite_dirs:
        print(f"  - {d.name}")

    if not bite_dirs:
        print("No 'Bite in the Night' directories found.")
        return

    # Create main collection directory
    main_collection = Path(albums_dir) / "Bite_In_The_Night_Collection"
    main_collection.mkdir(exist_ok=True)

    # Move all bite-related directories into the main collection
    moved_count = 0
    for bite_dir in bite_dirs:
        if bite_dir != main_collection:  # Don't move the collection into itself
            target_path = main_collection / bite_dir.name

            # Handle duplicates
            counter = 1
            while target_path.exists():
                target_path = main_collection / f"{bite_dir.name}_{counter}"
                counter += 1

            try:
                if target_path != bite_dir:
                    shutil.move(str(bite_dir), str(target_path))
                    print(f"  Moved: '{bite_dir.name}' -> '{target_path.name}'")
                    moved_count += 1
            except OSError as e:
                print(f"  Failed to move '{bite_dir.name}': {e}")

    print(f"Grouped {moved_count} 'Bite in the Night' directories into collection.")


def handle_remaining_uuid_directories(albums_dir):
    """
    Handle remaining UUID directories that couldn't be mapped.
    """
    print("\nHandling remaining UUID directories...")

    # Find all UUID-named directories
    uuid_dirs = []
    for item in Path(albums_dir).iterdir():
        if item.is_dir():
            dir_name = item.name

            # Check if the directory name looks like a UUID (with underscores)
            uuid_pattern = r"^[a-f0-9]{8}_[a-f0-9]{4}_[a-f0-9]{4}_[a-f0-9]{4}_[a-f0-9]{12}$"

            if re.match(uuid_pattern, dir_name.lower()):
                uuid_dirs.append(item)

    print(f"Found {len(uuid_dirs)} remaining UUID directories:")
    for d in uuid_dirs:
        print(f"  - {d.name}")

    if not uuid_dirs:
        print("No remaining UUID directories found.")
        return

    # Create a general 'Unmapped_UUIDs' directory to store unmapped UUID directories
    unmapped_dir = Path(albums_dir) / "Unmapped_UUIDs"
    unmapped_dir.mkdir(exist_ok=True)

    # Move all UUID directories to the unmapped directory
    moved_count = 0
    for uuid_dir in uuid_dirs:
        target_path = unmapped_dir / uuid_dir.name

        try:
            shutil.move(str(uuid_dir), str(target_path))
            print(f"  Moved UUID directory: '{uuid_dir.name}' -> 'Unmapped_UUIDs/{target_path.name}'")
            moved_count += 1
        except OSError as e:
            print(f"  Failed to move UUID directory '{uuid_dir.name}': {e}")

    print(f"Moved {moved_count} UUID directories to 'Unmapped_UUIDs' collection.")


def improve_existing_groupings(albums_dir):
    """
    Improve existing groupings by consolidating similar named directories.
    """
    print("\nImproving existing groupings...")

    # Dictionary to track potential groupings
    dir_groups = {}

    for item in Path(albums_dir).iterdir():
        if item.is_dir():
            dir_name = item.name

            # Skip if it's already a collection directory we created
            if dir_name in ["Bite_In_The_Night_Collection", "Unmapped_UUIDs"]:
                continue

            # Look for patterns indicating variations of the same song
            # Remove version numbers, timestamps, etc. to get base name
            base_name = re.sub(r"[_-]\d+[a-zA-Z]*$", "", dir_name)
            base_name = re.sub(r"[_-]\d+m?\s*x?tra?", "", base_name)
            base_name = re.sub(
                r"[_-](?:remaster|remastered|live|acoustic|instrumental|demo|edit|remix|version|v\d+)",
                "",
                base_name,
                flags=re.IGNORECASE,
            )
            base_name = re.sub(
                r"[_-](?:lady|ballade|indie|grunge|pluck|duo)\s*\d*",
                "",
                base_name,
                flags=re.IGNORECASE,
            )

            if base_name != dir_name:  # Only if we actually modified it
                if base_name not in dir_groups:
                    dir_groups[base_name] = []
                dir_groups[base_name].append(item)

    # Consolidate directories that share the same base name
    consolidated_count = 0
    for base_name, dirs in dir_groups.items():
        if len(dirs) > 1:
            # Create a main collection directory
            collection_dir = Path(albums_dir) / base_name
            collection_dir.mkdir(exist_ok=True)

            print(f"Consolidating {len(dirs)} directories under '{base_name}':")

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
                            print(f"  Consolidated: '{dir_item.name}' -> '{target_subdir.relative_to(albums_dir)}'")
                            consolidated_count += 1
                    except OSError as e:
                        print(f"  Failed to move directory '{dir_item.name}': {e}")

    print(f"Improved {consolidated_count} existing groupings.")


def main():
    # Define paths
    albums_dir = "/Users/steven/Music/nocTurneMeLoDieS/MUSIC_ORGANIZED/ALBUMS/"

    # Check if albums directory exists
    if not os.path.exists(albums_dir):
        print(f"Albums directory not found: {albums_dir}")
        return

    # Group "Bite in the Night" variations
    group_bite_in_the_night_variations(albums_dir)

    # Handle remaining UUID directories
    handle_remaining_uuid_directories(albums_dir)

    # Improve existing groupings
    improve_existing_groupings(albums_dir)

    print("\nSpecific organization fixes completed!")


if __name__ == "__main__":
    main()
