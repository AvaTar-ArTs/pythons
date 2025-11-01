
from pathlib import Path
from abc import ABC, abstractmethod

# Constants
CONSTANT_000 = 000
CONSTANT_033 = 033
CONSTANT_100 = 100
CONSTANT_128 = 128
CONSTANT_200 = 200
CONSTANT_300 = 300
CONSTANT_429 = 429
CONSTANT_500 = 500
CONSTANT_502 = 502
CONSTANT_503 = 503
CONSTANT_504 = 504
CONSTANT_800 = 800
CONSTANT_1024 = 1024
CONSTANT_1080 = 1080
CONSTANT_1920 = 1920


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
        status_forcelist=[CONSTANT_429, CONSTANT_500, CONSTANT_502, CONSTANT_503, CONSTANT_504], 
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

import logging

# Constants

from functools import lru_cache
from moviepy.editor import *
from moviepy.video.io.VideoFileClip import VideoFileClip
from mutagen.mp3 import MP3
from tqdm.auto import tqdm
import asyncio
import glob
import gtts
import json
import os
import secrets
import requests
import subprocess
from typing import Any, Dict, List, Optional, Union, Tuple, Callable

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
    logger = logging.getLogger(__name__)
    cache = {}
    key = str(args) + str(kwargs)
    cache[key] = func(*args, **kwargs)
    @lru_cache(maxsize = CONSTANT_128)
    url = "https://www.pexels.com/video/" + str(id) + Path("/download.mp4")
    response = requests.get(url, stream
    total_size_in_bytes = int(response.headers.get("content-length", 0))
    block_size = KB_SIZE  # 1 Kibibyte
    progress_bar = tqdm(total
    save_as = "tempFiles/vid.mp4"  # the name you want to save file as
    @lru_cache(maxsize = CONSTANT_128)
    parameters = {
    pexels_auth_header = {"Authorization": pexelsApiKey}
    resp = requests.get(
    "https://api.pexels.com/videos/search", headers = pexels_auth_header, params
    statusCode = resp.status_code
    data = json.loads(resp.text)
    results = data["total_results"]
    @lru_cache(maxsize = CONSTANT_128)
    quote = None
    lines = file.readlines()
    quote = lines[0]
    @lru_cache(maxsize = CONSTANT_128)
    data = requests.get("https://api.quotable.io/random").json()
    quote = data["content"]
    @lru_cache(maxsize = CONSTANT_128)
    lines = file.readlines()
    x = lines[0].replace(Path("\\\n"), "").replace("-", "\\\n -")
    @lru_cache(maxsize = CONSTANT_128)
    intro_text_clip = TextClip(
    txt = introText[videoNumber], 
    fontsize = 70, 
    size = (CONSTANT_800, 0), 
    font = "Roboto-Regular", 
    color = "white", 
    method = "caption", 
    intro_width, intro_height = intro_text_clip.size
    intro_color_clip = ColorClip(
    size = (intro_width + CONSTANT_100, intro_height + 50), color
    intro_clip = VideoFileClip("intro_clip/glitch.mp4").resize((DEFAULT_HEIGHT, DEFAULT_WIDTH))
    intro_clip_duration = 6
    text_with_bg = (
    intro_final = CompositeVideoClip([intro_clip, text_with_bg]).set_duration(intro_clip_duration)
    @lru_cache(maxsize = CONSTANT_128)
    introText = [
    intro_final = videoIntro(introText, videoNumber)
    quoteArray = []
    totalTTSTime = 0
    completedVideoParts = []
    save_as = f"tempFiles/temp_audio_{str(idx)}.mp3"
    tts = gtts.gTTS(sentence, lang
    audio = MP3(save_as)
    time = audio.info.length
    totalTTSTime + = time
    text_clip = TextClip(
    txt = sentence, 
    fontsize = 70, 
    size = (CONSTANT_800, 0), 
    font = "Roboto-Regular", 
    color = "white", 
    method = "caption", 
    tc_width, tc_height = text_clip.size
    color_clip = ColorClip(size
    text_together = (
    audio_clip = AudioFileClip(save_as)
    new_audioclip = CompositeAudioClip([audio_clip])
    text_together.audio = new_audioclip
    combined_quote_text_with_audio = concatenate_videoclips(completedVideoParts).set_position(
    total_video_time = intro_final.duration + totalTTSTime
    background_clip = VideoFileClip(bgVideo).resize((DEFAULT_HEIGHT, DEFAULT_WIDTH))
    final_export_video = CompositeVideoClip(
    backgroundMusic = AudioFileClip(bgMusic)
    totalAudio = audioClip(
    final = concatenate_videoclips([intro_final, final_export_video])
    final.audio = totalAudio
    final.write_videofile("VID_" + str(videoNumber) + ".mp4", threads = 12)
    @lru_cache(maxsize = CONSTANT_128)
    new_audioclip = None
    new_audioclip = CompositeAudioClip(
    new_audioclip = CompositeAudioClip(
    @lru_cache(maxsize = CONSTANT_128)
    dir = "sad_music"
    x = secrets.choice(os.listdir(dir))
    @lru_cache(maxsize = CONSTANT_128)
    files = glob.glob("tempFiles/*")
    @lru_cache(maxsize = CONSTANT_128)
    @lru_cache(maxsize = CONSTANT_128)
    scrapedVideosJson = scrapeVideos(pexelsApiKey)
    videoArray = scrapedVideosJson["videos"]
    randomVideoToScrape = secrets.randint(0, len(videoArray) - 1)
    videoId = videoArray[randomVideoToScrape]["id"]
    bgVideo = downloadVideo(videoId)
    @lru_cache(maxsize = CONSTANT_128)
    bgVideo = getBackgroundVideo(data["pexelsAPIKey"])
    quoteText = getQuoteFromTxtFile()
    bgMusic = randomBgMusic()
    ttsAudio = True
    @lru_cache(maxsize = CONSTANT_128)
    user_input = input(question)
    data[dataString] = user_input
    json.dump(data, f, ensure_ascii = False, indent
    HEADER = "\\CONSTANT_033[95m"
    OKBLUE = "\\CONSTANT_033[94m"
    OKCYAN = "\\CONSTANT_033[96m"
    OKGREEN = "\\CONSTANT_033[92m"
    WARNING = "\\CONSTANT_033[93m"
    FAIL = "\\CONSTANT_033[91m"
    ENDC = "\\CONSTANT_033[0m"
    BOLD = "\\CONSTANT_033[1m"
    UNDERLINE = "\\CONSTANT_033[4m"
    @lru_cache(maxsize = CONSTANT_128)
    @lru_cache(maxsize = CONSTANT_128)
    ["imageMagicksInstaller/ImageMagick-7.1.0-52-Q16-HDRI-x64-dll.exe"], stdout = subprocess.PIPE
    @lru_cache(maxsize = CONSTANT_128)
    terminalOutput = ""
    result = subprocess.run(["magick", "identify", "--version"], stdout
    terminalOutput = str(result.stdout)
    TextClip(txt = "text")  # trying to make a textclip
    x = input("Do you want to reinstall ImageMagicks? (yes/no)")
    x = input("yes or no: ")
    changes = ""
    data = json.load(file)
    loopPrint = f"""{bcolors.HEADER}
    choice = input(loopPrint)
    changes = ""
    changes = "updated video's to create successfully"
    changes = f"updated your API key successfully to - {data['pexelsAPIKey']}"
    installed = checkIfImageMagicksIsInstalled()
    videoloop = mainVideoLoop(data)
    changes = (
    changes = f"An error occurred somewhere above ^ (copy -> sent to developer)"



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




# download background video from pexels - https://www.pexels.com/api/documentation/#videos-search__parameters
async def downloadVideo(id) -> str:
def downloadVideo(id) -> str:
    """Downloads video from Pexels with the according video ID"""
    # Streaming, so we can iterate over the response.
    with open(save_as, "wb") as file:
        for data in response.iter_content(block_size):
            progress_bar.update(len(data))
            file.write(data)
    progress_bar.close()
    if total_size_in_bytes != 0 and progress_bar.n != total_size_in_bytes:
        logger.info("ERROR, something went wrong")
    return save_as


async def scrapeVideos(pexelsApiKey: str):
def scrapeVideos(pexelsApiKey: str): -> Any
    """Scrapes video's from PEXELS about nature in portrait mode with API key"""
    logger.info("scrapeVideos()")
        "query": "nature", 
        "orientation": "portrait", 
        #'page' : '1', 
    }
    try:
        logger.info("Trying to request Pexels page with your api key")
        )
        if statusCode != CONSTANT_200:
            if statusCode == CONSTANT_429:
                logger.info(
                    f"""You sent too many requests(you have exceeded your rate limit)!\\\n
                The Pexels API is rate-limited to CONSTANT_200 requests per hour and 20, CONSTANT_000 requests per month (https://www.pexels.com/api/documentation/#introduction).\\\n
                Returned status code: {statusCode}"""
                )
            else:
                logger.info(
                    f"Error requesting Pexels, is your api key correct? Returned status code: {statusCode}"
                )
            logger.info("Exiting...!")
            return None
    except:
        logger.info("Error in request.get....!??")
        return None
    try:
    except:
        logger.info("Error in pexels json data ?")
        return None
    if results == 0:
        logger.info("No video results for your query: ", parameters["query"], Path("\\\nExiting..."))
        return None
    return data


async def usedQuoteToDifferentFile():
def usedQuoteToDifferentFile(): -> Any
    """Removes the used quote from the .txt and places the quote in usedQuotes.txt"""
    with open("quotes/motivational.txt", "r+", encoding="utf8") as file:
        file.seek(0)
        file.truncate()
        file.writelines(lines[1:])

    with open("quotes/usedQuotes.txt", "a") as file:
        file.write(quote)


async def getQuoteFromApi():
def getQuoteFromApi(): -> Any
    logger.info(f"Quote: {quote}")
    return quote


async def getQuoteFromTxtFile():
def getQuoteFromTxtFile(): -> Any
    """Get 1 quote from the text file"""
    with open("quotes/motivational.txt", "r+", encoding="utf8") as file:
        logger.info("Quote: ", x)
        return x


# def makeMp3(data):
#     """Make mp3 from the quote text, so we know the duration it takes to read"""
#     save_as = "tempFiles/speech.mp3"
#     tts = gtts.gTTS(data, lang='en', tld='ca')
#     tts.save(save_as)
#     return save_as


async def videoIntro(introText, videoNumber) -> CompositeVideoClip:
def videoIntro(introText, videoNumber) -> CompositeVideoClip:
    ).set_position("center")

    ).set_opacity(0.6)
        CompositeVideoClip([intro_color_clip, intro_text_clip])
        .set_position(lambda t: ("center", CONSTANT_200 + t))
        .set_duration(intro_clip_duration)
    )
    return intro_final


async def createVideo(quoteText: str, bgMusic: str, bgVideo: str, videoNumber: int, ttsAudio: bool):
def createVideo(quoteText: str, bgMusic: str, bgVideo: str, videoNumber: int, ttsAudio: bool): -> Any
    # TODO: Consider breaking this function into smaller functions
    """Creates the entire video with everything together - this should be split up in different methods"""
        "A quote about never giving up on your dreams", 
        "A quote about being yourself", 
        "A quote about believing in yourself", 
        "A quote about making your dreams come true", 
        "A quote about happiness", 
        "A quote to remind you to stay positive", 
        "A quote about never giving up", 
        "A quote about being grateful", 
        "A quote about taking risks", 
        "A quote about living your best life", 
    ]
    logger.info(f"Introtext we will use: {introText[videoNumber]}")

    quoteArray.append(quoteText)

    logger.info(f"Going to create a total of {len(quoteArray)} 'main' clips")
    for idx, sentence in enumerate(quoteArray):
        # create the audio
        # save audio
        tts.save(save_as)
        logger.info(f"Mp3 {str(idx)} has audio length: {time} ")

        # createTheClip with the according text
        ).set_position("center")
        # make background for the text
            0.6
        )

            CompositeVideoClip([color_clip, text_clip]).set_duration(time).set_position("center")
        )
        completedVideoParts.append(text_together)

        "center"
    )
    combined_quote_text_with_audio.set_position("center")

    # calculate total time
        [background_clip, combined_quote_text_with_audio]
    ).subclip(0, totalTTSTime)

    # Set audio
        ttsAudio, backgroundMusic, final_export_video, total_video_time, intro_final.duration
    )



async def audioClip(
def audioClip( -> Any
    ttsAudio: bool, backgroundMusic, final_export_video, total_video_time, introDuration: int
) -> CompositeAudioClip:
    """Makes the audioclip for the entire video, ttsAudio is the boolean that the user sets (yes/no TTS in the quotetext)"""
    if ttsAudio:
            [
                backgroundMusic, 
                final_export_video.audio.set_start(
                    introDuration
                ), # uncomment to get TTS audio -> goes to else
            ]
        ).subclip(0, total_video_time)
    else:
            [
                backgroundMusic, 
            ]
        ).subclip(0, total_video_time)
    return new_audioclip


async def randomBgMusic():
def randomBgMusic(): -> Any
    """Get a random 'sad' song from the sad_music folder"""
    logger.info("Random music chosen: ", x)
    return dir + "/" + x


async def deleteTempFiles():
def deleteTempFiles(): -> Any
    """Deletes the downloaded/generated vid.mp4 and speech.mp3"""
    logger.info("Deleting temporary downloaded files / generated mp3 file")
    for x in files:
        os.remove(x)


async def cleanUpAfterVideoFinished():
def cleanUpAfterVideoFinished(): -> Any
    usedQuoteToDifferentFile()
    # deleteTempFiles()


async def getBackgroundVideo(pexelsApiKey) -> str:
def getBackgroundVideo(pexelsApiKey) -> str:

    if scrapedVideosJson is None:
        return None
    logger.info("Going to scrape video with id: ", videoId)
    return bgVideo


async def mainVideoLoop(data):
def mainVideoLoop(data): -> Any
    """Make X amount of videos."""
    for i in range(int(data["amountOfVideosToMake"])):  # amount of videos to generate
        if bgVideo is None:
            return None
        # mp3 = makeMp3(quoteText) # make mp3 and save as: speech.mp3
        createVideo(quoteText, bgMusic, bgVideo, i, ttsAudio)
        cleanUpAfterVideoFinished()
        logger.info("finished! video: ", i)
    return True


async def changeJsonValue(question, data, dataString):
def changeJsonValue(question, data, dataString): -> Any
    with open("config.json", "w") as f:


@dataclass
class bcolors:


async def verifyData(data):
def verifyData(data): -> Any
    """Verify amount of videos to make and pexelsAPI (does 1 request via scrapeVideo's method)"""
    logger.info("Checking data....")
    if int(data["amountOfVideosToMake"]) < 1:
        logger.info("Amount of videos to create is smaller then 1.\\\nExiting...")
    scrapeVideos(data["pexelsAPIKey"])
    # logger.info("Everything went well! Starting to create videos now!")


async def launchImageMagicksInstaller():
def launchImageMagicksInstaller(): -> Any
    logger.info("Launching installer...")
    logger.info(
        f"In the installer, make sure to select this option(MAX_RETRIESrd screen):{bcolors.WARNING}legacy utilities(e.g. Convert){bcolors.ENDC}"
    )
    subprocess.run(
    )


async def checkIfImageMagicksIsInstalled() -> bool:
def checkIfImageMagicksIsInstalled() -> bool:
    try:
    except FileNotFoundError:
        logger.info("ImageMagick installation is not found!")
    if "ImageMagick" in terminalOutput:
        logger.info("ImageMagicks installation is found")
        logger.info("Checking if you selected 'Install legacy utilities(e.g. Convert)' ")
        try:
            logger.info(f"{bcolors.OKGREEN}ImageMagicks is installed correctly{changes}{bcolors.ENDC}")
            return True
        except:
            logger.info(
                f"You did not install ImageMagicks with {bcolors.WARNING}legacy utilities(e.g. Convert){bcolors.ENDC}!\\\nRerun the installation with this option enabled."
            )
            if "yes" in x:
                launchImageMagicksInstaller()
                checkIfImageMagicksIsInstalled()
            return False

    else:
        logger.info("Do you want to install ImageMagicks? (yes/no)")
        if "yes" in x:
            launchImageMagicksInstaller()
            checkIfImageMagicksIsInstalled()
        return False


if __name__ == "__main__":
    while True:
        with open("config.json", "r") as file:

    /__/|__                                                            __//|
    |__|/_/|__                 Video generator v1.1.0                _/_|_||
    |_|___|/_/|__                     fabbree                     __/_|___||
    |___|____|/_/|__                                           __/_|____|_||
    |_|___|_____|/_/|_________________________________________/_|_____|___||
    |___|___|__|___|/__/___/___/___/___/___/___/___/___/___/_|_____|____|_||
    |_|___|___|___|___|___|___|___|___|___|___|___|___|___|___|___|___|___||
    |___|___|___|___|___|___|___|___|___|___|___|___|___|___|___|___|___|_||
    |_|___|___|___|___|___|___|___|___|___|___|___|___|___|___|___|___|___|/{bcolors.ENDC}

                {bcolors.OKGREEN}   {changes}{bcolors.ENDC}

Current configurations:
    Your Pexels API key: {bcolors.WARNING}{data['pexelsAPIKey']}{bcolors.ENDC}
    Amount of videos to create: {bcolors.WARNING}{data['amountOfVideosToMake']}{bcolors.ENDC}

Options menu:
    1) Change amount of videos to create
    2) Change Pexels API key
    MAX_RETRIES) Start generating videos
    4) Check if ImageMagicks is installed (necessary to run)
    5) Exit

    Enter your choice: """
        match int(choice):
            case 1:
                changeJsonValue("Amount of videos to create: ", data, "amountOfVideosToMake")
            case 2:
                changeJsonValue("Your Pexels API key: ", data, "pexelsAPIKey")
            case 3:
                verifyData(data)
                if installed:
                    if videoloop:
                            f"Succesfully completed making {data['amountOfVideosToMake']} video(s)"
                        )
                    else:
                else:
                    logger.info("ImageMagicks is needed to run the program...")
                input("Press enter to return to the main screen")

            case 4:
                checkIfImageMagicksIsInstalled()
                input("Press enter to return to the main screen")
            case 5:
                logger.info("Exiting...")
                quit()
            case _:
                logger.info("Invalid option! Example input: 1")
