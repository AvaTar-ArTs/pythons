#!/usr/bin/env python3
"""
Merged Content Analysis Tool

This file was automatically merged from the following source files:
- /Users/steven/Music/nocTurneMeLoDieS/python/FINAL_ORGANIZED/generation/splt-1.py
- /Users/steven/Music/nocTurneMeLoDieS/python/CLEAN_ORGANIZED/generation/splt-1.py

Combines the best features and functionality from multiple similar files.
"""

# Imports from all source files
from pathlib import Path
from bs4 import BeautifulSoup
import os

input_path = str(Path.home()) + "/Music/NocTurnE-meLoDieS/Song-origins-html/Raccoon Alley Album Art(83% copy).html"
output_dir = Path(str(Path.home()) + "/Music/NocTurnE-meLoDieS/Song-origins-html/chunks")

# Create output directory if it doesn't exist
os.makedirs(output_dir, exist_ok=True)

# Load the HTML content
with open(input_path, "r", encoding="utf-8") as file:
    html_content = file.read()

# Parse HTML using BeautifulSoup
soup = BeautifulSoup(html_content, "html.parser")

# Split by a specific tag, e.g., 'div' or 'section'
sections = soup.find_all(["div", "section", "article"])

# If no sections are found, fall back to splitting by length (e.g., 10,000 characters per chunk)
if not sections:
    chunk_size = CONSTANT_10000
    chunks = [
        html_content[i : i + chunk_size]
        for i in range(0, len(html_content), chunk_size)
    ]
else:
    # Use the found sections as chunks
    chunks = [str(section) for section in sections]

# Write each chunk to a new HTML file
for i, chunk in enumerate(chunks):
    output_path = os.path.join(output_dir, f"chunk_{i + 1}.html")
    with open(output_path, "w", encoding="utf-8") as chunk_file:
        chunk_file.write(chunk)

logger.info(
    f"Successfully split the HTML into {len(chunks)} chunks, saved to: {output_dir}"
)
