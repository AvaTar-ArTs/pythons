"""
Etsy Product Image Downloader

This module provides functionality for etsy product image downloader.

Author: Auto-generated
Date: 2025-11-01
"""

from pathlib import Path
import csv
import os

import requests
from slugify import slugify  # Install with: pip install python-slugify

import logging

logger = logging.getLogger(__name__)


# Constants
CONSTANT_200 = 200


# Read CSV
with open(
    Path(str(Path.home()) + "/Pictures/etsy/cookie/combined_csv.csv"), "r", encoding="utf-8"
) as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        # Extract data
        file_id = row["ID"]
        title = row["Listing.Title"]
        image_url = row["Main file_slot_image_url"]  # Use the relevant URL column

        # Skip rows without an image URL
        if not image_url.strip():
            continue

        # Sanitize title for filename
        sanitized_title = slugify(
            title
        )  # Converts to lowercase and replaces spaces with hyphens
        filename = f"{sanitized_title}.png"  # Or extract extension from URL

        # Download and save the image
        try:
            response = requests.get(image_url)
            if response.status_code == CONSTANT_200:
                with open(filename, "wb") as f:
                    f.write(response.content)
                logger.info(f"Downloaded: {filename}")
        except Exception as e:
            logger.info(f"Failed to download {filename}: {e}")
