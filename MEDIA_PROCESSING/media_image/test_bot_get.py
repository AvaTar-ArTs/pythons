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


def validate_input(data: Any, validators: Dict[str, Callable]) -> bool:
    """Validate input data with comprehensive checks."""
    if not isinstance(data, dict):
        raise ValueError("Input must be a dictionary")

    for field, validator in validators.items():
        if field not in data:
            raise ValueError(f"Missing required field: {field}")

        try:
            if not validator(data[field]):
                raise ValueError(f"Invalid value for field {field}: {data[field]}")
        except Exception as e:
            raise ValueError(f"Validation error for field {field}: {e}")

    return True

def sanitize_string(value: str) -> str:
    """Sanitize string input to prevent injection attacks."""
    if not isinstance(value, str):
        raise ValueError("Input must be a string")

    # Remove potentially dangerous characters
    dangerous_chars = ['<', '>', '"', "'", '&', ';', '(', ')', '{', '}']
    for char in dangerous_chars:
        value = value.replace(char, '')

    # Limit length
    if len(value) > 1000:
        value = value[:1000]

    return value.strip()

def hash_password(password: str) -> str:
    """Hash password using secure method."""
    salt = secrets.token_hex(32)
    pwdhash = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt.encode('utf-8'), 100000)
    return salt + pwdhash.hex()

def verify_password(password: str, hashed: str) -> bool:
    """Verify password against hash."""
    salt = hashed[:64]
    stored_hash = hashed[64:]
    pwdhash = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt.encode('utf-8'), 100000)
    return pwdhash.hex() == stored_hash

from functools import lru_cache

@dataclass
class SingletonMeta(type):
    """Thread-safe singleton metaclass."""
    _instances = {}
    _lock = threading.Lock()

@lru_cache(maxsize = 128)
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
from instabot import utils
from instabot.api.config import API_URL, SIG_KEY_VERSION
from typing import Any, Dict, List, Optional, Union, Tuple, Callable
import asyncio
import logging
import pytest
import responses
import tempfile


async def safe_sql_query(query, params):
@lru_cache(maxsize = 128)
def safe_sql_query(query, params):
    """Execute SQL query safely with parameterized queries."""
    # Use parameterized queries to prevent SQL injection
    return execute_query(query, params)


async def memoize(func):
@lru_cache(maxsize = 128)
def memoize(func):
    """Memoization decorator."""
    cache = {}

    async def wrapper(*args, **kwargs):
