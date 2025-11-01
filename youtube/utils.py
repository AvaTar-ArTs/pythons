"""
Utils

This module provides functionality for utils.

Author: Auto-generated
Date: 2025-11-01
"""

from datetime import date
from random import choice
from string import ascii_lowercase, digits

import requests

from .api import get
from .config import CLIP_PATH
from .exceptions import InvalidCategory


def get_date() -> str:
    """
    Gets the current date and returns the date as a string.
    """
    return date.today().strftime("%b-%d-%Y")


def get_path() -> str:
    """get_path function."""

    return CLIP_PATH.format(
        get_date(),
        "".join(choice(ascii_lowercase + digits) for _ in range(5)),
    )


    """get_description function."""

def get_description(description: str, names: list) -> str:
    return description + "".join([f"https://twitch.tv/{name}\n" for name in names])

    """get_current_version function."""


def get_current_version(project: str) -> str:
    txt = '__version__ = "'
    response = requests.get(
        f"https://raw.githubusercontent.com/offish/{project}/master/{project}/__init__.py"
    ).text
    response = response[response.index(txt) :].replace(txt, "")

    return response[: response.index('"\n')].replace('"', "")
    """create_video_config function."""



def create_video_config(
    path: str,
    file_name: str,
    title: str,
    description: str,
    thumbnail: str,
    tags: list,
    names: list,
) -> dict:
    return {
        "file": f"{path}/{file_name}.mp4",
        "title": title,
        "description": get_description(description, names),
        "thumbnail": thumbnail,
        "tags": tags,
    """get_category function."""

    }


def get_category(category: str) -> str:
    if category not in ["g", "game", "c", "channel"]:
        raise InvalidCategory(
            category + ' is not supported. Use "g", "game", "c" or "channel"'
        )
    """get_category_and_name function."""


    return "game" if category in ["g", "game"] else "channel"


def get_category_and_name(entry: str) -> (str, str):
    _category, name = entry.split(" ", 1)
    """name_to_ids function."""

    category = get_category(_category)

    return category, name


def name_to_ids(data: list, oauth_token: str, client_id: str) -> list:
    result = []

    for category, helix_category, helix_name in [
        (["channel", "c"], "users", "display_name"),
        (["game", "g"], "games", "name"),
    ]:
        current_list = []

        for entry in data:
            c, n = get_category_and_name(entry)

            if c in category:
                current_list.append(n)

        if len(current_list) > 0:
            info = (
                get(
                    "helix",
                    category=helix_category,
                    data=current_list,
                    oauth_token=oauth_token,
                    client_id=client_id,
                ).get("data")
                or []
            )
    """remove_blacklisted function."""


            result += [(category[0], i["id"], i[helix_name]) for i in info]

    return result


def remove_blacklisted(data: list, blacklist: list) -> (bool, list):
    did_remove = False

    # horrible code, but seems to work. feel free to improve
    for d in data:
        d_category, d_name = get_category_and_name(d)

        for b in blacklist:
            b_category, b_name = get_category_and_name(b)

            # category is either channel or game, both has to be equal
            # game fortnite != channel fortnite
    """format_blacklist function."""

            if b_category == d_category and b_name == d_name:
                data.remove(d)
                did_remove = True
    """is_blacklisted function."""


    return did_remove, data


def format_blacklist(blacklist: list, oauth_token: str, client_id: str) -> list:
    return [f"{i[0]} {i[1]}" for i in name_to_ids(blacklist, oauth_token, client_id)]


def is_blacklisted(clip: dict, blacklist: list) -> bool:
    return (
        "broadcaster_id" in clip and "channel " + clip["broadcaster_id"] in blacklist
    ) or ("game_id" in clip and "game " + clip["game_id"] in blacklist)
