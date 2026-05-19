#!/usr/bin/env python3
"""
Organize the zip directory which contains many loose files and subdirectories
This script will create a proper structure for the zip directory content
"""

import shutil
from datetime import datetime
from pathlib import Path


def organize_zip_directory():
    """Organize the zip directory with proper subdirectory structure"""
    zip_path = Path("/Users/steven/Music/nocTurneMeLoDieS/zip")

    # Initialize lists for categorization
    backup_archives = []
    suno_tools = []
    music_archives = []
    code_archives = []
    documentation_archives = []
    image_archives = []
    script_archives = []
    other_archives = []

    print("Analyzing zip directory contents...")

    # Categorize files based on name patterns
    for item in zip_path.iterdir():
        if item.is_file() and item.suffix.lower() == ".zip":
            name_lower = item.name.lower()

            if any(
                keyword in name_lower
                for keyword in [
                    "mp3",
                    "backup",
                    "nocturnemelodies",
                    "2025",
                    "2026",
                    "nocturne",
                    "night",
                    "nigth",
                ]
            ):
                backup_archives.append(item)
            elif any(keyword in name_lower for keyword in ["suno", "suno-", "suno_", "suno."]):
                suno_tools.append(item)
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
                music_archives.append(item)
            elif any(
                keyword in name_lower
                for keyword in [
                    "source",
                    "code",
                    "dev",
                    "src",
                    "project",
                    "implementation",
                ]
            ):
                code_archives.append(item)
            elif any(keyword in name_lower for keyword in ["doc", "manual", "guide", "readme", "tutorial", "howto"]):
                documentation_archives.append(item)
            elif any(keyword in name_lower for keyword in ["image", "img", "pic", "photo", "art", "visual", "typo"]):
                image_archives.append(item)
            elif any(keyword in name_lower for keyword in ["script", "py", "sh", "bash", "automation"]):
                script_archives.append(item)
            else:
                other_archives.append(item)
        elif item.is_dir() and item.name not in [".", ".."]:
            # Handle directories - move them to appropriate locations based on content
            dir_name_lower = item.name.lower()

            if any(keyword in dir_name_lower for keyword in ["suno", "suno-", "suno_", "suno."]):
                dest_dir = zip_path / "SUNO_TOOLS"
                dest_dir.mkdir(exist_ok=True)
                dest = dest_dir / item.name
                shutil.move(str(item), str(dest))
                print(f"Moved directory to SUNO_TOOLS: {item.name}")
            elif any(
                keyword in dir_name_lower
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
                dest_dir = zip_path / "MUSIC_ARCHIVES"
                dest_dir.mkdir(exist_ok=True)
                dest = dest_dir / item.name
                shutil.move(str(item), str(dest))
                print(f"Moved directory to MUSIC_ARCHIVES: {item.name}")
            elif any(keyword in dir_name_lower for keyword in ["image", "img", "pic", "art", "visual", "typo"]):
                dest_dir = zip_path / "IMAGE_ARCHIVES"
                dest_dir.mkdir(exist_ok=True)
                dest = dest_dir / item.name
                shutil.move(str(item), str(dest))
                print(f"Moved directory to IMAGE_ARCHIVES: {item.name}")
            elif any(keyword in dir_name_lower for keyword in ["script", "pythons", "python", "automation", "tool"]):
                dest_dir = zip_path / "SCRIPT_ARCHIVES"
                dest_dir.mkdir(exist_ok=True)
                dest = dest_dir / item.name
                shutil.move(str(item), str(dest))
                print(f"Moved directory to SCRIPT_ARCHIVES: {item.name}")
            else:
                dest_dir = zip_path / "OTHER_ARCHIVES"
                dest_dir.mkdir(exist_ok=True)
                dest = dest_dir / item.name
                shutil.move(str(item), str(dest))
                print(f"Moved directory to OTHER_ARCHIVES: {item.name}")

    # Move categorized zip files to their respective directories
    categories = [
        ("BACKUP_ARCHIVES", backup_archives),
        ("SUNO_TOOLS", suno_tools),
        ("MUSIC_ARCHIVES", music_archives),
        ("CODE_ARCHIVES", code_archives),
        ("DOCUMENTATION_ARCHIVES", documentation_archives),
        ("IMAGE_ARCHIVES", image_archives),
        ("SCRIPT_ARCHIVES", script_archives),
        ("OTHER_ARCHIVES", other_archives),
    ]

    for category_name, files in categories:
        if files:
            category_path = zip_path / category_name
            category_path.mkdir(exist_ok=True)

            for file in files:
                dest = category_path / file.name
                # Handle potential naming conflicts
                counter = 1
                while dest.exists():
                    stem = file.stem
                    suffix = file.suffix
                    dest = category_path / f"{stem}_{counter}{suffix}"
                    counter += 1

                shutil.move(str(file), str(dest))
                print(f"Moved {file.name} to {category_name}")

    # Handle loose non-zip files
    for item in zip_path.iterdir():
        if item.is_file() and item.suffix.lower() != ".zip":
            # Determine category based on file extension and name
            name_lower = item.name.lower()

            if any(keyword in name_lower for keyword in ["suno", "suno-", "suno_", "suno."]):
                dest_dir = zip_path / "SUNO_TOOLS"
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
                dest_dir = zip_path / "MUSIC_ARCHIVES"
            elif any(keyword in name_lower for keyword in ["image", "img", "pic", "art", "visual", "typo"]):
                dest_dir = zip_path / "IMAGE_ARCHIVES"
            elif any(keyword in name_lower for keyword in ["script", "py", "sh", "bash", "automation"]):
                dest_dir = zip_path / "SCRIPT_ARCHIVES"
            elif any(keyword in name_lower for keyword in ["doc", "manual", "guide", "readme", "tutorial", "howto"]):
                dest_dir = zip_path / "DOCUMENTATION_ARCHIVES"
            elif any(keyword in name_lower for keyword in ["mp3", "mp4", "wav", "m4a"]):
                dest_dir = zip_path / "MUSIC_ARCHIVES"
            elif any(keyword in name_lower for keyword in ["csv", "json", "txt", "md"]):
                dest_dir = zip_path / "DOCUMENTATION_ARCHIVES"
            else:
                dest_dir = zip_path / "OTHER_ARCHIVES"  # Default

            dest_dir.mkdir(exist_ok=True)
            dest = dest_dir / item.name

            # Handle potential naming conflicts
            counter = 1
            while dest.exists():
                stem = item.stem
                suffix = item.suffix
                dest = dest_dir / f"{stem}_{counter}{suffix}"
                counter += 1

            shutil.move(str(item), str(dest))
            print(f"Moved {item.name} to {dest_dir.name}")

    # Create a summary report
    summary_path = zip_path / "ORGANIZATION_SUMMARY.md"
    with open(summary_path, "w") as f:
        f.write("# Zip Directory Organization Summary\n\n")
        f.write(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")

        # Write the categories with their counts
        f.write("## Categories Summary:\n")
        f.write(f"- BACKUP_ARCHIVES: {len(backup_archives)} files\n")
        f.write(f"- SUNO_TOOLS: {len(suno_tools)} files\n")
        f.write(f"- MUSIC_ARCHIVES: {len(music_archives)} files\n")
        f.write(f"- CODE_ARCHIVES: {len(code_archives)} files\n")
        f.write(f"- DOCUMENTATION_ARCHIVES: {len(documentation_archives)} files\n")
        f.write(f"- IMAGE_ARCHIVES: {len(image_archives)} files\n")
        f.write(f"- SCRIPT_ARCHIVES: {len(script_archives)} files\n")
        f.write(f"- OTHER_ARCHIVES: {len(other_archives)} files\n\n")

        f.write("## Structure:\n")
        f.write("```\n")
        f.write("zip/\n")
        f.write("├── BACKUP_ARCHIVES/        # Large backup files\n")
        f.write("├── SUNO_TOOLS/             # Suno-related tools and exports\n")
        f.write("├── MUSIC_ARCHIVES/         # Music-related archives\n")
        f.write("├── CODE_ARCHIVES/          # Source code archives\n")
        f.write("├── DOCUMENTATION_ARCHIVES/ # Documentation archives\n")
        f.write("├── IMAGE_ARCHIVES/         # Image-related archives\n")
        f.write("├── SCRIPT_ARCHIVES/        # Script-related archives\n")
        f.write("└── OTHER_ARCHIVES/         # Everything else\n")
        f.write("```\n")

    print(f"\nOrganization complete! Summary saved to: {summary_path}")

    # Show final structure
    print("\nFinal directory structure:")
    for subdir in zip_path.iterdir():
        if subdir.is_dir():
            file_count = len([f for f in subdir.iterdir() if f.is_file()])
            print(f"  {subdir.name}/ - {file_count} files")


if __name__ == "__main__":
    organize_zip_directory()