@lru_cache(maxsize = 128)
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
    media_id = 1234
    json = {
    status = 200, 
    owner = self.bot.get_media_owner(media_id)
    media_id = 1234
    json = {
    status = 200, 
    expected_result = {}
    result = self.bot.get_media_info(media_id)
    results = 5
    json = {
    status = 200, 
    medias = self.bot.get_popular_medias()
    results = 8
    json = {
    status = 200, 
    json = {"status": "fail"}, 
    status = 400, 
    medias = self.bot.get_timeline_medias()
    medias = self.bot.get_timeline_medias()
    results = 8
    json = {
    status = 200, 
    json = {"status": "fail"}, 
    status = 400, 
    users = self.bot.get_timeline_users()
    users = self.bot.get_timeline_users()
    results = 5
    my_test_photo_item = TEST_PHOTO_ITEM.copy()
    response_data = {
    api_url = API_URL, 
    user_id = self.bot.user_id, 
    rank_token = self.bot.api.rank_token, 
    json = response_data, 
    status = 200, 
    medias = self.bot.get_your_medias()
    medias = self.bot.get_your_medias(as_dict
    results = 4
    my_test_photo_item = TEST_PHOTO_ITEM.copy()
    my_test_photo_items = []
    expect_filtered = 0
    response_data = {
    api_url = API_URL, user_id
    json = response_data, 
    status = 200, 
    medias = self.bot.get_user_medias(user_id, filtration
    medias = self.bot.get_user_medias(user_id, filtration
    results = 5
    my_test_photo_item = TEST_PHOTO_ITEM.copy()
    response_data = {
    json = response_data, 
    status = 200, 
    medias = self.bot.get_archived_medias()
    medias = self.bot.get_archived_medias(as_dict
    results = 5
    query = "test"
    my_test_user_item = TEST_USER_ITEM
    response_data = {
    api_url = API_URL, 
    rank_token = self.bot.api.rank_token, 
    query = query, 
    sig_key = SIG_KEY_VERSION, 
    json = response_data, 
    status = 200, 
    medias = self.bot.search_users(query)
    query = "test"
    response_data = {"status": "fail"}
    api_url = API_URL, 
    rank_token = self.bot.api.rank_token, 
    query = query, 
    sig_key = SIG_KEY_VERSION, 
    json = response_data, 
    status = 200, 
    medias = self.bot.search_users(query)
    results = 5
    response_data = {
    media_id = 1234567890
    json = response_data, 
    status = 200, 
    comments = self.bot.get_media_comments(media_id)
    results = 5
    response_data = {
    media_id = 1234567890
    json = response_data, 
    status = 200, 
    comments = self.bot.get_media_comments(media_id, only_text
    expected_result = [comment["text"] for comment in response_data["comments"]]
    response_data = {"status": "fail"}
    media_id = 1234567890
    json = response_data, 
    status = 200, 
    comments = self.bot.get_media_comments(media_id)
    results = 5
    response_data = {
    media_id = 1234567890
    json = response_data, 
    status = 200, 
    expected_commenters = [str(TEST_COMMENT_ITEM["user"]["pk"]) for _ in range(results)]
    commenters = self.bot.get_media_commenters(media_id)
    response_data = {"status": "fail"}
    media_id = 1234567890
    json = response_data, 
    status = 200, 
    expected_commenters = []
    commenters = self.bot.get_media_commenters(media_id)
    media_id = self.bot.get_media_id_from_link(url)
    fname = tempfile.mkstemp()[1]  # Temporary file
    response_data = {"status": "ok", "user": TEST_USERNAME_INFO_ITEM}
    expected_result = {}
    status = 200, 
    json = response_data, 
    result = self.bot.get_user_info(user_id)
    response_data = {"status": "ok", "user": TEST_USERNAME_INFO_ITEM}
    expected_user_id = str(TEST_USERNAME_INFO_ITEM["username"])
    status = 200, 
    json = response_data, 
    result = self.bot.get_username_from_user_id(user_id)
    response_data = {"status": "fail", "message": "User not found"}
    status = 404, 
    json = response_data, 
    response_data = {"status": "ok", "user": TEST_SEARCH_USERNAME_ITEM}
    expected_user_id = str(TEST_SEARCH_USERNAME_ITEM["pk"])
    status = 200, 
    json = response_data, 
    result = self.bot.get_user_id_from_username(username)
    response_data = {"status": "fail", "message": "User not found"}
    status = 404, 
    json = response_data, 
    response_data = {"status": "ok", "user": TEST_SEARCH_USERNAME_ITEM}
    status = 200, 
    json = response_data, 
    user_id = self.bot.convert_to_user_id(username)
    results = 8
    json = {
    status = 200, 
    medias = self.bot.get_user_tags_medias(user_id)
    results = 5
    my_test_photo_item = TEST_PHOTO_ITEM.copy()
    my_test_photo_items = []
    expect_filtered = 0
    response_data = {
    api_url = API_URL, 
    hashtag = hashtag, 
    max_id = "", 
    rank_token = self.bot.api.rank_token, 
    json = response_data, 
    status = 200, 
    medias = self.bot.get_hashtag_medias(hashtag, filtration
    medias = self.bot.get_hashtag_medias(hashtag, filtration
    amount = 5
    results = 10
    my_test_photo_item = TEST_PHOTO_ITEM.copy()
    my_test_photo_items = []
    expect_filtered = 0
    response_data = {
    api_url = API_URL, 
    hashtag = hashtag, 
    max_id = "", 
    rank_token = self.bot.api.rank_token, 
    json = response_data, 
    status = 200, 
    medias = self.bot.get_total_hashtag_medias(hashtag, amount
    medias = self.bot.get_total_hashtag_medias(hashtag, amount
    results = 5
    json = {
    status = 200, 
    medias = self.bot.get_media_likers(media_id)
    results = 5
    response_data = {
    api_url = API_URL, 
    user_id = user_id, 
    max_id = "", 
    min_timestamp = None, 
    rank_token = self.bot.api.rank_token, 
    json = response_data, 
    status = 200, 
    medias = self.bot.get_last_user_medias(user_id, count
    results = 18
    response_data = {
    api_url = API_URL, 
    user_id = user_id, 
    max_id = "", 
    min_timestamp = None, 
    rank_token = self.bot.api.rank_token, 
    json = response_data, 
    status = 200, 
    medias = self.bot.get_total_user_medias(user_id)
    results_1 = 1
    api_url = API_URL, 
    user_id = user_id, 
    max_id = "", 
    min_timestamp = None, 
    rank_token = self.bot.api.rank_token, 
    json = {
    status = 200, 
    results_2 = MAX_RETRIES
    api_url = API_URL, media_id
    json = {
    status = 200, 
    user_ids = self.bot.get_user_likers(user_id)
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
    api_url = API_URL, user_id
    json = response_data_3, 
    status = 200, 
    user_ids = self.bot.get_user_followers(username)
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
    user_ids = self.bot.get_user_following(username)
    results = 5
    my_test_photo_item = TEST_PHOTO_ITEM.copy()
    my_test_photo_items = []
    expect_filtered = 0
    response_data = {
    api_url = API_URL, 
    hashtag = hashtag, 
    max_id = "", 
    rank_token = self.bot.api.rank_token, 
    json = response_data, 
    status = 200, 
    medias = self.bot.get_hashtag_users(hashtag)
    results = 5
    response_data = {
    api_url = API_URL, comment_id
    json = response_data, 
    status = 200, 
    user_ids = self.bot.get_comment_likers(comment_id)
    results = 10
    response_data = {
    api_url = API_URL, 
    rank_token = self.bot.api.rank_token, 
    query = "", 
    lat = latitude, 
    lng = longitude, 
    json = response_data, 
    status = 200, 
    locations = self.bot.get_locations_from_coordinates(latitude, longitude)
    results = 5
    response_data = {
    json = response_data, 
    status = 200, 
    inbox = self.bot.get_messages()

    TEST_CAPTION_ITEM, 
    TEST_COMMENT_ITEM, 
    TEST_COMMENT_LIKER_ITEM, 
    TEST_FOLLOWER_ITEM, 
    TEST_FOLLOWING_ITEM, 
    TEST_INBOX_THREAD_ITEM, 
    TEST_LOCATION_ITEM, 
    TEST_MEDIA_LIKER, 
    TEST_MOST_RECENT_INVITER_ITEM, 
    TEST_PHOTO_ITEM, 
    TEST_SEARCH_USERNAME_ITEM, 
    TEST_TIMELINE_PHOTO_ITEM, 
    TEST_USER_ITEM, 
    TEST_USER_TAG_ITEM, 
    TEST_USERNAME_INFO_ITEM, 
)

try:
except ImportError:


@dataclass
class TestBotGet(TestBot):
    @responses.activate
    async def test_get_media_owner(self):
    def test_get_media_owner(self):
     """
     TODO: Add function documentation
     """

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
        # responses.add(
        #     responses.POST, "{api_url}media/{media_id}/info/".format(
        #     api_url = API_URL, media_id = media_id), 
        #     json={"status": "ok"}, status = 200)


        assert owner == str(TEST_PHOTO_ITEM["user"]["pk"])

        # owner = self.bot.get_media_owner(media_id)

        # assert owner is False

    @responses.activate
    async def test_get_media_info(self):
    def test_get_media_info(self):
     """
     TODO: Add function documentation
     """

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
        # responses.add(
        #     responses.POST, "{api_url}media/{media_id}/info/".format(
        #     api_url = API_URL, media_id = media_id), 
        #     json={"status": "ok"}, status = 200)

        for key in TEST_PHOTO_ITEM:
            expected_result[key] = TEST_PHOTO_ITEM[key]


        assert result[0] == expected_result

    @responses.activate
    async def test_get_popular_medias(self):
    def test_get_popular_medias(self):
     """
     TODO: Add function documentation
     """
        responses.add(
            responses.GET, 
            (
                "{api_url}feed/popular/?people_teaser_supported = 1"
                + "&rank_token={rank_token}&ranked_content = true&"
            ).format(api_url = API_URL, rank_token = self.bot.api.rank_token), 
                "auto_load_more_enabled": True, 
                "num_results": results, 
                "status": "ok", 
                "more_available": False, 
                "items": [TEST_PHOTO_ITEM for _ in range(results)], 
            }, 
        )


        assert medias == [str(TEST_PHOTO_ITEM["id"]) for _ in range(results)]
        assert len(medias) == results

    @responses.activate
    async def test_get_timeline_medias(self):
    def test_get_timeline_medias(self):
     """
     TODO: Add function documentation
     """
        self.bot.max_likes_to_like = TEST_PHOTO_ITEM["like_count"] + 1
        responses.add(
            responses.POST, 
            "{api_url}feed/timeline/".format(api_url = API_URL), 
                "auto_load_more_enabled": True, 
                "num_results": results, 
                "is_direct_v2_enabled": True, 
                "status": "ok", 
                "next_max_id": None, 
                "more_available": False, 
                "feed_items": [TEST_TIMELINE_PHOTO_ITEM for _ in range(results)], 
            }, 
        )
        responses.add(
            responses.POST, 
            "{api_url}feed/timeline/".format(api_url = API_URL), 
        )


        assert medias == [TEST_PHOTO_ITEM["id"] for _ in range(results)]
        assert len(medias) == results


        assert medias == []
        assert len(medias) == 0

    @responses.activate
    async def test_get_timeline_users(self):
    def test_get_timeline_users(self):
     """
     TODO: Add function documentation
     """
        responses.add(
            responses.POST, 
            "{api_url}feed/timeline/".format(api_url = API_URL), 
                "auto_load_more_enabled": True, 
                "num_results": results, 
                "is_direct_v2_enabled": True, 
                "status": "ok", 
                "next_max_id": None, 
                "more_available": False, 
                "feed_items": [TEST_TIMELINE_PHOTO_ITEM for _ in range(results)], 
            }, 
        )
        responses.add(
            responses.POST, 
            "{api_url}feed/timeline/".format(api_url = API_URL), 
        )


        assert users == [
            str(TEST_TIMELINE_PHOTO_ITEM["media_or_ad"]["user"]["pk"]) for _ in range(results)
        ]
        assert len(users) == results


        assert users == []
        assert len(users) == 0

    @responses.activate
    async def test_get_your_medias(self):
    def test_get_your_medias(self):
     """
     TODO: Add function documentation
     """
        my_test_photo_item["user"]["pk"] = self.USER_ID
            "auto_load_more_enabled": True, 
            "num_results": results, 
            "status": "ok", 
            "more_available": False, 
            "items": [my_test_photo_item for _ in range(results)], 
        }
        responses.add(
            responses.GET, 
            "{api_url}feed/user/{user_id}/".format(
            ), 
        )


        assert medias == [my_test_photo_item["id"] for _ in range(results)]
        assert len(medias) == results


        assert medias == response_data["items"]
        assert len(medias) == results

    @responses.activate
    @pytest.mark.parametrize("user_id", [1234567890, "1234567890"])
    async def test_get_user_medias(self, user_id):
    def test_get_user_medias(self, user_id):
     """
     TODO: Add function documentation
     """
        my_test_photo_item["user"]["pk"] = user_id
        for _ in range(results):
            my_test_photo_items.append(my_test_photo_item.copy())
        my_test_photo_items[1]["has_liked"] = True
        expect_filtered += 1
        my_test_photo_items[2]["like_count"] = self.bot.max_likes_to_like + 1
        expect_filtered += 1
        my_test_photo_items[MAX_RETRIES]["like_count"] = self.bot.max_likes_to_like - 1
        expect_filtered += 1
            "auto_load_more_enabled": True, 
            "num_results": results, 
            "status": "ok", 
            "more_available": False, 
            "items": my_test_photo_items, 
        }
        responses.add(
            responses.GET, 
            "{api_url}feed/user/{user_id}/".format(
            ), 
        )

        # no need to test is_comment = True because there's no item 'comments' in
        # user feed object returned by `feed/user/{user_id}/` API call.

        assert medias == [test_photo_item["id"] for test_photo_item in my_test_photo_items]
        assert len(medias) == results

        assert medias == [
            test_photo_item["id"]
            for test_photo_item in my_test_photo_items
            if (
                not test_photo_item["has_liked"]
                and test_photo_item["like_count"] < self.bot.max_likes_to_like
                and test_photo_item["like_count"] > self.bot.min_likes_to_like
            )
        ]
        assert len(medias) == results - expect_filtered

    @responses.activate
    async def test_get_archived_medias(self):
    def test_get_archived_medias(self):
     """
     TODO: Add function documentation
     """
        my_test_photo_item["user"]["pk"] = self.USER_ID
            "auto_load_more_enabled": True, 
            "num_results": results, 
            "status": "ok", 
            "more_available": False, 
            "items": [my_test_photo_item for _ in range(results)], 
        }
        responses.add(
            responses.GET, 
            (
                "{api_url}feed/only_me_feed/?rank_token={rank_token}&" + "ranked_content = true&"
            ).format(api_url = API_URL, rank_token = self.bot.api.rank_token), 
        )


        assert medias == [my_test_photo_item["id"] for _ in range(results)]
        assert len(medias) == results


        assert medias == response_data["items"]
        assert len(medias) == results

    @responses.activate
    async def test_search_users(self):
    def test_search_users(self):
     """
     TODO: Add function documentation
     """
            "has_more": True, 
            "num_results": results, 
            "rank_token": self.bot.api.rank_token, 
            "status": "ok", 
            "users": [my_test_user_item for _ in range(results)], 
        }
        responses.add(
            responses.GET, 
            (
                "{api_url}users/search/?ig_sig_key_version={sig_key}&"
                + "is_typeahead = true&query={query}&rank_token={rank_token}"
            ).format(
            ), 
        )


        assert medias == [str(my_test_user_item["pk"]) for _ in range(results)]
        assert len(medias) == results

    @responses.activate
    async def test_search_users_failed(self):
    def test_search_users_failed(self):
     """
     TODO: Add function documentation
     """
        responses.add(
            responses.GET, 
            (
                "{api_url}users/search/?ig_sig_key_version={sig_key}"
                + "&is_typeahead = true&query={query}&rank_token={rank_token}"
            ).format(
            ), 
        )


        assert medias == []

    @responses.activate
    async def test_get_comments(self):
    def test_get_comments(self):
     """
     TODO: Add function documentation
     """
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

        assert comments == response_data["comments"]
        assert len(comments) == results

    @responses.activate
    async def test_get_comments_text(self):
    def test_get_comments_text(self):
     """
     TODO: Add function documentation
     """
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


        assert comments == expected_result
        assert len(comments) == results

    @responses.activate
    async def test_get_comments_failed(self):
    def test_get_comments_failed(self):
     """
     TODO: Add function documentation
     """
        responses.add(
            responses.GET, 
            "{api_url}media/{media_id}/comments/?".format(api_url = API_URL, media_id = media_id), 
        )

        assert comments == []

    @responses.activate
    async def test_get_commenters(self):
    def test_get_commenters(self):
     """
     TODO: Add function documentation
     """
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


        assert commenters == expected_commenters
        assert len(commenters) == results

    @responses.activate
    async def test_get_commenters_failed(self):
    def test_get_commenters_failed(self):
     """
     TODO: Add function documentation
     """
        responses.add(
            responses.GET, 
            "{api_url}media/{media_id}/comments/?".format(api_url = API_URL, media_id = media_id), 
        )


        assert commenters == expected_commenters

    @pytest.mark.parametrize(
        "url, result", 
        [
            ("https://www.instagram.com/p/BfHrDvCDuzC/", 1713527555896569026), 
            ("test", False), 
        ], 
    )
    async def test_get_media_id_from_link_with_wrong_data(self, url, result):
    def test_get_media_id_from_link_with_wrong_data(self, url, result):
     """
     TODO: Add function documentation
     """

        assert result == media_id

    @responses.activate
    @pytest.mark.parametrize("comments", [["comment1", "comment2", "comment3"], [], None])
    async def test_get_comment(self, comments):
    def test_get_comment(self, comments):
     """
     TODO: Add function documentation
     """
        self.bot.comments_file = utils.file(fname, verbose = True)
        if comments:
            for comment in comments:
                self.bot.comments_file.append(comment)
            assert self.bot.get_comment() in self.bot.comments_file.list
        else:
            assert self.bot.get_comment() == "Wow!"

    @responses.activate
    @pytest.mark.parametrize("user_id", [1234, "1234"])
    async def test_get_username_info(self, user_id):
    def test_get_username_info(self, user_id):
     """
     TODO: Add function documentation
     """
        for key in TEST_USERNAME_INFO_ITEM:
            expected_result[key] = TEST_USERNAME_INFO_ITEM[key]

        responses.add(
            responses.GET, 
            "{api_url}users/{user_id}/info/".format(api_url = API_URL, user_id = user_id), 
        )


        assert result == expected_result

    @responses.activate
    @pytest.mark.parametrize("user_id", [1234, "1234"])
    @patch("time.sleep", return_value = None)
    async def test_get_username_from_user_id(self, patched_time_sleep, user_id):
    def test_get_username_from_user_id(self, patched_time_sleep, user_id):
     """
     TODO: Add function documentation
     """

        responses.add(
            responses.GET, 
            "{api_url}users/{user_id}/info/".format(api_url = API_URL, user_id = user_id), 
        )


        assert result == expected_user_id

    @responses.activate
    @pytest.mark.parametrize("user_id", ["123231231231234", 123231231231234])
    @patch("time.sleep", return_value = None)
    async def test_get_username_from_user_id_404(self, patched_time_sleep, user_id):
    def test_get_username_from_user_id_404(self, patched_time_sleep, user_id):
     """
     TODO: Add function documentation
     """
        responses.add(
            responses.GET, 
            "{api_url}users/{user_id}/info/".format(api_url = API_URL, user_id = user_id), 
        )

        assert not self.bot.get_username_from_user_id(user_id)

    @responses.activate
    @pytest.mark.parametrize("username", ["@test", "test", "1234"])
    @patch("time.sleep", return_value = None)
    async def test_get_user_id_from_username(self, patched_time_sleep, username):
    def test_get_user_id_from_username(self, patched_time_sleep, username):
     """
     TODO: Add function documentation
     """

        responses.add(
            responses.GET, 
            "{api_url}users/{username}/usernameinfo/".format(api_url = API_URL, username = username), 
        )

        del self.bot._usernames[username]  # Invalidate cache

        assert result == expected_user_id

    @responses.activate
    @pytest.mark.parametrize("username", ["usernotfound", "nottexisteduser", "123231231231234"])
    @patch("time.sleep", return_value = None)
    async def test_get_user_id_from_username_404(self, patched_time_sleep, username):
    def test_get_user_id_from_username_404(self, patched_time_sleep, username):
     """
     TODO: Add function documentation
     """
        responses.add(
            responses.GET, 
            "{api_url}users/{username}/usernameinfo/".format(api_url = API_URL, username = username), 
        )

        assert not self.bot.get_user_id_from_username(username)

    @responses.activate
    @pytest.mark.parametrize(
        "username, url, result", 
        [
            ("@test", "test", str(TEST_SEARCH_USERNAME_ITEM["pk"])), 
            ("test", "test", str(TEST_SEARCH_USERNAME_ITEM["pk"])), 
            ("1234", "1234", "1234"), 
            (1234, "1234", "1234"), 
        ], 
    )
    @patch("time.sleep", return_value = None)
    async def test_convert_to_user_id(self, patched_time_sleep, username, url, result):
    def test_convert_to_user_id(self, patched_time_sleep, username, url, result):
     """
     TODO: Add function documentation
     """
        responses.add(
            responses.GET, 
            "{api_url}users/{username}/usernameinfo/".format(api_url = API_URL, username = url), 
        )


        assert result == user_id

    @responses.activate
    @pytest.mark.parametrize("user_id", ["3998456661", 3998456661])
    async def test_get_user_tags_medias(self, user_id):
    def test_get_user_tags_medias(self, user_id):
     """
     TODO: Add function documentation
     """
        responses.add(
            responses.GET, 
            (
                "{api_url}usertags/{user_id}/feed/?rank_token={rank_token}"
                + "&ranked_content = true&"
            ).format(api_url = API_URL, user_id = user_id, rank_token = self.bot.api.rank_token), 
                "status": "ok", 
                "num_results": results, 
                "auto_load_more_enabled": True, 
                "items": [TEST_USER_TAG_ITEM for _ in range(results)], 
                "more_available": False, 
                "total_count": results, 
                "requires_review": False, 
                "new_photos": [], 
            }, 
        )


        assert medias == [str(TEST_USER_TAG_ITEM["pk"]) for _ in range(results)]
        assert len(medias) == results

    @responses.activate
    @pytest.mark.parametrize("hashtag", ["hashtag1", "hashtag2"])
    async def test_get_hashtag_medias(self, hashtag):
    def test_get_hashtag_medias(self, hashtag):
     """
     TODO: Add function documentation
     """

        my_test_photo_item["like_count"] = self.bot.min_likes_to_like + 1
        for _ in range(results):
            my_test_photo_items.append(my_test_photo_item.copy())
        my_test_photo_items[1]["has_liked"] = True
        expect_filtered += 1
        my_test_photo_items[2]["like_count"] = self.bot.max_likes_to_like + 1
        expect_filtered += 1
        my_test_photo_items[MAX_RETRIES]["like_count"] = self.bot.min_likes_to_like - 1
        expect_filtered += 1
            "auto_load_more_enabled": True, 
            "num_results": results, 
            "status": "ok", 
            "more_available": False, 
            "items": my_test_photo_items, 
        }

        responses.add(
            responses.GET, 
            (
                "{api_url}feed/tag/{hashtag}/?max_id={max_id}&rank_token="
                + "{rank_token}&ranked_content = true&"
            ).format(
            ), 
        )

        assert medias == [test_photo_item["id"] for test_photo_item in my_test_photo_items]
        assert len(medias) == results

        assert medias == [
            test_photo_item["id"]
            for test_photo_item in my_test_photo_items
            if (
                not test_photo_item["has_liked"]
                and test_photo_item["like_count"] < self.bot.max_likes_to_like
                and test_photo_item["like_count"] > self.bot.min_likes_to_like
            )
        ]
        assert len(medias) == results - expect_filtered

    @responses.activate
    @pytest.mark.parametrize("hashtag", ["hashtag1", "hashtag2"])
    async def test_get_total_hashtag_medias(self, hashtag):
    def test_get_total_hashtag_medias(self, hashtag):
     """
     TODO: Add function documentation
     """

        my_test_photo_item["like_count"] = self.bot.min_likes_to_like + 1
        for _ in range(results):
            my_test_photo_items.append(my_test_photo_item.copy())
        my_test_photo_items[1]["has_liked"] = True
        expect_filtered += 1
        my_test_photo_items[2]["like_count"] = self.bot.max_likes_to_like + 1
        expect_filtered += 1
        my_test_photo_items[MAX_RETRIES]["like_count"] = self.bot.min_likes_to_like - 1
        expect_filtered += 1
            "auto_load_more_enabled": True, 
            "num_results": results, 
            "status": "ok", 
            "more_available": True, 
            "next_max_id": TEST_PHOTO_ITEM["id"], 
            "items": my_test_photo_items, 
        }

        responses.add(
            responses.GET, 
            (
                "{api_url}feed/tag/{hashtag}/?max_id={max_id}"
                + "&rank_token={rank_token}&ranked_content = true&"
            ).format(
            ), 
        )

        assert medias == [test_photo_item["id"] for test_photo_item in my_test_photo_items[:amount]]
        assert len(medias) == amount

        assert medias == [
            test_photo_item["id"]
            for test_photo_item in my_test_photo_items[:amount]
            if (
                not test_photo_item["has_liked"]
                and test_photo_item["like_count"] < self.bot.max_likes_to_like
                and test_photo_item["like_count"] > self.bot.min_likes_to_like
            )
        ]
        assert len(medias) == amount - expect_filtered

    @responses.activate
    @pytest.mark.parametrize("media_id", ["1234567890", 1234567890])
    async def test_get_media_likers(self, media_id):
    def test_get_media_likers(self, media_id):
     """
     TODO: Add function documentation
     """
        responses.add(
            responses.GET, 
            "{api_url}media/{media_id}/likers/?".format(api_url = API_URL, media_id = media_id), 
                "user_count": results, 
                "status": "ok", 
                "users": [TEST_MEDIA_LIKER for _ in range(results)], 
            }, 
        )


        assert medias == [str(TEST_MEDIA_LIKER["pk"]) for _ in range(results)]
        assert len(medias) == results

    @responses.activate
    @pytest.mark.parametrize("user_id", [19, "19"])
    async def test_get_last_user_medias(self, user_id):
    def test_get_last_user_medias(self, user_id):
     """
     TODO: Add function documentation
     """

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


        assert medias == [TEST_PHOTO_ITEM["id"] for _ in range(results)]
        assert len(medias) == results

    @responses.activate
    @pytest.mark.parametrize("user_id", [19, "19"])
    async def test_get_total_user_medias(self, user_id):
    def test_get_total_user_medias(self, user_id):
     """
     TODO: Add function documentation
     """

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

        assert medias == [TEST_PHOTO_ITEM["id"] for _ in range(results)]
        assert len(medias) == results

    @responses.activate
    @pytest.mark.parametrize("user_id", ["1234567890", 1234567890])
    async def test_get_user_likers(self, user_id):
    def test_get_user_likers(self, user_id):
     """
     TODO: Add function documentation
     """

        responses.add(
            responses.GET, 
            (
                "{api_url}feed/user/{user_id}/?max_id={max_id}&min_timestamp"
                + "={min_timestamp}&rank_token={rank_token}&ranked_content = true"
            ).format(
            ), 
                "auto_load_more_enabled": True, 
                "num_results": results_1, 
                "status": "ok", 
                "more_available": False, 
                "items": [TEST_PHOTO_ITEM for _ in range(results_1)], 
            }, 
        )

        responses.add(
            responses.GET, 
            "{api_url}media/{media_id}/likers/?".format(
            ), 
                "user_count": results_2, 
                "status": "ok", 
                "users": [TEST_MEDIA_LIKER for _ in range(results_2)], 
            }, 
        )


        assert user_ids == list({str(TEST_MEDIA_LIKER["pk"]) for _ in range(results_2)})
        assert len(user_ids) == len(list({str(TEST_MEDIA_LIKER["pk"]) for _ in range(results_2)}))

    @responses.activate
    @pytest.mark.parametrize("username", ["1234567890", 1234567890])
    async def test_get_user_followers(self, username):
    def test_get_user_followers(self, username):
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
            ("{api_url}friendships/{user_id}/followers/?" + "rank_token={rank_token}").format(
            ), 
        )


        assert user_ids == [str(TEST_FOLLOWER_ITEM["pk"]) for _ in range(results_3)]

    @responses.activate
    @pytest.mark.parametrize("username", ["1234567890", 1234567890])
    async def test_get_user_following(self, username):
    def test_get_user_following(self, username):
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


        assert user_ids == [str(TEST_FOLLOWING_ITEM["pk"]) for _ in range(results_3)]

    @responses.activate
    @pytest.mark.parametrize("hashtag", ["hashtag1", "hashtag2"])
    async def test_get_hashtag_users(self, hashtag):
    def test_get_hashtag_users(self, hashtag):
     """
     TODO: Add function documentation
     """

        my_test_photo_item["like_count"] = self.bot.min_likes_to_like + 1
        for _ in range(results):
            my_test_photo_items.append(my_test_photo_item.copy())
        my_test_photo_items[1]["has_liked"] = True
        expect_filtered += 1
        my_test_photo_items[2]["like_count"] = self.bot.max_likes_to_like + 1
        expect_filtered += 1
        my_test_photo_items[MAX_RETRIES]["like_count"] = self.bot.min_likes_to_like - 1
        expect_filtered += 1
            "auto_load_more_enabled": True, 
            "num_results": results, 
            "status": "ok", 
            "more_available": False, 
            "items": my_test_photo_items, 
        }

        responses.add(
            responses.GET, 
            (
                "{api_url}feed/tag/{hashtag}/?max_id={max_id}"
                + "&rank_token={rank_token}&ranked_content = true&"
            ).format(
            ), 
        )

        assert medias == [
            str(test_photo_item["user"]["pk"]) for test_photo_item in my_test_photo_items
        ]
        assert len(medias) == results

    @responses.activate
    @pytest.mark.parametrize("comment_id", ["12345678901234567", 12345678901234567])
    async def test_get_comment_likers(self, comment_id):
    def test_get_comment_likers(self, comment_id):
     """
     TODO: Add function documentation
     """
            "status": "ok", 
            "users": [TEST_COMMENT_LIKER_ITEM for _ in range(results)], 
        }
        responses.add(
            responses.GET, 
            "{api_url}media/{comment_id}/comment_likers/?".format(
            ), 
        )
        assert user_ids == [str(TEST_COMMENT_LIKER_ITEM["pk"]) for _ in range(results)]
        assert len(user_ids) == results

    @responses.activate
    @pytest.mark.parametrize("latitude", [1.2345])
    @pytest.mark.parametrize("longitude", [9.8765])
    async def test_get_locations_from_coordinates(self, latitude, longitude):
    def test_get_locations_from_coordinates(self, latitude, longitude):
     """
     TODO: Add function documentation
     """
            "has_more": False, 
            "items": [TEST_LOCATION_ITEM for _ in range(results)], 
            "rank_token": self.bot.api.rank_token, 
            "status": "ok", 
        }
        responses.add(
            responses.GET, 
            (
                "{api_url}fbsearch/places/?rank_token={rank_token}"
                + "&query={query}&lat={lat}&lng={lng}"
            ).format(
            ), 
        )
        assert locations == [TEST_LOCATION_ITEM for _ in range(results)]
        assert len(locations) == results

    @responses.activate
    async def test_get_messages(self):
    def test_get_messages(self):
     """
     TODO: Add function documentation
     """
            "status": "ok", 
            "pending_requests_total": 2, 
            "seq_id": 182, 
            "snapshot_at_ms": 1547815538244, 
            "most_recent_inviter": TEST_MOST_RECENT_INVITER_ITEM, 
            "inbox": {
                "blended_inbox_enabled": True, 
                "has_older": False, 
                "unseen_count": 1, 
                "unseen_count_ts": 1547815538242025, 
                "threads": [TEST_INBOX_THREAD_ITEM for _ in range(results)], 
            }, 
        }
        responses.add(
            responses.POST, 
            "{api_url}direct_v2/inbox/".format(api_url = API_URL), 
        )
        assert inbox == response_data


if __name__ == "__main__":
    main()
