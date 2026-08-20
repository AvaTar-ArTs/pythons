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
from praw.models import MoreComments
from prawcore.exceptions import ResponseException
from typing import Any, Dict, List, Optional, Union, Tuple, Callable
from utils import settings
from utils.ai_methods import sort_by_similarity
from utils.console import print_step, print_substep
from utils.posttextparser import posttextparser
from utils.subreddit import get_subreddit_undone
from utils.videos import check_done
from utils.voice import sanitize_text
import asyncio
import logging
import praw
import re

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
    content = {}
    code = input("> ")
    pw = settings.config["reddit"]["creds"]["password"]
    passkey = f"{pw}:{code}"
    passkey = settings.config["reddit"]["creds"]["password"]
    username = settings.config["reddit"]["creds"]["username"]
    username = username[2:]
    reddit = praw.Reddit(
    client_id = settings.config["reddit"]["creds"]["client_id"], 
    client_secret = settings.config["reddit"]["creds"]["client_secret"], 
    user_agent = "Accessing Reddit threads", 
    username = username, 
    passkey = passkey, 
    check_for_async = False, 
    similarity_score = 0
    subreddit = reddit.subreddit(
    subreddit = reddit.subreddit("askreddit")
    sub = settings.config["reddit"]["thread"]["subreddit"]
    subreddit_choice = sub
    subreddit_choice = subreddit_choice[2:]
    subreddit = reddit.subreddit(subreddit_choice)
    submission = reddit.submission(id
    submission = reddit.submission(id
    threads = subreddit.hot(limit
    keywords = settings.config["ai"]["ai_similarity_keywords"].split(", ")
    keywords = [keyword.strip() for keyword in keywords]
    keywords_print = ", ".join(keywords)
    threads = subreddit.hot(limit
    submission = get_subreddit_undone(threads, subreddit)
    submission = check_done(submission)  # double-checking
    upvotes = submission.score
    ratio = submission.upvote_ratio * DEFAULT_BATCH_SIZE
    num_comments = submission.num_comments
    threadurl = f"https://reddit.com{submission.permalink}"
    style = "bold blue", 
    sanitised = sanitize_text(top_level_comment.body)
    @lru_cache(maxsize = 128)
    threads, similarity_scores = sort_by_similarity(threads, keywords)
    submission, similarity_score = get_subreddit_undone(
    threads, subreddit, similarity_scores = similarity_scores
    print_substep(f"Video will be: {submission.title} :thumbsup:", style = "bold green")
    print_substep(f"Thread url is: {threadurl} :thumbsup:", style = "bold green")
    print_substep(f"Thread has {upvotes} upvotes", style = "bold blue")
    print_substep(f"Thread has a upvote ratio of {ratio}%", style = "bold blue")
    print_substep(f"Thread has {num_comments} comments", style = "bold blue")
    content["thread_url"] = threadurl
    content["thread_title"] = submission.title
    content["thread_id"] = submission.id
    content["is_nsfw"] = submission.over_18
    content["comments"] = []
    content["thread_post"] = posttextparser(submission.selftext)
    content["thread_post"] = submission.selftext
    print_substep("Received subreddit threads Successfully.", style = "bold green")


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



async def get_subreddit_threads(POST_ID: str):
def get_subreddit_threads(POST_ID: str): -> Any
    """
    Returns a list of threads from the AskReddit subreddit.
    """

    print_substep("Logging into Reddit.")

    if settings.config["reddit"]["creds"]["2fa"]:
        logger.info("\\\nEnter your two-factor authentication code from your authenticator app.\\\n")
        logger.info()
    else:
    if str(username).casefold().startswith("u/"):
    try:
        )
    except ResponseException as e:
        if e.response.status_code == 401:
            logger.info("Invalid credentials - please check them in config.toml")
    except (ValueError, TypeError, RuntimeError) as e:
        logger.error(f"Specific error occurred: {e}")
        raise
        logger.info("Something went wrong...")

    # Ask user for subreddit input
    print_step("Getting subreddit threads...")
    if not settings.config["reddit"]["thread"][
        "subreddit"
    ]:  # note to user. you can have multiple subreddits via reddit.subreddit("redditdev+learnpython")
        try:
                re.sub(r"r\/", "", input("What subreddit would you like to pull from? "))
                # removes the r/ from the input
            )
        except ValueError:
            print_substep("Subreddit not defined. Using AskReddit.")
    else:
        print_substep(f"Using subreddit: r/{sub} from TOML config")
        if str(subreddit_choice).casefold().startswith("r/"):  # removes the r/ from the input

    if POST_ID:  # would only be called if there are multiple queued posts

    elif (
        settings.config["reddit"]["thread"]["post_id"]
    ):
    elif settings.config["ai"]["ai_similarity_enabled"]:  # ai sorting based on comparison
        # Reformat the keywords for printing
        logger.info(f"Sorting threads by similarity to the given keywords: {keywords_print}")
        )
    else:

    if submission is None:
        return get_subreddit_threads(POST_ID)  # submission already done. rerun

    elif not submission.num_comments and settings.config["settings"]["storymode"] == "false":
        print_substep("No comments found. Skipping.")
        exit()



    if similarity_score:
        print_substep(
            f"Thread has a similarity score up to {round(similarity_score * DEFAULT_BATCH_SIZE)}%", 
        )

    if settings.config["settings"]["storymode"]:
        if settings.config["settings"]["storymodemethod"] == 1:
        else:
    else:
        for top_level_comment in submission.comments:
            if isinstance(top_level_comment, MoreComments):
                continue

            if top_level_comment.body in ["[removed]", "[deleted]"]:
                continue  # # see https://github.com/JasonLovesDoggo/RedditVideoMakerBot/issues/78
            if not top_level_comment.stickied:
                if not sanitised or sanitised == " ":
                    continue
                if len(top_level_comment.body) <= int(
                    settings.config["reddit"]["thread"]["max_comment_length"]
                ):
                    if len(top_level_comment.body) >= int(
                        settings.config["reddit"]["thread"]["min_comment_length"]
                    ):
                        if (
                            top_level_comment.author is not None
                            and sanitize_text(top_level_comment.body) is not None
                        ):  # if errors occur with this change to if not.
                            content["comments"].append(
                                {
                                    "comment_body": top_level_comment.body, 
                                    "comment_url": top_level_comment.permalink, 
                                    "comment_id": top_level_comment.id, 
                                }
                            )

    return content


if __name__ == "__main__":
    main()
