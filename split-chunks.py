"""
Ai Image

This module provides functionality for ai image.

Author: Auto-generated
Date: 2025-11-01
"""

from pathlib import Path
import csv


def split_csv(input_file_path, output_file_prefix, chunk_size=50):
    """split_csv function."""

    with open(input_file_path, "r", encoding="utf-8") as input_file:
        reader = csv.reader(input_file)
        header = next(reader)  # Capture the header row

        file_index = 0
        current_chunk = []

        for row in reader:
            current_chunk.append(row)
            if len(current_chunk) == chunk_size:
                start_index = file_index * chunk_size + 1
                end_index = start_index + chunk_size - 1
                write_chunk(
                    output_file_prefix, start_index, end_index, header, current_chunk
                )
                file_index += 1
                current_chunk = []

        # Write any remaining records for the last file
        if current_chunk:
            start_index = file_index * chunk_size + 1
            end_index = start_index + len(current_chunk) - 1
            write_chunk(
                output_file_prefix, start_index, end_index, header, current_chunk
            )

    """write_chunk function."""


def write_chunk(prefix, start_index, end_index, header, chunk):
    filename = f"{prefix}_{start_index}-{end_index}.csv"
    with open(filename, "w", newline="", encoding="utf-8") as output_file:
        writer = csv.writer(output_file)
        writer.writerow(header)  # Write the header row
        writer.writerows(chunk)  # Write the chunk of data


# Usage
split_csv(Path("/Users/steven/master_image_info.csv"), Path("/Users/steven/image_info"))
