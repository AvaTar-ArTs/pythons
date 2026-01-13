from pathlib import Path
import csv
import os
from io import BytesIO

import requests
from PIL import Image

import logging

logger = logging.getLogger(__name__)


# Constants
CONSTANT_300 = 300


# Paths for input CSV and output directory
input_csv_path = str(Path.home()) + "/Downloads/Dalle-Aug2024 - Sheet1.csv"
output_dir = Path(
    str(Path.home()) + "/Downloads/output_images/"
)  # You can change the output directory if needed

# Ensure the output directory exists
os.makedirs(output_dir, exist_ok=True)

# Read URLs from the CSV
urls = []
with open(input_csv_path, newline="") as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        urls.append(row["URL"])


# Function to download an image and convert it to PNG with CONSTANT_300 DPI
def download_and_convert_to_png(url, output_dir, index):
    """download_and_convert_to_png function."""

    try:
        response = requests.get(url)
        img = Image.open(BytesIO(response.content))
        # Convert to RGB if not in RGB mode
        if img.mode != "RGB":
            img = img.convert("RGB")
        # Save the image as PNG with CONSTANT_300 DPI
        output_path = os.path.join(output_dir, f"image_{index}.png")
        img.save(output_path, "PNG", dpi=(CONSTANT_300, CONSTANT_300))
        logger.info(f"Saved: {output_path}")
    except Exception as e:
        logger.info(f"Failed to download or convert {url}: {str(e)}")


# Download and convert images
for i, url in enumerate(urls):
    download_and_convert_to_png(url, output_dir, i + 1)
