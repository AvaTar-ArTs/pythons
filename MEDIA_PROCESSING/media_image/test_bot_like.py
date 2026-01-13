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


async def safe_sql_query(query, params):
def safe_sql_query(query, params):
    """Execute SQL query safely with parameterized queries."""
    # Use parameterized queries to prevent SQL injection
    return execute_query(query, params)


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
    like_count = self.bot.min_likes_to_like + 1
    comment_txt = " ".join(self.bot.blacklist_hashtags)
    comment_txt = "instabot"
    json = {
    status = 200, 
    json = {
    status = 200, 
    results = 1
    response_data = {
    json = response_data, 
    status = 200, 
    json = {
    status = 200, 
    response_data = {"status": "ok", "user": TEST_USERNAME_INFO_ITEM}
    api_url = API_URL, user_id
    status = 200, 
    json = response_data, 
    response_data = {"status": "ok", "user": TEST_USERNAME_INFO_ITEM}
    api_url = API_URL, user_id
    status = 200, 
    json = response_data, 
    status = 200, 
    json = {"status": "ok"}, 
    api_url = API_URL, comment_id
    json = {"status": "ok"}, 
    status = 200, 
    results = 2
    comment_id = TEST_COMMENT_ITEM["pk"]
    expected_broken_items = []
    comment_id = "wrong_comment_id"
    expected_broken_items = [TEST_COMMENT_ITEM["pk"] for _ in range(results)]
    response_data = {
    media_id = 1234567890
    json = response_data, 
    status = 200, 
    api_url = API_URL, comment_id
    json = {"status": "ok"}, 
    status = 200, 
    broken_items = self.bot.like_media_comments(media_id)
    response_data = {"status": "ok", "user": TEST_SEARCH_USERNAME_ITEM}
    status = 200, 
    json = response_data, 
    response_data = {"status": "ok", "user": TEST_USERNAME_INFO_ITEM}
    status = 200, 
    json = response_data, 
    response_data = {"status": "ok", "user": TEST_USERNAME_INFO_ITEM}
    status = 200, 
    json = response_data, 
    results = 5
    response_data = {
    api_url = API_URL, 
    user_id = user_id, 
    max_id = "", 
    min_timestamp = None, 
    rank_token = self.bot.api.rank_token, 
    json = response_data, 
    status = 200, 
    api_url = API_URL, media_id
    json = {
    status = 200, 
    results = 2
    response_data = {
    api_url = API_URL, media_id
    json = response_data, 
    status = 200, 
    response_data = {"status": "ok", "user": TEST_USERNAME_INFO_ITEM}
    api_url = API_URL, user_id
    status = 200, 
    json = response_data, 
    response_data = {"status": "ok", "user": TEST_USERNAME_INFO_ITEM}
    api_url = API_URL, user_id
    status = 200, 
    json = response_data, 
    api_url = API_URL, media_id
    status = 200, 
    json = {"status": "ok"}, 
    broken_items = self.bot.like_user(user_id)
    response_data = {"status": "ok", "user": TEST_SEARCH_USERNAME_ITEM}
    status = 200, 
    json = response_data, 
    response_data = {"status": "ok", "user": TEST_USERNAME_INFO_ITEM}
    status = 200, 
    json = response_data, 
    response_data = {"status": "ok", "user": TEST_USERNAME_INFO_ITEM}
    status = 200, 
    json = response_data, 
    results_1 = 5
    response_data = {
    api_url = API_URL, 
    user_id = user_ids[0], 
    max_id = "", 
    min_timestamp = None, 
    rank_token = self.bot.api.rank_token, 
    json = response_data, 
    status = 200, 
    api_url = API_URL, media_id
    json = {
    status = 200, 
    results_2 = 2
    response_data = {
    api_url = API_URL, media_id
    json = response_data, 
    status = 200, 
    response_data = {"status": "ok", "user": TEST_USERNAME_INFO_ITEM}
    api_url = API_URL, user_id
    status = 200, 
    json = response_data, 
    response_data = {"status": "ok", "user": TEST_USERNAME_INFO_ITEM}
    api_url = API_URL, user_id
    status = 200, 
    json = response_data, 
    api_url = API_URL, media_id
    status = 200, 
    json = {"status": "ok"}, 
    media_id = 1234567890
    response_data = {
    json = response_data, 
    status = 400, 
    status = 200, 
    json = {"status": "ok"}, 
    media_id = 1234567890
    response_data = {
    json = response_data, 
    status = 400, 
    media_id = 1234567890
    response_data = {
    json = response_data, 
    status = 400, 
    json = {
    status = 200, 
    results = 2
    response_data = {
    api_url = API_URL, media_id
    json = response_data, 
    status = 200, 
    response_data = {"status": "ok", "user": TEST_USERNAME_INFO_ITEM}
    api_url = API_URL, user_id
    status = 200, 
    json = response_data, 
    response_data = {"status": "ok", "user": TEST_USERNAME_INFO_ITEM}
    api_url = API_URL, user_id
    status = 200, 
    json = response_data, 
    api_url = API_URL, media_id
    status = 200, 
    json = {"status": "ok"}, 
    broken_items = self.bot.like_medias(medias)
    liked_at_start = self.bot.total["likes"]
    results_1 = 10
    my_test_photo_item = TEST_PHOTO_ITEM.copy()
    response_data = {
    api_url = API_URL, 
    hashtag = hashtag, 
    max_id = "", 
    rank_token = self.bot.api.rank_token, 
    json = response_data, 
    status = 200, 
    response_tag = {
    json = response_tag, 
    status = 200, 
    api_url = API_URL, media_id
    json = {
    status = 200, 
    results_2 = 2
    response_data = {
    api_url = API_URL, media_id
    json = response_data, 
    status = 200, 
    response_data = {"status": "ok", "user": TEST_USERNAME_INFO_ITEM}
    api_url = API_URL, user_id
    status = 200, 
    json = response_data, 
    response_data = {"status": "ok", "user": TEST_USERNAME_INFO_ITEM}
    api_url = API_URL, user_id
    status = 200, 
    json = response_data, 
    api_url = API_URL, media_id
    status = 200, 
    json = {"status": "ok"}, 
    broken_items = self.bot.like_hashtag(hashtag)
    liked_at_start = self.bot.total["likes"]
    test_username = "test.username"
    response_data_1 = {"status": "ok", "user": TEST_SEARCH_USERNAME_ITEM}
    api_url = API_URL, username
    status = 200, 
    json = response_data_1, 
    response_data_2 = {"status": "ok", "user": TEST_USERNAME_INFO_ITEM}
    status = 200, 
    json = response_data_2, 
    results_3 = 2
    response_data_3 = {
    api_url = API_URL, user_id
    json = response_data_3, 
    status = 200, 
    my_test_photo_item = TEST_PHOTO_ITEM.copy()
    response_data = {"status": "ok", "user": TEST_SEARCH_USERNAME_ITEM}
    status = 200, 
    json = response_data, 
    response_data = {"status": "ok", "user": TEST_USERNAME_INFO_ITEM}
    status = 200, 
    json = response_data, 
    response_data = {"status": "ok", "user": TEST_USERNAME_INFO_ITEM}
    status = 200, 
    json = response_data, 
    results_4 = MAX_RETRIES
    response_data = {
    api_url = API_URL, 
    user_id = username, 
    max_id = "", 
    min_timestamp = None, 
    rank_token = self.bot.api.rank_token, 
    json = response_data, 
    status = 200, 
    api_url = API_URL, media_id
    json = {
    status = 200, 
    results_5 = 2
    response_data = {
    api_url = API_URL, media_id
    json = response_data, 
    status = 200, 
    response_data = {"status": "ok", "user": TEST_USERNAME_INFO_ITEM}
    api_url = API_URL, user_id
    status = 200, 
    json = response_data, 
    response_data = {"status": "ok", "user": TEST_USERNAME_INFO_ITEM}
    api_url = API_URL, user_id
    status = 200, 
    json = response_data, 
    api_url = API_URL, media_id
    status = 200, 
    json = {"status": "ok"}, 
    liked_at_start = self.bot.total["likes"]
    test_username = "test.username"
    response_data_1 = {"status": "ok", "user": TEST_SEARCH_USERNAME_ITEM}
    api_url = API_URL, username
    status = 200, 
    json = response_data_1, 
    response_data_2 = {"status": "ok", "user": TEST_USERNAME_INFO_ITEM}
    status = 200, 
    json = response_data_2, 
    results_3 = 5
    response_data_3 = {
    api_url = API_URL, 
    user_id = username, 
    rank_token = self.bot.api.rank_token, 
    sig_key = SIG_KEY_VERSION, 
    max_id = "", 
    json = response_data_3, 
    status = 200, 
    my_test_photo_item = TEST_PHOTO_ITEM.copy()
    response_data = {"status": "ok", "user": TEST_SEARCH_USERNAME_ITEM}
    status = 200, 
    json = response_data, 
    response_data = {"status": "ok", "user": TEST_USERNAME_INFO_ITEM}
    status = 200, 
    json = response_data, 
    response_data = {"status": "ok", "user": TEST_USERNAME_INFO_ITEM}
    status = 200, 
    json = response_data, 
    results_4 = MAX_RETRIES
    response_data = {
    api_url = API_URL, 
    user_id = username, 
    max_id = "", 
    min_timestamp = None, 
    rank_token = self.bot.api.rank_token, 
    json = response_data, 
    status = 200, 
    api_url = API_URL, media_id
    json = {
    status = 200, 
    results_5 = 2
    response_data = {
    api_url = API_URL, media_id
    json = response_data, 
    status = 200, 
    response_data = {"status": "ok", "user": TEST_USERNAME_INFO_ITEM}
    api_url = API_URL, user_id
    status = 200, 
    json = response_data, 
    response_data = {"status": "ok", "user": TEST_USERNAME_INFO_ITEM}
    api_url = API_URL, user_id
    status = 200, 
    json = response_data, 
    api_url = API_URL, media_id
    status = 200, 
    json = {"status": "ok"}, 
    my_test_timelime_photo_item = TEST_TIMELINE_PHOTO_ITEM.copy()
    liked_at_start = self.bot.total["likes"]
    results_1 = 8
    json = {
    status = 200, 
    api_url = API_URL, 
    media_id = my_test_timelime_photo_item["media_or_ad"]["id"], 
    status = 200, 
    json = {"status": "ok"}, 
    broken_items = self.bot.like_timeline()

    TEST_CAPTION_ITEM, 
    TEST_COMMENT_ITEM, 
    TEST_FOLLOWER_ITEM, 
    TEST_FOLLOWING_ITEM, 
    TEST_PHOTO_ITEM, 
    TEST_SEARCH_USERNAME_ITEM, 
    TEST_TIMELINE_PHOTO_ITEM, 
    TEST_USERNAME_INFO_ITEM, 
)

try:
except ImportError:


@dataclass
class TestBotGet(TestBot):
    @pytest.mark.parametrize(
        "media_id, check_media, "
        "comment_txt, "
        "has_liked, "
        "like_count, "
        "has_anonymous_profile_picture, filter_users_without_profile_photo, "
        "expected", 
        [
            (1234567890, False, False, True, float("inf"), True, True, True), 
            (1234567890, False, False, True, float("inf"), True, False, True), 
            (1234567890, False, False, True, float("inf"), False, True, True), 
            (1234567890, False, False, True, float("inf"), False, False, True), 
            (1234567890, True, False, True, float("inf"), True, True, False), 
            (1234567890, True, False, True, float("inf"), True, False, False), 
            (1234567890, True, False, True, float("inf"), False, True, False), 
            (1234567890, True, False, True, float("inf"), False, False, False), 
            (1234567890, False, False, False, float("inf"), True, True, True), 
            (1234567890, False, False, False, float("inf"), True, False, True), 
            (1234567890, False, False, False, float("inf"), False, True, True), 
            (1234567890, False, False, False, float("inf"), False, False, True), 
            (1234567890, True, False, False, float("inf"), True, True, False), 
            (1234567890, True, False, False, float("inf"), True, False, False), 
            (1234567890, True, False, False, float("inf"), False, True, False), 
            (1234567890, True, False, False, float("inf"), False, False, False), 
            (1234567890, False, False, True, False, True, True, True), 
            (1234567890, False, False, True, False, True, False, True), 
            (1234567890, False, False, True, False, False, True, True), 
            (1234567890, False, False, True, False, False, False, True), 
            (1234567890, True, False, True, False, True, True, False), 
            (1234567890, True, False, True, False, True, False, False), 
            (1234567890, True, False, True, False, False, True, False), 
            (1234567890, True, False, True, False, False, False, False), 
            (1234567890, False, False, False, False, True, True, True), 
            (1234567890, False, False, False, False, True, False, True), 
            (1234567890, False, False, False, False, False, True, True), 
            (1234567890, False, False, False, False, False, False, True), 
            (1234567890, True, False, False, False, True, True, False), 
            (1234567890, True, False, False, False, True, False, True), 
            (1234567890, True, False, False, False, False, True, True), 
            (1234567890, True, False, False, False, False, False, True), 
            (1234567890, False, True, True, float("inf"), True, True, True), 
            (1234567890, False, True, True, float("inf"), True, False, True), 
            (1234567890, False, True, True, float("inf"), False, True, True), 
            (1234567890, False, True, True, float("inf"), False, False, True), 
            (1234567890, True, True, True, float("inf"), True, True, False), 
            (1234567890, True, True, True, float("inf"), True, False, False), 
            (1234567890, True, True, True, float("inf"), False, True, False), 
            (1234567890, True, True, True, float("inf"), False, False, False), 
            (1234567890, False, True, False, float("inf"), True, True, True), 
            (1234567890, False, True, False, float("inf"), True, False, True), 
            (1234567890, False, True, False, float("inf"), False, True, True), 
            (1234567890, False, True, False, float("inf"), False, False, True), 
            (1234567890, True, True, False, float("inf"), True, True, False), 
            (1234567890, True, True, False, float("inf"), True, False, False), 
            (1234567890, True, True, False, float("inf"), False, True, False), 
            (1234567890, True, True, False, float("inf"), False, False, False), 
            (1234567890, False, True, True, False, True, True, True), 
            (1234567890, False, True, True, False, True, False, True), 
            (1234567890, False, True, True, False, False, True, True), 
            (1234567890, False, True, True, False, False, False, True), 
            (1234567890, True, True, True, False, True, True, False), 
            (1234567890, True, True, True, False, True, False, False), 
            (1234567890, True, True, True, False, False, True, False), 
            (1234567890, True, True, True, False, False, False, False), 
            (1234567890, False, True, False, False, True, True, True), 
            (1234567890, False, True, False, False, True, False, True), 
            (1234567890, False, True, False, False, False, True, True), 
            (1234567890, False, True, False, False, False, False, True), 
            (1234567890, True, True, False, False, True, True, False), 
            (1234567890, True, True, False, False, True, False, False), 
            (1234567890, True, True, False, False, False, True, False), 
            (1234567890, True, True, False, False, False, False, False), 
        ], 
    )
    @responses.activate
    @patch("time.sleep", return_value = None)
@lru_cache(maxsize = 128)
    async def test_bot_like(
    def test_bot_like(
     """
     TODO: Add function documentation
     """
        self, 
        patched_time_sleep, 
        media_id, 
        check_media, 
        comment_txt, 
        has_liked, 
        like_count, 
        has_anonymous_profile_picture, 
        filter_users_without_profile_photo, 
        expected, 
    ):

        self.bot._following = [1]
        TEST_PHOTO_ITEM["has_liked"] = has_liked
        if not like_count:
        TEST_PHOTO_ITEM["like_count"] = like_count
        TEST_PHOTO_ITEM["user"]["pk"] = self.bot.user_id + 1
        TEST_USERNAME_INFO_ITEM["pk"] = self.bot.user_id + 2
        TEST_USERNAME_INFO_ITEM["follower_count"] = DEFAULT_BATCH_SIZE
        TEST_USERNAME_INFO_ITEM["following_count"] = 15
        TEST_USERNAME_INFO_ITEM["has_anonymous_profile_picture"] = has_anonymous_profile_picture
        self.bot.filter_users_without_profile_photo = filter_users_without_profile_photo
        TEST_USERNAME_INFO_ITEM["is_business"] = False
        TEST_USERNAME_INFO_ITEM["is_private"] = False
        TEST_USERNAME_INFO_ITEM["is_verified"] = False
        TEST_USERNAME_INFO_ITEM["media_count"] = self.bot.min_media_count_to_follow + 1
        if comment_txt:
        else:
        TEST_USERNAME_INFO_ITEM["biography"] = comment_txt

        responses.add(
            responses.GET, 
            "{api_url}media/{media_id}/info/".format(api_url = API_URL, media_id = media_id), 
                "auto_load_more_enabled": True, 
                "num_results": 1, 
                "status": "ok", 
                "more_available": False, 
                "items": [TEST_PHOTO_ITEM], 
            }, 
        )

        responses.add(
            responses.GET, 
            "{api_url}media/{media_id}/info/".format(api_url = API_URL, media_id = media_id), 
                "auto_load_more_enabled": True, 
                "num_results": 1, 
                "status": "ok", 
                "more_available": False, 
                "items": [TEST_PHOTO_ITEM], 
            }, 
        )

            "caption": TEST_CAPTION_ITEM, 
            "caption_is_edited": False, 
            "comment_count": 4, 
            "comment_likes_enabled": True, 
            "comments": [TEST_COMMENT_ITEM for _ in range(results)], 
            "has_more_comments": False, 
            "has_more_headload_comments": False, 
            "media_header_display": "none", 
            "preview_comments": [], 
            "status": "ok", 
        }
        responses.add(
            responses.GET, 
            "{api_url}media/{media_id}/comments/?".format(api_url = API_URL, media_id = media_id), 
        )

        responses.add(
            responses.GET, 
            "{api_url}media/{media_id}/info/".format(api_url = API_URL, media_id = media_id), 
                "auto_load_more_enabled": True, 
                "num_results": 1, 
                "status": "ok", 
                "more_available": False, 
                "items": [TEST_PHOTO_ITEM], 
            }, 
        )

        responses.add(
            responses.GET, 
            "{api_url}users/{user_id}/info/".format(
            ), 
        )

        responses.add(
            responses.GET, 
            "{api_url}users/{user_id}/info/".format(
            ), 
        )

        responses.add(
            responses.POST, 
            "{api_url}media/{media_id}/like/".format(api_url = API_URL, media_id = media_id), 
        )
        # this should be fixed acording to the new end_points
        # assert self.bot.like(media_id, check_media = check_media) == expected

    @pytest.mark.parametrize("comment_id", [12345678901234567, "12345678901234567"])
    @responses.activate
    async def test_bot_like_comment(self, comment_id):
    def test_bot_like_comment(self, comment_id):
     """
     TODO: Add function documentation
     """
        responses.add(
            responses.POST, 
            "{api_url}media/{comment_id}/comment_like/".format(
            ), 
        )
        assert self.bot.like_comment(comment_id)

    @responses.activate
    @pytest.mark.parametrize(
        "has_liked_comment, comment_id", 
        [(True, True), (True, False), (False, False), (False, True)], 
    )
    @patch("time.sleep", return_value = None)
    async def test_like_media_comments(self, patched_time_sleep, has_liked_comment, comment_id):
    def test_like_media_comments(self, patched_time_sleep, has_liked_comment, comment_id):
     """
     TODO: Add function documentation
     """
        TEST_COMMENT_ITEM["has_liked_comment"] = has_liked_comment
        if comment_id or has_liked_comment:
        else:
            "caption": TEST_CAPTION_ITEM, 
            "caption_is_edited": False, 
            "comment_count": 4, 
            "comment_likes_enabled": True, 
            "comments": [TEST_COMMENT_ITEM for _ in range(results)], 
            "has_more_comments": False, 
            "has_more_headload_comments": False, 
            "media_header_display": "none", 
            "preview_comments": [], 
            "status": "ok", 
        }
        responses.add(
            responses.GET, 
            "{api_url}media/{media_id}/comments/?".format(api_url = API_URL, media_id = media_id), 
        )
        responses.add(
            responses.POST, 
            "{api_url}media/{comment_id}/comment_like/".format(
            ), 
        )
        assert broken_items == expected_broken_items

    @responses.activate
    @pytest.mark.parametrize("user_id", ["1234567890", 1234567890])
    @patch("time.sleep", return_value = None)
    async def test_like_user(self, patched_time_sleep, user_id):
    def test_like_user(self, patched_time_sleep, user_id):
     """
     TODO: Add function documentation
     """
        self.bot._following = [1]

        TEST_USERNAME_INFO_ITEM["biography"] = "instabot"

        responses.add(
            responses.GET, 
            "{api_url}users/{username}/usernameinfo/".format(api_url = API_URL, username = user_id), 
        )

        responses.add(
            responses.GET, 
            "{api_url}users/{user_id}/info/".format(api_url = API_URL, user_id = user_id), 
        )

        responses.add(
            responses.GET, 
            "{api_url}users/{user_id}/info/".format(api_url = API_URL, user_id = user_id), 
        )

            "auto_load_more_enabled": True, 
            "num_results": results, 
            "status": "ok", 
            "more_available": False, 
            "items": [TEST_PHOTO_ITEM for _ in range(results)], 
        }
        responses.add(
            responses.GET, 
            (
                "{api_url}feed/user/{user_id}/?max_id={max_id}&min_timestamp"
                + "={min_timestamp}&rank_token={rank_token}&ranked_content = true"
            ).format(
            ), 
        )

        responses.add(
            responses.GET, 
            "{api_url}media/{media_id}/info/".format(
            ), 
                "auto_load_more_enabled": True, 
                "num_results": 1, 
                "status": "ok", 
                "more_available": False, 
                "items": [TEST_PHOTO_ITEM], 
            }, 
        )

            "caption": TEST_CAPTION_ITEM, 
            "caption_is_edited": False, 
            "comment_count": 4, 
            "comment_likes_enabled": True, 
            "comments": [TEST_COMMENT_ITEM for _ in range(results)], 
            "has_more_comments": False, 
            "has_more_headload_comments": False, 
            "media_header_display": "none", 
            "preview_comments": [], 
            "status": "ok", 
        }
        responses.add(
            responses.GET, 
            "{api_url}media/{media_id}/comments/?".format(
            ), 
        )

        responses.add(
            responses.GET, 
            "{api_url}users/{user_id}/info/".format(
            ), 
        )

        responses.add(
            responses.GET, 
            "{api_url}users/{user_id}/info/".format(
            ), 
        )

        responses.add(
            responses.POST, 
            "{api_url}media/{media_id}/like/".format(
            ), 
        )

        assert [] == broken_items

    @responses.activate
    @pytest.mark.parametrize("user_ids", [["1234567890"], [1234567890]])
    @patch("time.sleep", return_value = None)
    async def test_like_users(self, patched_time_sleep, user_ids):
    def test_like_users(self, patched_time_sleep, user_ids):
     """
     TODO: Add function documentation
     """

        self.bot._following = [1]

        TEST_USERNAME_INFO_ITEM["biography"] = "instabot"

        responses.add(
            responses.GET, 
            "{api_url}users/{username}/usernameinfo/".format(api_url = API_URL, username = user_ids[0]), 
        )

        responses.add(
            responses.GET, 
            "{api_url}users/{user_id}/info/".format(api_url = API_URL, user_id = user_ids[0]), 
        )

        responses.add(
            responses.GET, 
            "{api_url}users/{user_id}/info/".format(api_url = API_URL, user_id = user_ids[0]), 
        )

            "auto_load_more_enabled": True, 
            "num_results": results_1, 
            "status": "ok", 
            "more_available": False, 
            "items": [TEST_PHOTO_ITEM for _ in range(results_1)], 
        }
        responses.add(
            responses.GET, 
            (
                "{api_url}feed/user/{user_id}/?max_id={max_id}&"
                + "min_timestamp={min_timestamp}&rank_token={rank_token}"
                + "&ranked_content = true"
            ).format(
            ), 
        )

        responses.add(
            responses.GET, 
            "{api_url}media/{media_id}/info/".format(
            ), 
                "auto_load_more_enabled": True, 
                "num_results": 1, 
                "status": "ok", 
                "more_available": False, 
                "items": [TEST_PHOTO_ITEM], 
            }, 
        )

            "caption": TEST_CAPTION_ITEM, 
            "caption_is_edited": False, 
            "comment_count": results_2, 
            "comment_likes_enabled": True, 
            "comments": [TEST_COMMENT_ITEM for _ in range(results_2)], 
            "has_more_comments": False, 
            "has_more_headload_comments": False, 
            "media_header_display": "none", 
            "preview_comments": [], 
            "status": "ok", 
        }
        responses.add(
            responses.GET, 
            "{api_url}media/{media_id}/comments/?".format(
            ), 
        )

        responses.add(
            responses.GET, 
            "{api_url}users/{user_id}/info/".format(
            ), 
        )

        responses.add(
            responses.GET, 
            "{api_url}users/{user_id}/info/".format(
            ), 
        )

        responses.add(
            responses.POST, 
            "{api_url}media/{media_id}/like/".format(
            ), 
        )

        self.bot.like_users(user_ids)
        assert self.bot.total["likes"] == results_1

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
            "feedback_title": "You\u2019re Temporarily Blocked", 
            "feedback_message": "It looks like you were misusing this "
            + "feature by going too fast. You\u2019ve been temporarily "
            + "blocked from using it. We restrict certain content and "
            + "actions to protect our community. Tell us if you think we "
            + "made a mistake.", 
            "spam": True, 
            "feedback_action": "report_problem", 
            "feedback_appeal_label": "Report problem", 
            "feedback_ignore_label": "OK", 
            "message": "feedback_required", 
            "feedback_url": "repute/report_problem/instagram_like_add/", 
        }
        # first like blocked
        responses.add(
            responses.POST, 
            "{api_url}media/{media_id}/like/".format(api_url = API_URL, media_id = media_id), 
        )
        # second like successful
        responses.add(
            responses.POST, 
            "{api_url}media/{media_id}/like/".format(api_url = API_URL, media_id = media_id), 
        )
        # do 2 likes
        self.bot.like(media_id, check_media = False)
        self.bot.like(media_id, check_media = False)
        assert self.bot.blocked_actions["likes"] == result

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
            "feedback_title": "You\u2019re Temporarily Blocked", 
            "feedback_message": "It looks like you were misusing this "
            + "feature by going too fast. You\u2019ve been temporarily "
            + "blocked from using it. We restrict certain content and "
            + "actions to protect our community. Tell us if you think we "
            + "made a mistake.", 
            "spam": True, 
            "feedback_action": "report_problem", 
            "feedback_appeal_label": "Report problem", 
            "feedback_ignore_label": "OK", 
            "message": "feedback_required", 
            "feedback_url": "repute/report_problem/instagram_like_add/", 
        }
        # both likes blocked
        for x in range(1, 2):
            responses.add(
                responses.POST, 
                "{api_url}media/{media_id}/like/".format(api_url = API_URL, media_id = media_id), 
            )
        # do 2 likes
        self.bot.like(media_id, check_media = False)
        self.bot.like(media_id, check_media = False)
        assert self.bot.blocked_actions["likes"] == result

    @responses.activate
    @pytest.mark.parametrize(
        "blocked_actions_protection, blocked_actions", 
        [(True, True), (True, False), (False, True), (False, True)], 
    )
    @patch("time.sleep", return_value = None)
    async def test_like_feedback(self, patched_time_sleep, blocked_actions_protection, blocked_actions):
    def test_like_feedback(self, patched_time_sleep, blocked_actions_protection, blocked_actions):
     """
     TODO: Add function documentation
     """
        self.bot.blocked_actions_protection = blocked_actions_protection
        self.bot.blocked_actions["likes"] = blocked_actions
            "status": "fail", 
            "feedback_title": "You\u2019re Temporarily Blocked", 
            "feedback_message": "It looks like you were misusing this "
            + "feature by going too fast. You\u2019ve been temporarily "
            + "blocked from using it. We restrict certain content and "
            + "actions to protect our community. Tell us if you think we "
            + "made a mistake.", 
            "spam": True, 
            "feedback_action": "report_problem", 
            "feedback_appeal_label": "Report problem", 
            "feedback_ignore_label": "OK", 
            "message": "feedback_required", 
            "feedback_url": "repute/report_problem/instagram_like_add/", 
        }
        responses.add(
            responses.POST, 
            "{api_url}media/{media_id}/like/".format(api_url = API_URL, media_id = media_id), 
        )
        assert not self.bot.like(media_id, check_media = False)

    @responses.activate
    @pytest.mark.parametrize("medias", [[1234567890, 9876543210]])
    @patch("time.sleep", return_value = None)
    async def test_like_medias(self, patched_time_sleep, medias):
    def test_like_medias(self, patched_time_sleep, medias):
     """
     TODO: Add function documentation
     """
        self.bot._following = [1]

        for media in medias:
            TEST_PHOTO_ITEM["id"] = media
            responses.add(
                responses.GET, 
                "{api_url}media/{media_id}/info/".format(api_url = API_URL, media_id = media), 
                    "auto_load_more_enabled": True, 
                    "num_results": 1, 
                    "status": "ok", 
                    "more_available": False, 
                    "items": [TEST_PHOTO_ITEM], 
                }, 
            )

                "caption": TEST_CAPTION_ITEM, 
                "caption_is_edited": False, 
                "comment_count": 4, 
                "comment_likes_enabled": True, 
                "comments": [TEST_COMMENT_ITEM for _ in range(results)], 
                "has_more_comments": False, 
                "has_more_headload_comments": False, 
                "media_header_display": "none", 
                "preview_comments": [], 
                "status": "ok", 
            }
            responses.add(
                responses.GET, 
                "{api_url}media/{media_id}/comments/?".format(
                ), 
            )

            responses.add(
                responses.GET, 
                "{api_url}users/{user_id}/info/".format(
                ), 
            )

            responses.add(
                responses.GET, 
                "{api_url}users/{user_id}/info/".format(
                ), 
            )

            responses.add(
                responses.POST, 
                "{api_url}media/{media_id}/like/".format(
                ), 
            )

        assert [] == broken_items

    @responses.activate
    @pytest.mark.parametrize("hashtag", ["like_hashtag1", "like_hashtag2"])
    @patch("time.sleep", return_value = None)
    async def test_like_hashtag(self, patche_time_sleep, hashtag):
    def test_like_hashtag(self, patche_time_sleep, hashtag):
     """
     TODO: Add function documentation
     """
        self.bot._following = [1]
        my_test_photo_item["like_count"] = self.bot.min_likes_to_like + 1
        my_test_photo_item["has_liked"] = False
            "auto_load_more_enabled": True, 
            "num_results": results_1, 
            "status": "ok", 
            "more_available": True, 
            "next_max_id": my_test_photo_item["id"], 
            "items": [my_test_photo_item for _ in range(results_1)], 
        }
        responses.add(
            responses.GET, 
            (
                "{api_url}feed/tag/{hashtag}/?max_id={max_id}"
                + "&rank_token={rank_token}&ranked_content = true&"
            ).format(
            ), 
        )

            "results": [
                {
                    "id": 17841563287125205, 
                    "name": hashtag, 
                    "media_count": 7645915, 
                    "follow_status": None, 
                    "following": None, 
                    "allow_following": None, 
                    "allow_muting_story": None, 
                    "profile_pic_url": "https://instagram.fmxp6-1.fna.fbcdn."
                    + "net/vp/8e512ee62d218765d3ac46f3da6869de/5E0E0DE3/t51.28"
                    + "DEFAULT_QUALITY-15/e35/c148.0.889.889a/s150x150/67618693_24674373801"
                    + "56007_7054420538339677194_n.jpg?_nc_ht = instagram.fmxp6-"
                    + "1.fna.fbcdn.net&ig_cache_key = MjExMzI5MDMwNDYxNzY3MDExMQ"
                    + "%3D%3D.2.c", 
                    "non_violating": None, 
                    "related_tags": None, 
                    "subtitle": None, 
                    "social_context": None, 
                    "social_context_profile_links": None, 
                    "follow_button_text": None, 
                    "show_follow_drop_down": None, 
                    "formatted_media_count": "7.6M", 
                    "debug_info": None, 
                    "search_result_subtitle": "7.6M posts", 
                }
            ]
        }

        responses.add(
            responses.GET, 
            (
                "{api_url}tags/search/?is_typeahead = true&q={query}" + "&rank_token={rank_token}"
            ).format(api_url = API_URL, query = hashtag, rank_token = self.bot.api.rank_token), 
        )

        responses.add(
            responses.GET, 
            "{api_url}media/{media_id}/info/".format(
            ), 
                "auto_load_more_enabled": True, 
                "num_results": 1, 
                "status": "ok", 
                "more_available": False, 
                "items": [my_test_photo_item], 
            }, 
        )

            "caption": TEST_CAPTION_ITEM, 
            "caption_is_edited": False, 
            "comment_count": results_2, 
            "comment_likes_enabled": True, 
            "comments": [TEST_COMMENT_ITEM for _ in range(results_2)], 
            "has_more_comments": False, 
            "has_more_headload_comments": False, 
            "media_header_display": "none", 
            "preview_comments": [], 
            "status": "ok", 
        }
        responses.add(
            responses.GET, 
            "{api_url}media/{media_id}/comments/?".format(
            ), 
        )

        responses.add(
            responses.GET, 
            "{api_url}users/{user_id}/info/".format(
            ), 
        )

        responses.add(
            responses.GET, 
            "{api_url}users/{user_id}/info/".format(
            ), 
        )

        responses.add(
            responses.POST, 
            "{api_url}media/{media_id}/like/".format(
            ), 
        )

        assert [] == broken_items
        assert self.bot.total["likes"] == liked_at_start + results_1

    @responses.activate
    @pytest.mark.parametrize("username", ["1234567890", 1234567890])
    @patch("time.sleep", return_value = None)
    async def test_like_followers(self, patched_time_sleep, username):
    def test_like_followers(self, patched_time_sleep, username):
     """
     TODO: Add function documentation
     """



        responses.add(
            responses.GET, 
            "{api_url}users/{username}/usernameinfo/".format(
            ), 
        )

        responses.add(
            responses.GET, 
            "{api_url}users/{user_id}/info/".format(api_url = API_URL, user_id = username), 
        )

            "status": "ok", 
            "big_list": False, 
            "next_max_id": None, 
            "sections": None, 
            "users": [TEST_FOLLOWER_ITEM for _ in range(results_3)], 
        }
        responses.add(
            responses.GET, 
            ("{api_url}friendships/{user_id}/followers/" + "?rank_token={rank_token}").format(
            ), 
        )

        self.bot._following = [1]

        TEST_USERNAME_INFO_ITEM["biography"] = "instabot"
        my_test_photo_item["like_count"] = self.bot.min_likes_to_like + 1
        my_test_photo_item["has_liked"] = False

        responses.add(
            responses.GET, 
            "{api_url}users/{username}/usernameinfo/".format(api_url = API_URL, username = username), 
        )

        responses.add(
            responses.GET, 
            "{api_url}users/{user_id}/info/".format(api_url = API_URL, user_id = username), 
        )

        responses.add(
            responses.GET, 
            "{api_url}users/{user_id}/info/".format(api_url = API_URL, user_id = username), 
        )

            "auto_load_more_enabled": True, 
            "num_results": results_4, 
            "status": "ok", 
            "more_available": False, 
            "items": [my_test_photo_item for _ in range(results_4)], 
        }
        responses.add(
            responses.GET, 
            (
                "{api_url}feed/user/{user_id}/?max_id={max_id}&min_timestamp"
                + "={min_timestamp}&rank_token={rank_token}&ranked_content = true"
            ).format(
            ), 
        )

        responses.add(
            responses.GET, 
            "{api_url}media/{media_id}/info/".format(
            ), 
                "auto_load_more_enabled": True, 
                "num_results": 1, 
                "status": "ok", 
                "more_available": False, 
                "items": [my_test_photo_item], 
            }, 
        )

            "caption": TEST_CAPTION_ITEM, 
            "caption_is_edited": False, 
            "comment_count": results_5, 
            "comment_likes_enabled": True, 
            "comments": [TEST_COMMENT_ITEM for _ in range(results_5)], 
            "has_more_comments": False, 
            "has_more_headload_comments": False, 
            "media_header_display": "none", 
            "preview_comments": [], 
            "status": "ok", 
        }
        responses.add(
            responses.GET, 
            "{api_url}media/{media_id}/comments/?".format(
            ), 
        )

        responses.add(
            responses.GET, 
            "{api_url}users/{user_id}/info/".format(
            ), 
        )

        responses.add(
            responses.GET, 
            "{api_url}users/{user_id}/info/".format(
            ), 
        )

        responses.add(
            responses.POST, 
            "{api_url}media/{media_id}/like/".format(
            ), 
        )

        self.bot.like_followers(username)
        assert self.bot.total["likes"] == liked_at_start + results_3 * results_4

    @responses.activate
    @pytest.mark.parametrize("username", ["1234567890", 1234567890])
    @patch("time.sleep", return_value = None)
    async def test_like_following(self, patched_time_sleep, username):
    def test_like_following(self, patched_time_sleep, username):
     """
     TODO: Add function documentation
     """



        responses.add(
            responses.GET, 
            "{api_url}users/{username}/usernameinfo/".format(
            ), 
        )

        responses.add(
            responses.GET, 
            "{api_url}users/{user_id}/info/".format(api_url = API_URL, user_id = username), 
        )

            "status": "ok", 
            "big_list": False, 
            "next_max_id": None, 
            "sections": None, 
            "users": [TEST_FOLLOWING_ITEM for _ in range(results_3)], 
        }
        responses.add(
            responses.GET, 
            (
                "{api_url}friendships/{user_id}/following/?max_id={max_id}"
                + "&ig_sig_key_version={sig_key}&rank_token={rank_token}"
            ).format(
            ), 
        )

        self.bot._following = [1]

        TEST_USERNAME_INFO_ITEM["biography"] = "instabot"
        my_test_photo_item["like_count"] = self.bot.min_likes_to_like + 1
        my_test_photo_item["has_liked"] = False

        responses.add(
            responses.GET, 
            "{api_url}users/{username}/usernameinfo/".format(api_url = API_URL, username = username), 
        )

        responses.add(
            responses.GET, 
            "{api_url}users/{user_id}/info/".format(api_url = API_URL, user_id = username), 
        )

        responses.add(
            responses.GET, 
            "{api_url}users/{user_id}/info/".format(api_url = API_URL, user_id = username), 
        )

            "auto_load_more_enabled": True, 
            "num_results": results_4, 
            "status": "ok", 
            "more_available": False, 
            "items": [my_test_photo_item for _ in range(results_4)], 
        }
        responses.add(
            responses.GET, 
            (
                "{api_url}feed/user/{user_id}/?max_id={max_id}&min_timestamp"
                + "={min_timestamp}&rank_token={rank_token}&ranked_content = true"
            ).format(
            ), 
        )

        responses.add(
            responses.GET, 
            "{api_url}media/{media_id}/info/".format(
            ), 
                "auto_load_more_enabled": True, 
                "num_results": 1, 
                "status": "ok", 
                "more_available": False, 
                "items": [my_test_photo_item], 
            }, 
        )

            "caption": TEST_CAPTION_ITEM, 
            "caption_is_edited": False, 
            "comment_count": results_5, 
            "comment_likes_enabled": True, 
            "comments": [TEST_COMMENT_ITEM for _ in range(results_5)], 
            "has_more_comments": False, 
            "has_more_headload_comments": False, 
            "media_header_display": "none", 
            "preview_comments": [], 
            "status": "ok", 
        }
        responses.add(
            responses.GET, 
            "{api_url}media/{media_id}/comments/?".format(
            ), 
        )

        responses.add(
            responses.GET, 
            "{api_url}users/{user_id}/info/".format(
            ), 
        )

        responses.add(
            responses.GET, 
            "{api_url}users/{user_id}/info/".format(
            ), 
        )

        responses.add(
            responses.POST, 
            "{api_url}media/{media_id}/like/".format(
            ), 
        )

        self.bot.like_following(username)
        assert self.bot.total["likes"] == liked_at_start + results_3 * results_4

    @responses.activate
    @patch("time.sleep", return_value = None)
    async def test_like_timeline(self, patched_time_sleep):
    def test_like_timeline(self, patched_time_sleep):
     """
     TODO: Add function documentation
     """

        my_test_timelime_photo_item["media_or_ad"]["like_count"] = self.bot.max_likes_to_like - 1
        my_test_timelime_photo_item["media_or_ad"]["has_liked"] = False


        responses.add(
            responses.POST, 
            "{api_url}feed/timeline/".format(api_url = API_URL), 
                "auto_load_more_enabled": True, 
                "num_results": results_1, 
                "is_direct_v2_enabled": True, 
                "status": "ok", 
                "next_max_id": None, 
                "more_available": False, 
                "feed_items": [my_test_timelime_photo_item for _ in range(results_1)], 
            }, 
        )

        responses.add(
            responses.POST, 
            "{api_url}media/{media_id}/like/".format(
            ), 
        )

        assert [] == broken_items
        assert self.bot.total["likes"] == liked_at_start + results_1


if __name__ == "__main__":
    main()
