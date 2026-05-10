#!/usr/bin/env python3
"""
Verification script to confirm that UUID-named directories and files have been renamed to proper titles
"""

import csv
import os
import re
from pathlib import Path


def load_uuid_to_title_mapping():
    """Load the UUID to title mapping from CSV files"""
    base_path = Path("/Users/steven/Music/nocTurneMeLoDieS")
    mapping = {}

    # Look for CSV files that might contain UUID to title mappings
    csv_files = list(base_path.rglob("*.csv"))

    for csv_file in csv_files:
        try:
            with open(csv_file, encoding="utf-8") as f:
                sample = f.read(2048)  # Read first 2KB to check if it contains UUID mappings
                f.seek(0)

                if any(
                    keyword in sample.lower()
                    for keyword in [
                        "uuid",
                        "id",
                        "title",
                        "song",
                        "filename",
                        "audio_url",
                        "url",
                    ]
                ):
                    reader = csv.DictReader(f)
                    for row in reader:
                        # Look for ID and title fields
                        uuid_val = None
                        title_val = None

                        # Common field names for UUID/ID
                        id_fields = [
                            "id",
                            "uuid",
                            "song_id",
                            "track_id",
                            "audio_id",
                            "url",
                            "audio_url",
                        ]
                        # Common field names for titles
                        title_fields = [
                            "title",
                            "song_title",
                            "name",
                            "track_name",
                            "prompt",
                            "gpt_prompt",
                        ]

                        for id_field in id_fields:
                            if id_field in row:
                                id_value = row[id_field].strip()
                                # Extract UUID from URL if needed
                                if id_value.startswith("http"):
                                    # Extract UUID from URL patterns like https://cdn1.suno.ai/603df13d-3318-4648-8e20-b2d9b70e16fe.mp3
                                    uuid_match = re.search(
                                        r"([0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12})",
                                        id_value,
                                    )
                                    if uuid_match:
                                        uuid_val = uuid_match.group(1)
                                        break
                                else:
                                    uuid_val = id_value
                                    break

                        for title_field in title_fields:
                            if title_field in row:
                                title_val = row[title_field].strip()
                                break

                        if uuid_val and title_val and len(uuid_val) >= 32:  # Ensure it's actually a UUID
                            # Clean the UUID (remove hyphens, etc.)
                            clean_uuid = uuid_val.replace("-", "_").replace("{", "").replace("}", "")
                            mapping[clean_uuid] = title_val

        except Exception as e:
            print(f"Could not read CSV {csv_file}: {e}")
            continue

    return mapping


def find_uuid_directories():
    """Find directories that still have UUID names"""
    base_path = Path("/Users/steven/Music/nocTurneMeLoDieS")
    uuid_dirs = []

    # Pattern for UUID directories
    uuid_pattern = re.compile(
        r"^[0-9a-f]{8}[-_][0-9a-f]{4}[-_][0-9a-f]{4}[-_][0-9a-f]{4}[-_][0-9a-f]{12}$",
        re.IGNORECASE,
    )

    albums_path = base_path / "MUSIC_ORGANIZED" / "ALBUMS"
    if albums_path.exists():
        for item in albums_path.iterdir():
            if item.is_dir():
                dir_name = item.name
                # Check if directory name looks like a UUID (with or without separators)
                if uuid_pattern.match(dir_name) or (
                    len(dir_name.replace("-", "").replace("_", "")) == 32
                    and re.match(
                        r"^[0-9a-f]+$",
                        dir_name.replace("-", "").replace("_", ""),
                        re.IGNORECASE,
                    )
                ):
                    uuid_dirs.append(item)

    return uuid_dirs


def find_uuid_files():
    """Find files that still have UUID names"""
    base_path = Path("/Users/steven/Music/nocTurneMeLoDieS")
    uuid_files = []

    # Pattern for UUID files
    uuid_pattern = re.compile(
        r"[0-9a-f]{8}[-_]?[0-9a-f]{4}[-_]?[0-9a-f]{4}[-_]?[0-9a-f]{4}[-_]?[0-9a-f]{12}",
        re.IGNORECASE,
    )

    for root, dirs, files in os.walk(base_path):
        for file in files:
            if uuid_pattern.search(file):
                uuid_files.append(Path(root) / file)

    return uuid_files


