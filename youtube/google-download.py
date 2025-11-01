"""
Script 169

This module provides functionality for script 169.

Author: Auto-generated
Date: 2025-11-01
"""

from pathlib import Path
import csv

from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

import logging

logger = logging.getLogger(__name__)


# Define the scopes
SCOPES = [
    "https://www.googleapis.com/auth/youtube.upload",
    "https://www.googleapis.com/auth/youtube",
]

## Authenticate and build the YouTube API service
flow = InstalledAppFlow.from_client_secrets_file(Path("/Users/steven/Movies/youtube-upload/client_secret.json"), SCOPES)

# Use run_local_server instead of run_console
credentials = flow.run_local_server(port=0)
youtube = build("youtube", "v3", credentials=credentials)


def add_video_to_playlist(youtube, video_id, playlist_id):
    """add_video_to_playlist function."""

    body = {
        "snippet": {
            "playlistId": playlist_id,
            "resourceId": {"kind": "youtube#video", "videoId": video_id},
        }
    }
    request = youtube.playlistItems().insert(part="snippet", body=body)
    response = request.execute()
    logger.info(f"Added video ID {video_id} to playlist: {response['snippet']['playlistId']}")


# Read the CSV file
with open("videos.csv", "r") as file:
    reader = csv.DictReader(file)
    for row in reader:
        # Prepare the video metadata
        body = {
            "snippet": {
                "title": row["title"],
                "description": row["description"],
                "tags": row["keywords"].split(","),
                "categoryId": "24",  # Category ID for Entertainment
            },
            "status": {"privacyStatus": "private"},  # or 'private' or 'unlisted'
        }

        # Specify the file path and upload the video
        video_file_path = row["file_path"]
        media = MediaFileUpload(video_file_path, chunksize=-1, resumable=True)
        upload_request = youtube.videos().insert(part="snippet,status", body=body, media_body=media)

        # Execute the upload request and get the video ID
        response = upload_request.execute()
        video_id = response["id"]
        logger.info(f"Uploaded video ID: {video_id}")

        # Now add the video to the playlist
        # You need to specify the playlist ID here
        playlist_id = "PLfudK7D_bQIgAVsQUK5WtfVe3_kz9cXjA"
        add_video_to_playlist(youtube, video_id, playlist_id)
