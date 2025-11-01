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


# --- Analysis of the code structure and logic ---

# 1. Imports:
#    - The script imports necessary modules for Google API client, authentication, and OS operations.
#    - It assumes the googleapiclient and google_auth_oauthlib libraries are installed.

# 2. Constants:
#    - SCOPES: Defines the OAuth scope for uploading to YouTube.
#    - CLIENT_SECRETS_FILE: Path to the OAuth client secrets JSON file.
#    - API_SERVICE_NAME and API_VERSION: Used to build the YouTube API client.

# 3. Authentication Function:
def get_authenticated_service():
    """
    Authenticates the user via OAuth2 and returns an authorized YouTube Data API service object.
    - Uses InstalledAppFlow for local user authentication.
    - Credentials are obtained and used to build the API client.
    """
    flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
        CLIENT_SECRETS_FILE, SCOPES)
    credentials = flow.run_local_server(port=0)
    return googleapiclient.discovery.build(API_SERVICE_NAME, API_VERSION,
                                            credentials=credentials)

# 4. Video Upload Function:
def upload_video(youtube, file_path, title, description, category_id, keywords, privacy_status):
    """
    Uploads a video to YouTube using the provided parameters.
    - Constructs the request body with snippet and status.
    - Uses MediaFileUpload for resumable uploads.
    - Handles upload progress and errors.
    """
    body = {
        'snippet': {
            'title': title,
            'description': description,
            'categoryId': category_id,
            'tags': keywords
        },
        'status': {
            'privacyStatus': privacy_status
        }
    }

    media = googleapiclient.http.MediaFileUpload(file_path, mimetype='video/*', chunksize=CONSTANT_1024*CONSTANT_1024, resumable=True)

    request = youtube.videos().insert(
        part="snippet,status",
        body=body,
        media=media
    )

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

# 5. Main Execution Block:
if __name__ == "__main__":
    # The following block sets up video metadata and triggers the upload process.

    # VIDEO_FILE_PATH: Path to the video file to upload.
    # NOTE: The current value is wrapped in extra single quotes, which may cause a file not found error.
    VIDEO_FILE_PATH = "'/Users/steven/Movies/PROJECt2025-DoMinIon/TrumpsFreudianCollapse_TheConfessio2025-05-31.mp4'"  # Replace with your video file path

    # VIDEO_TITLE: Title of the YouTube video.
    VIDEO_TITLE = "TrumpsFreudianCollapse_TheConfession"

    # VIDEO_DESCRIPTION: Description of the video.
    # NOTE: The current value contains newlines and non-ASCII characters (emojis, curly quotes).
    #       The string is not properly terminated, which will cause a syntax error.
Keywords:

Trump accusations
Psychological projection
Political rhetoric analysis
Narcissistic behavior
Hidden confessions
Political psychology
Public opinion manipulation
Emotional rhetoric
Cognitive bias
Media literacy
Bullet Points:

Analyze Trump’s accusations as psychological projections 🧠
Explore the concept of projection in political rhetoric 📢
Understand how accusations reveal hidden insecurities 🤫
Discover the impact of Trump’s rhetoric on public opinion 🌍
Learn about the narcissistic verbal spiral 🔄
Examine how rhetoric can incite violence and unrest ⚠️
Recognize the power of emotional manipulation in politics 🎭
Understand cognitive biases and the backfire effect 🔍
Reflect on the human tendency to project insecurities 😔
Tags:
#Trump #Psychology #Projection #PoliticalRhetoric #Narcissism #PublicOpinion #MediaLiteracy #CognitiveBias #EmotionalManipulation #PoliticalAnalysis"
    VIDEO_CATEGORY_ID = "22"  # See https://developers.google.com/youtube/v3/docs/videoCategories/list
    VIDEO_KEYWORDS = ["automation", "youtube", "api"]
    VIDEO_PRIVACY_STATUS = "private"  # "public", "private", or "unlisted"

    # Authenticate and build the YouTube service
    youtube = get_authenticated_service()

    # Upload the video
    upload_video(youtube, VIDEO_FILE_PATH, VIDEO_TITLE, VIDEO_DESCRIPTION,
                 VIDEO_CATEGORY_ID, VIDEO_KEYWORDS, VIDEO_PRIVACY_STATUS)