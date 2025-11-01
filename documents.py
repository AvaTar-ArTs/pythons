"""
Documents

This module provides functionality for documents.

Author: Auto-generated
Date: 2025-11-01
"""

import logging

logger = logging.getLogger(__name__)


# Constants
CONSTANT_1024 = 1024

#!/usr/bin/env python3
"""
Script to create a CSV backup of ~/documents directory in the same format as ~/clean
"""

from pathlib import Path
import os
import csv
import re
from datetime import datetime


def get_creation_date(filepath):
    """Get the creation date of a file in MM-DD-YY format"""
    try:
        return datetime.fromtimestamp(os.path.getctime(filepath)).strftime("%m-%d-%y")
    except Exception as e:
        logger.info(f"Error getting creation date for {filepath}: {e}")
        return "Unknown"


def format_file_size(size_in_bytes):
    """Format file size in human readable format"""
    try:
        if size_in_bytes < CONSTANT_1024:
            return f"{size_in_bytes:.2f} B"
        size_in_bytes /= CONSTANT_1024
        if size_in_bytes < CONSTANT_1024:
            return f"{size_in_bytes:.2f} KB"
        size_in_bytes /= CONSTANT_1024
        if size_in_bytes < CONSTANT_1024:
            return f"{size_in_bytes:.2f} MB"
        size_in_bytes /= CONSTANT_1024
        if size_in_bytes < CONSTANT_1024:
            return f"{size_in_bytes:.2f} GB"
        size_in_bytes /= CONSTANT_1024
        return f"{size_in_bytes:.2f} TB"
    except Exception as e:
        logger.info(f"Error formatting file size: {e}")
        return "Unknown"


def generate_documents_backup_csv(directory, csv_path):
    """Generate CSV backup of documents directory"""
    rows = []

    # Regex patterns for exclusions (same as in the original script)
    excluded_patterns = [
        r"^\..*",  # Hidden files and directories
        r".*\/venv\/.*",  # venv directories
        r".*\/\.venv\/.*",  # .venv directories
        r".*\/lib\/.*",  # venv directories
        r".*\/\.lib\/.*",  # .venv directories
        r".*\/my_global_venv\/.*",  # venv directories
        r".*\/simplegallery\/.*",
        r".*\/avatararts\/.*",
        r".*\/github\/.*",
        r".*\/Documents\/gitHub\/.*",  # Specific gitHub directory
        r".*\/\.my_global_venv\/.*",  # .venv directories
        r".*\/node\/.*",  # Any directory named node
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

    # File types to include (same as original)
    file_types = {
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

    logger.info(f"Scanning directory: {directory}")

    for root, dirs, files in os.walk(directory):
        # Skip hidden directories and system directories using regex
        dirs[:] = [
            d
            for d in dirs
            if not any(
                re.match(pattern, os.path.join(root, d))
                for pattern in excluded_patterns
            )
        ]

        for file in files:
            file_path = os.path.join(root, file)

            # Skip files that match the excluded patterns
            if any(re.match(pattern, file_path) for pattern in excluded_patterns):
                continue

            file_ext = os.path.splitext(file)[1].lower()

            # Add file to rows if it matches the logical file types
            if file_ext in file_types:
                try:
                    file_size = format_file_size(os.path.getsize(file_path))
                    creation_date = get_creation_date(file_path)
                    rows.append([file, file_size, creation_date, root])
                except Exception as e:
                    logger.info(f"Error processing file {file_path}: {e}")
                    continue

    # Write CSV file
    with open(csv_path, "w", newline="") as csvfile:
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

    logger.info(f"Found {len(rows)} files")
    return len(rows)


def get_unique_file_path(base_path):
    """Get a unique file path if the base path already exists"""
    if not os.path.exists(base_path):
        return base_path

    base, ext = os.path.splitext(base_path)
    counter = 1
    while True:
        new_path = f"{base}_{counter}{ext}"
        if not os.path.exists(new_path):
            return new_path
        counter += 1


if __name__ == "__main__":
    # Set the documents directory
    documents_dir = Path(str(Path.home()) + "/documents")

    # Generate output filename with timestamp
    current_date = datetime.now().strftime("%m-%d-%H:%M")
    csv_output_path = f"documents_backup_{current_date}.csv"
    csv_output_path = get_unique_file_path(csv_output_path)

    # Check if documents directory exists
    if not os.path.isdir(documents_dir):
        logger.info(f"Error: Directory {documents_dir} does not exist")
        exit(1)

    # Generate the CSV backup
    file_count = generate_documents_backup_csv(documents_dir, csv_output_path)

    logger.info(f"Documents backup completed. Output saved to {csv_output_path}")
    logger.info(f"Total files processed: {file_count}")
