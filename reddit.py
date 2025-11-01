"""
Reddit

This module provides functionality for reddit.

Author: Auto-generated
Date: 2025-11-01
"""

from moviepy.editor import *
import datetime as dt
import pandas as pd
import praw

import logging

logger = logging.getLogger(__name__)


# Constants
CONSTANT_188 = 188
CONSTANT_255 = 255


def comment_html(username, content):
    """comment_html function."""

    str = (
        "<!DOCTYPE html><html><head>"
        "<style>body {background-color: rgb(26, 26, 27);color: white;font-family: BentonSans, sans-serif;}.username {color: rgb(79, CONSTANT_188, CONSTANT_255);}.content {padding: 5px}.header {padding: 0 0 0 5px}</style>"
        "</head>"
        "<body><div><div class = 'header'><span class=username>"
        + username
        + "</span></div><div class = 'content'>"
        + content
        + "</div></div></body></html>"
    )
    return str

    """gen_comment_image function."""


def gen_comment_image(username, content, save_path):
    imgkit.from_string(
        comment_html("kindeep", "asdfasdfafg asgdfasdf sadgasdfewher sehagdsf"),
        save_path,
    )


logger.info("Subscribe or i'll end humanity.")

with open("reddit_secret.json") as f:
    secret = json.load(f)

reddit = praw.Reddit(
    client_id=secret["client_id"],
    client_secret=secret["client_secret"],
    user_agent=secret["user_agent"],
)

# logger.info(reddit.read_only)

for a_subreddit in reddit.subreddits.popular(limit=1):
    print(a_subreddit.display_name, "\n" + ("=" * len(a_subreddit.display_name)))
    for submission in a_subreddit.top(limit=10):
        logger.info(submission.title, "\n")


gen_comment_image("kindeep", "something", "media/test.png")
img_clip = ImageClip("media/test.png").set_duration(10)

imgs = ["media/test.png", "media/test.1.png"]

clips = [ImageClip(m).set_duration(2) for m in imgs]

concat_clip = concatenate_videoclips(clips, method="compose")
concat_clip.write_videofile("media/test.mp4", fps=24)
