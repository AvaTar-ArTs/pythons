#!/usr/bin/env python3
"""
Simple Music Organizer for nocTurneMeLoDieS
Focuses on organizing music files into thematic collections without complex nesting
"""

import re
import shutil
from pathlib import Path


def create_simple_structure():
    """Create a simple organizational structure"""
    base_path = Path("/Users/steven/Music/nocTurneMeLoDieS")

    # Simple directory structure
    structure = [
        "MUSIC/ALLEY_COLLECTIONS",
        "MUSIC/SUMMER_COLLECTIONS",
        "MUSIC/WILLOW_COLLECTIONS",
        "MUSIC/JUNKYARD_COLLECTIONS",
        "MUSIC/HERO_COLLECTIONS",
        "MUSIC/TRASHCAT_COLLECTIONS",
        "MUSIC/OTHER_THEMES",
        "MUSIC/SINGLES",
        "MUSIC/REMIXES",
        "DATA/CSV",
        "DATA/JSON",
        "DATA/BACKUPS",
        "SCRIPTS/PYTHON",
        "SCRIPTS/UTILITIES",
        "DOCUMENTATION/PROJECT_NOTES",
        "DOCUMENTATION/ANALYSIS",
    ]

    print("Creating simple organizational structure...")
    for directory in structure:
        dir_path = base_path / directory
        dir_path.mkdir(parents=True, exist_ok=True)
        print(f"  Created: {directory}")

    return structure


def normalize_name(name):
    """Normalize directory/file names to remove special characters and foreign languages"""
    # Remove file extensions if present
    stem = Path(name).stem

    # Remove emoji and special prefixes
    stem = re.sub(r"^[\U0001F300-\U0001F9FF\U00002600-\U000027BF🎵🔔⭐️✨💯🙂🇧🇷]+\s*", "", stem)

    # Replace underscores and hyphens with spaces
    stem = stem.replace("_", " ").replace("-", " ")

    # Remove extra whitespace
    stem = " ".join(stem.split())

    return stem.strip()


def determine_thematic_category(name):
    """Determine the thematic category for a music collection"""
    normalized = normalize_name(name).lower()

    # Alley-themed collections
    if any(
        keyword in normalized
        for keyword in [
            "alley",
            "in this alley",
            "this alley",
            "alley where",
            "a l ley",
            "a l l ey",
        ]
    ):
        return "MUSIC/ALLEY_COLLECTIONS"

    # Summer-themed collections
    elif any(keyword in normalized for keyword in ["summer", "summer love"]):
        return "MUSIC/SUMMER_COLLECTIONS"

    # Willow-themed collections
    elif any(keyword in normalized for keyword in ["willow", "whisp", "willow whispers", "whispers"]):
        return "MUSIC/WILLOW_COLLECTIONS"

    # Junkyard-themed collections
    elif any(keyword in normalized for keyword in ["junk", "junkyard", "symphony"]):
        return "MUSIC/JUNKYARD_COLLECTIONS"

    # Hero-themed collections
    elif any(keyword in normalized for keyword in ["hero", "heroes", "rise", "villain", "villains"]):
        return "MUSIC/HERO_COLLECTIONS"

    # TrashCat/Raccoon-themed collections
    elif any(keyword in normalized for keyword in ["trash", "raccoon", "raccoon", "trashcat", "trashy"]):
        return "MUSIC/TRASHCAT_COLLECTIONS"

    # Other common themes
    elif any(keyword in normalized for keyword in ["echo", "echoes", "moonlight", "moon"]):
        return "MUSIC/OTHER_THEMES"

    elif any(keyword in normalized for keyword in ["heart", "heartbreak", "heartbeat", "dark"]):
        return "MUSIC/OTHER_THEMES"

    elif any(keyword in normalized for keyword in ["love", "loves", "imperfection"]):
        return "MUSIC/OTHER_THEMES"

    elif any(keyword in normalized for keyword in ["vine", "void"]):
        return "MUSIC/OTHER_THEMES"

    elif any(keyword in normalized for keyword in ["book", "memory"]):
        return "MUSIC/OTHER_THEMES"

    elif any(keyword in normalized for keyword in ["feather", "fang"]):
        return "MUSIC/OTHER_THEMES"

    else:
        return "MUSIC/OTHER_THEMES"


