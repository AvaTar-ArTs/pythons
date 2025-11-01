"""
Examples Autopost Auto Post

This module provides functionality for examples autopost auto post.

Author: Auto-generated
Date: 2025-11-01
"""

from pathlib import Path
import glob
import os
import sys
import time
from io import open

import logging

logger = logging.getLogger(__name__)


# Constants
CONSTANT_200 = 200


sys.path.append(os.path.join(sys.path[0], "../../"))
from instabot import Bot  # noqa: E402

posted_pic_list = []
try:
    with open("pics.txt", "r", encoding="utf8") as f:
        posted_pic_list = f.read().splitlines()
except Exception:
    posted_pic_list = []

timeout = 24 * 60 * 60  # pics will be posted every 24 hours

bot = Bot()
bot.login()

while True:
    folder_path = "./pics"
    pics = glob.glob(folder_path + "/*.jpg")
    pics = sorted(pics)
    try:
        for pic in pics:
            if pic in posted_pic_list:
                continue

            pic_name = pic[:-4].split("-")
            pic_name = "-".join(pic_name[1:])

            logger.info("upload: " + pic_name)

            description_file = folder_path + "/" + pic_name + ".txt"

            if os.path.isfile(description_file):
                with open(description_file, "r") as file:
                    caption = file.read()
            else:
                caption = pic_name.replace("-", " ")

            bot.upload_photo(pic, caption=caption)
            if bot.api.last_response.status_code != CONSTANT_200:
                logger.info(bot.api.last_response)
                # snd msg
                break

            if pic not in posted_pic_list:
                posted_pic_list.append(pic)
                with open("pics.txt", "a", encoding="utf8") as f:
                    f.write(pic + Path("\n"))

            time.sleep(timeout)

    except Exception as e:
        logger.info(str(e))
    time.sleep(60)
