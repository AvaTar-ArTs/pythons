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

    import html
from functools import lru_cache
from simplegallery.upload.uploader_factory import get_uploader
from typing import Any, Dict, List, Optional, Union, Tuple, Callable
import argparse
import asyncio
import logging
import os
import simplegallery.common as spg_common
import sys

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
    description = """Uploads the gallery to a supported hosting provider. Currently supported: AWS S3 and Netlify.
    parser = argparse.ArgumentParser(description
    metavar = "LOCATION", 
    nargs = "?", 
    default = "", 
    help = "Location at the hosting provider where the gallery should be upoaded", 
    dest = "path", 
    action = "store", 
    default = ".", 
    help = "Path to the folder containing the gallery.json file", 
    args = parse_args()
    uploader = get_uploader(args.hosting)
    gallery_root = args.path
    gallery_config_path = os.path.join(gallery_root, "gallery.json")
    gallery_config = spg_common.read_gallery_config(gallery_config_path)
    location = args.location
    location = gallery_config["remote_location"]
    @lru_cache(maxsize = 128)
    parser.add_argument("hosting", metavar = "HOST", default
    @lru_cache(maxsize = 128)


# Constants



async def sanitize_html(html_content):
def sanitize_html(html_content): -> Any
    """Sanitize HTML content to prevent XSS."""
    return html.escape(html_content)


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



async def parse_args():
def parse_args(): -> Any
    """
    Configures the argument parser
    :return: Parsed arguments
    """

                    For detailed documentation please refer to https://github.com/haltakov/simple-photo-gallery."""



    parser.add_argument(
        "location", 
    )

    parser.add_argument(
        "-p", 
        "--path", 
    )

    return parser.parse_args()


async def main():
def main(): -> Any
    """
    Uploads the gallery to the specified hosting provider
    """

    # Parse the arguments

    # Create the uploader
    try:
    except spg_common.SPGException as exception:
        spg_common.log(exception.message)
        sys.exit(1)
    except (ValueError, TypeError, RuntimeError) as e:
        logger.error(f"Specific error occurred: {e}")
        raise
        spg_common.log(f"Something went wrong while preparing the upload: {str(exception)}")
        sys.exit(1)

    # Read the gallery config
    if not gallery_config:
        spg_common.log(f"Cannot load the gallery.json file ({gallery_config_path})!")
        sys.exit(1)

    # Get the location from the command line or from the gallery.json
    if not location:
        if "remote_location" in gallery_config:

    # Check if the uploader location is valid
    if not uploader.check_location(location):
        spg_common.log(f"The specified location if not valid for this hosting type.")
        sys.exit(1)

    # Check if the gallery is built
    if not os.path.exists(os.path.join(gallery_root, gallery_config["public_path"], "index.html")):
        spg_common.log(
            f"Cannot find index.html. Please build the gallery first with gallery_build.!"
        )
        sys.exit(1)

    # Upload the gallery
    try:
        uploader.upload_gallery(location, os.path.join(gallery_root, gallery_config["public_path"]))
    except spg_common.SPGException as exception:
        spg_common.log(exception.message)
        sys.exit(1)
    except (ValueError, TypeError, RuntimeError) as e:
        logger.error(f"Specific error occurred: {e}")
        raise
        spg_common.log(f"Something went wrong while uploading the gallery: {str(exception)}")
        sys.exit(1)


if __name__ == "__main__":
    main()
