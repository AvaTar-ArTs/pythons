#!/usr/bin/env python3
"""
IMPLEMENTATION SCRIPT FOR PYTHON SCRIPTS ORGANIZATION

This script implements the organization, sorting, and deduplication
plan for /Users/steven/pythons directory.

IMPORTANT: This script will make actual changes to your file system.
Please review carefully and make a backup before running.
"""

import shutil
from pathlib import Path
import hashlib


def get_file_category_mapping():
    """
    Returns a mapping of files to their target categories based on analysis.
    This is a simplified version - a full implementation would have more detailed rules.
    """
    base_dir = Path("/Users/steven/pythons")
    file_mapping = {}

    # Find all Python files
    all_scripts = list(base_dir.rglob("*.py"))

    for script_path in all_scripts:
        # Skip this script itself
        if "implement_organization.py" in str(script_path):
            continue

        str_path = str(script_path)
        relative_path = script_path.relative_to(base_dir)

        # Categorize based on file path and name
        if any(keyword in str_path.lower() for keyword in ["organize", "reorganize"]):
            if "organize" not in str(file_mapping.get("core_tools/organization", [])):
                file_mapping[str_path] = "core_tools/organization"
        elif any(
            keyword in str_path.lower()
            for keyword in ["cleanup", "clean", "final", "complete"]
        ):
            file_mapping[str_path] = "core_tools/cleanup"
        elif any(
            keyword in str_path.lower()
            for keyword in ["duplicate", "similarity", "similar", "dedupe"]
        ):
            file_mapping[str_path] = "core_tools/duplicate_management"
        elif any(
            keyword in str_path.lower()
            for keyword in ["analyze", "analysis", "scanner"]
        ):
            file_mapping[str_path] = "core_tools/analysis"
        elif any(
            keyword in str_path.lower()
            for keyword in ["openai", "claude", "anthropic", "gemini", "groq"]
        ):
            if any(
                keyword in str_path.lower()
                for keyword in ["generate", "text", "content"]
            ):
                file_mapping[str_path] = "ai_ml_tools/content_generation"
            else:
                file_mapping[str_path] = "ai_ml_tools/automation"
        elif (
            any("audio" in part.lower() for part in relative_path.parts)
            or "audio" in str_path.lower()
        ):
            file_mapping[str_path] = "media_tools/audio"
        elif (
            any("video" in part.lower() for part in relative_path.parts)
            or "video" in str_path.lower()
        ):
            file_mapping[str_path] = "media_tools/video"
        elif (
            any("image" in part.lower() for part in relative_path.parts)
            or "image" in str_path.lower()
        ):
            file_mapping[str_path] = "media_tools/image"
        elif "youtube" in str_path.lower():
            file_mapping[str_path] = "automation_tools/youtube"
        elif "instagram" in str_path.lower():
            file_mapping[str_path] = "automation_tools/instagram"
        elif any(
            keyword in str_path.lower() for keyword in ["tiktok", "twitter", "social"]
        ):
            file_mapping[str_path] = "automation_tools/general"
        elif any(
            keyword in str_path.lower() for keyword in ["data", "csv", "json", "pandas"]
        ):
            if any(keyword in str_path.lower() for keyword in ["convert", "transform"]):
                file_mapping[str_path] = "data_tools/conversion"
            else:
                file_mapping[str_path] = "data_tools/utilities"
        elif (
            any("file" in part.lower() for part in relative_path.parts)
            or "file" in str_path.lower()
        ):
            if any(
                keyword in str_path.lower()
                for keyword in ["op", "operation", "move", "copy"]
            ):
                file_mapping[str_path] = "utilities/file_ops"
            else:
                file_mapping[str_path] = "utilities/misc"
        elif (
            any("web" in part.lower() for part in relative_path.parts)
            or "web" in str_path.lower()
        ):
            file_mapping[str_path] = "utilities/web"
        else:
            file_mapping[str_path] = "utilities/misc"

    return file_mapping


def find_content_duplicates():
    """Find files with identical content"""
    base_dir = Path("/Users/steven/pythons")
    content_map = {}
    all_scripts = list(base_dir.rglob("*.py"))

    for script_path in all_scripts:
        # Skip this script itself
        if "implement_organization.py" in str(script_path):
            continue

        try:
            with open(script_path, "r", encoding="utf-8", errors="ignore") as f:
                content = f.read()

            # Compute hash of content
            content_hash = hashlib.md5(content.encode("utf-8")).hexdigest()

            if content_hash not in content_map:
                content_map[content_hash] = []
            content_map[content_hash].append(str(script_path))
        except Exception as e:
            print(f"Error reading {script_path}: {e}")

    # Return only content hashes with more than one file
    return {k: v for k, v in content_map.items() if len(v) > 1}


