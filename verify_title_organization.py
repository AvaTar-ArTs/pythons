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

                if any(keyword in sample.lower() for keyword in ["uuid", "id", "title", "song", "filename"]):
                    reader = csv.DictReader(f)
                    for row in reader:
                        # Look for UUID and title fields
                        uuid_fields = ["uuid", "id", "song_id", "track_id", "audio_id"]
                        title_fields = ["title", "song_title", "name", "track_name"]

                        uuid_val = None
                        title_val = None

                        for uuid_field in uuid_fields:
                            if uuid_field in row:
                                uuid_val = row[uuid_field].strip()
                                break

                        for title_field in title_fields:
                            if title_field in row:
                                title_val = row[title_field].strip()
                                break

                        if uuid_val and title_val:
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
        r"^[0-9a-f]{8}[_-][0-9a-f]{4}[_-][0-9a-f]{4}[_-][0-9a-f]{4}[_-][0-9a-f]{12}$",
        re.IGNORECASE,
    )

    albums_path = base_path / "MUSIC_ORGANIZED" / "ALBUMS"
    if albums_path.exists():
        for item in albums_path.iterdir():
            if item.is_dir():
                dir_name = item.name
                # Check if directory name looks like a UUID
                if uuid_pattern.match(dir_name.replace("_", "-")) or len(dir_name) == 32 or len(dir_name) == 36:
                    uuid_dirs.append(item)

    return uuid_dirs


def find_uuid_files():
    """Find files that still have UUID names"""
    base_path = Path("/Users/steven/Music/nocTurneMeLoDieS")
    uuid_files = []

    # Pattern for UUID files
    uuid_pattern = re.compile(
        r"[0-9a-f]{8}[_-]?[0-9a-f]{4}[_-]?[0-9a-f]{4}[_-]?[0-9a-f]{4}[_-]?[0-9a-f]{12}",
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
            if item.is_dir() and not re.match(
                r"^[0-9a-f]{8}[_-][0-9a-f]{4}[_-][0-9a-f]{4}[_-][0-9a-f]{4}[_-][0-9a-f]{12}$",
                item.name,
                re.IGNORECASE,
            ):
                proper_dirs.append(item.name)

        print(f"✅ Found {len(proper_dirs)} properly named directories")
        print("Sample of properly named directories:")
        for dir_name in proper_dirs[:15]:  # Show first 15
            # Count files in each directory
            file_count = len([f for f in (albums_path / dir_name).iterdir() if f.is_file()])
            print(f"  - {dir_name} ({file_count} files)")

    # Create verification report
    report_path = Path("/Users/steven/Music/nocTurneMeLoDieS/MUSIC_ORGANIZED/VERIFICATION_REPORT.md")
    report_path.parent.mkdir(parents=True, exist_ok=True)

    with open(report_path, "w") as f:
        f.write("# nocTurneMeLoDieS - UUID to Title Organization Verification Report\n\n")
        f.write(f"**Date**: {os.popen('date').read().strip()}\n\n")

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
            file_count = len([f for f in (albums_path / dir_name).iterdir() if f.is_file()])
            f.write(f"- {dir_name} ({file_count} files)\n")

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
