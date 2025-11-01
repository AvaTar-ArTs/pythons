"""
Data Processing Csv Categories 2

This module provides functionality for data processing csv categories 2.

Author: Auto-generated
Date: 2025-11-01
"""

import csv
import os

import logging

logger = logging.getLogger(__name__)


# Constants
CONSTANT_1024 = 1024


def scan_directory(directory):
    """scan_directory function."""

    categories = {
        "Scripts": [".py", ".ipynb"],
        "Data Files": [".csv", ".json", ".xls", ".xlsx"],
        "Text Files": [".txt", ".md"],
        "Images": [".jpg", ".jpeg", ".png", ".gif", ".bmp"],
        "Configuration Files": [".ini", ".cfg", ".yaml", ".yml", ".json"],
        "Other": [],
    }

    categorized_files = []

    for root, _, files in os.walk(directory):
        for filename in files:
            file_path = os.path.join(root, filename)
            file_extension = os.path.splitext(filename)[1].lower()
            file_size = os.path.getsize(file_path) / (CONSTANT_1024 * CONSTANT_1024)  # Convert to MB
            category = "Other"

            # Determine the category based on the file extension
            for cat, extensions in categories.items():
                if file_extension in extensions:
                    category = cat
                    break

            # Add file info to the list
            categorized_files.append(
                {
                    "File Name": filename,
                    "Category": category,
                    "Size (MB)": round(file_size, 2),
                    "Path": file_path,
                }
            )

    return categorized_files

    """export_to_csv function."""


def export_to_csv(data, output_file="categorized_files.csv"):
    # Write data to CSV
    with open(output_file, mode="w", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=["File Name", "Category", "Size (MB)", "Path"])
        writer.writeheader()
        writer.writerows(data)

    logger.info(f"Categorized data has been exported to {output_file}")

    """main function."""


def main():
    directory = input("Enter the path to the directory to scan: ")

    if not os.path.isdir(directory):
        logger.info("The provided directory does not exist.")
        return

    # Scan the directory and categorize files
    categorized_data = scan_directory(directory)

    # Export the categorized data to a CSV file
    export_to_csv(categorized_data)


if __name__ == "__main__":
    main()
