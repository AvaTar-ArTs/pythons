"""
Reddit Scraper

This module provides functionality for reddit scraper.

Author: Auto-generated
Date: 2025-11-01
"""

import os

import config
import praw
from redvid import Downloader

import logging

logger = logging.getLogger(__name__)


def download_vid(url, directory):  # Download reddit vid given URL and directory
    """download_vid function."""

    download = Downloader(url, max_q=True)
    download.path = directory
    download.download()
    logger.info(os.listdir(directory))

    """reddit_scraper function."""


def reddit_scraper(subreddit):  # pulls out top reddit posts
    logger.info("Logging into Reddit...")

    red = praw.Reddit(
        client_id=config.reddit_login["client_id"],
        client_secret=config.reddit_login["client_secret"],
        password=config.reddit_login["password"],
        user_agent=config.reddit_login["user_agent"],
        username=config.reddit_login["username"],
    )

    logger.info("Log in success! Retrieving post info...")

    sub = red.subreddit(subreddit).top("week", limit=25)

    output = []

    for i in sub:
        logger.info(f"{i.title}")
        if not i.stickied and not i.over_18:
            url = i.url
            if url.split(".")[0] != "https://v":
                continue
            title = i.title
            logger.info(
                "{}  {}  {}\n{}\n".format(title, i.subreddit, i.author.name, url)
            )
            output.append((url, title, i.author.name))

    return output
