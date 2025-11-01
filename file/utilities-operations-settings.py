"""
Utilities File Operations Settings 7

This module provides functionality for utilities file operations settings 7.

Author: Auto-generated
Date: 2025-11-01
"""

from pathlib import Path

# Constants
CONSTANT_600 = 600
CONSTANT_720 = 720
CONSTANT_1280 = 1280


subreddits = [
    "AmItheAsshole",
    "antiwork",
    "AskMen",
    "ChoosingBeggars",
    "hatemyjob",
    "NoStupidQuestions",
    "pettyrevenge",
    "Showerthoughts",
    "TooAfraidToAsk",
    "TwoXChromosomes",
    "unpopularopinion",
]

max_video_length = CONSTANT_600  # Seconds
comment_limit = CONSTANT_600

assets_directory = "assets"
audio_directory = str(Path("temp"))

background_directory = str(Path(assets_directory, "backgrounds"))
background_opacity = 0.5
background_volume = 0.5

video_height = CONSTANT_720
video_width = CONSTANT_1280
clip_size = (video_width, video_height)

disablecompile = False
disableupload = False

enable_overlay = True

fonts_directory = str(Path(assets_directory, "fonts"))
image_backgrounds_directory = str(Path(assets_directory, "image_backgrounds"))
images_directory = str(Path(assets_directory, "images"))
thumbnails_directory = str(Path(assets_directory, "images"))

pause = 1  # Pause after speech
soundeffects_directory = str(Path(assets_directory, "soundeffects"))

text_bg_color = "#1A1A1B"
text_bg_opacity = 1
text_color = "white"
text_font = "Verdana-Bold"
text_fontsize = 32

download_enabled = True
