"""
Script 216

This module provides functionality for script 216.

Author: Auto-generated
Date: 2025-11-01
"""

from instapy import InstaPy

# Constants
CONSTANT_100 = 100


session = InstaPy(username="your username here...", password="your password here...")
session.login()

# following section
session.set_do_follow(True, percentage=50, times=1)


# comment section
session.set_do_comment(True, percentage=CONSTANT_100)
session.set_comments(["I love your post @{}!"])

# like section
session.like_by_tags(["javascript", "python"], amount=3)
session.set_dont_like(["naked", "nsfw", "sex"])


session.end()
