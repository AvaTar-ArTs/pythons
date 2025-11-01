"""
Data Processing Csv Docs 11

This module provides functionality for data processing csv docs 11.

Author: Auto-generated
Date: 2025-11-01
"""

import os
import csv
import re
import logging
from pathlib import Path

# Constants
CONSTANT_1024 = 1024
CONSTANT_1234 = 1234


logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

# Pre-compile all patterns for performance and clarity
EXCLUDED_REGEXES = [
    re.compile(pattern)
    for pattern in [
        r"^\..*",  # Hidden files/directories at the root
        r".*\/venv\/.*",  # venv directories
        r".*\/\.venv\/.*",  # .venv directories
        r".*\/lib\/.*",  # library directories
        r".*\/\.lib\/.*",  # .lib directories
        r".*\/my_global_venv\/.*",
        r".*\/simplegallery\/.*",
        r".*\/avatararts\/.*",
        r".*\/GitHub\/.*",
        r".*\/bluesky\/.*",
        r".*\/Documents\/gitHub\/.*",
        r".*\/\.my_global_venv\/.*",
        r".*\/node\/.*",
        r".*\/miniconda3\/.*",
        r".*\/env\/.*",  # env directories
        r".*\/\.env\/.*",  # .env directories
        r".*\/Library\/.*",  # Library directories
        r".*\/\.config\/.*",  # .config directories
        r".*\/\.spicetify\/.*",  # .spicetify directories
        r".*\/\.gem\/.*",  # .gem directories
        r".*\/\.zprofile\/.*",  # .zprofile directories
        r"^.*\/\..*",  # Any file or directory starting with a dot
    ]
]

# Map extensions to their categories; here all are 'Documents'
FILE_TYPES = {
    ".pdf": "Documents",
    ".csv": "Documents",
    ".html": "Documents",
    ".css": "Documents",
    ".js": "Documents",
    ".json": "Documents",
    ".sh": "Documents",
    ".md": "Documents",
    ".txt": "Documents",
    ".doc": "Documents",
    ".docx": "Documents",
    ".ppt": "Documents",
    ".pptx": "Documents",
    ".xlsx": "Documents",
    ".py": "Documents",
    ".xml": "Documents",
}


def generate_dry_run_csv(directories, csv_path):
    """
    Recursively walks through each directory in 'directories', excluding paths
    matching EXCLUDED_REGEXES. For files whose extension appears in FILE_TYPES,
    gathers info (filename, size, creation date, parent directory) and writes it
    to 'csv_path' in CSV format.

    :param directories: List of directory paths (strings) to walk through.
    :param csv_path: The output CSV file path (string).
    :return: A list of lists, where each inner list is [filename, file_size, creation_date, parent_path].
    """
    rows = []

    for directory in directories:
        dir_path = Path(directory)

        if not dir_path.is_dir():
            logger.warning(f"Skipping non-directory path: {dir_path}")
            continue

        logger.info(f"Walking directory: {dir_path}")

        # Use rglob('*') to recursively walk through all items
        for path_object in dir_path.rglob("*"):
            # 1) Skip directories that match excluded patterns
            if path_object.is_dir():
                if any(rgx.match(str(path_object)) for rgx in EXCLUDED_REGEXES):
                    continue
                # If it doesn't match, we keep descending
            # 2) Process files
            elif path_object.is_file():
                file_path_str = str(path_object)

                # Skip files that match excluded patterns
                if any(rgx.match(file_path_str) for rgx in EXCLUDED_REGEXES):
                    continue

                file_ext = path_object.suffix.lower()
                if file_ext in FILE_TYPES:
                    # Single stat call for size & timestamps
                    stat_obj = path_object.stat()
                    file_size = format_file_size(stat_obj.st_size)
                    creation_date = get_creation_date(file_path_str, stat_obj)
                    rows.append(
                        [
                            path_object.name,
                            file_size,
                            creation_date,
                            str(path_object.parent),
                        ]
                    )
            else:
                # Symlink or special file; skip or handle as needed
                continue

    # Write results to CSV
    write_csv(csv_path, rows)
    logger.info(f"Collected {len(rows)} items. CSV saved to: {csv_path}")

    return rows


def write_csv(csv_path, rows):
    """
    Writes the collected rows to a CSV with header fields:
    'Filename', 'File Size', 'Creation Date', 'Original Path'.
    """
    with open(csv_path, "w", newline="", encoding="utf-8") as csvfile:
        fieldnames = ["Filename", "File Size", "Creation Date", "Original Path"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow(
                {
                    "Filename": row[0],
                    "File Size": row[1],
                    "Creation Date": row[2],
                    "Original Path": row[3],
                }
            )


def format_file_size(size_in_bytes):
    """
    Convert a numeric size in bytes to a human-readable string, e.g.:
    CONSTANT_1234 -> '1.21 KB'
    """
    # Basic example
    # You can extend this to handle GB, TB, etc., as needed.
    if size_in_bytes < CONSTANT_1024:
        return f"{size_in_bytes} B"
    elif size_in_bytes < CONSTANT_1024**2:
        return f"{size_in_bytes / CONSTANT_1024:.2f} KB"
    else:
        return f"{size_in_bytes / CONSTANT_1024**2:.2f} MB"


def get_creation_date(file_path, stat_obj=None):
    """
    Retrieves a creation or 'birth' time for the file. On Windows,
    st_ctime is the creation date; on Unix, it's the inode change time.
    This may not be an exact creation date on some systems.

    :param file_path: Full path to the file (string).
    :param stat_obj: Optional os.stat_result object to avoid repeated os.stat calls.
    :return: A string representation of the creation date (or change date).
    """
    if stat_obj is None:
        stat_obj = os.stat(file_path)
    # On many Unix systems, st_ctime is the time of last metadata change.
    # For Windows, it’s the creation time.
    import datetime

    ctime = stat_obj.st_ctime
    # Convert to a human-friendly date string
    return datetime.datetime.fromtimestamp(ctime).strftime("%Y-%m-%d %H:%M:%S")


# Optional: track last used directory
LAST_DIRECTORY_FILE = "/some/path/last_directory.txt"


def save_last_directory(directory):
    """
    Saves the last-used directory path into a file, so we can load it next time.
    """
    with open(LAST_DIRECTORY_FILE, "w", encoding="utf-8") as file:
        file.write(directory)


def load_last_directory():
    """
    Loads a previously saved directory path if it exists, else returns None.
    """
    if os.path.exists(LAST_DIRECTORY_FILE):
        with open(LAST_DIRECTORY_FILE, "r", encoding="utf-8") as file:
            return file.read().strip()
    return None


def get_unique_file_path(base_path):
    """
    If 'base_path' already exists, append an incrementing suffix:
    e.g., 'output.csv' -> 'output_1.csv' -> 'output_2.csv', etc.
    """
    if not os.path.exists(base_path):
        return base_path

    base, ext = os.path.splitext(base_path)
    counter = 1
    while True:
        new_path = f"{base}_{counter}{ext}"
        if not os.path.exists(new_path):
            return new_path
        counter += 1
