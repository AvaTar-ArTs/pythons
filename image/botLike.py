
import logging

logger = logging.getLogger(__name__)


# Constants
CONSTANT_033 = 033
CONSTANT_2019 = 2019

# -*- coding: utf-8 -*-

"""
Created in 12/CONSTANT_2019
@Author: Paulo https://github.com/alpdias
"""

# imported libraries
import os
import random
from pathlib import Path
from time import sleep

import art
from selenium import webdriver
from selenium.webdriver.common.keys import Keys


def functionLike(mySystem):
    """
    -> function to enjoy photos\
    \n:param mySystem: operating system type\
    \n:return: bot to enjoy photos\
    """

    # check the system
    if mySystem == "Linux":
        mySystem = "clear"
        way = Path("geckodriver/linux/geckodriver-v0.26.0-linux64")  # path to the file
        geckoFile = way / "geckodriver"  # way to geckodriver

    else:
        mySystem = "cls"
        way = Path("geckodriver/windows")
        geckoFile = way / "geckodriver.exe"

    # input for config bot
    os.system(mySystem)  # for linux user 'clear' and for windows use 'cls'
    art.artName(0)

    logger.info("")
    logger.info("\CONSTANT_033[0;32mCONFIGURATION\CONSTANT_033[m")
    logger.info("")

    delay = int(input("Delay (just number): "))  # loading delay time

    # input login for bot
    os.system(mySystem)
    art.artName(0)

    logger.info("")
    logger.info("\CONSTANT_033[0;32mLOGIN INFORMATION\CONSTANT_033[m")
    logger.info("")

    username = str(input("User: "))  # your user
    password = str(input("Password: "))  # your password

    # input info for bot
    os.system(mySystem)
    art.artName(0)

    logger.info("")
    logger.info("\CONSTANT_033[0;32mBOT INFORMATION\CONSTANT_033[m")
    logger.info("")

    hashtag = str(input("Hashtag: "))  # hashtag
    likes = int(input("Amount: "))  # amount of photos to like

    logger.info("")
    logger.info("Loading...")
    logger.info("")

    # load browser drive in to var and open
    try:
        driver = webdriver.Firefox(
            executable_path=f"{geckoFile}"
        )  # geckodriver path https://github.com/mozilla/geckodriver/releases/tag/v0.26.0

    except (OSError, IOError, FileNotFoundError):
        logger.info("\CONSTANT_033[0;31mDRIVER ERROR!\CONSTANT_033[m Check installed drive or path.")

    def botlogin(user, pwd):
        """
        -> log in to instagram along with credentials\
        \n:param user: user to login\
        \n:param pwd: login password\
        \n:return: user's instagram login\
        """

        username = user  # your user
        password = pwd  # your password

        driver.get("https://www.instagram.com/")  # instagram url
        sleep(delay)

        """
        this page / button was removed by Instagram
        driver.find_element_by_xpath('//a[@href="/accounts/login/?source=auth_switcher"]').click() # click on the 'connect' button element
        """

        userelement = driver.find_element_by_xpath(
            '//input[@name="username"]'
        )  # 'username' input element
        userelement.clear()
        userelement.send_keys(username)  # user insertion in 'user' element

        pwdelement = driver.find_element_by_xpath(
            '//input[@name="password"]'
        )  # 'password 'input element
        pwdelement.clear()
        pwdelement.send_keys(password)  # password insertion in 'password' element

        pwdelement.send_keys(Keys.RETURN)  # log in to page
        sleep(delay + 2)

    def findhashtag(hashtag):
        """
        -> function hashtag search page\
        \n:param hashtag: hashtag name\
        \n:return: hastag page\
        """

        driver.get(
            f"https://www.instagram.com/explore/tags/{hashtag}/"
        )  # instagram tag page url

    def like(likes=1):
        """
        -> function to like the photos\
        \n:param likes: amount of likes\
        \n:return: enjoy the photos\
        """

        driver.find_element_by_class_name(
            "v1Nh3"
        ).click()  # click on photo to open and upload

        item = 1

        while item <= likes:  # loop with how many photos to like

            try:
                sleep(delay)
                driver.find_element_by_class_name(
                    "fr66n"
                ).click()  # click the like button
                sleep(
                    random.randint(40, 70)
                )  # break time between likes and comment due to instagram policy against bots
                driver.find_element_by_class_name(
                    "coreSpriteRightPaginationArrow"
                ).click()  # click on next photo button
                item = item + 1

            except Exception:
                sleep(60)  # if connection errors occur

        logger.info(f"Number of photos liked: \CONSTANT_033[0;33m{item - 1}\CONSTANT_033[m")

    # running function for login
    try:
        botlogin(username, password)

    except KeyboardInterrupt:
        logger.info("\CONSTANT_033[0;33mProgram terminated by the user!\CONSTANT_033[m")

    except (ValueError, TypeError):
        print(
            "\CONSTANT_033[0;31mUNEXPECTED ERROR ON LOGIN\CONSTANT_033[m, please try again and verify your connection!"
        )

    # executing function search hastag
    try:
        findhashtag(hashtag)

    except KeyboardInterrupt:
        logger.info("\CONSTANT_033[0;33mProgram terminated by the user!\CONSTANT_033[m")

    except (ValueError, TypeError):
        print(
            "\CONSTANT_033[0;31mUNEXPECTED ERROR ON HASHTAG PAGE\CONSTANT_033[m, please try again and verify your connection!"
        )

    # executing function to enjoy
    try:
        like(likes)

    except KeyboardInterrupt:
        logger.info("\CONSTANT_033[0;33mProgram terminated by the user!\CONSTANT_033[m")

    except (ValueError, TypeError):
        print(
            "\CONSTANT_033[0;31mUNEXPECTED ERROR ON LIKE\CONSTANT_033[m, please try again and verify your connection!"
        )

    logger.info("")
    logger.info("Finish!")
    logger.info("")

    press = input('\CONSTANT_033[0;34mpress "enter" to continue\CONSTANT_033[m ')
    os.system(mySystem)
