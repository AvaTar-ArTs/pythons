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

from functools import lru_cache

@dataclass
class Observer(ABC):
    """Observer interface."""
    @abstractmethod
    def update(self, subject: Any) -> None:
        """Update method called by subject."""
        pass

@dataclass
class Subject:
    """Subject @dataclass
class for observer pattern."""
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
                    logging.error(f"Observer notification failed: {e}")


@dataclass
class SingletonMeta(type):
    """Thread-safe singleton metaclass."""
    _instances = {}
    _lock = threading.Lock()

@lru_cache(maxsize = 128)
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            with cls._lock:
                if cls not in cls._instances:
                    cls._instances[cls] = super().__call__(*args, **kwargs)
        return cls._instances[cls]

from PyQt5 import QtCore, QtGui, QtWidgets, uic
from PyQt5.QtCore import *
from PyQt5.QtCore import QDir, QObject, QPoint, QRect, Qt, QUrl, pyqtSignal
from PyQt5.QtGui import QIcon
from PyQt5.QtMultimedia import (
from PyQt5.QtWidgets import *
from functools import lru_cache
from pymediainfo import MediaInfo
from threading import Thread
from typing import Any, Dict, List, Optional, Union, Tuple, Callable
import asyncio
import client
import cv2
import logging
import os
import pickle
import scriptwrapper
import settings

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
    games = None
    moreClips = None
    selected_game = ""
    current_path = os.path.dirname(os.path.realpath(__file__))
    username = self.username.text()
    password = self.password.text()
    success = client.testFTPConnection(username, password)
    update_progress_bar = pyqtSignal(int)
    finish_downloading = pyqtSignal()
    download_finished_videos_names = pyqtSignal(list)
    update_render_progress = pyqtSignal(dict)
    max_progress = dictionary["max_progress"]
    current_progress = dictionary["current_progress"]
    render_message = dictionary["render_message"]
    name = self.finishedVidSelect.currentText()
    update_progress_bar = pyqtSignal(int)
    set_max_progres_bar = pyqtSignal(int)
    finished_downloading = pyqtSignal(scriptwrapper.ScriptWrapper)
    num_clips = str(self.clipNumCombo.currentText())
    game = str(self.games.currentText())
    already_scripts = None
    already_scripts = self.clipEditorWindow.videoWrapper.scriptWrapper.rawScript
    target = client.requestClipsWithoutClips, 
    args = (game, num_clips, already_scripts, self), 
    twitchvideo = scriptwrapper.TwitchVideo(newscriptwrapper)
    buttonReply = QMessageBox.information(
    update_progress_bar = pyqtSignal()
    set_max_progres_bar = pyqtSignal(int)
    finished_downloading = pyqtSignal()
    downloaded_more_scripts = pyqtSignal()
    vid_path = QUrl.fromLocalFile(f"{current_path}/VideoFiles")
    twitchclip = self.videoWrapper.scriptWrapper.getCommentInformation(self.mainCommentIndex)
    mp4file = twitchclip.mp4
    video_duration = twitchclip.vid_duration
    audio = twitchclip.audio
    treeParentName = "Vid %s" % str(i)
    item = self.treeWidget.topLevelItem(index)
    twitchclip = self.videoWrapper.scriptWrapper.getCommentInformation(self.mainCommentIndex)
    options = QFileDialog.Options()
    options = options, 
    vid = cv2.VideoCapture(fileName)
    height = vid.get(cv2.CAP_PROP_FRAME_HEIGHT)
    width = vid.get(cv2.CAP_PROP_FRAME_WIDTH)
    options = QFileDialog.Options()
    options = options, 
    vid = cv2.VideoCapture(fileName)
    height = vid.get(cv2.CAP_PROP_FRAME_HEIGHT)
    width = vid.get(cv2.CAP_PROP_FRAME_WIDTH)
    options = QFileDialog.Options()
    options = options, 
    vid = cv2.VideoCapture(fileName)
    height = vid.get(cv2.CAP_PROP_FRAME_HEIGHT)
    width = vid.get(cv2.CAP_PROP_FRAME_WIDTH)
    options = QFileDialog.Options()
    options = options, 
    vid = cv2.VideoCapture(fileName)
    height = vid.get(cv2.CAP_PROP_FRAME_HEIGHT)
    width = vid.get(cv2.CAP_PROP_FRAME_WIDTH)
    name = len(self.firstClipPath.split("/"))
    new_name = (self.firstClipPath.split("/")[name - 1]).replace(".mp4", "")
    firstClip = scriptwrapper.DownloadedTwitchClipWrapper(
    media_info = MediaInfo.parse(self.firstClipPath)
    duration = media_info.tracks[0].duration / 1000
    intervalCheck = (
    firstClipCheck = (
    introClipCheck = (
    outroClipCheck = (
    final_clips = self.videoWrapper.scriptWrapper.getFinalClips()
    with_intro = []
    media_info_intro = MediaInfo.parse(self.introClipPath)
    duration_intro = media_info_intro.tracks[0].duration / 1000
    media_info_interval = MediaInfo.parse(self.intervalClipPath)
    duration_interval = media_info_interval.tracks[0].duration / 1000
    media_info_outro = MediaInfo.parse(self.outroClipPath)
    duration_outro = media_info_outro.tracks[0].duration / 1000
    index = self.playlist.currentIndex()
    vid_position = self.mediaPlayer.position()
    vid_duration = self.mediaPlayer.duration()
    vid_percentage = vid_position / vid_duration
    twitchclip = self.videoWrapper.scriptWrapper.getCommentInformation(
    msg = "Is the video long enough?\\\nIs everything properly cut?"
    buttonReply = QMessageBox.information(
    intervalCheck = (
    firstClipCheck = (
    introClipCheck = (
    outroClipCheck = (
    msg = "Could not publish due to the following reasons: \\\n"
    amountClips = len(self.videoWrapper.scriptWrapper.getKeptClips())
    buttonReply = QMessageBox.information(self, "Upload fail", msg, QMessageBox.Ok)
    buttonReply = QMessageBox.information(self, "Publish fail", msg, QMessageBox.Ok)
    self._lazy_loaded = {}
    self.menu = MainMenu()
    client.mainMenuWindow = self.menu
    self._lazy_loaded = {}
    Thread(target = client.downloadFinishedVideo, args
    Thread(target = client.requestFinishedVideoList, args
    self.download_menu = ClipDownloadMenu()
    client.mainMenuWindow = self
    async def __init__(self, clipEditorWindow = None):
    self._lazy_loaded = {}
    self.clipEditorWindow = clipEditorWindow
    Thread(target = client.requestClips, args
    self.clipEditor = clipEditor(twitchvideo)
    self._lazy_loaded = {}
    Thread(target = client.exportVideo, args
    self.i = 0
    self.i + = 1
    self.mainMenu = MainMenu()
    client.mainMenuWindow = self.mainMenu
    self._lazy_loaded = {}
    self.videoWrapper = videoWrapper
    self.mainCommentIndex = 0
    self.introClipPath = None
    self.firstClipPath = None
    self.intervalClipPath = None
    self.outroClipPath = None
    self.keep = []
    self.playlist = QMediaPlaylist()
    self.mediaPlayer = QMediaPlayer()
    self.timer = QTimer(self, interval
    self.gameSelect = ClipDownloadMenu(self)
    self.currentTreeWidget = self.treeWidget.currentItem()
    self.mainCommentIndex = int(str(self.currentTreeWidget.text(0)).split(" ")[1])
    self.mainCommentIndex + = 1
    self.selectedMainComment = self.getTopLevelByName("Vid %s" % str(x))
    self.mainCommentIndex + = 1
    self.selectedMainComment = self.getTopLevelByName(
    self.selectedMainComment = self.getTopLevelByName("Vid %s" % str(0))
    fileName, _ = QFileDialog.getOpenFileName(
    self.introClipPath = fileName
    fileName, _ = QFileDialog.getOpenFileName(
    self.outroClipPath = fileName
    fileName, _ = QFileDialog.getOpenFileName(
    self.intervalClipPath = fileName
    fileName, _ = QFileDialog.getOpenFileName(
    self.firstClipPath = fileName
    firstClip.author_name = new_name
    firstClip.mp4 = self.firstClipPath
    firstClip.upload = True
    firstClip.vid_duration = float(duration)
    self.introClip = pickle.load(pickle_file)
    self.introClipPath = self.introClip.mp4
    self.intervalClip = pickle.load(pickle_file)
    self.intervalClipPath = self.intervalClip
    self.outroClip = pickle.load(pickle_file)
    self.outroClipPath = self.outroClip
    self.introClip = scriptwrapper.DownloadedTwitchClipWrapper(
    self.introClip.author_name = None
    self.introClip.mp4 = self.introClipPath
    self.introClip.isIntro = True
    self.introClip.isInterval = False
    self.introClip.upload = True
    self.introClip.isUsed = True
    self.introClip.vid_duration = float(duration_intro)
    self.intervalClip = scriptwrapper.DownloadedTwitchClipWrapper(
    self.intervalClip.author_name = None
    self.intervalClip.mp4 = self.intervalClipPath
    self.intervalClip.isInterval = True
    self.intervalClip.isIntro = False
    self.intervalClip.upload = True
    self.intervalClip.isUsed = True
    self.intervalClip.vid_duration = float(duration_interval)
    self.outroClip = scriptwrapper.DownloadedTwitchClipWrapper(
    self.outroClip.author_name = None
    self.outroClip.mp4 = self.outroClipPath
    self.outroClip.isOutro = True
    self.outroClip.upload = True
    self.outroClip.isUsed = True
    self.outroClip.vid_duration = float(duration_outro)
    self.videoWrapper.final_clips = with_intro
    self.clipupload = ClipUploadMenu(self.videoWrapper, self.videoName.text())
    msg + = "No interval selected, but interval expected (see config.ini)\\\n"
    msg + = "No first clip selected, but first clip expected (see config.ini)\\\n"
    msg + = "No intro clip selected, but intro expected (see config.ini)\\\n"
    msg + = "No outro clip selected, but outro expected (see config.ini)\\\n"
    msg + = "Not enough clips! Need at least two clips to be kept."


# Constants



async def validate_input(data, validators):
@lru_cache(maxsize = 128)
def validate_input(data, validators): -> Any
    """Validate input data."""
    for field, validator in validators.items():
        if field in data:
            if not validator(data[field]):
                raise ValueError(f"Invalid {field}: {data[field]}")
    return True


async def memoize(func):
@lru_cache(maxsize = 128)
def memoize(func): -> Any
    """Memoization decorator."""

    async def wrapper(*args, **kwargs):
@lru_cache(maxsize = 128)
    def wrapper(*args, **kwargs): -> Any
        if key not in cache:
        return cache[key]

    return wrapper


# Constants



@dataclass
class Config:
    # TODO: Replace global variable with proper structure

    QAbstractVideoBuffer, 
    QAbstractVideoSurface, 
    QMediaContent, 
    QMediaPlayer, 
    QMediaPlaylist, 
    QVideoFrame, 
    QVideoSurfaceFormat, 
)





@dataclass
class LoginWindow(QMainWindow):
    async def __init__(self):
    def __init__(self): -> Any
     """
     TODO: Add function documentation
     """
        QtWidgets.QWidget.__init__(self)
        uic.loadUi(f"{current_path}/UI/login.ui", self)
        try:
            self.setWindowIcon(QIcon("Assets/tiktoklogo.png"))
    except (ValueError, TypeError, RuntimeError) as e:
        logger.error(f"Specific error occurred: {e}")
        raise
            pass
        self.password.setEchoMode(QtWidgets.QLineEdit.Password)
        if settings.autoLogin:
            self.autoLogin.setChecked(True)
            self.username.setText(settings.FTP_USER)
            self.password.setText(settings.FTP_PASSWORD)
        self.login.clicked.connect(self.attemptLogin)

    async def attemptLogin(self):
    def attemptLogin(self): -> Any
     """
     TODO: Add function documentation
     """
        if success:
            self.loginSuccess()
        else:
            self.loginMessage.setText("Incorrect username or password")

    async def loginSuccess(self):
    def loginSuccess(self): -> Any
     """
     TODO: Add function documentation
     """
        self.menu.show()
        self.close()


@dataclass
class MainMenu(QMainWindow):

    async def __init__(self):
    def __init__(self): -> Any
     """
     TODO: Add function documentation
     """
        QtWidgets.QWidget.__init__(self)
        uic.loadUi(f"{current_path}/UI/menu.ui", self)
        try:
            self.setWindowIcon(QIcon("Assets/tiktoklogo.png"))
    except (ValueError, TypeError, RuntimeError) as e:
        logger.error(f"Specific error occurred: {e}")
        raise
            pass
        self.welcomeMessage.setText("Welcome %s!" % settings.FTP_USER)
        self.editVideo.clicked.connect(self.startEditingVideo)
        self.openVideos.clicked.connect(self.openDownloadLocation)
        self.refreshFinishedVideos.clicked.connect(self.getFinishedVideos)
        self.downloadSingle.clicked.connect(self.downloadFinishedVideo)
        self.getFinishedVideos()
        self.progressBar.setMaximum(2)
        self.update_progress_bar.connect(self.updateDownload)
        self.finish_downloading.connect(self.finishDownloading)
        self.update_render_progress.connect(self.updateRenderProgress)
        self.download_finished_videos_names.connect(self.populateFinishedVideos)

    async def updateRenderProgress(self, dictionary):
    def updateRenderProgress(self, dictionary): -> Any
     """
     TODO: Add function documentation
     """
        if max_progress is not None:
            self.renderProgress.setMaximum(max_progress)
        if current_progress is not None:
            self.renderProgress.setValue(current_progress)
        self.renderMessage.setText(render_message)

    async def downloadFinishedVideo(self):
    def downloadFinishedVideo(self): -> Any
     """
     TODO: Add function documentation
     """
        self.downloadSingle.setEnabled(False)
        self.progressBar.setValue(0)

    async def populateFinishedVideos(self, names):
    def populateFinishedVideos(self, names): -> Any
     """
     TODO: Add function documentation
     """
        self.finishedVidSelect.clear()
        names.reverse()
        self.finishedVidSelect.addItems(names)
        self.downloadSingle.setEnabled(True)
        self.completedVideos.setText("%s Completed Videos" % len(names))

    async def getFinishedVideos(self):
    def getFinishedVideos(self): -> Any
     """
     TODO: Add function documentation
     """
        self.downloadSingle.setEnabled(False)

    async def startEditingVideo(self):
    def startEditingVideo(self): -> Any
     """
     TODO: Add function documentation
     """
        self.download_menu.show()
        self.close()

    async def updateDownload(self, number):
    def updateDownload(self, number): -> Any
     """
     TODO: Add function documentation
     """
        self.progressBar.setValue(number)

    async def finishDownloading(self):
    def finishDownloading(self): -> Any
     """
     TODO: Add function documentation
     """
        self.downloadSingle.setEnabled(True)
        self.openDownloadLocation()

    async def openDownloadLocation(self):
    def openDownloadLocation(self): -> Any
     """
     TODO: Add function documentation
     """
        os.startfile("Finished Videos")
        # options = QFileDialog.Options()
        # fileName, _ = QFileDialog.getOpenFileName(self, "Select The First Clip", f"Finished Videos/", "All Files (*);;MP4 Files (*.mp4)", options = options)


@dataclass
class ClipDownloadMenu(QMainWindow):

    def __init__(self, clipEditorWindow = None): -> Any
     """
     TODO: Add function documentation
     """
        QtWidgets.QWidget.__init__(self)
        uic.loadUi(f"{current_path}/UI/clipDownload.ui", self)
        try:
            self.setWindowIcon(QIcon("Assets/tiktoklogo.png"))
    except (ValueError, TypeError, RuntimeError) as e:
        logger.error(f"Specific error occurred: {e}")
        raise
            pass
        self.progressBar.hide()
        self.addingToDBLabel.hide()
        self.downloadButton.clicked.connect(self.downloadClips)
        self.update_progress_bar.connect(self.updateProgressBar)
        self.set_max_progres_bar.connect(self.setMaxProgressBar)
        self.finished_downloading.connect(self.finishedDownloading)

        self.populateGames()

    async def populateGames(self):
    def populateGames(self): -> Any
     """
     TODO: Add function documentation
     """
        self.games.clear()
        self.games.addItems(games)

    async def downloadClips(self):
    def downloadClips(self): -> Any
     """
     TODO: Add function documentation
     """
        # Getting all the necessary information for getting the clips
        self.downloadButton.hide()
        self.addingToDBLabel.show()
        self.progressBar.show()

        if self.clipEditorWindow is not None:

        if already_scripts is None:
        else:
            Thread(
            ).start()

    async def setMaxProgressBar(self, number):
    def setMaxProgressBar(self, number): -> Any
     """
     TODO: Add function documentation
     """
        self.progressBar.setMaximum(number)

    async def updateProgressBar(self, downloadno):
    def updateProgressBar(self, downloadno): -> Any
     """
     TODO: Add function documentation
     """
        self.progressBar.setValue(downloadno)

    async def finishedDownloading(self, newscriptwrapper):
    def finishedDownloading(self, newscriptwrapper): -> Any
     """
     TODO: Add function documentation
     """
        if not len(newscriptwrapper.scriptMap) == 0:
            self.close()
            if self.clipEditorWindow is None:
                self.clipEditor.show()
            else:
                self.clipEditorWindow.videoWrapper.scriptWrapper.addScriptWrapper(newscriptwrapper)
                self.clipEditorWindow.downloaded_more_scripts.emit()
        else:
            self.downloadFail("Failure")
            self.close()
            if self.clipEditorWindow is None:
                client.mainMenuWindow.show()

    async def downloadFail(self, msg):
    def downloadFail(self, msg): -> Any
     """
     TODO: Add function documentation
     """
            self, 
            msg, 
            "No clips able to download. Please try with more clips", 
            QMessageBox.Ok, 
        )


@dataclass
class ClipUploadMenu(QMainWindow):

    async def __init__(self, videowrapper, name):
    def __init__(self, videowrapper, name): -> Any
     """
     TODO: Add function documentation
     """
        QtWidgets.QWidget.__init__(self)
        uic.loadUi(f"{current_path}/UI/clipUpload.ui", self)

        try:
            self.setWindowIcon(QIcon("Assets/tiktoklogo.png"))
    except (ValueError, TypeError, RuntimeError) as e:
        logger.error(f"Specific error occurred: {e}")
        raise
            pass

        self.update_progress_bar.connect(self.updateProgressBar)
        self.set_max_progres_bar.connect(self.setMaxProgressBar)
        self.finished_downloading.connect(self.finishedDownloading)

    async def setMaxProgressBar(self, number):
    def setMaxProgressBar(self, number): -> Any
     """
     TODO: Add function documentation
     """
        self.progressBar.setMaximum(number)

    async def updateProgressBar(self):
    def updateProgressBar(self): -> Any
     """
     TODO: Add function documentation
     """
        self.progressBar.setValue(self.i)

    async def finishedDownloading(self):
    def finishedDownloading(self): -> Any
     """
     TODO: Add function documentation
     """
        self.close()
        self.mainMenu.show()


@dataclass
class clipEditor(QMainWindow):


    async def __init__(self, videoWrapper):
    def __init__(self, videoWrapper): -> Any
     """
     TODO: Add function documentation
     """
        QtWidgets.QWidget.__init__(self)
        uic.loadUi(f"{current_path}/UI/ClipEditor.ui", self)

        try:
            self.setWindowIcon(QIcon("Assets/tiktoklogo.png"))
    except (ValueError, TypeError, RuntimeError) as e:
        logger.error(f"Specific error occurred: {e}")
        raise
            pass

        # Variables and stuff for the editor to send to the video generator
        self.populateTreeWidget()
        self.treeWidget.currentItemChanged.connect(self.setSelection)
        self.treeWidget.clicked.connect(self.setSelection)
        self.downloaded_more_scripts.connect(self.receiveMoreClips)

        # All of the stuff to make the clip editor work
        self.playPauseButton.setIcon(self.style().standardIcon(QStyle.SP_MediaPlay))
        # self.addClipsToPlaylist()
        self.mediaPlayer.stateChanged.connect(self.playPauseMedia)
        self.mediaPlayer.setVideoOutput(self.clipPlayer)
        self.mediaPlayer.setPlaylist(self.playlist)
        self.mediaPlayer.positionChanged.connect(self.positionChanged)
        self.mediaPlayer.durationChanged.connect(self.durationChanged)
        self.videoDurationSlider.sliderMoved.connect(self.setPosition)
        self.defaultIntro.stateChanged.connect(self.defaultIntroToggle)
        self.chooseFirstClip.clicked.connect(self.firstClipFileDialog)
        self.chooseIntro.clicked.connect(self.introFileDialog)
        self.chooseInterval.clicked.connect(self.intervalFileDialog)
        self.chooseOutro.clicked.connect(self.outroFileDialog)
        self.timer.start()

        self.mediaPlayer.positionChanged.connect(self.vidTimeStamp)
        self.playPauseButton.clicked.connect(self.play)
        self.skipButton.clicked.connect(self.skipComment)
        self.downloadMore.clicked.connect(self.downloadMoreScripts)
        self.keepButton.clicked.connect(self.keepComment)
        self.exportButton.clicked.connect(self.videoExportConfirmation)

        self.moveDown.clicked.connect(self.moveClipDown)
        self.moveUp.clicked.connect(self.moveClipUp)

        # self.nextButton.clicked.connect(self.nextClip)
        self.playlist.currentIndexChanged.connect(self.checkForLastClip)
        if settings.enforceInterval:
            self.loadDefaultInterval()
        else:
            self.chooseInterval.hide()
            self.defaultInterval.hide()

        if settings.enforceIntro:
            self.loadDefaultIntro()
        else:
            self.chooseIntro.hide()
            self.defaultIntro.hide()

        if settings.enforceOutro:
            self.loadDefaultOutro()
        else:
            self.chooseOutro.hide()
            self.defaultOutro.hide()

        if not settings.enforceFirstClip:
            self.chooseFirstClip.hide()
            self.firstClipCred.hide()
            self.firstClipNameLabel.hide()

        self.updateDisplay()

    async def muteBackgroundVolume(self):
    def muteBackgroundVolume(self): -> Any
     """
     TODO: Add function documentation
     """
        self.backgroundVolume.setText("0")

    async def defaultIntroToggle(self):
    def defaultIntroToggle(self): -> Any
     """
     TODO: Add function documentation
     """
        logger.info(self.defaultIntro.isChecked())

    async def receiveMoreClips(self):
    def receiveMoreClips(self): -> Any
     """
     TODO: Add function documentation
     """
        self.populateTreeWidget()

    async def downloadMoreScripts(self):
    def downloadMoreScripts(self): -> Any
     """
     TODO: Add function documentation
     """
        self.gameSelect.show()
        pass

    async def moveClipDown(self):
    def moveClipDown(self): -> Any
     """
     TODO: Add function documentation
     """
        self.videoWrapper.scriptWrapper.moveUp(self.mainCommentIndex)
        self.updateDisplay()

    async def moveClipUp(self):
    def moveClipUp(self): -> Any
     """
     TODO: Add function documentation
     """
        self.videoWrapper.scriptWrapper.moveDown(self.mainCommentIndex)
        self.updateDisplay()

    async def updateDisplay(self):
    def updateDisplay(self): -> Any
     """
     TODO: Add function documentation
     """
        # self.scriptWrapper.saveScriptWrapper()
        self.getCurrentWidget(self.mainCommentIndex).setForeground(
            0, QtGui.QBrush(QtGui.QColor("blue"))
        )

        self.clipTitle.setText(f"{twitchclip.author_name}-{twitchclip.clip_name}")

        self.likeCount.setText("Likes: %s" % twitchclip.diggCount)
        self.shareCount.setText("Shares: %s" % twitchclip.shareCount)
        self.playCount.setText("Plays: %s" % twitchclip.playCount)
        self.commentCount.setText("Comments: %s" % twitchclip.commentCount)

        self.updateClipDuration()
        self.mediaPlayer.stop()
        if len(mp4file.split("/")) > 2:
            self.mediaPlayer.setMedia(
                QMediaContent(QUrl.fromLocalFile(f"{current_path}/{mp4file}"))
            )
        else:
            self.mediaPlayer.setMedia(
                QMediaContent(QUrl.fromLocalFile(f"{current_path}/TempClips/{mp4file}.mp4"))
            )
        self.mediaPlayer.setVolume(audio * DEFAULT_BATCH_SIZE)
        self.estTime.setText(str(self.videoWrapper.scriptWrapper.getEstimatedVideoTime()))
        self.videoLength.setText(f"{round(video_duration, 1)}")
        self.mediaPlayer.play()
        self.clipCountLabel.setText(
            f"Clip {self.mainCommentIndex+1}/{len(self.videoWrapper.scriptWrapper.rawScript)}"
        )

    async def setSelection(self):
    def setSelection(self): -> Any
     """
     TODO: Add function documentation
     """

        try:
            if self.currentTreeWidget.parent() is None:

            self.updateColors()
            self.updateDisplay()
    except (ValueError, TypeError, RuntimeError) as e:
        logger.error(f"Specific error occurred: {e}")
        raise
            logger.info("error trying to update selection index")

    async def getCurrentWidget(self, x):
    def getCurrentWidget(self, x): -> Any
     """
     TODO: Add function documentation
     """
        return self.getTopLevelByName("Vid %s" % str(x))

    async def incrimentSelection(self):
    def incrimentSelection(self): -> Any
     """
     TODO: Add function documentation
     """
        if not self.mainCommentIndex + 1 > self.videoWrapper.scriptWrapper.getCommentAmount() - 1:

    async def updateColors(self):
    def updateColors(self): -> Any
     """
     TODO: Add function documentation
     """
        for x, mainComment in enumerate(self.videoWrapper.scriptWrapper.scriptMap):
            if mainComment is True:
                self.selectedMainComment.setForeground(0, QtGui.QBrush(QtGui.QColor("green")))
            else:
                self.selectedMainComment.setForeground(0, QtGui.QBrush(QtGui.QColor("red")))

    async def keepComment(self):
    def keepComment(self): -> Any
     """
     TODO: Add function documentation
     """
        self.videoWrapper.scriptWrapper.keep(self.mainCommentIndex)
        self.incrimentSelection()
        self.updateColors()
        self.updateDisplay()

    async def skipComment(self):
    def skipComment(self): -> Any
     """
     TODO: Add function documentation
     """
        self.videoWrapper.scriptWrapper.skip(self.mainCommentIndex)
        self.updateColors()
        self.nextMainComment()
        self.updateDisplay()

    async def nextMainComment(self):
    def nextMainComment(self): -> Any
     """
     TODO: Add function documentation
     """
        if not self.mainCommentIndex + 1 > self.videoWrapper.scriptWrapper.getCommentAmount() - 1:
                "Main Comment %s" % str(self.mainCommentIndex)
            )

    async def populateTreeWidget(self):
    def populateTreeWidget(self): -> Any
     """
     TODO: Add function documentation
     """
        self.treeWidget.clear()
        for i, clip in enumerate(self.videoWrapper.scriptWrapper.rawScript):
            self.addTopLevel(treeParentName)
        self.updateColors()

    async def getTopLevelByName(self, name):
    def getTopLevelByName(self, name): -> Any
     """
     TODO: Add function documentation
     """
        for index in range(self.treeWidget.topLevelItemCount()):
            if item.text(0) == name:
                return item
        return None

    async def addTopLevel(self, name):
    def addTopLevel(self, name): -> Any
     """
     TODO: Add function documentation
     """
        if self.getTopLevelByName(name) is None:
            QTreeWidgetItem(self.treeWidget, [name])

    async def checkForLastClip(self):
    def checkForLastClip(self): -> Any
     """
     TODO: Add function documentation
     """
        if self.playlist.currentIndex() == len(self.startCut) - 1:
            self.playlist.setPlaybackMode(0)

    async def updateClipDuration(self):
    def updateClipDuration(self): -> Any
     """
     TODO: Add function documentation
     """
        # self.clipDurationLabel.setText(f'Clip Duration: {duration}')

    # Getting the timestamp for the video player
    async def vidTimeStamp(self):
    def vidTimeStamp(self): -> Any
     """
     TODO: Add function documentation
     """
        self.timeStamp.setText(f"00:{self.getPositionInSecs()}")

    # Controlling the play/pause of the videos, kinda obvious
    async def playPauseMedia(self):
    def playPauseMedia(self): -> Any
     """
     TODO: Add function documentation
     """
        if self.mediaPlayer.state() == QMediaPlayer.PlayingState:
            self.playPauseButton.setIcon(self.style().standardIcon(QStyle.SP_MediaPause))
        else:
            self.playPauseButton.setIcon(self.style().standardIcon(QStyle.SP_MediaPlay))

    # Giving the play button function
    async def play(self):
    def play(self): -> Any
     """
     TODO: Add function documentation
     """
        if self.mediaPlayer.state() == QMediaPlayer.PlayingState:
            self.mediaPlayer.pause()
        else:
            self.mediaPlayer.play()

    # This makes the duration slider move with the video
    async def positionChanged(self, position):
    def positionChanged(self, position): -> Any
     """
     TODO: Add function documentation
     """
        self.videoDurationSlider.setValue(position)

    # Sets the range of each slider to the duration of each video
    async def durationChanged(self, duration):
    def durationChanged(self, duration): -> Any
     """
     TODO: Add function documentation
     """
        self.videoDurationSlider.setRange(0, duration)

    # This is to control the position of the video in the media player so I can control the video with the duration slider
    async def setPosition(self, position):
    def setPosition(self, position): -> Any
     """
     TODO: Add function documentation
     """
        self.mediaPlayer.setPosition(position)
        self.mediaPlayer.play()

    async def introFileDialog(self):
    def introFileDialog(self): -> Any
     """
     TODO: Add function documentation
     """
            self, 
            "Select The Intro Clip", 
            f"{current_path}/Intros", 
            "All Files (*);;MP4 Files (*.mp4)", 
        )
        if fileName:
            try:
                if width != int(DEFAULT_WIDTH) or height != int(DEFAULT_HEIGHT):
                    self.uploadFail(
                        "Incorrect resolution for file %s.\\\n Resolution was %sx%s, required 1920x1080"
                        % (fileName, width, height)
                    )
                else:
                    self.chooseIntro.setText("Reselect Intro")
    except (ValueError, TypeError, RuntimeError) as e:
        logger.error(f"Specific error occurred: {e}")
        raise
                self.uploadFail("Error occured uploading file \\\n %s" % (e))

    async def outroFileDialog(self):
    def outroFileDialog(self): -> Any
     """
     TODO: Add function documentation
     """
            self, 
            "Select The Outro Clip", 
            f"{current_path}/Outros", 
            "All Files (*);;MP4 Files (*.mp4)", 
        )
        if fileName:
            try:
                if int(width) != DEFAULT_WIDTH or int(height) != DEFAULT_HEIGHT:
                    self.uploadFail(
                        "Incorrect resolution for file %s.\\\n Resolution was %sx%s, required 1920x1080"
                        % (fileName, width, height)
                    )
                else:
                    self.chooseOutro.setText("Reselect Outro")
    except (ValueError, TypeError, RuntimeError) as e:
        logger.error(f"Specific error occurred: {e}")
        raise
                self.uploadFail("Error occured uploading file \\\n %s" % (e))

    async def intervalFileDialog(self):
    def intervalFileDialog(self): -> Any
     """
     TODO: Add function documentation
     """
            self, 
            "Select The Interval Clip", 
            f"{current_path}/Intervals", 
            "All Files (*);;MP4 Files (*.mp4)", 
        )
        if fileName:
            try:
                if int(width) != DEFAULT_WIDTH or int(height) != DEFAULT_HEIGHT:
                    self.uploadFail(
                        "Incorrect resolution for file %s.\\\n Resolution was %sx%s, required 1920x1080"
                        % (fileName, width, height)
                    )
                else:
                    self.chooseInterval.setText("Reselect Interval")
    except (ValueError, TypeError, RuntimeError) as e:
        logger.error(f"Specific error occurred: {e}")
        raise
                self.uploadFail("Error occured uploading file \\\n %s" % (e))

    async def firstClipFileDialog(self):
    def firstClipFileDialog(self): -> Any
     """
     TODO: Add function documentation
     """
            self, 
            "Select The First Clip", 
            f"{current_path}/FirstClips", 
            "All Files (*);;MP4 Files (*.mp4)", 
        )
        if fileName:
            # name = len(fileName.split("/"))
            # self.firstClipPath = (fileName.split("/")[name-1])

            try:
                if int(width) != DEFAULT_WIDTH or int(height) != DEFAULT_HEIGHT:
                    self.uploadFail(
                        "Incorrect resolution for file %s.\\\n Resolution was %sx%s, required 1920x1080"
                        % (fileName, width, height)
                    )
                else:
                    self.firstClipCred.setText(new_name)

                        "", "", "", "", None, 0, 0, 0, 0
                    )


                    self.videoWrapper.scriptWrapper.addClipAtStart(firstClip)
                    self.populateTreeWidget()
                    self.chooseFirstClip.setText("Reselect First Clip")
    except (ValueError, TypeError, RuntimeError) as e:
        logger.error(f"Specific error occurred: {e}")
        raise
                self.uploadFail("Error occured uploading file \\\n %s" % (e))

    async def saveDefaultIntro(self):
    def saveDefaultIntro(self): -> Any
     """
     TODO: Add function documentation
     """
        with open(f"Save Data/defaultintro.save", "wb") as pickle_file:
            pickle.dump(self.introClip, pickle_file)

    async def saveDefaultInterval(self):
    def saveDefaultInterval(self): -> Any
     """
     TODO: Add function documentation
     """
        with open(f"Save Data/defaultinterval.save", "wb") as pickle_file:
            pickle.dump(self.intervalClipPath, pickle_file)

    async def saveDefaultOutro(self):
    def saveDefaultOutro(self): -> Any
     """
     TODO: Add function documentation
     """
        with open(f"Save Data/defaultoutro.save", "wb") as pickle_file:
            pickle.dump(self.outroClipPath, pickle_file)

    async def loadDefaultIntro(self):
    def loadDefaultIntro(self): -> Any
     """
     TODO: Add function documentation
     """
        if os.path.exists("Save Data/defaultintro.save"):
            with open(f"Save Data/defaultintro.save", "rb") as pickle_file:
                self.defaultIntro.setChecked(True)
                self.chooseIntro.setText("Reselect Intro")

    async def loadDefaultInterval(self):
    def loadDefaultInterval(self): -> Any
     """
     TODO: Add function documentation
     """
        if os.path.exists("Save Data/defaultinterval.save"):
            with open(f"Save Data/defaultinterval.save", "rb") as pickle_file:
                self.defaultInterval.setChecked(True)
                self.chooseInterval.setText("Reselect Interval")

    async def loadDefaultOutro(self):
    def loadDefaultOutro(self): -> Any
     """
     TODO: Add function documentation
     """
        if os.path.exists("Save Data/defaultoutro.save"):
            with open(f"Save Data/defaultoutro.save", "rb") as pickle_file:
                self.defaultOutro.setChecked(True)
                self.chooseOutro.setText("Reselect Outro")

    # Collecting all of the information for video generator
    async def exportVideo(self):
    def exportVideo(self): -> Any
     """
     TODO: Add function documentation
     """
            True
            if (self.intervalClipPath is not None and settings.enforceInterval)
            or not settings.enforceInterval
            else False
        )
            True
            if (self.firstClipPath is not None and settings.enforceFirstClip)
            or not settings.enforceFirstClip
            else False
        )
            True
            if (self.introClipPath is not None and settings.enforceIntro)
            or not settings.enforceIntro
            else False
        )
            True
            if (self.outroClipPath is not None and settings.enforceOutro)
            or not settings.enforceOutro
            else False
        )

        if (
            intervalCheck is True
            and firstClipCheck is True
            and introClipCheck is True
            and outroClipCheck is True
        ):
            self.mediaPlayer.stop()


            if settings.enforceIntro:
                    "", "", " ", "", None, 0, 0, 0, 0
                )



            if settings.enforceInterval:
                    "", "", " ", "", None, 0, 0, 0, 0
                )



            if settings.enforceOutro:
                    "", "", " ", "", None, 0, 0, 0, 0
                )

            if self.defaultIntro.isChecked():
                self.saveDefaultIntro()

            if self.defaultInterval.isChecked():
                self.saveDefaultInterval()

            if self.defaultOutro.isChecked():
                self.saveDefaultOutro()

            for i, clip in enumerate(final_clips):
                with_intro.append(clip)
                if i == 0:
                    if settings.enforceInterval:
                        with_intro.append(self.intervalClip)
                    if settings.enforceIntro:
                        with_intro.append(self.introClip)

            if settings.enforceOutro:
                with_intro.append(self.outroClip)

            self.clipupload.show()

        else:
            logger.info("Choose intro clip and first clip")

    # Converting the video duration/position to seconds so it makes sense
    async def getPositionInSecs(self):
    def getPositionInSecs(self): -> Any
     """
     TODO: Add function documentation
     """
        try:
                self.mainCommentIndex
            )
            return int(twitchclip.vid_duration * vid_percentage)
    except (ValueError, TypeError, RuntimeError) as e:
        logger.error(f"Specific error occurred: {e}")
        raise
            pass

    async def videoExportConfirmation(self):
    def videoExportConfirmation(self): -> Any
     """
     TODO: Add function documentation
     """
            self, 
            "Video Export Confirmation", 
            msg, 
            QMessageBox.Yes | QMessageBox.Cancel, 
            QMessageBox.Cancel, 
        )
        if buttonReply == QMessageBox.Yes:

                True
                if (self.intervalClipPath is not None and settings.enforceInterval)
                or not settings.enforceInterval
                else False
            )
                True
                if (self.firstClipPath is not None and settings.enforceFirstClip)
                or not settings.enforceFirstClip
                else False
            )
                True
                if (self.introClipPath is not None and settings.enforceIntro)
                or not settings.enforceIntro
                else False
            )
                True
                if (self.outroClipPath is not None and settings.enforceOutro)
                or not settings.enforceOutro
                else False
            )

            if not intervalCheck:
            if not firstClipCheck:
            if not introClipCheck:
            if not outroClipCheck:

            if amountClips < 2:

            if (
                intervalCheck is False
                or firstClipCheck is False
                or introClipCheck is False
                or outroClipCheck is False
                or amountClips < 2
            ):
                self.publishFail(msg)
                return

            self.mediaPlayer.stop()
            self.close()
            self.exportVideo()
            logger.info("Yes clicked.")
        if buttonReply == QMessageBox.Cancel:
            logger.info("Cancel")

    async def uploadFail(self, msg):
    def uploadFail(self, msg): -> Any
     """
     TODO: Add function documentation
     """

    async def publishFail(self, msg):
    def publishFail(self, msg): -> Any
     """
     TODO: Add function documentation
     """


if __name__ == "__main__":
    main()
