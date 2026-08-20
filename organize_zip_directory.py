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

    # Create new structure within the zip directory
    new_structure = {
        "BACKUP_ARCHIVES": [],  # Large backup files like mp3.zip, NocTurnE-meLoDieS-*.zip
        "SUNO_TOOLS": [],  # Suno-related tools and exports
        "MUSIC_ARCHIVES": [],  # Music-related archives
        "CODE_ARCHIVES": [],  # Source code archives
        "DOCUMENTATION_ARCHIVES": [],  # Documentation archives
        "IMAGE_ARCHIVES": [],  # Image-related archives
        "SCRIPT_ARCHIVES": [],  # Script-related archives
        "OTHER_ARCHIVES": [],  # Everything else
    }

    print("Analyzing zip directory contents...")

    # Categorize files based on name patterns
    for item in zip_path.iterdir():
        if item.is_file() and item.suffix.lower() == ".zip":
            name_lower = item.name.lower()

            if any(keyword in name_lower for keyword in ["mp3", "backup", "nocturnemelodies", "2025", "2026"]):
                new_structure["BACKUP_ARCHIVES"].append(item)
            elif any(keyword in name_lower for keyword in ["suno", "suno-", "suno_"]):
                new_structure["SUNO_TOOLS"].append(item)
            elif any(keyword in name_lower for keyword in ["trash", "raccoon", "alley", "love", "willow", "hero"]):
                new_structure["MUSIC_ARCHIVES"].append(item)
            elif any(keyword in name_lower for keyword in ["source", "code", "dev", "src"]):
                new_structure["CODE_ARCHIVES"].append(item)
            elif any(keyword in name_lower for keyword in ["doc", "manual", "guide", "readme"]):
                new_structure["DOCUMENTATION_ARCHIVES"].append(item)
            elif any(keyword in name_lower for keyword in ["image", "img", "pic", "photo", "art"]):
                new_structure["IMAGE_ARCHIVES"].append(item)
            elif any(keyword in name_lower for keyword in ["script", "py", "sh", "bash"]):
                new_structure["SCRIPT_ARCHIVES"].append(item)
            else:
                new_structure["OTHER_ARCHIVES"].append(item)
        elif item.is_dir() and item.name not in [".", ".."]:
            # Handle directories - move them to appropriate locations based on content
            dir_name_lower = item.name.lower()

            if any(keyword in dir_name_lower for keyword in ["suno", "suno-"]):
                dest = zip_path / "SUNO_TOOLS" / item.name
                (zip_path / "SUNO_TOOLS").mkdir(exist_ok=True)
                shutil.move(str(item), str(dest))
                print(f"Moved directory to SUNO_TOOLS: {item.name}")
            elif any(keyword in dir_name_lower for keyword in ["trash", "raccoon", "alley", "love", "willow", "hero"]):
                dest = zip_path / "MUSIC_ARCHIVES" / item.name
                (zip_path / "MUSIC_ARCHIVES").mkdir(exist_ok=True)
                shutil.move(str(item), str(dest))
                print(f"Moved directory to MUSIC_ARCHIVES: {item.name}")
            elif any(keyword in dir_name_lower for keyword in ["image", "img", "pic", "art"]):
                dest = zip_path / "IMAGE_ARCHIVES" / item.name
                (zip_path / "IMAGE_ARCHIVES").mkdir(exist_ok=True)
                shutil.move(str(item), str(dest))
                print(f"Moved directory to IMAGE_ARCHIVES: {item.name}")
            else:
                dest = zip_path / "OTHER_ARCHIVES" / item.name
                (zip_path / "OTHER_ARCHIVES").mkdir(exist_ok=True)
                shutil.move(str(item), str(dest))
                print(f"Moved directory to OTHER_ARCHIVES: {item.name}")

    # Move categorized zip files to their respective directories
    for category, files in new_structure.items():
        if files:
            category_path = zip_path / category
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
                print(f"Moved {file.name} to {category}")

    # Handle loose non-zip files
    for item in zip_path.iterdir():
        if item.is_file() and item.suffix.lower() != ".zip":
            # Determine category based on file extension
            if item.suffix.lower() in [".py", ".sh", ".js", ".ts"]:
                dest_dir = zip_path / "SCRIPT_ARCHIVES"
            elif item.suffix.lower() in [".csv", ".json", ".txt"]:
                dest_dir = zip_path / "DOCUMENTATION_ARCHIVES"
            elif item.suffix.lower() in [".html", ".md"]:
                dest_dir = zip_path / "DOCUMENTATION_ARCHIVES"
            elif item.suffix.lower() in [".mp3", ".mp4", ".wav", ".m4a"]:
                dest_dir = zip_path / "MUSIC_ARCHIVES"
            elif item.suffix.lower() in [".jpg", ".jpeg", ".png", ".gif"]:
                dest_dir = zip_path / "IMAGE_ARCHIVES"
            else:
                dest_dir = zip_path / "DOCUMENTATION_ARCHIVES"  # Default

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

        for category, files in new_structure.items():
            f.write(f"## {category}\n")
            f.write(f"- Files moved: {len(files)}\n")
            for file in files:
                f.write(f"  - {file.name}\n")
            f.write("\n")

        f.write("## Structure:\n")
        f.write("```\n")
        f.write("zip/\n")
        f.write("├── BACKUP_ARCHIVES/     # Large backup files\n")
        f.write("├── SUNO_TOOLS/          # Suno-related tools and exports\n")
        f.write("├── MUSIC_ARCHIVES/      # Music-related archives\n")
        f.write("├── CODE_ARCHIVES/       # Source code archives\n")
        f.write("├── DOCUMENTATION_ARCHIVES/ # Documentation archives\n")
        f.write("├── IMAGE_ARCHIVES/      # Image-related archives\n")
        f.write("├── SCRIPT_ARCHIVES/     # Script-related archives\n")
        f.write("└── OTHER_ARCHIVES/      # Everything else\n")
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
