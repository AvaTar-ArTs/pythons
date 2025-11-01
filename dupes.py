"""
Dupes

This module provides functionality for dupes.

Author: Auto-generated
Date: 2025-11-01
"""

import csv
import hashlib
import os
import re
from collections import defaultdict

import logging

logger = logging.getLogger(__name__)


# Constants
CONSTANT_4096 = 4096


def is_excluded(path, patterns):
    """
    Check if a given path matches any of the exclusion patterns.

    Parameters:
    path (str): The path to check.
    patterns (list): A list of regex patterns for exclusion.

    Returns:
    bool: True if path matches any pattern, False otherwise.
    """
    for pattern in patterns:
        if re.search(pattern, path):
            return True
    return False


def scan_directory(directory, excluded_patterns):
    """
    Scan a given directory, excluding files and directories
    that match the patterns, and return the list of files.

    Parameters:
    directory (str): The directory to scan.
    excluded_patterns (list): A list of regex patterns for exclusion.

    Returns:
    list: A list of file paths that do not match any exclusion patterns.
    """
    files_list = []
    for root, dirs, files in os.walk(directory):
        # Exclude directories in-place
        dirs[:] = [
            d for d in dirs if not is_excluded(os.path.join(root, d), excluded_patterns)
        ]
        for file in files:
            file_path = os.path.join(root, file)
            if not is_excluded(file_path, excluded_patterns):
                files_list.append(file_path)
    return files_list


def compute_md5(file_path):
    """
    Compute the MD5 hash of a file.

    Parameters:
    file_path (str): The path to the file.

    Returns:
    str: The MD5 hash of the file.
    """
    hash_md5 = hashlib.md5()
    try:
        with open(file_path, "rb") as f:
            for chunk in iter(lambda: f.read(CONSTANT_4096), b""):
                hash_md5.update(chunk)
        return hash_md5.hexdigest()
    except Exception as e:
        logger.info(f"Error computing hash for {file_path}: {e}")
        return None


def generate_detailed_duplicate_report(directories, csv_path):
    """
    Generate a detailed duplicate report containing all non-excluded file paths,
    their MD5 hashes, and duplicate counts.

    Parameters:
    directories (list): List of directories to scan.
    csv_path (str): Path to the output CSV file.
    """
    file_hash_map = defaultdict(list)

    # Regex patterns for exclusions
    excluded_patterns = [
        r"^\..*",  # Hidden files and directories
        r".*/venv/.*",  # venv directories
        r".*/\.venv/.*",  # .venv directories
        r".*/my_global_venv/.*",  # Specific venv directory
        r".*/simplegallery/.*",  # Simplegallery directories
        r".*/avatararts/.*",  # Avatararts directories
        r".*/github/.*",  # General github directories
        r".*/Documents/gitHub/.*",  # Specific gitHub directory in Documents
        r".*/\.my_global_venv/.*",  # .my_global_venv directories
        r".*/node/.*",  # Any directory named node
        r".*/Movies/CapCut/.*",  # CapCut directories in Movies
        r".*/miniconda3/.*",  # Miniconda3 directories
        r".*/miniconda3.bak/.*",  # Miniconda3 directories
        r".*/Movies/movavi/.*",  # Movavi directories in Movies
        r".*/env/.*",  # env directories
        r".*/\.env/.*",  # .env directories
        r".*/Library/.*",  # Library directories
        r".*/\.config/.*",  # .config directories
        r".*/\.spicetify/.*",  # .spicetify directories
        r".*/\.gem/.*",  # .gem directories
        r".*/\.zprofile/.*",  # .zprofile directories
        r"^.*\/\..*",  # Any file or directory starting with a dot (hidden files)
    ]

    for directory in directories:
        files_list = scan_directory(directory, excluded_patterns)
        for file_path in files_list:
            file_hash = compute_md5(file_path)
            if file_hash:
                file_hash_map[file_hash].append(file_path)

    rows = []
    for file_hash, paths in file_hash_map.items():
        for path in paths:
            rows.append([path, file_hash, len(paths)])

    with open(csv_path, "w", newline="") as csvfile:
        csv_writer = csv.writer(csvfile)
        csv_writer.writerow(["File Path", "MD5 Hash", "Duplicate Count"])
        csv_writer.writerows(rows)

    logger.info(f"CSV output written to {csv_path}")


# Function to prompt user for directories
def prompt_for_directories():
    """prompt_for_directories function."""

    directories = []
    while True:
        dir_input = input("Enter a directory to scan (or 'N' to finish): ").strip()
        if dir_input.lower() == "n":
            if directories:
                verify = (
                    input(
                        f"Do you want to add '{directories[-1]}' as the last directory? (Y/N): "
                    )
                    .strip()
                    .lower()
                )
                if verify == "y":
                    logger.info("Directory list completed.")
                    break
                else:
                    directories.pop()
                    logger.info(f"Removed last directory. Current list: {directories}")
            else:
                logger.info("No directories were added. Exiting setup.")
                break
        else:
            directories.append(dir_input)
            logger.info(f"Added: {dir_input}")
            logger.info(f"Current list: {directories}")
    return directories


# Prompt user for directories until they are done
directories = prompt_for_directories()

# Check if directories are non-empty before generating CSV
if directories:
    csv_path = "detailed_duplicate_report.csv"
    generate_detailed_duplicate_report(directories, csv_path)
else:
    logger.info("No directories provided. Exiting.")
