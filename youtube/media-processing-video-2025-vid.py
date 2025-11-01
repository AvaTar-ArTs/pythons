"""
Media Processing Video 2025 Vid

This module provides functionality for media processing video 2025 vid.

Author: Auto-generated
Date: 2025-11-01
"""

import csv
import os
import re
from datetime import datetime

from mutagen.easymp4 import EasyMP4
from mutagen.mp4 import MP4

import logging

logger = logging.getLogger(__name__)


# Constants
CONSTANT_1024 = 1024
CONSTANT_3600 = 3600


LAST_DIRECTORY_FILE = "vids.txt"


# Function to get the creation date of a file
def get_creation_date(filepath):
    """get_creation_date function."""

    try:
        return datetime.fromtimestamp(os.path.getctime(filepath)).strftime("%m-%d-%y")
    except Exception as e:
        logger.info(f"Error getting creation date for {filepath}: {e}")
        return "Unknown"


# Function to extract metadata from a video file using Mutagen
    """get_video_metadata function."""

def get_video_metadata(filepath):
    try:
        file = MP4(filepath)
        duration = file.info.length
        return os.path.getsize(filepath), duration
    except Exception as e:
        logger.info(f"Error getting video metadata for {filepath}: {e}")
    return None, None


    """format_file_size function."""

# Function to format file size
def format_file_size(size_in_bytes):
    try:
        thresholds = [
            (CONSTANT_1024**4, "TB"),
            (CONSTANT_1024**3, "GB"),
            (CONSTANT_1024**2, "MB"),
            (CONSTANT_1024**1, "KB"),
            (CONSTANT_1024**0, "B"),
        ]
        for factor, suffix in thresholds:
            if size_in_bytes >= factor:
                break
        return f"{size_in_bytes / factor:.2f} {suffix}"
    except Exception as e:
        logger.info(f"Error formatting file size: {e}")
        return "Unknown"

    """format_duration function."""


# Function to format duration in H:M:S or M:S
def format_duration(duration_in_seconds):
    if duration_in_seconds is None:
        return "Unknown"
    try:
        hours = int(duration_in_seconds // CONSTANT_3600)
        minutes = int((duration_in_seconds % CONSTANT_3600) // 60)
        seconds = int(duration_in_seconds % 60)
        if hours > 0:
            return f"{hours}:{minutes:02d}:{seconds:02d}"
        else:
            return f"{minutes}:{seconds:02d}"
    except Exception as e:
        logger.info(f"Error formatting duration: {e}")
        return "Unknown"
    """generate_dry_run_csv function."""



# Function to generate a dry run CSV for organizing video files
def generate_dry_run_csv(directories, csv_path):
    rows = []

    # Regex patterns for exclusions
    excluded_patterns = [
        r"^\..*",  # Hidden files and directories
        # Your other exclusions here...
    ]

    file_types = {
        ".mp4": "Videos",
        ".mkv": "Videos",
        ".mov": "Videos",
        ".avi": "Videos",
        ".wmv": "Videos",
        ".webm": "Videos",
    }

    # Keywords to search for in file names (case insensitive)
    keywords = [r"project2025", r"Project 2025", r"project"]

    for directory in directories:
        for root, dirs, files in os.walk(directory):
            # Skip hidden directories and venv directories using regex
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

                # Add file to rows if it matches the file types and contains keyword
                if file_ext in file_types and any(
                    re.search(keyword, file, re.IGNORECASE) for keyword in keywords
                ):
                    creation_date = get_creation_date(file_path)
                    file_size, duration = get_video_metadata(file_path)
                    if file_size is None:
                        file_size = "Unknown"
                    else:
                        file_size = format_file_size(file_size)
                    formatted_duration = format_duration(duration)
                    rows.append(
                        [file, formatted_duration, file_size, creation_date, file_path]
                    )

    """write_csv function."""

    write_csv(csv_path, rows)


# Function to write data to a CSV file
def write_csv(csv_path, rows):
    with open(csv_path, "w", newline="") as csvfile:
        fieldnames = [
            "Filename",
            "Duration",
            "File Size",
            "Creation Date",
            "Original Path",
        ]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow(
                {
                    "Filename": row[0],
                    "Duration": row[1],
                    "File Size": row[2],
                    "Creation Date": row[3],
                    "Original Path": row[4],
    """get_unique_file_path function."""

                }
            )


# Function to get a unique file path (in case the file already exists)
def get_unique_file_path(base_path):
    if not os.path.exists(base_path):
        return base_path

    base, ext = os.path.splitext(base_path)
    counter = 1
    while True:
        new_path = f"{base}_{counter}{ext}"
    """save_last_directory function."""

        if not os.path.exists(new_path):
            return new_path
        counter += 1


    """load_last_directory function."""

# Function to save the last scanned directory
def save_last_directory(directory):
    with open(LAST_DIRECTORY_FILE, "w") as file:
        file.write(directory)


# Function to load the last scanned directory
def load_last_directory():
    if os.path.exists(LAST_DIRECTORY_FILE):
        with open(LAST_DIRECTORY_FILE, "r") as file:
            return file.read().strip()
    return None


# Main function to run the script
if __name__ == "__main__":
    directories = []
    last_directory = load_last_directory()

    while True:
        if last_directory:
            use_last = (
                input(
                    f"Do you want to use the last directory '{last_directory}'? (Y/N): "
                )
                .strip()
                .lower()
            )
            if use_last == "y":
                directories.append(last_directory)
                break
            else:
                source_directory = input(
                    "Please enter a new source directory to scan for video files: "
                ).strip()
        else:
            source_directory = input(
                "Please enter a source directory to scan for video files: "
            ).strip()

        if source_directory == "":
            break
        if os.path.isdir(source_directory):
            directories.append(source_directory)
            save_last_directory(source_directory)
        else:
            logger.info(f"'{source_directory}' is not a valid directory. Please try again.")

    if directories:
        current_date = datetime.now().strftime("%m-%d-%H:%M")
        csv_output_path = os.path.join(os.getcwd(), f"vids-{current_date}.csv")
        csv_output_path = get_unique_file_path(csv_output_path)

        generate_dry_run_csv(directories, csv_output_path)
        logger.info(f"Dry run completed. Output saved to {csv_output_path}")
    else:
        logger.info("No directories were provided to scan.")
