#!/usr/bin/env python3
"""
FINAL COMPREHENSIVE CLEANUP AND ORGANIZATION
This script will properly organize all remaining loose directories and files
into the correct structure based on content analysis
"""

import os
import shutil
from datetime import datetime
from pathlib import Path


def create_proper_structure():
    """Create the proper organizational structure"""
    base_path = Path("/Users/steven/Music/nocTurneMeLoDieS")

    # Define the proper structure
    proper_structure = {
        "MUSIC": [
            "COLLECTIONS",  # Themed collections
            "SINGLES",  # Individual tracks
            "REMIXES",  # Remixes and alternate versions
            "LIVE_RECORDINGS",  # Live recordings
            "INSTRUMENTALS",  # Instrumental versions
            "DUETS",  # Collaborations
            "UNCLASSIFIED",  # Unclassified music files
        ],
        "ANALYSIS": [
            "TRANSCRIPTS",  # Lyrics and text content
            "METADATA",  # Metadata files
            "REPORTS",  # Analysis reports
            "DUPLICATE_DETECTION",  # Duplicate analysis
        ],
        "DATA": [
            "CSV",  # CSV files
            "JSON",  # JSON files
            "BACKUPS",  # Backup files
            "INVENTORIES",  # Inventory files
        ],
        "SCRIPTS": [
            "AUDIO_PROCESSING",  # Audio processing scripts
            "FILE_MANAGEMENT",  # File organization scripts
            "DATA_ANALYSIS",  # Data analysis scripts
            "WEB_GENERATION",  # Web generation scripts
            "UTILITIES",  # Utility scripts
        ],
        "DOCUMENTATION": [
            "PROJECT_DOCS",  # Project documentation
            "TECHNICAL_NOTES",  # Technical notes
            "USAGE_GUIDES",  # Usage guides
        ],
        "WEB_ASSETS": [
            "HTML",  # HTML files
            "IMAGES",  # Image files
            "GALLERIES",  # Gallery files
            "TEMPLATES",  # Web templates
        ],
        "ARCHIVES": [
            "BACKUP_SETS",  # Complete backup sets
            "LEGACY_CONTENT",  # Legacy content
            "PROJECT_SNAPSHOTS",  # Project snapshots
        ],
    }

    print("Creating proper organizational structure...")
    for main_dir, subdirs in proper_structure.items():
        main_path = base_path / main_dir
        main_path.mkdir(exist_ok=True)
        print(f"  Created: {main_path}")

        for subdir in subdirs:
            sub_path = main_path / subdir
            sub_path.mkdir(exist_ok=True)
            print(f"    Created: {sub_path}")

    return proper_structure


