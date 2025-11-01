"""
Content Creation Nocturne Pics2Pdfs 100Album 1

This module provides functionality for content creation nocturne pics2pdfs 100album 1.

Author: Auto-generated
Date: 2025-11-01
"""

from pathlib import Path
import os

from PIL import Image, UnidentifiedImageError

import logging

logger = logging.getLogger(__name__)


# Constants
CONSTANT_100 = 100


# Increase the maximum number of pixels allowed to prevent DecompressionBombWarning.
# Note: Be cautious with this setting to avoid processing extremely large images that could exhaust system memory.
Image.MAX_IMAGE_PIXELS = (
    None  # This disables the limit. Alternatively, set it to a specific limit you're comfortable with.
)


def collect_image_files(source_directory):
    """Collects all PNG, JPG, JPEG files from the source directory and its subdirectories."""
    image_files = []
    for root, dirs, files in os.walk(source_directory):
        for file in files:
            if file.lower().endswith((".png", ".jpg", ".jpeg")):
                file_path = os.path.join(root, file)
                image_files.append(file_path)
    return image_files


def create_pdf_volumes(image_files, target_directory, volume_size=CONSTANT_100):
    """Creates PDF volumes from image files, each containing up to CONSTANT_100 images."""
    volume_number = 1
    for i in range(0, len(image_files), volume_size):
        volume_image_files = image_files[i : i + volume_size]
        images = []
        for img in volume_image_files:
            try:
                with Image.open(img) as im:
                    images.append(im.convert("RGB"))
            except UnidentifiedImageError:
                logger.info(f"Skipping file (unidentified image): {img}")
            except Exception as e:
                logger.info(f"Error processing file {img}: {e}")

        if images:  # Proceed only if there are valid images collected
            volume_path = os.path.join(target_directory, f"Image_Volume_{volume_number}.pdf")
            images[0].save(volume_path, save_all=True, append_images=images[1:])
            volume_number += 1


def main():
    """main function."""

    source_directory = Path("/Volumes/iMac")
    target_directory = Path("/Volumes/iMac/iPDF")

    if not os.path.exists(target_directory):
        os.makedirs(target_directory)

    image_files = collect_image_files(source_directory)
    create_pdf_volumes(image_files, target_directory)

    logger.info("Conversion completed. Check the target directory for the PDF volumes.")


if __name__ == "__main__":
    main()
