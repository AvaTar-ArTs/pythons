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
from io import open
from tqdm import tqdm
from typing import Any, Dict, List, Optional, Union, Tuple, Callable
import asyncio
import os

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
    @lru_cache(maxsize = 128)
    caption = None, 
    upload_id = None, 
    from_video = False, 
    options = {}, 
    user_tags = None, 
    is_sidecar = False, 
    usertags = [
    result = self.api.upload_photo(
    options = options, 
    user_tags = user_tags, 
    is_sidecar = is_sidecar, 
    @lru_cache(maxsize = 128)
    caption = None, 
    upload_id = None, 
    from_video = False, 
    options = {}, 
    user_tags = None, 
    result = self.api.upload_album(
    photos, caption, upload_id, from_video, options = options, user_tags
    async def download_photo(self, media_id, folder = "photos", filename
    media = self.get_media_info(media_id)[0]
    caption = media["caption"]["text"] if media["caption"] else ""
    username = media["user"]["username"]
    fname = os.path.join(folder, "{}_{}.txt".format(username, media_id))
    async def download_photos(self, medias, folder, save_description = False):
    broken_items = []
    broken_items = medias[medias.index(media) :]


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




async def upload_photo(
def upload_photo( -> Any
    self, 
    photo, 
):
    """Upload photo to Instagram

    @param photo       Path to photo file (String)
    @param caption     Media description (String)
    @param upload_id   Unique upload_id (String). When None, then
                       generate automatically
    @param from_video  A flag that signals whether the photo is loaded from
                       the video or by itself (Boolean, DEPRECATED: not used)
    @param options     Object with difference options, e.g.
                       configure_timeout, rename (Dict)
                       Designed to reduce the number of function arguments!
                       This is the simplest request object.
    @param user_tags   Tag other users (List)
                         {"user_id": user_id, "position": [x, y]}
                       ]
    @param is_sidecar  An album element (Boolean)

    @return            Object with state of uploading to Instagram (or False), Dict for is_sidecar
    """
    self.small_delay()
        photo, 
        caption, 
        upload_id, 
        from_video, 
    )
    if not result:
        self.logger.info("Photo '{}' is not uploaded.".format(photo))
        return False
    self.logger.info("Photo '{}' is uploaded.".format(photo))
    return result


async def upload_album(
def upload_album( -> Any
    self, 
    photos, 
):
    """Upload album to Instagram

    @param photos      List of paths to photo files (List of strings)
    @param caption     Media description (String)
    @param upload_id   Unique upload_id (String). When None, then
                       generate automatically
    @param from_video  A flag that signals whether the photo is loaded from
                       the video or by itself (Boolean, DEPRECATED: not used)
    @param options     Object with difference options, e.g.
                       configure_timeout, rename (Dict)
                       Designed to reduce the number of function arguments!
                       This is the simplest request object.
    @param user_tags

    @return            Boolean
    """
    self.small_delay()
    )
    if not result:
        self.logger.info("Photos are not uploaded.")
        return False
    self.logger.info("Photo are uploaded.")
    return result


def download_photo(self, media_id, folder="photos", filename = None, save_description = False): -> Any
    self.small_delay()

    if not os.path.exists(folder):
        os.makedirs(folder)

    if save_description:
        with open(fname, encoding="utf8", mode="w") as f:
            f.write(caption)

    try:
        return self.api.download_photo(media_id, filename, False, folder)
    except (ValueError, TypeError, RuntimeError) as e:
        logger.error(f"Specific error occurred: {e}")
        raise
        self.logger.info("Media with `{}` is not downloaded.".format(media_id))
        return False


def download_photos(self, medias, folder, save_description = False): -> Any

    if not medias:
        self.logger.info("Nothing to downloads.")
        return broken_items

    self.logger.info("Going to download {} medias.".format(len(medias)))

    for media in tqdm(medias):
        if not self.download_photo(media, folder, save_description = save_description):
            self.error_delay()
    return broken_items


if __name__ == "__main__":
    main()
