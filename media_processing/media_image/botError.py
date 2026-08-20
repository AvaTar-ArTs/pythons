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

    import html
from functools import lru_cache
from pathlib import Path
from pyfiglet import Figlet
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from time import sleep
from typing import Any, Dict, List, Optional, Union, Tuple, Callable
import asyncio
import logging
import os
import platform

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
    f = Figlet(font
    instagramName = f.renderText("Instagram bot")
    mySystem = "clear"
    way = Path("geckodriver/linux/geckodriver-v0.26.0-linux64")  # path to the file
    geckoFile = way / "geckodriver"  # way to geckodriver
    mySystem = "cls"
    way = Path("geckodriver/windows")
    geckoFile = way / "geckodriver.exe"
    delay = int(input("Delay (just number): "))  # loading delay time
    username = str(input("User: "))  # your user
    password = str(input("Password: "))  # your password
    hashtag = str(input("Hashtag: "))  # hashtag
    likes = int(input("Amount: "))  # amount of photos to like
    driver = webdriver.Firefox(
    executable_path = f"{geckoFile}"
    username = user  # your user
    password = pwd  # your password
    userelement = driver.find_element_by_xpath(
    pwdelement = driver.find_element_by_xpath(
    item = 1
    item = item + 1
    press = input('\\033[0;34mpress "enter" to continue\\033[m ')
    mySystem = "clear"
    way = Path("geckodriver/linux/geckodriver-v0.26.0-linux64")  # path to the file
    geckoFile = way / "geckodriver"  # way to geckodriver
    mySystem = "cls"
    way = Path("geckodriver/windows")
    geckoFile = way / "geckodriver.exe"
    delay = int(input("Delay (just number): "))  # loading delay time
    username = str(input("User: "))  # your user
    password = str(input("Password: "))  # your password
    hashtag = str(input("Hashtag: "))  # hashtag
    likes = int(input("Amount: "))  # amount of photos to like
    comment = str(input("Comment: "))  # comment in photos
    driver = webdriver.Firefox(
    executable_path = f"{geckoFile}"
    username = user  # your user
    password = pwd  # your password
    userelement = driver.find_element_by_xpath(
    pwdelement = driver.find_element_by_xpath(
    item = 1
    field = driver.find_element_by_class_name("Ypffh")
    item = item + 1
    press = input('\\033[0;34mpress "enter" to continue\\033[m ')
    mySystem = "clear"
    way = Path("geckodriver/linux/geckodriver-v0.26.0-linux64")  # path to the file
    geckoFile = way / "geckodriver"  # way to geckodriver
    mySystem = "cls"
    way = Path("geckodriver/windows")
    geckoFile = way / "geckodriver.exe"
    delay = int(input("Delay (just number): "))  # loading delay time
    username = str(input("User: "))  # your user
    password = str(input("Password: "))  # your password
    driver = webdriver.Firefox(
    executable_path = f"{geckoFile}"
    username = user  # your user
    password = pwd  # your password
    userelement = driver.find_element_by_xpath(
    pwdelement = driver.find_element_by_xpath(
    loadstories = ""  # variable to terminate the loop without errors
    loadstories = 0
    press = input('\\033[0;34mpress "enter" to continue\\033[m ')
    mySystem = "clear"
    way = Path("geckodriver/linux/geckodriver-v0.26.0-linux64")  # path to the file
    geckoFile = way / "geckodriver"  # way to geckodriver
    mySystem = "cls"
    way = Path("geckodriver/windows")
    geckoFile = way / "geckodriver.exe"
    delay = int(input("Delay (just number): "))  # loading delay time
    username = str(input("User: "))  # your user
    password = str(input("Password: "))  # your password
    imgPage = str(input("URL Image: "))  # photo path on instagram
    amount = int(input("Number of Comments: "))  # number of comments
    comment = str(input("Comment: "))  # comment
    driver = webdriver.Firefox(
    executable_path = f"{geckoFile}"
    username = user  # your user
    password = pwd  # your password
    userelement = driver.find_element_by_xpath(
    pwdelement = driver.find_element_by_xpath(
    item = 1
    field = driver.find_element_by_class_name("Ypffh")
    item = item + 1
    press = input('\\033[0;34mpress "enter" to continue\\033[m ')
    mySystem = platform.system()  # which operating system is running
    menu = ["Like", "Comment and Like", "View Stories", "Draw for Comment"]
    selected = int(
    @lru_cache(maxsize = 128)
    async def artName(timeSleep = 0):
    @lru_cache(maxsize = 128)
    @lru_cache(maxsize = 128)
    driver.find_element_by_xpath('//a[@href = "/accounts/login/?source
    '//input[@name = "username"]'
    '//input[@name = "password"]'
    @lru_cache(maxsize = 128)
    @lru_cache(maxsize = 128)
    async def like(likes = 1):
    @lru_cache(maxsize = 128)
    @lru_cache(maxsize = 128)
    driver.find_element_by_xpath('//a[@href = "/accounts/login/?source
    '//input[@name = "username"]'
    '//input[@name = "password"]'
    @lru_cache(maxsize = 128)
    @lru_cache(maxsize = 128)
    @lru_cache(maxsize = 128)
    async def likecomment(likes = 1, comment
    @lru_cache(maxsize = 128)
    @lru_cache(maxsize = 128)
    driver.find_element_by_xpath('//a[@href = "/accounts/login/?source
    '//input[@name = "username"]'
    '//input[@name = "password"]'
    @lru_cache(maxsize = 128)
    @lru_cache(maxsize = 128)
    @lru_cache(maxsize = 128)
    driver.find_element_by_xpath('//a[@href = "/accounts/login/?source
    '//input[@name = "username"]'
    '//input[@name = "password"]'
    @lru_cache(maxsize = 128)
    @lru_cache(maxsize = 128)
    @lru_cache(maxsize = 128)
    async def commentDraw(amount = 1, comment


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


# Constants


@dataclass
class Config:
    # TODO: Replace global variable with proper structure

# -*- coding: utf-8 -*-

"""
Created in 10/2020
@Author: Paulo https://github.com/alpdias
"""

# imported libraries



def artName(timeSleep = 0): -> Any
    """
    -> function to print text in ascii art\
    \\\n:param timeSleep: waiting time for execution\
    \\\n:return: ascii art\
    """

    logger.info(instagramName)
    sleep(timeSleep)


async def functionLike(mySystem):
def functionLike(mySystem): -> Any
    """
    -> function to enjoy photos\
    \\\n:param mySystem: operating system type\
    \\\n:return: bot to enjoy photos\
    """

    # check the system
    if mySystem == "Linux":

    else:

    # input for config bot
    os.system(mySystem)  # for linux user 'clear' and for windows use 'cls'
    artName(0)

    logger.info("")
    logger.info("\\033[0;32mCONFIGURATION\\033[m")
    logger.info("")


    # input login for bot
    os.system(mySystem)
    artName(0)

    logger.info("")
    logger.info("\\033[0;32mLOGIN INFORMATION\\033[m")
    logger.info("")


    # input info for bot
    os.system(mySystem)
    artName(0)

    logger.info("")
    logger.info("\\033[0;32mBOT INFORMATION\\033[m")
    logger.info("")


    logger.info("")
    logger.info("Loading...")
    logger.info("")

    # load browser drive in to var and open
    )  # geckodriver path https://github.com/mozilla/geckodriver/releases/tag/v0.26.0

    async def botlogin(user, pwd):
    def botlogin(user, pwd): -> Any
        """
        -> log in to instagram along with credentials\
        \\\n:param user: user to login\
        \\\n:param pwd: login password\
        \\\n:return: user's instagram login\
        """


        driver.get("https://www.instagram.com/")  # instagram url
        sleep(delay)

        """
        this page / button was removed by Instagram
        """

        )  # 'username' input element
        userelement.clear()
        userelement.send_keys(username)  # user insertion in 'user' element

        )  # 'password 'input element
        pwdelement.clear()
        pwdelement.send_keys(password)  # password insertion in 'password' element

        pwdelement.send_keys(Keys.RETURN)  # log in to page
        sleep(delay + 2)

    async def findhashtag(hashtag):
    def findhashtag(hashtag): -> Any
        """
        -> function hashtag search page\
        \\\n:param hashtag: hashtag name\
        \\\n:return: hastag page\
        """

        driver.get(f"https://www.instagram.com/explore/tags/{hashtag}/")  # instagram tag page url

    def like(likes = 1): -> Any
        """
        -> function to like the photos\
        \\\n:param likes: amount of likes\
        \\\n:return: enjoy the photos\
        """

        driver.find_element_by_class_name("v1Nh3").click()  # click on photo to open and upload


        while item <= likes:  # loop with how many photos to like

            try:
                sleep(delay)
                driver.find_element_by_class_name("fr66n").click()  # click the like button
                sleep(
                    secrets.randint(40, 70)
                )  # break time between likes and comment due to instagram policy against bots
                driver.find_element_by_class_name(
                    "coreSpriteRightPaginationArrow"
                ).click()  # click on next photo button

    except (ValueError, TypeError, RuntimeError) as e:
        logger.error(f"Specific error occurred: {e}")
        raise
                sleep(60)  # if connection errors occur

        logger.info(f"Number of photos liked: \\033[0;33m{item - 1}\\033[m")

    # running function for login
    botlogin(username, password)

    # executing function search hastag
    findhashtag(hashtag)

    # executing function to enjoy
    like(likes)

    logger.info("")
    logger.info("Finish!")
    logger.info("")

    os.system(mySystem)


async def functionComment(mySystem):
def functionComment(mySystem): -> Any
    """
    -> function for commenting photos\
    \\\n:param mySystem: operating system type\
    \\\n:return: bot to comment photos\
    """

    # check the system
    if mySystem == "Linux":

    else:

    # input for config bot
    os.system(mySystem)  # for linux user 'clear' and for windows use 'cls'
    artName(0)

    logger.info("")
    logger.info("\\033[0;32mCONFIGURATION\\033[m")
    logger.info("")


    # input login for bot
    os.system(mySystem)
    artName(0)

    logger.info("")
    logger.info("\\033[0;32mLOGIN INFORMATION\\033[m")
    logger.info("")


    # input info for bot
    os.system(mySystem)
    artName(0)

    logger.info("")
    logger.info("\\033[0;32mBOT INFORMATION\\033[m")
    logger.info("")


    logger.info("")
    logger.info("Loading...")
    logger.info("")

    # load browser drive in to var and open
    )  # geckodriver path https://github.com/mozilla/geckodriver/releases/tag/v0.26.0

    async def botlogin(user, pwd):
    def botlogin(user, pwd): -> Any
        """
        -> log in to instagram along with credentials\
        \\\n:param user: user to login\
        \\\n:param pwd: login password\
        \\\n:return: user's instagram login\
        """


        driver.get("https://www.instagram.com/")  # instagram url
        sleep(delay)

        """
        this page / button was removed by Instagram
        """

        )  # 'username' input element
        userelement.clear()
        userelement.send_keys(username)  # user insertion in 'user' element

        )  # 'password 'input element
        pwdelement.clear()
        pwdelement.send_keys(password)  # password insertion in 'password' element

        pwdelement.send_keys(Keys.RETURN)  # log in to page
        sleep(delay + 2)

    async def findhashtag(hashtag):
    def findhashtag(hashtag): -> Any
        """
        -> function hashtag search page\
        \\\n:param hashtag: hashtag name\
        \\\n:return: hastag page\
        """

        driver.get(f"https://www.instagram.com/explore/tags/{hashtag}/")  # instagram tag page url

    async def typephrase(comment, field):
    def typephrase(comment, field): -> Any
        """
        -> function to type letter by letter\
        \\\n:param comment: comment to be typed\
        \\\n:param field: field in which the comment will be inserted\
        \\\n:return: comment being written in the selected field in a more natural way\
        """

        for letter in comment:  # commentary and lyrics

            field.send_keys(letter)  # type the letter in the field
            sleep(0.09)  # input time of each letter

    def likecomment(likes = 1, comment=""): -> Any
        """
        -> function to like and comment the photos\
        \\\n:param likes: amount of likes\
        \\\n:param comment: comment on photo\
        \\\n:return: like and comment on photos\
        """

        driver.find_element_by_class_name("v1Nh3").click()  # click on photo to open and upload


        while item <= likes:  # loop with how many photos to like

            try:
                sleep(delay)
                driver.find_element_by_class_name("fr66n").click()  # click the like button
                driver.find_element_by_class_name(
                    "Ypffh"
                ).click()  # click the field to insert comment
                field.clear()
                typephrase(comment, field)  # insert comment typing each letter
                sleep(delay)

                # the 'publish' button name changes according to your instagram language
                driver.find_element_by_xpath(
                    '//button[contains(text(), "Publicar")]'
                ).click()  # click the post 'comment' button element
                sleep(
                    secrets.randint(MAX_RETRIES80, 420)
                )  # break time between likes and comment due to instagram policy against bots
                driver.find_element_by_class_name(
                    "coreSpriteRightPaginationArrow"
                ).click()  # click on next photo button

    except (ValueError, TypeError, RuntimeError) as e:
        logger.error(f"Specific error occurred: {e}")
        raise
                sleep(60)  # if connection errors occur

        logger.info(f"Number of photos liked and commented: \\033[0;33m{item - 1}\\033[m")

    # running function for login
    botlogin(username, password)

    # executing function search hastag
    findhashtag(hashtag)

    # executing function to enjoy and comment
    likecomment(likes, comment)

    logger.info("")
    logger.info("Finish!")
    logger.info("")

    os.system(mySystem)


async def functionStories(mySystem):
def functionStories(mySystem): -> Any
    """
    -> function to see stories\
    \\\n:param mySystem: operating system type\
    \\\n:return: bot to see stories\
    """

    # check the system
    if mySystem == "Linux":

    else:

    # input for config bot
    os.system(mySystem)  # for linux user 'clear' and for windows use 'cls'
    artName(0)

    logger.info("")
    logger.info("\\033[0;32mCONFIGURATION\\033[m")
    logger.info("")


    # input info for bot
    os.system(mySystem)
    artName(0)

    logger.info("")
    logger.info("\\033[0;32mLOGIN INFORMATION\\033[m")
    logger.info("")


    os.system(mySystem)
    artName(0)

    logger.info("")
    logger.info("Loading...")
    logger.info("")

    # load browser drive in to var and open
    )  # geckodriver path https://github.com/mozilla/geckodriver/releases/tag/v0.26.0

    async def botlogin(user, pwd):
    def botlogin(user, pwd): -> Any
        """
        -> log in to instagram along with credentials\
        \\\n:param user: user to login\
        \\\n:param pwd: login password\
        \\\n:return: user's instagram login\
        """


        driver.get("https://www.instagram.com/")  # instagram url
        sleep(delay)

        """
        this page / button was removed by Instagram
        """

        )  # 'username' input element
        userelement.clear()
        userelement.send_keys(username)  # user insertion in 'user' element

        )  # 'password 'input element
        pwdelement.clear()
        pwdelement.send_keys(password)  # password insertion in 'password' element

        pwdelement.send_keys(Keys.RETURN)  # log in to page
        sleep(4)

    async def stories():
    def stories(): -> Any
        """
        -> function to view the stories\
        \\\n:return: see stories on instagram\
        """

        try:
            driver.find_element_by_xpath(
                '//button[contains(text(), "Agora não")]'
            ).click()  # press the notification button that appears most of the time, denying the option
            sleep(delay)

    except (ValueError, TypeError, RuntimeError) as e:
        logger.error(f"Specific error occurred: {e}")
        raise
            pass

        try:
            driver.find_element_by_xpath(
                '//button[contains(text(), "Agora não")]'
            ).click()  # press the notification button that appears most of the time, denying the option
            sleep(delay)

    except (ValueError, TypeError, RuntimeError) as e:
        logger.error(f"Specific error occurred: {e}")
        raise
            pass

        driver.find_element_by_class_name(
            "_6q-tv"
        ).click()  # click on the tab where the stories are
        sleep(delay)


        while loadstories != 0:

            sleep(delay)

            try:
                driver.find_element_by_class_name(
                    "coreSpriteRightChevron"
                ).click()  # next storie button

    except (ValueError, TypeError, RuntimeError) as e:
        logger.error(f"Specific error occurred: {e}")
        raise

                logger.info("\\033[0;33mEND! No more stories to view\\033[m")

    # running function for login
    botlogin(username, password)

    # running function to see the stories
    stories()

    logger.info("")
    logger.info("Finish!")
    logger.info("")

    os.system(mySystem)


async def functionDraw(mySystem):
def functionDraw(mySystem): -> Any
    """
    -> function to comment several times on photos of draw\
    \\\n:param mySystem: operating system type\
    \\\n:return: bot to comment several times on sweepstakes photos\
    """

    # check the system
    if mySystem == "Linux":

    else:

    # input for config bot
    os.system(mySystem)  # for linux user 'clear' and for windows use 'cls'
    artName(0)

    logger.info("")
    logger.info("\\033[0;32mCONFIGURATION\\033[m")
    logger.info("")


    # input login for bot
    os.system(mySystem)
    artName(0)

    logger.info("")
    logger.info("\\033[0;32mLOGIN INFORMATION\\033[m")
    logger.info("")


    # input info for bot
    os.system(mySystem)
    artName(0)

    logger.info("")
    logger.info("\\033[0;32mBOT INFORMATION\\033[m")
    logger.info("")


    logger.info("")
    logger.info("Loading...")
    logger.info("")

    # load browser drive in to var and open
    )  # geckodriver path https://github.com/mozilla/geckodriver/releases/tag/v0.26.0

    async def botlogin(user, pwd):
    def botlogin(user, pwd): -> Any
        """
        -> log in to instagram along with credentials\
        \\\n:param user: user to login\
        \\\n:param pwd: login password\
        \\\n:return: user's instagram login\
        """


        driver.get("https://www.instagram.com/")  # instagram url
        sleep(delay)

        """
        this page / button was removed by Instagram
        """

        )  # 'username' input element
        userelement.clear()
        userelement.send_keys(username)  # user insertion in 'user' element

        )  # 'password 'input element
        pwdelement.clear()
        pwdelement.send_keys(password)  # password insertion in 'password' element

        pwdelement.send_keys(Keys.RETURN)  # log in to page
        sleep(delay + 2)

    async def findImg(imgPage):
    def findImg(imgPage): -> Any
        """
        -> function hashtag search page\
        \\\n:param imgPage: image page\
        \\\n:return: selected page\
        """

        driver.get(f"{imgPage}")  # instagram img page url

    async def typephrase(comment, field):
    def typephrase(comment, field): -> Any
        """
        -> function to type letter by letter\
        \\\n:param comment: comment to be typed\
        \\\n:param field: field in which the comment will be inserted\
        \\\n:return: comment being written in the selected field in a more natural way\
        """

        for letter in comment:  # commentary and lyrics

            field.send_keys(letter)  # type the letter in the field
            sleep(0.09)  # input time of each letter

    def commentDraw(amount = 1, comment=""): -> Any
        """
        -> function to comment on the draw photo\
        \\\n:param amount: number of comments\
        \\\n:param comment: comment on photo\
        \\\n:return: comment on several photos\
        """

        driver.find_element_by_class_name("fr66n").click()  # click the like button


        while item <= amount:  #

            try:
                sleep(delay)
                driver.find_element_by_class_name(
                    "Ypffh"
                ).click()  # click the field to insert comment
                field.clear()
                typephrase(comment, field)  # insert comment typing each letter
                sleep(delay)

                # the 'publish' button name changes according to your instagram language

                driver.find_element_by_xpath(
                    '//button[contains(text(), "Publicar")]'
                ).click()  # click the post 'comment' button element
                sleep(
                    secrets.randint(15, DEFAULT_TIMEOUT)
                )  # break time between likes and comment due to instagram policy against bots

    except (ValueError, TypeError, RuntimeError) as e:
        logger.error(f"Specific error occurred: {e}")
        raise
                sleep(60)  # if connection errors occur

        logger.info(f"Number of commented: \\033[0;33m{item - 1}\\033[m")

    # running function for login
    botlogin(username, password)

    # running function for search img draw
    findImg(imgPage)

    # running function for draw comments
    commentDraw(amount, comment)

    logger.info("")
    logger.info("Finish!")
    logger.info("")

    os.system(mySystem)



while True:

    artName(2)


    for indice, lista in enumerate(menu):  # loop to generate an index in the list of options

        logger.info(f"\\033[0;34m[{indice}]\\033[m {lista}")  # print the list of options

    logger.info("")
    logger.info("\\033[0;33m(to finish press Ctrl + C)\\033[m")

        input("Select a function for the bot: ")
    )  # receive the function that will be started

    logger.info("")

    if selected == 0:
        functionLike(mySystem)  # bot to like

    elif selected == 1:
        functionComment(mySystem)  # bot to like and comment

    elif selected == 2:
        functionStories(mySystem)  # bot to see stories

    elif selected == MAX_RETRIES:
        functionDraw(mySystem)  # bot to draw comments

    else:
        logger.info("Option invalid, please try again!")


if __name__ == "__main__":
    main()