def organize_music_content():
    """Organize music content into simple thematic collections"""
    base_path = Path("/Users/steven/Music/nocTurneMeLoDieS")

    # Create simple structure
    create_simple_structure()

    # Find directories that likely contain music collections
    all_dirs = [d for d in base_path.iterdir() if d.is_dir()]

    # Skip already organized directories
    skip_dirs = {
        "MUSIC",
        "DATA",
        "SCRIPTS",
        "DOCUMENTATION",
        "ANALYSIS",
        "ARCHIVES",
        "WEB_ASSETS",
        "MUSIC_ORGANIZED",
        "OLD_STRUCTURE_ACCESS",
    }

    moved_count = 0
    failed_count = 0

    print("\nOrganizing music collections...")

    for directory in all_dirs:
        if directory.name in skip_dirs or directory.name.startswith("."):
            continue  # Skip already organized or system directories

        # Determine category based on directory name
        category = determine_thematic_category(directory.name)

        # Create target path
        target_dir = base_path / category
        target_path = target_dir / directory.name

        # Handle naming conflicts
        counter = 1
        while target_path.exists():
            target_path = target_dir / f"{directory.name}_{counter}"
            counter += 1

        try:
            shutil.move(str(directory), str(target_path))
            print(f"✓ Moved: {directory.name} -> {category}")
            moved_count += 1
        except Exception as e:
            print(f"✗ Failed to move {directory.name}: {str(e)}")
            failed_count += 1

    # Handle loose files
    print("\nOrganizing loose files...")
    all_files = [f for f in base_path.iterdir() if f.is_file()]

    for file in all_files:
        if file.name in [
            "simple_organization_plan.md",
            "simple_music_organizer.py",
            "simple_music_organizer_fixed.py",
        ]:
            continue  # Skip our own scripts

        extension = file.suffix.lower()

        # Handle audio files
        if extension in [".mp3", ".wav", ".flac", ".m4a", ".aac", ".ogg"]:
            category = determine_thematic_category(file.name)
            target_dir = base_path / category
            target_file = target_dir / file.name

            # Handle naming conflicts
            counter = 1
            while target_file.exists():
                stem = file.stem
                suffix = file.suffix
                target_file = target_dir / f"{stem}_{counter}{suffix}"
                counter += 1

            try:
                shutil.move(str(file), str(target_file))
                print(f"✓ Moved audio: {file.name} -> {category}")
                moved_count += 1
            except Exception as e:
                print(f"✗ Failed to move audio {file.name}: {str(e)}")
                failed_count += 1

        # Handle data files
        elif extension in [".csv", ".json", ".xlsx", ".xls"]:
            if extension == ".csv":
                target_dir = base_path / "DATA" / "CSV"
            elif extension == ".json":
                target_dir = base_path / "DATA" / "JSON"
            else:
                target_dir = base_path / "DATA" / "BACKUPS"

            target_dir.mkdir(parents=True, exist_ok=True)
            target_file = target_dir / file.name

            # Handle naming conflicts
            counter = 1
            while target_file.exists():
                stem = file.stem
                suffix = file.suffix
                target_file = target_dir / f"{stem}_{counter}{suffix}"
                counter += 1

            try:
                shutil.move(str(file), str(target_file))
                print(f"✓ Moved data: {file.name} -> {target_dir.name}")
                moved_count += 1
            except Exception as e:
                print(f"✗ Failed to move data {file.name}: {str(e)}")
                failed_count += 1

        # Handle script files
        elif extension in [".py", ".sh", ".js", ".ts"]:
            if extension == ".py":
                target_dir = base_path / "SCRIPTS" / "PYTHON"
            else:
                target_dir = base_path / "SCRIPTS" / "UTILITIES"

            target_dir.mkdir(parents=True, exist_ok=True)
            target_file = target_dir / file.name

            # Handle naming conflicts
            counter = 1
            while target_file.exists():
                stem = file.stem
                suffix = file.suffix
                target_file = target_dir / f"{stem}_{counter}{suffix}"
                counter += 1

            try:
                shutil.move(str(file), str(target_file))
                print(f"✓ Moved script: {file.name} -> {target_dir.name}")
                moved_count += 1
            except Exception as e:
                print(f"✗ Failed to move script {file.name}: {str(e)}")
                failed_count += 1

        # Handle documentation files
        elif extension in [".txt", ".md", ".pdf", ".doc", ".docx"]:
            if any(keyword in file.name.lower() for keyword in ["readme", "note", "doc", "documentation"]):
                target_dir = base_path / "DOCUMENTATION" / "PROJECT_NOTES"
            else:
                target_dir = base_path / "DOCUMENTATION" / "ANALYSIS"

            target_dir.mkdir(parents=True, exist_ok=True)
            target_file = target_dir / file.name

            # Handle naming conflicts
            counter = 1
            while target_file.exists():
                stem = file.stem
                suffix = file.suffix
                target_file = target_dir / f"{stem}_{counter}{suffix}"
                counter += 1

            try:
                shutil.move(str(file), str(target_file))
                print(f"✓ Moved doc: {file.name} -> {target_dir.name}")
                moved_count += 1
            except Exception as e:
                print(f"✗ Failed to move doc {file.name}: {str(e)}")
                failed_count += 1

    # Create summary
    summary_path = base_path / "SIMPLE_ORGANIZATION_SUMMARY.md"
    with open(summary_path, "w") as f:
        f.write("# Simple Music Organization Summary\n\n")
        f.write(f"**Date**: {Path(__file__).stat().st_mtime}\n\n")  # Using current time
        f.write(f"**Directories/Files moved**: {moved_count}\n")
        f.write(f"**Operations failed**: {failed_count}\n\n")

        f.write("## New Simple Structure\n\n")
        f.write("```\n")
        f.write("MUSIC/\n")
        f.write("├── ALLEY_COLLECTIONS/     # Alley-themed songs\n")
        f.write("├── SUMMER_COLLECTIONS/    # Summer-themed songs\n")
        f.write("├── WILLOW_COLLECTIONS/    # Willow-themed songs\n")
        f.write("├── JUNKYARD_COLLECTIONS/  # Junkyard-themed songs\n")
        f.write("├── HERO_COLLECTIONS/      # Hero-themed songs\n")
        f.write("├── TRASHCAT_COLLECTIONS/  # TrashCat-themed songs\n")
        f.write("├── OTHER_THEMES/          # Other themed collections\n")
        f.write("├── SINGLES/               # Individual tracks\n")
        f.write("└── REMIXES/               # Remixes and alternate versions\n")
        f.write("DATA/\n")
        f.write("├── CSV/                   # CSV files\n")
        f.write("├── JSON/                  # JSON files\n")
        f.write("└── BACKUPS/               # Backup files\n")
        f.write("SCRIPTS/\n")
        f.write("├── PYTHON/                # Python scripts\n")
        f.write("└── UTILITIES/             # Utility scripts\n")
        f.write("DOCUMENTATION/\n")
        f.write("├── PROJECT_NOTES/         # Project documentation\n")
        f.write("└── ANALYSIS/              # Analysis reports\n")
        f.write("```\n\n")

        f.write("## Organization Principles\n\n")
        f.write("- Simple thematic grouping\n")
        f.write("- English directory names only\n")
        f.write("- Minimal nesting (2-3 levels max)\n")
        f.write("- All music content preserved\n")
        f.write("- Easy navigation and maintenance\n")

    print(f"\n{'=' * 50}")
    print("SIMPLE ORGANIZATION COMPLETED!")
    print(f"{'=' * 50}")
    print(f"Items moved: {moved_count}")
    print(f"Items failed: {failed_count}")
    print(f"Summary saved to: {summary_path}")

    return {"moved": moved_count, "failed": failed_count, "summary": str(summary_path)}


if __name__ == "__main__":
    results = organize_music_content()
    print(f"\nFinal Results: {results}")
