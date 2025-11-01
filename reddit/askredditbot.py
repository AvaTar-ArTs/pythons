"""
Askredditbot 1

This module provides functionality for askredditbot 1.

Author: Auto-generated
Date: 2025-11-01
"""

import time

from AskReddit import gen_video_from_hot

delay = 60 * 60 * 12

while True:
    gen_video_from_hot()
    time.sleep(delay)
