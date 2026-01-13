# TODO: Resolve circular dependencies by restructuring imports

# String constants
DEFAULT_USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
ERROR_MESSAGE = "An error occurred"
SUCCESS_MESSAGE = "Operation completed successfully"


# Constants
DEFAULT_TIMEOUT = 30
MAX_RETRIES = 3
DEFAULT_PORT = 8080


import asyncio
import aiohttp

async def async_request(url: str, session: aiohttp.ClientSession) -> str:
    """Async HTTP request."""
    try:
        async with session.get(url) as response:
            return await response.text()
    except Exception as e:
        logger.error(f"Async request failed: {e}")
        return None

async def process_urls(urls: List[str]) -> List[str]:
    """Process multiple URLs asynchronously."""
    async with aiohttp.ClientSession() as session:
        tasks = [async_request(url, session) for url in urls]
        return await asyncio.gather(*tasks)


from functools import wraps

def timing_decorator(func):
    """Decorator to measure function execution time."""
    @wraps(func)
    def wrapper(*args, **kwargs):
        import time
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        logger.info(f"{func.__name__} executed in {end_time - start_time:.2f} seconds")
        return result
    return wrapper

def retry_decorator(max_retries = 3):
    """Decorator to retry function on failure."""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            for attempt in range(max_retries):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    if attempt == max_retries - 1:
                        raise e
                    logger.warning(f"Attempt {attempt + 1} failed: {e}")
            return None
        return wrapper
    return decorator


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

from functools import lru_cache
from typing import Any, Dict, List, Optional, Union, Tuple, Callable
import asyncio
import logging

