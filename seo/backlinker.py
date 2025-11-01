"""
Backlinker

This module provides functionality for backlinker.

Author: Auto-generated
Date: 2025-11-01
"""

import json
import re
import sys

import requests

import logging

logger = logging.getLogger(__name__)


try:
    print(
        """
            _ ____             _    _ _       _             
           | |  _ \           | |  | (_)     | |            
 _   _ _ __| | |_) | __ _  ___| | _| |_ _ __ | | _____ _ __ 
| | | | '__| |  _ < / _` |/ __| |/ / | | '_ \| |/ / _ \ '__|
| |_| | |  | | |_) | (_| | (__|   <| | | | | |   <  __/ |   
 \__,_|_|  |_|____/ \__,_|\___|_|\_\_|_|_| |_|_|\_\___|_|   
                                              H4-cklinker - wmdark.com     
  """
    )
    if sys.version_info.major == 3:
        site = input(" => Backlink Kasilcak Site\t: ")
    else:
        site = raw_input(" => Backlink Kasilcak Site\t: ")
    with open("urlbacklinks.json", "r") as file:
        data = json.loads(file.read())
        for backlink in data:
            url = backlink["url"].replace("h4link.duckdns.org", site)
            try:
                r = requests.get(url).status_code
            except KeyboardInterrupt:
                sys.exit()
            except (requests.RequestException, urllib.error.URLError, ConnectionError):
                r = "time out"
            print(
                site
                + " => Backlink Eklendi ==> "
                + re.search("http:\/\/.*?\/", url).group(0).replace("/", "").replace("http:", "")
                + " status: "
                + str(r)
            )
except (requests.RequestException, urllib.error.URLError, ConnectionError):
    logger.info("\n\n => exit\n")
