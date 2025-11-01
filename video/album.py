"""
Album

This module provides functionality for album.

Author: Auto-generated
Date: 2025-11-01
"""

from pathlib import Path
import os
import shutil
import pandas as pd

import logging

logger = logging.getLogger(__name__)


# Constants
CONSTANT_2025 = 2025


# Input file locations (change if needed)
VIDS_CSV = "/Users/steven/Movies/project2025/vids-05-31-18:16.csv"
DOCS_CSV = "/Users/steven/Movies/project2025/docs-05-31-18:16.csv"
PATHS_TXT = Path("/Users/steven/Movies/project2025/paths-CONSTANT_2025.txt")

# Album file types to sort (ignore .png, .jpg, etc.)
SUFFIXES = [".mp4", ".mp3", "_analysis.txt", "_transcript.txt"]
MP4_BASE = Path("/Users/steven/Movies/project2025/mp4")


def extract_album(filename):
    """extract_album function."""

    for suf in SUFFIXES:
        if filename.endswith(suf):
            return filename[: -len(suf)]
    return None


# Load all valid paths from paths-CONSTANT_2025.txt
with open(PATHS_TXT, "r") as f:
    all_paths = set(line.strip() for line in f if line.strip())

# Load CSVs
vids_df = pd.read_csv(VIDS_CSV)
docs_df = pd.read_csv(DOCS_CSV)

# Collect candidate files from both CSVs that exist in paths-CONSTANT_2025.txt and live in mp4
entries = []

for _, row in vids_df.iterrows():
    path = row["Original Path"]
    fname = row["Filename"]
    if path in all_paths and path.startswith(MP4_BASE) and any(fname.endswith(suf) for suf in SUFFIXES):
        album = extract_album(fname)
        if album:
            entries.append((path, album, fname))

for _, row in docs_df.iterrows():
    path = row["Original Path"]
    fname = row["Filename"]
    if path in all_paths and path.startswith(MP4_BASE) and any(fname.endswith(suf) for suf in SUFFIXES):
        album = extract_album(fname)
        if album:
            entries.append((path, album, fname))

# Group all found files by album
from collections import defaultdict

album_map = defaultdict(list)
for path, album, fname in entries:
    album_map[album].append((path, fname))

logger.info(f"Discovered {len(album_map)} albums with {len(entries)} total files.")

# Create folder and move each file for each album
for album, files in album_map.items():
    album_dir = os.path.join(MP4_BASE, album)
    if not os.path.isdir(album_dir):
        try:
            os.makedirs(album_dir)
            logger.info(f"Created folder: {album_dir}")
        except Exception as e:
            logger.info(f"Error creating {album_dir}: {e}")
            continue

    for src_path, fname in files:
        dest_path = os.path.join(album_dir, fname)
        if os.path.abspath(src_path) == os.path.abspath(dest_path):
            logger.info(f"Already in place: {src_path}")
            continue
        if os.path.exists(dest_path):
            logger.info(f"Skipped (already exists): {dest_path}")
            continue
        try:
            shutil.move(src_path, dest_path)
            logger.info(f"Moved: {src_path} → {dest_path}")
        except Exception as e:
            logger.info(f"Error moving {src_path} to {dest_path}: {e}")

logger.info("✅ Album-style sorting complete.")
