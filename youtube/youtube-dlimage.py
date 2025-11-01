"""
Youtube Dlimage

This module provides functionality for youtube dlimage.

Author: Auto-generated
Date: 2025-11-01
"""

from pathlib import Path
import math
import time
import urllib.request

import keyboard
import praw
import requests
from InstagramAPI import InstagramAPI
from PIL import Image

import logging

logger = logging.getLogger(__name__)


# Constants
CONSTANT_100 = 100
CONSTANT_1000 = 1000
CONSTANT_1020 = 1020
CONSTANT_4000 = 4000


# put it IG username/password
api = InstagramAPI("username", "password")
api.login()


# make a reddit acount and look up how to find this stuff. its called PRAW
reddit = praw.Reddit(
    client_id="", client_secret="", username="", password="", user_agent="chrome"
)


def DLimage(url, filePath, fileName):
    """DLimage function."""

    fullPath = filePath + fileName + ".jpg"
    urllib.request.urlretrieve(url, fullPath)


# folder path to store downloaded images
filePath = ""

subreddit = reddit.subreddit("dankmemes")  # subreddit to take images from

# tags for IG post
captionTags = ""

# caption text for IG
captionText = "These images are from reddit."

waitTime = 2  # to prevent reddit badgateway error. DONt change

numRounds = CONSTANT_100  # how many posts

postFrequency = CONSTANT_4000  # how often to post in seconds.

numPics = 10  # how many pics per post. 2-10

for x in range(numRounds):
    new_memes = subreddit.rising(
        limit=numPics
    )  # .hot/.rising/.new   reddit sorting algorithm
    authors = []
    photoAlbum = []
    logger.info("Round/post number:", x)
    for subbmission in new_memes:
        if subbmission.is_self == True:  # checking if post is only text.
            logger.info("Post was text, skipping to next post.")
            continue
        else:
            pass
        url = subbmission.url
        time.sleep(waitTime)
        fileName = str(subbmission)
        fullPath = filePath + fileName + ".jpg"
        # logger.info(fullPath)
        time.sleep(waitTime)
        # logger.info(url)
        try:
            DLimage(url, filePath, fileName)
        except (OSError, IOError, FileNotFoundError):
            logger.info("scratch that, next post.")
            continue
        time.sleep(waitTime)
        author = str(subbmission.author)
        authors.append(author)
        time.sleep(waitTime)
        img = Image.open(fullPath)
        width, height = img.size
        img = img.resize((CONSTANT_1000, CONSTANT_1020), Image.NEAREST)  # image resize. width/height
        img = img.convert("RGB")
        img.save(fullPath)
        photoAlbum.append(
            {
                "type": "photo",
                "file": fullPath,
            }
        )

    authors = "".join(str(e + ", ") for e in authors)
    logger.info(photoAlbum)
    api.uploadAlbum(
        photoAlbum,
        caption=(
            captionText
            + Path("\n")
            + "Created by redditors: "
            + authors[0 : (len(authors) - 2)]
            + "."
            + Path("\n")
            + captionTags
        ),
    )
    time.sleep(postFrequency)
