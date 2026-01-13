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


from abc import ABC, abstractmethod

class Strategy(ABC):
    """Strategy interface."""
    @abstractmethod
    def execute(self, data: Any) -> Any:
        """Execute the strategy."""
        pass

class Context:
    """Context class for strategy pattern."""
    def __init__(self, strategy: Strategy):
        self._strategy = strategy

    def set_strategy(self, strategy: Strategy) -> None:
        """Set the strategy."""
        self._strategy = strategy

    def execute_strategy(self, data: Any) -> Any:
        """Execute the current strategy."""
        return self._strategy.execute(data)


from abc import ABC, abstractmethod

class Observer(ABC):
    """Observer interface."""
    @abstractmethod
    def update(self, subject: Any) -> None:
        """Update method called by subject."""
        pass

class Subject:
    """Subject class for observer pattern."""
    def __init__(self):
        self._observers: List[Observer] = []
        self._lock = threading.Lock()

    def attach(self, observer: Observer) -> None:
        """Attach an observer."""
        with self._lock:
            self._observers.append(observer)

    def detach(self, observer: Observer) -> None:
        """Detach an observer."""
        with self._lock:
            if observer in self._observers:
                self._observers.remove(observer)

    def notify(self) -> None:
        """Notify all observers."""
        with self._lock:
            for observer in self._observers:
                try:
                    observer.update(self)
                except Exception as e:
                    logger.error(f"Observer notification failed: {e}")


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


# Connection pooling for HTTP requests
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

def get_session() -> requests.Session:
    """Get a configured session with connection pooling."""
    session = requests.Session()

    # Configure retry strategy
    retry_strategy = Retry(
        total = 3, 
        backoff_factor = 1, 
        status_forcelist=[429, 500, 502, 503, 504], 
    )

    # Mount adapter with retry strategy
    adapter = HTTPAdapter(max_retries = retry_strategy)
    session.mount("http://", adapter)
    session.mount("https://", adapter)

    return session


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

                from os.path import relpath
            from os import remove
        from . import __version__
