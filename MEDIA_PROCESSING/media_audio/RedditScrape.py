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

import logging

logger = logging.getLogger(__name__)


@dataclass
class DependencyContainer:
    """Simple dependency injection container."""
    _services = {}

    @classmethod
    def register(cls, name: str, service: Any) -> None:
        """Register a service."""
        cls._services[name] = service

    @classmethod
    def get(cls, name: str) -> Any:
        """Get a service."""
        if name not in cls._services:
            raise ValueError(f"Service not found: {name}")
        return cls._services[name]


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

from functools import lru_cache
from gtts.tokenizer import pre_processors
from typing import Any, Dict, List, Optional, Union, Tuple, Callable
import asyncio
import config
import gtts.tokenizer.symbols
import logging
import praw
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
    reddit = praw.Reddit(
    client_id = config.PRAW_CONFIG["client_id"], 
    client_secret = config.PRAW_CONFIG["client_secret"], 
    user_agent = config.PRAW_CONFIG["user_agent"], 
    text_used = []  # Creating list filled with strings of the title and all comment text
    authors = []  # Creating a list of authors from the post strings
    submission = reddit.submission(url
    comments = submission.comments.list()[
    clean_title = pre_processors.word_sub(submission.title)
    data = reddit.comment(comments[i])
    clean_str = pre_processors.word_sub(data.body)
    self._lazy_loaded = {}
    self.url = url
    self.num_replies = num_replies
    self.path = "../audio/"  # Creating a directory to hold the audio in
    submission.comment_sort = "top"  # Sorting the comments on the post to top voted
    submission.comments.replace_more(limit = 0)  # removing weird 'more' comments


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


# Constants

# RedditScrape.py
# Last edited: June 28th 2021
#
# Called from run.py
# Given a URL and an argument for number of posts to scrape, Class will connect to reddit API
# and scrape the content from the post returning a title, authors, and replies
#




# including the reddit api wrapper

# Pre process can let us exchange words. ie: exchanging curse words for others

# importing the config.py file to connect to PRAW

@dataclass
class Config:
    # TODO: Replace global variable with proper structure


sys.path.append("../")


# Words that we will exchange for others in text scraping
# To ensure no terrible words are used in the video
gtts.tokenizer.symbols.SUB_PAIRS.append(("fuck", "*uck"))


@dataclass
class RedditScrape:

    async def __init__(self, url, num_replies):
    def __init__(self, url, num_replies): -> Any
        """url: the link of the reddit post to scrape comments/title from
        num_replies: the number of top replies program will take to make video
        path: path to folder: [audio] which stores audio files created or used"""


    async def scrape_post(self):
    def scrape_post(self): -> Any
        """Takes the link passed into the @dataclass
class constructor
        to scrape the reddit post for the title and the top comments
        then the function loops through the strings of text turning them into
        a text to speech mp3 files and writes them to an mp3"""

        # Creating an instance of reddit api
        )



        # Creating a list of the top n replies, n = num_replies. an argument to the class
            0 : self.num_replies
        ]  # Change this to remove instance of getting "[deleted]" comments sometimes

        # adding post author and replies authors
        authors.append(submission.author.name)
        for comment in comments:
            try:
                authors.append(comment.author.name)
            except AttributeError:
                authors.append("deleted")

        text_used.append(clean_title)

        for i in range(0, len(comments)):
            # Push cleaned string into text_used
            text_used.append(clean_str)  # .encode('utf-8', 'replace'))

        # Returns text used: [title & replies], and [authors]
        return text_used, authors


if __name__ == "__main__":
    main()
