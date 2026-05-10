# Load API keys from ~/.env.d/ (best practice - handles export statements, quotes, comments)
from pathlib import Path as PathLib

def load_env_d():
    """Load all .env files from ~/.env.d directory (sophisticated pattern from youtube-load.py)"""
    env_d_path = PathLib.home() / ".env.d"
    if env_d_path.exists():
        for env_file in env_d_path.glob("*.env"):
            try:
                with open(env_file) as f:
                    for line in f:
                        line = line.strip()
                        if line and not line.startswith("#") and "=" in line:
                            # Handle export statements
                            if line.startswith("export "):
                                line = line[7:]
                            key, value = line.split("=", 1)
                            key = key.strip()
                            value = value.strip().strip('"').strip("'")
                            # Skip source statements
                            if not key.startswith("source"):
                                os.environ[key] = value
            except Exception as e:
                # Logger not initialized yet, use print
                print(f"Warning: Error loading {env_file}: {e}")

load_env_d()

# Also load from ~/.env as fallback using dotenv
try:
    from dotenv import load_dotenv
    load_dotenv(os.path.expanduser("~/.env"))
except ImportError:
    pass

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
