"""
Organize Albums V3

This module provides functionality for organize albums v3.

Author: Auto-generated
Date: 2025-11-01
"""

from pathlib import Path
import os
import shutil

import logging

logger = logging.getLogger(__name__)


# Define the base directory
base_dir = Path(str(Path.home()) + "/Music/NocTurnE-meLoDieS/albums/")


# Helper function to create folders and move files
def organize_files():
    """organize_files function."""

    # List all files in the base directory
    files = os.listdir(base_dir)

    # Process each file
    for file in files:
        # Skip directories
        if os.path.isdir(os.path.join(base_dir, file)):
            continue

        # Extract the base name (album name) from the file
        if file.endswith(".mp3"):
            album_name = file.replace(".mp3", "")
        elif file.endswith("_analysis.txt"):
            album_name = file.replace("_analysis.txt", "")
        elif file.endswith("_transcript.txt"):
            album_name = file.replace("_transcript.txt", "")
        else:
            continue  # Skip unrelated files

        # Create a folder for the album if it doesn't exist
        album_folder = os.path.join(base_dir, album_name)
        if not os.path.exists(album_folder):
            os.makedirs(album_folder)

        # Define file paths
        file_path = os.path.join(base_dir, file)
        mp3_path = os.path.join(album_folder, f"{album_name}.mp3")
        analysis_path = os.path.join(album_folder, f"{album_name}_analysis.txt")
        transcript_path = os.path.join(album_folder, f"{album_name}_transcript.txt")
        cover_image_path = os.path.join(album_folder, f"{album_name}.png")

        # Move the files to the corresponding folder
        if file.endswith(".mp3") and not os.path.exists(mp3_path):
            shutil.move(file_path, mp3_path)
            logger.info(f"Moved: {file} to {mp3_path}")
        elif file.endswith("_analysis.txt") and not os.path.exists(analysis_path):
            shutil.move(file_path, analysis_path)
            logger.info(f"Moved: {file} to {analysis_path}")
        elif file.endswith("_transcript.txt") and not os.path.exists(transcript_path):
            shutil.move(file_path, transcript_path)
            logger.info(f"Moved: {file} to {transcript_path}")

        # Check if a cover image exists and move it if found
        potential_image = os.path.join(base_dir, f"{album_name}.png")
        if os.path.exists(potential_image) and not os.path.exists(cover_image_path):
            shutil.move(potential_image, cover_image_path)
            logger.info(f"Moved: {potential_image} to {cover_image_path}")


if __name__ == "__main__":
    organize_files()
    logger.info("All files have been organized successfully.")
