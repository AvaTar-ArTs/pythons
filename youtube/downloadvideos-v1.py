"""
Downloadvideos

This module provides functionality for downloadvideos.

Author: Auto-generated
Date: 2025-11-01
"""


import logging

logger = logging.getLogger(__name__)

"""
1. Download daily trending TikTok clips
"""

import os
import random
import string

from TikTokApi import TikTokApi

DAILY_TRENDING_DIR = r"directory location for downloaded tiktok videos"
verifyFp = "use s_v_web_id cookie from tiktok.com"
did = "".join(random.choice(string.digits) for num in range(19))

api = TikTokApi.get_instance(custom_verifyFp=verifyFp, use_test_endpoints=True)

tiktoks = api.trending()
video_bytes = api.get_Video_By_TikTok(tiktoks[0])


def download_tiktoks():
    """download_tiktoks function."""

    os.chdir(DAILY_TRENDING_DIR)
    for tiktok in tiktoks:
        video_bytes = api.get_Video_By_TikTok(tiktok)
        author = tiktok["author"]["uniqueId"]
        # logger.info(author)
        with open(str(author) + ".mp4", "wb") as o:
            o.write(video_bytes)
        logger.info("Downloading: " + tiktok["author"]["uniqueId"])
