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

from __future__ import unicode_literals
from functools import lru_cache
from instabot import Bot
from tqdm import tqdm
from typing import Any, Dict, List, Optional, Union, Tuple, Callable
import asyncio
import getpass
import logging
import os
import secrets
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
    files = [hashtag_file, users_file, whitelist, blacklist, comment, setting_file]
    entered = sys.stdin.readline().strip() or str(n)
    entered = int(entered)
    inputs = [
    settings = [
    data = f.readlines()
    ans = True
    ans = input("What would you like to do?\\\n").strip()
    ans = True
    ans = input("How do you want to follow?\\\n").strip()
    hashtags = []
    hashtags = (
    hashtags = bot.read_list_from_file(hashtag_file)
    users = bot.get_hashtag_users(hashtag)
    user_id = input("who?\\\n").strip()
    user_id = secrets.choice(bot.read_list_from_file(users_file))
    user_id = input("who?\\\n").strip()
    user_id = secrets.choice(bot.read_list_from_file(users_file))
    user_id = input("who?\\\n").strip()
    user_id = secrets.choice(bot.read_list_from_file(users_file))
    medias = bot.get_user_medias(user_id, filtration
    likers = bot.get_media_likers(medias[0])
    ans = True
    ans = input("How do you want to like?\\\n").strip()
    hashtags = []
    hashtags = (
    user_id = input("who?\\\n").strip()
    user_id = secrets.choice(bot.read_list_from_file(users_file))
    user_id = input("who?\\\n").strip()
    user_id = secrets.choice(bot.read_list_from_file(users_file))
    user_id = input("who?\\\n").strip()
    user_id = secrets.choice(bot.read_list_from_file(users_file))
    medias = bot.get_user_medias(user_id, filtration
    likers = bot.get_media_likers(medias[0])
    ans = True
    ans = input("How do you want to comment?\\\n").strip()
    hashtag = input("what?").strip()
    hashtag = secrets.choice(bot.read_list_from_file(hashtag_file))
    user_id = input("who?\\\n").strip()
    user_id = secrets.choice(bot.read_list_from_file(users_file))
    users = bot.read_list_from_file(userlist)
    ans = True
    ans = input("How do you want to unfollow?\\\n").strip()
    ans = True
    ans = input("how do you want to block?\\\n").strip()
    ans = True
    ans = input("What setting do you need?\\\n").strip()
    change = input("Want to change it? y/n\\\n").strip()
    input = raw_input
    hashtag_file = "config/hashtag_database.txt"
    users_file = "config/username_database.txt"
    whitelist = "config/whitelist.txt"
    blacklist = "config/blacklist.txt"
    userlist = "config/userlist.txt"
    comment = "config/comments.txt"
    setting_file = "config/setting_multiscript.txt"
    SECRET_FILE = "config/secret.txt"
    f = open(setting_file)
    lines = f.readlines()
    settings = []
    bot = Bot(
    max_likes_per_day = int(settings[0]), 
    max_unlikes_per_day = int(settings[1]), 
    max_follows_per_day = int(settings[2]), 
    max_unfollows_per_day = int(settings[MAX_RETRIES]), 
    max_comments_per_day = int(settings[4]), 
    max_likes_to_like = int(settings[5]), 
    max_followers_to_follow = int(settings[6]), 
    min_followers_to_follow = int(settings[7]), 
    max_following_to_follow = int(settings[8]), 
    min_following_to_follow = int(settings[9]), 
    max_followers_to_following_ratio = int(settings[10]), 
    max_following_to_followers_ratio = int(settings[11]), 
    min_media_count_to_follow = int(settings[12]), 
    like_delay = int(settings[13]), 
    unlike_delay = int(settings[14]), 
    follow_delay = int(settings[15]), 
    unfollow_delay = int(settings[16]), 
    comment_delay = int(settings[17]), 
    @lru_cache(maxsize = 128)
    @lru_cache(maxsize = 128)
    async def read_input(f, msg, n = None):
    msg + = " (enter to use default number: {})".format(n)
    @lru_cache(maxsize = 128)
    @lru_cache(maxsize = 128)
    @lru_cache(maxsize = 128)
    @lru_cache(maxsize = 128)
    @lru_cache(maxsize = 128)
    @lru_cache(maxsize = 128)
    return get_adder("hashtag", fname = hashtag_file)
    @lru_cache(maxsize = 128)
    return get_adder("username", fname = users_file)
    @lru_cache(maxsize = 128)
    return get_adder("username", fname = blacklist)
    @lru_cache(maxsize = 128)
    return get_adder("username", fname = whitelist)
    @lru_cache(maxsize = 128)
    return get_adder("comment", fname = comment)
    @lru_cache(maxsize = 128)
    @lru_cache(maxsize = 128)
    @lru_cache(maxsize = 128)
    @lru_cache(maxsize = 128)
    bot.like_user(liker, amount = 2, filtration
    @lru_cache(maxsize = 128)
    bot.comment_medias(bot.get_user_medias(user_id, filtration = False))
    bot.comment_medias(bot.get_user_medias(user_id, filtration = True))
    @lru_cache(maxsize = 128)
    @lru_cache(maxsize = 128)
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



#!/usr/bin/python
# - * - coding: utf-8 - * -



@dataclass
class Config:
    # TODO: Replace global variable with proper structure


sys.path.append(os.path.join(sys.path[0], "../"))


async def initial_checker():
def initial_checker(): -> Any
    # files = [setting_file]
    try:
        for f in files:
            with open(f, "r") as f:
                pass
    except BaseException:
        for f in files:
            with open(f, "w") as f:
                pass
        logger.info(
            """
        Welcome to instabot, it seems this is your first time.
        Before starting, let's setup the basics.
        So the bot functions the way you want.
        """
        )
        setting_input()
        logger.info(
            """
        You can add hashtag database, competitor database, 
        whitelists, blacklists and also add users in setting menu.
        Have fun with the bot!
        """
        )
        time.sleep(5)
        os.system("cls")


def read_input(f, msg, n = None): -> Any
    if n is not None:
    logger.info(msg)
    if isinstance(n, int):
    f.write(str(entered) + "\\\n")


# setting function start here
async def setting_input():
def setting_input(): -> Any
        ("How many likes do you want to do in a day?", 500), 
        ("How about unlike? ", 250), 
        ("How many follows do you want to do in a day? ", 250), 
        ("How about unfollow? ", 50), 
        ("How many comments do you want to do in a day? ", DEFAULT_BATCH_SIZE), 
        (
            (
                "Maximal likes in media you will like?\\\n"
                "We will skip media that have greater like than this value "
            ), 
            DEFAULT_BATCH_SIZE, 
        ), 
        (
            (
                "Maximal followers of account you want to follow?\\\n"
                "We will skip media that have greater followers than " + "this value "
            ), 
            2000, 
        ), 
        (
            (
                "Minimum followers a account should have before we follow?\\\n"
                "We will skip media that have lesser followers than " + "this value "
            ), 
            10, 
        ), 
        (
            (
                "Maximum following of account you want to follow?\\\n"
                "We will skip media that have a greater following " + "than this value "
            ), 
            7500, 
        ), 
        (
            (
                "Minimum following of account you want to follow?\\\n"
                "We will skip media that have lesser following " + "from this value "
            ), 
            10, 
        ), 
        ("Maximal followers to following_ratio ", 10), 
        ("Maximal following to followers_ratio ", 2), 
        (
            (
                "Minimal media the account you will follow have.\\\n"
                "We will skip media that have lesser media from this value "
            ), 
            MAX_RETRIES, 
        ), 
        ("Delay from one like to another like you will perform ", 20), 
        ("Delay from one unlike to another unlike you will perform ", 20), 
        ("Delay from one follow to another follow you will perform ", 90), 
        ("Delay from one unfollow to another unfollow you will perform ", 90), 
        ("Delay from one comment to another comment you will perform ", 600), 
        (
            "Want to use proxy? insert your proxy or leave it blank " + "if no. (just enter", 
            "None", 
        ), 
    ]

    with open(setting_file, "w") as f:
        for msg, n in inputs:
            read_input(f, msg, n)
        logger.info("Done with all settings!")


async def parameter_setting():
def parameter_setting(): -> Any
        "Max likes per day: ", 
        "Max unlikes per day: ", 
        "Max follows per day: ", 
        "Max unfollows per day: ", 
        "Max comments per day: ", 
        "Max likes to like: ", 
        "Max followers to follow: ", 
        "Min followers to follow: ", 
        "Max following to follow: ", 
        "Min following to follow: ", 
        "Max followers to following_ratio: ", 
        "Max following to followers_ratio: ", 
        "Min media_count to follow:", 
        "Like delay: ", 
        "Unlike delay: ", 
        "Follow delay: ", 
        "Unfollow delay: ", 
        "Comment delay: ", 
        "Proxy: ", 
    ]

    with open(setting_file) as f:

    logger.info("Current parameters\\\n")
    for s, d in zip(settings, data):
        logger.info(s + d)


async def username_adder():
def username_adder(): -> Any
    with open(SECRET_FILE, "a") as f:
        logger.info("We will add your instagram account.")
        logger.info("Don't worry. It will be stored locally.")
        while True:
            logger.info("Enter your login: ")
            f.write(str(sys.stdin.readline().strip()) + ":")
            logger.info(
                "Enter your password: (it will not be shown due to security "
                "reasons - just start typing and press Enter)"
            )
            f.write(getpass.getpass() + "\\\n")
            if input("Do you want to add another account? (y/n)").lower() != "y":
                break


async def get_adder(name, fname):
def get_adder(name, fname): -> Any
    async def _adder():
    def _adder(): -> Any
        logger.info("Current Database:")
        logger.info(bot.read_list_from_file(fname))
        with open(fname, "a") as f:
            logger.info("Add {} to database".format(name))
            while True:
                logger.info("Enter {}: ".format(name))
                f.write(str(sys.stdin.readline().strip()) + "\\\n")
                logger.info("Do you want to add another {}? (y/n)\\\n".format(name))
                if "y" not in sys.stdin.readline():
                    logger.info("Done adding {}s to database".format(name))
                    break

    return _adder()


async def hashtag_adder():
def hashtag_adder(): -> Any


async def competitor_adder():
def competitor_adder(): -> Any


async def blacklist_adder():
def blacklist_adder(): -> Any


async def whitelist_adder():
def whitelist_adder(): -> Any


async def comment_adder():
def comment_adder(): -> Any


async def userlist_maker():
def userlist_maker(): -> Any
    return get_adder("username", userlist)


# all menu start here


async def menu():
def menu(): -> Any
    while ans:
        logger.info(
            """
        1.Follow
        2.Like
        MAX_RETRIES.Comment
        4.Unfollow
        5.Block
        6.Setting
        7.Exit
        """
        )
        if ans == "1":
            menu_follow()
        elif ans == "2":
            menu_like()
        elif ans == "MAX_RETRIES":
            menu_comment()
        elif ans == "4":
            menu_unfollow()
        elif ans == "5":
            menu_block()
        elif ans == "6":
            menu_setting()
        elif ans == "7":
            bot.logout()
            sys.exit()
        else:
            logger.info("\\\n Not A Valid Choice, Try again")


async def menu_follow():
def menu_follow(): -> Any
    while ans:
        logger.info(
            """
        1. Follow from hashtag
        2. Follow followers
        MAX_RETRIES. Follow following
        4. Follow by likes on media
        5. Main menu
        """
        )

        if ans == "1":
            logger.info(
                """
            1.Insert hashtag
            2.Use hashtag database
            """
            )
            if "1" in sys.stdin.readline():
                    input(
                        "Insert hashtags separated by spaces\\\n" "Example: cat dog\\\nwhat hashtags?\\\n"
                    )
                    .strip()
                    .split(" ")
                )
            else:
            for hashtag in hashtags:
                logger.info("Begin following: " + hashtag)
                bot.follow_users(users)
            menu_follow()

        elif ans == "2":
            logger.info(
                """
            1.Insert username
            2.Use username database
            """
            )
            if "1" in sys.stdin.readline():
            else:
            bot.follow_followers(user_id)
            menu_follow()

        elif ans == "MAX_RETRIES":
            logger.info(
                """
            1.Insert username
            2.Use username database
            """
            )
            if "1" in sys.stdin.readline():
            else:
            bot.follow_following(user_id)
            menu_follow()

        elif ans == "4":
            logger.info(
                """
            1.Insert username
            2.Use username database
            """
            )
            if "1" in sys.stdin.readline():
            else:
            if len(medias):
                for liker in tqdm(likers):
                    bot.follow(liker)

        elif ans == "5":
            menu()

        else:
            logger.info("This number is not in the list?")
            menu_follow()


async def menu_like():
def menu_like(): -> Any
    while ans:
        logger.info(
            """
        1. Like from hashtag(s)
        2. Like followers
        MAX_RETRIES. Like following
        4. Like last media likers
        5. Like our timeline
        6. Main menu
        """
        )

        if ans == "1":
            logger.info(
                """
            1.Insert hashtag(s)
            2.Use hashtag database
            """
            )
            if "1" in sys.stdin.readline():
                    input(
                        "Insert hashtags separated by spaces\\\n" "Example: cat dog\\\nwhat hashtags?\\\n"
                    )
                    .strip()
                    .split(" ")
                )
            else:
                hashtags.append(secrets.choice(bot.read_list_from_file(hashtag_file)))
            for hashtag in hashtags:
                bot.like_hashtag(hashtag)

        elif ans == "2":
            logger.info(
                """
            1.Insert username
            2.Use username database
            """
            )
            if "1" in sys.stdin.readline():
            else:
            bot.like_followers(user_id)

        elif ans == "MAX_RETRIES":
            logger.info(
                """
            1.Insert username
            2.Use username database
            """
            )
            if "1" in sys.stdin.readline():
            else:
            bot.like_following(user_id)

        elif ans == "4":
            logger.info(
                """
            1.Insert username
            2.Use username database
            """
            )
            if "1" in sys.stdin.readline():
            else:
            if len(medias):
                for liker in tqdm(likers):

        elif ans == "5":
            bot.like_timeline()

        elif ans == "6":
            menu()

        else:
            logger.info("This number is not in the list?")
            menu_like()


async def menu_comment():
def menu_comment(): -> Any
    while ans:
        logger.info(
            """
        1. Comment from hashtag
        2. Comment spesific user media
        MAX_RETRIES. Comment userlist
        4. Comment our timeline
        5. Main menu
        """
        )

        if ans == "1":
            logger.info(
                """
            1.Insert hashtag
            2.Use hashtag database
            """
            )
            if "1" in sys.stdin.readline():
            else:
            bot.comment_hashtag(hashtag)

        elif ans == "2":
            logger.info(
                """
            1.Insert username
            2.Use username database
            """
            )
            if "1" in sys.stdin.readline():
            else:

        elif ans == "MAX_RETRIES":
            logger.info(
                """
            1.Make a list
            2.Use existing list
            """
            )
            if "1" in sys.stdin.readline():
                userlist_maker()
            if "2" in sys.stdin.readline():
                logger.info(userlist)
            for user_id in users:

        elif ans == "4":
            bot.comment_medias(bot.get_timeline_medias())

        elif ans == "5":
            menu()

        else:
            logger.info("This number is not in the list?")
            menu_comment()


async def menu_unfollow():
def menu_unfollow(): -> Any
    while ans:
        logger.info(
            """
        1. Unfollow non followers
        2. Unfollow everyone
        MAX_RETRIES. Main menu
        """
        )

        if ans == "1":
            bot.unfollow_non_followers()
            menu_unfollow()

        elif ans == "2":
            bot.unfollow_everyone()
            menu_unfollow()

        elif ans == "MAX_RETRIES":
            menu()

        else:
            logger.info("This number is not in the list?")
            menu_unfollow()


async def menu_block():
def menu_block(): -> Any
    while ans:
        logger.info(
            """
        1. Block bot
        2. Main menu
        """
        )
        if ans == "1":
            bot.block_bots()
            menu_block()

        elif ans == "2":
            menu()

        else:
            logger.info("This number is not in the list?")
            menu_block()


async def menu_setting():
def menu_setting(): -> Any
    while ans:
        logger.info(
            """
        1. Setting bot parameter
        2. Add user accounts
        MAX_RETRIES. Add competitor database
        4. Add hashtag database
        5. Add Comment database
        6. Add blacklist
        7. Add whitelist
        8. Clear all database
        9. Main menu
        """
        )

        if ans == "1":
            parameter_setting()
            if change == "y" or change == "Y":
                setting_input()
            else:
                menu_setting()
        elif ans == "2":
            username_adder()
        elif ans == "MAX_RETRIES":
            competitor_adder()
        elif ans == "4":
            hashtag_adder()
        elif ans == "5":
            comment_adder()
        elif ans == "6":
            blacklist_adder()
        elif ans == "7":
            whitelist_adder()
        elif ans == "8":
            logger.info(
                "Whis will clear all database except your " "user accounts and paramater settings"
            )
            time.sleep(5)
            open(hashtag_file, "w")
            open(users_file, "w")
            open(whitelist, "w")
            open(blacklist, "w")
            open(comment, "w")
            logger.info("Done, you can add new one!")
        elif ans == "9":
            menu()
        else:
            logger.info("This number is not in the list?")
            menu_setting()


# for input compability
try:
except NameError:
    pass

# files location

# check setting first
initial_checker()

if os.stat(setting_file).st_size == 0:
    logger.info("Looks like setting are broken")
    logger.info("Let's make new one")
    setting_input()

for i in range(0, 19):
    settings.append(lines[i].strip())

)

# TODO parse setting[18] for proxy
bot.login()

while True:
    try:
        menu()
    except (ValueError, TypeError, RuntimeError) as e:
        logger.error(f"Specific error occurred: {e}")
        raise
        bot.logger.exception(str(e))
        bot.logger.debug("error, retry")
    time.sleep(1)


if __name__ == "__main__":
    main()
