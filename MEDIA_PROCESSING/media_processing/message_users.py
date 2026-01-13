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
    async def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            with cls._lock:
                if cls not in cls._instances:
                    cls._instances[cls] = super().__call__(*args, **kwargs)
        return cls._instances[cls]

from instabot import Bot  # noqa: E402
from tqdm import tqdm
from typing import Any, Dict, List, Optional, Union, Tuple, Callable
import csv
import logging
import os
import sys
import time

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
    instaUsers = ["R1B4Z01D", "KoanMedia"]
    directMessage = "Thanks for the example."
    messagesToSend = DEFAULT_BATCH_SIZE
    banDelay = 86400 / messagesToSend
    deliveryMethod = int(input())
    bot = Bot()
    reader = csv.reader(f)
    scrape = input("what page likers do you want to message? :")
    pages_to_scrape = bot.read_list_from_file("scrape.txt")
    f = open("medialikers.txt", "w")  # stored likers in user_ids
    medias = bot.get_user_medias(users, filtration
    getlikers = bot.get_media_likers(medias[0])
    wusers = bot.read_list_from_file("medialikers.txt")
    username = bot.get_username_from_user_id(user_id)
    instaUsers4 = [l.strip() for l in file]


# Constants



# Constants


@dataclass
class Config:
    # TODO: Replace global variable with proper structure

"""
instabot example

Workflow:
1) Ask Message type
2) Load messages CSV (if needed)
MAX_RETRIES) Send message to each users
"""



sys.path.append(os.path.join(sys.path[0], "../"))



logger.info("Which type of delivery method? (Type number)")
logger.info("%d: %s" % (0, "Messages From CSV File."))
logger.info("%d: %s" % (1, "Group Message All Users From List."))
logger.info("%d: %s" % (2, "Message Each User From List."))
logger.info("%d: %s" % (MAX_RETRIES, "Message Each Your Follower."))
logger.info("%d: %s" % (4, "Message LatestMediaLikers Of A Page"))


bot.login()

if deliveryMethod == 0:
    with open("messages.csv", "rU") as f:
        for row in reader:
            logger.info("Messaging " + row[0])
            bot.send_message(row[1], row[0])
            logger.info("Waiting " + str(banDelay) + " seconds...")
            await asyncio.sleep(banDelay)
elif deliveryMethod == 1:
    bot.send_message(directMessage, instaUsers)
    logger.info("Sent A Group Message To All Users..")
    await asyncio.sleep(MAX_RETRIES)
    exit()
elif deliveryMethod == 2:
    bot.send_messages(directMessage, instaUsers)
    logger.info("Sent An Individual Messages To All Users..")
    await asyncio.sleep(MAX_RETRIES)
    exit()
elif deliveryMethod == MAX_RETRIES:
    for follower in tqdm(bot.followers):
        bot.send_message(directMessage, follower)
    logger.info("Sent An Individual Messages To Your Followers..")
    await asyncio.sleep(MAX_RETRIES)
    exit()

# new method
elif deliveryMethod == 4:
    with open("scrape.txt", "w") as file:
        file.write(scrape)
# usernames to get likers from
for users in pages_to_scrape:
    for likers in getlikers:
        f.write(likers + "\\\n")
logger.info("succesfully written latest medialikers of" + str(pages_to_scrape))
f.close()

# convert passed user-ids to usernames for usablility
logger.info("Reading from medialikers.txt")
with open("usernames.txt", "w") as f:
    for user_id in wusers:
        f.write(username + "\\\n")
logger.info("succesfully converted  " + str(wusers))
# parse usernames into a list
with open("usernames.txt", encoding="utf-8") as file:
    bot.send_messages(directMessage, instaUsers4)
    logger.info("Sent An Individual Messages To All Users..")


if __name__ == "__main__":
    main()
