"""
Leonardo Processr V2

This module provides functionality for leonardo processr v2.

Author: Auto-generated
Date: 2025-11-01
"""

from pathlib import Path
import csv
import json

import logging

logger = logging.getLogger(__name__)


# File paths
input_file_path = Path(
    "/Users/steven/Pictures/leonardo.json"
)  # Path to the input JSON file
output_file_path = Path(
    "/Users/steven/Pictures/leonardo_generations_full.csv"
)  # Path to the output CSV file

# Headers for the CSV file
headers = [
    "id",
    "prompt",
    "negativePrompt",
    "url",
    "motionMP4URL",
    "motionStrength",
    "height",
    "width",
    "duration",
]

# Open and process the JSON file
with open(input_file_path, "r") as json_file:
    data = json.load(json_file)
    generations = data.get("generations", [])

    # Extract relevant fields
    rows = []
    for generation in generations:
        for image in generation.get("generated_images", []):
            row = {
                "id": generation.get("id"),
                "prompt": generation.get("prompt", ""),
                "negativePrompt": generation.get("negativePrompt", ""),
                "url": image.get("url"),
                "motionMP4URL": image.get("motionMP4URL"),
                "motionStrength": generation.get("motionStrength"),
                "height": generation.get("imageHeight"),
                "width": generation.get("imageWidth"),
                "duration": None,  # Placeholder for duration, if applicable
            }
            rows.append(row)

# Write data to CSV
with open(output_file_path, "w", newline="", encoding="utf-8") as csv_file:
    writer = csv.DictWriter(csv_file, fieldnames=headers)
    writer.writeheader()
    writer.writerows(rows)

logger.info(f"Data processed and saved to {output_file_path}")
