"""
Csv Url Down

This module provides functionality for csv url down.

Author: Auto-generated
Date: 2025-11-01
"""

from pathlib import Path
import csv
import os

import requests

import logging

logger = logging.getLogger(__name__)


# Constants
CONSTANT_8192 = 8192


# Set the output directory
output_directory = "downloaded_files"
os.makedirs(output_directory, exist_ok=True)

# Path to the CSV file containing URLs
csv_file_path = Path(str(Path.home()) + "/Pictures/etsy/printify/mydesigns-export.CSV")

# Column name in the CSV that contains the URLs
url_column_name = "url"  # Adjust to match your CSV file's structure

# Read the CSV file and download each URL
with open(csv_file_path, newline="", encoding="utf-8") as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        url = row[url_column_name]
        try:
            response = requests.get(url, stream=True)
            response.raise_for_status()  # Raise an error for bad responses (4xx and 5xx)

            # Extract file name from the URL
            file_name = os.path.basename(url)
            output_path = os.path.join(output_directory, file_name)

            # Save the file content
            with open(output_path, "wb") as output_file:
                for chunk in response.iter_content(chunk_size=CONSTANT_8192):
                    output_file.write(chunk)
            logger.info(f"Downloaded: {file_name}")
        except requests.RequestException as e:
            logger.info(f"Failed to download {url}: {e}")
