#!/usr/bin/env python3
"""
Final synchronization script for NocturneMelodies collections.
This script will organize the iCloud collection to mirror the local structure.
"""

import json
import os
import re
import shutil
import sys
from pathlib import Path


def normalize_name(name):
    """Normalize directory/file names for comparison."""
    # Remove special characters and convert to uppercase for comparison
    normalized = re.sub(r"[^\w\s]", " ", name.upper())
    normalized = re.sub(r"\s+", "_", normalized.strip())
    return normalized


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
                    local_files[file] = {
                        "full_path": str(full_path),
                        "relative_path": str(rel_path),
                        "directory": str(rel_path.parent),
                    }

    return local_files


def get_icloud_files(icloud_path):
    """Get all MP3 files from iCloud collection."""
    icloud_files = {}

    for root, dirs, files in os.walk(icloud_path):
        for file in files:
            if file.lower().endswith(".mp3"):
                full_path = Path(root) / file
                rel_path = full_path.relative_to(Path(icloud_path))
                icloud_files[file] = {
                    "full_path": str(full_path),
                    "relative_path": str(rel_path),
                    "directory": str(rel_path.parent),
                }

    return icloud_files


def create_directory_mapping(local_files, icloud_files):
    """Create a mapping between iCloud and local directory structures."""
    # Get unique directories from both collections
    local_dirs = set()
    icloud_dirs = set()

    for info in local_files.values():
        local_dirs.add(info["directory"])

    for info in icloud_files.values():
        icloud_dirs.add(info["directory"])

    # Create mapping based on name similarity
    dir_mapping = {}

    for icloud_dir in icloud_dirs:
        normalized_icloud = normalize_name(icloud_dir)

        best_match = None
        best_score = 0

        for local_dir in local_dirs:
            normalized_local = normalize_name(local_dir)

            # Calculate similarity score
            if normalized_icloud == normalized_local:
                score = 100
            else:
                # Count common words
                icloud_words = set(normalized_icloud.split("_"))
                local_words = set(normalized_local.split("_"))
                common_words = icloud_words.intersection(local_words)
                score = len(common_words) * 10  # Weight common words

            if score > best_score:
                best_score = score
                best_match = local_dir

        if best_match and best_score > 0:
            dir_mapping[icloud_dir] = best_match
        else:
            # If no good match, use the original name but in the organized format
            dir_mapping[icloud_dir] = icloud_dir.replace(" ", "_").upper()

    return dir_mapping