def verify_organization():
    """Verify that the organization from UUIDs to proper titles was successful"""
    print("🔍 Verifying Music Collection Organization")
    print("=" * 60)

    # Load UUID to title mapping
    print("Loading UUID to title mappings...")
    uuid_mapping = load_uuid_to_title_mapping()
    print(f"Loaded {len(uuid_mapping)} UUID to title mappings")

    # Find any remaining UUID directories
    print("\nChecking for UUID-named directories...")
    uuid_dirs = find_uuid_directories()

    if uuid_dirs:
        print(f"⚠️  Found {len(uuid_dirs)} directories with UUID names:")
        for uuid_dir in uuid_dirs[:10]:  # Show first 10
            print(f"  - {uuid_dir.name}")
        if len(uuid_dirs) > 10:
            print(f"  ... and {len(uuid_dirs) - 10} more")
    else:
        print("✅ No UUID-named directories found in ALBUMS/")

    # Find any remaining UUID files
    print("\nChecking for UUID-named files...")
    uuid_files = find_uuid_files()

    if uuid_files:
        print(f"⚠️  Found {len(uuid_files)} files with UUID names:")
        for uuid_file in uuid_files[:10]:  # Show first 10
            print(f"  - {uuid_file.name}")
        if len(uuid_files) > 10:
            print(f"  ... and {len(uuid_files) - 10} more")
    else:
        print("✅ No UUID-named files found")

    # Check a sample of properly named directories
    print("\nChecking properly named directories...")
    albums_path = Path("/Users/steven/Music/nocTurneMeLoDieS/MUSIC_ORGANIZED/ALBUMS")
    if albums_path.exists():
        proper_dirs = []
        for item in albums_path.iterdir():
            if item.is_dir():
                # Check if directory name does NOT look like a UUID
                dir_name = item.name
                uuid_pattern = re.compile(
                    r"^[0-9a-f]{8}[-_][0-9a-f]{4}[-_][0-9a-f]{4}[-_][0-9a-f]{4}[-_][0-9a-f]{12}$",
                    re.IGNORECASE,
                )

                if not uuid_pattern.match(dir_name) and len(dir_name.replace("-", "").replace("_", "")) != 32:
                    proper_dirs.append(item.name)

        print(f"✅ Found {len(proper_dirs)} properly named directories")
        print("Sample of properly named directories:")
        for dir_name in proper_dirs[:15]:  # Show first 15
            # Count files in each directory
            dir_path = albums_path / dir_name
            if dir_path.exists():
                file_count = len([f for f in dir_path.iterdir() if f.is_file()])
                print(f"  - {dir_name} ({file_count} files)")

    # Create verification report
    report_path = Path("/Users/steven/Music/nocTurneMeLoDieS/MUSIC_ORGANIZED/VERIFICATION_REPORT.md")
    report_path.parent.mkdir(parents=True, exist_ok=True)

    with open(report_path, "w") as f:
        f.write("# nocTurneMeLoDieS - UUID to Title Organization Verification Report\n\n")
        f.write(f"**Date**: {Path.cwd().joinpath('').stat().st_mtime}\n\n")  # Using current time instead

        f.write("## Summary\n\n")
        f.write(f"- **UUID to Title mappings loaded**: {len(uuid_mapping)}\n")
        f.write(f"- **UUID-named directories remaining**: {len(uuid_dirs)}\n")
        f.write(f"- **UUID-named files remaining**: {len(uuid_files)}\n")
        f.write(f"- **Properly named directories**: {len(proper_dirs)}\n\n")

        f.write("## Status\n\n")
        if len(uuid_dirs) == 0 and len(uuid_files) == 0:
            f.write("✅ **SUCCESS**: All UUID-named directories and files have been renamed to proper titles!\n\n")
            f.write("The music collection is now fully organized with human-readable names instead of cryptic UUIDs.\n")
        else:
            f.write("⚠️ **PARTIAL SUCCESS**: Some UUID-named items remain that need attention.\n\n")

        f.write("## Sample of Properly Named Directories\n\n")
        for dir_name in proper_dirs[:20]:
            f.write(f"- {dir_name}\n")

        if uuid_dirs:
            f.write("\n## Remaining UUID Directories\n\n")
            for uuid_dir in uuid_dirs:
                f.write(f"- {uuid_dir.name}\n")

        if uuid_files:
            f.write("\n## Remaining UUID Files\n\n")
            for uuid_file in uuid_files[:20]:  # First 20
                f.write(f"- {uuid_file.name}\n")
            if len(uuid_files) > 20:
                f.write(f"- ... and {len(uuid_files) - 20} more\n")

    print(f"\n📋 Verification report saved to: {report_path}")

    return {
        "uuid_mappings_loaded": len(uuid_mapping),
        "uuid_directories_remaining": len(uuid_dirs),
        "uuid_files_remaining": len(uuid_files),
        "proper_directories_found": len(proper_dirs),
        "report_path": str(report_path),
    }


if __name__ == "__main__":
    results = verify_organization()
    print(f"\nVerification Results: {results}")
