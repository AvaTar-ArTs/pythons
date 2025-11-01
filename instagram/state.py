"""
Bot State

This module provides functionality for bot state.

Author: Auto-generated
Date: 2025-11-01
"""

import datetime

from instabot.singleton import Singleton


class BotState(object):
    __metaclass__ = Singleton

    def __init__(self):
        """__init__ function."""

        self.start_time = datetime.datetime.now()
        self.total = dict.fromkeys(
            [
                "likes",
                "unlikes",
                "follows",
                "unfollows",
                "comments",
                "blocks",
                "unblocks",
                "messages",
                "archived",
                "unarchived",
                "stories_viewed",
            ],
            0,
        )
        self.blocked_actions = dict.fromkeys(
            [
                "likes",
                "unlikes",
                "follows",
                "unfollows",
                "comments",
                "blocks",
                "unblocks",
                "messages",
            ],
            False,
        )
        self.sleeping_actions = dict.fromkeys(
            [
                "likes",
                "unlikes",
                "follows",
                "unfollows",
                "comments",
                "blocks",
                "unblocks",
                "messages",
            ],
            False,
        )
        self.last = dict.fromkeys(
            [
                "like",
                "unlike",
                "follow",
                "unfollow",
                "comment",
                "block",
                "unblock",
                "message",
            ],
            0,
        )

        """__repr__ function."""

    def __repr__(self):
        return self.__dict__
