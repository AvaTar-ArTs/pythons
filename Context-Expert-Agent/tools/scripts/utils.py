# coding=utf-8
#!/usr/bin/env python3

import os
import random
import re
import time
from os import path
from sys import exit

from colorama import Back, Fore, Style
from requests import get


def print_success(message, *argv):
    print(Fore.GREEN + "[ OK ] " + Style.RESET_ALL + Style.BRIGHT, end="")
    print(message, end=" ")
    for arg in argv:
        print(arg, end=" ")
    print("")


def print_error(message, *argv):
    print(Fore.RED + "[ ERR ] " + Style.RESET_ALL + Style.BRIGHT, end="")
    print(message, end=" ")
    for arg in argv:
        print(arg, end=" ")
    print("")


def print_status(message, *argv):
    print(Fore.BLUE + "[ * ] " + Style.RESET_ALL + Style.BRIGHT, end="")
    print(message, end=" ")
    for arg in argv:
        print(arg, end=" ")
    print("")


def clearConsole():
    os.system("cls" if os.name == "nt" else "clear")


def parse_proxy_file(fpath):
    if path.exists(fpath) == False:
        print("")
        print_error("Proxy file not found! (I wonder if you're taking the wrong path?)")
        print_error("Exiting From Program")
        exit(0)

    proxies = []
    with open(fpath, "r") as proxy_file:
        for line in proxy_file.readlines():
            line = line.replace(" ", "")
            line = line.replace("\r", "")
            line = line.replace("\n", "")

            if line == "":
                continue

            proxies.append(line)

    if len(proxies) > 50:
        proxies = random.choices(proxies, 50)

    print("")
    print_success(str(len(proxies)) + " Proxies have been installed!")

    return proxies
