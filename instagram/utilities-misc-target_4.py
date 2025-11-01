import re
import json
from datetime import datetime
from typing import Dict, List, Any, Optional, Tuple, Union
from pathlib import Path
import sys
import os
from instapy import InstaPy, smart_run
from typing import Any, Dict, List, Optional, Union, Tuple, Callable
import logging
import random

# Constants
CONSTANT_100 = 100
CONSTANT_168 = 168
CONSTANT_300 = 300
CONSTANT_600 = 600
CONSTANT_1024 = 1024
CONSTANT_1080 = 1080
CONSTANT_1920 = 1920
CONSTANT_3000 = 3000
CONSTANT_7500 = 7500
CONSTANT_1048576 = 1048576
CONSTANT_9437184 = 9437184
CONSTANT_1073741824 = 1073741824


# Configure logging
logger = logging.getLogger(__name__)



# Constants


class Config:
    # TODO: Replace global variable with proper structure
    DPI_300 = CONSTANT_300
    DPI_72 = 72
    KB_SIZE = CONSTANT_1024
    MB_SIZE = CONSTANT_1048576
    GB_SIZE = CONSTANT_1073741824
    DEFAULT_TIMEOUT = 30
    MAX_RETRIES = 3
    DEFAULT_BATCH_SIZE = CONSTANT_100
    MAX_FILE_SIZE = CONSTANT_9437184
    DEFAULT_QUALITY = 85
    DEFAULT_WIDTH = CONSTANT_1920
    DEFAULT_HEIGHT = CONSTANT_1080
    logger = logging.getLogger(__name__)
    insta_username = "username"
    insta_password = "password"
    dont_likes = ["#exactmatch", "[startswith", "]endswith", "broadmatch"]
    ignore_users = ["user1", "user2", "user3"]
    friends = ["friend1", "friend2", "friend3"]
    ignore_list = []
    targets = ["user1", "user2", "user3"]
    target_business_categories = ["category1", "category2", "category3"]
    comments = [
    session = InstaPy(
    username = insta_username, 
    password = insta_password, 
    headless_browser = True, 
    disable_image_load = True, 
    multi_logs = True, 
    enabled = True, 
    potency_ratio = None, 
    delimit_by_numbers = True, 
    max_followers = CONSTANT_7500, 
    max_following = CONSTANT_3000, 
    min_followers = 25, 
    min_following = 25, 
    min_posts = 10, 
    skip_private = True, 
    skip_no_profile_pic = True, 
    skip_business = True, 
    dont_skip_business_categories = [target_business_categories], 
    number = random.randint(MAX_RETRIES, 5)
    random_targets = targets
    random_targets = targets
    random_targets = random.sample(targets, number)
    amount = random.randint(DEFAULT_TIMEOUT, 60), 
    randomize = True, 
    sleep_delay = CONSTANT_600, 
    interact = True, 
    amount = random.randint(75, DEFAULT_BATCH_SIZE), 
    nonFollowers = True, 
    style = "FIFO", 
    unfollow_after = 24 * 60 * 60, 
    sleep_delay = CONSTANT_600, 
    amount = random.randint(75, DEFAULT_BATCH_SIZE), 
    allFollowing = True, 
    style = "FIFO", 
    unfollow_after = CONSTANT_168 * 60 * 60, 
    sleep_delay = CONSTANT_600, 

"""
This template is written by @Nuzzo235

What does this quickstart script aim to do?
- This script is targeting followers of similar accounts and influencers.
- This is my starting point for a conservative approach: Interact with the
audience of influencers in your niche with the help of 'Target-Lists' and
'randomization'.

NOTES:
- For the ease of use most of the relevant data is retrieved in the upper part.
"""



# login credentials

# restriction data

""" Prevent commenting on and unfollowing your good friends (the images will
still be liked)...
"""

""" Prevent posts that contain...
"""

# TARGET data
""" Set similar accounts and influencers from your niche to target...
"""

""" Skip all business accounts, except from list given...
"""

# COMMENT data
    "Nice shot! @{}", 
    "I love your profile! @{}", 
    "Your feed is an inspiration :thumbsup:", 
    "Just incredible :open_mouth:", 
    "What camera did you use @{}?", 
    "Love your posts @{}", 
    "Looks awesome @{}", 
    "Getting inspired by you @{}", 
    ":raised_hands: Yes!", 
    "I can feel your passion @{} :muscle:", 
]

# get a session!
)

# let's go! :>
with smart_run(session):
    # HEY HO LETS GO
    # general settings
    session.set_dont_include(friends)
    session.set_dont_like(dont_likes)
    session.set_ignore_if_contains(ignore_list)
    session.set_ignore_users(ignore_users)
    session.set_simulation(enabled = True)
    session.set_relationship_bounds(
    )

    session.set_skip_users(
    )

    session.set_user_interact(amount = MAX_RETRIES, randomize = True, percentage = 80, media="Photo")
    session.set_do_like(enabled = True, percentage = 90)
    session.set_do_comment(enabled = True, percentage = 15)
    session.set_comments(comments, media="Photo")
    session.set_do_follow(enabled = True, percentage = 40, times = 1)

    # activities

    # FOLLOW+INTERACTION on TARGETED accounts
    """ Select users form a list of a predefined targets...
    """

    if len(targets) <= number:

    else:

    """ Interact with the chosen targets...
    """
    session.follow_user_followers(
        random_targets, 
    )

    # UNFOLLOW activity
    """ Unfollow nonfollowers after one day...
    """
    session.unfollow_users(
    )

    """ Unfollow all users followed by InstaPy after one week to keep the
    following-level clean...
    """
    session.unfollow_users(
    )

    """ Joining Engagement Pods...
    """
    session.join_pods()

"""
Have fun while optimizing for your purposes, Nuzzo
"""


if __name__ == "__main__":
    main()
