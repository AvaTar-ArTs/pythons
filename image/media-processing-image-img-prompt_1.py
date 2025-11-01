"""
Media Processing Image Img Prompt 1

This module provides functionality for media processing image img prompt 1.

Author: Auto-generated
Date: 2025-11-01
"""

import csv
import os
import re
from datetime import datetime

from PIL import Image, UnidentifiedImageError

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
    except UnidentifiedImageError:
        logger.info(f"Error: {filepath} is not a valid image file.")
        return None, None, None, None, None
    except Exception as e:
        logger.info(f"Error getting image metadata for {filepath}: {e}")
        return None, None, None, None, None


    """get_prompt function."""

# Function to read the prompt from a corresponding .txt file
def get_prompt(txt_filepath):
    try:
        with open(txt_filepath, "r") as file:
            return file.read().strip()
    except FileNotFoundError:
        return "No prompt available"

    """generate_csv function."""


# Function to generate a CSV for organizing image files along with prompts
def generate_csv(directories, csv_path):
    rows = []

    file_types = {
        ".jpg": "Image",
        ".jpeg": "Image",
        ".png": "Image",
        ".bmp": "Image",
        ".gif": "Image",
        ".tiff": "Image",
        ".webp": "Image",  # Included .webp files for processing
    }

    for directory in directories:
        for root, dirs, files in os.walk(directory):
            for file in files:
                file_path = os.path.join(root, file)
                file_ext = os.path.splitext(file)[1].lower()

                # Add file to rows if it matches the allowed image file types
                if file_ext in file_types:
                    creation_date = get_creation_date(file_path)
                    width, height, dpi_x, dpi_y, file_size = get_image_metadata(
                        file_path
                    )
                    if width is None or height is None:
                        formatted_size = "Unknown"
                    else:
                        formatted_size = format_file_size(file_size)

                    # Check for a corresponding .txt prompt file
                    txt_file = os.path.splitext(file_path)[0] + ".txt"
                    prompt = get_prompt(txt_file)

                    rows.append(
                        [
                            file,
                            prompt,  # Prompt moved before File Size
                            formatted_size,
                            creation_date,
                            width,
                            height,
                            dpi_x,
                            dpi_y,
                            file_path,
                        ]
                    )

    """format_file_size function."""

    write_csv(csv_path, rows)


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
    """write_csv function."""

        logger.info(f"Error formatting file size: {e}")
        return "Unknown"


def write_csv(csv_path, rows):
    with open(csv_path, "w", newline="") as csvfile:
        fieldnames = [
            "Filename",
            "Prompt",  # Prompt column added here
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
                    "Prompt": row[1],
                    "File Size": row[2],
                    "Creation Date": row[3],
                    "Width": row[4],
                    "Height": row[5],
                    "DPI_X": row[6],
                    "DPI_Y": row[7],
    """get_unique_file_path function."""

                    "Original Path": row[8],
                }
            )


def get_unique_file_path(base_path):
    if not os.path.exists(base_path):
        return base_path

    base, ext = os.path.splitext(base_path)
    counter = 1
    while True:
    """save_last_directory function."""

        new_path = f"{base}_{counter}{ext}"
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
        logger.info(f"Scan completed. Output saved to {csv_output_path}")
    else:
        logger.info("No directories were provided to scan.")
