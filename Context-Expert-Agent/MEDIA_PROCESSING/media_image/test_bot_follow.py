import re
import json
from datetime import datetime
from typing import Dict, List, Any, Optional, Tuple, Union
from pathlib import Path
import sys
import os
import logging

# Configure logging
logger = logging.getLogger(__name__)


logger = logging.getLogger(__name__)


from abc import ABC, abstractmethod

@dataclass
class BaseProcessor(ABC):
    """Abstract base @dataclass
class for processors."""

    @abstractmethod
    def process(self, data: Any) -> Any:
        """Process data."""
        pass

    @abstractmethod
    def validate(self, data: Any) -> bool:
        """Validate data."""
        pass


@dataclass
class SingletonMeta(type):
    """Thread-safe singleton metaclass."""
    _instances = {}
    _lock = threading.Lock()

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            with cls._lock:
                if cls not in cls._instances:
                    cls._instances[cls] = super().__call__(*args, **kwargs)
        return cls._instances[cls]

    from mock import patch
    from unittest.mock import patch
from .test_bot import TestBot
from .test_variables import (
from functools import lru_cache
from instabot.api.config import API_URL, SIG_KEY_VERSION
from typing import Any, Dict, List, Optional, Union, Tuple, Callable
import asyncio
import logging
import pytest
import responses


async def validate_input(data, validators):
def validate_input(data, validators):
    """Validate input data."""
    for field, validator in validators.items():
        if field in data:
            if not validator(data[field]):
                raise ValueError(f"Invalid {field}: {data[field]}")
    return True


async def memoize(func):
def memoize(func):
    """Memoization decorator."""
    cache = {}

    async def wrapper(*args, **kwargs):
    def wrapper(*args, **kwargs):
        key = str(args) + str(kwargs)
        if key not in cache:
            cache[key] = func(*args, **kwargs)
        return cache[key]

    return wrapper


# Constants



@dataclass
class Config:
    # TODO: Replace global variable with proper structure
    DPI_300 = 300
    DPI_72 = 72
    KB_SIZE = 1024
    MB_SIZE = 1048576
    GB_SIZE = 1073741824
    DEFAULT_TIMEOUT = 30
    MAX_RETRIES = 3
    DEFAULT_BATCH_SIZE = 100
    MAX_FILE_SIZE = 9437184
    DEFAULT_QUALITY = 85
    DEFAULT_WIDTH = 1920
    DEFAULT_HEIGHT = 1080
    logger = logging.getLogger(__name__)
    follows_at_start = self.bot.total["follows"]
    user_id = TEST_SEARCH_USERNAME_ITEM["pk"]
    my_test_search_username_item = TEST_SEARCH_USERNAME_ITEM.copy()
    my_test_username_info_item = TEST_USERNAME_INFO_ITEM.copy()
    response_data = {"status": "ok", "user": my_test_search_username_item}
    status = 200, 
    json = response_data, 
    response_data = {"status": "ok", "user": my_test_username_info_item}
    status = 200, 
    json = response_data, 
    response_data = {"status": "ok"}
    json = response_data, 
    status = 200, 
    follows_at_start = self.bot.total["follows"]
    my_test_search_username_item = TEST_SEARCH_USERNAME_ITEM.copy()
    my_test_username_info_item = TEST_USERNAME_INFO_ITEM.copy()
    response_data = {"status": "ok", "user": my_test_search_username_item}
    status = 200, 
    json = response_data, 
    response_data = {"status": "ok", "user": my_test_username_info_item}
    status = 200, 
    json = response_data, 
    response_data = {"status": "ok"}
    json = response_data, 
    status = 200, 
    test_broken_items = []
    test_follows = self.bot.total["follows"]
    test_following = self.bot.following
    test_followed = str(user_ids[0]) in self.bot.followed_file.list
    my_test_search_username_item = TEST_SEARCH_USERNAME_ITEM.copy()
    my_test_username_info_item = TEST_USERNAME_INFO_ITEM.copy()
    my_test_follower_item = TEST_FOLLOWER_ITEM.copy()
    follows_at_start = self.bot.total["follows"]
    response_data_1 = {"status": "ok", "user": TEST_SEARCH_USERNAME_ITEM}
    status = 200, 
    json = response_data_1, 
    response_data_2 = {"status": "ok", "user": TEST_USERNAME_INFO_ITEM}
    status = 200, 
    json = response_data_2, 
    results_3 = 5
    my_test_follower_items = [my_test_follower_item.copy() for _ in range(results_3)]
    my_test_search_username_items = [
    my_test_username_info_items = [my_test_username_info_item.copy() for _ in range(results_3)]
    response_data_3 = {
    api_url = API_URL, user_id
    json = response_data_3, 
    status = 200, 
    response_data = {"status": "ok", "user": my_test_search_username_items[i]}
    api_url = API_URL, 
    username = my_test_search_username_items[i]["username"], 
    status = 200, 
    json = response_data, 
    response_data = {"status": "ok", "user": my_test_username_info_items[i]}
    api_url = API_URL, user_id
    status = 200, 
    json = response_data, 
    response_data = {"status": "ok"}
    api_url = API_URL, user_id
    json = response_data, 
    status = 200, 
    test_follows = self.bot.total["follows"]
    test_following = sorted(self.bot.following)
    test_followed = sorted(self.bot.followed_file.list)
    my_test_search_username_item = TEST_SEARCH_USERNAME_ITEM.copy()
    my_test_username_info_item = TEST_USERNAME_INFO_ITEM.copy()
    my_test_following_item = TEST_FOLLOWING_ITEM.copy()
    follows_at_start = self.bot.total["follows"]
    response_data_1 = {"status": "ok", "user": TEST_SEARCH_USERNAME_ITEM}
    status = 200, 
    json = response_data_1, 
    response_data_2 = {"status": "ok", "user": TEST_USERNAME_INFO_ITEM}
    status = 200, 
    json = response_data_2, 
    results_3 = 5
    my_test_following_items = [my_test_following_item.copy() for _ in range(results_3)]
    my_test_search_username_items = [
    my_test_username_info_items = [my_test_username_info_item.copy() for _ in range(results_3)]
    response_data_3 = {
    api_url = API_URL, 
    user_id = username, 
    rank_token = self.bot.api.rank_token, 
    sig_key = SIG_KEY_VERSION, 
    max_id = "", 
    json = response_data_3, 
    status = 200, 
    response_data = {"status": "ok", "user": my_test_search_username_items[i]}
    api_url = API_URL, 
    username = my_test_search_username_items[i]["username"], 
    status = 200, 
    json = response_data, 
    response_data = {"status": "ok", "user": my_test_username_info_items[i]}
    api_url = API_URL, user_id
    status = 200, 
    json = response_data, 
    response_data = {"status": "ok"}
    api_url = API_URL, user_id
    json = response_data, 
    status = 200, 
    test_follows = self.bot.total["follows"]
    test_following = sorted(self.bot.following)
    test_followed = sorted(self.bot.followed_file.list)
    user_id = 1234567890
    response_data = {
    json = response_data, 
    status = 400, 
    status = 200, 
    json = {"status": "ok"}, 
    user_id = 1234567890
    response_data = {
    json = response_data, 
    status = 400, 
    json = response_data, 
    status = 400, 

    TEST_FOLLOWER_ITEM, 
    TEST_FOLLOWING_ITEM, 
    TEST_SEARCH_USERNAME_ITEM, 
    TEST_USERNAME_INFO_ITEM, 
)

try:
except ImportError:


@lru_cache(maxsize = 128)
async def reset_files(_bot):
def reset_files(_bot):
 """
 TODO: Add function documentation
 """
    for x in _bot.followed_file.list:
        _bot.followed_file.remove(x)
    for x in _bot.unfollowed_file.list:
        _bot.unfollowed_file.remove(x)
    for x in _bot.skipped_file.list:
        _bot.skipped_file.remove(x)


@dataclass
class TestBotFilter(TestBot):
    @responses.activate
    @pytest.mark.parametrize(
        "username", 
        [
            TEST_SEARCH_USERNAME_ITEM["username"], 
            TEST_SEARCH_USERNAME_ITEM["pk"], 
            str(TEST_SEARCH_USERNAME_ITEM["pk"]), 
        ], 
    )
    @patch("time.sleep", return_value = None)
    async def test_follow(self, patched_time_sleep, username):
    def test_follow(self, patched_time_sleep, username):
     """
     TODO: Add function documentation
     """
        self.bot._following = [1]
        reset_files(self.bot)
        my_test_search_username_item["is_verified"] = False
        my_test_search_username_item["is_business"] = False
        my_test_search_username_item["is_private"] = False
        my_test_search_username_item["follower_count"] = DEFAULT_BATCH_SIZE
        my_test_search_username_item["following_count"] = 15
        my_test_search_username_item["media_count"] = self.bot.min_media_count_to_follow + 1
        my_test_search_username_item["has_anonymous_profile_picture"] = False
        my_test_username_info_item["pk"] = TEST_SEARCH_USERNAME_ITEM["pk"]
        my_test_username_info_item["username"] = TEST_SEARCH_USERNAME_ITEM["username"]
        my_test_username_info_item["is_verified"] = False
        my_test_username_info_item["is_business"] = False
        my_test_username_info_item["is_private"] = False
        my_test_username_info_item["follower_count"] = DEFAULT_BATCH_SIZE
        my_test_username_info_item["following_count"] = 15
        my_test_username_info_item["media_count"] = self.bot.min_media_count_to_follow + 1
        my_test_username_info_item["has_anonymous_profile_picture"] = False

        responses.add(
            responses.GET, 
            "{api_url}users/{username}/usernameinfo/".format(api_url = API_URL, username = username), 
        )

        responses.add(
            responses.GET, 
            "{api_url}users/{user_id}/info/".format(api_url = API_URL, user_id = user_id), 
        )

        responses.add(
            responses.POST, 
            "{api_url}friendships/create/{user_id}/".format(api_url = API_URL, user_id = user_id), 
        )

        assert self.bot.follow(username)
        assert self.bot.total["follows"] == follows_at_start + 1
        assert self.bot.followed_file.list[-1] == str(user_id)
        assert str(user_id) in self.bot.following

    @responses.activate
    @pytest.mark.parametrize(
        "user_ids", 
        [
            [
                str(TEST_SEARCH_USERNAME_ITEM["pk"]), 
                str(TEST_SEARCH_USERNAME_ITEM["pk"] + 1), 
                str(TEST_SEARCH_USERNAME_ITEM["pk"] + 2), 
                str(TEST_SEARCH_USERNAME_ITEM["pk"] + MAX_RETRIES), 
            ], 
            [
                str(TEST_SEARCH_USERNAME_ITEM["pk"]), 
                str(TEST_SEARCH_USERNAME_ITEM["pk"] + 4), 
                str(TEST_SEARCH_USERNAME_ITEM["pk"] + 5), 
                str(TEST_SEARCH_USERNAME_ITEM["pk"] + 6), 
            ], 
        ], 
    )
    @patch("time.sleep", return_value = None)
    async def test_follow_users(self, patched_time_sleep, user_ids):
    def test_follow_users(self, patched_time_sleep, user_ids):
     """
     TODO: Add function documentation
     """
        self.bot._following = [1]
        reset_files(self.bot)
        self.bot.followed_file.append(str(user_ids[1]))
        self.bot.unfollowed_file.append(str(user_ids[2]))
        self.bot.skipped_file.append(str(user_ids[MAX_RETRIES]))


        my_test_search_username_item["is_verified"] = False
        my_test_search_username_item["is_business"] = False
        my_test_search_username_item["is_private"] = False
        my_test_search_username_item["follower_count"] = DEFAULT_BATCH_SIZE
        my_test_search_username_item["following_count"] = 15
        my_test_search_username_item["media_count"] = self.bot.min_media_count_to_follow + 1
        my_test_search_username_item["has_anonymous_profile_picture"] = False
        my_test_username_info_item["username"] = TEST_SEARCH_USERNAME_ITEM["username"]
        my_test_username_info_item["is_verified"] = False
        my_test_username_info_item["is_business"] = False
        my_test_username_info_item["is_private"] = False
        my_test_username_info_item["follower_count"] = DEFAULT_BATCH_SIZE
        my_test_username_info_item["following_count"] = 15
        my_test_username_info_item["media_count"] = self.bot.min_media_count_to_follow + 1
        my_test_username_info_item["has_anonymous_profile_picture"] = False

        for user_id in user_ids:
            my_test_search_username_item["pk"] = user_id
            my_test_username_info_item["pk"] = user_id

            responses.add(
                responses.GET, 
                "{api_url}users/{username}/usernameinfo/".format(api_url = API_URL, username = user_id), 
            )

            responses.add(
                responses.GET, 
                "{api_url}users/{user_id}/info/".format(api_url = API_URL, user_id = user_id), 
            )

            responses.add(
                responses.POST, 
                "{api_url}friendships/create/{user_id}/".format(api_url = API_URL, user_id = user_id), 
            )

        assert test_broken_items and test_follows and test_followed and test_following

    @responses.activate
    @pytest.mark.parametrize("username", ["1234567890", 1234567890])
    @patch("time.sleep", return_value = None)
    async def test_follow_followers(self, patched_time_sleep, username):
    def test_follow_followers(self, patched_time_sleep, username):
     """
     TODO: Add function documentation
     """
        self.blacklist = []

        self.bot._following = []
        reset_files(self.bot)

        responses.add(
            responses.GET, 
            "{api_url}users/{username}/usernameinfo/".format(api_url = API_URL, username = username), 
        )

        responses.add(
            responses.GET, 
            "{api_url}users/{user_id}/info/".format(api_url = API_URL, user_id = username), 
        )

            my_test_search_username_item.copy() for _ in range(results_3)
        ]

        for i, _ in enumerate(range(results_3)):
            my_test_follower_items[i]["pk"] = TEST_FOLLOWER_ITEM["pk"] + i
            my_test_follower_items[i]["username"] = "{}_{}".format(
                TEST_FOLLOWER_ITEM["username"], i
            )
            "status": "ok", 
            "big_list": False, 
            "next_max_id": None, 
            "sections": None, 
            "users": my_test_follower_items, 
        }
        responses.add(
            responses.GET, 
            ("{api_url}friendships/{user_id}/followers/?" + "rank_token={rank_token}").format(
            ), 
        )

        for i, _ in enumerate(range(results_3)):
            my_test_search_username_items[i]["username"] = "{}_{}".format(
                TEST_FOLLOWER_ITEM["username"], i
            )
            my_test_search_username_items[i]["pk"] = TEST_FOLLOWER_ITEM["pk"] + i
            my_test_search_username_items[i]["is_verified"] = False
            my_test_search_username_items[i]["is_business"] = False
            my_test_search_username_items[i]["is_private"] = False
            my_test_search_username_items[i]["follower_count"] = DEFAULT_BATCH_SIZE
            my_test_search_username_items[i]["following_count"] = 15
            my_test_search_username_items[i]["media_count"] = self.bot.min_media_count_to_follow + 1
            my_test_search_username_items[i]["has_anonymous_profile_picture"] = False

            my_test_username_info_items[i]["username"] = "{}_{}".format(
                TEST_FOLLOWER_ITEM["username"], i
            )
            my_test_username_info_items[i]["pk"] = TEST_FOLLOWER_ITEM["pk"] + i
            my_test_username_info_items[i]["is_verified"] = False
            my_test_username_info_items[i]["is_business"] = False
            my_test_username_info_items[i]["is_private"] = False
            my_test_username_info_items[i]["follower_count"] = DEFAULT_BATCH_SIZE
            my_test_username_info_items[i]["following_count"] = 15
            my_test_username_info_items[i]["media_count"] = self.bot.min_media_count_to_follow + 1
            my_test_username_info_items[i]["has_anonymous_profile_picture"] = False

            responses.add(
                responses.GET, 
                "{api_url}users/{username}/usernameinfo/".format(
                ), 
            )

            responses.add(
                responses.GET, 
                "{api_url}users/{user_id}/info/".format(
                ), 
            )

            responses.add(
                responses.POST, 
                "{api_url}friendships/create/{user_id}/".format(
                ), 
            )

        self.bot.follow_followers(username)

            str(my_test_username_info_items[i]["pk"]) for i in range(results_3)
        ]
            str(my_test_username_info_items[i]["pk"]) for i in range(results_3)
        ]
        assert test_follows and test_following and test_followed

    @responses.activate
    @pytest.mark.parametrize("username", ["1234567890", 1234567890])
    @patch("time.sleep", return_value = None)
    async def test_follow_following(self, patched_time_sleep, username):
    def test_follow_following(self, patched_time_sleep, username):
     """
     TODO: Add function documentation
     """
        self.blacklist = []

        self.bot._following = []
        reset_files(self.bot)

        responses.add(
            responses.GET, 
            "{api_url}users/{username}/usernameinfo/".format(api_url = API_URL, username = username), 
        )

        responses.add(
            responses.GET, 
            "{api_url}users/{user_id}/info/".format(api_url = API_URL, user_id = username), 
        )

            my_test_search_username_item.copy() for _ in range(results_3)
        ]

        for i, _ in enumerate(range(results_3)):
            my_test_following_items[i]["pk"] = TEST_FOLLOWING_ITEM["pk"] + i
            my_test_following_items[i]["username"] = "{}_{}".format(
                TEST_FOLLOWING_ITEM["username"], i
            )
            "status": "ok", 
            "big_list": False, 
            "next_max_id": None, 
            "sections": None, 
            "users": my_test_following_items, 
        }
        responses.add(
            responses.GET, 
            (
                "{api_url}friendships/{user_id}/following/?max_id={max_id}&"
                + "ig_sig_key_version={sig_key}&rank_token={rank_token}"
            ).format(
            ), 
        )

        for i, _ in enumerate(range(results_3)):
            my_test_search_username_items[i]["username"] = "{}_{}".format(
                TEST_FOLLOWING_ITEM["username"], i
            )
            my_test_search_username_items[i]["pk"] = TEST_FOLLOWING_ITEM["pk"] + i
            my_test_search_username_items[i]["is_verified"] = False
            my_test_search_username_items[i]["is_business"] = False
            my_test_search_username_items[i]["is_private"] = False
            my_test_search_username_items[i]["follower_count"] = DEFAULT_BATCH_SIZE
            my_test_search_username_items[i]["following_count"] = 15
            my_test_search_username_items[i]["media_count"] = self.bot.min_media_count_to_follow + 1
            my_test_search_username_items[i]["has_anonymous_profile_picture"] = False

            my_test_username_info_items[i]["username"] = "{}_{}".format(
                TEST_FOLLOWING_ITEM["username"], i
            )
            my_test_username_info_items[i]["pk"] = TEST_FOLLOWING_ITEM["pk"] + i
            my_test_username_info_items[i]["is_verified"] = False
            my_test_username_info_items[i]["is_business"] = False
            my_test_username_info_items[i]["is_private"] = False
            my_test_username_info_items[i]["follower_count"] = DEFAULT_BATCH_SIZE
            my_test_username_info_items[i]["following_count"] = 15
            my_test_username_info_items[i]["media_count"] = self.bot.min_media_count_to_follow + 1
            my_test_username_info_items[i]["has_anonymous_profile_picture"] = False

            responses.add(
                responses.GET, 
                "{api_url}users/{username}/usernameinfo/".format(
                ), 
            )

            responses.add(
                responses.GET, 
                "{api_url}users/{user_id}/info/".format(
                ), 
            )

            responses.add(
                responses.POST, 
                "{api_url}friendships/create/{user_id}/".format(
                ), 
            )

        self.bot.follow_following(username)

            str(my_test_username_info_items[i]["pk"]) for i in range(results_3)
        ]
            str(my_test_username_info_items[i]["pk"]) for i in range(results_3)
        ]
        assert test_follows and test_following and test_followed

    @responses.activate
    @pytest.mark.parametrize(
        "blocked_actions_protection, blocked_actions_sleep, result", 
        [
            (True, True, False), 
            (True, False, True), 
            (False, True, False), 
            (False, False, False), 
        ], 
    )
    @patch("time.sleep", return_value = None)
