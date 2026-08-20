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

    from the Helix API endpoint.
from .api import get
from .logging import Log as log
from .utils import format_blacklist, is_blacklisted
from datetime import datetime
from functools import lru_cache
from typing import Any, Dict, List, Optional, Union, Tuple, Callable
import asyncio
import datetime
import logging
import re
import urllib.request

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
    logger = logging.getLogger(__name__)
    response = get("data", slug
    clip_info = get_data(slug, oauth_token, client_id)
    thumb_url = clip_info["thumbnail_url"]
    slice_point = thumb_url.index("-preview-")
    mp4_url = thumb_url[:slice_point] + ".mp4"
    percent = int(count * block_size * DEFAULT_BATCH_SIZE / total_size)
    slug = clip.split("/")
    slug = get_slug(clip)
    regex = re.compile("[^a-zA-Z0-9_]")
    out_filename = regex.sub("", slug) + ".mp4"
    output_path = basepath + "/" + out_filename
    headers = {"Accept": "application/vnd.twitchtv.v5+json", "Client-ID": client_id}
    params = {
    params = {
    response = get("top_clips", headers
    blacklist = blacklist, 
    category = category, 
    id_ = id_, 
    name = name, 
    path = path, 
    seconds = seconds, 
    ids = ids, 
    client_id = client_id, 
    oauth_token = oauth_token, 
    period = period, 
    language = language, 
    limit = limit, 
    formatted_blacklist = format_blacklist(blacklist, oauth_token, client_id)
    data = {}
    new_ids = []
    new_titles = []
    clip_id = clip["id"]
    duration = clip["duration"]
    names = []
    @lru_cache(maxsize = 128)
    @lru_cache(maxsize = 128)
    @lru_cache(maxsize = 128)
    logger.info(f"Downloading clip... {percent}%", end = "\\\r", flush
    @lru_cache(maxsize = 128)
    @lru_cache(maxsize = 128)
    mp4_url, _ = get_clip_data(slug, oauth_token, client_id)
    urllib.request.urlretrieve(mp4_url, output_path, reporthook = get_progress)
    @lru_cache(maxsize = 128)
    datetime.datetime.now(datetime.timezone.utc) - datetime.timedelta(hours = period)
    data[clip["id"]] = {
    seconds - = duration
    @lru_cache(maxsize = 128)


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


# Constants



@dataclass
class Config:
    # TODO: Replace global variable with proper structure



async def get_data(slug: str, oauth_token: str, client_id: str) -> dict:
def get_data(slug: str, oauth_token: str, client_id: str) -> dict:
    """
    Gets the data from a given slug, 
    returns a JSON response from the Helix API endpoint
    """

    try:
        return response["data"][0]
    except KeyError as e:
        log.error(f"Ran into exception: {e}, {response}")
        return response


async def get_clip_data(slug: str, oauth_token: str, client_id: str) -> tuple:
def get_clip_data(slug: str, oauth_token: str, client_id: str) -> tuple:
    """
    Gets the data for given slug, returns a tuple first
    entry being the mp4_url used to download the clip, 
    second entry being the title of the clip to be used as filename.
    """

    if "thumbnail_url" in clip_info and "title" in clip_info:
        # All to get what we need to return
        # the mp4_url and title of the clip

        return mp4_url, clip_info["title"]

    raise TypeError(f"We didn't receieve what we wanted. /helix/clips endpoint gave:\\\n{clip_info}")


async def get_progress(count, block_size, total_size) -> None:
def get_progress(count, block_size, total_size) -> None:
    """
    Used for printing the download progress
    """


async def get_slug(clip: str) -> str:
def get_slug(clip: str) -> str:
    """
    Splits up the URL given and returns the slug
    of the clip.
    """
    return slug[len(slug) - 1]


async def download_clip(clip: str, basepath: str, oauth_token: str, client_id: str) -> None:
def download_clip(clip: str, basepath: str, oauth_token: str, client_id: str) -> None:
    """
    Downloads the clip, does not return anything.
    """
    # Remove special characters so we can save the video

    log.clip(f"Downloading clip with slug: {slug}.")
    log.clip(f"Saving '{slug}' as '{out_filename}'.")
    # Download the clip with given mp4_url
    log.clip(f"{slug} has been downloaded.\\\n")


async def get_clips(
def get_clips( -> Any
    blacklist: list, 
    category: str, 
    id_: str, 
    name: str, 
    path: str, 
    seconds: float, 
    ids: list, 
    client_id: str, 
    oauth_token: str, 
    period: int, 
    language: str, 
    limit: int, 
) -> (dict, list, list):
    """
    Gets the top clips for given game, returns JSON response
    """

    # params = {"period": period, "limit": limit}
        "first": limit, 
    }

    if period:
            **params, 
            "ended_at": datetime.datetime.now(datetime.timezone.utc).isoformat(), 
            "started_at": (
            ).isoformat(), 
        }


    log.info(f"Getting clips for {category} {name}")


    if not response.get("data"):
        if response.get("error") == "Internal Server Error":
            # the error is twitch's fault, we try again
            get_clips(
            )

        else:
            log.warn(
                f'Did not find "data" in response {response} for {category} {name}, period: {period} language: {language}'
            )


    if "data" in response:

        for clip in response["data"]:

            if seconds <= 0.0:
                break

            if (
                clip_id not in ids
                and not is_blacklisted(clip, formatted_blacklist)
            ):
                    "url": clip["url"], 
                    "title": clip["title"], 
                    "display_name": clip["broadcaster_name"], 
                    "duration": duration, 
                }
                new_ids.append(clip_id)
                new_titles.append(clip["title"])

        return data, new_ids, new_titles

    return {}, [], []


async def download_clips(data: dict, path: str, oauth_token: str, client_id: str) -> list:
def download_clips(data: dict, path: str, oauth_token: str, client_id: str) -> list:
    """
    Downloads clips, returns a list of streamer names.
    """

    for clip, value in data.items():
        download_clip(value["url"], path, oauth_token, client_id)
        names.append(data[clip]["display_name"])

    log.info(f"Downloaded {len(data)} clips from this batch\\\n")
    return names


if __name__ == "__main__":
    main()
