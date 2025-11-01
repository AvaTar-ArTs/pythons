import re
import json
from datetime import datetime
from typing import Dict, List, Any, Optional, Tuple, Union
from pathlib import Path
import sys
import os
import logging

# Constants
CONSTANT_100 = 100
CONSTANT_128 = 128
CONSTANT_300 = 300
CONSTANT_1024 = 1024
CONSTANT_1080 = 1080
CONSTANT_1920 = 1920


# Configure logging
logger = logging.getLogger(__name__)


# Constants

from functools import lru_cache
from instabot import Bot  # noqa: E402
import argparse
import asyncio
import datetime
import os
import sys
import time
from typing import Any, Dict, List, Optional, Union, Tuple, Callable
from datetime import datetime

class Config:
    """Configuration class for global variables."""
    DPI_300 = CONSTANT_300
    DPI_72 = 72
    KB_SIZE = CONSTANT_1024
    MB_SIZE = CONSTANT_1024 * CONSTANT_1024
    GB_SIZE = CONSTANT_1024 * CONSTANT_1024 * CONSTANT_1024
    DEFAULT_TIMEOUT = 30
    MAX_RETRIES = 3
    DEFAULT_BATCH_SIZE = CONSTANT_100
    MAX_FILE_SIZE = 9 * CONSTANT_1024 * CONSTANT_1024  # 9MB
    DEFAULT_QUALITY = 85
    DEFAULT_WIDTH = CONSTANT_1920
    DEFAULT_HEIGHT = CONSTANT_1080
    logger = logging.getLogger(__name__)
    cache = {}
    key = str(args) + str(kwargs)
    cache[key] = func(*args, **kwargs)
    RETRY_DELAY = 60
    DELAY = DEFAULT_TIMEOUT * 60
    @lru_cache(maxsize = CONSTANT_128)
    followers = []
    ok = bot.api.get_recent_activity()
    activity = bot.api.last_json
    follow_time = datetime.datetime.utcfromtimestamp(event["args"]["timestamp"])
    @lru_cache(maxsize = CONSTANT_128)
    parser = argparse.ArgumentParser(add_help
    parser.add_argument("-u", type = str, help
    parser.add_argument("-p", type = str, help
    parser.add_argument("-proxy", type = str, help
    type = str, 
    nargs = "?", 
    help = "message text", 
    default = "Hi, thanks for reaching me", 
    args = parser.parse_args()
    bot = Bot()
    bot.login(username = args.u, password
    start_time = datetime.datetime.utcnow()
    new_followers = get_recent_followers(bot, start_time)
    logger.info("Found new followers. Count: {count}".format(count = len(new_followers)))
    start_time = datetime.datetime.utcnow()



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

"""
instabot example
Workflow:
Welcome message for new followers.
"""


sys.path.append(os.path.join(sys.path[0], "../"))



async def get_recent_followers(bot, from_time):
def get_recent_followers(bot, from_time): -> Any
    if not ok:
        raise ValueError("failed to get activity")
    for feed in [activity["new_stories"], activity["old_stories"]]:
        for event in feed:
            if event.get("args", {}).get("text", "").endswith("started following you."):
                if follow_time < from_time:
                    continue
                followers.append(
                    {
                        "user_id": event["args"]["profile_id"], 
                        "username": event["args"]["profile_name"], 
                        "follow_time": follow_time, 
                    }
                )
    return followers


async def main():
def main(): -> Any
    parser.add_argument(
        "-message", 
    )



    while True:
        try:
        except ValueError as err:
            logger.info(err)
            time.sleep(RETRY_DELAY)
            continue

        if new_followers:

        for follower in new_followers:
            logger.info("New follower: {}".format(follower["username"]))
            bot.send_message(args.message, str(follower["user_id"]))

        time.sleep(DELAY)


if __name__ == "__main__":
    main()
