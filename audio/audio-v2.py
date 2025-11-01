"""
Audio Test

This module provides functionality for audio test.

Author: Auto-generated
Date: 2025-11-01
"""

from clips import *

videoclip = VideoFileClip("media/askreddit_submission_test0.mp4")
videoclip.audio = gen_background_audio_clip(videoclip.duration)
videoclip.to_videofile('temp/loop.mp4')


