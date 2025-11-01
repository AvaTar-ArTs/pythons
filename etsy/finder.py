"""
Finder

This module provides functionality for finder.

Author: Auto-generated
Date: 2025-11-01
"""

import logging

logger = logging.getLogger(__name__)


# Constants
CONSTANT_100 = 100
CONSTANT_1024 = 1024
CONSTANT_4096 = 4096

#!/usr/bin/env python3
"""
Comprehensive Duplicate File Detection Script
Analyzes files for exact duplicates using MD5 hashing and naming patterns
"""

import os
import hashlib
import json
from collections import defaultdict
from pathlib import Path
import re


def calculate_file_hash(filepath):
    """Calculate MD5 hash of a file"""
    hash_md5 = hashlib.md5()
    try:
        with open(filepath, "rb") as f:
            for chunk in iter(lambda: f.read(CONSTANT_4096), b""):
                hash_md5.update(chunk)
        return hash_md5.hexdigest()
    except (IOError, OSError) as e:
        logger.info(f"Error reading {filepath}: {e}")
        return None


def extract_base_name(filename):
    """Extract base name without (1), (2) etc. suffixes"""
    # Remove file extension
    name_without_ext = os.path.splitext(filename)[0]
    # Remove (1), (2), etc. patterns
    base_name = re.sub(r"\s*\(\d+\)$", "", name_without_ext)
    return base_name


def find_duplicates(directory):
    """Find all types of duplicates in the directory"""
    logger.info(f"Analyzing directory: {directory}")
    logger.info("=" * 60)

    # Storage for different types of duplicates
    hash_groups = defaultdict(list)  # Files with same MD5 hash
    name_groups = defaultdict(list)  # Files with similar base names
    all_files = []

    # Get all JPG files
    jpg_files = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.lower().endswith(".jpg"):
                full_path = os.path.join(root, file)
                jpg_files.append(full_path)

    logger.info(f"Found {len(jpg_files)} JPG files")
    logger.info("Calculating file hashes...")

    # Process files and calculate hashes
    processed = 0
    for filepath in jpg_files:
        if processed % CONSTANT_100 == 0:
            logger.info(f"Processed {processed}/{len(jpg_files)} files...")

        filename = os.path.basename(filepath)
        file_size = os.path.getsize(filepath)

        # Calculate hash
        file_hash = calculate_file_hash(filepath)
        if file_hash:
            hash_groups[file_hash].append(
                {"path": filepath, "filename": filename, "size": file_size}
            )

        # Group by base name (without (1), (2) suffixes)
        base_name = extract_base_name(filename)
        name_groups[base_name].append(
            {"path": filepath, "filename": filename, "size": file_size}
        )

        processed += 1

    logger.info(f"Analysis complete! Processed {processed} files")
    logger.info("=" * 60)

    # Find exact duplicates (same hash)
    exact_duplicates = {h: files for h, files in hash_groups.items() if len(files) > 1}

    # Find potential duplicates by name
    name_duplicates = {
        name: files for name, files in name_groups.items() if len(files) > 1
    }

    # Generate reports
    logger.info("\n🔍 DUPLICATE ANALYSIS RESULTS")
    logger.info("=" * 60)

    logger.info(f"\n📊 SUMMARY:")
    logger.info(f"  • Total files analyzed: {len(jpg_files)}")
    logger.info(f"  • Exact duplicates (same content): {len(exact_duplicates)} groups")
    logger.info(
        f"  • Potential duplicates (similar names): {len(name_duplicates)} groups"
    )

    # Calculate space that could be saved
    total_duplicate_size = 0
    for files in exact_duplicates.values():
        # Keep one file, calculate size of duplicates
        if len(files) > 1:
            duplicate_size = sum(f["size"] for f in files[1:])  # Skip first file
            total_duplicate_size += duplicate_size

    logger.info(
        f"  • Space that could be saved: {total_duplicate_size / (CONSTANT_1024*CONSTANT_1024):.2f} MB"
    )

    # Report exact duplicates
    if exact_duplicates:
        logger.info(f"\n🎯 EXACT DUPLICATES (Same Content):")
        logger.info("-" * 40)
        for i, (file_hash, files) in enumerate(exact_duplicates.items(), 1):
            logger.info(
                f"\nGroup {i} ({len(files)} files, {files[0]['size'] / CONSTANT_1024:.1f} KB each):"
            )
            for file_info in files:
                logger.info(f"  • {file_info['filename']}")

    # Report name-based duplicates
    if name_duplicates:
        logger.info(f"\n📝 POTENTIAL DUPLICATES (Similar Names):")
        logger.info("-" * 40)
        for i, (base_name, files) in enumerate(name_duplicates.items(), 1):
            if i <= 10:  # Show first 10 groups
                logger.info(f"\nGroup {i} ({len(files)} files):")
                for file_info in files:
                    logger.info(f"  • {file_info['filename']}")
            elif i == 11:
                logger.info(f"\n... and {len(name_duplicates) - 10} more groups")
                break

    # Save detailed results to JSON
    results = {
        "summary": {
            "total_files": len(jpg_files),
            "exact_duplicate_groups": len(exact_duplicates),
            "name_duplicate_groups": len(name_duplicates),
            "space_savings_mb": total_duplicate_size / (CONSTANT_1024 * CONSTANT_1024),
        },
        "exact_duplicates": {h: files for h, files in exact_duplicates.items()},
        "name_duplicates": {name: files for name, files in name_duplicates.items()},
    }

    with open(os.path.join(directory, "duplicate_analysis.json"), "w") as f:
        json.dump(results, f, indent=2)

    logger.info(f"\n💾 Detailed results saved to: duplicate_analysis.json")

    return results


if __name__ == "__main__":
    directory = Path(str(Path.home()) + "/Pictures/etsy/ideo-1012")
    results = find_duplicates(directory)
