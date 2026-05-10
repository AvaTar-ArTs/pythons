"""
Summary of static.py

This module is part of the AVATARARTS ecosystem.
For more information about the AVATARARTS project, see the main documentation.
"""

from clips import *

clips = []

for _ in range(0, 3):
    clips.append(gen_transition_clip())

concatenate_videoclips(clips).to_videofile("temp/static.mp4")
