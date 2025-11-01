"""
Development Web Frameworks Python 8

This module provides functionality for development web frameworks python 8.

Author: Auto-generated
Date: 2025-11-01
"""

import logging

logger = logging.getLogger(__name__)


# Constants
CONSTANT_1024 = 1024
CONSTANT_8192 = 8192

#!/usr/bin/env python3
"""
Enhanced Python Directory Metadata Analyzer
Creates comprehensive CSV with file metadata, analysis, and categorization
"""

import csv
import os
import time
import hashlib
import mimetypes
from pathlib import Path
from collections import defaultdict, Counter


def get_file_hash(filepath, chunk_size=CONSTANT_8192):
    """Calculate MD5 hash of file for duplicate detection"""
    hash_md5 = hashlib.md5()
    try:
        with open(filepath, "rb") as f:
            for chunk in iter(lambda: f.read(chunk_size), b""):
                hash_md5.update(chunk)
        return hash_md5.hexdigest()
    except (IOError, OSError):
        return "ERROR"


def analyze_python_file(filepath):
    """Analyze Python file for imports, functions, classes, and patterns"""
    analysis = {
        "imports": [],
        "functions": 0,
        "classes": 0,
        "lines_of_code": 0,
        "has_main": False,
        "has_docstring": False,
        "complexity_indicators": [],
    }

    try:
        with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
            lines = f.readlines()
            analysis["lines_of_code"] = len(lines)

            for i, line in enumerate(lines):
                line = line.strip()

                # Check for imports
                if line.startswith(("import ", "from ")):
                    analysis["imports"].append(line)

                # Count functions and classes
                if line.startswith("def "):
                    analysis["functions"] += 1
                elif line.startswith("class "):
                    analysis["classes"] += 1

                # Check for main block
                if line.startswith("if __name__"):
                    analysis["has_main"] = True

                # Check for docstring
                if i == 0 and ('"""' in line or "'''" in line):
                    analysis["has_docstring"] = True

                # Complexity indicators
                if any(
                    indicator in line
                    for indicator in [
                        "try:",
                        "except:",
                        "finally:",
                        "with ",
                        "lambda ",
                        "list(",
                        "dict(",
                        "set(",
                    ]
                ):
                    analysis["complexity_indicators"].append(line)

    except (IOError, OSError, UnicodeDecodeError):
        pass

    return analysis


def categorize_file(filename, filepath):
    """Categorize file based on name and path patterns"""
    categories = []
    filename_lower = filename.lower()
    path_lower = filepath.lower()

    # File type categories
    if filename_lower.endswith(".py"):
        categories.append("python")
    elif filename_lower.endswith((".txt", ".md", ".rst")):
        categories.append("documentation")
    elif filename_lower.endswith((".json", ".yaml", ".yml", ".toml")):
        categories.append("config")
    elif filename_lower.endswith((".csv", ".tsv")):
        categories.append("data")
    elif filename_lower.endswith((".log", ".out", ".err")):
        categories.append("log")

    # Functional categories based on naming patterns
    if any(pattern in filename_lower for pattern in ["test", "spec", "check"]):
        categories.append("testing")
    if any(pattern in filename_lower for pattern in ["util", "helper", "tool"]):
        categories.append("utility")
    if any(pattern in filename_lower for pattern in ["config", "setting", "conf"]):
        categories.append("configuration")
    if any(
        pattern in filename_lower for pattern in ["data", "process", "analyze", "parse"]
    ):
        categories.append("data_processing")
    if any(pattern in filename_lower for pattern in ["ai", "ml", "neural", "model"]):
        categories.append("ai_ml")
    if any(
        pattern in filename_lower
        for pattern in ["web", "api", "server", "flask", "django"]
    ):
        categories.append("web")
    if any(pattern in filename_lower for pattern in ["backup", "sync", "copy", "move"]):
        categories.append("file_management")
    if any(pattern in filename_lower for pattern in ["convert", "transform", "format"]):
        categories.append("conversion")
    if any(pattern in filename_lower for pattern in ["duplicate", "dedup", "unique"]):
        categories.append("deduplication")
    if any(pattern in filename_lower for pattern in ["install", "setup", "init"]):
        categories.append("installation")

    return "|".join(categories) if categories else "uncategorized"


