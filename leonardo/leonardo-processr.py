"""
Leonardo Processr

This module provides functionality for leonardo processr.

Author: Auto-generated
Date: 2025-11-01
"""

from pathlib import Path
import csv
import gzip
import json
import os

import logging

logger = logging.getLogger(__name__)


# Configuration
OUTPUT_DIR = Path("/Users/steven/Downloads/leonardo_images")
CSV_FILE = os.path.join(OUTPUT_DIR, "leonardo_metadata.csv")

# Headers for CSV
HEADERS = [
    "id",
    "prompt",
    "negativePrompt",
    "motionStrength",
    "createdAt",
    "image_url",
    "motion_url",
    "local_image_path",
    "local_motion_path",
]


def process_json_to_csv(json_file, csv_writer):
    """Process a single JSON file and write its content to the CSV."""
    with gzip.open(json_file, "rt", encoding="utf-8") as file:
        data = json.load(file)

        for record in data:
            gen_id = record.get("id")
            prompt = record.get("prompt", "")
            negative_prompt = record.get("negativePrompt", "")
            motion_strength = record.get("motionStrength")
            created_at = record.get("createdAt", "")

            for image in record.get("images", []):
                csv_writer.writerow(
                    [
                        gen_id,
                        prompt,
                        negative_prompt,
                        motion_strength,
                        created_at,
                        image.get("image_url"),
                        image.get("motion_url"),
                        image.get("local_path") if image.get("image_url") else "",
                        image.get("local_path") if image.get("motion_url") else "",
                    ]
                )


def combine_json_to_csv():
    """Combine all JSON files into a single CSV."""
    json_files = sorted([f for f in os.listdir(OUTPUT_DIR) if f.endswith(".json.gz")])
    csv_headers_written = False

    with open(CSV_FILE, "w", newline="", encoding="utf-8") as csv_file:
        csv_writer = csv.writer(csv_file)

        for json_file in json_files:
            json_path = os.path.join(OUTPUT_DIR, json_file)
            logger.info(f"Processing: {json_path}")

            if not csv_headers_written:
                csv_writer.writerow(HEADERS)
                csv_headers_written = True

            process_json_to_csv(json_path, csv_writer)

    logger.info(f"CSV created at {CSV_FILE}")


if __name__ == "__main__":
    combine_json_to_csv()