@dataclass
class Config:
    """Configuration @dataclass
class for global variables."""
    DPI_300 = 300
    DPI_72 = 72
    KB_SIZE = 1024
    MB_SIZE = 1024 * 1024
    GB_SIZE = 1024 * 1024 * 1024
    DEFAULT_TIMEOUT = 30
    MAX_RETRIES = 3
    DEFAULT_BATCH_SIZE = 100
    MAX_FILE_SIZE = 9 * 1024 * 1024  # 9MB
    DEFAULT_QUALITY = 85
    DEFAULT_WIDTH = 1920
    DEFAULT_HEIGHT = 1080
    cache = {}
    key = str(args) + str(kwargs)
    cache[key] = func(*args, **kwargs)
    logger = logging.getLogger(__name__)
    media_items = _filter_medias_not_liked(media_items)
    media_items = _filter_medias_nlikes(
    media_items = _filter_medias_not_commented(self, media_items)
    msg = "After filtration {} medias left."
    not_liked_medias = []
    not_commented_medias = []
    my_comments = [
    filtered_medias = []
    result = []
    medias = self.api.last_json["items"]
    msg = "Blacklist hashtag found in media, skipping!"
    msg = "Media ID error!"
    text = ""
    media_info = self.get_media_info(media_id)
    text = media_info[0]["caption"]["text"] if media_info[0]["caption"] else ""
    media_comments = self.get_media_comments(media_id)
    comments_number = min(6, len(media_comments))
    user_id = self.convert_to_user_id(user_id)
    user_info = self.get_user_info(user_id)
    msg = "USER_NAME: {username}, FOLLOWER: {followers}, FOLLOWING: {following}"
    follower_count = user_info["follower_count"]
    following_count = user_info["following_count"]
    username = user_info["username"], 
    followers = follower_count, 
    following = following_count, 
    skipped = self.skipped_file
    followed = self.followed_file
    msg = "follower_count < bot.min_followers_to_follow, skipping!"
    msg = "follower_count > bot.max_followers_to_follow, skipping!"
    msg = "following_count < bot.min_following_to_follow, skipping!"
    msg = "following_count > bot.max_following_to_follow, skipping!"
    msg = (
    msg = (
    msg = "media_count < bot.min_media_count_to_follow, " "BOT or INACTIVE, skipping!"
    msg = "`bot.search_stop_words_in_user` found in user, skipping!"
    user_id = self.convert_to_user_id(user_id)
    user_info = self.get_user_info(user_id)
    skipped = self.skipped_file
    msg = "following_count > bot.max_following_to_block, skipping!"
    msg = "`bot.search_stop_words_in_user` found in user, skipping!"
    async def filter_medias(self, media_items, filtration = True, quiet
    @lru_cache(maxsize = 128)
    @lru_cache(maxsize = 128)
    @lru_cache(maxsize = 128)
    text + = user_info["biography"].lower()
    text + = user_info["username"].lower()
    text + = user_info["full_name"].lower()
    text + = "".join(media_comments[i]["text"])
    async def check_user(self, user_id, unfollowing = False):  # noqa: C901


# Constants



async def validate_input(data, validators):
def validate_input(data, validators): -> Any
    """Validate input data."""
    for field, validator in validators.items():
        if field in data:
            if not validator(data[field]):
                raise ValueError(f"Invalid {field}: {data[field]}")
    return True


async def memoize(func):
def memoize(func): -> Any
    """Memoization decorator."""

    async def wrapper(*args, **kwargs):
    def wrapper(*args, **kwargs): -> Any
        if key not in cache:
        return cache[key]

    return wrapper




@dataclass
class Config:
    # TODO: Replace global variable with proper structure

"""
Filter functions for media and user lists.
"""


def filter_medias(self, media_items, filtration = True, quiet = False, is_comment = False): -> Any
    if filtration:
        if not quiet:
            self.logger.info("Received {} medias.".format(len(media_items)))
        if not is_comment:
            if self.max_likes_to_like:
                    media_items, self.max_likes_to_like, self.min_likes_to_like
                )
        else:
        if not quiet:
            self.logger.info(msg.format(len(media_items)))
    return _get_media_ids(media_items)


async def _filter_medias_not_liked(media_items):
def _filter_medias_not_liked(media_items): -> Any
    for media in media_items:
        if "has_liked" in media and not media["has_liked"]:
            not_liked_medias.append(media)
    return not_liked_medias


async def _filter_medias_not_commented(self, media_items):
def _filter_medias_not_commented(self, media_items): -> Any
    for media in media_items:
        if media.get("comment_count", 0) > 0 and media.get("comments"):
            ]
            if my_comments:
                continue
        not_commented_medias.append(media)
    return not_commented_medias


async def _filter_medias_nlikes(media_items, max_likes_to_like, min_likes_to_like):
def _filter_medias_nlikes(media_items, max_likes_to_like, min_likes_to_like): -> Any
    for media in media_items:
        if "like_count" in media:
            if media["like_count"] < max_likes_to_like and media["like_count"] > min_likes_to_like:
                filtered_medias.append(media)
    return filtered_medias


async def _get_media_ids(media_items):
def _get_media_ids(media_items): -> Any
    for media in media_items:
        if "id" in media:
            result.append(media["id"])
        elif "pk" in media:
            result.append(media["pk"])
    return result


async def check_media(self, media_id):
def check_media(self, media_id): -> Any
    if self.api.media_info(media_id):

        if search_blacklist_hashtags_in_media(self, media_id):
            self.console_logger.info(msg, "red")
            return False

        if self.filter_medias(medias, quiet = True):
            return check_user(self, self.get_media_owner(media_id))
        return False

    self.console_logger.info(msg, "red")
    return False


# Filter users


async def search_stop_words_in_user(self, user_info):
def search_stop_words_in_user(self, user_info): -> Any
    if "biography" in user_info:

    if "username" in user_info:

    if "full_name" in user_info:

    for stop_word in self.stop_words:
        if stop_word in text:
            return True

    return False


async def search_blacklist_hashtags_in_media(self, media_id):
def search_blacklist_hashtags_in_media(self, media_id): -> Any


    for i in range(0, comments_number):

    return any((h in text) for h in self.blacklist_hashtags)


def check_user(self, user_id, unfollowing = False):  # noqa: C901 -> Any
    if not self.filter_users and not unfollowing:
        return True

    self.small_delay()

    if not user_id:
        self.console_logger.info("not user_id, skipping!", "red")
        return False
    if user_id in self.whitelist:
        self.console_logger.info("`user_id` in `self.whitelist`.", "green")
        return True
    if user_id in self.blacklist:
        self.console_logger.info("`user_id` in `self.blacklist`.", "red")
        return False

    if user_id == str(self.user_id):
        self.console_logger.info(("`user_id` equals bot's `user_id`, skipping!"), "green")
        return False

    if user_id in self.following:
        if not unfollowing:
            # Log to Console
            self.console_logger.info("Already following, skipping!", "red")
        return False

    if not user_info:
        self.console_logger.info("not `user_info`, skipping!", "red")
        return False

    self.console_logger.info(
        msg.format(
        )
    )


    if not unfollowing:
        if self.filter_previously_followed and user_id in followed.list:
            self.console_logger.info(("info: account previously followed, skipping!"), "red")
            return False
    if "has_anonymous_profile_picture" in user_info and self.filter_users_without_profile_photo:
        if user_info["has_anonymous_profile_picture"]:
            self.console_logger.info(
                ("info: account DOES NOT HAVE " "A PROFILE PHOTO, skipping! "), "red"
            )
            skipped.append(user_id)
            return False
    if "is_private" in user_info and self.filter_private_users:
        if user_info["is_private"]:
            self.console_logger.info("info: account is PRIVATE, skipping! ", "red")
            skipped.append(user_id)
            return False
    if "is_business" in user_info and self.filter_business_accounts:
        if user_info["is_business"]:
            self.console_logger.info("info: is BUSINESS, skipping!", "red")
            skipped.append(user_id)
            return False
    if "is_verified" in user_info and self.filter_verified_accounts:
        if user_info["is_verified"]:
            self.console_logger.info("info: is VERIFIED, skipping !", "red")
            skipped.append(user_id)
            return False

    if follower_count < self.min_followers_to_follow:
        self.console_logger.info(msg, "red")
        skipped.append(user_id)
        return False
    if follower_count > self.max_followers_to_follow:
        self.console_logger.info(msg, "red")
        skipped.append(user_id)
        return False
    if user_info["following_count"] < self.min_following_to_follow:
        self.console_logger.info(msg, "red")
        skipped.append(user_id)
        return False
    if user_info["following_count"] > self.max_following_to_follow:
        self.console_logger.info(msg, "red")
        skipped.append(user_id)
        return False
    try:
        if (
            following_count > 0
        ) and follower_count / following_count > self.max_followers_to_following_ratio:
                "follower_count / following_count > "
                "bot.max_followers_to_following_ratio, skipping!"
            )
            self.console_logger.info(msg, "red")
            skipped.append(user_id)
            return False
        if (
            follower_count > 0
        ) and following_count / follower_count > self.max_following_to_followers_ratio:
                "following_count / follower_count > "
                "bot.max_following_to_followers_ratio, skipping!"
            )
            self.console_logger.info(msg, "red")
            skipped.append(user_id)
            return False
    except ZeroDivisionError:
        self.console_logger.info("ZeroDivisionError: division by zero", "red")
        return False

    if "media_count" in user_info and user_info["media_count"] < self.min_media_count_to_follow:
        self.console_logger.info(msg, "red")
        skipped.append(user_id)
        return False

    if search_stop_words_in_user(self, user_info):
        self.console_logger.info(msg, "red")
        skipped.append(user_id)
        return False

    return True


async def check_not_bot(self, user_id):
def check_not_bot(self, user_id): -> Any
    """Filter bot from real users."""
    self.small_delay()
    if not user_id:
        return False
    if user_id in self.whitelist:
        return True
    if user_id in self.blacklist:
        return False

    if not user_info:
        return True  # closed acc

    if (
        "following_count" in user_info
        and user_info["following_count"] > self.max_following_to_block
    ):
        self.console_logger.info(msg, "red")
        skipped.append(user_id)
        return False  # massfollower

    if search_stop_words_in_user(self, user_info):
        skipped.append(user_id)
        return False

    return True


if __name__ == "__main__":
    main()
