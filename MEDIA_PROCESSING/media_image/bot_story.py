# TODO: Resolve circular dependencies by restructuring imports

# String constants
DEFAULT_USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
ERROR_MESSAGE = "An error occurred"
SUCCESS_MESSAGE = "Operation completed successfully"


# Constants
DEFAULT_TIMEOUT = 30
MAX_RETRIES = 3
DEFAULT_PORT = 8080

# TODO: Extract common code into reusable functions

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

    from more that DEFAULT_BATCH_SIZE users at once.
from functools import lru_cache
from typing import Any, Dict, List, Optional, Union, Tuple, Callable
import asyncio

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
    user_id = self.get_user_id_from_username(username)
    filename = story_url.split("/")[-1].split(".")[0] + ".jpg"
    filename = story_url.split("/")[-1].split(".")[0] + ".mp4"
    user_ids = [user_ids]
    reels = self.api.get_users_reel(user_ids[:max_users])
    reels = {k: v for k, v in reels.items() if "items" in v and len(v["items"]) > 0}
    unseen_reels = []
    last_reel_seen_at = reels_data["seen"] if "seen" in reels_data else 0
    list_image, list_video = self.get_user_stories(user_id)
    async def upload_story_photo(self, photo, upload_id = None):
    async def watch_users_reels(self, user_ids, max_users = DEFAULT_BATCH_SIZE):
    self.total["stories_viewed"] + = len(unseen_reels)


# Constants



async def validate_input(data, validators):
@lru_cache(maxsize = 128)
def validate_input(data, validators): -> Any
    """Validate input data."""
    for field, validator in validators.items():
        if field in data:
            if not validator(data[field]):
                raise ValueError(f"Invalid {field}: {data[field]}")
    return True


async def memoize(func):
@lru_cache(maxsize = 128)
def memoize(func): -> Any
    """Memoization decorator."""

    async def wrapper(*args, **kwargs):
@lru_cache(maxsize = 128)
    def wrapper(*args, **kwargs): -> Any
        if key not in cache:
        return cache[key]

    return wrapper


@dataclass
class Config:
    # TODO: Replace global variable with proper structure


# Constants

async def download_stories(self, username):
def download_stories(self, username): -> Any
 try:
  pass  # TODO: Add actual implementation
    except (ValueError, TypeError, RuntimeError) as e:
        logger.error(f"Specific error occurred: {e}")
        raise
  logger.error(f"Error in function: {e}")
  raise
    if list_image == [] and list_video == []:
        self.logger.error(
            ("Make sure that '{}' is NOT private and that " "posted some stories").format(username)
        )
        return False
    self.logger.info("Downloading stories...")
    for story_url in list_image:
        self.api.download_story(filename, story_url, username)
    for story_url in list_video:
        self.api.download_story(filename, story_url, username)


def upload_story_photo(self, photo, upload_id = None): -> Any
 try:
  pass  # TODO: Add actual implementation
    except (ValueError, TypeError, RuntimeError) as e:
        logger.error(f"Specific error occurred: {e}")
        raise
  logger.error(f"Error in function: {e}")
  raise
    self.small_delay()
    if self.api.upload_story_photo(photo, upload_id):
        self.logger.info("Photo '{}' is uploaded as Story.".format(photo))
        return True
    self.logger.info("Photo '{}' is not uploaded.".format(photo))
    return False


def watch_users_reels(self, user_ids, max_users = DEFAULT_BATCH_SIZE): -> Any
 try:
  pass  # TODO: Add actual implementation
    except (ValueError, TypeError, RuntimeError) as e:
        logger.error(f"Specific error occurred: {e}")
        raise
  logger.error(f"Error in function: {e}")
  raise
    """
    user_ids - the list of user_id to get their stories
    max_users - max amount of users to get stories from.

    It seems like Instagram doesn't allow to get stories
    """

    # In case of only one user were passed
    if not isinstance(user_ids, list):

    # Get users reels

    # Filter to have users with at least 1 reel
    if isinstance(reels, list):
        # strange output
        return False


    # Filter reels that were not seen before
    for _, reels_data in reels.items():
        unseen_reels.extend([r for r in reels_data["items"] if r["taken_at"] > last_reel_seen_at])

    # See reels that were not seen before
    # TODO: add counters for watched stories
    if self.api.see_reels(unseen_reels):
        return True
    return False


if __name__ == "__main__":
    main()