def main():
    """main function."""

    directory = Path("/Users/steven/Documents/python")
    metadata_list = []
    file_hashes = defaultdict(list)
    duplicate_groups = []

    logger.info(f"Analyzing directory: {directory}")
    logger.info("Collecting file metadata...")

    # First pass: collect basic metadata
    for root, dirs, files in os.walk(directory):
        for file in files:
            filepath = os.path.join(root, file)
            try:
                stat = os.stat(filepath)
                relative_path = os.path.relpath(filepath, directory)

                # Get file hash for duplicate detection
                file_hash = get_file_hash(filepath)
                if file_hash != "ERROR":
                    file_hashes[file_hash].append(filepath)

                # Basic metadata
                metadata = {
                    "relative_path": relative_path,
                    "absolute_path": filepath,
                    "filename": file,
                    "directory": os.path.dirname(relative_path),
                    "size_bytes": stat.st_size,
                    "size_mb": round(stat.st_size / (CONSTANT_1024 * CONSTANT_1024), 2),
                    "created": time.strftime(
                        "%Y-%m-%d %H:%M:%S", time.localtime(stat.st_ctime)
                    ),
                    "modified": time.strftime(
                        "%Y-%m-%d %H:%M:%S", time.localtime(stat.st_mtime)
                    ),
                    "accessed": time.strftime(
                        "%Y-%m-%d %H:%M:%S", time.localtime(stat.st_atime)
                    ),
                    "file_extension": os.path.splitext(file)[1],
                    "mime_type": mimetypes.guess_type(filepath)[0] or "unknown",
                    "file_hash": file_hash,
                    "categories": categorize_file(file, relative_path),
                }

                # Python-specific analysis
                if file.endswith(".py"):
                    analysis = analyze_python_file(filepath)
                    metadata.update(
                        {
                            "imports_count": len(analysis["imports"]),
                            "functions_count": analysis["functions"],
                            "classes_count": analysis["classes"],
                            "lines_of_code": analysis["lines_of_code"],
                            "has_main_block": analysis["has_main"],
                            "has_docstring": analysis["has_docstring"],
                            "complexity_score": len(analysis["complexity_indicators"]),
                            "top_imports": "|".join(
                                analysis["imports"][:5]
                            ),  # Top 5 imports
                        }
                    )

                metadata_list.append(metadata)

            except (OSError, IOError) as e:
                logger.info(f"Error processing {filepath}: {e}")
                continue

    # Identify duplicates
    for file_hash, paths in file_hashes.items():
        if len(paths) > 1:
            duplicate_groups.append(
                {"hash": file_hash, "count": len(paths), "files": paths}
            )

    # Write comprehensive CSV
    csv_path = Path("/Users/steven/Documents/python/python_directory_metadata.csv")
    fieldnames = [
        "relative_path",
        "absolute_path",
        "filename",
        "directory",
        "size_bytes",
        "size_mb",
        "created",
        "modified",
        "accessed",
        "file_extension",
        "mime_type",
        "file_hash",
        "categories",
        "imports_count",
        "functions_count",
        "classes_count",
        "lines_of_code",
        "has_main_block",
        "has_docstring",
        "complexity_score",
        "top_imports",
    ]

    with open(csv_path, mode="w", newline="", encoding="utf-8") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for row in metadata_list:
            writer.writerow(row)

    # Generate summary statistics
    total_files = len(metadata_list)
    total_size = sum(row["size_bytes"] for row in metadata_list)
    python_files = [row for row in metadata_list if row["filename"].endswith(".py")]

    logger.info(f"\n=== ANALYSIS COMPLETE ===")
    logger.info(f"Total files analyzed: {total_files}")
    logger.info(f"Total size: {total_size / (CONSTANT_1024*CONSTANT_1024):.2f} MB")
    logger.info(f"Python files: {len(python_files)}")
    logger.info(f"Duplicate groups found: {len(duplicate_groups)}")
    logger.info(f"CSV saved to: {csv_path}")

    # Show top categories
    all_categories = []
    for row in metadata_list:
        all_categories.extend(row["categories"].split("|"))

    category_counts = Counter(all_categories)
    logger.info(f"\nTop file categories:")
    for category, count in category_counts.most_common(10):
        logger.info(f"  {category}: {count}")

    # Show largest files
    logger.info(f"\nLargest files:")
    largest_files = sorted(metadata_list, key=lambda x: x["size_bytes"], reverse=True)[
        :10
    ]
    for file_info in largest_files:
        logger.info(f"  {file_info['relative_path']}: {file_info['size_mb']} MB")

    # Show duplicates
    if duplicate_groups:
        logger.info(f"\nDuplicate files found:")
        for group in duplicate_groups[:5]:  # Show top 5 duplicate groups
            logger.info(f"  Hash {group['hash'][:8]}... ({group['count']} files)")
            for file_path in group["files"]:
                logger.info(f"    {os.path.relpath(file_path, directory)}")


if __name__ == "__main__":
    main()
