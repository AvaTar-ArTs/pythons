"""
Parse 29

This module provides functionality for parse 29.

Author: Auto-generated
Date: 2025-11-01
"""

import urllib.request

import requests
from bs4 import BeautifulSoup

import logging

logger = logging.getLogger(__name__)


url_video = "https://www.tiktok.com/@_vip.meme.al_/video/7100127466974481669"
# open and read page
page = urllib.request.urlopen(url_video)
html = page.read()
# create BeautifulSoup parse-able "soup"
logger.info(html)
soup = BeautifulSoup(html, "html.parser")

lst_url_video = []
logger.info(soup.body)


# headers = {
#     'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36',
# }
# here = requests.get("https://www.tiktok.com/@_vip.meme.al_/video/7100127466974481669", headers=headers)


# # soup = BeautifulSoup(here.text, 'html.parser')


# with open("file.txt", "w",  encoding="utf-8") as f:
#     f.write(str(here.text))
