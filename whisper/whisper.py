"""
Whisper 5

This module provides functionality for whisper 5.

Author: Auto-generated
Date: 2025-11-01
"""

import json
import os
from glob import glob

import pandas as pd

import logging

logger = logging.getLogger(__name__)


# Define the root directory path where JSON files are stored
ROOT_DIR = "/Users/steven/Library/Application Support/WhisperTranscribe/library"

# Recursively find all JSON files in subdirectories
json_files = sorted(
    glob(os.path.join(ROOT_DIR, "**/*.json"), recursive=True),
    key=lambda x: (
        int("".join(filter(str.isdigit, x))) if any(c.isdigit() for c in x) else 0
    ),
)

data_list = []

# Define the updated headers we want in the CSV
HEADERS = [
    "Title",
    "Summary",
    "Quotes",
    "Chapters",
    "Show Notes",
    "Newsletter",
    "Blog post",
    "LinkedIn",
    "Instagram",
    "X [Twitter]",
    "youtube seo info",
    "short youtube seo",
    "seo-trendy",
    "Typog",
    "creative youtube seo",
    "trans",
    "Origins",
    "Img-typog",
    "seo-title-keys",
]

# Process JSON files
for file in json_files:
    with open(file, "r", encoding="utf-8") as f:
        data = json.load(f)

    content_map = {}
    for entry in data:
        if isinstance(entry, dict) and "name" in entry and "results" in entry:
            name = entry["name"]
            content = entry["results"][0]["body"] if entry["results"] else ""
            content_map[name] = content

    row_data = {col: content_map.get(col, "") for col in HEADERS}
    data_list.append(row_data)

# Convert to DataFrame
df = pd.DataFrame(data_list, columns=HEADERS)

# Save as CSV
output_csv = os.path.join(ROOT_DIR, "combined_output.csv")
df.to_csv(output_csv, index=False, encoding="utf-8-sig")

logger.info(f"Success! Created combined CSV with {len(df)} rows at: {output_csv}")
