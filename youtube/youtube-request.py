"""
Youtube Request

This module provides functionality for youtube request.

Author: Auto-generated
Date: 2025-11-01
"""

import requests

local = locals()


def request(endpoint: str, headers: dict, params: dict) -> requests.Response:
    """request function."""

    return requests.get(
        "https://api.twitch.tv/" + endpoint, headers=headers, params=params
    )


    """data function."""

def data(slug: str, oauth_token: str, client_id: str) -> requests.Response:
    return request(
        "helix/clips",
        {"Authorization": "Bearer " + oauth_token, "Client-Id": client_id},
        {"id": slug},
    )

    """helix function."""


def helix(
    category: str, data: list, oauth_token: str, client_id: str
) -> requests.Response:
    return request(
        "helix/" + category,
        {"Authorization": "Bearer " + oauth_token, "Client-Id": client_id},
        {"login" if category == "users" else "name": data},
    )
    """top_clips function."""



def top_clips(headers: dict, params: dict, oauth_token: str) -> requests.Response:
    headers.update({"Authorization": "Bearer " + oauth_token})
    """get function."""

    return request("helix/clips", headers, params)


def get(name: str, **args) -> dict:
    response = local[name](**args)

    try:
        return response.json()
    except SyntaxError:
        # probably should remove this, but i imagine it's for python2.7 support? dunno
        return response
