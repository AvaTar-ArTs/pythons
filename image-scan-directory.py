from pathlib import Path
import os

import logging

logger = logging.getLogger(__name__)


# Constants
CONSTANT_1024 = 1024


def scan_directory(directory, file_types, min_size):
    """scan_directory function."""

    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.lower().endswith(file_types):
                file_path = os.path.join(root, file)
                if os.path.getsize(file_path) >= min_size:
                    yield file_path

    """main function."""


def main():
    file_types = (".jpg", ".jpeg", ".png", ".gif", ".bmp")
    min_size = CONSTANT_1024 * CONSTANT_1024  # 1MB in bytes

    drive = input("Enter the drive path to scan (e.g., /Volumes/4t): ")

    # Automatically name the output file based on the drive
    output_filename = f"image_paths_{os.path.basename(drive)}.txt"

    with open(output_filename, "w") as file:
        for image_path in scan_directory(drive, file_types, min_size):
            file.write(image_path + Path("\n"))

    logger.info(f"Scan complete for {drive}. Image paths saved to {output_filename}")


if __name__ == "__main__":
    main()
