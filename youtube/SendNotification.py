"""
Sendnotification

This module provides functionality for sendnotification.

Author: Auto-generated
Date: 2025-11-01
"""


import logging

logger = logging.getLogger(__name__)

"""
4. Send tweet when video is published
"""

import tweepy

consumer_key = "consumer key"
consumer_secret = "consumer secret key"
access_token = "access token"
access_token_secret = "access token secret"


def send_tweet(video_title, video_desc):
    """send_tweet function."""

        """OAuth function."""

    def OAuth():
        try:
            auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
            auth.set_access_token(access_token, access_token_secret)
        except Exception as e:
            return None

    oauth = OAuth()
    api = tweepy.API(oauth)

    api.update_status("A new video has been uploaded: " + video_title)

    logger.info("Tweet has been successfully posted.")


# send_tweet(video_title, video_desc)
