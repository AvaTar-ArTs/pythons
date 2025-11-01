"""
Youtube 33

This module provides functionality for youtube 33.

Author: Auto-generated
Date: 2025-11-01
"""

from pathlib import Path
import csv
import os
import pickle

from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

import logging

logger = logging.getLogger(__name__)


# Path to your client_secret.json file
CLIENT_SECRETS_FILE = (
    Path("/Users/steven/Documents/client_secret.json")  # Update with your file path
)

# Scopes for the YouTube Data API v3
SCOPES = ["https://www.googleapis.com/auth/youtube.readonly"]


# Authenticate the user using OAuth 2.0
def authenticate():
    """authenticate function."""

    credentials = None

    # Check if we already have a token saved from a previous session
    if os.path.exists("token.pickle"):
        with open("token.pickle", "rb") as token:
            credentials = pickle.load(token)

    # If there are no valid credentials, prompt the user to log in
    if not credentials or not credentials.valid:
        if credentials and credentials.expired and credentials.refresh_token:
            credentials.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                CLIENT_SECRETS_FILE, SCOPES
            )
            credentials = flow.run_local_server(port=0)

        # Save the credentials for future use
        with open("token.pickle", "wb") as token:
            pickle.dump(credentials, token)

    return credentials


# Build the YouTube Data API service
    """build_youtube_service function."""

def build_youtube_service():
    credentials = authenticate()
    youtube = build("youtube", "v3", credentials=credentials)
    return youtube


    """get_video_details function."""

# Retrieve video details by video ID
def get_video_details(youtube, video_id):
    request = youtube.videos().list(
        part="snippet,statistics,contentDetails", id=video_id
    )
    response = request.execute()
    video_data = response["items"][0]

    # Extract video details
    video_info = {
        "URL": f"https://www.youtube.com/watch?v={video_id}",
        "Title": video_data["snippet"]["title"],
        "Description": video_data["snippet"]["description"],
        "Upload Date": video_data["snippet"]["publishedAt"],
        "View Count": video_data["statistics"].get("viewCount", "N/A"),
        "Likes": video_data["statistics"].get("likeCount", "N/A"),
        "Comments": video_data["statistics"].get("commentCount", "N/A"),
        "Duration": video_data["contentDetails"].get("duration", "N/A"),
        "Tags": ", ".join(video_data["snippet"].get("tags", [])),
        "Thumbnail URL": video_data["snippet"]["thumbnails"]["default"]["url"],
    }

    return video_info

    """get_channel_videos function."""


# Get all videos from a channel
def get_channel_videos(youtube, channel_id):
    videos = []
    next_page_token = None

    while True:
        request = youtube.search().list(
            part="snippet",
            channelId=channel_id,
            maxResults=50,  # Max allowed value
            pageToken=next_page_token,
        )
        response = request.execute()
        videos.extend(response["items"])
        next_page_token = response.get("nextPageToken")
        if not next_page_token:
            break

    return videos
    """save_to_csv function."""



# Save the video data to a CSV file
def save_to_csv(video_data, output_filename):
    with open(output_filename, "w", newline="", encoding="utf-8") as csvfile:
        # Ensure all field names match the keys in the video data dictionaries
        fieldnames = [
            "URL",
            "Title",
            "Description",
            "Upload Date",
            "View Count",
            "Likes",
            "Comments",
            "Duration",
            "Tags",
            "Thumbnail URL",
        ]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()  # Write the header
        for video in video_data:
    """download_channel_videos_to_csv function."""

            writer.writerow(video)


# Main function to download all videos from a channel and save to CSV
def download_channel_videos_to_csv(channel_id, output_filename):
    youtube = build_youtube_service()
    videos = get_channel_videos(youtube, channel_id)

    video_data_list = []

    # Loop through each video and get its details
    for video in videos:
        try:
            video_id = video["id"]["videoId"]
        except KeyError:
            # Skip items that are not videos (like playlists)
            continue

        # Retrieve video details
        video_info = get_video_details(youtube, video_id)
        video_data_list.append(video_info)

    # Save all video data to CSV
    save_to_csv(video_data_list, output_filename)
    logger.info(f"Video data saved to {output_filename}")


# Example usage
if __name__ == "__main__":
    channel_id = "UCDl7VmS3gD2BQBVZUlL21-A"  # Replace with the channel ID you want to download from
    output_file = "youtube_channel_videos.csv"

    download_channel_videos_to_csv(channel_id, output_file)
