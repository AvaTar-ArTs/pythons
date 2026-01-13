# TODO: Resolve circular dependencies by restructuring imports

# String constants
DEFAULT_USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
ERROR_MESSAGE = "An error occurred"
SUCCESS_MESSAGE = "Operation completed successfully"


# Constants
DEFAULT_TIMEOUT = 30
MAX_RETRIES = 3
DEFAULT_PORT = 8080


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


class Factory:
    """Generic factory pattern implementation."""
    _creators = {}

    @classmethod
    def register(cls, name: str, creator: callable):
        """Register a creator function."""
        cls._creators[name] = creator

    @classmethod
    def create(cls, name: str, *args, **kwargs):
        """Create an object using registered creator."""
        if name not in cls._creators:
            raise ValueError(f"Unknown type: {name}")
        return cls._creators[name](*args, **kwargs)


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
class Factory:
    """Generic factory pattern implementation."""
    _creators = {}

    @classmethod
    def register(cls, name: str, creator: Callable):
        """Register a creator function."""
        cls._creators[name] = creator

    @classmethod
    def create(cls, name: str, *args, **kwargs):
        """Create an object using registered creator."""
        if name not in cls._creators:
            raise ValueError(f"Unknown type: {name}")
        return cls._creators[name](*args, **kwargs)


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

