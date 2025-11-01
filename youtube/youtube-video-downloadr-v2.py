"""
Youtube Video Downloadr V2

This module provides functionality for youtube video downloadr v2.

Author: Auto-generated
Date: 2025-11-01
"""

from pathlib import Path
import googleapiclient.discovery
import googleapiclient.errors
import google_auth_oauthlib.flow
import google.auth.transport.requests
import os

import logging

logger = logging.getLogger(__name__)


# Constants
CONSTANT_100 = 100
CONSTANT_1024 = 1024


SCOPES = ["https://www.googleapis.com/auth/youtube.upload"]
CLIENT_SECRETS_FILE = Path(
    "/Users/steven/Documents/python/Youtube/client_secrets.json"
)  # Replace with your client secrets file
API_SERVICE_NAME = "youtube"
API_VERSION = "v3"


def get_authenticated_service():
    """Authenticates and returns the YouTube Data API service."""
    flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(CLIENT_SECRETS_FILE, SCOPES)
    credentials = flow.run_local_server(port=0)
    return googleapiclient.discovery.build(API_SERVICE_NAME, API_VERSION, credentials=credentials)


def upload_video(youtube, file_path, title, description, category_id, keywords, privacy_status):
    """Uploads a video to YouTube."""
    body = {
        "snippet": {"title": title, "description": description, "categoryId": category_id, "tags": keywords},
        "status": {"privacyStatus": privacy_status},
    }

    media = googleapiclient.http.MediaFileUpload(
        file_path, mimetype="video/*", chunksize=CONSTANT_1024 * CONSTANT_1024, resumable=True
    )

    request = youtube.videos().insert(part="snippet,status", body=body, media=media)

    response = None
    while response is None:
        try:
            status, response = request.next_chunk()
            if status:
                logger.info(f"Uploaded {int(status.progress() * CONSTANT_100)}%")
        except googleapiclient.errors.HttpError as e:
            logger.info(f"An HTTP error {e.resp.status} occurred:\n{e.content}")
            break
    if response:
        logger.info(f"Video uploaded successfully! Video ID: {response['id']}")


if __name__ == "__main__":
    # Set your video details here
    VIDEO_FILE_PATH = "your_video.mp4"  # Replace with your video file path
    VIDEO_TITLE = "My Automated Upload"
    VIDEO_DESCRIPTION = "This video was automatically uploaded using the YouTube Data API."
    VIDEO_CATEGORY_ID = "22"  # See https://developers.google.com/youtube/v3/docs/videoCategories/list
    VIDEO_KEYWORDS = ["automation", "youtube", "api"]
    VIDEO_PRIVACY_STATUS = "private"  # "public", "private", or "unlisted"

    # Authenticate and build the YouTube service
    youtube = get_authenticated_service()

    # Upload the video
    upload_video(
        youtube,
        VIDEO_FILE_PATH,
        VIDEO_TITLE,
        VIDEO_DESCRIPTION,
        VIDEO_CATEGORY_ID,
        VIDEO_KEYWORDS,
        VIDEO_PRIVACY_STATUS,
    )
