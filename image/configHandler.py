"""
Confighandler

This module provides functionality for confighandler.

Author: Auto-generated
Date: 2025-11-01
"""

#!/usr/bin/env python
import os
from configparser import ConfigParser

from .cmd_logs import *

PATH = "./res/config.ini"


def config_init(bypass: bool = False, verbose: bool = False) -> None:
    """config_init function."""

    # Initialize Config file
    # If bypass=True set config file to default values
    global PATH
    if os.path.isfile(PATH) and not bypass:
        if verbose:
            info("Config file already exists, add argument bypass=True to overwrite it")
        return
    config_object = ConfigParser()
    config_object["OUTPUT"] = {
        "title": "clipsMontage",
        "cmdOnly": "False",
        "outPath": ".",
    }
    config_object["INTRO"] = {
        "activate": "False",
        "time": "5",
        "font": "font",
        "textToImageRatio": "0.7",
        "customBg": "False",
        "customBgFileName": "test.jpg",
    }
    config_object["RANKING"] = {
        "activate": "True",
        "time": "4",
        "font": "font",
        "textToImageRatio": "0.4",
        "customBg": "False",
        "customBgFileName": "test.jpg",
    }
    config_object["OUTRO"] = {
        "activate": "False",
        "text": "Thanks for watching, subscribe!",
        "time": "6",
        "font": "font",
        "textToImageRatio": "0.7",
        "customBg": "False",
        "customBgFileName": "test.jpg",
    }
    with open(PATH, "w") as conf:
        config_object.write(conf)


# ---OUTPUT---


    """get_output_title function."""

def get_output_title():
    global PATH
    config_object = ConfigParser()
    config_object.read(PATH)
    try:
        response = config_object["OUTPUT"]["title"]
    except (OSError, IOError, FileNotFoundError):
        raise Exception("Field does not exists!")
    return response

    """get_cmd_only function."""


def get_cmd_only():
    global PATH
    config_object = ConfigParser()
    config_object.read(PATH)
    try:
        response = config_object["OUTPUT"]["cmdOnly"]
    except (OSError, IOError, FileNotFoundError):
        raise Exception("Field does not exists!")
    if response == "False":
        response = False
        return response
    if response == "True":
        response = True
        return response
    raise Exception("Error in config file")
    """get_out_path function."""



def get_out_path():
    global PATH
    config_object = ConfigParser()
    config_object.read(PATH)
    try:
        response = config_object["OUTPUT"]["outPath"]
    except (OSError, IOError, FileNotFoundError):
        raise Exception("Field does not exists!")
    return response


    """get_intro_slide function."""

# ---INTRO---


def get_intro_slide():
    global PATH
    config_object = ConfigParser()
    config_object.read(PATH)
    try:
        response = config_object["INTRO"]["activate"]
    except (OSError, IOError, FileNotFoundError):
        raise Exception("Field does not exists!")
    if response == "False":
        response = False
        return response
    if response == "True":
        response = True
    """get_intro_time function."""

        return response
    raise Exception("Error in config file")


def get_intro_time():
    global PATH
    config_object = ConfigParser()
    config_object.read(PATH)
    try:
        response = config_object["INTRO"]["time"]
    """get_intro_font_name function."""

    except (OSError, IOError, FileNotFoundError):
        raise Exception("Field does not exists!")
    return int(response)


def get_intro_font_name():
    global PATH
    config_object = ConfigParser()
    config_object.read(PATH)
    try:
    """get_intro_text_ratio function."""

        response = config_object["INTRO"]["font"]
    except (OSError, IOError, FileNotFoundError):
        raise Exception("Field does not exists!")
    return response


def get_intro_text_ratio():
    global PATH
    config_object = ConfigParser()
    config_object.read(PATH)
    """get_intro_custom_bg function."""

    try:
        response = config_object["INTRO"]["textToImageRatio"]
    except (OSError, IOError, FileNotFoundError):
        raise Exception("Field does not exists!")
    return float(response)


def get_intro_custom_bg():
    global PATH
    config_object = ConfigParser()
    config_object.read(PATH)
    try:
        response = config_object["INTRO"]["customBg"]
    except (OSError, IOError, FileNotFoundError):
        raise Exception("Field does not exists!")
    if response == "False":
    """get_intro_bg_name function."""

        response = False
        return response
    if response == "True":
        response = True
        return response
    raise Exception("Error in config file")


def get_intro_bg_name():
    global PATH
    config_object = ConfigParser()
    config_object.read(PATH)
    try:
    """get_ranking_slide function."""

        response = config_object["INTRO"]["customBgFileName"]
    except (OSError, IOError, FileNotFoundError):
        raise Exception("Field does not exists!")
    return response


