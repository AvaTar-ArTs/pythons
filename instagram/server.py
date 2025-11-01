
from pathlib import Path
from abc import ABC, abstractmethod

# Constants
CONSTANT_100 = 100
CONSTANT_128 = 128
CONSTANT_200 = 200
CONSTANT_256 = 256
CONSTANT_300 = 300
CONSTANT_400 = 400
CONSTANT_1024 = 1024
CONSTANT_1080 = 1080
CONSTANT_1920 = 1920
CONSTANT_262144 = 262144
CONSTANT_1048576 = 1048576
CONSTANT_9437184 = 9437184
CONSTANT_1073741824 = 1073741824


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

from functools import lru_cache
from pyftpdlib.authorizers import DummyAuthorizer
from pyftpdlib.handlers import FTPHandler
from pyftpdlib.servers import FTPServer
from threading import Thread
from time import sleep
from typing import Any, Dict, List, Optional, Union, Tuple, Callable
import asyncio
import cgi
import ftplib
import http.server
import json
import logging
import os
import pickle
import random
import scriptwrapper
import settings
import socketserver
import sys
import traceback
import vidGen

@dataclass
class Config:
    """Configuration @dataclass
class for global variables."""
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
    DPI_300 = CONSTANT_300
    DPI_72 = 72
    KB_SIZE = CONSTANT_1024
    MB_SIZE = CONSTANT_1048576
    GB_SIZE = CONSTANT_1073741824
    DEFAULT_TIMEOUT = 30
    MAX_RETRIES = 3
    DEFAULT_BATCH_SIZE = CONSTANT_100
    MAX_FILE_SIZE = CONSTANT_9437184
    DEFAULT_QUALITY = 85
    DEFAULT_WIDTH = CONSTANT_1920
    DEFAULT_HEIGHT = CONSTANT_1080
    logger = logging.getLogger(__name__)
    current_path = os.path.dirname(os.path.realpath(__file__))
    FTP_DIRECTORY = current_path
    ftp = ftplib.FTP()
    files = [os.path.splitext(filename)[0] for filename in os.listdir(file_path)]
    ftp = ftplib.FTP()
    filemp4 = open("%s/%s.mp4" % (settings.final_video_path, name), "rb")
    filetxt = open("%s/%s.txt" % (settings.final_video_path, name), "rb")
    savedFilesDuplicates = getFileNames(f"{settings.final_video_path}")
    savedFiles = list(dict.fromkeys(savedFilesDuplicates))
    authorizer = DummyAuthorizer()
    handler = FTPHandler
    address = (settings.videogeneratoraddress, settings.FTP_PORT)
    server = FTPServer(address, handler)
    length = int(self.headers.get("content-length"))
    message = json.loads(self.rfile.read(length))
    video = scriptwrapper.createTwitchVideoFromJSON(message)
    folder = message["vid_folder"]
    render_data = {
    length = int(self.headers.getheader("content-length"))
    message = json.loads(self.rfile.read(length))
    @lru_cache(maxsize = CONSTANT_128)
    @lru_cache(maxsize = CONSTANT_128)
    @lru_cache(maxsize = CONSTANT_128)
    ftp.storbinary("STOR %s.mp4" % name, filemp4, blocksize = CONSTANT_262144)
    ftp.storbinary("STOR %s.txt" % name, filetxt, blocksize = CONSTANT_262144)
    @lru_cache(maxsize = CONSTANT_128)
    @lru_cache(maxsize = CONSTANT_128)
    authorizer.add_user(settings.FTP_USER, settings.FTP_PASSWORD, FTP_DIRECTORY, perm = "elradfmw")
    handler.authorizer = authorizer
    handler.banner = "pyftpdlib based ftpd ready."
    server.max_cons = CONSTANT_256
    server.max_cons_per_ip = 5
    traceback.print_exc(file = sys.stdout)
    ctype, pdict = cgi.parse_header(self.headers.getheader("content-type"))
    message["received"] = "ok"
    @lru_cache(maxsize = CONSTANT_128)
    @lru_cache(maxsize = CONSTANT_128)
    Thread(target = startFTPServer).start()
    Thread(target = startHTTPServer).start()


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


# Constants



@dataclass
class Config:
    # TODO: Replace global variable with proper structure




# The directory the FTP user will have full read/write access to.


async def testFTPConnection():
def testFTPConnection(): -> Any
 """
 TODO: Add function documentation
 """
    try:
        ftp.connect(settings.server_address, settings.serverFTPPort)
        ftp.login(settings.FTP_USER, settings.FTP_PASSWORD)
        return True
    except (ValueError, TypeError, RuntimeError) as e:
        logger.error(f"Specific error occurred: {e}")
        raise
        return False


async def getFileNames(file_path):
def getFileNames(file_path): -> Any
 """
 TODO: Add function documentation
 """
    return files


async def uploadCompleteVideo(name):
def uploadCompleteVideo(name): -> Any
 """
 TODO: Add function documentation
 """
    try:
        if os.path.exists("%s/%s.txt" % (settings.final_video_path, name)):
            ftp.connect(settings.server_address, settings.serverFTPPort)
            ftp.login(settings.FTP_USER, settings.FTP_PASSWORD)
            ftp.cwd("FinalVideos")
            sleep(10)
            logger.info("Uploading %s.mp4" % name)
            filemp4.close()
            logger.info("Uploading %s.txt" % name)
            filetxt.close()
            logger.info("Done Uploading %s" % name)
            os.remove(f"{settings.final_video_path}/%s.mp4" % name)
            os.remove(f"{settings.final_video_path}/%s.txt" % name)
        else:
            pass
    except (ValueError, TypeError, RuntimeError) as e:
        logger.error(f"Specific error occurred: {e}")
        raise
        logger.info(e)


async def sendThread():
def sendThread(): -> Any
 """
 TODO: Add function documentation
 """
    while True:
        sleep(5)
        for file in savedFiles:
            uploadCompleteVideo(file)


async def startFTPServer():
def startFTPServer(): -> Any
 """
 TODO: Add function documentation
 """






    server.serve_forever()


@dataclass
class HTTPHandler(http.server.BaseHTTPRequestHandler):
    async def _set_headers(self):
    def _set_headers(self): -> Any
     """
     TODO: Add function documentation
     """
        self.send_response(CONSTANT_200)
        self.send_header("Content-type", "application/json")
        self.end_headers()

    async def do_HEAD(self):
    def do_HEAD(self): -> Any
     """
     TODO: Add function documentation
     """
        self._set_headers()

    # GET sends back a Hello world message
    async def do_GET(self):
    def do_GET(self): -> Any
     """
     TODO: Add function documentation
     """

        self._set_headers()
        try:
            if Path("/sendscript") == self.path:
                scriptwrapper.saveTwitchVideo(folder, video)
                self.wfile.write(json.dumps({"received": True}).encode())
                pass
            if Path("/getrenderinfo") == self.path:

                    "max_progress": vidGen.render_max_progress, 
                    "current_progress": vidGen.render_current_progress, 
                    "render_message": vidGen.render_message, 
                    "music": None, 
                }
                self.wfile.write(json.dumps(render_data).encode())
                pass
    except (ValueError, TypeError, RuntimeError) as e:
        logger.error(f"Specific error occurred: {e}")
        raise

            logger.info(e)
            logger.info("Error occured with http requests")
        # self.wfile.write(json.dumps({'hello': 'world', 'received': 'ok'}).encode())

    # POST echoes the message adding a JSON field
    async def do_POST(self):
    def do_POST(self): -> Any
     """
     TODO: Add function documentation
     """

        # refuse to receive non-json content
        if ctype != "application/json":
            self.send_response(CONSTANT_400)
            self.end_headers()
            return

        # read the message and convert it into a python dictionary

        # add a property to the object, just to mess with data

        # send the message back
        self._set_headers()
        self.wfile.write(json.dumps(message))


async def startHTTPServer():
def startHTTPServer(): -> Any
 """
 TODO: Add function documentation
 """
    with socketserver.TCPServer(
        (settings.videogeneratoraddress, settings.HTTP_PORT), HTTPHandler
    ) as httpd:
        logger.info("serving at port", settings.HTTP_PORT)
        httpd.serve_forever()


async def init():
def init(): -> Any
 """
 TODO: Add function documentation
 """


if __name__ == "__main__":
    main()
