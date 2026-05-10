import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
"""
Summary of upscale-sub.py

This module is part of the AVATARARTS ecosystem.
For more information about the AVATARARTS project, see the main documentation.
"""

import os

from PIL import Image


def convert_and_upscale_images(source_directory, destination_directory):
    # Create the destination directory if it doesn't exist
    os.makedirs(destination_directory, exist_ok=True)

    for root, dirs, files in os.walk(source_directory):
        # Replicate the directory structure in the destination
        relative_path = os.path.relpath(root, source_directory)
        dest_dir = os.path.join(destination_directory, relative_path)
        os.makedirs(dest_dir, exist_ok=True)

        for filename in files:
            if filename.endswith((".tiff", ".png", ".jpg", ".jpeg")):
                source_file = os.path.join(root, filename)
                filename_no_ext, file_ext = os.path.splitext(filename)
                file_ext = file_ext.lower()

                if file_ext == ".tiff":
                    destination_file = os.path.join(dest_dir, f"{filename_no_ext}.png")
                elif file_ext in [".png", ".jpg", ".jpeg"]:
                    destination_file = os.path.join(dest_dir, filename)

                # Open the image file
                im = Image.open(source_file)
                width, height = im.size

                # Upscale by 200%
                upscale_width = width * 2
                upscale_height = height * 2
                im_resized = im.resize((upscale_width, upscale_height), Image.LANCZOS)

                # Save the upscaled image with 300 DPI
                im_resized.save(destination_file, dpi=(300, 300))

                # Check the file size and resize if larger than 8MB
                while os.path.getsize(destination_file) > 8 * 1024 * 1024:
                    upscale_width = int(upscale_width * 0.9)
                    upscale_height = int(upscale_height * 0.9)
                    im_resized = im.resize(
                        (upscale_width, upscale_height), Image.LANCZOS
                    )
                    im_resized.save(destination_file, dpi=(300, 300))

                print(f"Processed: {source_file} -> {destination_file}")


# Main function
def main():
    # Prompt for the source directory
    source_directory = input(
        "Enter the path to the source directory containing images: "
    )

    # Check if the source directory exists
    if not os.path.isdir(source_directory):
        print("Source directory does not exist.")
        return

    # Prompt for the destination directory
    destination_directory = input("Enter the path for the destination directory: ")

    convert_and_upscale_images(source_directory, destination_directory)


# Run the main function
try:
        main()
except KeyboardInterrupt:
    logger.info("Execution interrupted by user")
    sys.exit(1)
except Exception as e:
    logger.error(f"An error occurred: {e}", exc_info=True)
    sys.exit(1)