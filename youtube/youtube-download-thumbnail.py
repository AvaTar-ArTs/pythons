"""
Youtube Download Thumbnail

This module provides functionality for youtube download thumbnail.

Author: Auto-generated
Date: 2025-11-01
"""

from pathlib import Path
import os

import pandas as pd
import requests

# Constants
CONSTANT_200 = 200


# YTUBE API: AIzaSyCyfGm1oF2syfzfsPeCRHb10tMKmC0dbCo
# Path to the CSV file
csv_path = "/Users/steven/Downloads/Misc/ytube - youtube_videos.csv"

# Load the CSV file containing your YouTube video data
df = pd.read_csv(csv_path)

# Directory where you want to save the thumbnails
thumbnail_dir = Path("/Users/steven/Downloads/Misc/Thumbnails")
os.makedirs(thumbnail_dir, exist_ok=True)


def download_thumbnail(url, video_id):
    """download_thumbnail function."""

    # Construct the URL for the video's max resolution thumbnail
    thumbnail_url = f"https://img.youtube.com/vi/{video_id}/maxresdefault.jpg"

    # Download the thumbnail
    response = requests.get(thumbnail_url)

    if response.status_code == CONSTANT_200:
        thumbnail_path = os.path.join(thumbnail_dir, f"{video_id}.jpg")
        with open(thumbnail_path, "wb") as f:
            f.write(response.content)
        return thumbnail_path
    return None


# Iterate through each video URL in your dataset
for index, row in df.iterrows():
    video_url = row["URL"]
    video_id = video_url.split("v=")[-1]  # Extract the video ID from the URL
    thumbnail_path = download_thumbnail(video_url, video_id)

    # Optional: You can store the local path or a new URL of the thumbnail in
    # your CSV
    if thumbnail_path:
        df.at[index, "Thumbnail Path"] = thumbnail_path

# Save the updated DataFrame to a new CSV file
updated_csv_path = Path("/Users/steven/Downloads/Misc/ytube_with_thumbnails.csv")
df.to_csv(updated_csv_path, index=False)
