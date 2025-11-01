"""
Webm To Mp

This module provides functionality for webm to mp.

Author: Auto-generated
Date: 2025-11-01
"""

from pathlib import Path
import os
import subprocess

import logging

logger = logging.getLogger(__name__)


def convert_webm_to_mp3(directory_path):
    """
    Converts all .webm files in the specified directory to .mp3 format.

    Args:
    directory_path (str): The path to the directory containing .webm files.
    """
    for filename in os.listdir(directory_path):
        if filename.endswith(".webm"):
            # Construct the full path to the source .webm file
            webm_path = os.path.join(directory_path, filename)
            # Construct the full path for the output .mp3 file
            mp3_path = os.path.join(
                directory_path, os.path.splitext(filename)[0] + ".mp3"
            )

            # Construct the ffmpeg command for converting .webm to .mp3
            command = [
                "ffmpeg",
                "-i",
                webm_path,
                "-vn",
                "-ab",
                "128k",
                "-ar",
                "44100",
                "-y",
                mp3_path,
            ]

            try:
                # Execute the ffmpeg command
                subprocess.run(command, check=True)
                logger.info(f"Converted {filename} to .mp3 successfully.")
            except subprocess.CalledProcessError as e:
                logger.info(f"Failed to convert {filename} to .mp3. Error: {e}")


if __name__ == "__main__":
    directory_path = Path(
        "/Users/steven/Movies/CoH-Grab"
    )  # Path to the directory containing .webm files
    convert_webm_to_mp3(directory_path)
