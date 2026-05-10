#!/usr/bin/env python3
"""
File Organization Script
Organizes and sorts the analyzed files into recommended structure.
"""

import shutil
from pathlib import Path

# Base directory
BASE_DIR = Path("/Users/steven/Downloads/Misc")

# File mappings: (source, destination_folder, new_name)
FILE_MAPPINGS = [
    # Image Generation Frameworks
    (
        "unified_digital_dive_framework.yaml",
        "Frameworks",
        "digital_dive_v1_unified.yaml",
    ),
    (
        "digital_dive_two_batch_template.yaml",
        "Frameworks",
        "digital_dive_v2_batch_template.yaml",
    ),
    ("lyrics_bound_framework.yaml", "Frameworks", "lyrics_bound_framework.yaml"),
    # Configuration Files
    ("fabric_temp.txt", "Config", "fabric.env"),
    # API Documentation
    ("plugin-redoc-0.yaml", "API_Docs", "mistral_ai_openapi.yaml"),
]


def create_directories():
    """Create the recommended directory structure."""
    directories = ["Frameworks", "Config", "API_Docs"]
    for dir_name in directories:
        dir_path = BASE_DIR / dir_name
        dir_path.mkdir(exist_ok=True)
        print(f"✓ Created/verified directory: {dir_path}")


def organize_files(dry_run=True):
    """Organize files according to recommendations."""
    if dry_run:
        print("\n🔍 DRY RUN MODE - No files will be moved\n")
    else:
        print("\n📦 MOVING FILES\n")

    for source_file, dest_folder, new_name in FILE_MAPPINGS:
        source_path = BASE_DIR / source_file
        dest_dir = BASE_DIR / dest_folder
        dest_path = dest_dir / new_name

        if not source_path.exists():
            print(f"⚠️  Source file not found: {source_path}")
            continue

        if dry_run:
            print(f"Would move: {source_file}")
            print(f"    → {dest_folder}/{new_name}")
        else:
            try:
                shutil.move(str(source_path), str(dest_path))
                print(f"✓ Moved: {source_file} → {dest_folder}/{new_name}")
            except Exception as e:
                print(f"✗ Error moving {source_file}: {e}")


def main():
    """Main execution."""
    print("=" * 60)
    print("File Organization Script")
    print("=" * 60)

    # Create directories
    create_directories()

    # Show what would happen
    organize_files(dry_run=True)

    # Ask for confirmation
    print("\n" + "=" * 60)
    response = input("Proceed with file organization? (yes/no): ").strip().lower()

    if response in ["yes", "y"]:
        organize_files(dry_run=False)
        print("\n✅ File organization complete!")
    else:
        print("\n❌ Operation cancelled.")


if __name__ == "__main__":
    main()
