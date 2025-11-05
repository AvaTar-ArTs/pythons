import os
from pathlib import Path
from urllib.parse import urlparse

import pandas as pd
import requests

import logging

logger = logging.getLogger(__name__)


# Constants
CONSTANT_200 = 200
CONSTANT_1024 = 1024


def safe_filename(title):
    """Create a safe filename from a title."""
    return "".join([c if c.isalnum() else "_" for c in title])


def download_image(url, path):
    """Download an image from a URL and save it to a path."""
    try:
        response = requests.get(url, stream=True)
        if response.status_code == CONSTANT_200:
            with open(path, "wb") as file:
                for chunk in response.iter_content(CONSTANT_1024):
                    file.write(chunk)
            logger.info(f"Downloaded: {path}")
        else:
            logger.info(f"Failed to download {url}")
    except Exception as e:
        logger.info(f"Error downloading {url}: {e}")


# User input for CSV file and directory name
csv_file = input("Enter the path to your CSV file: ")
base_image_dir = input("Enter the name of the directory to save images: ")

# Read CSV file
df = pd.read_csv(csv_file)

# Create base directory
os.makedirs(base_image_dir, exist_ok=True)

# Iterate through the rows
for index, row in df.iterrows():
    # Create a subdirectory for each product/listing
    title = safe_filename(row["TITLE"])
    product_dir = os.path.join(base_image_dir, title)
    os.makedirs(product_dir, exist_ok=True)

    # Download and save each image
    for i in range(1, 11):  # Assuming up to 10 image columns (IMAGE1 to IMAGE10)
        image_url = row.get(f"IMAGE{i}")
        if pd.notna(image_url):
            file_name = f"{title}_{i}.jpg"  # Change extension if necessary
            file_path = os.path.join(product_dir, file_name)
            download_image(image_url, file_path)

logger.info("Image downloading process completed.")
