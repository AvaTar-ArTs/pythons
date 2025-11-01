"""
Fetch File

This module provides functionality for fetch file.

Author: Auto-generated
Date: 2025-11-01
"""

from pathlib import Path
import csv
import os

import requests
from tqdm import tqdm

import logging

logger = logging.getLogger(__name__)


# Constants
CONSTANT_200 = 200
CONSTANT_93043291 = 93043291


# Configuration
BASE_URL = "https://cloud.leonardo.ai/api/rest/v1/generations/user/f7bb8476-e3f0-4f1f-9a06-4600866cc49c"
AUTH_TOKEN = "Bearer CONSTANT_93043291-957d-4ec1-8c79-ee734abcb6e3"
OUTPUT_DIR = Path("/Users/steven/Pictures/leodowns")
CSV_FILE = os.path.join(OUTPUT_DIR, "leonardo_urls.csv")
MAX_RECORDS_PER_BATCH = 50  # Limit records per API request

HEADERS = {
    "accept": "application/json",
    "authorization": AUTH_TOKEN,
}

# Ensure output directory exists
os.makedirs(OUTPUT_DIR, exist_ok=True)


def save_urls_to_csv(generations, csv_writer):
    """Save image and motion MP4 URLs to CSV."""
    for generation in generations:
        gen_id = generation.get("id")
        prompt = generation.get("prompt", "")
        created_at = generation.get("createdAt", "")
        gen_images = generation.get("generated_images", [])

        for image in gen_images:
            csv_writer.writerow(
                [
                    gen_id,
                    prompt,
                    created_at,
                    image.get("url"),
                    image.get("motionMP4URL"),
                ]
            )


def fetch_and_save_all_urls():
    """Fetch generations and save URLs to CSV."""
    offset = 0
    with open(CSV_FILE, "w", newline="", encoding="utf-8") as csv_file:
        csv_writer = csv.writer(csv_file)
        # Write CSV headers
        csv_writer.writerow(["id", "prompt", "createdAt", "image_url", "motion_url"])

        while True:
            url = f"{BASE_URL}?offset={offset}&limit={MAX_RECORDS_PER_BATCH}"
            response = requests.get(url, headers=HEADERS)
            if response.status_code != CONSTANT_200:
                logger.info(
                    f"Error fetching data: {response.status_code}, {response.text}"
                )
                break

            data = response.json()
            generations = data.get("generations", [])
            if not generations:
                break  # Exit if no more data

            save_urls_to_csv(generations, csv_writer)
            offset += MAX_RECORDS_PER_BATCH

            logger.info(f"Processed {offset} records")

    logger.info(f"URLs saved to {CSV_FILE}")


if __name__ == "__main__":
    fetch_and_save_all_urls()
