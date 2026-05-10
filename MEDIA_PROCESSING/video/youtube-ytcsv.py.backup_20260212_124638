from pathlib import Path
from pytube import Playlist

import logging

logger = logging.getLogger(__name__)


# Replace the playlist URL below with your desired playlist URL
playlist_url = (
    "https://www.youtube.com/playlist?list=PLfudK7D_bQIjRgAqVU_jkbnb1N5V_pNiG"
)

# Define the directory where you want to save the downloads
download_directory = Path(str(Path.home()) + "/Movies/ESO/qshorts")

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
