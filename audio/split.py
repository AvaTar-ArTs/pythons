"""
Split 2

This module provides functionality for split 2.

Author: Auto-generated
Date: 2025-11-01
"""

import os

import logging

logger = logging.getLogger(__name__)


# Constants
CONSTANT_1000 = 1000



def split_html_file(file_path, lines_per_chunk=CONSTANT_1000):
    """split_html_file function."""

    # Ensure the file exists
    if not os.path.isfile(file_path):
        logger.info(f"File '{file_path}' not found.")
        return

    # Create output directory
    output_dir = os.path.join(os.path.dirname(file_path), "chunks")
    os.makedirs(output_dir, exist_ok=True)

    # Initialize variables
    with open(file_path, "r", encoding="utf-8") as file:
        lines = file.readlines()
        total_lines = len(lines)
        chunk_count = 0

        # Iterate over lines in chunks
        for i in range(0, total_lines, lines_per_chunk):
            chunk = lines[i : i + lines_per_chunk]
            chunk_file_path = os.path.join(output_dir, f"chunk_{chunk_count}.html")

            # Write the chunk to a new HTML file
            with open(chunk_file_path, "w", encoding="utf-8") as chunk_file:
                # Optional: add HTML doctype and head tags
                chunk_file.write(
                    "<!DOCTYPE html>\n<html>\n<head>\n<meta charset='utf-8'>\n</head>\n<body>\n"
                )
                chunk_file.writelines(chunk)
                chunk_file.write("\n</body>\n</html>")

            logger.info(f"Created chunk file: {chunk_file_path}")
            chunk_count += 1

    logger.info(f"Splitting completed. {chunk_count} files created in '{output_dir}'.")


# Example usage
split_html_file(
    "/Users/steven/Music/NocTurnE-meLoDieS/Song-origins-html/Raccoon Alley Album Art(83% copy).html"
)
