"""
Reddit Video Maker Examples Youtube Tool

This module provides functionality for reddit video maker examples youtube tool.

Author: Auto-generated
Date: 2025-11-01
"""

import sys

import praw

import logging

logger = logging.getLogger(__name__)


sys.path.append("../")
import config


# Main driver function for software
def main() -> int:
    """main function."""

    # Creating a reddit api instance
    reddit = praw.Reddit(
        client_id=config.PRAW_CONFIG["client_id"],
        client_secret=config.PRAW_CONFIG["client_secret"],
        user_agent=config.PRAW_CONFIG["user_agent"],
    )

    # Looping a subreddit
    for submission in reddit.subreddit("learnpython").hot(limit=10):
        logger.info(submission.title)

    return 0


# Calling the main function
if __name__ == "__main__":
    exit(main())