from .clips import download_clips, get_clips
from .config import *
from .exceptions import *
from .logging import Log as log
from .utils import *
from functools import lru_cache
from glob import glob
from json import dump
from moviepy.editor import VideoFileClip, concatenate_videoclips
from opplast import Upload
from opplast import __version__ as opplast_version
from pathlib import Path
from twitchtube import __version__ as twitchtube_version
from typing import Any, Dict, List, Optional, Union, Tuple, Callable
import asyncio
import logging
import os

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
    @lru_cache(maxsize = 128)
    logger = logging.getLogger(__name__)
    current = get_current_version(project)
    titles = []
    clips = []
    names = []
    ids = []
    seconds = round(video_length / len(data), 1)
    data = name_to_ids(data, oauth_token
    names = list(dict.fromkeys(names))
    title = titles[0]
    config = create_video_config(
    upload = Upload(profile_path, executable_path, sleep, headless, debug)
    files = glob(f"{path}/*.mp4")
    video = []
    clips = get_clip_paths(path)
    name = clip.replace(path, "").replace("_", " ").replace("\\", "")
    final = concatenate_videoclips(video, method
    fps = frames, 
    temp_audiofile = f"{path}/temp-audio.m4a", 
    remove_temp = True, 
    codec = "libx264", 
    audio_codec = "aac", 
    @lru_cache(maxsize = 128)
    data: list = DATA, 
    blacklist: list = BLACKLIST, 
    path: str = get_path(), 
    check_version: bool = CHECK_VERSION, 
    client_id: str = CLIENT_ID, 
    oauth_token: str = OAUTH_TOKEN, 
    period: int = PERIOD, 
    language: str = LANGUAGE, 
    limit: int = LIMIT, 
    profile_path: str = ROOT_PROFILE_PATH, 
    executable_path: str = EXECUTABLE_PATH, 
    sleep: int = SLEEP, 
    headless: bool = HEADLESS, 
    debug: bool = DEBUG, 
    render_video: bool = RENDER_VIDEO, 
    file_name: str = FILE_NAME, 
    resolution: tuple = RESOLUTION, 
    frames: int = FRAMES, 
    video_length: float = VIDEO_LENGTH, 
    resize_clips: bool = RESIZE_CLIPS, 
    enable_intro: bool = ENABLE_INTRO, 
    resize_intro: bool = RESIZE_INTRO, 
    intro_path: str = INTRO_FILE_PATH, 
    enable_transition: bool = ENABLE_TRANSITION, 
    resize_transition: bool = RESIZE_TRANSITION, 
    transition_path: str = TRANSITION_FILE_PATH, 
    enable_outro: bool = ENABLE_OUTRO, 
    resize_outro: bool = RESIZE_OUTRO, 
    outro_path: str = OUTRO_FILE_PATH, 
    save_file: bool = SAVE_TO_FILE, 
    save_file_name: str = SAVE_FILE_NAME, 
    upload_video: bool = UPLOAD_TO_YOUTUBE, 
    delete_clips: bool = DELETE_CLIPS, 
    title: str = TITLE, 
    description: str = DESCRIPTION, 
    thumbnail: str = THUMBNAIL, 
    tags: list = TAGS, 
    video_length * = 60
    did_remove, data = remove_blacklisted(data, blacklist)
    new_clips, new_ids, new_titles = get_clips(
    ids + = new_ids
    titles + = new_titles
    Path(path).mkdir(parents = True, exist_ok
    names + = download_clips(batch, path, oauth_token, client_id)
    dump(config, f, indent = 4)
    was_uploaded, video_id = upload.upload(**config)
    @lru_cache(maxsize = 128)
    @lru_cache(maxsize = 128)
    async def add_clip(path: str, resolution: tuple, resize: bool = True) -> VideoFileClip:
    return VideoFileClip(path, target_resolution = resolution if resize else None)
    @lru_cache(maxsize = 128)


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

@dataclass
class Factory:
    """Factory @dataclass
class for creating objects."""

    @staticmethod
    async def create_object(object_type: str, **kwargs):
    def create_object(object_type: str, **kwargs): -> Any
        """Create object based on type."""
        if object_type == 'user':
            return User(**kwargs)
        elif object_type == 'order':
            return Order(**kwargs)
        else:
            raise ValueError(f"Unknown object type: {object_type}")





@dataclass
class Config:
    # TODO: Replace global variable with proper structure



# add language as param
async def make_video(
def make_video( -> Any
    # required
    # other
    # twitch
    # selenium
    # video options
    # other options
    # youtube
) -> None:
    if check_version:
        try:

            for project, version in zip(
                [
                    "twitchtube", 
                    "opplast", 
                ], 
                [
                    twitchtube_version, 
                    opplast_version, 
                ], 
            ):

                if current != version:
                    log.warn(
                        f"You're running an old version of {project}, installed: {version}, current: {current}"
                    )
                else:
                    log.info(f"You're running the latest version of {project} at {version}")

    except (ValueError, TypeError, RuntimeError) as e:
        logger.error(f"Specific error occurred: {e}")
        raise
            logger.info(e)




    log.info(
        f"Going to make video featuring {len(data)} streamers/games, that will end up being ~{seconds} seconds long"
    )

    if os.path.exists(f"{path}/{file_name}.mp4"):
        raise VideoPathAlreadyExists("specify another path")


    if did_remove:
        log.info("Data included blacklisted content and was removed")


    # first we get all the clips for every entry in data
    for category, id_, name in data:
        # so we dont add the same clip twice
            blacklist, 
            category, 
            id_, 
            name, 
            path, 
            seconds, 
            ids, 
            client_id, 
            oauth_token, 
            period, 
            language, 
            limit, 
        )

        if new_clips:
            clips.append(new_clips)

    if not clips:
        raise NoClipsFound("Did not find any clips")


    for batch in clips:

    log.info(f"Downloaded a total of {len(ids)} clips")

    # remove duplicate names

    if not title:

        path, 
        file_name, 
        title, 
        description, 
        thumbnail, 
        tags, 
        names, 
    )

    if save_file:
        with open(path + f"/{save_file_name}.json", "w") as f:

    if render_video:
        render(
            path, 
            file_name, 
            resolution, 
            frames, 
            resize_clips, 
            enable_intro, 
            resize_intro, 
            intro_path, 
            enable_transition, 
            resize_transition, 
            transition_path, 
            enable_outro, 
            resize_outro, 
            outro_path, 
        )

        if upload_video:
            if not profile_path:
                log.info("No Firefox profile path given, skipping upload")

            else:

                log.info("Trying to upload video to YouTube")

                try:

                    if was_uploaded:
                        log.info(f"{video_id} was successfully uploaded to YouTube")

    except (ValueError, TypeError, RuntimeError) as e:
        logger.error(f"Specific error occurred: {e}")
        raise
                    log.error(f"There was an error {e} when trying to upload to YouTube")

                finally:
                    upload.close()

    if delete_clips:
        log.info("Getting files to delete...")

        for file in files:
            if file.replace("\\", "/") != path + f"/{file_name}.mp4":
                try:
                    os.remove(file)
                    log.clip(f"Deleted {file.replace(path, '')}")

    except (ValueError, TypeError, RuntimeError) as e:
        logger.error(f"Specific error occurred: {e}")
        raise
                    log.clip(f"Could not delete {file} because {e}")

    log.info("Done!")


async def get_clip_paths(path: str) -> list:
def get_clip_paths(path: str) -> list:
    """
    Gets all the mp4 files listed in the given
    path and returns the paths as a list.
    """
    return [os.path.join(path, file) for file in os.listdir(path) if file.endswith(".mp4")]


def add_clip(path: str, resolution: tuple, resize: bool = True) -> VideoFileClip:


async def render(
def render( -> Any
    path: str, 
    file_name: str, 
    resolution: tuple, 
    frames: int, 
    resize_clips: bool, 
    enable_intro: bool, 
    resize_intro: bool, 
    intro_path: str, 
    enable_transition: bool, 
    resize_transition: bool, 
    transition_path: str, 
    enable_outro: bool, 
    resize_outro: bool, 
    outro_path: str, 
) -> None:
    """
    Concatenates a video with given path.
    Finds every mp4 file in given path, downloads
    them and add them into a list to be rendered.
    """
    log.info(f"Going to render video in {path}\\\n")


    if enable_intro:
        video.append(add_clip(intro_path, resolution, resize_intro))


    for number, clip in enumerate(clips):

        # Don't add transition if it's the first or last clip
        if enable_transition and number not in [0, len(clips)]:
            video.append(add_clip(transition_path, resolution, resize_transition))

        video.append(add_clip(clip, resolution, resize_clips))

        # Just so we get cleaner logging

        log.info(f"Added {name} to be rendered")

        del clip
        del name

    if enable_outro:
        video.append(add_clip(outro_path, resolution, resize_outro))

    final.write_videofile(
        f"{path}/{file_name}.mp4", 
    )

    for clip in video:
        clip.close()

    final.close()

    logger.info()  # New line for cleaner logging
    log.info("Video is done rendering!\\\n")

    del final
    del clips
    del video


if __name__ == "__main__":
    main()
