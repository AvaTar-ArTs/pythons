"""
Get File

This module provides functionality for get file.

Author: Auto-generated
Date: 2025-11-01
"""

import os
import time
from datetime import datetime

from PIL import Image, UnidentifiedImageError
from tqdm import tqdm

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
MAX_FILE_SIZE_BYTES = 8 * CONSTANT_1024 * CONSTANT_1024  # 8MB in bytes

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


# Function to apply CONSTANT_300 DPI to an image
    """apply_dpi function."""

def apply_dpi(im, output_path):
    im.save(output_path, dpi=(CONSTANT_300, CONSTANT_300), quality=85)
    logger.info(f"✅ Applied CONSTANT_300 DPI to: {output_path}")


    """resize_image function."""

# Function to resize images
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

    """process_batch function."""


# Function to process a batch of images
def process_batch(batch, root):
    for file in tqdm(batch, desc="🔄 Processing batch"):
        file_path = os.path.join(root, file)
        file_ext = file.lower().split(".")[-1]

        # Skip unsupported file formats
        if file_ext not in ("jpg", "jpeg", "png"):
            logger.info(f"⚠️ Skipping {file}: Unsupported file format.")
            continue

        try:
            im = Image.open(file_path)
            width, height = im.size
            logger.info(f"\n🖼️ Processing {file}: Original size: {width}x{height}")

            # Apply DPI
            temp_file_dpi = os.path.join(root, f"300dpi_{file}")
            apply_dpi(im, temp_file_dpi)

            # Resize the image
            temp_file_resize = os.path.join(root, f"resized_{file}")
            resize_image(Image.open(temp_file_dpi), temp_file_resize)

            # Replace the original file with the resized image
            os.rename(temp_file_resize, file_path)
            os.remove(temp_file_dpi)  # Clean up intermediate DPI-adjusted file

            logger.info(f"✅ Successfully resized {file} with CONSTANT_300 DPI")

        except UnidentifiedImageError:
            logger.info(f"⚠️ Skipping {file}: Cannot identify image.")
        except Exception as e:
            logger.info(f"⚠️ Error processing {file}: {e}")
    """process_images function."""



# Process images
def process_images(source_directory):
    batch = []
    for root, _, files in os.walk(source_directory):
        for file in files:
            batch.append(file)
            if len(batch) >= BATCH_SIZE:
                process_batch(batch, root)
                batch = []
                logger.info(f"⏸️ Pausing for {PAUSE_DURATION} seconds...")
                time.sleep(PAUSE_DURATION)

        if batch:
            process_batch(batch, root)
    """main function."""

            batch = []


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
