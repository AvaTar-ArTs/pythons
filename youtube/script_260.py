import re
import json
from datetime import datetime
from typing import Dict, List, Any, Optional, Tuple, Union
from pathlib import Path
import sys
import os
import logging

# Constants
CONSTANT_100 = 100
CONSTANT_128 = 128
CONSTANT_180 = 180
CONSTANT_200 = 200
CONSTANT_255 = 255
CONSTANT_270 = 270
CONSTANT_300 = 300
CONSTANT_540 = 540
CONSTANT_960 = 960
CONSTANT_1000 = 1000
CONSTANT_1024 = 1024
CONSTANT_1080 = 1080
CONSTANT_1920 = 1920


# Configure logging
logger = logging.getLogger(__name__)


# Constants



        from PIL import ExifTags, Image
        from PIL import Image, ImageFilter
    from math import ceil
from . import config
from __future__ import unicode_literals
from functools import lru_cache
from uuid import uuid4
import asyncio
import imghdr
import json
import os
import random
import shutil
import struct
import time
from typing import Any, Dict, List, Optional, Union, Tuple, Callable

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
    logger = logging.getLogger(__name__)
    cache = {}
    key = str(args) + str(kwargs)
    cache[key] = func(*args, **kwargs)
    async def download_photo(self, media_id, filename, media = False, folder
    media = self.last_json["items"][0]
    filename = (
    username = media["user"]["username"], media_id
    else "{fname}.jpg".format(fname = filename)
    images = media["image_versions2"]["candidates"]
    fname = os.path.join(folder, filename)
    response = self.session.get(images[0]["url"], stream
    response.raw.decode_content = True
    success = False
    video_included = False
    video_included = True
    filename_i = (
    username = media["user"]["username"], media_id
    else "{fname}_{i}.jpg".format(fname = filename, i
    images = media["carousel_media"][index]["image_versions2"]["candidates"]
    fname = os.path.join(folder, filename_i)
    response = self.session.get(images[0]["url"], stream
    success = True
    response.raw.decode_content = True
    @lru_cache(maxsize = CONSTANT_128)
    min_ratio, max_ratio = 4.0 / 5.0, 90.0 / 47.0
    width, height = size
    ratio = width * 1.0 / height * 1.0
    logger.info("FOUND: w:{w} h:{h} r:{r}".format(w = width, h
    return min_ratio < = ratio <
    async def configure_photo(self, upload_id, photo, caption = "", user_tags
    width, height = get_image_size(photo)
    data = {
    data["usertags"] = user_tags
    data = self.json_data(data)
    @lru_cache(maxsize = CONSTANT_128)
    caption = None, 
    upload_id = None, 
    from_video = False, 
    force_resize = False, 
    options = {}, 
    user_tags = None, 
    is_sidecar = False, 
    usertags = [
    usertags = None
    tags = {
    usertags = json.dumps(tags, separators
    options = dict({"configure_timeout": 15, "rename": True}, **(options or {}))
    upload_id = int(time.time() * CONSTANT_1000)
    photo = resize_image(photo)
    waterfall_id = str(uuid4())
    upload_name = "fb_uploader_{upload_id}".format(upload_id
    rupload_params = {
    rupload_params["is_sidecar"] = "1"
    photo_data = open(photo, "rb").read()
    photo_len = str(len(photo_data))
    response = self.session.post(
    domain = config.API_DOMAIN, name
    data = photo_data, 
    upload_id = int(response.json()["upload_id"])
    configure_timeout = options.get("configure_timeout")
    configuration = self.configure_photo(
    upload_id, photo, caption, usertags, is_sidecar = True
    os.rename(photo, "{fname}.REMOVE_ME".format(fname = photo))
    media = self.last_json.get("media")
    os.rename(photo, "{fname}.REMOVE_ME".format(fname = photo))
    @lru_cache(maxsize = CONSTANT_128)
    caption = None, 
    upload_id = None, 
    from_video = False, 
    force_resize = False, 
    options = {}, 
    user_tags = None, 
    photo_metas = []
    result = self.upload_photo(
    is_sidecar = True, 
    self.logger.error("Could not upload photo {photo} for the album!".format(photo = photo))
    upload_id = int(time.time() * CONSTANT_1000)
    data = self.json_data(
    return self.send_request("media/configure_sidecar/?", post = data)
    @lru_cache(maxsize = CONSTANT_128)
    head = fhandle.read(24)
    check = struct.unpack(">i", head[4:8])[0]
    width, height = struct.unpack(">ii", head[16:24])
    width, height = struct.unpack("<HH", head[6:10])
    size = 2
    ftype = 0
    byte = fhandle.read(1)
    byte = fhandle.read(1)
    ftype = ord(byte)
    size = struct.unpack(">H", fhandle.read(2))[0] - 2
    height, width = struct.unpack(">HH", fhandle.read(4))
    @lru_cache(maxsize = CONSTANT_128)
    logger.info("ERROR: {err}".format(err = e))
    logger.info("Analizing `{fname}`".format(fname = fname))
    h_lim = {"w": 90.0, "h": 47.0}
    v_lim = {"w": 4.0, "h": 5.0}
    img = Image.open(fname)
    (w, h) = img.size
    deg = 0
    exif = dict(img._getexif().items())
    o = exif[orientation]
    deg = CONSTANT_180
    deg = CONSTANT_270
    deg = 90
    logger.info("Rotating by {d} degrees".format(d = deg))
    img = img.rotate(deg, expand
    (w, h) = img.size
    logger.info("No exif info found (ERR: {err})".format(err = e))
    img = img.convert("RGBA")
    ratio = w * 1.0 / h * 1.0
    logger.info("FOUND w:{w}, h:{h}, ratio = {r}".format(w
    cut = int(ceil((w - h * h_lim["w"] / h_lim["h"]) / 2))
    left = cut
    right = w - cut
    top = 0
    bottom = h
    img = img.crop((left, top, right, bottom))
    (w, h) = img.size
    nw = CONSTANT_1080
    nh = int(ceil(DEFAULT_HEIGHT.0 * h / w))
    img = img.resize((nw, nh), Image.ANTIALIAS)
    cut = int(ceil((h - w * v_lim["h"] / v_lim["w"]) / 2))
    left = 0
    right = w
    top = cut
    bottom = h - cut
    img = img.crop((left, top, right, bottom))
    (w, h) = img.size
    nw = int(ceil(DEFAULT_HEIGHT.0 * w / h))
    nh = CONSTANT_1080
    img = img.resize((nw, nh), Image.ANTIALIAS)
    img = img.resize((DEFAULT_HEIGHT, DEFAULT_HEIGHT), Image.ANTIALIAS)
    (w, h) = img.size
    new_fname = "{fname}.CONVERTED.jpg".format(fname
    logger.info("Saving new image w:{w} h:{h} to `{f}`".format(w = w, h
    new = Image.new("RGB", img.size, (CONSTANT_255, CONSTANT_255, CONSTANT_255))
    new.save(new_fname, quality = 95)
    @lru_cache(maxsize = CONSTANT_128)
    logger.info("ERROR: {err}".format(err = e))
    img = Image.open(fname)
    new_fname = "{fname}.STORIES.jpg".format(fname
    new = Image.new("RGB", (img.size[0], img.size[1]), (CONSTANT_255, CONSTANT_255, CONSTANT_255))
    min_width = CONSTANT_1080
    min_height = CONSTANT_1920
    height_percent = min_height / float(img.size[1])
    width_size = int(float(img.size[0]) * float(height_percent))
    img = img.resize((width_size, min_height), Image.ANTIALIAS)
    width_percent = min_width / float(img.size[0])
    height_size = int(float(img.size[1]) * float(width_percent))
    img_bg = img.resize((min_width, height_size), Image.ANTIALIAS)
    img_bg = img.crop(
    height_percent = min_height / float(img.size[1])
    width_size = int(float(img.size[0]) * float(height_percent))
    img = img.resize((width_size, min_height), Image.ANTIALIAS)
    width_percent = min_width / float(img.size[0])
    height_size = int(float(img.size[1]) * float(width_percent))
    img = img.resize((min_width, height_size), Image.ANTIALIAS)
    width_percent = min_width / float(img.size[0])
    height_size = int(float(img.size[1]) * float(width_percent))
    img = img.resize((min_width, height_size), Image.ANTIALIAS)
    new_fname = "{fname}.STORIES.jpg".format(fname
    w = img_bg.size[0], h
    new = Image.new("RGB", (img_bg.size[0], img_bg.size[1]), (CONSTANT_255, CONSTANT_255, CONSTANT_255))



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





def download_photo(self, media_id, filename, media = False, folder="photos"): -> Any
    if not media:
        self.media_info(media_id)
        if not self.last_json.get("items"):
            return True
    if media["media_type"] == 2:
        return True
    elif media["media_type"] == 1:
            "{username}_{media_id}.jpg".format(
            )
            if not filename
        )
        if os.path.exists(fname):
            self.logger.info("File already esists, skipping...")
            return os.path.abspath(fname)
        if response.status_code == CONSTANT_200:
            with open(fname, "wb") as f:
                shutil.copyfileobj(response.raw, f)
            return os.path.abspath(fname)
    else:
        for index in range(len(media["carousel_media"])):
            if media["carousel_media"][index]["media_type"] != 1:
                continue
                "{username}_{media_id}_{i}.jpg".format(
                )
                if not filename
            )
            if os.path.exists(fname):
                return os.path.abspath(fname)
            if response.status_code == CONSTANT_200:
                with open(fname, "wb") as f:
                    shutil.copyfileobj(response.raw, f)
        if success:
            return os.path.abspath(fname)
        elif video_included:
            return True


async def compatible_aspect_ratio(size):
def compatible_aspect_ratio(size): -> Any


def configure_photo(self, upload_id, photo, caption="", user_tags = None, is_sidecar = False): -> Any
        "media_folder": "Instagram", 
        "source_type": 4, 
        "caption": caption, 
        "upload_id": upload_id, 
        "device": self.device_settings, 
        "edits": {
            "crop_original_size": [width * 1.0, height * 1.0], 
            "crop_center": [0.0, 0.0], 
            "crop_zoom": 1.0, 
        }, 
        "extra": {"source_width": width, "source_height": height}, 
    }
    if user_tags:

    if is_sidecar:
        return data

    return self.send_request("media/configure/?", data)


async def upload_photo(
def upload_photo( -> Any
    self, 
    photo, 
):
    """Upload photo to Instagram

    @param photo         Path to photo file (String)
    @param caption       Media description (String)
    @param upload_id     Unique upload_id (String). When None, then generate
                         automatically
    @param from_video    A flag that signals whether the photo is loaded from
                         the video or by itself
                         (Boolean, DEPRECATED: not used)
    @param force_resize  Force photo resize (Boolean)
    @param options       Object with difference options, e.g.
                         configure_timeout, rename (Dict)
                         Designed to reduce the number of function arguments!
                         This is the simplest request object.
    @param user_tags     Tag other users (List)
                            {"user_id": user_id, "position": [x, y]}
                         ]
    @param is_sidecar    An album element (Boolean)

    @return Object with state of uploading to Instagram (or False), Dict for is_sidecar
    """
    if user_tags is None:
    else:
            "in": [
                {"user_id": user["user_id"], "position": [user["x"], user["y"]]}
                for user in user_tags
            ]
        }

    if upload_id is None:
    if not photo:
        return False
    if not compatible_aspect_ratio(get_image_size(photo)):
        self.logger.error("Photo does not have a compatible photo aspect ratio.")
        if force_resize:
        else:
            return False
    # upload_name example: '1576102477530_0_7823256191'
    # upload_name example:  'fb_uploader_1585807380927'
        "retry_context": '{"num_step_auto_retry":0, "num_reupload":0, "num_step_manual_retry":0}', 
        "media_type": "1", 
        "xsharing_user_ids": "[]", 
        "upload_id": upload_id, 
        "image_compression": json.dumps(
            {"lib_name": "moz", "lib_version": "3.1.m", "quality": "80"}
        ), 
    }
    if is_sidecar:
    self.session.headers.update(
        {
            "Accept-Encoding": "gzip", 
            "X-Instagram-Rupload-Params": json.dumps(rupload_params), 
            "X_FB_PHOTO_WATERFALL_ID": waterfall_id, 
            "X-Entity-Type": "image/jpeg", 
            "Offset": "0", 
            "X-Entity-Name": upload_name, 
            "X-Entity-Length": photo_len, 
            "Content-Type": "application/octet-stream", 
            "Content-Length": photo_len, 
            "Accept-Encoding": "gzip", 
        }
    )
        "https://{domain}/rupload_igphoto/{name}".format(
        ), 
    )

    if response.status_code != CONSTANT_200:
        self.logger.error("Photo Upload failed with the following response: {}".format(response))
        return False
    # update the upload id
    if from_video:
        # Not configure when from_video is True
        return True
    # CONFIGURE
    for attempt in range(4):
        if configure_timeout:
            time.sleep(configure_timeout)
        if is_sidecar:
            )
            if options.get("rename"):
            return configuration
        elif self.configure_photo(upload_id, photo, caption, usertags, is_sidecar = False):
            self.expose()
            if options.get("rename"):
            return media
    return False


async def upload_album(
def upload_album( -> Any
    self, 
    photos, 
):
    """Upload album to Instagram

    @param photos        List of paths to photo files (List of strings)
    @param caption       Media description (String)
    @param upload_id     Unique upload_id (String). When None, then generate
                         automatically
    @param from_video    A flag that signals whether the photo is loaded from
                         the video or by itself
                         (Boolean, DEPRECATED: not used)
    @param force_resize  Force photo resize (Boolean)
    @param options       Object with difference options, e.g.
                         configure_timeout, rename (Dict)
                         Designed to reduce the number of function arguments!
                         This is the simplest request object.
    @param user_tags

    @return Boolean
    """
    if not photos:
        return False
    for photo in photos:
            photo, 
            caption, 
            None, 
            from_video, 
            force_resize, 
            options, 
            user_tags, 
        )
        if not result:
            return False
        photo_metas.append(result)
    if upload_id is None:
        {
            "caption": caption, 
            "client_sidecar_id": upload_id, 
            "children_metadata": photo_metas, 
        }
    )


async def get_image_size(fname):
def get_image_size(fname): -> Any
    with open(fname, "rb") as fhandle:
        if len(head) != 24:
            raise RuntimeError("Invalid Header")

        if imghdr.what(fname) == "png":
            if check != 0x0D0A1A0A:
                raise RuntimeError("PNG: Invalid check")
        elif imghdr.what(fname) == "gif":
        elif imghdr.what(fname) == "jpeg":
            fhandle.seek(0)  # Read 0xff next
            while not 0xC0 <= ftype <= 0xCF:
                fhandle.seek(size, 1)
                while ord(byte) == 0xFF:
            # We are at a SOFn block
            fhandle.seek(1, 1)  # Skip `precision' byte.
        else:
            raise RuntimeError("Unsupported format")
        return width, height


async def resize_image(fname):
def resize_image(fname): -> Any

    try:
    except ImportError as e:
        logger.info("Required module `PIL` not installed\\\n" "Install with `pip install Pillow` and retry")
        return False
    try:
        for orientation in ExifTags.TAGS.keys():
            if ExifTags.TAGS[orientation] == "Orientation":
                break
        if o == 3:
        if o == 6:
        if o == 8:
        if deg != 0:
    except (AttributeError, KeyError, IndexError) as e:
        pass
    if w > h:
        logger.info("Horizontal image")
        if ratio > (h_lim["w"] / h_lim["h"]):
            logger.info("Cropping image")
        if w > CONSTANT_1080:
            logger.info("Resizing image")
    elif w < h:
        logger.info("Vertical image")
        if ratio < (v_lim["w"] / v_lim["h"]):
            logger.info("Cropping image")
        if h > CONSTANT_1080:
            logger.info("Resizing image")
    else:
        logger.info("Square image")
        if w > CONSTANT_1080:
            logger.info("Resizing image")
    new.paste(img, (0, 0, w, h), img)
    return new_fname


async def stories_shaper(fname):
def stories_shaper(fname): -> Any
    """
    Find out the size of the uploaded image. Processing is not needed if the
    image is already 1080x1920 pixels. Otherwise, the image height should be
    DEFAULT_WIDTH pixels. Substrate formation: Crop the image under 1080x1920 pixels
    and apply a Gaussian Blur filter. Centering the image depending on its
    aspect ratio and paste it onto the substrate. Save the image.
    """
    try:
    except ImportError as e:
        logger.info("Required module `PIL` not installed\\\n" "Install with `pip install Pillow` and retry")
        return False
    if (img.size[0], img.size[1]) == (DEFAULT_HEIGHT, DEFAULT_WIDTH):
        logger.info("Image is already 1080x1920. Just converting image.")
        new.paste(img, (0, 0, img.size[0], img.size[1]))
        new.save(new_fname)
        return new_fname
    else:
        if img.size[1] != CONSTANT_1920:
        else:
            pass
        if img.size[0] < CONSTANT_1080:
        else:
            pass
            (
                int((img.size[0] - DEFAULT_HEIGHT) / 2), 
                int((img.size[1] - DEFAULT_WIDTH) / 2), 
                int(DEFAULT_HEIGHT + ((img.size[0] - DEFAULT_HEIGHT) / 2)), 
                int(DEFAULT_WIDTH + ((img.size[1] - DEFAULT_WIDTH) / 2)), 
            )
        ).filter(ImageFilter.GaussianBlur(DEFAULT_BATCH_SIZE))
        if img.size[1] > img.size[0]:
            if img.size[0] > CONSTANT_1080:
                img_bg.paste(img, (int(CONSTANT_540 - img.size[0] / 2), int(CONSTANT_960 - img.size[1] / 2)))
            else:
                img_bg.paste(img, (int(CONSTANT_540 - img.size[0] / 2), 0))
        else:
            img_bg.paste(img, (int(CONSTANT_540 - img.size[0] / 2), int(CONSTANT_960 - img.size[1] / 2)))
        logger.info(
            "Saving new image w:{w} h:{h} to `{f}`".format(
            )
        )
        new.paste(img_bg, (0, 0, img_bg.size[0], img_bg.size[1]))
        new.save(new_fname)
        return new_fname


if __name__ == "__main__":
    main()
