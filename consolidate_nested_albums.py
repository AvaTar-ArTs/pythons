#!/usr/bin/env python3
"""
nocTurneMeLoDieS V4 - AvatarArts Consolidation Script
Consolidates content from nested Albums structure to main ALBUMS directory
"""

import json
import logging
import os
import shutil
from datetime import datetime
from pathlib import Path

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)


def consolidate_albums():
    """Consolidate all content from ALBUMS/Albums/ into main ALBUMS directory"""

    base_path = Path("/Users/steven/Music/nocTurneMeLoDieS/ALBUMS")
    nested_path = base_path / "Albums"

    if not nested_path.exists():
        logger.info(f"Nested Albums directory does not exist: {nested_path}")
        return

    logger.info(f"Starting consolidation from {nested_path} to {base_path}")

    # Track consolidation results
    results = {
        "directories_processed": 0,
        "files_moved": 0,
        "conflicts_resolved": 0,
        "errors": [],
    }

    # Walk through all subdirectories in ALBUMS/Albums/
    for root, dirs, files in os.walk(nested_path):
        for directory in dirs:
            source_dir = Path(root) / directory
            target_dir = base_path / directory

            # Skip the MAJOR_COLLECTIONS, MEDIUM_COLLECTIONS, SMALL_COLLECTIONS, etc. parent directories
            if source_dir == nested_path or source_dir.parent == nested_path:
                continue

            if source_dir.is_dir():
                logger.info(f"Processing directory: {source_dir}")

                # Check if target directory already exists
                if target_dir.exists():
                    logger.info(f"Target directory exists: {target_dir}")

                    # Move files from source to target, handling conflicts
                    for item in source_dir.iterdir():
                        target_item = target_dir / item.name

                        if target_item.exists():
                            # Handle conflict by adding suffix
                            counter = 1
                            stem = item.stem
                            suffix = item.suffix

                            while target_item.exists():
                                new_name = f"{stem}_{counter}{suffix}"
                                target_item = target_dir / new_name
                                counter += 1

                            logger.info(f"Renamed conflicting file: {item.name} -> {target_item.name}")
                            results["conflicts_resolved"] += 1

                        # Move the file
                        try:
                            if item.is_file():
                                shutil.move(str(item), str(target_item))
                                results["files_moved"] += 1
                                logger.info(f"Moved file: {item.name} -> {target_item.name}")
                            elif item.is_dir():
                                # For subdirectories, copy contents
                                shutil.move(str(item), str(target_item))
                                results["files_moved"] += len(list(item.rglob("*")))
                                logger.info(f"Moved directory: {item.name} -> {target_item.name}")
                        except Exception as e:
                            error_msg = f"Error moving {item} to {target_item}: {str(e)}"
                            logger.error(error_msg)
                            results["errors"].append(error_msg)
                else:
                    # Directory doesn't exist, move the entire directory
                    try:
                        shutil.move(str(source_dir), str(target_dir))

                        # Count files moved
                        if source_dir.is_dir():
                            files_in_dir = len(list(source_dir.rglob("*")))
                            results["files_moved"] += files_in_dir

                        results["directories_processed"] += 1
                        logger.info(f"Moved directory: {source_dir} -> {target_dir}")
                    except Exception as e:
                        error_msg = f"Error moving directory {source_dir} to {target_dir}: {str(e)}"
                        logger.error(error_msg)
                        results["errors"].append(error_msg)

    # After moving all content, remove the now-empty nested structure
    try:
        shutil.rmtree(nested_path)
        logger.info(f"Removed empty nested Albums directory: {nested_path}")
    except Exception as e:
        logger.error(f"Error removing nested Albums directory: {str(e)}")

    # Create summary
    results["end_time"] = datetime.now().isoformat()
    logger.info(f"Consolidation completed. Results: {results}")

    # Save results to a summary file
    summary_path = base_path / "CONSOLIDATION_SUMMARY.json"
    with open(summary_path, "w") as f:
        json.dump(results, f, indent=2)

    logger.info(f"Consolidation summary saved to: {summary_path}")
    return results


def verify_consolidation():
    """Verify that consolidation was successful"""
    base_path = Path("/Users/steven/Music/nocTurneMeLoDieS/ALBUMS")

    # Check that nested Albums directory no longer exists
    nested_path = base_path / "Albums"
    if nested_path.exists():
        logger.warning(f"Nested Albums directory still exists: {nested_path}")
        return False

    # Count main album directories
    album_dirs = [d for d in base_path.iterdir() if d.is_dir() and d.name != "CONSOLIDATION_SUMMARY.json"]
    logger.info(f"Found {len(album_dirs)} main album directories after consolidation")

    # Look for key directories that should exist
    expected_dirs = [
        "In_This_Alley_Where_I_Hide",
        "Willow_Whispers",
        "Summer_Love",
        "Heroes_Rise_Villains_Overthrow",
    ]
    found_expected = []

    for expected_dir in expected_dirs:
        if (base_path / expected_dir).exists():
            found_expected.append(expected_dir)
            # Count files in each directory
            files_count = len(list((base_path / expected_dir).rglob("*")))
            logger.info(f"Found {expected_dir} with {files_count} items")

    logger.info(f"Found {len(found_expected)} out of {len(expected_dirs)} expected directories")
    return len(found_expected) == len(expected_dirs)


if __name__ == "__main__":
    print("Starting nocTurneMeLoDieS V4 - AvatarArts Consolidation Process...")
    print("This will consolidate content from ALBUMS/Albums/ into main ALBUMS directory")

    # Perform consolidation
    results = consolidate_albums()

    # Verify results
    verification_passed = verify_consolidation()

    print("\nConsolidation Results:")
    print(f"- Directories processed: {results['directories_processed']}")
    print(f"- Files moved: {results['files_moved']}")
    print(f"- Conflicts resolved: {results['conflicts_resolved']}")
    print(f"- Errors: {len(results['errors'])}")
    print(f"- Verification passed: {verification_passed}")

    if results["errors"]:
        print("\nErrors encountered:")
        for error in results["errors"]:
            print(f"  - {error}")

    print("\nConsolidation process completed.")
