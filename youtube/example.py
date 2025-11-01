"""
Example

This module provides functionality for example.

Author: Auto-generated
Date: 2025-11-01
"""

from twitchtube.video import make_video

import os
from dotenv import load_dotenv

# Constants
CONSTANT_1080 = 1080
CONSTANT_1920 = 1920


load_dotenv()

make_video(
    data=["c xQcOW", "game Just Chatting"],
    client_id=os.getenv("TWITCH_CLIENT_ID"),
    oauth_token=os.getenv("TWITCH_OAUTH_TOKEN"),
    video_length=10.5,
    resolution=(CONSTANT_1080, CONSTANT_1920),
    frames=60,
)
