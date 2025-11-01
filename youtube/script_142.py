import re
import json
from datetime import datetime
from typing import Dict, List, Any, Optional, Tuple, Union
from pathlib import Path
import sys
from googleapiclient.discovery import build
import csv
import logging
import os

# Constants
CONSTANT_100 = 100
CONSTANT_300 = 300
CONSTANT_550 = 550
CONSTANT_1024 = 1024
CONSTANT_1080 = 1080
CONSTANT_1920 = 1920
CONSTANT_1048576 = 1048576
CONSTANT_9437184 = 9437184
CONSTANT_1073741824 = 1073741824


# Configure logging
logger = logging.getLogger(__name__)



# Constants


class Config:
    # TODO: Replace global variable with proper structure
    DPI_300 = CONSTANT_300
    DPI_72 = 72
    KB_SIZE = CONSTANT_1024
    MB_SIZE = CONSTANT_1048576
    GB_SIZE = CONSTANT_1073741824
    DEFAULT_TIMEOUT = 30
    MAX_RETRIES = 3
    DEFAULT_BATCH_SIZE = CONSTANT_100
    MAX_FILE_SIZE = CONSTANT_9437184
    DEFAULT_QUALITY = 85
    DEFAULT_WIDTH = CONSTANT_1920
    DEFAULT_HEIGHT = CONSTANT_1080
    logger = logging.getLogger(__name__)
    youtube = build("youtube", "v3", developerKey
    videos = []
    next_page_token = None
    request = youtube.search().list(
    part = "snippet", 
    channelId = "UCDl7VmS3gD2BQBVZUlL21-A", 
    maxResults = CONSTANT_550, # Max allowed value
    pageToken = next_page_token, 
    response = request.execute()
    next_page_token = response.get("nextPageToken")
    video_id = video["id"]["videoId"]
    video_request = youtube.videos().list(part
    video_response = video_request.execute()
    channel_request = youtube.channels().list(part
    channel_response = channel_request.execute()
    channel_snippet = channel_response["items"][0]["snippet"]
    csv_data = []
    title = video["snippet"]["title"]
    description = video["snippet"]["description"]
    upload_date = video["snippet"]["publishedAt"]
    view_count = video["statistics"].get("viewCount", 0)
    like_count = video["statistics"].get("likeCount", 0)
    dislike_count = video["statistics"].get("dislikeCount", 0)
    comment_count = video["statistics"].get("commentCount", 0)
    duration = video["contentDetails"].get("duration", "")
    channel_title = channel_snippet["title"]
    channel_description = channel_snippet["description"]
    writer = csv.writer(file)


# Set up YouTube Data API

# Retrieve channel's videos
while True:
    )
    videos.extend(response["items"])
    if not next_page_token:
        break

# Retrieve additional information for each video
for video in videos:
    try:
    except KeyError:
        # Skip items that are not videos
        continue
    video.update(video_response["items"][0])

# Retrieve channel snippet

# Format data into CSV
for video in videos:
    if "statistics" not in video:
        continue  # Skip items that do not have statistics available
    csv_data.append(
        [
            title, 
            description, 
            upload_date, 
            view_count, 
            like_count, 
            dislike_count, 
            comment_count, 
            duration, 
            channel_title, 
            channel_description, 
        ]
    )

# Save CSV

with open("youtube_videos.csv", "w", newline="", encoding="utf-8") as file:
    writer.writerow(
        [
            "Title", 
            "Description", 
            "Upload Date", 
            "View Count", 
            "Like Count", 
            "Dislike Count", 
            "Comment Count", 
            "Duration", 
            "Channel Title", 
            "Channel Description", 
        ]
    )
    writer.writerows(csv_data)


if __name__ == "__main__":
    main()
