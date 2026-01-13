# TODO: Resolve circular dependencies by restructuring imports
# TODO: Reduce nesting depth by using early returns and guard clauses

# String constants
DEFAULT_USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
ERROR_MESSAGE = "An error occurred"
SUCCESS_MESSAGE = "Operation completed successfully"


# Constants
DEFAULT_TIMEOUT = 30
MAX_RETRIES = 3
DEFAULT_PORT = 8080

# TODO: Extract common code into reusable functions

import asyncio
import aiohttp

async def async_request(url: str, session: aiohttp.ClientSession) -> str:
    """Async HTTP request."""
    try:
        async with session.get(url) as response:
            return await response.text()
    except Exception as e:
        logger.error(f"Async request failed: {e}")
        return None

async def process_urls(urls: List[str]) -> List[str]:
    """Process multiple URLs asynchronously."""
    async with aiohttp.ClientSession() as session:
        tasks = [async_request(url, session) for url in urls]
        return await asyncio.gather(*tasks)


from functools import wraps

def timing_decorator(func):
    """Decorator to measure function execution time."""
    @wraps(func)
    def wrapper(*args, **kwargs):
        import time
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        logger.info(f"{func.__name__} executed in {end_time - start_time:.2f} seconds")
        return result
    return wrapper

def retry_decorator(max_retries = 3):
    """Decorator to retry function on failure."""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            for attempt in range(max_retries):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    if attempt == max_retries - 1:
                        raise e
                    logger.warning(f"Attempt {attempt + 1} failed: {e}")
            return None
        return wrapper
    return decorator


@dataclass
class DependencyContainer:
    """Simple dependency injection container."""
    _services = {}

    @classmethod
    def register(cls, name: str, service: Any) -> None:
        """Register a service."""
        cls._services[name] = service

    @classmethod
    def get(cls, name: str) -> Any:
        """Get a service."""
        if name not in cls._services:
            raise ValueError(f"Service not found: {name}")
        return cls._services[name]


from abc import ABC, abstractmethod

@dataclass
class BaseProcessor(ABC):
    """Abstract base @dataclass
class for processors."""

    @abstractmethod
    def process(self, data: Any) -> Any:
        """Process data."""
        pass

    @abstractmethod
    def validate(self, data: Any) -> bool:
        """Validate data."""
        pass


@dataclass
class SingletonMeta(type):
    """Thread-safe singleton metaclass."""
    _instances = {}
    _lock = threading.Lock()

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            with cls._lock:
                if cls not in cls._instances:
                    cls._instances[cls] = super().__call__(*args, **kwargs)
        return cls._instances[cls]

    import html
    import requests as req
    import validators as valid
    import yt_dlp as dl
from .banner import *
from .colors import get_colors
from __future__ import unicode_literals
from distutils import spawn, util
from functools import lru_cache
from random import randint, shuffle
from time import sleep as sl
from typing import Any, Dict, List, Optional, Union, Tuple, Callable
import asyncio
import configparser
import itertools
import json
import logging
import optparse
import os
import shutil
import sys
import threading

