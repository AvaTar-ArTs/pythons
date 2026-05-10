#!/usr/bin/env python3
"""
Organize the zip directory with proper structure based on content analysis
"""

import shutil
from datetime import datetime
from pathlib import Path


def organize_zip_folder():
    """Organize the zip directory with proper structure"""
    zip_path = Path("/Users/steven/Music/nocTurneMeLoDieS/zip")

    # Create new organizational structure
    categories = [
        "BACKUPS/PROJECT_BACKUPS",
        "BACKUPS/MP3_COLLECTIONS",
        "BACKUPS/CONFIG_BACKUPS",
        "MUSIC_COLLECTIONS/ALLEY_COLLECTIONS",
        "MUSIC_COLLECTIONS/WILLOW_COLLECTIONS",
        "MUSIC_COLLECTIONS/TRASHCAT_COLLECTIONS",
        "MUSIC_COLLECTIONS/HERO_COLLECTIONS",
        "MUSIC_COLLECTIONS/OTHER_THEMES",
        "TOOLS/SUNO_TOOLS",
        "TOOLS/AUDIO_TOOLS",
        "TOOLS/IMAGE_TOOLS",
        "TOOLS/WEB_TOOLS",
        "DOCUMENTATION",
        "EXPORTS",
        "MISC",
    ]

    for category in categories:
        (zip_path / category).mkdir(parents=True, exist_ok=True)

    # Categorize and move zip files
    moved_files = 0
    failed_moves = 0

    print("Organizing zip files...")

    for zip_file in zip_path.glob("*.zip"):
        if zip_file.is_file():
            name_lower = zip_file.name.lower()

            # Determine category based on name
            if any(keyword in name_lower for keyword in ["mp3", "backup", "bak"]):
                target_dir = zip_path / "BACKUPS" / "MP3_COLLECTIONS"
            elif any(
                keyword in name_lower
                for keyword in [
                    "export",
                    "2025",
                    "2026",
                    "nocturne",
                    "nocturnemelodies",
                ]
            ):
                target_dir = zip_path / "BACKUPS" / "PROJECT_BACKUPS"
            elif any(keyword in name_lower for keyword in ["alley", "inthis", "hiide", "aLLey", "alley"]):
                target_dir = zip_path / "MUSIC_COLLECTIONS" / "ALLEY_COLLECTIONS"
            elif any(keyword in name_lower for keyword in ["willow", "whisp"]):
                target_dir = zip_path / "MUSIC_COLLECTIONS" / "WILLOW_COLLECTIONS"
            elif any(keyword in name_lower for keyword in ["trash", "raccoon", "raccoon", "trashcat", "trashy"]):
                target_dir = zip_path / "MUSIC_COLLECTIONS" / "TRASHCAT_COLLECTIONS"
            elif any(keyword in name_lower for keyword in ["hero", "villain", "rise"]):
                target_dir = zip_path / "MUSIC_COLLECTIONS" / "HERO_COLLECTIONS"
            elif any(keyword in name_lower for keyword in ["suno", "suno-"]):
                target_dir = zip_path / "TOOLS" / "SUNO_TOOLS"
            elif any(keyword in name_lower for keyword in ["audio", "mp3", "music"]):
                target_dir = zip_path / "TOOLS" / "AUDIO_TOOLS"
            elif any(keyword in name_lower for keyword in ["image", "typo", "prompt"]):
                target_dir = zip_path / "TOOLS" / "IMAGE_TOOLS"
            elif any(keyword in name_lower for keyword in ["web", "html", "site"]):
                target_dir = zip_path / "TOOLS" / "WEB_TOOLS"
            elif any(keyword in name_lower for keyword in ["doc", "readme", "manual"]):
                target_dir = zip_path / "DOCUMENTATION"
            elif any(keyword in name_lower for keyword in ["export"]):
                target_dir = zip_path / "EXPORTS"
            else:
                target_dir = zip_path / "MISC"

            # Move the file
            target_path = target_dir / zip_file.name
            counter = 1
            while target_path.exists():
                stem = zip_file.stem
                suffix = zip_file.suffix
                target_path = target_dir / f"{stem}_{counter}{suffix}"
                counter += 1

            try:
                shutil.move(str(zip_file), str(target_path))
                print(f"✓ Moved {zip_file.name} to {target_dir.name}")
                moved_files += 1
            except Exception as e:
                print(f"✗ Failed to move {zip_file.name}: {str(e)}")
                failed_moves += 1

    # Process subdirectories
    print("\nOrganizing subdirectories...")

    for subdir in list(zip_path.iterdir()):  # Use list() to avoid iteration issues during move
        if subdir.is_dir() and subdir.name not in [
            "BACKUPS",
            "MUSIC_COLLECTIONS",
            "TOOLS",
            "DOCUMENTATION",
            "EXPORTS",
            "MISC",
        ]:
            name_lower = subdir.name.lower()

            # Determine category based on directory name
            if any(keyword in name_lower for keyword in ["suno", "suno-", "suno_", "suno."]):
                target_dir = zip_path / "TOOLS" / "SUNO_TOOLS"
            elif any(
                keyword in name_lower
                for keyword in [
                    "trash",
                    "raccoon",
                    "alley",
                    "love",
                    "willow",
                    "hero",
                    "junk",
                    "echo",
                    "heart",
                    "moon",
                    "shadow",
                ]
            ):
                target_dir = zip_path / "MUSIC_COLLECTIONS" / "OTHER_THEMES"
            elif any(keyword in name_lower for keyword in ["image", "img", "pic", "art", "visual", "typo"]):
                target_dir = zip_path / "TOOLS" / "IMAGE_TOOLS"
            elif any(keyword in name_lower for keyword in ["script", "pythons", "python", "automation", "tool"]):
                target_dir = zip_path / "TOOLS" / "AUDIO_TOOLS"
            elif any(keyword in name_lower for keyword in ["doc", "manual", "guide", "readme", "tutorial", "howto"]):
                target_dir = zip_path / "DOCUMENTATION"
            elif any(keyword in name_lower for keyword in ["web", "html", "site", "gallery"]):
                target_dir = zip_path / "TOOLS" / "WEB_TOOLS"
            elif any(keyword in name_lower for keyword in ["backup", "archive", "export"]):
                target_dir = zip_path / "BACKUPS" / "PROJECT_BACKUPS"
            else:
                target_dir = zip_path / "MISC"

            # Move the directory
            target_path = target_dir / subdir.name
            counter = 1
            while target_path.exists():
                target_path = target_dir / f"{subdir.name}_{counter}"
                counter += 1

            try:
                shutil.move(str(subdir), str(target_path))
                print(f"✓ Moved directory {subdir.name} to {target_dir.name}")
                moved_files += 1
            except Exception as e:
                print(f"✗ Failed to move directory {subdir.name}: {str(e)}")
                failed_moves += 1

    # Handle loose files that aren't zip
    print("\nOrganizing loose files...")

    for loose_file in list(zip_path.iterdir()):  # Use list() to avoid iteration issues
        if loose_file.is_file() and loose_file.suffix.lower() != ".zip":
            name_lower = loose_file.name.lower()

            # Determine category based on file extension and name
            if loose_file.suffix.lower() in [".mp4", ".mov", ".avi", ".mkv"]:
                target_dir = zip_path / "MUSIC_COLLECTIONS" / "OTHER_THEMES"
            elif loose_file.suffix.lower() in [".mp3", ".wav", ".flac", ".m4a"]:
                target_dir = zip_path / "BACKUPS" / "MP3_COLLECTIONS"
            elif loose_file.suffix.lower() in [".py", ".js", ".sh"]:
                target_dir = zip_path / "TOOLS" / "AUDIO_TOOLS"
            elif loose_file.suffix.lower() in [".csv", ".json", ".txt"]:
                if any(keyword in name_lower for keyword in ["suno", "export"]):
                    target_dir = zip_path / "EXPORTS"
                else:
                    target_dir = zip_path / "DOCUMENTATION"
            elif loose_file.suffix.lower() in [".html", ".md"]:
                target_dir = zip_path / "DOCUMENTATION"
            elif loose_file.suffix.lower() in [".jpg", ".jpeg", ".png", ".gif"]:
                target_dir = zip_path / "TOOLS" / "IMAGE_TOOLS"
            else:
                target_dir = zip_path / "MISC"

            # Move the file
            target_path = target_dir / loose_file.name
            counter = 1
            while target_path.exists():
                stem = loose_file.stem
                suffix = loose_file.suffix
                target_path = target_dir / f"{stem}_{counter}{suffix}"
                counter += 1

            try:
                shutil.move(str(loose_file), str(target_path))
                print(f"✓ Moved loose file {loose_file.name} to {target_dir.name}")
                moved_files += 1
            except Exception as e:
                print(f"✗ Failed to move loose file {loose_file.name}: {str(e)}")
                failed_moves += 1

    # Create final summary
    summary_path = zip_path / "ORGANIZATION_SUMMARY_FINAL.md"
    with open(summary_path, "w") as f:
        f.write("# Zip Directory Organization Complete\n\n")
        f.write(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        f.write(f"Files organized: {moved_files}\n")
        f.write(f"Files failed to move: {failed_moves}\n\n")

        f.write("## New Structure:\n")
        f.write("```\n")
        f.write("zip/\n")
        f.write("├── BACKUPS/\n")
        f.write("│   ├── PROJECT_BACKUPS/     # Project backup archives\n")
        f.write("│   ├── MP3_COLLECTIONS/     # MP3 collection backups\n")
        f.write("│   └── CONFIG_BACKUPS/      # Configuration backups\n")
        f.write("├── MUSIC_COLLECTIONS/\n")
        f.write("│   ├── ALLEY_COLLECTIONS/   # Alley-themed music\n")
        f.write("│   ├── WILLLOW_COLLECTIONS/ # Willow-themed music\n")
        f.write("│   ├── TRASHCAT_COLLECTIONS/ # TrashCat-themed music\n")
        f.write("│   ├── HERO_COLLECTIONS/    # Hero-themed music\n")
        f.write("│   └── OTHER_THEMES/        # Other themed collections\n")
        f.write("├── TOOLS/\n")
        f.write("│   ├── SUNO_TOOLS/          # Suno-related tools\n")
        f.write("│   ├── AUDIO_TOOLS/         # Audio processing tools\n")
        f.write("│   ├── IMAGE_TOOLS/         # Image generation tools\n")
        f.write("│   └── WEB_TOOLS/           # Web interface tools\n")
        f.write("├── DOCUMENTATION/           # Documentation files\n")
        f.write("├── EXPORTS/                 # Export archives\n")
        f.write("└── MISC/                    # Miscellaneous files\n")
        f.write("```\n")

    print("\nOrganization complete!")
    print(f"Files organized: {moved_files}")
    print(f"Files failed to move: {failed_moves}")
    print(f"Summary saved to: {summary_path}")


if __name__ == "__main__":
    organize_zip_folder()
