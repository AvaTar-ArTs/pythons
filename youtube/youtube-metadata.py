import csv
import os

from googleapiclient.discovery import build

import logging

logger = logging.getLogger(__name__)


# Securely load the API key
api_key = os.getenv("YOUTUBE_API_KEY")

# Set up YouTube Data API
youtube = build("youtube", "v3", developerKey=api_key)

# Retrieve channel's videos
videos = []
next_page_token = None
try:
    while True:
        request = youtube.search().list(
            part="snippet",
            channelId="UCDl7VmS3gD2BQBVZUlL21-A",
            maxResults=50,  # Max allowed value
            pageToken=next_page_token,
        )
        response = request.execute()
        videos.extend(response["items"])
        next_page_token = response.get("nextPageToken")
        if not next_page_token:
            break
except Exception as e:
    logger.info(f"An error occurred: {e}")

# Format data into CSV
csv_data = []
for video in videos:
    title = video["snippet"]["title"]
    description = video["snippet"]["description"]
    upload_date = video["snippet"]["publishedAt"]
    csv_data.append([title, description, upload_date])

# Save CSV
with open("youtube_videos.csv", "w", newline="", encoding="utf-8") as file:
    writer = csv.writer(file)
    writer.writerow(["Title", "Description", "Upload Date"])
    writer.writerows(csv_data)
