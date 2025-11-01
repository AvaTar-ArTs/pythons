"""
Content Creation Nocturne Scan 4

This module provides functionality for content creation nocturne scan 4.

Author: Auto-generated
Date: 2025-11-01
"""

from pathlib import Path
import os
import re
import csv
from datetime import datetime

import logging

logger = logging.getLogger(__name__)


# Constants
CONSTANT_1024 = 1024


# Define base directories to scan
BASE_DIRS = [
    Path("/Users/steven/Documents/Python_backup"),
    Path("/Users/steven/Documents/Python"),
    Path("/Users/steven/Music/nocTurneMeLoDieS/lyrics-keys-indo"),
    Path("/Users/steven/Music/nocTurneMeLoDieS/mp3-analyze-transcribe")
]

# Regex patterns for exclusions
EXCLUDED_PATTERNS = [
    r'^\..*',
    r'.*/venv/.*',
    r'.*/\.venv/.*',
    r'.*/lib/.*',
    r'.*/\.lib/.*',
    r'.*/my_global_venv/.*',
    r'.*/simplegallery/.*',
    r'.*/avatararts/.*',
    r'.*/github/.*',
    r'.*/Documents/gitHub/.*',
    r'.*/\.my_global_venv/.*',
    r'.*/node/.*',
    r'.*/miniconda3/.*',
    r'.*/env/.*',
    r'.*/\.env/.*',
    r'.*/Library/.*',
    r'.*/\.config/.*',
    r'.*/\.spicetify/.*',
    r'.*/\.gem/.*',
    r'.*/\.zprofile/.*',
    r'^.*/\..*'
]

# File type categories
FILE_TYPES = {
    '.pdf': 'Documents', '.csv': 'Documents', '.html': 'Documents',
    '.css': 'Documents', '.js': 'Documents', '.json': 'Documents',
    '.sh': 'Documents', '.md': 'Documents', '.txt': 'Documents',
    '.doc': 'Documents', '.docx': 'Documents', '.ppt': 'Documents',
    '.pptx': 'Documents', '.xlsx': 'Documents', '.py': 'Documents',
    '.xml': 'Documents'
}

def is_excluded(path):
    return any(re.match(pattern, path) for pattern in EXCLUDED_PATTERNS)
def scan_directory(base_dir):
    results = []
    for root, _, files in os.walk(base_dir):
        for file in files:
            full_path = os.path.join(root, file)
            if is_excluded(full_path):
                continue
            if os.path.islink(full_path):
                continue
            try:
                size_kb = os.path.getsize(full_path) // CONSTANT_1024
            except (FileNotFoundError, OSError):
                logger.info(f"⚠️ Skipped broken file path: {full_path}")
                continue
            ext = os.path.splitext(file)[1].lower()
            file_type = FILE_TYPES.get(ext, 'Other')
            results.append([file, ext, file_type, size_kb, full_path])
    return results

def save_csv(data, output_path):
    headers = ['File Name', 'Extension', 'Type', 'Size (KB)', 'Full Path']
    with open(output_path, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(headers)
        writer.writerows(data)

def main():
    all_results = []
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    for base_dir in BASE_DIRS:
        logger.info(f"🔍 Scanning: {base_dir}")
        results = scan_directory(base_dir)
        all_results.extend(results)
        output_path = os.path.join(base_dir, f"scan_results_{timestamp}.csv")
        save_csv(results, output_path)
        logger.info(f"📄 Saved CSV for {base_dir} → {output_path}")

    # Save total summary CSV
    total_csv = f"/Users/steven/Documents/scan_total_summary_{timestamp}.csv"
    save_csv(all_results, total_csv)
    logger.info(f"✅ All results saved to {total_csv}")

if __name__ == "__main__":
    main()