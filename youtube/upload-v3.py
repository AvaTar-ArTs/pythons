"""
Upload 6

This module provides functionality for upload 6.

Author: Auto-generated
Date: 2025-11-01
"""

from pathlib import Path
import os
import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors
import pandas as pd

import logging

logger = logging.getLogger(__name__)


# Load client secrets from environment variable
CLIENT_SECRETS_FILE = os.getenv("GOOGLE_CLIENT_SECRET")

# Define the required scope for uploading videos
SCOPES = ["https://www.googleapis.com/auth/youtube.upload"]


def authenticate():
    """Authenticates the user and returns a YouTube API client."""
    flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(CLIENT_SECRETS_FILE, SCOPES)
    credentials = flow.run_console()
    return googleapiclient.discovery.build("youtube", "v3", credentials=credentials)


def upload_video(youtube, video_data):
    """Uploads a video to YouTube."""
    request_body = {
        "snippet": {
            "title": video_data["Title"],
            "description": video_data["Description"],
            "tags": video_data["Tags"].split(","),
            "categoryId": video_data["Category"],
        },
        "status": {
            "privacyStatus": video_data["Privacy Status"],
            "publishAt": video_data["Publish At"],
        },
    }

    media = googleapiclient.http.MediaFileUpload(video_data["File Path"])

    response_upload = youtube.videos().insert(part="snippet,status", body=request_body, media_body=media).execute()

    youtube.thumbnails().set(videoId=response_upload["id"], media_body=video_data["Thumbnail Path"]).execute()


def main():
    """main function."""

    youtube = authenticate()
    df = pd.read_csv(Path("/path/to/yt-upload.csv"))

    for index, row in df.iterrows():
        logger.info(f"Uploading {row['Title']}...")
        upload_video(youtube, row)
        logger.info(f"Uploaded {row['Title']} successfully.")


if __name__ == "__main__":
    main()