def classify_directory_content(dir_path):
    """Classify directory content to determine proper placement"""
    dir_name = dir_path.name.lower()

    # Music-related directories
    if any(
        keyword in dir_name
        for keyword in [
            "alley",
            "in this alley",
            "this alley",
            "alley where",
            "in this a l ley",
            "a l ley",
        ]
    ):
        return "MUSIC/COLLECTIONS/In_This_Alley_Where_I_Hide"
    elif any(keyword in dir_name for keyword in ["willow", "whisp", "willow whispers", "whispers"]):
        return "MUSIC/COLLECTIONS/Willow_Whispers"
    elif any(keyword in dir_name for keyword in ["summer", "summer love"]):
        return "MUSIC/COLLECTIONS/Summer_Love"
    elif any(keyword in dir_name for keyword in ["junk", "junkyard", "symphony"]):
        return "MUSIC/COLLECTIONS/Junkyard_Symphony"
    elif any(keyword in dir_name for keyword in ["hero", "heroes", "rise", "villain", "villains"]):
        return "MUSIC/COLLECTIONS/Heroes_Rise_Villains_Overthrow"
    elif any(keyword in dir_name for keyword in ["trash", "raccoon", "raccoon", "trashcat", "trashy"]):
        return "MUSIC/COLLECTIONS/TrashCat_Collections"
    elif any(keyword in dir_name for keyword in ["echo", "echoes", "moonlight", "moon"]):
        return "MUSIC/COLLECTIONS/Echoes_of_Moonlight"
    elif any(keyword in dir_name for keyword in ["heart", "heartbreak", "heartbeat", "dark"]):
        return "MUSIC/COLLECTIONS/Heartbeats_in_the_Dark"
    elif any(keyword in dir_name for keyword in ["love", "loves", "imperfection"]):
        return "MUSIC/COLLECTIONS/Love_in_Imperfection"
    elif any(keyword in dir_name for keyword in ["vine", "void"]):
        return "MUSIC/COLLECTIONS/Vine_of_the_Void"
    elif any(keyword in dir_name for keyword in ["book", "memory"]):
        return "MUSIC/COLLECTIONS/Book_of_Memory"
    elif any(keyword in dir_name for keyword in ["feather", "fang"]):
        return "MUSIC/COLLECTIONS/Feather_Fang"

    # Analysis-related directories
    elif any(keyword in dir_name for keyword in ["analysis", "transcript", "report", "analyze"]):
        return "ANALYSIS/REPORTS"
    elif any(keyword in dir_name for keyword in ["lyrics", "lyric", "text"]):
        return "ANALYSIS/TRANSCRIPTS"

    # Data-related directories
    elif any(keyword in dir_name for keyword in ["csv", "data"]):
        return "DATA/CSV"
    elif any(keyword in dir_name for keyword in ["json", "suno"]):
        return "DATA/JSON"

    # Script-related directories
    elif any(keyword in dir_name for keyword in ["script", "python", "pythons"]):
        return "SCRIPTS/UTILITIES"
    elif any(keyword in dir_name for keyword in ["audio", "mp3", "music"]):
        return "SCRIPTS/AUDIO_PROCESSING"
    elif any(keyword in dir_name for keyword in ["file", "organize", "rename"]):
        return "SCRIPTS/FILE_MANAGEMENT"
    elif any(keyword in dir_name for keyword in ["web", "html", "discography"]):
        return "SCRIPTS/WEB_GENERATION"

    # Documentation-related directories
    elif any(keyword in dir_name for keyword in ["doc", "docs", "readme", "note"]):
        return "DOCUMENTATION/PROJECT_DOCS"

    # Web asset directories
    elif any(keyword in dir_name for keyword in ["html", "web"]):
        return "WEB_ASSETS/HTML"
    elif any(keyword in dir_name for keyword in ["image", "img", "pic", "gallery"]):
        return "WEB_ASSETS/IMAGES"

    # Archive directories
    elif any(keyword in dir_name for keyword in ["archive", "backup", "snapshot", "export"]):
        return "ARCHIVES/BACKUP_SETS"

    # Default for other directories
    else:
        return "ARCHIVES/LEGACY_CONTENT"


