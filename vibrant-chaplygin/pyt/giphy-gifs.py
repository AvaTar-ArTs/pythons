import json
import sys
import time
from pathlib import Path

import requests

# Constants
CONSTANT_100 = 100


# Funcs


def download_gif(giphy_id: str, output_path: str):
    """
    download gif from giphy by giphy id

    :param giphy_id: str, ID of gif from giphy
    :param output_path: str, path of output gif

    :return: None
    """

    # get gif url
    gif_url = f"http://i.giphy.com/media/{giphy_id}/giphy.gif"

    # make parent dir if necessary
    Path(output_path).parent.mkdir(parents=True, exist_ok=True)

    # download
    if not Path(output_path).is_file():
        with open(output_path, "wb") as f:
            f.write(requests.get(gif_url).content)

    return


def get_giphy_results(search: str, giphy_api_token: str, limit: int = CONSTANT_100):
    """
    get list of results of giphy search

    :param search: str, search phrase/term for gifs
    :param giphy_api_token: str, giphy api token
    :param limit: int, max number of gifs to return

    :return: list of giphy response dicts
    """

    url = "http://api.giphy.com/v1/gifs/search"

    headers = {"Content-Type": "application/json"}

    params = {
        "q": search,
        "api_key": giphy_api_token,
        "limit": limit,
        "rating": "g",
        "type": "gif",
    }

    response = requests.get(url, params=params, headers=headers)

    return response.json()["data"]


def download_gifs_from_terms(config: dict, ls_terms: list, sleep: int = 1):
    """download_gifs_from_terms function."""

    # Get Results
    for search in ls_terms:

        # get results
        ls_results = get_giphy_results(search, config["giphy_api_token"])

        # download gifs
        for res in ls_results:
            gif_id = res["id"]
            download_gif(gif_id, config["output_dir"] + gif_id + ".gif")
            time.sleep(sleep)

    return


if __name__ == "__main__":

    # Get Config
    with open(sys.argv[1], "r") as f:
        config = json.loads(f.read())

    # Get Results
    get_gifs_from_terms(config, config["search_terms"])

# Quickstart
# python -m get_gifs ./config/giphy.json
