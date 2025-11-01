"""
Convert 39

This module provides functionality for convert 39.

Author: Auto-generated
Date: 2025-11-01
"""

import os

from PIL import Image

import logging

logger = logging.getLogger(__name__)


# Constants
CONSTANT_100 = 100
CONSTANT_300 = 300
CONSTANT_1024 = 1024


def convert_and_downscale_images_in_subfolders(source_directory):
    """convert_and_downscale_images_in_subfolders function."""

    for root, dirs, files in os.walk(source_directory):
        for filename in files:
            if filename.endswith(".png"):
                source_file = os.path.join(root, filename)
                filename_no_ext = os.path.splitext(filename)[0]
                temp_file = os.path.join(root, f"{filename_no_ext}_temp.png")

                # Open the image and retrieve the original dimensions
                im = Image.open(source_file)
                width, height = im.size
                logger.info(f"🖼️ Processing {filename}: Original size: {width}x{height}")

                # Downscale the image by 50%
                downscale_width = width // 2
                downscale_height = height // 2
                im_resized = im.resize((downscale_width, downscale_height))

                # Show progress of resizing
                logger.info(f"🔄 Downscaling {filename} to: {downscale_width}x{downscale_height}")

                # Save the image with CONSTANT_300 DPI
                im_resized.save(temp_file, dpi=(CONSTANT_300, CONSTANT_300), format="PNG")

                # Check file size and reduce quality if larger than 8MB
                file_size = os.path.getsize(temp_file)
                if file_size > 8 * CONSTANT_1024 * CONSTANT_1024:  # 8MB in bytes
                    logger.info(f"⚠️ File size of {temp_file} exceeds 8MB. Reducing quality.")
                    im_resized.save(temp_file, dpi=(CONSTANT_300, CONSTANT_300), format="PNG", quality=CONSTANT_100)

                # Remove the original image and rename the temp file to the original filename
                os.remove(source_file)
                os.rename(temp_file, source_file)

                # Show completion with an emoji
                logger.info(f"✅ Successfully converted and downscaled: {filename}")

    """main function."""


def main():
    source_directory = input("Enter the path to the source directory containing images: ")

    if not os.path.isdir(source_directory):
        logger.info("Source directory does not exist.")
        return

    convert_and_downscale_images_in_subfolders(source_directory)


if __name__ == "__main__":
    main()
