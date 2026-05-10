import pandas as pd
from pytube import Playlist

import logging

logger = logging.getLogger(__name__)


try:
    playlist_url = (
        "https://www.youtube.com/playlist?list=PLfudK7D_bQIjRgAqVU_jkbnb1N5V_pNiG"
    )
    playlist = Playlist(playlist_url)

    videos_info = {
        "Title": [],
        "Video URL": [],
        "Length (seconds)": [],
        "Views": [],
        "Thumbnail URL": [],
        "Description": [],
    }

    for video in playlist.videos:
        videos_info["Title"].append(video.title)
        videos_info["Video URL"].append(video.watch_url)
        videos_info["Length (seconds)"].append(video.length)
        videos_info["Views"].append(video.views)
        videos_info["Thumbnail URL"].append(video.thumbnail_url)
        videos_info["Description"].append(video.description)

    df = pd.DataFrame(videos_info)
    df.to_csv("playlist_info.csv", index=False)
    logger.info("Playlist data has been written to CSV.")

except Exception as e:
    logger.info(f"An error occurred: {e}")
