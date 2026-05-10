import os
from PIL import Image

import logging

logger = logging.getLogger(__name__)


# Constants
CONSTANT_300 = 300


# Function to convert WebP images to PNG and upscale by 200% with CONSTANT_300 DPI


def convert_and_upscale_images(source_directory, destination_directory):
    """convert_and_upscale_images function."""

    # Create the destination directory if it doesn't exist
    os.makedirs(destination_directory, exist_ok=True)

    for filename in os.listdir(source_directory):
        if filename.endswith(".tiff"):
            source_file = os.path.join(source_directory, filename)
            filename_no_ext = os.path.splitext(filename)[0]
            destination_file = os.path.join(
                destination_directory, f"{filename_no_ext}.png"
            )

            # Convert WebP to PNG and upscale by 200% with CONSTANT_300 DPI
            im = Image.open(source_file)
            width, height = im.size
            upscale_width = width * 2
            upscale_height = height * 2
            im_resized = im.resize((upscale_width, upscale_height))
            im_resized.save(destination_file, dpi=(CONSTANT_300, CONSTANT_300))

            # Remove the original WebP file
            os.remove(source_file)

            print(
                f"Converted, upscaled, and removed: {filename} -> {filename_no_ext}.png"
            )

    # Main function

    """main function."""


def main():
    # Prompt for the source directory containing WebP images
    source_directory = input(
        "Enter the path to the source directory containing WebP images: "
    )

    # Check if the source directory exists
    if not os.path.isdir(source_directory):
        logger.info("Source directory does not exist.")
        return

    # Prompt for the destination directory
    destination_directory = input("Enter the path for the destination directory: ")

    convert_and_upscale_images(source_directory, destination_directory)


# Run the main function
if __name__ == "__main__":
    main()
