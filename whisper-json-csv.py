"""
Summary of whisper-json-csv.py

This module is part of the AVATARARTS ecosystem.
For more information about the AVATARARTS project, see the main documentation.
"""

import json
import os
from glob import glob

import pandas as pd
from natsort import natsorted

ROOT_DIR = "/Users/steven/Documents/Whisper-Text/"

json_files = glob(os.path.join(ROOT_DIR, "**/*.json"), recursive=True)
json_files = natsorted(json_files)

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
]

data_list = []

for file in json_files:
    try:
        with open(file, "r", encoding="utf-8") as f:
            data = json.load(f)
    except Exception as e:
        print(f"⚠️ Skipping {file} due to error: {e}")
        continue

    if not isinstance(data, list):
        print(f"⚠️ Invalid format in {file}: Expected list, got {type(data)}")
        continue

    content_map = {}
    for entry in data:
        if not isinstance(entry, dict):
            continue

        if "name" in entry and "results" in entry:
            original_name = entry["name"]
            # Case-insensitive header matching
            matched_header = next((h for h in HEADERS if h.lower() == original_name.lower()), None)

            if matched_header:
                content = entry["results"][0]["body"] if entry["results"] else ""

                if matched_header in content_map:
                    print(f"⚠️ Duplicate field '{matched_header}' in {file} - overwriting")

                content_map[matched_header] = content

    row_data = {col: content_map.get(col, "") for col in HEADERS}
    data_list.append(row_data)

df = pd.DataFrame(data_list, columns=HEADERS)

output_csv = os.path.join(ROOT_DIR, "combined_output3.csv")
df.to_csv(output_csv, index=False, encoding="utf-8-sig")

print(f"✅ Success! Created CSV with {len(df)} rows at:\n{output_csv}")