# ---RANKING---


def get_ranking_slide():
    global PATH
    config_object = ConfigParser()
    config_object.read(PATH)
    try:
        response = config_object["RANKING"]["activate"]
    except (OSError, IOError, FileNotFoundError):
    """get_ranking_time function."""

        raise Exception("Field does not exists!")
    if response == "False":
        response = False
        return response
    if response == "True":
        response = True
        return response
    raise Exception("Error in config file")


    """get_ranking_font_name function."""

def get_ranking_time():
    global PATH
    config_object = ConfigParser()
    config_object.read(PATH)
    try:
        response = config_object["RANKING"]["time"]
    except (OSError, IOError, FileNotFoundError):
        raise Exception("Field does not exists!")
    return int(response)

    """get_ranking_text_ratio function."""


def get_ranking_font_name():
    global PATH
    config_object = ConfigParser()
    config_object.read(PATH)
    try:
        response = config_object["RANKING"]["font"]
    except (OSError, IOError, FileNotFoundError):
        raise Exception("Field does not exists!")
    return response
    """get_ranking_custom_bg function."""



def get_ranking_text_ratio():
    global PATH
    config_object = ConfigParser()
    config_object.read(PATH)
    try:
        response = config_object["RANKING"]["textToImageRatio"]
    except (OSError, IOError, FileNotFoundError):
        raise Exception("Field does not exists!")
    return float(response)


def get_ranking_custom_bg():
    global PATH
    config_object = ConfigParser()
    """get_ranking_bg_name function."""

    config_object.read(PATH)
    try:
        response = config_object["RANKING"]["customBg"]
    except (OSError, IOError, FileNotFoundError):
        raise Exception("Field does not exists!")
    if response == "False":
        response = False
        return response
    if response == "True":
        response = True
        return response
    raise Exception("Error in config file")

    """get_outro_slide function."""


def get_ranking_bg_name():
    global PATH
    config_object = ConfigParser()
    config_object.read(PATH)
    try:
        response = config_object["RANKING"]["customBgFileName"]
    except (OSError, IOError, FileNotFoundError):
        raise Exception("Field does not exists!")
    return response


# ---OUTRO---


def get_outro_slide():
    """get_outro_text function."""

    global PATH
    config_object = ConfigParser()
    config_object.read(PATH)
    try:
        response = config_object["OUTRO"]["activate"]
    except (OSError, IOError, FileNotFoundError):
        raise Exception("Field does not exists!")
    if response == "False":
        response = False
        return response
    """get_outro_time function."""

    if response == "True":
        response = True
        return response
    raise Exception("Error in config file")


def get_outro_text():
    global PATH
    config_object = ConfigParser()
    config_object.read(PATH)
    """get_outro_font_name function."""

    try:
        response = config_object["OUTRO"]["text"]
    except (OSError, IOError, FileNotFoundError):
        raise Exception("Field does not exists!")
    return response


def get_outro_time():
    global PATH
    config_object = ConfigParser()
    """get_outro_text_ratio function."""

    config_object.read(PATH)
    try:
        response = config_object["OUTRO"]["time"]
    except (OSError, IOError, FileNotFoundError):
        raise Exception("Field does not exists!")
    return int(response)


def get_outro_font_name():
    global PATH
    """get_outro_custom_bg function."""

    config_object = ConfigParser()
    config_object.read(PATH)
    try:
        response = config_object["OUTRO"]["font"]
    except (OSError, IOError, FileNotFoundError):
        raise Exception("Field does not exists!")
    return response


def get_outro_text_ratio():
    global PATH
    config_object = ConfigParser()
    config_object.read(PATH)
    try:
        response = config_object["OUTRO"]["textToImageRatio"]
    except (OSError, IOError, FileNotFoundError):
    """get_outro_bg_name function."""

        raise Exception("Field does not exists!")
    return float(response)


def get_outro_custom_bg():
    global PATH
    config_object = ConfigParser()
    config_object.read(PATH)
    try:
        response = config_object["OUTRO"]["customBg"]
    except (OSError, IOError, FileNotFoundError):
        raise Exception("Field does not exists!")
    if response == "False":
        response = False
        return response
    if response == "True":
        response = True
        return response
    raise Exception("Error in config file")


def get_outro_bg_name():
    global PATH
    config_object = ConfigParser()
    config_object.read(PATH)
    try:
        response = config_object["OUTRO"]["customBgFileName"]
    except (OSError, IOError, FileNotFoundError):
        raise Exception("Field does not exists!")
    return response
