"""
Web Scraping Download Scrape 6

This module provides functionality for web scraping download scrape 6.

Author: Auto-generated
Date: 2025-11-01
"""

from pathlib import Path
import requests
from bs4 import BeautifulSoup

url = requests.get("https://redditmetrics.com/top")

soup = BeautifulSoup(url.text, "html.parser")


with open("sb.txt", "w") as f:
    for subreddit in soup.find_all("a"):
        try:
            if Path("/r") in subreddit.string:
                f.write(subreddit.string[3:] + Path("\n"))
        except (OSError, IOError, FileNotFoundError):
            TypeError