from .exceptions import (
from .logger import Logger
from .spotify import Spotify
from .track import Track
from .types import *
from .utils import (
from ffmpy import FFmpeg, FFRuntimeError
from functools import lru_cache
from multiprocessing import cpu_count
from multiprocessing.dummy import Pool as ThreadPool
from pathlib import Path
from shutil import Error as ShutilError
from shutil import move
from typing import Any, Dict, List, Optional, Union, Tuple, Callable
from urllib.error import URLError
from youtube_dl import YoutubeDL
import asyncio
import os
import requests
import time
import tldextract
import validators

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
    __all__ = ["Savify"]
    group = group.replace("%artist%", safe_path_string(track.artists[0]))
    group = group.replace("%album%", safe_path_string(track.album_name))
    group = group.replace("%playlist%", safe_path_string(track.playlist))
    api_credentials = None, 
    quality = Quality.BEST, 
    download_format = Format.MP3, 
    group = None, 
    latest_ver = requests.get(
    current_ver = f"v{__version__}"
    result = list()
    result = self.spotify.link(query, artist_albums
    result = self.spotify.search(query, query_type
    result = self.spotify.search(query, query_type
    result = self.spotify.search(query, query_type
    result = self.spotify.search(
    query_type = Type.TRACK, 
    create_m3u = False, 
    queue = self._parse_query(query, query_type
    start_time = time.time()
    jobs = pool.map(self._download, queue)
    failed_jobs = list()
    successful_jobs = list()
    track = successful_jobs[0]["track"]
    playlist = safe_path_string(track.playlist)
    playlist = track.album_name
    playlist = track.artists[0]
    playlist = track.name
    m3u = f"#EXTM3U\\\n#PLAYLIST:{playlist}\\\n"
    m3u_location = self.path_holder.get_download_dir() / f"{playlist}.m3u"
    track = job["track"]
    location = job["location"]
    message = (
    extractor = "ytsearch"
    query = (
    query = ""
    output = (
    output_temp = f"{str(self.path_holder.get_temp_dir())}/{track.id}.%(ext)s"
    status = {
    options = {
    output_temp = output_temp.replace("%(ext)s", self.download_format)
    attempt = 0
    attempt = 0
    cover_art_name = f"{track.album_name} - {track.artists[0]}"
    cover_art = self.downloaded_cover_art[cover_art_name]
    cover_art = self.path_holder.download_file(track.cover_art_url, extension
    ffmpeg = FFmpeg(
    executable = self.ffmpeg_location, 
    inputs = {
    outputs = {
    @lru_cache(maxsize = 128)
    @lru_cache(maxsize = 128)
    @lru_cache(maxsize = 128)
    self._lazy_loaded = {}
    path_holder: PathHolder = None, 
    retry: int = 3, 
    ydl_options: dict = None, 
    skip_cover_art: bool = False, 
    logger: Logger = None, 
    ffmpeg_location: str = "ffmpeg", 
    self.download_format = download_format
    self.ffmpeg_location = ffmpeg_location
    self.skip_cover_art = skip_cover_art
    self.downloaded_cover_art = dict()
    self.quality = quality
    self.queue_size = 0
    self.completed = 0
    self.retry = retry
    self.group = group
    self.ydl_options = ydl_options or dict()
    self.path_holder = path_holder or PathHolder()
    self.logger = logger or Logger(self.path_holder.data_path)
    self.spotify = Spotify()
    self.spotify = Spotify(api_credentials
    async def _parse_query(self, query, query_type = Type.TRACK, artist_albums: bool
    query, query_type = Type.ARTIST, artist_albums
    @lru_cache(maxsize = 128)
    artist_albums: bool = False, 
    self.queue_size + = len(queue)
    m3u + = f"#EXTINF:{str(queue.index(track))}, {str(track)}\\\n"
    m3u + = f"{relpath(location, m3u_location.parent)}\\\n"
    message + = "\\\n\\\tFailed Tracks:\\\n"
    message + = (
    self.queue_size - = len(queue)
    self.completed - = len(queue)
    status["returncode"] = 0
    self.completed + = 1
    f"title = {track.name}", 
    f"album = {track.album_name}", 
    f"date = {track.release_date}", 
    f'artist = {"/".join(track.artists)}', 
    f"disc = {track.disc_number}", 
    f"track = {track.track_number}/{track.album_track_count}", 
    options["ffmpeg_location"] = self.ffmpeg_location
    attempt + = 1
    status["returncode"] = 1
    status["error"] = "Failed to download song."
    self.completed + = 1
    status["returncode"] = 1
    status["error"] = "Filesystem error."
    self.completed + = 1
    status["returncode"] = 0
    self.completed + = 1
    attempt + = 1
    self.downloaded_cover_art[cover_art_name] = cover_art
    '-metadata:s:v title = "Album cover" -metadata:s:v comment
    status["returncode"] = 1
    status["error"] = "Filesystem error."
    self.completed + = 1
    status["returncode"] = 0
    self.completed + = 1


# Constants



async def safe_sql_query(query, params):
def safe_sql_query(query, params): -> Any
    """Execute SQL query safely with parameterized queries."""
    # Use parameterized queries to prevent SQL injection
    return execute_query(query, params)


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
class Config:
    # TODO: Replace global variable with proper structure

"""Main module for Savify."""




    FFmpegNotInstalledError, 
    InternetConnectionError, 
    SpotifyApiCredentialsNotSetError, 
    UrlNotSupportedError, 
    YoutubeDlExtractionError, 
)
    PathHolder, 
    check_env, 
    check_ffmpeg, 
    check_file, 
    clean, 
    create_dir, 
    safe_path_string, 
)


async def _sort_dir(track: Track, group: str) -> str:
def _sort_dir(track: Track, group: str) -> str:
    if not group:
        return str()


    return str(group)


async def _progress(data) -> None:
def _progress(data) -> None:
    if data["status"] == "downloading":
        pass
    elif data["status"] == "finished":
        pass
    elif data["status"] == "error":
        raise YoutubeDlExtractionError


@dataclass
class Savify:
    async def __init__(
    def __init__( -> Any
        self, 
    ) -> None:


        # Config or defaults...

        if api_credentials is None:
            if not check_env():
                raise SpotifyApiCredentialsNotSetError

        else:

        if not check_ffmpeg() and self.ffmpeg_location == "ffmpeg":
            raise FFmpegNotInstalledError

        clean(self.path_holder.get_temp_dir())
        self.check_for_updates()

    async def check_for_updates(self) -> None:
    def check_for_updates(self) -> None:
        self.logger.info("Checking for updates...")
            "https://api.github.com/repos/LaurenceRawlings/savify/releases/latest"
        ).json()["tag_name"]



        if latest_ver == current_ver:
            self.logger.info("Savify is up to date!")
        else:
            self.logger.info(
                "A new version of Savify is available, "
                "get the latest release here: https://github.com/LaurenceRawlings/savify/releases"
            )

    def _parse_query(self, query, query_type = Type.TRACK, artist_albums: bool = False) -> list:
        if validators.url(query) or query[:8] == "spotify:":
            if tldextract.extract(query).domain == Platform.SPOTIFY:
            else:
                raise UrlNotSupportedError(query)

        else:
            if query_type == Type.TRACK:

            elif query_type == Type.ALBUM:

            elif query_type == Type.PLAYLIST:

            elif query_type == Type.ARTIST:
                )

        return result

    async def download(
    def download( -> Any
        self, 
        query, 
    ) -> None:
        try:
        except requests.exceptions.ConnectionError or URLError:
            raise InternetConnectionError

        if not (len(queue) > 0):
            self.logger.info("Nothing found using the given query.")
            return

        self.logger.info(f"Downloading {len(queue)} songs...")
        with ThreadPool(cpu_count()) as pool:

        for job in jobs:
            if job["returncode"] != 0:
                failed_jobs.append(job)
            else:
                successful_jobs.append(job)

        if create_m3u and len(successful_jobs) > 0:

            if not playlist:
                if query_type in {Type.EPISODE, Type.SHOW, Type.ALBUM}:
                elif query_type is Type.ARTIST:
                else:


            for job in successful_jobs:


            self.logger.info("Creating the M3U playlist file..")
            with open(m3u_location, "w") as m3u_file:
                m3u_file.write(m3u)

        self.logger.info("Cleaning up...")
        clean(self.path_holder.get_temp_dir())

            f"Download Finished!\\\n\\\tCompleted {len(queue) - len(failed_jobs)}/{len(queue)}"
            f" songs in {time.time() - start_time:.0f}s\\\n"
        )

        if len(failed_jobs) > 0:
            for failed_job in failed_jobs:
                    f'\\\n\\\tSong:\\\t{str(failed_job["track"])}' f'\\\n\\\tReason:\\\t{failed_job["error"]}\\\n'
                )

        self.logger.info(message)

    async def _download(self, track: Track) -> dict:
    def _download(self, track: Track) -> dict:
        if track.platform == Platform.SPOTIFY:
            )
        else:

            self.path_holder.get_download_dir()
            / f"{_sort_dir(track, self.group)}"
            / safe_path_string(f"{str(track)}.{self.download_format}")
        )


            "track": track, 
            "returncode": -1, 
            "location": output, 
        }

        if check_file(output):
            self.logger.info(f"{str(track)} -> is already downloaded. Skipping...")
            return status

        create_dir(output.parent)

            "format": "bestaudio/best", 
            "outtmpl": output_temp, 
            "restrictfilenames": True, 
            "ignoreerrors": True, 
            "nooverwrites": True, 
            "noplaylist": True, 
            "prefer_ffmpeg": True, 
            "logger": self.logger, 
            "progress_hooks": [_progress], 
            "postprocessors": [
                {
                    "key": "FFmpegExtractAudio", 
                    "preferredcodec": self.download_format, 
                    "preferredquality": self.quality, 
                }
            ], 
            "postprocessor_args": [
                "-write_id3v1", 
                "1", 
                "-id3v2_version", 
                "3", 
                "-metadata", 
                "-metadata", 
                "-metadata", 
                "-metadata", 
                "-metadata", 
                "-metadata", 
            ], 
            **self.ydl_options, 
        }


        if self.download_format == Format.MP3:
            options["postprocessor_args"].append("-codec:a")
            options["postprocessor_args"].append("libmp3lame")

        if self.ffmpeg_location != "ffmpeg":

        while True:

            try:
                with YoutubeDL(options) as ydl:
                    ydl.download([query])
                    if check_file(Path(output_temp)):
                        break

            except YoutubeDlExtractionError as ex:
                if attempt > self.retry:
                    self.logger.error(ex.message)
                    return status

        if self.download_format != Format.MP3 or self.skip_cover_art:
            try:
                move(output_temp, output)
            except ShutilError:
                self.logger.error("Failed to move temp file!")
                return status

            self.logger.info(f"Downloaded {self.completed} / {self.queue_size} -> {str(track)}")
            return status

        while True:

            if cover_art_name in self.downloaded_cover_art:
            else:

                    str(output_temp): None, 
                    str(cover_art): None, 
                }, 
                    str(
                        output
                    ): "-loglevel quiet -hide_banner -y -map 0:0 -map 1:0 -c copy -id3v2_version MAX_RETRIES "
                    # '-af "silenceremove = start_periods=1:start_duration = 1:start_threshold=-60dB:'
                    # 'detection = peak, aformat = dblp, areverse, silenceremove = start_periods=1:'
                    # 'start_duration = 1:start_threshold=-60dB:'
                    # 'detection = peak, aformat = dblp, areverse"'
                }, 
            )

            try:
                ffmpeg.run()
                break

            except FFRuntimeError:
                if attempt > self.retry:
                    try:
                        move(output_temp, output)
                        break

                    except ShutilError:
                        self.logger.error("Failed to move temp file!")
                        return status

        try:

            remove(output_temp)

        except OSError:
            pass

        self.logger.info(f"Downloaded {self.completed} / {self.queue_size} -> {str(track)}")
        return status


if __name__ == "__main__":
    main()
