#!/usr/bin/env python3
"""
Execute reorganization in priority order:
1. Remove content duplicates
2. Implement service-based structure
3. Reorganize social_media/
"""

import sys
import shutil
from pathlib import Path
import csv

# Avoid importing local files
if str(Path(__file__).parent) in sys.path:
    sys.path.remove(str(Path(__file__).parent))


def remove_content_duplicates(root_dir, dry_run=True):
    """Remove files identified as content duplicates."""
    root_path = Path(root_dir)
    media_path = root_path / "MEDIA_PROCESSING"

    print("=" * 80)
    print("1️⃣  REMOVING CONTENT DUPLICATES")
    print("=" * 80)
    print()

    # Confirmed duplicates from content analysis
    duplicates_to_remove = [
        media_path / "upscale" / "upscale--.py",  # duplicate of upscale.py
        media_path
        / "upscale"
        / "upscale--_media_image.py",  # duplicate of upscale copy.py
    ]

    removed = 0
    for file_path in duplicates_to_remove:
        if file_path.exists():
            if dry_run:
                print(f"   Would delete: {file_path.relative_to(root_path)}")
            else:
                try:
                    file_path.unlink()
                    print(f"   ✅ Deleted: {file_path.relative_to(root_path)}")
                    removed += 1
                except Exception as e:
                    print(f"   ❌ Error: {e}")
        else:
            print(f"   ⚠️  Not found: {file_path.relative_to(root_path)}")

    print()
    return removed


