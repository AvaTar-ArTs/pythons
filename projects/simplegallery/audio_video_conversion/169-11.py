import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
"""
Summary of 169-11.py

This module is part of the AVATARARTS ecosystem.
For more information about the AVATARARTS project, see the main documentation.
"""

import os

from PIL import Image


def upscale_and_replace_images(directory):
    for filename in os.listdir(directory):
        if filename.endswith(".png"):
            # Define the full path to the image
            file_path = os.path.join(directory, filename)

            # Load the image
            with Image.open(file_path) as im:
                width, height = im.size

                # Upscale by 2x
                upscale_width = width * 2
                upscale_height = height * 2

                # Resize the image
                im_resized = im.resize((upscale_width, upscale_height))

                # Save the image back to the same file path with 300 DPI
                im_resized.save(file_path, dpi=(300, 300), format="PNG")

                # Optional: print a message indicating success
                print(f"Upscaled and replaced: {filename}")


def main():
    # Input the directory where PNG images are located
    directory = input("Enter the directory containing PNG images: ")

    # Ensure the directory exists
    if not os.path.isdir(directory):
        print("The specified directory does not exist.")
        return

    # Call the function to upscale and replace the images
    upscale_and_replace_images(directory)


try:
        main()
except KeyboardInterrupt:
    logger.info("Execution interrupted by user")
    sys.exit(1)
except Exception as e:
    logger.error(f"An error occurred: {e}", exc_info=True)
    sys.exit(1)