"""
Utilities File Operations Archives 2

This module provides functionality for utilities file operations archives 2.

Author: Auto-generated
Date: 2025-11-01
"""

from pathlib import Path
import os
import tarfile

import logging

logger = logging.getLogger(__name__)


# List of directories to include in the tar.gz archive
directories = [
    "/Users/steven/Pictures/other-07-25-05:32.csv",
    "/Users/steven/Pictures/audio-07-25-05:31.csv",
    "/Users/steven/Pictures/docs-07-25-05:31.csv",
    "/Users/steven/Pictures/image_data-07-25-05:32.csv",
    "/Users/steven/Pictures/vids-07-25-05:34.csv",
]

# Output tar.gz file
output_filename = Path("/Users/steven/Pictures/data_archive.tar.gz")


# Function to create tar.gz archive
def create_tar_gz(output_filename, directories):
    """create_tar_gz function."""

    with tarfile.open(output_filename, "w:gz") as tar:
        for dir_path in directories:
            for root, _, files in os.walk(os.path.dirname(dir_path)):
                for file in files:
                    fullpath = os.path.join(root, file)
                    tar.add(
                        fullpath,
                        arcname=os.path.relpath(fullpath, os.path.dirname(directories[0])),
                    )
    logger.info(f"Archive {output_filename} created successfully.")


# Create the tar.gz archive
create_tar_gz(output_filename, directories)
