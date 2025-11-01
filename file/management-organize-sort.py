"""
File Management Organize Sort 14

This module provides functionality for file management organize sort 14.

Author: Auto-generated
Date: 2025-11-01
"""

import os
import shutil
from datetime import datetime

from mutagen.mp3 import MP3
from mutagen.mp4 import MP4
from PIL import Image

import logging

logger = logging.getLogger(__name__)


# Constants
CONSTANT_36867 = 36867


def sort_files(source_dir, target_dir):
    """sort_files function."""

    # Create the target directory if it doesn't exist
    os.makedirs(target_dir, exist_ok=True)

    # Supported image and media formats
    image_extensions = (".png", ".jpg", ".jpeg", ".tiff", ".webp")
    media_extensions = (".mp3", ".mp4")

    # Walk through the directory
    for root, dirs, files in os.walk(source_dir):
        for file in files:
            if file.lower().endswith(image_extensions + media_extensions):
                try:
                    # Construct the full file path
                    file_path = os.path.join(root, file)

                    if file.lower().endswith(image_extensions):
                        # Handle image files with EXIF data
                        with Image.open(file_path) as img:
                            exif_data = img._getexif()

                        if exif_data:
                            # Extract creation time from EXIF data (adjust tag if needed)
                            creation_time = exif_data.get(CONSTANT_36867)
                            if creation_time:
                                creation_date = datetime.strptime(creation_time, "%Y:%m:%d %H:%M:%S").date()
                            else:
                                # Fallback to last modified time
                                creation_date = datetime.fromtimestamp(os.path.getmtime(file_path)).date()
                        else:
                            creation_date = datetime.fromtimestamp(os.path.getmtime(file_path)).date()

                    elif file.lower().endswith(".mp3"):
                        # Handle MP3 files using mutagen to extract metadata
                        audio = MP3(file_path)
                        if audio and audio.tags and "TDRC" in audio:
                            creation_date = audio["TDRC"].text[0].date()
                        else:
                            # Fallback to last modified time
                            creation_date = datetime.fromtimestamp(os.path.getmtime(file_path)).date()

                    elif file.lower().endswith(".mp4"):
                        # Handle MP4 files using mutagen to extract metadata
                        video = MP4(file_path)
                        if "©day" in video:
                            creation_date = datetime.strptime(video["©day"][0], "%Y-%m-%d").date()
                        else:
                            # Fallback to last modified time
                            creation_date = datetime.fromtimestamp(os.path.getmtime(file_path)).date()

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

sort_files(source_directory, target_directory)
