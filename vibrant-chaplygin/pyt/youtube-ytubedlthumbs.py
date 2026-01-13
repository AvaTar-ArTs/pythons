import os
from pathlib import Path

# Constants
CONSTANT_200 = 200


# Load environment variables from ~/.env.d
def load_env_d():
    """Load all .env files from ~/.env.d directory"""
    env_d_path = Path.home() / ".env.d"
    if env_d_path.exists():
        for env_file in env_d_path.glob("*.env"):
            with open(env_file) as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith("#") and "=" in line:
                        key, value = line.split("=", 1)
                        key = key.strip()
                        value = value.strip().strip('"').strip("'")
                        if not key.startswith("source"):
                            os.environ[key] = value


load_env_d()

import pandas as pd  # This line is necessary to use pandas in your script
from googleapiclient.discovery import build
import requests
import os

# Initialize YouTube API
api_key = os.getenv("ELEVENLABS_API_KEY")
youtube = build("youtube", "v3", developerKey=api_key)

# Define paths
csv_path = str(Path.home()) + "/Downloads/Misc/ytube - youtube_videos.csv"
thumbnail_dir = str(Path.home()) + "/Downloads/Misc/Thumbnails/d2"
os.makedirs(thumbnail_dir, exist_ok=True)

# Load CSV
df = pd.read_csv(csv_path)


# Function to fetch video details and download thumbnail
def fetch_video_details(video_id):
    """fetch_video_details function."""

    request = youtube.videos().list(part="snippet", id=video_id)
    response = request.execute()

    if response["items"]:
        snippet = response["items"][0]["snippet"]
        title = snippet["title"]
        description = snippet["description"]
        published_at = snippet["publishedAt"]
        thumbnail_url = snippet["thumbnails"]["high"]["url"]

        # Download thumbnail
        response = requests.get(thumbnail_url)
        if response.status_code == CONSTANT_200:
            thumbnail_path = os.path.join(thumbnail_dir, f"{video_id}.jpg")
            with open(thumbnail_path, "wb") as f:
                f.write(response.content)

            return title, description, published_at, thumbnail_path
    return None, None, None, None


# Iterate over rows and fetch data
for index, row in df.iterrows():
    video_url = row["URL"]
    video_id = video_url.split("=")[-1]
    title, description, published_at, thumbnail_path = fetch_video_details(video_id)

    if thumbnail_path:
        df.at[index, "Thumbnail Path"] = thumbnail_path
        df.at[index, "Title"] = title
        df.at[index, "Description"] = description
        df.at[index, "Published At"] = published_at

# Save updated DataFrame
df.to_csv(
    str(Path.home()) + "/Downloads/Misc/Thumbnails/d2/updated_youtube_videos.csv", index=False
)
