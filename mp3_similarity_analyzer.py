#!/usr/bin/env python3
"""
Script to analyze MP3 files for similar titles and group them by similarity.
"""

import os
import re
import unicodedata
from collections import defaultdict
from difflib import SequenceMatcher


def normalize_title(title):
    """Normalize title for comparison by removing version indicators and special formatting."""
    # Remove file extension
    if title.lower().endswith(".mp3"):
        title = title[:-4]

    # Convert to lowercase and normalize unicode characters
    title = title.lower()
    title = unicodedata.normalize("NFKD", title)

    # Remove common version indicators and extra info in parentheses/brackets
    title = re.sub(r"\([^)]*\)", "", title)  # Remove content in parentheses
    title = re.sub(r"\[[^\]]*\]", "", title)  # Remove content in brackets
    title = re.sub(r"_+", " ", title)  # Replace underscores with spaces
    title = re.sub(r"\s+", " ", title)  # Replace multiple spaces with single space
    title = re.sub(r"v\d+", "", title)  # Remove version numbers like v4
    title = re.sub(r"_remaster(ed)?", "", title)  # Remove remaster indicators
    title = re.sub(r"_live", "", title)  # Remove live indicators
    title = re.sub(r"_acoustic", "", title)  # Remove acoustic indicators
    title = re.sub(r"_instrumental", "", title)  # Remove instrumental indicators
    title = re.sub(r"_demo", "", title)  # Remove demo indicators
    title = re.sub(r"_edit", "", title)  # Remove edit indicators
    title = re.sub(r"\d+$", "", title)  # Remove trailing numbers

    # Remove common prefixes/suffixes that indicate versions
    title = re.sub(r"_\d+$", "", title)  # Remove trailing numbers after underscore
    title = re.sub(r"_\d+_\d+$", "", title)  # Remove double number endings
    title = re.sub(r"_version$", "", title)
    title = re.sub(r"_original$", "", title)
    title = re.sub(r"_official$", "", title)
    title = re.sub(r"_radio_edit$", "", title)
    title = re.sub(r"_single_edit$", "", title)
    title = re.sub(r"_album_version$", "", title)
    title = re.sub(r"_clean$", "", title)
    title = re.sub(r"_dirty$", "", title)

    # Clean up extra spaces again after processing
    title = title.strip()
    title = re.sub(r"\s+", " ", title)

    return title


def similarity(a, b):
    """Calculate similarity ratio between two strings."""
    return SequenceMatcher(None, a, b).ratio()


def extract_core_title(filepath):
    """Extract the core title from a file path."""
    filename = os.path.basename(filepath)
    normalized = normalize_title(filename)
    return normalized


def find_similar_titles(file_paths, threshold=0.8):
    """Find similar titles among the provided file paths."""
    # Group files by their normalized core title
    groups = defaultdict(list)

    for path in file_paths:
        core_title = extract_core_title(path)
        groups[core_title].append(path)

    # Now find titles that are similar but not identical
    similar_groups = []
    processed = set()

    titles = list(groups.keys())

    for i, title1 in enumerate(titles):
        if title1 in processed:
            continue

        current_group = {
            "titles": [title1],
            "files": groups[title1][:],  # Copy the list
            "normalized_representative": title1,
        }

        for j, title2 in enumerate(titles[i + 1 :], i + 1):
            if title2 in processed:
                continue

            sim_ratio = similarity(title1, title2)

            if sim_ratio >= threshold:
                current_group["titles"].append(title2)
                current_group["files"].extend(groups[title2])
                processed.add(title2)

        processed.add(title1)

        # Only include groups with multiple unique titles or multiple files
        if len(current_group["titles"]) > 1 or len(current_group["files"]) > 1:
            # Find the most common or representative title
            current_group["normalized_representative"] = max(current_group["titles"], key=lambda t: len(groups[t]))
            similar_groups.append(current_group)

    return similar_groups


def main():
    # Read all MP3 file paths from stdin or from a predefined list
    import sys

    if len(sys.argv) > 1:
        mp3_dir = sys.argv[1]
        file_paths = []
        for root, dirs, files in os.walk(mp3_dir):
            for file in files:
                if file.lower().endswith(".mp3"):
                    file_paths.append(os.path.join(root, file))
    else:
        # Read from stdin if no directory provided
        import fileinput

        file_paths = [line.strip() for line in fileinput.input()]

    print(f"Analyzing {len(file_paths)} MP3 files for similar titles...\n")

    # Find similar titles
    similar_groups = find_similar_titles(file_paths, threshold=0.7)

    # Sort groups by number of files (largest groups first)
    similar_groups.sort(key=lambda x: len(x["files"]), reverse=True)

    print("=" * 80)
    print("SIMILAR TITLE GROUPINGS REPORT")
    print("=" * 80)
    print(f"Found {len(similar_groups)} groups of similar titles\n")

    for idx, group in enumerate(similar_groups, 1):
        print(f"{idx}. CORE SONG: {group['normalized_representative']}")
        print(f"   Variations found ({len(group['titles'])}): {', '.join(group['titles'])}")
        print(f"   Total files: {len(group['files'])}")
        print("   File paths:")
        for file_path in sorted(group["files"]):
            print(f"     - {file_path}")
        print()

    # Group files by their normalized core title to find exact duplicates
    groups = defaultdict(list)

    for path in file_paths:
        core_title = extract_core_title(path)
        groups[core_title].append(path)

    # Also look for potential duplicates (exact same normalized title)
    exact_duplicates = [(k, v) for k, v in groups.items() if len(v) > 1]

    if exact_duplicates:
        print("=" * 80)
        print("EXACT DUPLICATES (same normalized title)")
        print("=" * 80)
        for title, files in exact_duplicates:
            print(f"Title: {title}")
            print(f"Files ({len(files)}):")
            for file_path in files:
                print(f"  - {file_path}")
            print()

    # Summary statistics
    print("=" * 80)
    print("SUMMARY STATISTICS")
    print("=" * 80)
    print(f"Total MP3 files analyzed: {len(file_paths)}")
    print(f"Groups of similar titles: {len(similar_groups)}")
    print(f"Exact duplicate groups: {len(exact_duplicates)}")

    # Count total files in similar groups
    total_in_groups = sum(len(group["files"]) for group in similar_groups)
    print(f"Files in similar title groups: {total_in_groups}")
    print(f"Percentage in similar groups: {(total_in_groups / len(file_paths) * 100):.2f}%")


if __name__ == "__main__":
    main()
