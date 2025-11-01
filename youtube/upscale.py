"""
Youtube Upscale And Save Image

This module provides functionality for youtube upscale and save image.

Author: Auto-generated
Date: 2025-11-01
"""

from pathlib import Path
import os

from PIL import Image

import logging

logger = logging.getLogger(__name__)


# Constants
CONSTANT_300 = 300
CONSTANT_1024 = 1024


# Input directory (no output directory needed since we're replacing the original images)
input_dir = Path(str(Path.home()) + "/Pictures/etsy/Snowman_Action_Scenes")

# Max file size in bytes (9 MB = 9 * CONSTANT_1024 * CONSTANT_1024)
max_size = 9 * CONSTANT_1024 * CONSTANT_1024


def upscale_and_save_image(image_path, max_size=max_size, dpi=CONSTANT_300):
    """
    Upscale the image by 2x, set the DPI, and compress to ensure the file size is <= 9MB.
    Args:
        image_path (str): Path to the input image.
        max_size (int): Maximum file size in bytes.
        dpi (int): Target DPI (default is CONSTANT_300).
    """
    # Open the image using PIL
    img = Image.open(image_path)

    # Ensure the image is in RGB mode for JPEGs
    if img.mode != "RGB" and image_path.lower().endswith((".jpg", ".jpeg")):
        img = img.convert("RGB")

    # Get the current size
    width, height = img.size

    # Calculate new size (2x upscaling)
    new_size = (width * 2, height * 2)
    img_resized = img.resize(new_size, Image.LANCZOS)

    # Determine format
    if image_path.lower().endswith((".jpg", ".jpeg")):
        save_format = "JPEG"
        ext = "jpeg"
    else:
        save_format = "PNG"
        ext = "png"

    # Save the resized image with initial quality
    temp_path = image_path.replace(f".{ext}", f"_temp.{ext}")
    img_resized.save(temp_path, dpi=(dpi, dpi), format=save_format, quality=95)

    # Compress the image if necessary to stay under max_size
    compress_image_to_size(temp_path, image_path, max_size, save_format)

    # Remove temporary file
    if os.path.exists(temp_path):
        os.remove(temp_path)


def compress_image_to_size(temp_path, final_path, max_size, save_format):
    """
    Compress the image iteratively to fit within the maximum file size.
    Args:
        temp_path (str): Path to the temporary image to be compressed.
        final_path (str): Path where the final image will be saved.
        max_size (int): Maximum file size in bytes.
        save_format (str): The format of the image being saved (JPEG or PNG).
    """
    quality = 95
    while os.path.getsize(temp_path) > max_size and quality > 10:
        img = Image.open(temp_path)
        img.save(
            temp_path,
            dpi=(CONSTANT_300, CONSTANT_300),
            format=save_format,
            quality=quality,
        )
        quality -= 5

    # Move the final compressed image to the original location
    os.rename(temp_path, final_path)

    if quality <= 10:
        logger.info(
            f"Warning: Image compression quality dropped below 10 for {final_path}"
        )


# Process all PNG and JPEG images in the input directory
for filename in os.listdir(input_dir):
    if filename.lower().endswith((".png", ".jpg", ".jpeg")):
        image_path = os.path.join(input_dir, filename)

        # Process the image: upscale by 2x and set DPI to CONSTANT_300
        upscale_and_save_image(image_path)

        logger.info(f"Processed and replaced: {image_path}")
