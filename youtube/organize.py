"""
Organize 49

This module provides functionality for organize 49.

Author: Auto-generated
Date: 2025-11-01
"""

import logging

logger = logging.getLogger(__name__)


# Constants
CONSTANT_1000 = 1000

#!/usr/bin/env python3
"""
Hierarchical Directory Organization Script
Creates a proper nested folder structure: root → subfolder → subfolder → subfolder, etc.
"""

import os
import shutil
import re
from pathlib import Path
from collections import defaultdict


def sanitize_folder_name(name):
    """Sanitize folder name to be filesystem-safe"""
    # Remove or replace problematic characters
    name = re.sub(r'[<>:"/\\|?*]', "_", name)
    # Remove multiple underscores
    name = re.sub(r"_+", "_", name)
    # Remove leading/trailing underscores
    name = name.strip("_")
    # Capitalize first letter of each word
    name = " ".join(word.capitalize() for word in name.split("_"))
    return name


def analyze_file_content(file_path):
    """Analyze file content to determine appropriate category"""
    try:
        with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
            content = f.read(CONSTANT_1000)  # Read first CONSTANT_1000 characters
            content_lower = content.lower()

            # AI and Analysis tools
            if any(
                keyword in content_lower
                for keyword in ["openai", "gpt", "claude", "analysis", "analyze", "transcription", "whisper"]
            ):
                return "AI_Analysis"

            # Media processing
            elif any(
                keyword in content_lower for keyword in ["video", "audio", "mp4", "mp3", "ffmpeg", "media", "image"]
            ):
                return "Media_Processing"

            # Web scraping and automation
            elif any(
                keyword in content_lower
                for keyword in ["scrape", "selenium", "requests", "beautifulsoup", "youtube", "web"]
            ):
                return "Web_Automation"

            # Data management
            elif any(keyword in content_lower for keyword in ["csv", "json", "data", "database", "sql", "pandas"]):
                return "Data_Management"

            # Development tools
            elif any(
                keyword in content_lower for keyword in ["test", "debug", "config", "setup", "install", "requirements"]
            ):
                return "Development_Tools"

            # Creative tools
            elif any(keyword in content_lower for keyword in ["creative", "story", "content", "generate", "prompt"]):
                return "Creative_Tools"

            # Utilities
            elif any(keyword in content_lower for keyword in ["util", "helper", "tool", "convert", "batch"]):
                return "Utilities"

            else:
                return "General"

    except Exception:
        return "General"


def get_file_category(file_path):
    """Determine file category based on name and content"""
    filename = file_path.name.lower()

    # Check filename patterns first
    if any(pattern in filename for pattern in ["transcription", "transcribe", "whisper", "audio", "speech"]):
        return "AI_Analysis/Transcription"
    elif any(pattern in filename for pattern in ["image", "photo", "visual", "dalle", "generate"]):
        return "AI_Analysis/Image_Generation"
    elif any(pattern in filename for pattern in ["video", "mp4", "ffmpeg", "media"]):
        return "Media_Processing/Video"
    elif any(pattern in filename for pattern in ["audio", "mp3", "sound", "music"]):
        return "Media_Processing/Audio"
    elif any(pattern in filename for pattern in ["scrape", "youtube", "web", "selenium"]):
        return "Web_Automation/Scraping"
    elif any(pattern in filename for pattern in ["data", "csv", "json", "database"]):
        return "Data_Management/Processing"
    elif any(pattern in filename for pattern in ["test", "debug", "config", "setup"]):
        return "Development_Tools/Testing"
    elif any(pattern in filename for pattern in ["creative", "story", "content", "prompt"]):
        return "Creative_Tools/Content_Generation"
    elif any(pattern in filename for pattern in ["util", "helper", "tool", "convert"]):
        return "Utilities/General"
    else:
        # Fall back to content analysis
        category = analyze_file_content(file_path)
        if category == "AI_Analysis":
            return "AI_Analysis/General"
        elif category == "Media_Processing":
            return "Media_Processing/General"
        elif category == "Web_Automation":
            return "Web_Automation/General"
        elif category == "Data_Management":
            return "Data_Management/General"
        elif category == "Development_Tools":
            return "Development_Tools/General"
        elif category == "Creative_Tools":
            return "Creative_Tools/General"
        elif category == "Utilities":
            return "Utilities/General"
        else:
            return "General/Uncategorized"