def implement_organization():
    base_dir = Path("/Users/steven/pythons")

    # Create target directories
    directories = [
        base_dir / "core_tools" / "organization",
        base_dir / "core_tools" / "cleanup",
        base_dir / "core_tools" / "duplicate_management",
        base_dir / "core_tools" / "analysis",
        base_dir / "ai_ml_tools" / "content_generation",
        base_dir / "ai_ml_tools" / "automation",
        base_dir / "media_tools" / "audio",
        base_dir / "media_tools" / "video",
        base_dir / "media_tools" / "image",
        base_dir / "automation_tools" / "youtube",
        base_dir / "automation_tools" / "instagram",
        base_dir / "automation_tools" / "general",
        base_dir / "data_tools" / "conversion",
        base_dir / "data_tools" / "utilities",
        base_dir / "utilities" / "file_ops",
        base_dir / "utilities" / "web",
        base_dir / "utilities" / "misc",
    ]

    for directory in directories:
        directory.mkdir(parents=True, exist_ok=True)

    print("Created directory structure")

    # Get file mappings
    file_mapping = get_file_category_mapping()

    # Move files to appropriate directories
    move_operations = []
    for source_path_str, target_category in file_mapping.items():
        source_path = Path(source_path_str)
        if source_path.exists():  # Only process if file still exists
            target_dir = base_dir / target_category
            target_path = target_dir / source_path.name

            # Handle naming conflicts by adding a number
            counter = 1
            original_target_path = target_path
            while target_path.exists():
                stem = original_target_path.stem
                suffix = original_target_path.suffix
                target_path = target_dir / f"{stem}_{counter}{suffix}"
                counter += 1

            move_operations.append((source_path, target_path))

    # Perform the move operations
    for source, target in move_operations:
        try:
            # Make sure we're not moving to the same location
            if source != target:
                shutil.move(str(source), str(target))
                print(f"Moved: {source.name} -> {target.parent.name}/")
        except Exception as e:
            print(f"Error moving {source} to {target}: {e}")

    print(f"Moved {len(move_operations)} files to new locations")

    # Find and remove content duplicates
    content_duplicates = find_content_duplicates()

    print(f"\\nFound {len(content_duplicates)} sets of content duplicates")

    duplicates_removed = 0
    for content_hash, file_paths in content_duplicates.items():
        # Keep the first file, remove the rest
        for dup_path_str in file_paths[1:]:
            dup_path = Path(dup_path_str)
            try:
                if dup_path.exists():
                    dup_path.unlink()
                    print(f"Removed duplicate: {dup_path.name}")
                    duplicates_removed += 1
            except Exception as e:
                print(f"Error removing {dup_path}: {e}")

    print(f"\\nRemoved {duplicates_removed} duplicate files")
    print("Organization, sorting, and deduplication complete!")


def preview_organization():
    """Show what the organization would look like without making changes"""
    print("PREVIEW OF ORGANIZATION PLAN")
    print("=" * 50)

    file_mapping = get_file_category_mapping()

    # Group files by destination
    destination_groups = {}
    for source_path, target_category in file_mapping.items():
        if target_category not in destination_groups:
            destination_groups[target_category] = []
        destination_groups[target_category].append(Path(source_path).name)

    # Print grouping summary
    for category, files in destination_groups.items():
        print(f"\\n{category}: {len(files)} files")
        # Show first 5 files as examples
        for file in files[:5]:
            print(f"  - {file}")
        if len(files) > 5:
            print(f"  ... and {len(files) - 5} more")

    # Find content duplicates without removing them
    content_duplicates = find_content_duplicates()
    print(f"\\nContent duplicates found: {len(content_duplicates)} sets")

    for content_hash, file_paths in content_duplicates.items():
        print(f"  Duplicate set ({len(file_paths)} files):")
        for path in file_paths:
            print(f"    - {Path(path).name}")


if __name__ == "__main__":
    print("This script will make changes to your filesystem.")
    print("First, let's preview what will happen:\\n")

    preview_organization()

    response = input("\\nDo you want to proceed with these changes? (yes/no): ")
    if response.lower() in ["yes", "y"]:
        implement_organization()
    else:
        print("Operation cancelled.")
