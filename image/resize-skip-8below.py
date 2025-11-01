"""
Resize Skip 8Below Og

This module provides functionality for resize skip 8below og.

Author: Auto-generated
Date: 2025-11-01
"""

import os
import time
from datetime import datetime

from PIL import Image, UnidentifiedImageError

import logging

logger = logging.getLogger(__name__)


# Constants
CONSTANT_300 = 300
CONSTANT_720 = 720
CONSTANT_1024 = 1024
CONSTANT_1080 = 1080
CONSTANT_1280 = 1280
CONSTANT_1920 = 1920
CONSTANT_4500 = 4500
CONSTANT_5400 = 5400


# Constants
MAX_WIDTH, MAX_HEIGHT = CONSTANT_4500, CONSTANT_5400
TARGET_DPI = CONSTANT_300
BATCH_SIZE = 50
PAUSE_DURATION = 5
MIN_FILE_SIZE_BYTES = 8 * CONSTANT_1024 * CONSTANT_1024  # 8MB in bytes

# Aspect Ratio Minimums
ASPECT_RATIO_MINIMUMS = {
    "16:9": (CONSTANT_720, CONSTANT_1280),  # Landscape
    "9:16": (CONSTANT_1080, CONSTANT_1920),  # Portrait
    "1:1": (CONSTANT_1024, CONSTANT_1024),  # Square
}


# Function to get the closest aspect ratio
def get_closest_aspect_ratio(width, height):
    """get_closest_aspect_ratio function."""

    aspect_ratios = {
        "16:9": 16 / 9,
        "9:16": 9 / 16,
        "1:1": 1 / 1,
    }
    current_ratio = width / height
    closest_ratio = min(aspect_ratios, key=lambda ar: abs(current_ratio - aspect_ratios[ar]))
    return closest_ratio, ASPECT_RATIO_MINIMUMS[closest_ratio]

    # Function to resize images
    """resize_image function."""


def resize_image(im, output_path):
    width, height = im.size
    closest_ratio, (min_width, min_height) = get_closest_aspect_ratio(width, height)
    aspect_ratio = width / height

    # Determine new dimensions
    if width < min_width or height < min_height:
        if closest_ratio == "16:9":
            new_width, new_height = min_width, int(min_width / aspect_ratio)
        elif closest_ratio == "9:16":
            new_height, new_width = min_height, int(min_height * aspect_ratio)
        elif closest_ratio == "1:1":
            new_width, new_height = max(min_width, min_height), max(min_width, min_height)
    elif width > MAX_WIDTH or height > MAX_HEIGHT:
        if width / MAX_WIDTH > height / MAX_HEIGHT:
            new_width, new_height = MAX_WIDTH, int(MAX_WIDTH / aspect_ratio)
        else:
            new_height, new_width = MAX_HEIGHT, int(MAX_HEIGHT * aspect_ratio)
    else:
        new_width, new_height = width, height

    logger.info(f"🔄 Resizing to: {new_width}x{new_height}")
    im = im.resize((new_width, new_height), Image.LANCZOS)
    im.save(output_path, dpi=(TARGET_DPI, TARGET_DPI), quality=85)
    return im

    """process_batch function."""


# Function to process a batch of images
def process_batch(batch, root):
    for file in batch:
        file_path = os.path.join(root, file)
        file_ext = file.lower().split(".")[-1]

        # Skip unsupported file formats
        if file_ext not in ("jpg", "jpeg", "png"):
            logger.info(f"⚠️ Skipping {file}: Unsupported file format.")
            continue

        # Skip files smaller than 8MB
        file_size = os.path.getsize(file_path)
        if file_size < MIN_FILE_SIZE_BYTES:
            print(f"⚠️ Skipping {file}: File size is below 8MB ({file_size / (CONSTANT_1024 ** 2):.2f} MB)")
            continue

        try:
            im = Image.open(file_path)
            width, height = im.size
            print(f"\n🖼️ Processing {file}: Original size: {width}x{height}, {file_size / (CONSTANT_1024 ** 2):.2f} MB")

            # Temporary file for resizing
            temp_file = os.path.join(root, f"resized_{file}")
            resize_image(im, temp_file)

            # Replace the original file with the resized one
            os.remove(file_path)
            os.rename(temp_file, file_path)
            logger.info(f"✅ Successfully resized {file} and replaced the original file")

        except UnidentifiedImageError:
            logger.info(f"⚠️ Skipping {file}: Cannot identify image.")
        except Exception as e:
            logger.info(f"⚠️ Error processing {file}: {e}")

    """process_images function."""


# Function to process images
def process_images(source_directory):
    batch = []

    for root, _, files in os.walk(source_directory):
        for file in files:
            batch.append(file)
            if len(batch) >= BATCH_SIZE:
                logger.info(f"🔄 Processing batch of {BATCH_SIZE} images in {root}...")
                process_batch(batch, root)
                batch = []
                logger.info(f"⏸️ Pausing for {PAUSE_DURATION} seconds...")
                time.sleep(PAUSE_DURATION)

        if batch:
            logger.info(f"🔄 Processing remaining {len(batch)} images in {root}...")
            process_batch(batch, root)
            batch = []
    """main function."""


# Main function
def main():
    source_directory = input("Enter the path to the source directory containing images: ").strip()
    if not os.path.isdir(source_directory):
        logger.info("Source directory does not exist.")
        return

    process_images(source_directory)
    logger.info("🎉 All images processed successfully!")


if __name__ == "__main__":
    main()
