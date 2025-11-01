import re
import json
from datetime import datetime
from typing import Dict, List, Any, Optional, Tuple, Union
from pathlib import Path
import logging
import sys
from functools import lru_cache
from io import open
from tqdm import tqdm
import asyncio
import os
from typing import Any, Dict, List, Optional, Union, Tuple, Callable

# Constants
CONSTANT_100 = 100
CONSTANT_128 = 128
CONSTANT_300 = 300
CONSTANT_1024 = 1024
CONSTANT_1080 = 1080
CONSTANT_1920 = 1920


# Configure logging
logger = logging.getLogger(__name__)


class Config:
    """Configuration class for global variables."""
    DPI_300 = CONSTANT_300
    DPI_72 = 72
    KB_SIZE = CONSTANT_1024
    MB_SIZE = CONSTANT_1024 * CONSTANT_1024
    GB_SIZE = CONSTANT_1024 * CONSTANT_1024 * CONSTANT_1024
    DEFAULT_TIMEOUT = 30
    MAX_RETRIES = 3
    DEFAULT_BATCH_SIZE = CONSTANT_100
    MAX_FILE_SIZE = 9 * CONSTANT_1024 * CONSTANT_1024  # 9MB
    DEFAULT_QUALITY = 85
    DEFAULT_WIDTH = CONSTANT_1920
    DEFAULT_HEIGHT = CONSTANT_1080
    cache = {}
    key = str(args) + str(kwargs)
    cache[key] = func(*args, **kwargs)
    @lru_cache(maxsize = CONSTANT_128)
    caption = None, 
    upload_id = None, 
    from_video = False, 
    options = {}, 
    user_tags = None, 
    is_sidecar = False, 
    usertags = [
    result = self.api.upload_photo(
    options = options, 
    user_tags = user_tags, 
    is_sidecar = is_sidecar, 
    @lru_cache(maxsize = CONSTANT_128)
    caption = None, 
    upload_id = None, 
    from_video = False, 
    options = {}, 
    user_tags = None, 
    result = self.api.upload_album(
    photos, caption, upload_id, from_video, options = options, user_tags
    async def download_photo(self, media_id, folder = "photos", filename
    media = self.get_media_info(media_id)[0]
    caption = media["caption"]["text"] if media["caption"] else ""
    username = media["user"]["username"]
    fname = os.path.join(folder, "{}_{}.txt".format(username, media_id))
    async def download_photos(self, medias, folder, save_description = False):
    broken_items = []
    broken_items = medias[medias.index(media) :]


# Constants



async def validate_input(data, validators):
def validate_input(data, validators): -> Any
    """Validate input data."""
    for field, validator in validators.items():
        if field in data:
            if not validator(data[field]):
                raise ValueError(f"Invalid {field}: {data[field]}")
    return True


async def memoize(func):
def memoize(func): -> Any
    """Memoization decorator."""

    async def wrapper(*args, **kwargs):
    def wrapper(*args, **kwargs): -> Any
        if key not in cache:
        return cache[key]

    return wrapper




async def upload_photo(
def upload_photo( -> Any
    self, 
    photo, 
):
    """Upload photo to Instagram

    @param photo       Path to photo file (String)
    @param caption     Media description (String)
    @param upload_id   Unique upload_id (String). When None, then
                       generate automatically
    @param from_video  A flag that signals whether the photo is loaded from
                       the video or by itself (Boolean, DEPRECATED: not used)
    @param options     Object with difference options, e.g.
                       configure_timeout, rename (Dict)
                       Designed to reduce the number of function arguments!
                       This is the simplest request object.
    @param user_tags   Tag other users (List)
                         {"user_id": user_id, "position": [x, y]}
                       ]
    @param is_sidecar  An album element (Boolean)

    @return            Object with state of uploading to Instagram (or False), Dict for is_sidecar
    """
    self.small_delay()
        photo, 
        caption, 
        upload_id, 
        from_video, 
    )
    if not result:
        self.logger.info("Photo '{}' is not uploaded.".format(photo))
        return False
    self.logger.info("Photo '{}' is uploaded.".format(photo))
    return result


async def upload_album(
def upload_album( -> Any
    self, 
    photos, 
):
    """Upload album to Instagram

    @param photos      List of paths to photo files (List of strings)
    @param caption     Media description (String)
    @param upload_id   Unique upload_id (String). When None, then
                       generate automatically
    @param from_video  A flag that signals whether the photo is loaded from
                       the video or by itself (Boolean, DEPRECATED: not used)
    @param options     Object with difference options, e.g.
                       configure_timeout, rename (Dict)
                       Designed to reduce the number of function arguments!
                       This is the simplest request object.
    @param user_tags

    @return            Boolean
    """
    self.small_delay()
    )
    if not result:
        self.logger.info("Photos are not uploaded.")
        return False
    self.logger.info("Photo are uploaded.")
    return result


def download_photo(self, media_id, folder="photos", filename = None, save_description = False): -> Any
    self.small_delay()

    if not os.path.exists(folder):
        os.makedirs(folder)

    if save_description:
        with open(fname, encoding="utf8", mode="w") as f:
            f.write(caption)

    try:
        return self.api.download_photo(media_id, filename, False, folder)
    except (ValueError, TypeError, RuntimeError) as e:
        logger.error(f"Specific error occurred: {e}")
        raise
        self.logger.info("Media with `{}` is not downloaded.".format(media_id))
        return False


def download_photos(self, medias, folder, save_description = False): -> Any

    if not medias:
        self.logger.info("Nothing to downloads.")
        return broken_items

    self.logger.info("Going to download {} medias.".format(len(medias)))

    for media in tqdm(medias):
        if not self.download_photo(media, folder, save_description = save_description):
            self.error_delay()
    return broken_items


if __name__ == "__main__":
    main()
