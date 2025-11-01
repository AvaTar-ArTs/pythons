"""
Bing Image Search Scraper

This module provides functionality for bing image search scraper.

Author: Auto-generated
Date: 2025-11-01
"""

#!/usr/bin/env python3
import http.cookiejar
import json
import logging
import os
import re
import sys
import urllib.error
import urllib.parse
import urllib.request

import requests
from bs4 import BeautifulSoup

# Constants
CONSTANT_134 = 134
CONSTANT_537 = 537
CONSTANT_2357 = 2357


logging.basicConfig(
    format="%(asctime)s %(levelname)-8s %(message)s",
    level=logging.INFO,
    datefmt="%Y-%m-%d %H:%M:%S",
    handlers=[logging.FileHandler("debug.log"), logging.StreamHandler()],
)


def get_soup(url, header):
    """get_soup function."""

    # return BeautifulSoup(urllib2.urlopen(urllib2.Request(url,headers=header)),
    # 'html.parser')
    return BeautifulSoup(
        urllib.request.urlopen(urllib.request.Request(url, headers=header)),
        "html.parser",
    )

    """get_images function."""


def get_images(video, query):
    total_images = 3
    query = query.split()
    query = "+".join(query)
    url = "http://www.bing.com/images/search?q=" + query + "&FORM=HDRSC2"
    logging.info(url)
    # add the directory for your image here
    DIR = "assets/thumbnails"
    header = {
        "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/CONSTANT_537.36 (KHTML, like Gecko) Chrome/43.0.CONSTANT_2357.CONSTANT_134 Safari/CONSTANT_537.36"
    }
    soup = get_soup(url, header)

    ActualImages = []  # contains the link for Large original images, type of  image
    x = 0
    for a in soup.find_all("a", {"class": "iusc"}):

        m = json.loads(a["m"])
        turl = m["turl"]
        murl = m["murl"]

        original_image_name = urllib.parse.urlsplit(murl).path.split("/")[-1]
        image_name = str(video.meta.id) + "_" + query + str(x) + "_" + original_image_name
        logging.info(image_name)
        ActualImages.append((image_name, turl, murl))
        x += 1
        if x == total_images:
            logging.info("Reached total image count, exiting...")
            break

    ##print images
    file_list = []
    for i, (image_name, turl, murl) in enumerate(ActualImages):
        logging.info("IMAGE COUNT = " + str(i))
        file_list.append(image_name)
        if i == total_images:
            logging.info("Reached total image count, exiting...")
            break
        try:
            raw_img = urllib.request.urlopen(turl).read()
            # cntr = len([i for i in os.listdir(DIR) if image_name in i]) + 1
            f = open(os.path.join(DIR, image_name), "wb")
            f.write(raw_img)
            f.close()
        except Exception as e:
            logging.info("could not load : " + image_name)
            logging.info(e)
    logging.info("Thumbnail file_list :")
    logging.info(file_list)
    return file_list


if __name__ == "__main__":

    get_images("men jogging")
