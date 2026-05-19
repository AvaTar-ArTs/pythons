#!/usr/bin/env python3
"""
HTML File Consolidation Script for nocTurneMeLoDieS

This script consolidates scattered HTML files into a centralized structure
based on content type and function.
"""

import json
import shutil
from datetime import datetime
from pathlib import Path


def create_consolidation_map():
    """Create a mapping of file characteristics to destination folders"""
    consolidation_map = {
        # Artist and website related files
        "artist": ["artist-profile", "profile", "display_diverse_skills", "avatar"],
        "website": ["website", "page", "index", "landing"],
        "album": ["album", "cover", "gallery"],
        # Conversations and AI interactions
        "conversation": ["conversion", "transcript", "chat", "conversation", "export"],
        # Lyrics and music analysis
        "lyrics": ["lyrics", "analysis", "song", "origin"],
        # Discography and collections
        "discography": ["discography", "collection", "catalog"],
        # Templates and reusable components
        "template": ["template", "structure", "framework"],
        # Documentation
        "documentation": ["doc", "guide", "manual", "tutorial"],
        # Suno related files
        "suno": ["suno", "music", "track", "audio"],
        # TrashCat related files
        "trashcat": ["trashcat", "raccoon", "grunge", "alley"],
        # Cover art related files
        "covers": ["cover", "art", "image", "design"],
        # Miscellaneous files
        "misc": [],
    }
    return consolidation_map


def analyze_file_content(filepath):
    """Analyze file content to determine category"""
    try:
        with open(filepath, encoding="utf-8", errors="ignore") as f:
            content = f.read().lower()[:2000]  # Read first 2000 chars for analysis

        # Check for specific content indicators
        if "avatar" in content or "profile" in content:
            return "artist"
        elif "conversation" in content or "message" in content or "user:" in content or "assistant:" in content:
            return "conversation"
        elif "lyric" in content or "song" in content:
            return "lyrics"
        elif "discography" in content or "album" in content:
            return "discography"
        elif "template" in content or "structure" in content:
            return "template"
        elif "suno" in content:
            return "suno"
        elif "trashcat" in content or "raccoon" in content:
            return "trashcat"
        elif "cover" in content or "art" in content:
            return "covers"
        elif "website" in content or "page" in content:
            return "website"
        elif "doc" in content or "guide" in content or "tutorial" in content:
            return "documentation"
        else:
            return "misc"
    except (OSError, ValueError):
        return "misc"


def get_file_category(filepath, consolidation_map):
    """Determine the category for a file based on name and content"""
    filename = Path(filepath).name.lower()
    filepath_str = str(filepath).lower()

    # First check filename for category indicators
    for category, keywords in consolidation_map.items():
        if category == "misc":
            continue
        for keyword in keywords:
            if keyword in filename or keyword in filepath_str:
                return category

    # If no keyword match, analyze content
    return analyze_file_content(filepath)


def consolidate_html_files(source_dir, dest_dir):
    """Consolidate HTML files from source to destination directory"""

    # Create destination directory structure
    dest_path = Path(dest_dir)
    categories = [
        "artist",
        "website",
        "album",
        "conversation",
        "lyrics",
        "discography",
        "template",
        "documentation",
        "suno",
        "trashcat",
        "covers",
        "misc",
    ]

    for category in categories:
        (dest_path / category).mkdir(parents=True, exist_ok=True)

    # Get all HTML files
    html_files = list(Path(source_dir).rglob("*.html"))
    html_files = [f for f in html_files if not str(f).endswith("_mobile.html")]  # Exclude mobile versions

    print(f"Found {len(html_files)} HTML files to consolidate...")

    # Create consolidation map
    consolidation_map = create_consolidation_map()

    # Track moved files for mapping
    file_mapping = {}
    category_counts = {cat: 0 for cat in categories}

    for html_file in html_files:
        # Skip if it's a mobile version
        if "_mobile.html" in str(html_file):
            continue

        # Determine category
        category = get_file_category(html_file, consolidation_map)

        # Create new filename to avoid conflicts
        original_name = html_file.name
        dest_subdir = dest_path / category
        new_file_path = dest_subdir / original_name

        # Handle filename conflicts
        counter = 1
        while new_file_path.exists():
            stem = html_file.stem
            suffix = html_file.suffix
            new_filename = f"{stem}_{counter}{suffix}"
            new_file_path = dest_subdir / new_filename
            counter += 1

        # Copy file to new location
        shutil.copy2(html_file, new_file_path)

        # Record in mapping
        original_path = str(html_file.relative_to(Path(source_dir)))
        new_relative_path = str(new_file_path.relative_to(dest_path))
        file_mapping[original_path] = {
            "new_location": new_relative_path,
            "category": category,
            "timestamp": datetime.now().isoformat(),
        }

        category_counts[category] += 1

        print(f"Copied: {original_path} -> {new_relative_path}")

    # Save mapping file
    mapping_file = dest_path / "consolidation_mapping.json"
    with open(mapping_file, "w", encoding="utf-8") as f:
        json.dump(file_mapping, f, indent=2)

    # Save summary
    summary_file = dest_path / "consolidation_summary.txt"
    with open(summary_file, "w", encoding="utf-8") as f:
        f.write("HTML File Consolidation Summary\n")
        f.write("=" * 40 + "\n")
        f.write(f"Total files consolidated: {len(html_files)}\n")
        f.write(f"Consolidation date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        f.write("Files by category:\n")
        for category, count in category_counts.items():
            if count > 0:
                f.write(f"  {category}: {count}\n")

    print("\nConsolidation complete!")
    print(f"Files organized into {len(categories)} categories")
    print(f"Mapping saved to: {mapping_file}")
    print(f"Summary saved to: {summary_file}")

    return file_mapping


def main():
    source_directory = "/Users/steven/Music/nocTurneMeLoDieS"
    dest_directory = "/Users/steven/Music/nocTurneMeLoDieS/CONSOLIDATED_HTML"

    print("Starting HTML file consolidation...")
    print(f"Source: {source_directory}")
    print(f"Destination: {dest_directory}")

    try:
        consolidate_html_files(source_directory, dest_directory)
        print("\nConsolidation completed successfully!")
    except Exception as e:
        print(f"Error during consolidation: {str(e)}")


if __name__ == "__main__":
    main()