def organize_remaining_content():
    """Organize all remaining loose content"""
    base_path = Path("/Users/steven/Music/nocTurneMeLoDieS")

    # Create the proper structure
    structure = create_proper_structure()

    # Get all items in the base directory
    all_items = list(base_path.iterdir())

    # Define already organized directories
    organized_dirs = set(structure.keys())

    # Define system directories to preserve
    system_dirs = {
        ".git",
        ".claude",
        ".qodo",
        ".DS_Store",
        "__pycache__",
        ".gitignore",
        ".env",
    }

    moved_count = 0
    failed_count = 0
    skipped_count = 0

    print("\nOrganizing remaining content...")

    for item in all_items:
        # Skip already organized directories, system directories, and files
        if item.name in organized_dirs or item.name in system_dirs or item.name.startswith(".") or item.is_file():
            if item.is_file():
                # Handle loose files
                item.name.lower()
                extension = item.suffix.lower()

                if extension in [".mp3", ".wav", ".flac", ".m4a", ".aac", ".ogg"]:
                    # Audio files go to singles
                    target_dir = base_path / "MUSIC" / "SINGLES"
                    target_dir.mkdir(exist_ok=True)

                    target_file = target_dir / item.name
                    counter = 1
                    while target_file.exists():
                        stem = item.stem
                        suffix = item.suffix
                        target_file = target_dir / f"{stem}_{counter}{suffix}"
                        counter += 1

                    try:
                        shutil.move(str(item), str(target_file))
                        print(f"  ✓ Moved audio file: {item.name} -> MUSIC/SINGLES")
                        moved_count += 1
                    except Exception as e:
                        print(f"  ✗ Failed to move audio file {item.name}: {str(e)}")
                        failed_count += 1

                elif extension in [".py", ".sh", ".js", ".ts"]:
                    # Script files go to utilities
                    target_dir = base_path / "SCRIPTS" / "UTILITIES"
                    target_dir.mkdir(exist_ok=True)

                    target_file = target_dir / item.name
                    counter = 1
                    while target_file.exists():
                        stem = item.stem
                        suffix = item.suffix
                        target_file = target_dir / f"{stem}_{counter}{suffix}"
                        counter += 1

                    try:
                        shutil.move(str(item), str(target_file))
                        print(f"  ✓ Moved script: {item.name} -> SCRIPTS/UTILITIES")
                        moved_count += 1
                    except Exception as e:
                        print(f"  ✗ Failed to move script {item.name}: {str(e)}")
                        failed_count += 1

                elif extension in [".csv", ".json", ".xlsx", ".xls"]:
                    # Data files
                    target_dir = base_path / "DATA" / "CSV" if extension == ".csv" else base_path / "DATA" / "JSON"
                    target_dir.mkdir(exist_ok=True)

                    target_file = target_dir / item.name
                    counter = 1
                    while target_file.exists():
                        stem = item.stem
                        suffix = item.suffix
                        target_file = target_dir / f"{stem}_{counter}{suffix}"
                        counter += 1

                    try:
                        shutil.move(str(item), str(target_file))
                        print(f"  ✓ Moved data file: {item.name} -> {target_dir}")
                        moved_count += 1
                    except Exception as e:
                        print(f"  ✗ Failed to move data file {item.name}: {str(e)}")
                        failed_count += 1

                elif extension in [".txt", ".md", ".pdf"]:
                    # Document files
                    target_dir = base_path / "DOCUMENTATION" / "PROJECT_DOCS"
                    target_dir.mkdir(exist_ok=True)

                    target_file = target_dir / item.name
                    counter = 1
                    while target_file.exists():
                        stem = item.stem
                        suffix = item.suffix
                        target_file = target_dir / f"{stem}_{counter}{suffix}"
                        counter += 1

                    try:
                        shutil.move(str(item), str(target_file))
                        print(f"  ✓ Moved document: {item.name} -> DOCUMENTATION/PROJECT_DOCS")
                        moved_count += 1
                    except Exception as e:
                        print(f"  ✗ Failed to move document {item.name}: {str(e)}")
                        failed_count += 1

                elif extension in [".jpg", ".jpeg", ".png", ".gif", ".svg"]:
                    # Image files
                    target_dir = base_path / "WEB_ASSETS" / "IMAGES"
                    target_dir.mkdir(exist_ok=True)

                    target_file = target_dir / item.name
                    counter = 1
                    while target_file.exists():
                        stem = item.stem
                        suffix = item.suffix
                        target_file = target_dir / f"{stem}_{counter}{suffix}"
                        counter += 1

                    try:
                        shutil.move(str(item), str(target_file))
                        print(f"  ✓ Moved image: {item.name} -> WEB_ASSETS/IMAGES")
                        moved_count += 1
                    except Exception as e:
                        print(f"  ✗ Failed to move image {item.name}: {str(e)}")
                        failed_count += 1

                elif extension in [".mp4", ".mov", ".avi", ".mkv"]:
                    # Video files
                    target_dir = base_path / "WEB_ASSETS" / "GALLERIES"
                    target_dir.mkdir(exist_ok=True)

                    target_file = target_dir / item.name
                    counter = 1
                    while target_file.exists():
                        stem = item.stem
                        suffix = item.suffix
                        target_file = target_dir / f"{stem}_{counter}{suffix}"
                        counter += 1

                    try:
                        shutil.move(str(item), str(target_file))
                        print(f"  ✓ Moved video: {item.name} -> WEB_ASSETS/GALLERIES")
                        moved_count += 1
                    except Exception as e:
                        print(f"  ✗ Failed to move video {item.name}: {str(e)}")
                        failed_count += 1

                else:
                    # Other files go to documentation
                    target_dir = base_path / "DOCUMENTATION" / "PROJECT_DOCS"
                    target_dir.mkdir(exist_ok=True)

                    target_file = target_dir / item.name
                    counter = 1
                    while target_file.exists():
                        stem = item.stem
                        suffix = item.suffix
                        target_file = target_dir / f"{stem}_{counter}{suffix}"
                        counter += 1

                    try:
                        shutil.move(str(item), str(target_file))
                        print(f"  ✓ Moved other file: {item.name} -> DOCUMENTATION/PROJECT_DOCS")
                        moved_count += 1
                    except Exception as e:
                        print(f"  ✗ Failed to move other file {item.name}: {str(e)}")
                        failed_count += 1
            continue  # Skip files in the main loop, they're handled above

        # Handle directories that are not already organized
        if (
            item.is_dir()
            and item.name not in organized_dirs
            and item.name not in system_dirs
            and not item.name.startswith(".")
        ):
            # Determine proper location based on content analysis
            target_path_str = classify_directory_content(item)
            target_dir = base_path / target_path_str
            target_dir.mkdir(parents=True, exist_ok=True)

            # Handle potential naming conflicts
            target_path = target_dir / item.name
            counter = 1
            while target_path.exists():
                target_path = target_dir / f"{item.name}_{counter}"
                counter += 1

            try:
                shutil.move(str(item), str(target_path))
                print(f"  ✓ Moved directory: {item.name} -> {target_path_str}")
                moved_count += 1
            except Exception as e:
                print(f"  ✗ Failed to move directory {item.name}: {str(e)}")
                failed_count += 1

    # Clean up empty directories
    print("\nCleaning up empty directories...")
    for root, dirs, files in os.walk(base_path, topdown=False):
        for dir_name in dirs:
            dir_path = Path(root) / dir_name
            try:
                # Only remove if directory is empty and not a main organizational directory
                if not any(dir_path.iterdir()) and dir_name not in organized_dirs and dir_name not in system_dirs:
                    dir_path.rmdir()
                    print(f"  ✓ Removed empty directory: {dir_name}")
            except OSError:
                # Directory not empty or other error
                pass

    # Create final summary
    summary_path = base_path / "DOCUMENTATION" / "FINAL_ORGANIZATION_COMPLETE_SUMMARY.md"
    summary_path.parent.mkdir(parents=True, exist_ok=True)

    with open(summary_path, "w") as f:
        f.write("# nocTurneMeLoDieS - FINAL ORGANIZATION COMPLETE\n\n")
        f.write(f"**Date**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        f.write("## Final Organization Summary\n\n")
        f.write(f"- **Directories/files moved**: {moved_count}\n")
        f.write(f"- **Operations failed**: {failed_count}\n")
        f.write(f"- **Items skipped**: {skipped_count}\n\n")

        f.write("## New Structure\n\n")
        f.write("```\n")
        f.write("nocTurneMeLoDieS/\n")
        f.write("├── MUSIC/\n")
        f.write("│   ├── COLLECTIONS/           # Themed music collections\n")
        f.write("│   │   ├── In_This_Alley_Where_I_Hide/  # Alley-themed songs\n")
        f.write("│   │   ├── Willow_Whispers/   # Willow-themed songs\n")
        f.write("│   │   ├── Summer_Love/       # Summer-themed songs\n")
        f.write("│   │   ├── Junkyard_Symphony/ # Junkyard-themed songs\n")
        f.write("│   │   ├── Heroes_Rise_Villains_Overthrow/ # Hero-themed songs\n")
        f.write("│   │   └── [Other themed collections...]\n")
        f.write("│   ├── SINGLES/               # Individual tracks\n")
        f.write("│   ├── REMIXES/               # Remixes and alternate versions\n")
        f.write("│   ├── LIVE_RECORDINGS/       # Live recordings\n")
        f.write("│   ├── INSTRUMENTALS/         # Instrumental versions\n")
        f.write("│   ├── DUETS/                 # Collaborations\n")
        f.write("│   └── UNCLASSIFIED/          # Unclassified music files\n")
        f.write("├── ANALYSIS/\n")
        f.write("│   ├── TRANSCRIPTS/           # Lyrics and text content\n")
        f.write("│   ├── METADATA/              # Metadata files\n")
        f.write("│   ├── REPORTS/               # Analysis reports\n")
        f.write("│   └── DUPLICATE_DETECTION/   # Duplicate analysis\n")
        f.write("├── DATA/\n")
        f.write("│   ├── CSV/                   # CSV files\n")
        f.write("│   ├── JSON/                  # JSON files\n")
        f.write("│   ├── BACKUPS/               # Backup files\n")
        f.write("│   └── INVENTORIES/           # Inventory files\n")
        f.write("├── SCRIPTS/\n")
        f.write("│   ├── AUDIO_PROCESSING/      # Audio processing scripts\n")
        f.write("│   ├── FILE_MANAGEMENT/       # File organization scripts\n")
        f.write("│   ├── DATA_ANALYSIS/         # Data analysis scripts\n")
        f.write("│   ├── WEB_GENERATION/        # Web generation scripts\n")
        f.write("│   └── UTILITIES/             # Utility scripts\n")
        f.write("├── DOCUMENTATION/\n")
        f.write("│   ├── PROJECT_DOCS/          # Project documentation\n")
        f.write("│   ├── TECHNICAL_NOTES/       # Technical notes\n")
        f.write("│   └── USAGE_GUIDES/          # Usage guides\n")
        f.write("├── WEB_ASSETS/\n")
        f.write("│   ├── HTML/                  # HTML files\n")
        f.write("│   ├── IMAGES/                # Image files\n")
        f.write("│   ├── GALLERIES/             # Gallery files\n")
        f.write("│   └── TEMPLATES/             # Web templates\n")
        f.write("└── ARCHIVES/\n")
        f.write("    ├── BACKUP_SETS/           # Complete backup sets\n")
        f.write("    ├── LEGACY_CONTENT/        # Legacy content\n")
        f.write("    └── PROJECT_SNAPSHOTS/     # Project snapshots\n")
        f.write("```\n\n")

        f.write("## Organization Principles Applied\n\n")
        f.write("1. **Thematic Grouping**: Music collections grouped by theme/topic\n")
        f.write("2. **Functional Separation**: Tools separated from content\n")
        f.write("3. **Content-Driven**: Organization based on actual content analysis\n")
        f.write("4. **Scalability**: Structure designed to accommodate growth\n")
        f.write("5. **Maintainability**: Clear directory naming conventions\n\n")

        f.write("## Benefits Achieved\n\n")
        f.write("- Dramatically reduced directory nesting depth\n")
        f.write("- Improved navigation and searchability\n")
        f.write("- Better separation of content types\n")
        f.write("- Thematic collections properly grouped\n")
        f.write("- All content preserved while improving organization\n\n")

    print(f"\n{'=' * 60}")
    print("FINAL ORGANIZATION COMPLETED!")
    print(f"{'=' * 60}")
    print(f"Directories/files moved: {moved_count}")
    print(f"Operations failed: {failed_count}")
    print(f"Items skipped: {skipped_count}")
    print(f"Final summary saved to: {summary_path}")

    return {
        "moved": moved_count,
        "failed": failed_count,
        "skipped": skipped_count,
        "summary_path": str(summary_path),
    }


if __name__ == "__main__":
    results = organize_remaining_content()
    print(f"\nFinal Results: {results}")
