"""
Converts

This module provides functionality for converts.

Author: Auto-generated
Date: 2025-11-01
"""

import os
from PIL import Image

import logging

logger = logging.getLogger(__name__)


# Constants
CONSTANT_300 = 300
CONSTANT_1024 = 1024



def convert_and_upscale_images(source_directory, destination_directory):
    """convert_and_upscale_images function."""

    # Create the destination directory if it doesn't exist
    os.makedirs(destination_directory, exist_ok=True)

    for filename in os.listdir(source_directory):
        if filename.endswith((".tiff", ".png", ".jpg", ".jpeg")):
            source_file = os.path.join(source_directory, filename)
            filename_no_ext, file_ext = os.path.splitext(filename)
            file_ext = file_ext.lower()

            if file_ext == ".tiff":
                destination_file = os.path.join(
                    destination_directory, f"{filename_no_ext}.png"
                )
            elif file_ext in [".png", ".jpg", ".jpeg"]:
                destination_file = os.path.join(
                    destination_directory, filename)

            # Open the image file
            im = Image.open(source_file)
            width, height = im.size

            # Upscale by 200%
            upscale_width = width * 2
            upscale_height = height * 2
            im_resized = im.resize(
                (upscale_width, upscale_height), Image.LANCZOS)

            # Save the upscaled image with CONSTANT_300 DPI
            im_resized.save(destination_file, dpi=(CONSTANT_300, CONSTANT_300))

            # Check the file size and resize if larger than 8MB
            while os.path.getsize(destination_file) > 8 * CONSTANT_1024 * CONSTANT_1024:
                upscale_width = int(upscale_width * 0.9)
                upscale_height = int(upscale_height * 0.9)
                im_resized = im.resize(
                    (upscale_width, upscale_height), Image.LANCZOS)
                im_resized.save(destination_file, dpi=(CONSTANT_300, CONSTANT_300))

            print(
                f"Processed: {filename} -> {os.path.basename(destination_file)}")


# Main function
    """main function."""

def main():
    # Prompt for the source directory
    source_directory = input(
        "Enter the path to the source directory containing images: "
    )

    # Check if the source directory exists
    if not os.path.isdir(source_directory):
        logger.info("Source directory does not exist.")
        return

    # Prompt for the destination directory
    destination_directory = input(
        "Enter the path for the destination directory: ")

    convert_and_upscale_images(source_directory, destination_directory)


# Run the main function
if __name__ == "__main__":
    main()
