"""
Utilities File Operations Scan 9

This module provides functionality for utilities file operations scan 9.

Author: Auto-generated
Date: 2025-11-01
"""

from pathlib import Path
import os

import logging

logger = logging.getLogger(__name__)


# List of drives to scan
drives = [
    Path("/Users/steven/CoH-Story"),
    Path("/Users/steven/CoMic"),
    Path("/Users/steven/Downloads"),
    Path("/Users/steven/Documents"),
    Path("/Users/steven/"),
    Path("/Users/steven/Music"),
    Path("/Users/steven/Pictures"),
]
# File types to look for
file_types = (".jpg", ".jpeg", ".png", ".gif", "webp")


# Function to scan a directory for image files
def scan_directory(directory):
    """scan_directory function."""

    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.lower().endswith(file_types):
                yield os.path.join(root, file)


# Open a file to write the paths
with open("image_paths.csv", "w") as file:
    for drive in drives:
        for image_path in scan_directory(drive):
            file.write(image_path + Path("\n"))

logger.info("Scan complete. Image paths saved to image_paths.csv")
