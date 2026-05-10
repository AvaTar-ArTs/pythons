#!/usr/bin/env python3
"""
Simplified Music Collection Organizer

This script creates a simplified organization structure focusing on the 5 main
thematic collections as requested: Alley, Willow, Summer, Hero, and TrashCat themes.
"""

import re
import shutil
from pathlib import Path


def create_simplified_structure():
    """Create the simplified directory structure"""

    # Define the simplified structure
    base_path = Path("/Users/steven/Music/nocTurneMeLoDieS/MUSIC_ORGANIZED_SIMPLIFIED")

    # Create main directories
    directories = [
        base_path / "ALLEY_COLLECTION",
        base_path / "WILLOW_COLLECTION",
        base_path / "SUMMER_COLLECTION",
        base_path / "HERO_COLLECTION",
        base_path / "TRASHCAT_COLLECTION",
        base_path / "ALL_OTHER_MUSIC",
        base_path / "COVER_ART",
        base_path / "LYRICS",
        base_path / "ANALYSIS",
        base_path / "TRANSCRIPTS",
    ]

    for directory in directories:
        directory.mkdir(parents=True, exist_ok=True)
        print(f"Created directory: {directory}")

    return base_path


def move_thematic_content(base_path):
    """Move content to the appropriate thematic collections"""

    source_albums = Path("/Users/steven/Music/nocTurneMeLoDieS/MUSIC_ORGANIZED/ALBUMS")

    if not source_albums.exists():
        print(f"Source directory does not exist: {source_albums}")
        return

    # Define patterns for each theme
    themes = {
        "alley": [
            r"in[ _-]*this[ _-]*alley",
            r"ally",
            r"alley",
            r"in[ _-]*this[ _-]*a+ll+e+y",
            r"hide",
        ],
        "willow": [r"willow[ _-]*whisp", r"whisper", r"willow"],
        "summer": [r"summer[ _-]*lov", r"summer"],
        "hero": [r"hero", r"rise", r"villain", r"overthrow"],
        "trashcat": [
            r"trash[ _-]*cat",
            r"raccoon",
            r"junkyard",
            r"dumpster",
            r"rubbi",
            r"trashi",
        ],
    }

    moved_count = {
        "alley": 0,
        "willow": 0,
        "summer": 0,
        "hero": 0,
        "trashcat": 0,
        "other": 0,
    }

    # Process each directory in the source albums
    for item in source_albums.iterdir():
        if item.is_dir():
            dir_name_lower = item.name.lower()

            # Check each theme
            moved = False
            for theme, patterns in themes.items():
                for pattern in patterns:
                    if re.search(pattern, dir_name_lower):
                        # Move to appropriate collection
                        dest_dir = base_path / f"{theme.upper()}_COLLECTION" / item.name
                        try:
                            shutil.move(str(item), str(dest_dir))
                            print(f"Moved to {theme.upper()}_COLLECTION: {item.name}")
                            moved_count[theme] += 1
                            moved = True
                            break
                        except Exception as e:
                            print(f"Error moving {item.name}: {str(e)}")

                if moved:
                    break

            # If not moved to a specific theme, move to ALL_OTHER_MUSIC
            if not moved:
                dest_dir = base_path / "ALL_OTHER_MUSIC" / item.name
                try:
                    shutil.move(str(item), str(dest_dir))
                    print(f"Moved to ALL_OTHER_MUSIC: {item.name}")
                    moved_count["other"] += 1
                except Exception as e:
                    print(f"Error moving {item.name} to other: {str(e)}")

    # Print summary
    print("\n--- MOVEMENT SUMMARY ---")
    print(f"Alley-themed items moved: {moved_count['alley']}")
    print(f"Willow-themed items moved: {moved_count['willow']}")
    print(f"Summer-themed items moved: {moved_count['summer']}")
    print(f"Hero-themed items moved: {moved_count['hero']}")
    print(f"TrashCat-themed items moved: {moved_count['trashcat']}")
    print(f"All other items moved: {moved_count['other']}")
    print(f"Total items processed: {sum(moved_count.values())}")


def preserve_supporting_content():
    """Copy supporting content to the simplified structure"""

    base_path = Path("/Users/steven/Music/nocTurneMeLoDieS/MUSIC_ORGANIZED_SIMPLIFIED")
    source_base = Path("/Users/steven/Music/nocTurneMeLoDieS/MUSIC_ORGANIZED")

    # Copy supporting directories if they exist
    supporting_dirs = ["COVER_ART", "LYRICS", "ANALYSIS", "TRANSCRIPTS"]

    for dir_name in supporting_dirs:
        source_dir = source_base / dir_name
        dest_dir = base_path / dir_name

        if source_dir.exists():
            try:
                # Use distutils.dir_util.copy_tree for copying directory contents
                import distutils.dir_util

                distutils.dir_util.copy_tree(str(source_dir), str(dest_dir))
                print(f"Copied {dir_name} content to simplified structure")
            except ImportError:
                # Alternative approach if distutils is not available
                try:
                    shutil.copytree(source_dir, dest_dir, dirs_exist_ok=True)
                    print(f"Copied {dir_name} content to simplified structure")
                except Exception as e:
                    print(f"Error copying {dir_name}: {str(e)}")
            except Exception as e:
                print(f"Error copying {dir_name}: {str(e)}")


def create_readme(base_path):
    """Create a README file explaining the simplified structure"""

    readme_content = """# Simplified Music Collection

This simplified organization focuses on the 5 main thematic collections:

## Collections
- **ALLEY_COLLECTION**: All "In This Alley Where I Hide" variations
- **WILLOW_COLLECTION**: All "Willow Whispers" variations
- **SUMMER_COLLECTION**: All "Summer Love" variations
- **HERO_COLLECTION**: All "Heroes Rise Villains Overthrow" variations
- **TRASHCAT_COLLECTION**: All TrashCat-themed songs
- **ALL_OTHER_MUSIC**: Everything else

## Supporting Content
- **COVER_ART**: All cover art
- **LYRICS**: All lyrics
- **ANALYSIS**: All analysis files
- **TRANSCRIPTS**: All transcripts

This structure makes it easy to find your main themed collections without navigating through hundreds of individual directories.
"""

    readme_path = base_path / "README.md"
    with open(readme_path, "w") as f:
        f.write(readme_content)
    print(f"Created README at {readme_path}")


def main():
    print("Creating simplified music collection organization...")

    # Create the simplified structure
    base_path = create_simplified_structure()

    # Move thematic content
    print("\nMoving thematic content...")
    move_thematic_content(base_path)

    # Preserve supporting content
    print("\nPreserving supporting content...")
    preserve_supporting_content()

    # Create README
    print("\nCreating documentation...")
    create_readme(base_path)

    print("\nSimplified organization complete!")
    print(f"Simplified structure created at: {base_path}")
    print("\nThe 5 main collections are now easily accessible:")
    print("- ALLEY_COLLECTION/")
    print("- WILLOW_COLLECTION/")
    print("- SUMMER_COLLECTION/")
    print("- HERO_COLLECTION/")
    print("- TRASHCAT_COLLECTION/")


if __name__ == "__main__":
    main()
