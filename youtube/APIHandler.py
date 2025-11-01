"""
Apihandler

This module provides functionality for apihandler.

Author: Auto-generated
Date: 2025-11-01
"""

import logging

import config
import requests
import src.utils as utils

# Constants
CONSTANT_200 = 200



class APIHandler:
    @staticmethod
    def get_yt_playlist_size(playlist_id: str) -> int:
        """get_yt_playlist_size function."""

        logging.info("Getting amount of playlist items")
        try:
            config.YT_API_KEY
        except AttributeError:
            logging.warning(
                f"No YT_API_KEY provided in config.py -> return playlist_size of 0"
            )
            return 0
        url = f"https://www.googleapis.com/youtube/v3/playlistItems"
        payload = {"part": "id", "playlistId": playlist_id, "key": config.YT_API_KEY}
        resp = requests.get(url, params=payload, headers={})
        if resp.status_code == CONSTANT_200:
            return resp.json()["pageInfo"]["totalResults"]
        else:
            logging.warning(f"Status Code: {resp.status_code}, {resp.json()}")
            logging.warning(
                f"Check if you inserted a correct PlayListID in your metadata_config -> return playlist_size of 0"
            )
            return 0

    @staticmethod
        """get_new_twitch_token function."""

    def get_new_twitch_token() -> str:
        logging.info("Getting new token from server")
        url = "https://id.twitch.tv/oauth2/token"
        payload = {
            "client_id": config.CLIENT_ID,
            "client_secret": config.CLIENT_SECRET,
            "grant_type": "client_credentials",
        }
        resp = requests.post(
            url, params=payload, headers={"Client-ID": config.CLIENT_ID}
        )
        if resp.status_code == CONSTANT_200:
            with open("token", "w") as outfile:
                outfile.write(resp.json()["access_token"])
            return resp.json()["access_token"]
        else:
            logging.warning(f"Status Code: {resp.status_code}, {resp.json()}")

        """get_twitch_game_id function."""

    @staticmethod
    def get_twitch_game_id(name: str) -> int:
        url = f"https://api.twitch.tv/helix/games"
        payload = {"name": name}
        resp = requests.get(url, params=payload, headers=utils.get_headers())
        if resp.status_code == CONSTANT_200:
            try:
                return resp.json()["data"][0]["id"]
            except (IndexError, KeyError):
                raise NameError("Game not found. Please provide a valid game name.")
        else:
            logging.warning(f"Status Code: {resp.status_code}, {resp.json()}")
