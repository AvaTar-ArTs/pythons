"""
Content Creation Nocturne Ytcsv 1

This module provides functionality for content creation nocturne ytcsv 1.

Author: Auto-generated
Date: 2025-11-01
"""

import logging

logger = logging.getLogger(__name__)

#!/usr/bin/env python3
"""
Merged Content Analysis Tool

This file was automatically merged from the following source files:
- /Users/steven/Music/nocTurneMeLoDieS/python/FINAL_ORGANIZED/generation/ytcsv.py
- /Users/steven/Music/nocTurneMeLoDieS/python/CLEAN_ORGANIZED/generation/ytcsv.py

Combines the best features and functionality from multiple similar files.
"""

# Imports from all source files
from pathlib import Path
from pytube import Playlist

playlist_url = (
    "https://www.youtube.com/playlist?list=PLfudK7D_bQIjRgAqVU_jkbnb1N5V_pNiG"
)

# Define the directory where you want to save the downloads
download_directory = Path("/Users/steven/Movies/ESO/qshorts")

# Create a Playlist object
playlist = Playlist(playlist_url)

# Loop through the videos in the playlist
for video in playlist.videos:
    # Download the video
    video.streams.get_highest_resolution().download()

    # Get video metadata
    title = video.title
    description = video.description
    tags = video.keywords

    # Print or save the metadata as needed
    logger.info(f"Title: {title}")
    logger.info(f"Description: {description}")
    logger.info(f"Tags: {', '.join(tags)}")