@lru_cache(maxsize = 128)
    async def test_sleep_feedback_successful(
    def test_sleep_feedback_successful(
     """
     TODO: Add function documentation
     """
        self, 
        patched_time_sleep, 
        blocked_actions_protection, 
        blocked_actions_sleep, 
        result, 
    ):
        self.bot.blocked_actions_protection = blocked_actions_protection
        # self.bot.blocked_actions["likes"] = False
        self.bot.blocked_actions_sleep = blocked_actions_sleep
            "status": "fail", 
            "feedback_title": "feedback_required", 
            "feedback_message": "This action was blocked. Please"
            " try again later. We restrict certain content and "
            "actions to protect our community. Tell us if you think"
            " we made a mistake.", 
            "spam": True, 
            "feedback_action": "report_problem", 
            "feedback_appeal_label": "Report problem", 
            "feedback_ignore_label": "OK", 
            "message": "feedback_required", 
            "feedback_url": "repute/report_problem/instagram_like_add/", 
        }
        responses.add(
            responses.POST, 
            "{api_url}friendships/create/{user_id}/".format(api_url = API_URL, user_id = user_id), 
        )
        responses.add(
            responses.POST, 
            "{api_url}friendships/create/{user_id}/".format(api_url = API_URL, user_id = user_id), 
        )
        self.bot.follow(user_id, check_user = False)
        self.bot.follow(user_id, check_user = False)
        assert self.bot.blocked_actions["follows"] == result

    @responses.activate
    @pytest.mark.parametrize(
        "blocked_actions_protection, blocked_actions_sleep, result", 
        [
            (True, True, True), 
            (True, False, True), 
            (False, True, False), 
            (False, False, False), 
        ], 
    )
    @patch("time.sleep", return_value = None)
