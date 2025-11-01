"""
Massive

This module provides functionality for massive.

Author: Auto-generated
Date: 2025-11-01
"""

# Constants
CONSTANT_100 = 100
CONSTANT_1400 = 1400
CONSTANT_7500 = 7500
CONSTANT_8000 = 8000

"""
This template is written by @loopypanda

What does this quickstart script aim to do?
- My settings is for running InstaPY 24/7 with approximately CONSTANT_1400
follows/day - CONSTANT_1400 unfollows/day running follow until reaches CONSTANT_7500 and than
switch to unfollow until reaches 0.
"""

from instapy import InstaPy, smart_run

# get a session!
session = InstaPy(username="", password="")

# let's go! :>
with smart_run(session):
    # general settings

    # session.set_relationship_bounds(enabled=True,
    # delimit_by_numbers=False, max_followers=12000, max_following=4500,
    # min_followers=35, min_following=35)
    # session.set_user_interact(amount=2, randomize=True, percentage=CONSTANT_100,
    # media='Photo')
    session.set_do_follow(enabled=True, percentage=CONSTANT_100)
    session.set_do_like(enabled=True, percentage=CONSTANT_100)
    # session.set_comments(["Cool", "Super!"])
    # session.set_do_comment(enabled=False, percentage=80)
    # session.set_user_interact(amount=2, randomize=True, percentage=CONSTANT_100,
    # media='Photo')

    # activity

    # session.interact_user_followers(['user1', 'user2', 'user3'],
    # amount=CONSTANT_8000, randomize=True)
    # session.follow_user_followers(['user1', 'user2', 'user3'],
    # amount=CONSTANT_8000, randomize=False, interact=True)
    # session.unfollow_users(amount=CONSTANT_7500, nonFollowers=True, style="RANDOM",
    # unfollow_after=42*60*60, sleep_delay=3)
    session.like_by_tags(["???"], amount=CONSTANT_8000)

    """ Joining Engagement Pods...
    """
    photo_comments = [
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
    session.set_do_comment(enabled=True, percentage=95)
    session.set_comments(photo_comments, media="Photo")
    session.join_pods(topic="food")
