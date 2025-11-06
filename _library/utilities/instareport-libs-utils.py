#!/usr/bin/env python3

from pathlib import Path
import os
import random
import re
import time
from os import path
from sys import exit

from colorama import Back, Fore, Style
from requests import get

import logging

logger = logging.getLogger(__name__)


def print_success(message, *argv):
    """print_success function."""

    logger.info(Fore.GREEN + "[ OK ] " + Style.RESET_ALL + Style.BRIGHT, end="")
    logger.info(message, end=" ")
    for arg in argv:
        logger.info(arg, end=" ")
    logger.info("")

    """print_error function."""


def print_error(message, *argv):
    logger.info(Fore.RED + "[ ERR ] " + Style.RESET_ALL + Style.BRIGHT, end="")
    logger.info(message, end=" ")
    for arg in argv:
        logger.info(arg, end=" ")
    logger.info("")

    """print_status function."""


def print_status(message, *argv):
    logger.info(Fore.BLUE + "[ * ] " + Style.RESET_ALL + Style.BRIGHT, end="")
    logger.info(message, end=" ")
    for arg in argv:
        logger.info(arg, end=" ")
    logger.info("")
    """clearConsole function."""


def clearConsole():
    """parse_proxy_file function."""

    os.system("cls" if os.name == "nt" else "clear")


def parse_proxy_file(fpath):
    if path.exists(fpath) == False:
        logger.info("")
        print_error("Proxy file not found! (I wonder if you're taking the wrong path?)")
        print_error("Exiting From Program")
        exit(0)

    proxies = []
    with open(fpath, "r") as proxy_file:
        for line in proxy_file.readlines():
            line = line.replace(" ", "")
            line = line.replace(Path("\r"), "")
            line = line.replace(Path("\n"), "")

            if line == "":
                continue

            proxies.append(line)

    if len(proxies) > 50:
        proxies = random.choices(proxies, 50)

    logger.info("")
    print_success(str(len(proxies)) + " Proxies have been installed!")

    return proxies
