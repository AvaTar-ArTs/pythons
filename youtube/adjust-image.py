"""
Youtube Adjust Image Size

This module provides functionality for youtube adjust image size.

Author: Auto-generated
Date: 2025-11-01
"""

import os

from PIL import Image, UnidentifiedImageError

import logging

logger = logging.getLogger(__name__)


# Constants
CONSTANT_300 = 300
CONSTANT_1024 = 1024
CONSTANT_4500 = 4500
CONSTANT_5400 = 5400


def adjust_image_size(im, target_file_size, temp_file, target_dpi, upscale=False):
    """adjust_image_size function."""

    file_size = os.path.getsize(temp_file)

    # Size limits: 4500x5400 max, 1024x1024 min
    max_width, max_height = CONSTANT_4500, CONSTANT_5400
    min_width, min_height = CONSTANT_1024, CONSTANT_1024

    while (file_size > target_file_size) or (upscale and file_size < target_file_size):
        # Downscale if image is too large
        if (
            file_size > target_file_size
            or im.size[0] > max_width
            or im.size[1] > max_height
        ):
            scale_factor = 0.9  # Downscale by 10%
        # Upscale if image is too small
        elif im.size[0] < min_width or im.size[1] < min_height:
            scale_factor = 1.1  # Upscale by 10%
        else:
            # If within allowed dimensions but file size still not within target, resize
            scale_factor = 0.9 if file_size > target_file_size else 1.1

        new_width = min(max(int(im.size[0] * scale_factor), min_width), max_width)
        new_height = min(max(int(im.size[1] * scale_factor), min_height), max_height)

        im = im.resize((new_width, new_height), Image.ANTIALIAS)
        logger.info(f"🔄 Resizing to: {new_width}x{new_height}")

        # Save the resized image
        im.save(temp_file, dpi=(target_dpi, target_dpi), format="JPEG", quality=85)
        file_size = os.path.getsize(temp_file)
        logger.info(
            f"File size after resizing: {file_size / (CONSTANT_1024 * CONSTANT_1024):.2f} MB"
        )

    return im

    """convert_and_downscale_images_in_subfolders function."""


def convert_and_downscale_images_in_subfolders(
    source_directory,
    target_file_size=8 * CONSTANT_1024 * CONSTANT_1024,
    target_dpi=CONSTANT_300,
):
    total_original_size = 0
    total_resized_size = 0

    for root, dirs, files in os.walk(source_directory):
        for filename in files:
            if filename.endswith(".png"):
                source_file = os.path.join(root, filename)
                filename_no_ext = os.path.splitext(filename)[0]
                temp_file = os.path.join(
                    root, f"{filename_no_ext}_temp.jpg"
                )  # Use JPEG for better size control

                try:
                    # Try to open the image
                    im = Image.open(source_file)
                    width, height = im.size
                    original_size = os.path.getsize(source_file)
                    total_original_size += original_size
                    print(
                        f"🖼️ Processing {filename}: Original size: {width}x{height}, {original_size / (CONSTANT_1024 * CONSTANT_1024):.2f} MB"
                    )

                    # If the image has an alpha channel, convert it to RGB
                    if im.mode == "RGBA":
                        im = im.convert("RGB")
                        logger.info(f"Converted {filename} from RGBA to RGB")

                    # Save initial image to check file size
                    im.save(
                        temp_file,
                        dpi=(target_dpi, target_dpi),
                        format="JPEG",
                        quality=85,
                    )
                    resized_size = os.path.getsize(temp_file)
                    logger.info(
                        f"Initial file size: {resized_size / (CONSTANT_1024 * CONSTANT_1024):.2f} MB"
                    )

                    # Check if the image needs to be upscaled or downscaled
                    upscale = width < CONSTANT_1024 or height < CONSTANT_1024
                    im_resized = adjust_image_size(
                        im, target_file_size, temp_file, target_dpi, upscale
                    )

                    resized_size = os.path.getsize(
                        temp_file
                    )  # Get final resized file size
                    total_resized_size += resized_size

                    # Check if the file exists before renaming
                    if os.path.exists(temp_file):
                        os.remove(source_file)  # Remove original PNG
                        os.rename(
                            temp_file, os.path.join(root, f"{filename_no_ext}.jpg")
                        )  # Save as JPEG
                        print(
                            f"✅ Successfully resized {filename} to under {target_file_size / (CONSTANT_1024 * CONSTANT_1024)} MB"
                        )
                    else:
                        logger.info(
                            f"❌ Temporary file {temp_file} not found. Image resizing failed."
                        )

                except UnidentifiedImageError:
                    logger.info(f"❌ Skipping {filename}: Cannot identify image file.")
                except Exception as e:
                    logger.info(f"Error processing {filename}: {e}")

    # Calculate and print the total space saved
    total_original_gb = total_original_size / (CONSTANT_1024**3)
    total_resized_gb = total_resized_size / (CONSTANT_1024**3)
    space_saved_gb = total_original_gb - total_resized_gb
    logger.info(f"\n📊 Total space saved: {space_saved_gb:.2f} GB")
    logger.info(
        f"Original size: {total_original_gb:.2f} GB, Resized size: {total_resized_gb:.2f} GB"
    )

    """main function."""


def main():
    source_directory = input(
        "Enter the path to the source directory containing images: "
    )

    if not os.path.isdir(source_directory):
        logger.info("Source directory does not exist.")
        return

    convert_and_downscale_images_in_subfolders(source_directory)


if __name__ == "__main__":
    main()
