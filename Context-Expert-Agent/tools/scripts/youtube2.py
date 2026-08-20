from googleapiclient.discovery import build

# Set up YouTube Data API
youtube = build("youtube", "v3", developerKey="AIzaSyC08MXHwy-tkAwAhvW0TumdKJmSfOJYFqw")

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
    video.update(video_response["items"][0])

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
    channel_title = channel_snippet["title"]
    channel_description = channel_snippet["description"]
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
import csv

with open("youtube_videos.csv", "w", newline="", encoding="utf-8") as file:
    writer = csv.writer(file)
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
