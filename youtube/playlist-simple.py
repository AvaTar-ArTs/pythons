"""
Yt Playlist

This module provides functionality for yt playlist.

Author: Auto-generated
Date: 2025-11-01
"""

import pandas as pd
from pytube import Playlist

import logging

logger = logging.getLogger(__name__)


# Replace 'YOUR_PLAYLIST_URL' with the URL of your YouTube playlist
playlist_url = (
    "https://www.youtube.com/playlist?list=PLfudK7D_bQIgAVsQUK5WtfVe3_kz9cXjA"
)
playlist = Playlist(playlist_url)

# Dictionary to store video information
videos_info = {
    "Title": [],
    "Video URL": [],
    "Length (seconds)": [],
    "Views": [],
    "Thumbnail URL": [],
    "Description": [],
}

# Loop through all videos in the playlist
for video in playlist.videos:
    videos_info["Title"].append(video.title)
    videos_info["Video URL"].append(video.watch_url)
    videos_info["Length (seconds)"].append(video.length)
    videos_info["Views"].append(video.views)
    videos_info["Thumbnail URL"].append(video.thumbnail_url)
    videos_info["Description"].append(video.description)

# Create a DataFrame and save to CSV
df = pd.DataFrame(videos_info)
df.to_csv("playlist_info.csv", index=False)
logger.info("Playlist data has been written to CSV.")
