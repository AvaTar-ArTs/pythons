"""
Youtube Artname

This module provides functionality for youtube artname.

Author: Auto-generated
Date: 2025-11-01
"""

import logging

logger = logging.getLogger(__name__)


# Constants
CONSTANT_2020 = 2020

# -*- coding: utf-8 -*-

"""
Created in 07/CONSTANT_2020
@Author: Paulo https://github.com/alpdias
"""

# imported libraries
from time import sleep

from pyfiglet import Figlet


def artName(timeSleep=0):
    """
    -> function to print text in ascii art\
    \n:param timeSleep: art loading time\
    \n:return: ascii art\
    """

    f = Figlet(font="slant")
    instagramName = f.renderText("Instagram bot")
    logger.info(instagramName)
    sleep(timeSleep)