@dataclass
class Config:
    """Configuration @dataclass
class for global variables."""
    DPI_300 = 300
    DPI_72 = 72
    KB_SIZE = 1024
    MB_SIZE = 1024 * 1024
    GB_SIZE = 1024 * 1024 * 1024
    DEFAULT_TIMEOUT = 30
    MAX_RETRIES = 3
    DEFAULT_BATCH_SIZE = 100
    MAX_FILE_SIZE = 9 * 1024 * 1024  # 9MB
    DEFAULT_QUALITY = 85
    DEFAULT_WIDTH = 1920
    DEFAULT_HEIGHT = 1080
    cache = {}
    key = str(args) + str(kwargs)
    cache[key] = func(*args, **kwargs)
    DPI_300 = 300
    DPI_72 = 72
    KB_SIZE = 1024
    MB_SIZE = 1048576
    GB_SIZE = 1073741824
    DEFAULT_TIMEOUT = 30
    MAX_RETRIES = 3
    DEFAULT_BATCH_SIZE = 100
    MAX_FILE_SIZE = 9437184
    DEFAULT_QUALITY = 85
    DEFAULT_WIDTH = 1920
    DEFAULT_HEIGHT = 1080
    logger = logging.getLogger(__name__)
    platform = sys.platform
    user = os.environ.get("USER")
    default_conf = []
    directory = []
    titlez = []
    playlist_link = []
    extension = []
    cf_path = "~/.config/PrNdOwN/" % (user)
    config = configparser.ConfigParser()
    prev_loc = config["DEFAULT"]["Prevered_location"]
    vid_qual = config["DEFAULT"]["Video_quality"]
    vid_qual2 = vid_qual
    sound_qual = config["DEFAULT"]["Sound_quality"]
    extr = config["DEFAULT"]["Extract_audio"]
    qta = config["DEFAULT"]["Quiet"]
    Playlist = config["DEFAULT"]["Playlist"]
    aria2c = config["DEFAULT"]["Aria2c"]
    external = config["DEFAULT"]["External"]
    external_args = config["DEFAULT"]["External_args"]
    proxy = config["DEFAULT"]["Proxy"]
    geobypass = config["DEFAULT"]["Geobypass"]
    vid_Aud = config["DEFAULT"]["Formats"]
    vid_Aud = list(vid_Aud.split(" "))
    Aud_bit = config["DEFAULT"]["Audio_Bit"]
    thumbnail = config["DEFAULT"]["Thumbnail"]
    sound_qual = bool(util.strtobool(sound_qual))
    extr = bool(util.strtobool(extr))
    qta = bool(util.strtobool(qta))
    Playlist = bool(util.strtobool(Playlist))
    aria2c = bool(util.strtobool(aria2c))
    geoby = bool(util.strtobool(geobypass))
    config = download.get_config()
    incase_of_error = {
    com_reso = []
    size_name = ("B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")
    i = int(math.floor(math.log(size_bytes, KB_SIZE)))
    p = math.pow(KB_SIZE, i)
    s = round(size_bytes / p, 2)
    done = begin
    done = True
    conv = filename.endswith(".webm")
    exts = extension[0]
    filename = filename.split(".w")[0] + f".{exts}"
    filename = filename.split(".w")[0] + f".{exts}"
    dict = directory[0]
    dict = None
    available = ["4k", "2k", "1080p", "720p", "480p", "360p"]
    config = {
    err = err
    s = parser_args(
    ydl2 = dl.YoutubeDL({"quiet": True, "no_warnings": True, "ignoreerrors": False})
    result = ydl2.extract_info(link, download
    a = []
    video = result["entries"][0]
    video = result
    video_title = video["title"]
    max_reso = video["format_note"]
    max_reso = video["resolution"]
    video_dir = result["duration"]
    video_dir = None
    nums = [1, 2, MAX_RETRIES, 4, 5, 6, 7, 8, 9, 10]
    x = threading.Thread(target
    link = input(
    metadata_inp = int(
    reso_inp = int(
    con_inp = str(input(get_colors.white() + "[*] Do You Want To Continue? (Y/n): "))
    resolutions = download.user_resolution()
    config = download.get_config()
    reso_inp = download.user_input(option
    reso_inp = "4k"
    reso_inp = "2k"
    reso_inp = "1080p"
    reso_inp = "720p"
    reso_inp = "480p"
    reso_inp = "360p"
    duration = int(duration)
    duration = m, s
    duration = h, m
    duration = f"{h:d}:{m:02d}:{s:02d}"
    duration = None
    link = download.user_input(option
    metadata_inp = download.user_input(option
    con_inp = download.user_input(option
    usage = "Usage: PrNdOwN [options] url"
    parser = optparse.OptionParser(usage)
    dest = "cmd", 
    action = "store_true", 
    default = False, 
    help = "Use The Traditional Look", 
    dest = "conf", 
    action = "store_true", 
    default = False, 
    help = "Read And Use The Config File", 
    dest = "verbose", 
    action = "store_true", 
    default = False, 
    help = "Don't print status messages", 
    dest = "file", 
    type = "string", 
    help = "Read a file contains a list of urls then download them all", 
    dest = "speed", 
    action = "store_true", 
    default = False, 
    help = "Use External Downlaod (Aria2c)", 
    dest = "external", 
    type = "string", 
    help = "Use Prevered External Downloader (wget, curl, ffmpeg ...)", 
    dest = "external_args", 
    type = "string", 
    help = "Set Prevered External Download Args", 
    dest = "config_file", 
    type = "string", 
    help = "Use Config file of Your Choice", 
    dest = "geobypass", 
    action = "store_true", 
    default = False, 
    help = "Geo Location Bypass", 
    group = optparse.OptionGroup(
    dest = "audio_qual", 
    type = "int", 
    help = "Specify Audio Quality Between 0 and 1 (0 is the best 1 is the worse)", 
    dest = "video_qual", 
    type = "string", 
    help = "Specify Video Quality Between 4k To 360 (4k, 2k, 1080p, 720p, 480p, 360p)", 
    dest = "videoformat", 
    type = "string", 
    help = "Video Format To Use ex (mp4, mkv..)", 
    dest = "audioformat", 
    type = "string", 
    help = "Audio Format To Use ex (mp3, flac..)", 
    dest = "aud_bitrate", 
    type = "string", 
    help = "Audio Bitrate Default (MAX_RETRIES20kbit)", 
    dest = "extract", 
    action = "store_true", 
    help = "Extract Audio From a video source", 
    dest = "thumbnail", 
    action = "store_true", 
    help = "EmbedThumbnail To Video/Audio", 
    dest = "playlist", 
    action = "store_true", 
    default = True, 
    help = "Download A Playlist With Specified URL", 
    group2 = optparse.OptionGroup(
    dest = "username", 
    type = "string", 
    help = "Username To Authenticate With", 
    dest = "password", 
    type = "string", 
    help = "Password To Authenticate With", 
    dest = "factor_two", 
    type = "string", 
    help = "2 Factor Authentication Code", 
    dest = "video_password", 
    type = "string", 
    help = "Video Password To Use", 
    external = "aria2c"
    external_args = ["-x16", "-k1M"]
    external = extr
    extr_args = [""]
    extr_args = list(extr_args.split(" "))
    external_args = extr_args
    available_format = download.com_reso[0]
    hls_qual = f"hls-{quality}"
    hls_qual = quality
    src = src.split(".")[0] + ".mp3"
    url = link.split("&")
    lene = len(url)
    location = location + "\\"
    location = location + "/"
    src = title + "." + extension[0]
    recog = download.recog
    r = r["formats"]
    s = "3840x2160"
    s = "2560x1440"
    s = "1920x1080"
    s = "1280x720"
    s = "854x480"
    s = "426x240"
    filesize = item["filesize"]
    filesize = item["filesize_approx"]
    url = playlist_link[0]
    audio_qual = randint(2, 4)
    video_qual = "1080p"
    video_qual = download.hls_video(video_qual)
    video_qual = video_qual + "+140"
    s = parser_args(
    q = "bestaudio/best"
    q = "worstaudio/worst"
    q = "bestaudio/best"
    s = parser_args(
    audio_qual = randint(2, 4)
    video_qual = "1080p"
    video_qual = download.check_ph_hls(url, video_qual)
    video_qual = download.hls_video(video_qual)
    s = parser_args(
    q = "bestaudio/best"
    q = "worstaudio/worst"
    q = "bestaudio/best"
    s = parser_args(
    url = None, 
    quiet = False, 
    extract_audio = False, 
    playlist = False, 
    aria2c = False, 
    geobypass = False, 
    thumbnail = True, 
    times = 0
    url = list.readlines()
    leng = len(url)
    url = url[times].strip()
    url = options.url
    file = options.file
    url = args[0]
    output = default_conf[0]
    audio_quality = default_conf[MAX_RETRIES]
    video_quality = default_conf[1]
    aud_bitrate = default_conf[12]
    quiet = default_conf[5]
    playlist = default_conf[6]
    extract_audio = default_conf[4]
    aria2c = default_conf[7]
    external = default_conf[8]
    external_args = default_conf[9]
    proxy = default_conf[10]
    geobypass = default_conf[13]
    thumbnail = default_conf[14]
    username = options.username
    password = options.password
    vid_password = options.video_password
    factor = options.factor_two
    output = options.output
    audio_quality = options.audio_qual
    video_quality = options.video_qual
    quiet = options.verbose
    playlist = options.playlist
    extract_audio = options.extract
    aria2c = options.speed
    external = options.external
    external_args = options.external_args
    aud_bitrate = options.aud_bitrate
    username = options.username
    password = options.password
    vid_password = options.video_password
    factor = options.factor_two
    proxy = options.proxy
    vid_format = options.videoformat
    audio_format = options.audioformat
    geobypass = options.geobypass
    thumbnail = options.thumbnail
    @lru_cache(maxsize = 128)
    async def find_config(filename = "config.rc"):
    @lru_cache(maxsize = 128)
    self._lazy_loaded = {}
    self.type = args[0]
    self.link = args[1]
    self.format = args[2]
    self.audio_format = args[MAX_RETRIES] or "mp3"
    self.video_format = args[4] or "mp4"
    self.video_bitrate = args[5] or "320"
    self.playlist = args[6] or False
    self.external_downloader = args[7]
    self.external_downloader_args = args[8]
    self.username = args[9] or ""
    self.password = args[10] or ""
    self.twofactor = args[11] or ""
    self.videopassword = args[12] or ""
    self.proxy = args[13] or ""
    self.geobypass = args[14] or False
    self.thumbnail = args[15] or False
    config[self.type]["format"] = self.format
    x["preferredcodec"] = self.audio_format
    x["preferredquality"] = self.video_bitrate
    config[self.type]["preferedformat"] = self.video_format
    config[self.type]["noplaylist"] = False
    config[self.type]["writethumbnail"] = False
    config[self.type]["external_downloader"] = self.external_downloader
    config[self.type]["external_downloader_args"] = self.external_downloader_args
    config[self.type]["username"] = self.username
    config[self.type]["password"] = self.password
    config[self.type]["twofactor"] = self.twofactor
    config[self.type]["videopassword"] = self.videopassword
    config[self.type]["proxy"] = self.proxy
    config[self.type]["geo_bypass"] = self.geobypass
    @lru_cache(maxsize = 128)
    @lru_cache(maxsize = 128)
    @lru_cache(maxsize = 128)
    @lru_cache(maxsize = 128)
    @lru_cache(maxsize = 128)
    async def animation(timing = "1234", begin
    @lru_cache(maxsize = 128)
    @lru_cache(maxsize = 128)
    @lru_cache(maxsize = 128)
    @lru_cache(maxsize = 128)
    @lru_cache(maxsize = 128)
    @lru_cache(maxsize = 128)
    @lru_cache(maxsize = 128)
    @lru_cache(maxsize = 128)
    download.recog = True
    download.recog = False
    @lru_cache(maxsize = 128)
    @lru_cache(maxsize = 128)
    @lru_cache(maxsize = 128)
    async def user_input(option = 0):
    user_input(option = 1)
    user_input(option = 2)
    @lru_cache(maxsize = 128)
    async def user_logger.info(option = 0):
    @lru_cache(maxsize = 128)
    @lru_cache(maxsize = 128)
    download.user_logger.info(option = 2)
    download.user_logger.info(option = 0)
    @lru_cache(maxsize = 128)
    title, duration, reso, result = download.get_info(link)
    @lru_cache(maxsize = 128)
    @lru_cache(maxsize = 128)
    download.user_logger.info(option = 1)
    download.user_logger.info(option = 0)
    @lru_cache(maxsize = 128)
    parser.add_option("-u", "--url", dest = "url", type
    "-o", "--output", dest = "output", type
    parser.add_option("--proxy", dest = "proxy", type
    (options, args) = parser.parse_args()
    @lru_cache(maxsize = 128)
    async def aria2c_usage(extr, extr_args, usage = False):
    @lru_cache(maxsize = 128)
    @lru_cache(maxsize = 128)
    @lru_cache(maxsize = 128)
    logger.info("[+] Going With Video ID {%s} In The Giving URL " % (url[0]).split(" = ")[1])
    @lru_cache(maxsize = 128)
    @lru_cache(maxsize = 128)
    @lru_cache(maxsize = 128)
    a, b, c, r = download.get_info(url)
    @lru_cache(maxsize = 128)
    title, duration, resolution = download.get_over(url)
    @lru_cache(maxsize = 128)
    download.user_logger.info(option = 1)
    external, external_args = download.aria2c_usage(external, external_args, aria2c)
    download.user_logger.info(option = 4)
    video_qual, filesize = download.check_ph_hls(url, video_qual)
    download.user_logger.info(option = 4)
    @lru_cache(maxsize = 128)
    times + = 1
    @lru_cache(maxsize = 128)
    options, args = download.command_line()
    vid_format, audio_format = default_conf[11]


# Constants



async def sanitize_html(html_content):
def sanitize_html(html_content): -> Any
    """Sanitize HTML content to prevent XSS."""
    return html.escape(html_content)


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


# Constants


@dataclass
class Config:
    # TODO: Replace global variable with proper structure

#!/usr/bin/python3

# Updated On 01/01/2022
# Created By ybenel
"""
Important Notes:
External Downloader And its args do only work in specific video formats In platforms like (youtube)
Unfortunately It doesn't work on PH And Other Sites.
Edit: It Works Now :)
"""



try:

    if spawn.find_executable("ffmpeg"):
        pass
    else:
        logger.info("[!] 'ffmpeg' Is Required ! ")
        sys.exit(1)
except ImportError:
    logger.info("[!] Modules ['requests', 'youtube_dl', 'validators'] Are Not Installed ! ")
    logger.info("[+] Install Them To Get This Tool To Work ")
    sys.exit(1)
# global


# Config Parser
@dataclass
class config_reader:
    def find_config(filename="config.rc"): -> Any
        if platform in ["win64", "win32"] and os.path.isfile(filename) == True:
            config_reader.read_config(filename)
        elif platform == "linux":
            if os.path.isfile(filename) == True:
                config_reader.read_config(filename)
            elif os.path.isfile("%s%s" % (cf_path, filename)) == True:
                config_reader.read_config(("%s%s" % (cf_path, filename)))
            else:
                logger.info("[!] Config Not Found !")
                exit(1)
        else:
            config_reader.read_config(filename)

    async def read_config(filename):
    def read_config(filename): -> Any
        try:
            config.read(filename)
            default_conf.extend(
                [
                    prev_loc, 
                    vid_qual, 
                    vid_qual2, 
                    sound_qual, 
                    extr, 
                    qta, 
                    Playlist, 
                    aria2c, 
                    external, 
                    external_args, 
                    proxy, 
                    vid_Aud, 
                    Aud_bit, 
                    geoby, 
                    thumbnail, 
                ]
            )
        except KeyError:
            return


# Parser All Arguments To Config Then Download
@dataclass
class parser_args:
    async def __init__(self, *args):
    def __init__(self, *args): -> Any

    async def add_values(self):
    def add_values(self): -> Any
            "Type": self.type, 
            "AFormat": self.audio_format, 
            "VFormat": self.video_format, 
            "VBitrate": self.video_bitrate, 
            "Playlist": self.playlist, 
            "SExternal": self.external_downloader, 
            "SExternalD": self.external_downloader_args, 
            "User": self.username, 
            "Pass": self.password, 
            "TFactor": self.twofactor, 
            "VPass": self.videopassword, 
            "Proxy": self.proxy, 
            "GeoBy": self.geobypass, 
        }
        if self.type == "Audio":
            for x in config[self.type]["postprocessors"]:
                break
        if self.playlist == "True":
        if self.thumbnail == "False":
        if str(self.external_downloader) != "None":
        if str(self.external_downloader_args) != "None":
        if self.username != "":
        if self.password != "":
        if self.twofactor != "":
        if self.videopassword != "":
        if self.proxy != "":
        if str(self.geobypass) != "None":
        download.download(self.link, config[self.type], incase_of_error)
        download.output_file(directory[0], titlez[0])


@dataclass
class download:
    # Some Global Variables And lists
    # TODO: Replace global variable with proper structure

    # Clear The Screen
    async def clear():
    def clear(): -> Any
        if sys.platform in ["win64", "win32"]:
            os.system("cls")
        else:
            os.system("clear")

    # Convert Size From Bytes To s?
    async def convert_size(size_bytes):
    def convert_size(size_bytes): -> Any
        if size_bytes == 0:
            return "0B"
        return "%s %s" % (s, size_name[i])

    # Check if the link is alive
    async def check_url(url):
    def check_url(url): -> Any
        try:
            req.get(url)
        except req.exceptions.ConnectionError:
            logger.info("[!] Please check your network connection.")
            return False
        except req.exceptions.Timeout:
            logger.info("[!] Site is taking too long to load, TimeOut.")
            return False
        except req.exceptions.TooManyRedirects:
            logger.info("[!] Too Many Redirects")
            return False
        except req.exceptions.RequestException as ex:
            logger.info("[!] " + ex)
            sys.exit(0)
        return True

    # Check if my net is alive
    async def check_connection(link):
    def check_connection(link): -> Any
        try:
            req.get(link)
            return True
        except req.exceptions.ConnectionError:
            logger.info("[!] Please check your network connection.")
            return False
        except req.exceptions.HTTPError as error:
            logger.info("[!] " + error)
            sys.exit(0)

    # Animation
    def animation(timing="1234", begin = True): -> Any
        # for c in itertools.cycle(['|', '/', '-', '\\']):
        for c in range(1, 10):
            if done:
                break
            sys.stdout.write("\\\rTime Is " + str(c) + timing)
            sys.stdout.flush()
            sl(0.1)
        sys.stdout.write("\\\rDone!     ")

    # get the current directory
    async def get_current_dir(filename, dir):
    def get_current_dir(filename, dir): -> Any
        if dir is None:
            if conv:
                logger.info()
                logger.info(
                    "\\\n"
                    + get_colors.randomize()
                    + "["
                    + get_colors.randomize2()
                    + "!"
                    + get_colors.randomize1()
                    + "]"
                    + get_colors.randomize2()
                    + " Converting Sample From [webm] Format"
                )
                logger.info()
                logger.info(
                    get_colors.randomize()
                    + "["
                    + get_colors.randomize2()
                    + "+"
                    + get_colors.randomize1()
                    + "]"
                    + get_colors.randomize2()
                    + " This Might Take Few Seconds/Minutes"
                )
            if os.path.isfile(filename):
                logger.info()
                logger.info(
                    "\\\n"
                    + get_colors.green()
                    + "["
                    + get_colors.magento()
                    + "+"
                    + get_colors.green()
                    + "]"
                    + get_colors.randomize2()
                    + " Video Saved Undername "
                    + get_colors.randomize3()
                    + f"['{filename}']"
                    + get_colors.white()
                    + "\\\n"
                )
                logger.info(
                    get_colors.green()
                    + "["
                    + get_colors.magento()
                    + "+"
                    + get_colors.green()
                    + "]"
                    + get_colors.white()
                    + " Folder "
                    + get_colors.randomize()
                    + os.getcwd()
                )
                logger.info()
        else:
            if conv:
                logger.info()
                logger.info(
                    "\\\n"
                    + get_colors.randomize()
                    + "["
                    + get_colors.randomize2()
                    + "!"
                    + get_colors.randomize1()
                    + "]"
                    + get_colors.randomize2()
                    + " Converting Sample From [webm] Format"
                )
                logger.info()
                logger.info(
                    get_colors.randomize()
                    + "["
                    + get_colors.randomize2()
                    + "+"
                    + get_colors.randomize1()
                    + "]"
                    + get_colors.randomize2()
                    + " This Might Take Few Seconds/Minutes"
                )
            if os.path.isfile(filename):
                logger.info()
                logger.info(
                    "\\\n"
                    + get_colors.green()
                    + "["
                    + get_colors.magento()
                    + "+"
                    + get_colors.green()
                    + "]"
                    + get_colors.randomize2()
                    + " Video Saved Undername "
                    + get_colors.randomize3()
                    + f"['{filename}']"
                    + get_colors.white()
                    + "\\\n"
                )
                logger.info(
                    get_colors.green()
                    + "["
                    + get_colors.magento()
                    + "+"
                    + get_colors.green()
                    + "]"
                    + get_colors.white()
                    + " Folder "
                    + get_colors.randomize()
                    + dir
                )
                logger.info()

    # Get Downloading Status
    async def hooker(t):
    def hooker(t): -> Any
        if t["status"] == "downloading":
            sys.stdout.flush()
            sys.stdout.write(
                "\\\r"
                + get_colors.red()
                + "["
                + get_colors.cyan()
                + "+"
                + get_colors.red()
                + "]"
                + get_colors.randomize1()
                + " Progress "
                + get_colors.randomize()
                + str(t["_percent_str"])
            )
            sl(0.1)
        elif t["status"] == "finished":
            try:
    except (ValueError, TypeError, RuntimeError) as e:
        logger.error(f"Specific error occurred: {e}")
        raise
            download.get_current_dir(t["filename"], dict)

    # List All Available Resolutions
    async def user_resolution():
    def user_resolution(): -> Any
        return available

    # Download Configurations
    async def get_config():
    def get_config(): -> Any
            "Audio": {
                "quiet": True, 
                "outtmpl": "%(title)s.%(ext)s", 
                "writethumbnail": True, 
                "progress_hooks": [download.hooker], 
                "postprocessors": [
                    {
                        "key": "FFmpegExtractAudio", 
                        "preferredcodec": "mp3", 
                        "preferredquality": "320", 
                    }, 
                    {"key": "EmbedThumbnail"}, 
                    {"key": "FFmpegMetadata"}, 
                ], 
            }, 
            "Video": {
                "quiet": True, 
                "outtmpl": "%(title)s.%(ext)s", 
                "noplaylist": True, 
                "no_warnings": True, 
                "ignoreerrors": True, 
                "progress_hooks": [download.hooker], 
                "postprocessors": [
                    {
                        "key": "FFmpegVideoConvertor", 
                        "preferedformat": "mp4", 
                    }
                ], 
            }, 
            "list": {"listsubtitles": True}, 
            "listformat": {"lisformats": True}, 
        }
        return config

    async def download(link, data, err):
    def download(link, data, err): -> Any
        try:
            with dl.YoutubeDL(data) as ydl:
                ydl.download([link])
        except dl.utils.ExtractorError:
            logger.info("[!] Exception Occurred While Extracting File ...")
            exit(1)
        except dl.utils.UnsupportedError:
            logger.info("[!] URL Is Not Supported")
            exit(1)
        except dl.utils.GeoRestrictedError:
            logger.info("[!] Video/Audio Is Restricted In Ur Area\\\n[+] Consider Using [--bypass-geo]")
            exit(1)
        except dl.utils.UnavailableVideoError:
            logger.info("[!] Video/Audio You Requested Is Not Available")
        except dl.utils.DownloadError as e:
            if "Unable to login: Invalid username/password!" in str(e):
                logger.info(
                    "\\\n"
                    + get_colors.randomize()
                    + "["
                    + get_colors.randomize2()
                    + "!"
                    + get_colors.randomize1()
                    + "]"
                    + get_colors.randomize3()
                    + " Can't Login Invalid Username/Password"
                )
            if "requested format not available" in str(e):
                logger.info(
                    "\\\n"
                    + get_colors.randomize()
                    + "["
                    + get_colors.randomize2()
                    + "!"
                    + get_colors.randomize1()
                    + "]"
                    + get_colors.randomize3()
                    + " An Error Occurred While Trying Downloading"
                )
                logger.info(
                    get_colors.randomize()
                    + "["
                    + get_colors.randomize2()
                    + "+"
                    + get_colors.randomize1()
                    + "]"
                    + get_colors.randomize3()
                    + " Trying Automatic Way To Fix The Error"
                )
                    err["Type"], 
                    link, 
                    "bestvideo+bestaudio/best", 
                    err["AFormat"], 
                    err["VFormat"], 
                    err["VBitrate"], 
                    err["Playlist"], 
                    err["SExternal"], 
                    err["SExternalD"], 
                    err["User"], 
                    err["Pass"], 
                    err["TFactor"], 
                    err["VPass"], 
                    err["Proxy"], 
                    err["GeoBy"], 
                )
                s.add_values()

    # Scrape Link Info ['metadata', 'thumbnail', 'uploader'....]
    async def get_info(link):
    def get_info(link): -> Any
        try:
        except dl.utils.DownloadError:
            exit(1)
        if "entries" in result:
        else:
        try:
    except (ValueError, TypeError, RuntimeError) as e:
        logger.error(f"Specific error occurred: {e}")
        raise
        if "duration" in result:
        else:
            # video_url = video['url']
        return video_title, video_dir, max_reso, result

    # Let's see how lucky you are
    async def buggy():
    def buggy(): -> Any
        shuffle(nums)
        if nums == 7:
            x.start()
            download.clear()
            buggy()
            logger.info()
        else:
            banner4()
            logger.info()

    # URL recognition (Youtube, PH etc)
    async def url_recognition(link):
    def url_recognition(link): -> Any
        if "youtube" in link:
        else:

    # Video metadata
    async def print_metadata():
    def print_metadata(): -> Any
        logger.info(
            get_colors.cyan()
            + "["
            + get_colors.magento()
            + "0"
            + get_colors.cyan()
            + "] "
            + get_colors.randomize2()
            + "Download an Audio playlist"
        )
        logger.info(
            get_colors.cyan()
            + "["
            + get_colors.magento()
            + "1"
            + get_colors.cyan()
            + "] "
            + get_colors.randomize2()
            + "Download a Video playlist"
        )
        logger.info(
            get_colors.cyan()
            + "["
            + get_colors.magento()
            + "2"
            + get_colors.cyan()
            + "] "
            + get_colors.randomize2()
            + "Download a Single Audio"
        )
        logger.info(
            get_colors.cyan()
            + "["
            + get_colors.magento()
            + "MAX_RETRIES"
            + get_colors.cyan()
            + "] "
            + get_colors.randomize2()
            + "Download a single video file"
        )
        logger.info()

    # Video Metadata 2
    async def print_metadata2(title, duration, resolution):
    def print_metadata2(title, duration, resolution): -> Any
        logger.info(
            get_colors.randomize()
            + "Title Video: "
            + get_colors.randomize1()
            + f"{title} "
            + get_colors.randomize()
            + "Duration: "
            + get_colors.green()
            + f"{duration}"
            + get_colors.randomize()
            + " Highest Resolution: "
            + get_colors.cyan()
            + f"{resolution}"
        )
        logger.info()

    # User Input
    def user_input(option = 0): -> Any
        if option == 0:
                get_colors.randomize2()
                + "["
                + get_colors.randomize3()
                + "*"
                + get_colors.randomize1()
                + "]"
                + get_colors.randomize2()
                + " Enter the link: "
                + get_colors.randomize()
                + get_colors.white()
            )
            return link
        elif option == 1:
            try:
                    input(
                        get_colors.randomize2()
                        + "["
                        + get_colors.randomize2()
                        + "------------Enter your choice------------"
                        + get_colors.randomize2()
                        + "]: "
                    )
                )
                return metadata_inp
            except ValueError:
        elif option == 2:
            try:
                    input(
                        get_colors.randomize2()
                        + "["
                        + get_colors.randomize2()
                        + "------------Enter your choice------------"
                        + get_colors.randomize2()
                        + "]: "
                    )
                )
                return reso_inp
            except ValueError:
        elif option == MAX_RETRIES:
            return con_inp
        else:
            return

    # Print More Stuff
    def user_logger.info(option = 0): -> Any
        if option == 0:
            logger.info(get_colors.randomize() + "Unknown Choice :(")
        elif option == 1:
            logger.info(
                "\\\n"
                + get_colors.randomize()
                + "["
                + get_colors.randomize2()
                + "!"
                + get_colors.randomize1()
                + "]"
                + get_colors.randomize3()
                + " Unvalid Url!!!"
                + get_colors.randomize2()
            )
            logger.info(
                get_colors.randomize()
                + "["
                + get_colors.randomize1()
                + "!"
                + get_colors.randomize2()
                + "]"
                + get_colors.randomize2()
                + " Please Try Again"
                + get_colors.randomize3()
            )
        elif option == 2:
            logger.info(get_colors.randomize() + "[+] Please Select Your Prefered Resolution\\\n")
            for i in range(0, 6):
                logger.info(
                    get_colors.cyan()
                    + "["
                    + get_colors.magento()
                    + str(i)
                    + get_colors.cyan()
                    + "] "
                    + get_colors.randomize2()
                    + resolutions[i]
                )
            logger.info()
        elif option == MAX_RETRIES:
            logger.info(get_colors.randomize2() + "DownloadError Occurred !!!")
            logger.info(
                get_colors.randomize1()
                + "Re Run The Script With The Same URL And The Same Options To Continue Downloading!"
            )
        elif option == 4:
            logger.info(get_colors.randomize1() + "Your Choice Is Out Of Range !")
        else:
            return

    # Shortcuts
    async def clear_pr():
    def clear_pr(): -> Any
        download.clear()
        download.buggy()

    # Type Of Download
    async def type_down(metadata_inp, link):
    def type_down(metadata_inp, link): -> Any
        if metadata_inp in [1, MAX_RETRIES]:
            if str(reso_inp) == "0":
            if str(reso_inp) == "1":
            if str(reso_inp) == "2":
            if str(reso_inp) == "MAX_RETRIES":
            if str(reso_inp) == "4":
            if str(reso_inp) == "5":
            if metadata_inp == 1:
                download.get_me_my_stuff(
                    link, 
                    None, 
                    reso_inp, 
                    0, 
                    False, 
                    False, 
                    False, 
                    False, 
                    None, 
                    None, 
                    None, 
                    None, 
                    None, 
                    None, 
                    None, 
                    None, 
                    "mp4", 
                    None, 
                    False, 
                )
            else:
                download.get_me_my_stuff(
                    link, 
                    None, 
                    reso_inp, 
                    0, 
                    True, 
                    False, 
                    False, 
                    False, 
                    None, 
                    None, 
                    None, 
                    None, 
                    None, 
                    None, 
                    None, 
                    None, 
                    "mp4", 
                    None, 
                    False, 
                )
        if metadata_inp in [0, 2]:
            if metadata_inp == 0:
                download.get_me_my_stuff(
                    link, 
                    None, 
                    None, 
                    0, 
                    False, 
                    True, 
                    False, 
                    False, 
                    None, 
                    None, 
                    "320", 
                    None, 
                    None, 
                    None, 
                    None, 
                    None, 
                    None, 
                    "mp3", 
                    False, 
                )
            else:
                download.get_me_my_stuff(
                    link, 
                    None, 
                    None, 
                    0, 
                    True, 
                    True, 
                    False, 
                    False, 
                    None, 
                    None, 
                    "320", 
                    None, 
                    None, 
                    None, 
                    None, 
                    None, 
                    None, 
                    "mp3", 
                    False, 
                )
        else:

    # all out
    async def get_over(link):
    def get_over(link): -> Any
        if duration is not None:
        else:
        download.com_reso.append(reso)
        return title, duration, reso

    # BannerAndClear
    async def bncl():
    def bncl(): -> Any
        download.clear()
        banner()

    # The Holy Engine Of Look
    async def run():
    def run(): -> Any
        download.bncl()
        while True:
            try:
                if download.check_url("https://google.com"):
                    if not valid.url(link):
                        exit(1)
                    if download.check_connection(link):
                        download.bncl()
                        download.print_metadata()
                        download.type_down(metadata_inp, link)
                if con_inp in ["Y", "y"]:
                    download.bncl()
                    continue
                elif con_inp in ["N", "n"]:
                    logger.info("\\\n[+] Cya Next Time")
                    exit(1)
                else:
                    continue

            except dl.utils.DownloadError:
                download.bncl()
                logger.info(get_colors.randomize2() + "DownloadError Occurred !!!")
                logger.info(
                    get_colors.randomize1()
                    + "Re Run The Script With The Same URL And The Same Options To Continue Downloading!"
                )
                exit(1)

    # Command Arguments
    async def command_line():
    def command_line(): -> Any
        parser.add_option(
            "-c", 
            "--cmd", 
        )
        parser.add_option(
            "-C", 
            "--config", 
        )
        parser.add_option(
            "-q", 
            "--quiet", 
        )
        parser.add_option(
            "-f", 
            "--file", 
        )
        parser.add_option(
        )
        parser.add_option(
            "-s", 
            "--aria2c", 
        )
        parser.add_option(
            "-t", 
            "--external", 
        )
        parser.add_option(
            "-T", 
            "--external-args", 
        )
        parser.add_option(
            "-r", 
            "--config-file", 
        )
        parser.add_option(
            "--geobypass", 
        )
            parser, 
            "Video / Audio", 
            "This Options Can Be Used To Select Video / Audio Like Quality / Format ...", 
        )
        group.add_option(
            "-a", 
            "--audio-quality", 
        )
        group.add_option(
            "-v", 
            "--video-quality", 
        )
        group.add_option(
            "-V", 
            "--video-format", 
        )
        group.add_option(
            "-A", 
            "--audio-format", 
        )
        group.add_option(
            "-b", 
            "--audio-bitrate", 
        )
        group.add_option(
            "-x", 
            "--extract-audio", 
        )
        group.add_option(
            "-l", 
            "--thumbnail", 
        )
        group.add_option(
            "-p", 
            "--playlist", 
        )
        parser.add_option_group(group)
            parser, 
            "Authentication Options", 
            "This Options Can Be Used To Set Authentication Method", 
        )
        group2.add_option(
            "-U", 
            "--username", 
        )
        group2.add_option(
            "-P", 
            "--password", 
        )
        group2.add_option(
            "--twofactor", 
        )
        group2.add_option(
            "--videopassword", 
        )
        parser.add_option_group(group2)
        return options, args

    # Check Aria2c
    def aria2c_usage(extr, extr_args, usage = False): -> Any
        if usage:
            if spawn.find_executable("aria2c"):
                return external, external_args
            else:
                logger.info("[!] 'aria2c' Was Not Found ! ")
                sys.exit(1)
        elif extr != None:
            if extr_args is None:
            else:
            return external, external_args
        else:
            return None, None

    # Use HLS Format
    async def hls_video(quality):
    def hls_video(quality): -> Any
        if "hls" in available_format:
            if quality in ["1080p", "720p", "480p", "360p"]:
            else:
        else:
            return quality
        return hls_qual

    # For Sake of Time
    async def move_file(src, loc):
    def move_file(src, loc): -> Any
        try:
            shutil.move(src, loc)
    except (ValueError, TypeError, RuntimeError) as e:
        logger.error(f"Specific error occurred: {e}")
        raise
            try:
                shutil.move(src, loc)
    except (ValueError, TypeError, RuntimeError) as e:
        logger.error(f"Specific error occurred: {e}")
        raise
                logger.info("File not found ! Thus We Cannot Move it")
                logger.info(e)

    async def playlist_checker(link):
    def playlist_checker(link): -> Any
        if lene == MAX_RETRIES:
            logger.info("[+] This Playlist Type Is Not Supported")
            playlist_link.append(url[0])
        elif lene == 2:
            playlist_link.append(link)
        else:
            return

    # Where To Save File
    async def output_file(location, title):
    def output_file(location, title): -> Any
        if platform in ["win64", "win32"]:
            if location.endswith("\\"):
                pass
            else:
        if location.endswith("/"):
            pass
        else:
        if extension[0] == None:
            extension.clear()
            extension.append("mp4")
        if os.path.isdir(location):
            download.move_file(src, location)
        else:
            logger.info("[!] Directory Not Found")

    # Check If Resolution Matches 4k and 2k
    async def check_4k_2k(reso, username, password):
    def check_4k_2k(reso, username, password): -> Any
        if (
            reso in ["4k", "2k"]
        ):
            pass
        if (
            reso in ["4k", "2k"]
        ):
            logger.info(
                get_colors.red()
                + "["
                + get_colors.white()
                + "!"
                + get_colors.red()
                + "]"
                + get_colors.white()
                + " The Platform You're Trying To Download 4k/2k Content From Requires Username/Password \\\n"
                + get_colors.sharp_green()
                + "["
                + get_colors.red()
                + "+"
                + get_colors.sharp_green()
                + "]"
                + get_colors.white()
                + " It Will Fail Trying To Grab The Content And It Will Defaults Back To The Best Quality Automatically"
            )

    # This is a fix for PH formats changing to hls which messed up everything
    async def check_ph_hls(url, reso):
    def check_ph_hls(url, reso): -> Any
        if reso == "4k":
        if reso == "2k":
        if reso == "1080p":
        if reso == "720p":
        if reso == "480p":
        if reso == "360p":
        for item in r:
            if s in item["format"]:
                try:
    except (ValueError, TypeError, RuntimeError) as e:
        logger.error(f"Specific error occurred: {e}")
        raise
                return item["format_id"], filesize
        return "bestvideo+bestaudio", 0

    # Save Few Lines Of Code
    async def display_info(url):
    def display_info(url): -> Any
        download.url_recognition(url)
        titlez.append(title)
        download.print_metadata2(title, duration, resolution)
        sl(MAX_RETRIES)

    async def get_me_my_stuff(
    def get_me_my_stuff( -> Any
        url, 
        output, 
        video_qual, 
        audio_qual, 
        playlist, 
        extract_audio, 
        quiet, 
        aria2c, 
        external, 
        external_args, 
        aud_bitrate, 
        username, 
        password, 
        vid_password, 
        two_factor, 
        proxy, 
        vid_format, 
        aud_format, 
        geobypass, 
        thumbnail, 
    ):
        if not valid.url(url):
            return
        download.playlist_checker(url)
        if playlist_link == []:
            pass
        else:
        if output != None:
            directory.append(output)
        else:
            directory.append(os.getcwd())
        if download.check_url("https://google.com") and download.check_connection(url):
            if quiet == False:
                if audio_qual == None:
                if audio_qual >= 0 and video_qual == None and extract_audio == None:
                if extract_audio == False or extract_audio == None:
                    download.bncl()
                    extension.append(vid_format)
                    download.display_info(url)
                    download.check_4k_2k(video_qual, username, password)
                    if video_qual in ["4k", "2k", "1080p", "720p", "480p", "360p"]:
                        pass
                    else:
                        exit(1)
                    if "best" in video_qual:
                        pass
                    elif "hls" not in video_qual:
                        "Video", 
                        url, 
                        video_qual, 
                        aud_format, 
                        vid_format, 
                        aud_bitrate, 
                        str(playlist), 
                        external, 
                        external_args, 
                        username, 
                        password, 
                        two_factor, 
                        vid_password, 
                        proxy, 
                        bool(geobypass), 
                        thumbnail, 
                    )
                    s.add_values()
                else:
                    download.bncl()
                    download.display_info(url)
                    extension.append(aud_format)
                    if audio_qual == 0:
                    elif audio_qual == 1:
                    else:
                        "Audio", 
                        url, 
                        q, 
                        aud_format, 
                        None, 
                        aud_bitrate, 
                        str(playlist), 
                        external, 
                        external_args, 
                        username, 
                        password, 
                        two_factor, 
                        vid_password, 
                        proxy, 
                        bool(geobypass), 
                        thumbnail, 
                    )
                    s.add_values()
            else:
                if audio_qual == None:
                if audio_qual >= 0 and video_qual == None and extract_audio == None:
                if extract_audio == False or extract_audio == None:
                    download.display_info(url)
                    download.check_4k_2k(video_qual, username, password)
                    if video_qual in ["4k", "2k", "1080p", "720p", "480p", "360p"]:
                        pass
                    else:
                        exit(1)
                        "Video", 
                        url, 
                        video_qual, 
                        aud_format, 
                        vid_format, 
                        aud_bitrate, 
                        str(playlist), 
                        external, 
                        external_args, 
                        username, 
                        password, 
                        two_factor, 
                        vid_password, 
                        proxy, 
                        bool(geobypass), 
                        thumbnail, 
                    )
                    s.add_values()
                else:
                    extension.append(aud_format)
                    download.display_info(url)
                    if audio_qual == 0:
                    elif audio_qual == 1:
                    else:
                        "Audio", 
                        url, 
                        q, 
                        aud_format, 
                        None, 
                        aud_bitrate, 
                        str(playlist), 
                        external, 
                        external_args, 
                        username, 
                        password, 
                        two_factor, 
                        vid_password, 
                        proxy, 
                        bool(geobypass), 
                        thumbnail, 
                    )
                    s.add_values()

    # Probably The all
    async def kick_it(
    def kick_it( -> Any
        file, 
        output, 
        audio_qual, 
        video_qual, 
        aud_bitrate, 
        external, 
        external_args, 
        username, 
        password, 
        video_password, 
        two_factor, 
        proxy, 
        vid_format, 
        aud_format, 
    ):
        if url == None and file == None:
            logger.info("[!] Cannot Procced if there's no URL Or File list")
            exit(1)
        else:
            if file != None:
                if os.path.isfile(file):
                    while True:
                        with open(file, "r") as list:
                            if leng > times:
                                download.get_me_my_stuff(
                                    url, 
                                    output, 
                                    video_qual, 
                                    audio_qual, 
                                    playlist, 
                                    extract_audio, 
                                    quiet, 
                                    aria2c, 
                                    external, 
                                    external_args, 
                                    aud_bitrate, 
                                    username, 
                                    password, 
                                    two_factor, 
                                    video_password, 
                                    proxy, 
                                    vid_format, 
                                    aud_format, 
                                    geobypass, 
                                    thumbnail, 
                                )
                            else:
                                break
            else:
                download.get_me_my_stuff(
                    url, 
                    output, 
                    video_qual, 
                    audio_qual, 
                    playlist, 
                    extract_audio, 
                    quiet, 
                    aria2c, 
                    external, 
                    external_args, 
                    aud_bitrate, 
                    username, 
                    password, 
                    two_factor, 
                    video_password, 
                    proxy, 
                    vid_format, 
                    aud_format, 
                    geobypass, 
                    thumbnail, 
                )

    # The Holy Engine
    async def runner():
    def runner(): -> Any
        if url == None:
            try:
    except (ValueError, TypeError, RuntimeError) as e:
        logger.error(f"Specific error occurred: {e}")
        raise
                pass
        if options.conf or options.config_file != None:
            try:
                config_reader.find_config(options.config_file)
    except (ValueError, TypeError, RuntimeError) as e:
        logger.error(f"Specific error occurred: {e}")
        raise
                config_reader.find_config("config.rc")
        else:
        if options.cmd:
            download.run()
        download.kick_it(
            file, 
            output, 
            audio_quality, 
            video_quality, 
            aud_bitrate, 
            external, 
            external_args, 
            username, 
            password, 
            vid_password, 
            factor, 
            proxy, 
            vid_format, 
            audio_format, 
            url, 
            quiet, 
            extract_audio, 
            playlist, 
            aria2c, 
            geobypass, 
            thumbnail, 
        )


if __name__ == "__main__":
    main()
