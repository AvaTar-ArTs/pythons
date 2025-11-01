"""
Nocturne Music Catalog Csv

This module provides functionality for nocturne music catalog csv.

Author: Auto-generated
Date: 2025-11-01
"""

from pathlib import Path
import csv
import os

import logging

logger = logging.getLogger(__name__)


# Define the directories
mp3_dir = Path(str(Path.home()) + "/Music/NocTurnE-meLoDieS/mp3")
txt_dir = Path(str(Path.home()) + "/Music/NocTurnE-meLoDieS/mp3")
csv_output = Path(str(Path.home()) + "/Music/NocTurnE-meLoDieS/songs_data.csv")

# Collect the list of MP3 and text files
mp3_files = [f for f in os.listdir(mp3_dir) if f.endswith(".mp3")]
txt_files = [f for f in os.listdir(txt_dir) if f.endswith(".txt")]


# Function to match song with corresponding text files
def get_matching_files(song_title, txt_files):
    """get_matching_files function."""

    analysis_file = None
    transcript_file = None
    base_title = song_title.replace(".mp3", "")
    for txt in txt_files:
        if base_title in txt:
            if "analysis" in txt.lower():
                analysis_file = txt
            elif "transcript" in txt.lower():
                transcript_file = txt
    return analysis_file, transcript_file


# Create and write to the CSV
with open(csv_output, mode="w", newline="") as file:
    writer = csv.writer(file)
    writer.writerow(
        [
            "Title",
            "Artist",
            "MP3 Path",
            "Analysis Path",
            "Transcript Path",
            "Image Path",
            "Description",
        ]
    )

    # Loop over MP3 files
    for mp3 in mp3_files:
        song_title = mp3.replace(".mp3", "")
        analysis_file, transcript_file = get_matching_files(mp3, txt_files)

        # Set Artist as TrashCaTs but allow customization in the CSV
        writer.writerow(
            [
                song_title,
                "TrashCaTs (Customizable)",  # Customize later for each song
                os.path.join(mp3_dir, mp3),  # MP3 path
                (
                    os.path.join(txt_dir, analysis_file) if analysis_file else ""
                ),  # Analysis path
                (
                    os.path.join(txt_dir, transcript_file) if transcript_file else ""
                ),  # Transcript path
                "https://via.placeholder.com/150",  # Placeholder for an image
                "Lorem ipsum dolor sit amet.",  # Placeholder description
            ]
        )

logger.info(f"CSV file generated at: {csv_output}")
