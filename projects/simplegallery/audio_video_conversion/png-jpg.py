import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
"""
Summary of png-jpg.py

This module is part of the AVATARARTS ecosystem.
For more information about the AVATARARTS project, see the main documentation.
"""

import os

from PIL import Image


def convert_images_to_jpeg(source_directory):
    for root, dirs, files in os.walk(source_directory):
        for filename in files:
            if filename.endswith(".png"):
                source_file = os.path.join(root, filename)
                filename_no_ext = os.path.splitext(filename)[0]
                jpeg_file = os.path.join(root, f"{filename_no_ext}.jpg")

                # Open the PNG image
                im = Image.open(source_file)

                # Convert the image to RGB mode (JPEG doesn't support transparency)
                im = im.convert("RGB")

                # Save the image as JPEG
                im.save(
                    jpeg_file,
                    format="JPEG",
                    quality=85,
                )  # Adjust quality as needed

                # Show completion with an emoji
                print(f"✅ Successfully converted {filename} to JPEG: {jpeg_file}")

                # Remove the original PNG file
                os.remove(source_file)


def main():
    source_directory = input(
        "Enter the path to the source directory containing images: ",
    )

    if not os.path.isdir(source_directory):
        print("Source directory does not exist.")
        return

    convert_images_to_jpeg(source_directory)


try:
        main()
except KeyboardInterrupt:
    logger.info("Execution interrupted by user")
    sys.exit(1)
except Exception as e:
    logger.error(f"An error occurred: {e}", exc_info=True)
    sys.exit(1)