def organize_files_hierarchically(root_dir):
    """Organize files into hierarchical folder structure"""
    root_path = Path(root_dir)
    organized_files = []
    errors = []

    # Get all files (excluding directories and hidden files)
    all_files = [f for f in root_path.iterdir() if f.is_file() and not f.name.startswith(".")]

    logger.info(f"Found {len(all_files)} files to organize")

    # Group files by category
    files_by_category = defaultdict(list)

    for file_path in all_files:
        category = get_file_category(file_path)
        files_by_category[category].append(file_path)

    # Create hierarchical structure and move files
    for category, files in files_by_category.items():
        logger.info(f"\nProcessing category: {category} ({len(files)} files)")

        # Create category path
        category_parts = category.split("/")
        category_path = root_path

        for part in category_parts:
            part = sanitize_folder_name(part)
            category_path = category_path / part
            category_path.mkdir(exist_ok=True)

        # Move files to category folder
        for file_path in files:
            try:
                target_path = category_path / file_path.name

                # Handle filename conflicts
                counter = 1
                while target_path.exists():
                    name_parts = file_path.name.rsplit(".", 1)
                    if len(name_parts) == 2:
                        new_name = f"{name_parts[0]}_{counter}.{name_parts[1]}"
                    else:
                        new_name = f"{file_path.name}_{counter}"
                    target_path = category_path / new_name
                    counter += 1

                shutil.move(str(file_path), str(target_path))
                organized_files.append((str(file_path), str(target_path)))
                logger.info(f"  Moved: {file_path.name} -> {category}/{target_path.name}")

            except Exception as e:
                errors.append((str(file_path), str(e)))
                logger.info(f"  Error moving {file_path.name}: {e}")

    return organized_files, errors, files_by_category


def create_navigation_guide(root_dir, files_by_category):
    """Create a navigation guide for the new structure"""
    root_path = Path(root_dir)
    guide_content = []

    guide_content.append("# Python Directory - Hierarchical Organization Guide\n")
    guide_content.append(f"Generated: {os.popen('date').read().strip()}\n")
    guide_content.append(f"Total categories: {len(files_by_category)}\n")
    guide_content.append(f"Total files: {sum(len(files) for files in files_by_category.values())}\n\n")

    guide_content.append("## Directory Structure\n\n")

    # Create tree-like structure
    for category in sorted(files_by_category.keys()):
        parts = category.split("/")
        indent = "  " * (len(parts) - 1)
        guide_content.append(f"{indent}📁 {parts[-1]}/ ({len(files_by_category[category])} files)\n")

    guide_content.append("\n## File Categories\n\n")

    for category in sorted(files_by_category.keys()):
        guide_content.append(f"### {category.replace('/', ' → ')}\n")
        guide_content.append(f"**Files:** {len(files_by_category[category])}\n")
        guide_content.append(f"**Path:** `{category.replace('/', '/')}/`\n\n")

        # List some example files
        example_files = sorted(files_by_category[category])[:5]
        for file_path in example_files:
            guide_content.append(f"- `{file_path.name}`\n")

        if len(files_by_category[category]) > 5:
            guide_content.append(f"- ... and {len(files_by_category[category]) - 5} more files\n")

        guide_content.append(Path("\n"))

    # Write navigation guide
    guide_path = root_path / "NAVIGATION_GUIDE.md"
    with open(guide_path, "w", encoding="utf-8") as f:
        f.writelines(guide_content)

    logger.info(f"Created navigation guide: {guide_path}")
    return guide_path


def create_readme_files(root_dir, files_by_category):
    """Create README files for each category"""
    root_path = Path(root_dir)

    for category, files in files_by_category.items():
        category_parts = category.split("/")
        category_path = root_path

        for part in category_parts:
            part = sanitize_folder_name(part)
            category_path = category_path / part

        readme_path = category_path / "README.md"

        readme_content = []
        readme_content.append(f"# {category.replace('/', ' → ')}\n\n")
        readme_content.append(f"**Total files:** {len(files)}\n\n")
        readme_content.append("## Files in this category:\n\n")

        for file_path in sorted(files):
            readme_content.append(f"- `{file_path.name}`\n")

        readme_content.append(f"\n## Description\n\n")
        readme_content.append(
            f"This directory contains {len(files)} files related to {category.split('/')[-1].replace('_', ' ').lower()}.\n"
        )

        with open(readme_path, "w", encoding="utf-8") as f:
            f.writelines(readme_content)


if __name__ == "__main__":
    root_directory = Path("/Users/steven/AvaTarArTs/python")

    logger.info("Starting hierarchical directory organization...")
    logger.info(f"Root directory: {root_directory}")

    # Organize files hierarchically
    organized_files, errors, files_by_category = organize_files_hierarchically(root_directory)

    logger.info(f"\nOrganized {len(organized_files)} files")
    if errors:
        logger.info(f"Encountered {len(errors)} errors")
        for source, error in errors:
            logger.info(f"  {source}: {error}")

    # Create navigation guide
    logger.info("\nCreating navigation guide...")
    guide_path = create_navigation_guide(root_directory, files_by_category)

    # Create README files for each category
    logger.info("Creating README files for each category...")
    create_readme_files(root_directory, files_by_category)

    logger.info("\nHierarchical organization complete!")
    logger.info(f"Navigation guide: {guide_path}")
    logger.info("\nNew directory structure:")
    logger.info("Root → Category → Subcategory → Files")
