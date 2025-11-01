"""
Data Processing Pandas Csv Json 1

This module provides functionality for data processing pandas csv json 1.

Author: Auto-generated
Date: 2025-11-01
"""

from pathlib import Path
import json
import os
from glob import glob

import pandas as pd
from natsort import natsorted

import logging

logger = logging.getLogger(__name__)


# Set your root directory containing the JSON files
ROOT_DIR = Path(str(Path.home()) + "/Documents/Conversation_JSONs/")  # Adjust as needed

# Find all JSON files recursively and sort them naturally
json_files = glob(os.path.join(ROOT_DIR, "**/*.json"), recursive=True)
json_files = natsorted(json_files)

# Define the headers for the CSV
HEADERS = ["Title", "Node ID", "Parent", "Children", "Author Role", "Content", "Status"]

data_list = []

for file in json_files:
    try:
        with open(file, "r", encoding="utf-8") as f:
            data = json.load(f)
    except Exception as e:
        logger.info(f"⚠️ Skipping {file} due to error: {e}")
        continue

    # Expecting the JSON file to be a list with one summary object
    if not isinstance(data, list):
        logger.info(f"⚠️ Invalid format in {file}: Expected list, got {type(data)}")
        continue

    summary = data[0]
    title = summary.get("title", "")
    mapping = summary.get("mapping", {})

    # Iterate over each node in the mapping
    for node_id, node in mapping.items():
        parent = node.get("parent", "")
        children = "; ".join(node.get("children", []))
        message = node.get("message")
        if message:
            author_role = message.get("author", {}).get("role", "")
            content_parts = message.get("content", {}).get("parts", [])
            # Join parts, converting non-strings if necessary
            content = " ".join(
                [part if isinstance(part, str) else str(part) for part in content_parts]
            )
            status = message.get("status", "")
        else:
            author_role = ""
            content = ""
            status = ""

        row_data = {
            "Title": title,
            "Node ID": node_id,
            "Parent": parent,
            "Children": children,
            "Author Role": author_role,
            "Content": content,
            "Status": status,
        }
        data_list.append(row_data)

# Create a DataFrame and write to CSV
df = pd.DataFrame(data_list, columns=HEADERS)
output_csv = os.path.join(ROOT_DIR, "combined_output.csv")
df.to_csv(output_csv, index=False, encoding="utf-8-sig")

logger.info(f"✅ Success! Created CSV with {len(df)} rows at:\n{output_csv}")
