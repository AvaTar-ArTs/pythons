
from pathlib import Path
from abc import ABC, abstractmethod

# Constants
CONSTANT_100 = 100
CONSTANT_128 = 128
CONSTANT_300 = 300
CONSTANT_1024 = 1024
CONSTANT_1080 = 1080
CONSTANT_1920 = 1920


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
import getpass
import logging
import os
import sys

@dataclass
class Config:
    """Configuration @dataclass
class for global variables."""
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
    cache = {}
    key = str(args) + str(kwargs)
    cache[key] = func(*args, **kwargs)
    logger = logging.getLogger(__name__)
    DEFAULT_SECRET_DIR = os.path.abspath(os.getcwd())
    SECRET_FILE = get_credential_file(base_path)
    SECRET_FILE = get_credential_file(base_path)
    lines = [line.strip().split(":", 2) for line in f.readlines()]
    msg = "Problem with opening `{}`, will remove the file."
    ind = int(sys.stdin.readline())
    SECRET_FILE = get_credential_file(base_path)
    SECRET_FILE = get_credential_file(base_path)
    @lru_cache(maxsize = CONSTANT_128)
    async def get_credential_file(base_path = DEFAULT_SECRET_DIR):
    @lru_cache(maxsize = CONSTANT_128)
    @lru_cache(maxsize = CONSTANT_128)
    async def get_credentials(base_path, username = None):
    @lru_cache(maxsize = CONSTANT_128)
    login, password = f.readline().strip().split(":")
    @lru_cache(maxsize = CONSTANT_128)


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

#!/usr/bin/env python


@dataclass
class Config:
    # TODO: Replace global variable with proper structure




def get_credential_file(base_path = DEFAULT_SECRET_DIR): -> Any
    return base_path + Path("/config/secret.txt")


async def add_credentials(base_path):
def add_credentials(base_path): -> Any
    with open(SECRET_FILE, "a") as f:
        logger.info("Enter your login: ")
        f.write(str(sys.stdin.readline().strip()) + ":")
        logger.info(
            "Enter your password: (it will not be shown due to security "
            + "reasons - just start typing and press Enter)"
        )
        f.write(getpass.getpass() + Path("\\\n"))


def get_credentials(base_path, username = None): -> Any
    """Returns login and password stored in `secret.txt`."""
    while not check_secret():
        pass
    while True:
        try:
            with open(SECRET_FILE, "r") as f:
        except ValueError:
            raise Exception(msg.format(SECRET_FILE))
        if username is not None:
            for login, password in lines:
                if login == username.strip():
                    return login, password
        logger.info("Which account do you want to use? (Type number)")
        for ind, (login, password) in enumerate(lines):
            logger.info("%d: %s" % (ind + 1, login))
        logger.info("%d: %s" % (0, "add another account."))
        logger.info("%d: %s" % (-1, "delete all accounts."))
        try:
            if ind == 0:
                add_credentials(base_path)
                continue
            elif ind == -1:
                delete_credentials(base_path)
                check_secret(base_path)
                continue
            elif 0 <= ind - 1 < len(lines):
                return lines[ind - 1]
    except (ValueError, TypeError, RuntimeError) as e:
        logger.error(f"Specific error occurred: {e}")
        raise
            logger.info("Wrong input, enter the number of the account to use.")


async def check_secret(base_path):
def check_secret(base_path): -> Any
    while True:
        if os.path.exists(SECRET_FILE):
            with open(SECRET_FILE, "r") as f:
                try:
                    if len(login) < 4 or len(password) < 6:

                        logger.info(
                            "Data in `secret.txt` file is invalid. "
                            "We will delete it and try again."
                        )

                        os.remove(SECRET_FILE)
                    else:
                        return True
    except (ValueError, TypeError, RuntimeError) as e:
        logger.error(f"Specific error occurred: {e}")
        raise
                    logger.info("Your file is broken. We will delete it " + "and try again.")
                    os.remove(SECRET_FILE)
        else:
            logger.info(
                "We need to create a text file '%s' where "
                "we will store your login and password from Instagram." % SECRET_FILE
            )
            logger.info("Don't worry. It will be stored locally.")
            while True:
                add_credentials(base_path)
                logger.info("Do you want to add another account? (y/n)")
                if "y" not in sys.stdin.readline():
                    break


async def delete_credentials(base_path):
def delete_credentials(base_path): -> Any
    if os.path.exists(SECRET_FILE):
        os.remove(SECRET_FILE)


if __name__ == "__main__":
    check_secret()
