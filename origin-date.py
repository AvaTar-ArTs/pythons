"""
Img Origin Date

This module provides functionality for img origin date.

Author: Auto-generated
Date: 2025-11-01
"""

from pathlib import Path
import csv
import os
from datetime import datetime

from PIL import Image

import logging

logger = logging.getLogger(__name__)


# Constants
CONSTANT_1024 = 1024


# Function to get the creation date of a file
def get_creation_date(filepath):
    """get_creation_date function."""

    try:
        return datetime.fromtimestamp(os.path.getctime(filepath)).strftime("%y-%m-%d")
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

    """generate_csv function."""


# Function to generate a CSV for organizing image files
def generate_csv(directory, csv_path):
    rows = []

    file_types = {
        ".jpg": "Image",
        ".jpeg": "Image",
        ".png": "Image",
        ".bmp": "Image",
        ".gif": "Image",
        ".tiff": "Image",
    }

    for root, dirs, files in os.walk(directory):
        for file in files:
            file_path = os.path.join(root, file)
            file_ext = os.path.splitext(file)[1].lower()

            if file_ext in file_types:
                logger.info(f"Processing file: {file_path}")  # Debugging statement
                creation_date = get_creation_date(file_path)
                width, height, dpi_x, dpi_y, file_size = get_image_metadata(file_path)
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
                }
            )


if __name__ == "__main__":
    directory = Path("/Volumes/2T-Xx")

    current_date = datetime.now().strftime("%m-%d-%H-%M")
    csv_output_path = os.path.join(os.getcwd(), f"image_data-{current_date}.csv")

    generate_csv(directory, csv_output_path)
    logger.info(f"Dry run completed. Output saved to {csv_output_path}")
