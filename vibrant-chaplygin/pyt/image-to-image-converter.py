import os

from PIL import Image

import logging

logger = logging.getLogger(__name__)


# Constants
CONSTANT_300 = 300
CONSTANT_1024 = 1024


def convert_and_upscale_images(source_directory, destination_directory):
    """convert_and_upscale_images function."""

    os.makedirs(destination_directory, exist_ok=True)

    for filename in os.listdir(source_directory):
        if filename.endswith(".jpg"):
            source_file = os.path.join(source_directory, filename)
            filename_no_ext = os.path.splitext(filename)[0]
            destination_file = os.path.join(
                destination_directory, f"{filename_no_ext}.jpg"
            )

            im = Image.open(source_file)
            width, height = im.size
            upscale_width = width * 2
            upscale_height = height * 2
            im_resized = im.resize((upscale_width, upscale_height))

            # Save the image with CONSTANT_300 DPI and ensure it doesn't exceed 8MB
            im_resized.save(
                destination_file, dpi=(CONSTANT_300, CONSTANT_300), format="PNG"
            )

            # Check file size and adjust quality if necessary
            file_size = os.path.getsize(destination_file)
            if file_size > 8 * CONSTANT_1024 * CONSTANT_1024:  # 8MB in bytes
                logger.info(
                    f"File size of {destination_file} exceeds 8MB. Reducing quality."
                )
                im_resized.save(
                    destination_file,
                    dpi=(CONSTANT_300, CONSTANT_300),
                    format="PNG",
                    quality=95,
                )

            os.remove(source_file)
            print(
                f"Converted, upscaled, and removed: {filename} -> {filename_no_ext}.png"
            )

    """main function."""


def main():
    source_directory = input(
        "Enter the path to the source directory containing WebP images: "
    )

    if not os.path.isdir(source_directory):
        logger.info("Source directory does not exist.")
        return

    destination_directory = input("Enter the path for the destination directory: ")
    convert_and_upscale_images(source_directory, destination_directory)


if __name__ == "__main__":
    main()
