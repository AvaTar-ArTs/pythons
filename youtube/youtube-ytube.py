import os
from dotenv import load_dotenv
from googleapiclient.discovery import build


# Load API keys from ~/.env.d/
from pathlib import Path as PathLib
from dotenv import load_dotenv

env_dir = PathLib.home() / ".env.d"
if env_dir.exists():
    for env_file in env_dir.glob("*.env"):
        load_dotenv(env_file)


# load_dotenv()  # Now using ~/.env.d/

# Set up YouTube Data API
youtube = build("youtube", "v3", developerKey=os.getenv("YOUTUBE_API_KEY"))

# Retrieve channel's videos
videos = []
next_page_token = None
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

# Retrieve additional information for each video
for video in videos:
    try:
        video_id = video["id"]["videoId"]
    except KeyError:
        # Skip items that are not videos
        continue
    video_request = youtube.videos().list(
        part="snippet,statistics,contentDetails", id=video_id
    )
    video_response = video_request.execute()
    video_data = video_response["items"][0]
    video["url"] = f"https://www.youtube.com/watch?v={video_id}"
    video.update(video_data)

# Retrieve channel snippet
channel_request = youtube.channels().list(part="snippet", id="UCDl7VmS3gD2BQBVZUlL21-A")
channel_response = channel_request.execute()
channel_snippet = channel_response["items"][0]["snippet"]

# Format data into CSV
csv_data = []
for video in videos:
    if "statistics" not in video:
        continue  # Skip items that do not have statistics available
    title = video["snippet"]["title"]
    description = video["snippet"]["description"]
    upload_date = video["snippet"]["publishedAt"]
    view_count = video["statistics"].get("viewCount", 0)
    like_count = video["statistics"].get("likeCount", 0)
    dislike_count = video["statistics"].get("dislikeCount", 0)
    comment_count = video["statistics"].get("commentCount", 0)
    duration = video["contentDetails"].get("duration", "")
    url = video.get("url", "")
    csv_data.append([url, title, description, upload_date, view_count, duration])

# Save CSV
import csv

with open("youtube_videos.csv", "w", newline="", encoding="utf-8") as file:
    writer = csv.writer(file)
    writer.writerow(
        ["URL", "Title", "Description", "Upload Date", "View Count", "Duration"]
    )
    writer.writerows(csv_data)
