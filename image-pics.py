"""
Media Processing Image Pics 1

This module provides functionality for media processing image pics 1.

Author: Auto-generated
Date: 2025-11-01
"""

import os
import csv
from datetime import datetime
from PIL import Image

import logging

logger = logging.getLogger(__name__)


# Constants
CONSTANT_1024 = 1024



LAST_DIRECTORY_FILE = "images.txt"

# Function to get the creation date of a file


def get_creation_date(filepath):
    try:
        return datetime.fromtimestamp(
            os.path.getctime(filepath)).strftime("%m-%d-%y")
    except Exception as e:
        logger.info(f"Error getting creation date for {filepath}: {e}")
        return "Unknown"


# Function to extract metadata from an image file using PIL
def get_image_metadata(filepath):
    try:
        with Image.open(filepath) as img:
            width, height = img.size
            dpi = img.info.get("dpi", (None, None))
            return width, height, dpi[0], dpi[1]
    except Exception as e:
        logger.info(f"Error getting image metadata for {filepath}: {e}")
        return None, None, None, None


# Function to format file size

def format_file_size(size_in_bytes):
    thresholds = [
        (CONSTANT_1024**4, "TB"),
        (CONSTANT_1024**3, "GB"),
        (CONSTANT_1024**2, "MB"),
        (CONSTANT_1024**1, "KB"),
    ]
    for factor, suffix in thresholds:
        if size_in_bytes >= factor:
            break
    return f"{size_in_bytes / factor:.2f} {suffix}"


# Function to generate a CSV for organizing image files


def generate_csv(directories, csv_path):
    rows = []
    file_types = {".jpg", ".jpeg", ".png", ".gif", ".bmp", ".tiff"}
# Function to generate a dry run CSV for organizing audio files


def generate_dry_run_csv(directories, csv_path):
    rows = []

    # Regex patterns for exclusions
    excluded_patterns = [
        r"^\..*",  # Hidden files and directories
        r".*\/venv\/.*",  # venv directories
        r".*\/\.venv\/.*",  # .venv directories
        r".*\/my_global_venv\/.*",  # venv directories
        r".*\/simplegallery\/.*",
        r".*\/avatararts\/.*",
        r".*\/github\/.*",
        r".*\/Documents\/gitHub\/.*",  # Specific gitHub directory
        r".*\/\.my_global_venv\/.*",  # .venv directories
        r".*\/node\/.*",  # Any directory named node
        r".*\/Movies\/capcut\/.*",
        r".*\/miniconda3\/.*",
        r".*\/Movies\/movavi\/.*",
        r".*\/env\/.*",  # env directories
        r".*\/\.env\/.*",  # .env directories
        r".*\/Library\/.*",  # Library directories
        r".*\/\.config\/.*",  # .config directories
        r".*\/\.spicetify\/.*",  # .spicetify directories
        r".*\/\.gem\/.*",  # .gem directories
        r".*\/\.zprofile\/.*",  # .zprofile directories
        r"^.*\/\..*",  # Any file or directory starting with a dot
    ]

    file_types = {
        ".mp3": "Audio",
        ".wav": "Audio",
        ".flac": "Audio",
        ".aac": "Audio",
        ".m4a": "Audio",
    }

    for directory in directories:
        for root, dirs, files in os.walk(directory):
            for file in files:
                file_path = os.path.join(root, file)
                file_ext = os.path.splitext(file)[1].lower()

                if file_ext in file_types:
                    creation_date = get_creation_date(file_path)
                    file_size = format_file_size(os.path.getsize(file_path))
                    width, height, dpi_x, dpi_y = get_image_metadata(file_path)
                    rows.append(
                        [
                            file,
                            file_size,
                            creation_date,
                            width,
                            height,
                            dpi_x,
                            dpi_y,
                            file_path,
                        ]
                    )

    write_csv(csv_path, rows)


def write_csv(csv_path, rows):
    with open(csv_path, "w", newline="") as csvfile:
        fieldnames = [
            "Filename",
            "File Size",
            "Creation Date",
            "Width",
            "Height",
            "DPI_X",
            "DPI_Y",
            "Original Path",
        ]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow(
                {
                    "Filename": row[0],
                    "File Size": row[1],
                    "Creation Date": row[2],
                    "Width": row[3],
                    "Height": row[4],
                    "DPI_X": row[5],
                    "DPI_Y": row[6],
                    "Original Path": row[7],
                }
            )


def get_unique_file_path(base_path):
    if not os.path.exists(base_path):
        return base_path

    base, ext = os.path.splitext(base_path)
    counter = 1
    while True:
        new_path = f"{base}_{counter}{ext}"
        if not os.path.exists(new_path):
            return new_path
        counter += 1


def save_last_directory(directory):
    with open(LAST_DIRECTORY_FILE, "w") as file:
        file.write(directory)


def load_last_directory():
    if os.path.exists(LAST_DIRECTORY_FILE):
        with open(LAST_DIRECTORY_FILE, "r") as file:
            return file.read().strip()
    return None


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
                    "Please enter a new source directory to scan for image files: "
                ).strip()
        else:
            source_directory = input(
                "Please enter a source directory to scan for image files: "
            ).strip()

        if source_directory == "":
            break
        if os.path.isdir(source_directory):
            directories.append(source_directory)
            save_last_directory(source_directory)
        else:
            print(
                f"'{source_directory}' is not a valid directory. Please try again.")

    if directories:
        current_date = datetime.now().strftime("%m-%d-%H:%M")
        csv_output_path = os.path.join(
            os.getcwd(), f"images-{current_date}.csv")
        csv_output_path = get_unique_file_path(csv_output_path)

        generate_csv(directories, csv_output_path)
        logger.info(f"Dry run completed. Output saved to {csv_output_path}")
    else:
        logger.info("No directories were provided to scan.")
