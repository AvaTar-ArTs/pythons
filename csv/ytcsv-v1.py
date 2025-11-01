"""
Ytcsv

This module provides functionality for ytcsv.

Author: Auto-generated
Date: 2025-11-01
"""

import csv

from pytube import YouTube

import logging

logger = logging.getLogger(__name__)


# Function to extract video metadata
def get_video_info(url):
    """get_video_info function."""

    yt = YouTube(url)
    video_info = {
        "Title": yt.title,
        "Views": yt.views,
        "Likes": yt.rating,
        "Length (seconds)": yt.length,
        "Description": yt.description,
    }
    return video_info

    # Function to write info to CSV
    """write_to_csv function."""


def write_to_csv(video_info, csv_filename):
    with open(csv_filename, "w", newline="") as csvfile:
        fieldnames = video_info.keys()
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()  # Write the header
        writer.writerow(video_info)  # Write the video info


# Main
video_url = "https://youtu.be/VTRp7hQkZos"  # Replace with your YouTube URL
csv_file = "video_info.csv"  # Output CSV file

video_info = get_video_info(video_url)
write_to_csv(video_info, csv_file)

logger.info(f"Video information saved to {csv_file}")