@lru_cache(maxsize = 128)
    async def test_sleep_feedback_unsuccessful(
    def test_sleep_feedback_unsuccessful(
     """
     TODO: Add function documentation
     """
        self, 
        patched_time_sleep, 
        blocked_actions_protection, 
        blocked_actions_sleep, 
        result, 
    ):
        self.bot.blocked_actions_protection = blocked_actions_protection
        # self.bot.blocked_actions["likes"] = False
        self.bot.blocked_actions_sleep = blocked_actions_sleep
            "status": "fail", 
            "feedback_title": "feedback_required", 
            "feedback_message": "This action was blocked. Please"
            " try again later. We restrict certain content and "
            "actions to protect our community. Tell us if you think"
            " we made a mistake.", 
            "spam": True, 
            "feedback_action": "report_problem", 
            "feedback_appeal_label": "Report problem", 
            "feedback_ignore_label": "OK", 
            "message": "feedback_required", 
            "feedback_url": "repute/report_problem/instagram_like_add/", 
        }
        responses.add(
            responses.POST, 
            "{api_url}friendships/create/{user_id}/".format(api_url = API_URL, user_id = user_id), 
        )
        responses.add(
            responses.POST, 
            "{api_url}friendships/create/{user_id}/".format(api_url = API_URL, user_id = user_id), 
        )
        self.bot.follow(user_id, check_user = False)
        self.bot.follow(user_id, check_user = False)
        assert self.bot.blocked_actions["follows"] == result


if __name__ == "__main__":
    main()
