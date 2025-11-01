"""
3. Upload video to YouTube
"""

import datetime
import os

from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload


def upload_compilation(video_file, video_title, video_desc):
    CLIENT_SECRET_FILE = os.getenv("GOOGLE_CLIENT_SECRET", "client_secrets.json")
    SCOPES = ["https://www.googleapis.com/auth/youtube.upload"]
    flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRET_FILE, SCOPES)
    credentials = flow.run_console()
    youtube = build("youtube", "v3", credentials=credentials)

    now = datetime.datetime.now()
    upload_date_time = (
        datetime.datetime(
            now.year, now.month, now.day, now.hour, now.minute, int(now.second)
        ).isoformat()
        + ".000Z"
    )

    request_body = {
        "snippet": {
            "category": 19,
            "title": video_title,
            "description": video_desc,
            "tags": ["Python", "YouTube API", "Google"],
        },
        "status": {
            "privacyStatus": "public",
            "publishAt": upload_date_time,
            "selfDeclaredMadeForKids": False,
        },
        "notifySubscribers": False,
    }

    mediaFile = MediaFileUpload(video_file)

    response_upload = (
        youtube.videos()
        .insert(part="snippet,status", body=request_body, media_body=mediaFile)
        .execute()
    )
