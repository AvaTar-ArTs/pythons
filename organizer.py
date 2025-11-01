"""
Image Organizer

This module provides functionality for image organizer.

Author: Auto-generated
Date: 2025-11-01
"""

import os
import shutil
from datetime import datetime

from PIL import Image

import logging

logger = logging.getLogger(__name__)


# Constants
CONSTANT_36867 = 36867


def sort_images(source_dir, target_dir):
    """sort_images function."""

    # Create the target directory if it doesn't exist
    os.makedirs(target_dir, exist_ok=True)

    # Supported image formats
    extensions = (".png", ".jpg", ".jpeg", ".tiff", ".mp4", ".webp")

    # Walk through the directory
    for root, dirs, files in os.walk(source_dir):
        for file in files:
            if file.lower().endswith(extensions):
                try:
                    # Construct the full file path
                    file_path = os.path.join(root, file)

                    # Open the image file
                    with Image.open(file_path) as img:
                        # Extract EXIF data
                        exif_data = img._getexif()

                    # Find the creation time (this is platform-dependent)
                    if exif_data:
                        # Convert the timestamp to a datetime object (adjust tag as necessary)
                        creation_time = exif_data.get(CONSTANT_36867)
                        if creation_time:
                            creation_date = datetime.strptime(
                                creation_time, "%Y:%m:%d %H:%M:%S"
                            ).date()
                        else:
                            # Fallback to last modified time if EXIF data is missing
                            creation_date = datetime.fromtimestamp(
                                os.path.getmtime(file_path)
                            ).date()
                    else:
                        creation_date = datetime.fromtimestamp(
                            os.path.getmtime(file_path)
                        ).date()

                    # Create a new directory for this date if it doesn't exist
                    date_dir = os.path.join(target_dir, str(creation_date))
                    os.makedirs(date_dir, exist_ok=True)

                    # Move the file
                    shutil.move(file_path, os.path.join(date_dir, file))
                    logger.info(f"Moved: {file_path} -> {os.path.join(date_dir, file)}")

                except Exception as e:
                    logger.info(f"Error processing {file}: {e}")


# Get user input for the source and target directories
source_directory = input("Enter the source directory path: ")
target_directory = input("Enter the target directory path: ")

sort_images(source_directory, target_directory)
