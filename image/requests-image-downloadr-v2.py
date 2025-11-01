"""
Requests Image Downloadr

This module provides functionality for requests image downloadr.

Author: Auto-generated
Date: 2025-11-01
"""

from pathlib import Path
import gzip
import json
import os
from concurrent.futures import ThreadPoolExecutor

import requests
from tqdm import tqdm

import logging

logger = logging.getLogger(__name__)


# Constants
CONSTANT_200 = 200
CONSTANT_500 = 500
CONSTANT_8192 = 8192
CONSTANT_93043291 = 93043291


# Configuration
BASE_URL = "https://cloud.leonardo.ai/api/rest/v1/generations/user/f7bb8476-e3f0-4f1f-9a06-4600866cc49c"
AUTH_TOKEN = "Bearer CONSTANT_93043291-957d-4ec1-8c79-ee734abcb6e3"
OUTPUT_DIR = Path("/Users/steven/Pictures/leodowns")
MAX_RECORDS_PER_FILE = CONSTANT_500  # Limit records per JSON file
MAX_WORKERS = 5  # For parallel downloads
INCLUDE_IMAGES = True  # Set False to skip image downloads

HEADERS = {
    "accept": "application/json",
    "authorization": AUTH_TOKEN,
}

# Ensure output directory exists
os.makedirs(OUTPUT_DIR, exist_ok=True)

# State file for resuming
STATE_FILE = os.path.join(OUTPUT_DIR, "state.json")


def download_image(url, path):
    """Download an image with retries."""
    for attempt in range(3):  # Retry up to 3 times
        try:
            response = requests.get(url, stream=True)
            response.raise_for_status()
            with open(path, "wb") as file:
                for chunk in response.iter_content(chunk_size=CONSTANT_8192):
                    file.write(chunk)
            return True
        except Exception as e:
            logger.info(f"Retry {attempt + 1} for {url}: {e}")
    logger.info(f"Failed to download after retries: {url}")
    return False


def save_metadata_to_file(metadata, index):
    """Save metadata to a JSON file, compressing the output."""
    file_path = os.path.join(OUTPUT_DIR, f"leonardo_images{index}.json.gz")
    with gzip.open(file_path, "wt", encoding="utf-8") as gz_file:
        json.dump(metadata, gz_file, indent=4)
    logger.info(f"Saved metadata to {file_path}")


def fetch_and_download_all_generations():
    """Fetch generations and handle downloading images and saving metadata."""
    offset, file_index, record_count = 0, 1, 0
    all_metadata = []

    # Resume state if available
    if os.path.exists(STATE_FILE):
        with open(STATE_FILE, "r") as state:
            saved_state = json.load(state)
            offset = saved_state.get("offset", 0)
            file_index = saved_state.get("file_index", 1)

    while True:
        url = f"{BASE_URL}?offset={offset}&limit=50"
        response = requests.get(url, headers=HEADERS)
        if response.status_code != CONSTANT_200:
            logger.info(f"Error fetching data: {response.status_code}, {response.text}")
            break

        data = response.json()
        generations = data.get("generations", [])
        if not generations:
            break  # Exit if no more data

        for generation in tqdm(generations, desc=f"Processing Batch {file_index}"):
            gen_id = generation.get("id")
            gen_images = generation.get("generated_images", [])
            gen_metadata = {
                "id": gen_id,
                "prompt": generation.get("prompt", ""),
                "negativePrompt": generation.get("negativePrompt", ""),
                "motionStrength": generation.get("motionStrength"),
                "createdAt": generation.get("createdAt"),
                "images": [],
            }

            for image in gen_images:
                image_url = image.get("url")
                motion_url = image.get("motionMP4URL")

                if INCLUDE_IMAGES:
                    if image_url:
                        image_path = os.path.join(
                            OUTPUT_DIR, f"{gen_id}_{image.get('id')}.jpg"
                        )
                        if download_image(image_url, image_path):
                            gen_metadata["images"].append(
                                {"image_url": image_url, "local_path": image_path}
                            )

                    if motion_url:
                        motion_path = os.path.join(
                            OUTPUT_DIR, f"{gen_id}_{image.get('id')}.mp4"
                        )
                        if download_image(motion_url, motion_path):
                            gen_metadata["images"].append(
                                {"motion_url": motion_url, "local_path": motion_path}
                            )

            all_metadata.append(gen_metadata)
            record_count += 1

            # Save and reset if MAX_RECORDS_PER_FILE is reached
            if record_count >= MAX_RECORDS_PER_FILE:
                save_metadata_to_file(all_metadata, file_index)
                all_metadata = []
                record_count = 0
                file_index += 1

                # Save state
                with open(STATE_FILE, "w") as state:
                    json.dump({"offset": offset + 1, "file_index": file_index}, state)

        offset += 50

    # Save remaining records
    if all_metadata:
        save_metadata_to_file(all_metadata, file_index)

    # Clear state after completion
    if os.path.exists(STATE_FILE):
        os.remove(STATE_FILE)


if __name__ == "__main__":
    fetch_and_download_all_generations()
