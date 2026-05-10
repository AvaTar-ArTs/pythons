import os

import google.oauth2.credentials
import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors
from googleapiclient.http import MediaFileUpload

# --- Configuration ---
CLIENT_SECRETS_FILE = "/Users/steven/Movies/PROJECt2025-DoMinIon/mp4/client_secret.json"  # Path to your downloaded credentials.json
SCOPES = ["https://www.googleapis.com/auth/youtube.upload"]  # YouTube Upload Scope
API_SERVICE_NAME = "youtube"
API_VERSION = "v3"


def get_authenticated_service():
    """
    Authenticates and authorizes the user. Returns the YouTube Data API service object.
    """
    # 1. Load existing credentials, if they exist
    creds = None
    if os.path.exists("token.json"):  # File to store refresh token and access token
        creds = google.oauth2.credentials.Credentials.from_authorized_user_file(
            "token.json", SCOPES
        )

    # 2. If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            try:
                creds.refresh(google.auth.transport.requests.Request())
            except Exception as e:
                print(f"Error refreshing credentials: {e}")  # Detailed error message
                os.remove("token.json")  # Remove invalid token file
                creds = None  # Force re-authorization
        else:
            flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
                CLIENT_SECRETS_FILE, SCOPES
            )
            creds = flow.run_local_server(port=0)

        # 3. Save the credentials for the next run
        with open("token.json", "w") as token:
            token.write(creds.to_json())

    return googleapiclient.discovery.build(
        API_SERVICE_NAME, API_VERSION, credentials=creds
    )


def upload_video(:
    youtube, video_file_path, title, description, category_id, keywords, privacy_status
):
    """
    Uploads a video to YouTube.

    Args:
        youtube: Authenticated YouTube Data API service object.
        video_file_path: Path to the video file.
        title: Title of the video.
        description: Description of the video.
        category_id: YouTube video category ID (e.g., 22 for People & Blogs).
        keywords: Comma-separated string of keywords.
        privacy_status: "public", "private", or "unlisted".
    """
    body = {
        "snippet": {
            "category_id": category_id,
            "title": title,
            "description": description,
            "tags": keywords.split(","),  # Split keywords into a list
        },
        "status": {"privacyStatus": privacy_status},
    }

    # Use resumable upload for larger files
    media = MediaFileUpload(
        video_file_path, mimetype="video/*", resumable=True
    )  # Mimetype wildcard

    request = youtube.videos().insert(part="snippet,status", body=body, media=media)

    response = None  # Initialize response

    try:  # Handle potential upload errors gracefully.
        while response is None:
            status, response = request.next_chunk()
            if status:
                print(f"Uploaded {int(status.progress() * 100)}%")
        print(f"Video uploaded successfully! Video ID: {response['id']}")

    except googleapiclient.errors.HttpError as e:
        print(f"An HTTP error occurred: {e}")  # Provide specific error details

    except Exception as e:
        print(f"An unexpected error occurred during upload: {e}")


def main():
    """
    Main function to orchestrate the authentication and video upload.
    """

    #  Video details (Customize these)
    VIDEO_FILE_PATH = "/Users/steven/Movies/PROJECt2025-DoMinIon/mp4/TheNewApostolicReformation_AThreat.mp4"  # Replace with your video file
    TITLE = "Unmasking the New Apostolic Reformation: A Rising Force in American Politics 🇺🇸o"  # Replace with your video title
    DESCRIPTION = "This is a description of my awesome video."  # Replace with your video description
    CATEGORY_ID = "22"  # Replace with the appropriate category ID.
    KEYWORDS = "video, awesome, fun"  # Replace with relevant keywords.
    PRIVACY_STATUS = "private"  # Can be "public", "private", or "unlisted"

    #  Error Handling: Check if the credentials file exists
    if not os.path.exists(CLIENT_SECRETS_FILE):
        print(f"Error: Credentials file '{CLIENT_SECRETS_FILE}' not found.")
        return  # Exit if credentials file is missing

    try:
        youtube = get_authenticated_service()
        upload_video(
            youtube,
            VIDEO_FILE_PATH,
            TITLE,
            DESCRIPTION,
            CATEGORY_ID,
            KEYWORDS,
            PRIVACY_STATUS,
        )

    except Exception as e:
        print(f"An error occurred: {e}")  # General error handling


if __name__ == "__main__":
    main()