def create_service_based_structure(root_dir, dry_run=True):
    """Create service-based directory structure."""
    root_path = Path(root_dir)
    media_path = root_path / "MEDIA_PROCESSING"

    print("=" * 80)
    print("2️⃣  CREATING SERVICE-BASED STRUCTURE")
    print("=" * 80)
    print()

    # Read functionality groups to determine service-based organization
    func_csv = root_path / "FUNCTIONALITY_GROUPS.csv"
    if not func_csv.exists():
        print("   ⚠️  FUNCTIONALITY_GROUPS.csv not found")
        print("   Run group_by_functionality.py first")
        return

    # Parse CSV to group by service
    service_groups = {
        "instagram": [],
        "youtube": [],
        "audio_apis": [],
        "image_processing": [],
        "video_processing": [],
        "upscaling": [],
        "file_operations": [],
    }

    with open(func_csv, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            folder = row["folder"]
            file = row["file"]
            keywords = row["keywords"].lower()
            functionality = row["functionality"]

            file_path = media_path / folder / file

            # Determine service based on keywords and functionality
            if "instagram" in keywords:
                service_groups["instagram"].append((folder, file, file_path))
            elif "youtube" in keywords:
                service_groups["youtube"].append((folder, file, file_path))
            elif "audio" in keywords or "polly" in keywords or "tts" in keywords:
                service_groups["audio_apis"].append((folder, file, file_path))
            elif "upscal" in keywords or folder == "upscale":
                service_groups["upscaling"].append((folder, file, file_path))
            elif "image" in keywords and "processing" in keywords:
                service_groups["image_processing"].append((folder, file, file_path))
            elif "video" in keywords and "processing" in keywords:
                service_groups["video_processing"].append((folder, file, file_path))
            elif functionality == "file_operations":
                service_groups["file_operations"].append((folder, file, file_path))

    # Create new structure
    new_structure = {
        "apis": {"instagram": [], "youtube": [], "audio_apis": []},
        "processing": {"image_processing": [], "video_processing": [], "upscaling": []},
        "file_operations": [],
    }

    # Map files to new structure
    for folder, file, file_path in service_groups["instagram"]:
        new_structure["apis"]["instagram"].append((file_path, f"apis/instagram/{file}"))

    for folder, file, file_path in service_groups["youtube"]:
        new_structure["apis"]["youtube"].append((file_path, f"apis/youtube/{file}"))

    for folder, file, file_path in service_groups["audio_apis"]:
        new_structure["apis"]["audio_apis"].append(
            (file_path, f"apis/audio_apis/{file}")
        )

    for folder, file, file_path in service_groups["upscaling"]:
        new_structure["processing"]["upscaling"].append(
            (file_path, f"processing/upscaling/{file}")
        )

    # Show plan
    print("Service-based structure plan:")
    print()
    print("📁 apis/")
    print(f"   ├── instagram/ ({len(new_structure['apis']['instagram'])} files)")
    print(f"   ├── youtube/ ({len(new_structure['apis']['youtube'])} files)")
    print(f"   └── audio_apis/ ({len(new_structure['apis']['audio_apis'])} files)")
    print()
    print("📁 processing/")
    print(f"   └── upscaling/ ({len(new_structure['processing']['upscaling'])} files)")
    print()

    if dry_run:
        print("🔍 DRY RUN - Structure would be created")
        print("   Run with --execute to create directories")
    else:
        # Create directories
        for category, services in new_structure.items():
            if category == "apis":
                for service, files in services.items():
                    if files:
                        dir_path = media_path / "apis" / service
                        dir_path.mkdir(parents=True, exist_ok=True)
                        print(f"   ✅ Created: apis/{service}/")
            elif category == "processing":
                for service, files in services.items():
                    if files:
                        dir_path = media_path / "processing" / service
                        dir_path.mkdir(parents=True, exist_ok=True)
                        print(f"   ✅ Created: processing/{service}/")

    print()
    return new_structure


def reorganize_social_media(root_dir, dry_run=True):
    """Reorganize social_media folder by functionality."""
    root_path = Path(root_dir)
    social_path = root_path / "MEDIA_PROCESSING" / "social_media"

    if not social_path.exists():
        print("   ⚠️  social_media folder not found")
        return

    print("=" * 80)
    print("3️⃣  REORGANIZING social_media/")
    print("=" * 80)
    print()

    # Read functionality groups
    func_csv = root_path / "FUNCTIONALITY_GROUPS.csv"
    if not func_csv.exists():
        print("   ⚠️  FUNCTIONALITY_GROUPS.csv not found")
        return

    # Group files from social_media
    groups = {"instagram": [], "actions": [], "tests": [], "uploads": []}

    with open(func_csv, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row["folder"] == "social_media":
                file = row["file"]
                keywords = row["keywords"].lower()
                file_path = social_path / file

                if "test" in file.lower():
                    groups["tests"].append((file_path, f"tests/{file}"))
                elif "upload" in file.lower() or "newupload" in file.lower():
                    groups["uploads"].append((file_path, f"uploads/{file}"))
                elif any(x in keywords for x in ["like", "follow", "unfollow"]):
                    groups["actions"].append((file_path, f"actions/{file}"))
                elif "instagram" in keywords or "bot" in keywords:
                    groups["instagram"].append((file_path, f"instagram/{file}"))
                else:
                    groups["instagram"].append((file_path, f"instagram/{file}"))

    # Show plan
    print("Reorganization plan for social_media/:")
    print()
    print(f"📁 instagram/ ({len(groups['instagram'])} files)")
    print(f"📁 actions/ ({len(groups['actions'])} files)")
    print(f"📁 uploads/ ({len(groups['uploads'])} files)")
    print(f"📁 tests/ ({len(groups['tests'])} files)")
    print()

    if dry_run:
        print("🔍 DRY RUN - Files would be moved")
        print("   Sample moves:")
        for group_name, files in groups.items():
            if files:
                print(f"   {group_name}/:")
                for src, dst in files[:3]:
                    print(f"      {src.name} → {dst}")
                if len(files) > 3:
                    print(f"      ... and {len(files) - 3} more")
                print()
    else:
        # Create directories and move files
        moved = 0
        for group_name, files in groups.items():
            if files:
                group_dir = social_path / group_name
                group_dir.mkdir(exist_ok=True)

                for src, dst in files:
                    if src.exists():
                        try:
                            dest_path = social_path / dst
                            dest_path.parent.mkdir(parents=True, exist_ok=True)
                            shutil.move(str(src), str(dest_path))
                            print(f"   ✅ Moved: {src.name} → {dst}")
                            moved += 1
                        except Exception as e:
                            print(f"   ❌ Error moving {src.name}: {e}")

        print()
        print(f"   ✅ Moved {moved} files")

    print()
    return groups


def main():
    """Main execution."""
    root_directory = Path.home() / "pythons"
    dry_run = "--execute" not in sys.argv

    if dry_run:
        print("🔍 DRY RUN MODE - No changes will be made")
        print("   Run with --execute to apply changes")
        print()

    # 1. Remove duplicates
    removed = remove_content_duplicates(root_directory, dry_run)

    # 2. Create service-based structure
    create_service_based_structure(root_directory, dry_run)

    # 3. Reorganize social_media
    social_groups = reorganize_social_media(root_directory, dry_run)

    # Summary
    print("=" * 80)
    print("📊 SUMMARY")
    print("=" * 80)
    print()
    print(f"1. Duplicates removed: {removed}")
    print("2. Service structure: Created")
    print(
        f"3. social_media reorganized: {sum(len(files) for files in social_groups.values())} files"
    )
    print()

    if dry_run:
        print("💡 Run with --execute to apply these changes")
    else:
        print("✅ All changes applied!")


if __name__ == "__main__":
    main()
