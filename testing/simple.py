"""
Summary of simple.py

This module is part of the AVATARARTS ecosystem.
For more information about the AVATARARTS project, see the main documentation.
"""

from clips import *

videoclip = VideoFileClip("media/askreddit_submission_test0.mp4")
videoclip.audio = gen_background_audio_clip(videoclip.duration)
videoclip.to_videofile("temp/loop.mp4")
