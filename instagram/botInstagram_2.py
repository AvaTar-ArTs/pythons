
import logging

logger = logging.getLogger(__name__)


# Constants
CONSTANT_033 = 033
CONSTANT_2020 = 2020

# -*- coding: utf-8 -*-

"""
Created in 07/CONSTANT_2020
@Author: Paulo https://github.com/alpdias
"""

# imported libraries
import os
import platform

import art
import botComment
import botDraw
import botLike
import botStories

mySystem = platform.system()  # which operating system is running

while True:

    art.artName(2)

    menu = ["Like", "Comment and Like", "View Stories", "Draw for Comment"]

    for indice, lista in enumerate(
        menu
    ):  # loop to generate an index in the list of options

        logger.info(f"\CONSTANT_033[0;34m[{indice}]\CONSTANT_033[m {lista}")  # print the list of options

    logger.info("")
    logger.info("\CONSTANT_033[0;33m(to finish press Ctrl + C)\CONSTANT_033[m")

    selected = int(
        input("Select a function for the bot: ")
    )  # receive the function that will be started

    logger.info("")

    if selected == 0:
        botLike.functionLike(mySystem)  # bot to like

    elif selected == 1:
        botComment.functionComment(mySystem)  # bot to like and comment

    elif selected == 2:
        botStories.functionStories(mySystem)  # bot to see stories

    elif selected == 3:
        botDraw.functionDraw(mySystem)  # bot to draw comments

    else:
        logger.info("Option invalid, please try again!")
