
# Constants
CONSTANT_100 = 100
CONSTANT_128 = 128
CONSTANT_300 = 300
CONSTANT_1024 = 1024
CONSTANT_1080 = 1080
CONSTANT_1920 = 1920


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

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            with cls._lock:
                if cls not in cls._instances:
                    cls._instances[cls] = super().__call__(*args, **kwargs)
        return cls._instances[cls]

from functools import lru_cache
import logging
import os
import pickle
import sys
from threading import Thread
from time import sleep

import autodownloader
import database
import scriptwrapper
import server
import settings
import tiktok
from filtercreator import FilterCreationWindow
from PyQt5 import QtCore, QtGui, QtWidgets, uic
from PyQt5.QtCore import *
from PyQt5.QtCore import QDir, QObject, QPoint, QRect, Qt, QUrl, pyqtSignal
from PyQt5.QtGui import QIcon
from PyQt5.QtMultimedia import (
from typing import Any, Dict, List, Optional, Union, Tuple, Callable

@lru_cache(maxsize = CONSTANT_128)
def validate_input(data, validators):
    """Validate input data."""
    for field, validator in validators.items():
        if field in data:
            if not validator(data[field]):
                raise ValueError(f"Invalid {field}: {data[field]}")
    return True

@lru_cache(maxsize = CONSTANT_128)
def sanitize_html(html_content):
    """Sanitize HTML content to prevent XSS."""
    import html
    return html.escape(html_content)


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
    current_path = os.path.dirname(os.path.realpath(__file__))
    clips = database.getClipsByStatus("DOWNLOADED")
    filePath = f"{settings.vid_filepath}/%s.mp4" % clip.mp4
    clips = database.getFilterClipsByStatus(filter, "DOWNLOADED")
    filePath = f"{settings.vid_filepath}/%s.mp4" % clip.mp4
    update_log_found_clips = pyqtSignal(str, int, str)
    update_log_found_total_clips = pyqtSignal(str, int)
    update_log_start_downloading_game = pyqtSignal(str, int)
    update_log_downloaded_clip = pyqtSignal(int)
    update_done_downloading_game = pyqtSignal(str, int)
    start_clip_search = pyqtSignal()
    start_download_search = pyqtSignal()
    update_combo_box_filter = pyqtSignal()
    end_find_search = pyqtSignal()
    end_download_search = pyqtSignal()
    username = self.username.text()
    password = self.password.text()
    toRemove = self.userToRemove.currentText()
    index = [i for i in range(len(server.usersList)) if server.usersList[i][0]
    username = user[0]
    password = user[1]
    users = []
    game = self.gameSelectToDelete.currentText()
    filters = []
    saved_filters = database.getFilterNames()
    filter = self.filterSelect.currentText()
    filterObject = database.getSavedFilterByName(filter)
    filters = database.getAllSavedFilters()  # get all saved filters
    total_downloaded = 0
    amount = database.getFilterClipCount(filter)[0][0]
    amount_downloaded = database.getFilterClipCountByStatus(filter, "DOWNLOADED")[0][0]
    amount_used = database.getFilterClipCountByStatus(filter, "USED")[0][0]
    self.autoDownloadQueue = []
    self.autoWrapper = autodownloader.AutoDownloader(self, self.autoDownloadQueue)
    self.clipEditorWindow = clipEditorWindow
    self.clipFindIndex = 0
    self.filter_window = FilterCreationWindow(self)
    self.autoWrapper.auto = True
    self.autoWrapper.auto = False
    self.autoDownloadQueue = pickle.load(pickle_file)
    self.autoWrapper.autoDownloadQueue = self.autoDownloadQueue
    self.autoWrapper.autoDownloadQueue = self.autoDownloadQueue
    total_downloaded + = amount_downloaded


# Constants


@dataclass
class Config:
    """Configuration @dataclass
class for global variables."""

    QAbstractVideoBuffer, 
    QAbstractVideoSurface, 
    QMediaContent, 
    QMediaPlayer, 
    QMediaPlaylist, 
    QVideoFrame, 
    QVideoSurfaceFormat, 
)
from PyQt5.QtWidgets import *



@lru_cache(maxsize = CONSTANT_128)
def cleanDatabase():
 """
 TODO: Add function documentation
 """

    logger.info("Checking %s clips for MP4s" % len(clips))

    for i, clip in enumerate(clips):
        logger.info(f"Checking if clip ({i + 1}/{len(clips)}) exists")
        if not os.path.exists(f"{settings.vid_filepath}/%s.mp4" % clip.mp4):
            logger.info(f"Clip does not exist {filePath}")
            database.updateStatus(clip.id, "MISSING")


@lru_cache(maxsize = CONSTANT_128)
def deleteClipsForFilter(filter):
 """
 TODO: Add function documentation
 """

    logger.info("Attemping to delete all clips for %s (%s downloaded found)" % (filter, len(clips)))
    for i, clip in enumerate(clips):
        logger.info(f"Checking if clip ({i + 1}/{len(clips)}) exists")
        if not os.path.exists(f"{settings.vid_filepath}/%s.mp4" % clip.mp4):
            logger.info(f"Clip does not exist {filePath}")
            database.updateStatus(clip.id, "FOUND")
        else:
            os.remove(f"{settings.vid_filepath}/%s.mp4" % clip.mp4)
            logger.info(f"Clip exists, deleting it {filePath}")
            database.updateStatus(clip.id, "FOUND")


@dataclass
class PassiveDownloaderWindow(QMainWindow):



    def __init__(self, clipEditorWindow = None):
     """
     TODO: Add function documentation
     """
        QtWidgets.QWidget.__init__(self)
        uic.loadUi(f"{current_path}/UI/clipPassiveDownload.ui", self)
        try:
            self.setWindowIcon(QIcon("Assets/tiktoklogo.png"))
        except Exception as e:
            pass

        self.loadGameQueue()
        self.addFilter.clicked.connect(self.addFilterToQueue)
        self.clearFilters.clicked.connect(self.clearFilterQueue)

        self.startFinding.clicked.connect(self.startFindingProcess)
        self.stopFinding.clicked.connect(self.stopFindingProcess)
        self.startDownloading.clicked.connect(self.startDownloadingProcess)
        self.stopDownloading.clicked.connect(self.stopDownloadingProcess)
        self.refreshFilterClips.clicked.connect(self.logGetAmountClips)
        self.deleteClips.clicked.connect(self.deleteClipsByGame)
        self.updateStatus.clicked.connect(self.cleanDatabase)
        self.addNewFilter.clicked.connect(self.addFilterPopup)

        self.update_log_found_clips.connect(self.logAddClipFoundInfo)
        self.update_log_found_total_clips.connect(self.logAddTotalClipFoundInfo)
        self.update_log_start_downloading_game.connect(self.logStartDownloadFilterInfo)
        self.update_log_downloaded_clip.connect(self.updateProgressBar)
        self.update_done_downloading_game.connect(self.logDoneDownloadingFilterInfo)

        self.start_clip_search.connect(self.logStartClipSearchInfo)
        self.end_find_search.connect(self.logCompletedClipSearchInfo)
        self.end_download_search.connect(self.logCompletedDownloadInfo)
        self.start_download_search.connect(self.logStartDownloadInfo)

        self.update_combo_box_filter.connect(self.populateComboBox)

        self.startAuto.clicked.connect(self.startAutoProcess)
        self.stopAuto.clicked.connect(self.stopAutoProcess)
        self.addNewUser.clicked.connect(self.addNewFTPUser)
        self.removeUser.clicked.connect(self.deleteFTPUser)
        self.finishVidDirectory.clicked.connect(self.openFinishedVids)
        self.clipBinDirectory.clicked.connect(self.openClipBin)
        self.startAuto.setEnabled(False)

        self.populateComboBox()

        self.updateAccountInfo()

    def closeEvent(self, evnt):
     """
     TODO: Add function documentation
     """
        sys.exit()

    def openFinishedVids(self):
     """
     TODO: Add function documentation
     """
        os.startfile(settings.final_video_path)

    def openClipBin(self):
     """
     TODO: Add function documentation
     """
        os.startfile(settings.vid_filepath)

    def addNewFTPUser(self):
     """
     TODO: Add function documentation
     """
        if username == "" or password == "":
            self.userAddStatus.setText("Please enter a password or username")
        elif username in [i[0] for i in server.usersList]:
            self.userAddStatus.setText("Account already exists with this name!")
        else:
            self.userAddStatus.setText("Successfully added new user %s" % username)
            server.usersList.append((username, password))
            self.updateAccountInfo()
            server.saveUsersTable()

    def deleteFTPUser(self):
     """
     TODO: Add function documentation
     """
        if toRemove:
            del server.usersList[index[0]]
            logger.info("Successfully deleted user %s" % toRemove)
        else:
            logger.info("Couldn't delete user %s" % toRemove)
        self.updateAccountInfo()
        server.saveUsersTable()

    def updateAccountInfo(self):
     """
     TODO: Add function documentation
     """
        self.accountInfo.clear()
        for user in server.usersList:

            self.accountInfo.append("User %s, password %s" % (username, password))
        self.populateRemoveUserList()

    def populateRemoveUserList(self):
     """
     TODO: Add function documentation
     """
        self.userToRemove.clear()
        for user in server.usersList:
            if user[0] == settings.videoGeneratorFTPUser:
                continue
            users.append(user[0])
        self.userToRemove.addItems(users)

    def deleteClipsByGame(self):
     """
     TODO: Add function documentation
     """
        deleteClipsForFilter(game)

    def cleanDatabase(self):
     """
     TODO: Add function documentation
     """
        cleanDatabase()

    def addFilterPopup(self):
     """
     TODO: Add function documentation
     """

        self.filter_window.show()

    def populateComboBox(self):
     """
     TODO: Add function documentation
     """
        self.filterSelect.clear()
        self.gameSelectToDelete.clear()
        for filter in saved_filters:
            filters.append(filter)
        self.filterSelect.addItems(filters)
        self.gameSelectToDelete.addItems(filters)

    def startFindingProcess(self):
     """
     TODO: Add function documentation
     """
        self.refreshFilterClips.setEnabled(False)
        self.addFilter.setEnabled(False)
        self.clearFilters.setEnabled(False)
        self.startFinding.setEnabled(False)
        self.stopFinding.setEnabled(True)
        self.startAuto.setEnabled(False)
        self.stopAuto.setEnabled(False)

        self.autoWrapper.findClips()
        pass

    def stopFindingProcess(self):
     """
     TODO: Add function documentation
     """
        self.startFinding.setEnabled(True)
        self.startFinding.setEnabled(True)
        self.stopFinding.setEnabled(False)
        # self.startAuto.setEnabled(True)
        self.startAuto.setEnabled(False)
        self.stopAuto.setEnabled(False)
        self.autoWrapper.stop()
        pass

    def startDownloadingProcess(self):
     """
     TODO: Add function documentation
     """
        self.refreshFilterClips.setEnabled(False)
        self.addFilter.setEnabled(False)
        self.clearFilters.setEnabled(False)
        self.stopFinding.setEnabled(False)
        self.startAuto.setEnabled(False)
        self.stopAuto.setEnabled(False)
        self.startFinding.setEnabled(False)
        self.startDownloading.setEnabled(False)
        self.stopDownloading.setEnabled(True)

        self.autoWrapper.downloadClips()
        pass

    def stopDownloadingProcess(self):
     """
     TODO: Add function documentation
     """
        self.refreshFilterClips.setEnabled(True)
        self.addFilter.setEnabled(True)
        self.clearFilters.setEnabled(True)
        self.stopFinding.setEnabled(False)
        # self.startAuto.setEnabled(True)
        self.startAuto.setEnabled(False)
        self.stopAuto.setEnabled(False)
        self.startFinding.setEnabled(True)
        self.startDownloading.setEnabled(True)
        self.stopDownloading.setEnabled(False)

        self.autoWrapper.stop()
        pass

    def startAutoProcess(self):
     """
     TODO: Add function documentation
     """
        self.refreshFilterClips.setEnabled(False)
        self.addFilter.setEnabled(False)
        self.clearFilters.setEnabled(False)
        self.stopFinding.setEnabled(False)
        self.startFinding.setEnabled(True)
        self.startAuto.setEnabled(False)
        self.stopAuto.setEnabled(True)
        self.startFinding.setEnabled(False)
        self.startDownloading.setEnabled(False)

        self.autoWrapper.startAutoMode()
        pass

    def stopAutoProcess(self):
     """
     TODO: Add function documentation
     """
        self.autoWrapper.stop()

    def loadGameQueue(self):
     """
     TODO: Add function documentation
     """
        try:
            with open(f"{current_path}/autodownloaderfilters.save", "rb") as pickle_file:
        except Exception:
            pass
        self.updateAutoDownloadQueue()
        self.logGetAmountClips()

    def addFilterToQueue(self):
     """
     TODO: Add function documentation
     """
        self.clearFilterQueue()
        if filter not in [tempfilter[0] for tempfilter in self.autoDownloadQueue]:
            self.autoDownloadQueue.append([filter, filterObject])

        with open(f"{current_path}/autodownloaderfilters.save", "wb") as pickle_file:
            pickle.dump(self.autoDownloadQueue, pickle_file)

        self.logGetAmountClips()
        self.updateAutoDownloadQueue()

    def clearFilterQueue(self):
     """
     TODO: Add function documentation
     """
        self.autoDownloadQueue.clear()
        self.autoWrapper.autoDownloadQueue.clear()
        self.updateAutoDownloadQueue()

    def updateAutoDownloadQueue(self):
     """
     TODO: Add function documentation
     """
        self.autoDownloadInfo.clear()
        for filter in self.autoDownloadQueue:
            self.autoDownloadInfo.append(filter[0])

    def logStartClipSearchInfo(self):  # called in autodownloader
     """
     TODO: Add function documentation
     """
        self.downloadLog.append("Starting Clip Search for %s filters" % len(self.autoDownloadQueue))

    def logAddClipFoundInfo(self, game_name, amount, period):  # called in twitch
     """
     TODO: Add function documentation
     """
        self.downloadLog.append(
            "Found %s for filter %s for period %s" % (amount, game_name, period)
        )

    def logAddTotalClipFoundInfo(self, game_name, amount):  # called in twitch
     """
     TODO: Add function documentation
     """
        self.downloadLog.append("Found %s for filter %s" % (amount, game_name))
        self.autoWrapper.findClips()

    def logCompletedClipSearchInfo(self):  # called in autodownloader
     """
     TODO: Add function documentation
     """
        self.downloadLog.append(
            "Completed clip search for %s filters" % len(self.autoDownloadQueue)
        )
        self.logGetAmountClips()
        self.refreshFilterClips.setEnabled(True)
        self.addFilter.setEnabled(True)
        self.clearFilters.setEnabled(True)
        self.startFinding.setEnabled(True)
        self.stopFinding.setEnabled(False)
        self.stopAuto.setEnabled(False)
        # self.startAuto.setEnabled(True)
        self.startAuto.setEnabled(False)

    def logGetAmountClips(self):  # called here
     """
     TODO: Add function documentation
     """
        self.clipBinInformation.clear()
        for filter in [i[0] for i in filters]:
            self.clipBinInformation.append(
                "Filter: %s amount clips %s (downloaded %s | used %s)"
                % (filter, amount, amount_downloaded, amount_used)
            )
        self.clipBinInformation.append("Total Downloaded: %s" % total_downloaded)

    def logStartDownloadInfo(self):  # called in autodownloader
     """
     TODO: Add function documentation
     """
        self.downloadLog.append("Starting downloads for %s filters" % len(self.autoDownloadQueue))

    def logStartDownloadFilterInfo(self, filter, amount):  # called tiktok
     """
     TODO: Add function documentation
     """
        self.progressBar.setValue(0)
        self.progressBar.setMaximum(amount)
        self.downloadLog.append("Downloading %s clips for filter %s" % (amount, filter))
        self.currentDownloadFilter.setText("Current Filter: %s" % filter)
        self.amountCurrentPass.setText("Amount in current pass: %s" % amount)

    def logDoneDownloadingFilterInfo(self, filter, amount):  # called in tiktok
     """
     TODO: Add function documentation
     """
        self.downloadLog.append("Finished downloading %s clips for filter %s" % (amount, filter))
        self.autoWrapper.downloadClips()

    def logCompletedDownloadInfo(self):  # called in autodownloader
     """
     TODO: Add function documentation
     """
        self.downloadLog.append("Completed downloading %s clips" % len(self.autoDownloadQueue))
        self.logGetAmountClips()
        self.refreshFilterClips.setEnabled(True)
        self.addFilter.setEnabled(True)
        self.clearFilters.setEnabled(True)
        self.startFinding.setEnabled(True)
        self.startDownloading.setEnabled(True)
        self.stopDownloading.setEnabled(False)
        self.stopFinding.setEnabled(False)

    def updateProgressBar(self, number):  # called in twitch
     """
     TODO: Add function documentation
     """
        self.progressBar.setValue(number)
        self.downloadProgressAmount.setText("Download progress: %s" % number)


if __name__ == "__main__":
    main()
