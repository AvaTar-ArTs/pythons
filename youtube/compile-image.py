"""
Youtube Compile Image Info

This module provides functionality for youtube compile image info.

Author: Auto-generated
Date: 2025-11-01
"""

from pathlib import Path
import csv
import os


def compile_image_info(root_directory, master_csv_file_path):
    """compile_image_info function."""

    with open(
        master_csv_file_path, mode="w", newline="", encoding="utf-8"
    ) as master_file:
        master_writer = csv.writer(master_file)
        master_writer.writerow(
            [
                "Subfolder",
                "Product Name",
                "Product Link",
                "Est. Monthly Revenue",
                "Reviews",
                "Listing Age",
                "Favorites",
                "Est. Total Sales",
                "Price",
                "Tags",
            ]
        )

        for subdir in os.listdir(root_directory):
            subdir_path = os.path.join(root_directory, subdir)
            if os.path.isdir(subdir_path):
                csv_path = os.path.join(subdir_path, "image_info.csv")
                if os.path.exists(csv_path):
                    with open(csv_path, mode="r", encoding="utf-8") as sub_file:
                        csv_reader = csv.reader(sub_file)
                        next(csv_reader, None)  # Skip header row
                        for row in csv_reader:
                            master_writer.writerow([subdir] + row)


compile_image_info(
    Path(str(Path.home()) + "/csv2"), Path(str(Path.home()) + "/master_image_info.csv")
)
