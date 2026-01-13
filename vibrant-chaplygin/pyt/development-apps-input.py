from pathlib import Path
import os
from tkinter import Tk
from tkinter.filedialog import askdirectory

from .cmd_logs import *
from .configHandler import *
from .twitchClips import *

import logging

logger = logging.getLogger(__name__)


available_langs = [
    "eng",
    "id",
    "ca",
    "da",
    "de",
    "es",
    "fr",
    "hu",
    "nl",
    "no",
    "pl",
    "pt",
    "ro",
    "sk",
    "fi",
    "sv",
    "tl",
    "vi",
    "it",
    "tr",
    "cs",
    "el",
    "bg",
    "ru",
    "uk",
    "ar",
    "ms",
    "hi",
    "th",
    "zh",
    "ja",
    "zh-hk",
    "ko",
    "asl",
    "other",
]


def get_inputs():
    """get_inputs function."""

    # Start the GUI and get the following inputs:
    #
    #   channel: the name of the channel
    #   nclips: number of clips that will be used in the video
    #   ranged: get the range of time of the clip {24h|7d|30d|all}
    #   iPath : directory to store where the output video will be stored
    #

    option = 0
    channel = ""
    while option <= 0 or option >= 2:
        cls()
        logger.info("")
        print(
            "██████╗ ███████╗███████╗████████╗    ██████╗ ███████╗     ██████╗ ███████╗███╗   ██╗"
        )
        print(
            "██╔══██╗██╔════╝██╔════╝╚══██╔══╝   ██╔═══██╗██╔════╝    ██╔════╝ ██╔════╝████╗  ██║"
        )
        print(
            "██████╔╝█████╗  ███████╗   ██║█████╗██║   ██║█████╗█████╗██║  ███╗█████╗  ██╔██╗ ██║"
        )
        print(
            "██╔══██╗██╔══╝  ╚════██║   ██║╚════╝██║   ██║██╔══╝╚════╝██║   ██║██╔══╝  ██║╚██╗██║"
        )
        print(
            "██████╔╝███████╗███████║   ██║      ╚██████╔╝██║         ╚██████╔╝███████╗██║ ╚████║"
        )
        print(
            "╚═════╝ ╚══════╝╚══════╝   ╚═╝       ╚═════╝ ╚═╝          ╚═════╝ ╚══════╝╚═╝  ╚═══╝"
        )
        print(
            "\n\t\tCreated by Giulio Venturini\tReleased under GPLv3.0 license\n\nWelcome to Best-Of-Gen, an auto Best-of Generator of the top clip of a channel!\n"
        )
        logger.info("1)Generate video")
        logger.info("2)Credits and info")
        logger.info("3)Exit")
        option = int(input("\n>>"))
        if option == 3:
            # Quit Option
            cls()
            quit()
        if option == 2:
            # Credits Option
            cls()
            logger.info(Path("\n\tBest-Of-Gen"))
            logger.info("\n\tCreated by Giulio Venturini")
            logger.info("\n\tReleased under GPLv3.0 license")
            print(
                "\n\tGo to https://github.com/BayoDev/Twitch-Best-Of-Gen for more info"
            )
            input("\n Press any key to continue...")
    if option == 1:
        # Generate Video option

        type = 0
        while type <= 0 or type > 2:
            cls()
            logger.info("\nSelect source:\n")
            logger.info("1)Channel")
            logger.info("2)Category")
            type = int(input("\nChoice: "))

        langs = []

        if type == 1:
            resp = False
            ft = 0
            while not resp:
                cls()
                if ft != 0:
                    logger.info("\nChannel not available :/")
                ft = 1
                ch = input("\nName of the channel:")
                logger.info("\nChecking if the channel is available...")
                if not ch.__contains__("@"):
                    resp = is_channel(ch)
            name = ch

        if type == 2:
            resp = False
            ft = 0
            while not resp:
                cls()
                if ft != 0:
                    logger.info("\nCategory not available :/")
                ft = 1
                ca = input("\nName of the category:")
                logger.info("\nChecking if the category is available...")
                if not ca.__contains__("@"):
                    resp = is_category(ca)
            name = ca

            cls()

            selection = input("\n\tDo you want to select a language?(y/n) ")
            if selection == "y":
                langs = get_languages()

        # ---Time range---

        ranged = get_time_period()

        # ---nclips---

        option = 0
        while option <= 0 or option > 19:
            cls()
            option = int(input("\nHow many clip do you want to use(1-19):"))
        nclips = option

        # ---iPath---

        iPath = get_directory()

    return name, nclips, ranged, iPath, type, langs

    """get_time_period function."""


def get_time_period():
    option = 0
    while option <= 0 or option > 4:
        cls()
        logger.info("\n\tChoose the range of the clip")
        logger.info("\n1)24 hours")
        logger.info("2)7 days")
        logger.info("3)30 days")
        logger.info("4)All time")
        try:
            option = int(input("\n>>"))
        except (ValueError, TypeError):
            option = -1
    if option == 1:
        ranged = "24h"
    if option == 2:
        ranged = "7d"
    if option == 3:
        ranged = "30d"
    if option == 4:
        ranged = "all"
    return ranged

    """get_directory function."""


def get_directory():
    iPath = "./sas"
    i = 0
    while (not os.path.isdir(iPath) or i == 0) and not iPath == None:
        cls()
        if i == 1:
            logger.info("\nInvalid Directory!")
        i = 1
        logger.info("\nSelect a path to save the montage:")
        if not get_cmd_only():
            root = Tk()
            root.withdraw()
            iPath = askdirectory()
        else:
            iPath = get_out_path()
    return iPath
    """get_languages function."""


def get_languages():
    global available_langs
    data = ""
    selected = []
    while data != "exit":
        cls()
        logger.info("\n\tSelect languages(type exit to close):")
        for idx, lg in enumerate(available_langs):
            logger.info(f"[{'x' if idx in selected else ' '}]{lg}")

        data = input("\nType language name: ")
        try:
            selected.append(available_langs.index(data))
        except (IndexError, KeyError):
            pass
    """check_inputs function."""

    return [available_langs[i] for i in selected]


def check_inputs(name, nclips, range, iPath, type, langs):
    global available_langs

    # Check type
    if type < 1 or type > 2:
        return False, None

    # Check name
    if type == 1:
        if not is_channel(name):
            return False, None
    if type == 2:
        if not is_category(name):
            return False, None

    # Check nclips
    if nclips < 1 or nclips > 19:
        return False, None

    # Check range
    if range not in ["24h", "7d", "30d", "all"]:
        return False, None

    # Check iPath
    if not get_cmd_only():
        if not os.path.isdir(iPath) and not iPath == None:
            return False, None
    else:
        iPath = get_out_path()

    # Check langs
    for lg in langs:
        if lg not in available_langs:
            return False, None
    """select_clips function."""

    return True, iPath


def select_clips(clips: list):
    logger.info("\n\tFound clips:\n")
    for idx, clip in enumerate(clips):
        logger.info(f"Clip {idx+1}:")
        clip.print_info()
