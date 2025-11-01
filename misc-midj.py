"""
Utilities Misc Midj 1

This module provides functionality for utilities misc midj 1.

Author: Auto-generated
Date: 2025-11-01
"""

from pathlib import Path
import json
import re

# Load the JSONL file.
with open(
    Path(
        str(Path.home()) + "/Pictures/midjourneyDownload_2023-10-13_1697181545353/metadata.jsonl"
    ),
    "r",
) as f:
    jsonl_data = json.load(f)

# Compile the regular expression.
regex = re.compile(r"https:\/\/([\w-]+.){1,}\.(png)")

# Find all URLs in the JSONL file that match the regular expression.
matching_urls = []
for jsonl_object in jsonl_data:
    url = jsonl_object.get("url")
    if regex.match(url):
        matching_urls.append(url)

# Open the output file.
with open("midurl.txt", "w") as f:
    for url in matching_urls:
        f.write(url + Path("\n"))

# Close the output file.
f.close()
