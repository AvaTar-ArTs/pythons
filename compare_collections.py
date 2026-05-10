#!/usr/bin/env python3
"""
Script to analyze and compare NocturneMelodies collections between local and iCloud storage.
"""

import json
import os
from collections import defaultdict
from pathlib import Path


def get_local_files(local_path):
    """Get all MP3 files from local organized collection."""
    local_files = {}

    # Look in the organized albums directory
    albums_path = Path(local_path) / "MUSIC_ORGANIZED" / "ALBUMS"
    if albums_path.exists():
        for root, dirs, files in os.walk(albums_path):
            for file in files:
                if file.lower().endswith(".mp3"):
                    full_path = Path(root) / file
                    rel_path = full_path.relative_to(albums_path)
                    local_files[file] = str(rel_path)

    # Also look for any MP3s in the main directory
    main_path = Path(local_path)
    for root, dirs, files in os.walk(main_path):
        # Skip the organized albums directory since we already processed it
        if "MUSIC_ORGANIZED/ALBUMS" in str(root):
            continue
        for file in files:
            if file.lower().endswith(".mp3"):
                full_path = Path(root) / file
                rel_path = full_path.relative_to(main_path)
                if file not in local_files:  # Don't overwrite if already found in albums
                    local_files[file] = str(rel_path)

    return local_files


def get_icloud_files(icloud_path):
    """Get all MP3 files from iCloud collection."""
    icloud_files = {}

    for root, dirs, files in os.walk(icloud_path):
        for file in files:
            if file.lower().endswith(".mp3"):
                full_path = Path(root) / file
                rel_path = full_path.relative_to(Path(icloud_path))
                icloud_files[file] = str(rel_path)

    return icloud_files


def analyze_collections(local_path, icloud_path):
    """Analyze and compare the two collections."""

    print("Analyzing Local Collection...")
    local_files = get_local_files(local_path)
    print(f"Found {len(local_files)} MP3 files in local collection")

    print("\nAnalyzing iCloud Collection...")
    icloud_files = get_icloud_files(icloud_path)
    print(f"Found {len(icloud_files)} MP3 files in iCloud collection")

    # Find common files
    local_filenames = set(local_files.keys())
    icloud_filenames = set(icloud_files.keys())

    common_files = local_filenames.intersection(icloud_filenames)
    only_local = local_filenames.difference(icloud_filenames)
    only_icloud = icloud_filenames.difference(local_filenames)

    print("\nComparison Summary:")
    print(f"- Common files: {len(common_files)}")
    print(f"- Files only in local: {len(only_local)}")
    print(f"- Files only in iCloud: {len(only_icloud)}")

    # Get directory distribution for both collections
    local_dirs = defaultdict(int)
    for filepath in local_files.values():
        dirname = Path(filepath).parent.name
        local_dirs[dirname] += 1

    icloud_dirs = defaultdict(int)
    for filepath in icloud_files.values():
        dirname = Path(filepath).parent.name
        icloud_dirs[dirname] += 1

    print("\nLocal collection directory distribution (top 20):")
    for dir_name, count in sorted(local_dirs.items(), key=lambda x: x[1], reverse=True)[:20]:
        print(f"  {dir_name}: {count} files")

    print("\niCloud collection directory distribution:")
    for dir_name, count in sorted(icloud_dirs.items(), key=lambda x: x[1], reverse=True):
        print(f"  {dir_name}: {count} files")

    # Generate detailed reports
    report = {
        "summary": {
            "local_total": len(local_files),
            "icloud_total": len(icloud_files),
            "common_files": len(common_files),
            "only_local": len(only_local),
            "only_icloud": len(only_icloud),
        },
        "local_files": local_files,
        "icloud_files": icloud_files,
        "common_files": list(common_files),
        "only_local": list(only_local),
        "only_icloud": list(only_icloud),
        "local_directories": dict(local_dirs),
        "icloud_directories": dict(icloud_dirs),
    }

    return report


def generate_sync_plan(report):
    """Generate a plan to organize iCloud collection to mirror local structure."""

    print(f"\n{'=' * 60}")
    print("SYNCHRONIZATION PLAN")
    print("=" * 60)

    print("\n1. Current State Analysis:")
    print(f"   - Local collection: {report['summary']['local_total']} files in organized structure")
    print(f"   - iCloud collection: {report['summary']['icloud_total']} files in less organized structure")
    print(f"   - Common files: {report['summary']['common_files']}")
    print(f"   - Files to sync from local to iCloud: {report['summary']['only_local']}")

    print("\n2. Organization Strategy:")
    print("   - Mirror the local directory structure in iCloud")
    print("   - Move files from flat/icloud-specific structure to organized album-based structure")
    print("   - Preserve existing iCloud files while adding missing ones from local")

    print("\n3. Implementation Steps:")
    print("   a) Create directory mapping between local and iCloud structures")
    print("   b) Copy missing files from local to iCloud with proper organization")
    print("   c) Reorganize existing iCloud files to match local structure")
    print("   d) Verify synchronization completeness")

    print("\n4. Directory Mapping Recommendations:")

    # Identify potential mappings between iCloud and local directories
    icloud_to_local_mapping = {}
    for icloud_dir in report["icloud_directories"].keys():
        # Look for similar names in local directories
        best_match = None
        highest_similarity = 0

        for local_dir in report["local_directories"].keys():
            # Simple similarity based on common words
            icloud_words = set(icloud_dir.lower().replace("_", " ").replace("-", " ").split())
            local_words = set(local_dir.lower().replace("_", " ").replace("-", " ").split())

            similarity = len(icloud_words.intersection(local_words))

            if similarity > highest_similarity:
                highest_similarity = similarity
                best_match = local_dir

        if best_match:
            icloud_to_local_mapping[icloud_dir] = best_match

    for icloud_dir, local_dir in icloud_to_local_mapping.items():
        print(f"   - '{icloud_dir}' -> '{local_dir}' ({report['icloud_directories'][icloud_dir]} files)")

    print("\n5. Action Items:")
    print("   - Create script to copy files from local to iCloud with proper directory structure")
    print("   - Move existing iCloud files to match local organization")
    print("   - Handle duplicate/named files appropriately")
    print("   - Preserve metadata and analysis files where possible")


def main():
    local_path = "/Users/steven/Music/nocTurneMeLoDieS"
    icloud_path = "/Users/steven/Library/Mobile Documents/com~apple~CloudDocs/nocTurneMeLoDieS"

    report = analyze_collections(local_path, icloud_path)

    # Save detailed report
    with open("collection_comparison_report.json", "w") as f:
        json.dump(report, f, indent=2)

    print("\nDetailed report saved to 'collection_comparison_report.json'")

    generate_sync_plan(report)


if __name__ == "__main__":
    main()
