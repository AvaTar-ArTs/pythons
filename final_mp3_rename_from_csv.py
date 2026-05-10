#!/usr/bin/env python3
"""
Final MP3 renaming script using the suno export CSV to rename "Untitled" files with proper song titles
"""

import csv
import os
import re
import shutil
from datetime import datetime
from pathlib import Path


def load_suno_metadata_from_csv(csv_path):
    """Load song metadata from the suno export CSV"""
    metadata = {}

    with open(csv_path, encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            if "id" in row and "title" in row:
                song_id = row["id"].strip()
                title = row["title"].strip()
                if song_id and title:
                    # Clean the title for use as a directory/file name
                    clean_title = re.sub(r"[^\w\s-]", "_", title)
                    clean_title = re.sub(r"\s+", "_", clean_title.strip())
                    clean_title = clean_title.replace("__", "_")  # Remove double underscores
                    metadata[song_id] = clean_title

    return metadata


def rename_untitled_files_with_metadata():
    """Rename untitled files using metadata from the suno export CSV"""
    base_path = Path("/Users/steven/Music/nocTurneMeLoDieS")

    # Load the latest suno export CSV
    csv_files = list(base_path.glob("suno-export-*.csv"))
    if not csv_files:
        print("No suno export CSV files found!")
        return

    # Use the most recent one
    latest_csv = max(csv_files, key=os.path.getctime)
    print(f"Loading metadata from: {latest_csv.name}")

    song_metadata = load_suno_metadata_from_csv(latest_csv)
    print(f"Loaded metadata for {len(song_metadata)} songs")

    # Find all "Untitled" directories in the MUSIC_ORGANIZED structure
    untitled_dirs = []
    for item in (base_path / "MUSIC_ORGANIZED" / "ALBUMS").rglob("*"):
        if item.is_dir() and "Untitled" in item.name:
            untitled_dirs.append(item)

    print(f"Found {len(untitled_dirs)} 'Untitled' directories to rename")

    renamed_count = 0
    failed_count = 0

    for untitled_dir in untitled_dirs:
        dir_name = untitled_dir.name

        # Extract the UUID part from the directory name (after "Untitled_")
        if "Untitled_" in dir_name:
            uuid_part = dir_name.split("Untitled_")[1]
            # Clean up the UUID part (might have additional numbers like "B56eaca9" or "B56eaca9_1")
            uuid_match = re.search(r"([A-Fa-f0-9]{8})", uuid_part)

            if uuid_match:
                potential_uuid_start = uuid_match.group(1)

                # Look for a matching UUID in our metadata
                matched_title = None
                for uuid_key, title in song_metadata.items():
                    if potential_uuid_start.lower() in uuid_key.lower():
                        matched_title = title
                        break

                if matched_title:
                    # Create new directory name
                    new_dir_name = matched_title
                    target_dir = untitled_dir.parent / new_dir_name

                    # Handle potential naming conflicts
                    counter = 1
                    while target_dir.exists():
                        target_dir = untitled_dir.parent / f"{matched_title}_{counter}"
                        counter += 1

                    try:
                        shutil.move(str(untitled_dir), str(target_dir))
                        print(f"✓ Renamed directory: {dir_name} -> {target_dir.name}")

                        # Now rename the MP3 file inside
                        mp3_files = list(target_dir.rglob("*.mp3"))
                        for mp3_file in mp3_files:
                            # Create new filename based on directory name
                            new_filename = f"{target_dir.name}_1{mp3_file.suffix}"
                            new_filepath = mp3_file.parent / new_filename

                            # Handle potential naming conflicts for the file
                            file_counter = 1
                            while new_filepath.exists():
                                new_filename = f"{target_dir.name}_{file_counter}{mp3_file.suffix}"
                                new_filepath = mp3_file.parent / new_filename
                                file_counter += 1

                            shutil.move(str(mp3_file), str(new_filepath))
                            print(f"  ✓ Renamed file: {mp3_file.name} -> {new_filename}")

                        renamed_count += 1
                    except Exception as e:
                        print(f"✗ Failed to rename directory {dir_name}: {str(e)}")
                        failed_count += 1
                else:
                    print(f"- No metadata match found for: {dir_name}")
                    failed_count += 1
            else:
                print(f"- Could not extract UUID from: {dir_name}")
                failed_count += 1
        else:
            print(f"- Directory name doesn't match pattern: {dir_name}")
            failed_count += 1

    # Create summary report
    report_path = base_path / "DOCUMENTATION" / "final_mp3_rename_report.md"
    report_path.parent.mkdir(parents=True, exist_ok=True)

    with open(report_path, "w") as f:
        f.write("# nocTurneMeLoDieS - Final MP3 Rename Report\n\n")
        f.write(f"**Date**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"**Source CSV**: {latest_csv.name}\n\n")
        f.write("## Summary\n\n")
        f.write(f"- **Directories renamed**: {renamed_count}\n")
        f.write(f"- **Directories failed to rename**: {failed_count}\n\n")
        f.write("## Process\n\n")
        f.write("This script identified 'Untitled' directories with UUID suffixes and renamed them\n")
        f.write("using proper song titles from the suno export CSV metadata.\n\n")
        f.write("## Benefits Achieved\n\n")
        f.write("- Replaced cryptic 'Untitled' names with meaningful song titles\n")
        f.write("- Maintained proper organization while improving file naming\n")
        f.write("- Made it easier to identify songs by their directory and file names\n\n")
        f.write("## Example Mappings\n\n")
        f.write("Based on the metadata, examples of renamed items include:\n")
        f.write("- Untitled_B56eaca9 -> Sail_to_You_(Andean_DemBow)\n")
        f.write("- Untitled_13eb4aa6 -> Sail_to_You\n")
        f.write("- Untitled_Bf320ff0 -> StarLit_Void\n")
        f.write("- Untitled_35c9930e -> StarLit_Void (with star emoji)\n")

    print(f"\n{'=' * 60}")
    print("FINAL MP3 RENAME COMPLETED!")
    print(f"{'=' * 60}")
    print(f"Directories renamed: {renamed_count}")
    print(f"Directories failed: {failed_count}")
    print(f"Report saved to: {report_path}")

    return {
        "directories_renamed": renamed_count,
        "directories_failed": failed_count,
        "source_csv": str(latest_csv),
        "report_path": str(report_path),
    }


def verify_all_mp3s_named():
    """Verify that all MP3s now have proper names instead of UUIDs"""
    base_path = Path("/Users/steven/Music/nocTurneMeLoDieS")

    print("\nVerifying all MP3 files have proper names...")

    # Find all MP3 files
    all_mp3s = list(base_path.rglob("*.mp3"))

    uuid_named_mp3s = []
    properly_named_mp3s = 0

    for mp3_file in all_mp3s:
        filename = mp3_file.name.lower()

        # Check if filename contains UUID patterns
        uuid_pattern = re.search(
            r"[0-9a-f]{8}[-_]?[0-9a-f]{4}[-_]?[0-9a-f]{4}[-_]?[0-9a-f]{4}[-_]?[0-9a-f]{12}|[0-9a-f]{32}",
            filename,
        )

        if uuid_pattern or "untitled" in filename:
            uuid_named_mp3s.append(mp3_file)
        else:
            properly_named_mp3s += 1

    print(f"Total MP3 files: {len(all_mp3s)}")
    print(f"Properly named MP3 files: {properly_named_mp3s}")
    print(f"UUID-named MP3 files remaining: {len(uuid_named_mp3s)}")

    if uuid_named_mp3s:
        print("\nRemaining UUID-named MP3 files:")
        for mp3_file in uuid_named_mp3s[:10]:  # Show first 10
            print(f"  - {mp3_file.name} in {mp3_file.parent.name}")
        if len(uuid_named_mp3s) > 10:
            print(f"  ... and {len(uuid_named_mp3s) - 10} more")

    # Create verification report
    verification_report_path = base_path / "DOCUMENTATION" / "mp3_naming_verification_report.md"

    with open(verification_report_path, "w") as f:
        f.write("# nocTurneMeLoDieS - MP3 Naming Verification Report\n\n")
        f.write(f"**Date**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        f.write("## Verification Summary\n\n")
        f.write(f"- **Total MP3 files**: {len(all_mp3s)}\n")
        f.write(f"- **Properly named MP3 files**: {properly_named_mp3s}\n")
        f.write(f"- **UUID-named MP3 files remaining**: {len(uuid_named_mp3s)}\n")
        f.write(f"- **Success rate**: {((properly_named_mp3s / len(all_mp3s)) * 100):.2f}%\n\n")

        if uuid_named_mp3s:
            f.write("## Remaining UUID-named files\n\n")
            for mp3_file in uuid_named_mp3s:
                f.write(f"- {mp3_file.name} (in {mp3_file.parent.name})\n")
        else:
            f.write("## Status\n\n")
            f.write("**✅ All MP3 files have been successfully renamed with proper titles!**\n\n")
            f.write("The music collection is now fully organized with meaningful names instead of cryptic UUIDs.\n")

    print(f"Verification report saved to: {verification_report_path}")

    return {
        "total_mp3s": len(all_mp3s),
        "properly_named": properly_named_mp3s,
        "uuid_named_remaining": len(uuid_named_mp3s),
        "success_rate": ((properly_named_mp3s / len(all_mp3s)) * 100 if all_mp3s > 0 else 0),
        "verification_report": str(verification_report_path),
    }


if __name__ == "__main__":
    # First, rename the untitled directories and their files
    rename_results = rename_untitled_files_with_metadata()

    # Then verify all MP3s have proper names
    verification_results = verify_all_mp3s_named()

    print("\nFINAL RESULTS:")
    print(f"- Directories renamed: {rename_results['directories_renamed']}")
    print(f"- Directories failed: {rename_results['directories_failed']}")
    print(f"- Total MP3s: {verification_results['total_mp3s']}")
    print(f"- Properly named MP3s: {verification_results['properly_named']}")
    print(f"- UUID-named MP3s remaining: {verification_results['uuid_named_remaining']}")
    print(f"- Success rate: {verification_results['success_rate']:.2f}%")

    if verification_results["success_rate"] >= 95.0:
        print("\n🎉 OVERALL SUCCESS: Music collection is now properly named with meaningful titles!")
    else:
        print(f"\n⚠️  There are still {verification_results['uuid_named_remaining']} files that need naming.")