def sync_collections(local_path, icloud_path, dry_run=True):
    """Synchronize collections with option for dry run."""

    print("Analyzing collections...")
    local_files = get_local_files(local_path)
    icloud_files = get_icloud_files(icloud_path)

    print(f"Local files: {len(local_files)}")
    print(f"iCloud files: {len(icloud_files)}")

    # Create directory mapping
    dir_mapping = create_directory_mapping(local_files, icloud_files)

    print(f"\nDirectory mapping created ({len(dir_mapping)} mappings)")

    # Identify files that need to be moved/copied
    local_filenames = set(local_files.keys())
    icloud_filenames = set(icloud_files.keys())

    files_only_local = local_filenames - icloud_filenames
    files_only_icloud = icloud_filenames - local_filenames
    common_files = local_filenames & icloud_filenames

    print(f"Files only in local: {len(files_only_local)}")
    print(f"Files only in iCloud: {len(files_only_icloud)}")
    print(f"Common files: {len(common_files)}")

    # Plan operations
    operations = []

    # 1. Move existing iCloud files to match local organization
    for filename, info in icloud_files.items():
        current_dir = info["directory"]
        target_dir = dir_mapping.get(current_dir, current_dir)

        if current_dir != target_dir:
            target_path = Path(icloud_path) / target_dir / filename
            operations.append(
                {
                    "action": "move",
                    "source": info["full_path"],
                    "target": str(target_path),
                    "reason": f"Reorganize to match local structure: {current_dir} -> {target_dir}",
                }
            )

    # 2. Copy missing files from local to iCloud
    for filename in files_only_local:
        local_info = local_files[filename]
        target_dir = local_info["directory"]
        target_path = Path(icloud_path) / target_dir / filename

        operations.append(
            {
                "action": "copy",
                "source": local_info["full_path"],
                "target": str(target_path),
                "reason": "Sync missing file from local to iCloud",
            }
        )

    print(f"\nPlanned operations: {len(operations)}")

    # Show summary of operations
    move_ops = [op for op in operations if op["action"] == "move"]
    copy_ops = [op for op in operations if op["action"] == "copy"]

    print(f"Move operations: {len(move_ops)}")
    print(f"Copy operations: {len(copy_ops)}")

    if dry_run:
        print("\nDRY RUN MODE - No actual changes will be made")
        print("To execute the synchronization, run with dry_run=False")

        # Show sample operations
        print("\nSample operations:")
        for i, op in enumerate(operations[:5]):
            print(f"  {i + 1}. {op['action'].upper()}: {op['source']} -> {op['target']}")
            print(f"     Reason: {op['reason']}")

        if len(operations) > 5:
            print(f"  ... and {len(operations) - 5} more operations")

    else:
        print("\nEXECUTING SYNCHRONIZATION...")

        # Execute operations
        successful_ops = 0
        failed_ops = 0

        for op in operations:
            try:
                source_path = Path(op["source"])
                target_path = Path(op["target"])

                # Create target directory if it doesn't exist
                target_path.parent.mkdir(parents=True, exist_ok=True)

                if op["action"] == "move":
                    if source_path.exists():
                        shutil.move(str(source_path), str(target_path))
                        print(f"MOVED: {source_path.name} -> {target_path.parent.name}/")
                    else:
                        print(f"WARNING: Source file does not exist: {source_path}")
                        failed_ops += 1
                        continue
                elif op["action"] == "copy":
                    if source_path.exists():
                        shutil.copy2(str(source_path), str(target_path))
                        print(f"COPIED: {source_path.name} -> {target_path.parent.name}/")
                    else:
                        print(f"WARNING: Source file does not exist: {source_path}")
                        failed_ops += 1
                        continue

                successful_ops += 1

            except Exception as e:
                print(f"ERROR processing {op['source']}: {str(e)}")
                failed_ops += 1

        print("\nSynchronization completed!")
        print(f"Successful operations: {successful_ops}")
        print(f"Failed operations: {failed_ops}")

    return operations


def generate_report(local_path, icloud_path, operations):
    """Generate a detailed report of the synchronization."""

    report = {
        "timestamp": str(__import__("datetime").datetime.now()),
        "collections": {"local_path": local_path, "icloud_path": icloud_path},
        "statistics": {
            "total_operations": len(operations),
            "move_operations": len([op for op in operations if op["action"] == "move"]),
            "copy_operations": len([op for op in operations if op["action"] == "copy"]),
        },
        "operations": operations,
    }

    with open("synchronization_report.json", "w") as f:
        json.dump(report, f, indent=2)

    print("\nDetailed report saved to 'synchronization_report.json'")


def main(dry_run=True):
    local_path = "/Users/steven/Music/nocTurneMeLoDieS"
    icloud_path = "/Users/steven/Library/Mobile Documents/com~apple~CloudDocs/nocTurneMeLoDieS"

    print("=" * 60)
    print("NOCTURNEMELODIES COLLECTION SYNCHRONIZATION")
    print("=" * 60)

    if dry_run:
        print("Running in DRY RUN mode - no changes will be made")
        print("To execute synchronization, run: python sync_collections_final.py execute")
    else:
        print("RUNNING ACTUAL SYNCHRONIZATION")
        print("WARNING: This will make actual changes to your iCloud files!")
        confirm = input("Type 'CONFIRM' to proceed: ")
        if confirm != "CONFIRM":
            print("Synchronization cancelled.")
            return []

    operations = sync_collections(local_path, icloud_path, dry_run=dry_run)

    if operations:
        generate_report(local_path, icloud_path, operations)

    return operations


if __name__ == "__main__":
    # Check command line arguments
    if len(sys.argv) > 1 and sys.argv[1] == "execute":
        operations = main(dry_run=False)
    else:
        operations = main(dry_run=True)
