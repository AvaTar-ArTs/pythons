"""
Image Upscaler Sips Macos

This module provides functionality for image upscaler sips macos.

Author: Auto-generated
Date: 2025-11-01
"""

import csv
import os
import re
from datetime import datetime

from PIL import Image

import logging

logger = logging.getLogger(__name__)


# Constants
CONSTANT_1024 = 1024


# Constants
LAST_DIRECTORY_FILE = "image_data.txt"

# Function to get the creation date of a file


def get_creation_date(filepath):
    """get_creation_date function."""

    try:
        return datetime.fromtimestamp(os.path.getctime(filepath)).strftime("%m-%d-%y")
    except Exception as e:
        logger.info(f"Error getting creation date for {filepath}: {e}")
        return "Unknown"


# Function to extract metadata from an image file using PIL


    """get_image_metadata function."""

def get_image_metadata(filepath):
    try:
        with Image.open(filepath) as img:
            width, height = img.size
            dpi = img.info.get("dpi", (None, None))  # Extract DPI if available
            dpi_x = dpi[0] if dpi and len(dpi) > 0 else None
            dpi_y = dpi[1] if dpi and len(dpi) > 1 else None
            file_size = os.path.getsize(filepath)
            return width, height, dpi_x, dpi_y, file_size
    except Exception as e:
        logger.info(f"Error getting image metadata for {filepath}: {e}")
        return None, None, None, None, None


# Function to format file size

    """format_file_size function."""


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


# Function to generate a CSV for organizing image files
    """generate_csv function."""



def generate_csv(directories, csv_path):
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
        ".jpg": "Image",
        ".jpeg": "Image",
        ".png": "Image",
        ".bmp": "Image",
        ".gif": "Image",
        ".tiff": "Image",
    }

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

                # Add file to rows if it matches the logical file types
                if file_ext in file_types:
                    creation_date = get_creation_date(file_path)
                    width, height, dpi_x, dpi_y, file_size = get_image_metadata(
                        file_path
                    )
                    if width is None or height is None:
                        formatted_size = "Unknown"
                    else:
                        formatted_size = format_file_size(file_size)
                    rows.append(
                        [
                            file,
                            formatted_size,
                            creation_date,
                            width,
                            height,
                            dpi_x,
                            dpi_y,
                            file_path,
                        ]
                    )

    """write_csv function."""

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
    """get_unique_file_path function."""

                }
            )


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


def save_last_directory(directory):
    with open(LAST_DIRECTORY_FILE, "w") as file:
        file.write(directory)


def load_last_directory():
    if os.path.exists(LAST_DIRECTORY_FILE):
        with open(LAST_DIRECTORY_FILE, "r") as file:
            return file.read().strip()
    return None


if __name__ == "__main__":
    last_directory = load_last_directory()

    if last_directory:
        directories = [last_directory]
    else:
        print(
            "No last directory found. Please enter a source directory to scan for image files."
        )
        source_directory = input(
            "Please enter a source directory to scan for image files: "
        ).strip()
        if os.path.isdir(source_directory):
            directories = [source_directory]
            save_last_directory(source_directory)
        else:
            logger.info(f"'{source_directory}' is not a valid directory. Exiting.")
            exit(1)

    if directories:
        current_date = datetime.now().strftime("%m-%d-%H-%M")
        csv_output_path = os.path.join(os.getcwd(), f"image_data-{current_date}.csv")
        csv_output_path = get_unique_file_path(csv_output_path)

        generate_csv(directories, csv_output_path)
        logger.info(f"Dry run completed. Output saved to {csv_output_path}")
    else:
        logger.info("No directories were provided to scan.")
