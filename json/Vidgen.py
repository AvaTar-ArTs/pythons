import re
import json
from datetime import datetime
from typing import Dict, List, Any, Optional, Tuple, Union
from pathlib import Path
import os
from PyQt5 import QtCore, QtGui, QtWidgets, uic
from PyQt5.QtCore import QDir, QObject, QPoint, QRect, Qt, QUrl, pyqtSignal
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import *
from distutils.dir_util import copy_tree
from functools import lru_cache
from typing import Any, Dict, List, Optional, Union, Tuple, Callable
import asyncio
import logging
import pickle
import server
import settings
import shutil
import sys
import traceback
import vidGen

# Constants
CONSTANT_100 = 100
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
    logger = logging.getLogger(__name__)
    script_queue_update = pyqtSignal()
    render_progress = pyqtSignal()
    update_backups = pyqtSignal()
    savedFiles = vidGen.getFileNames(f"{settings.backup_path}")
    saved_names = []
    script = pickle.load(pickle_file)
    backupName = self.backupSelection.currentText()
    backupPath = None
    savedFiles = vidGen.getFileNames(f"{settings.backup_path}")
    script = pickle.load(pickle_file)
    backupPath = f"{settings.backup_path}/{file}"
    backupName = self.backupSelection.currentText()
    backupPath = None
    savedFiles = vidGen.getFileNames(f"{settings.backup_path}")
    script = pickle.load(pickle_file)
    backupPath = f"{settings.backup_path}/{file}"
    success = server.testFTPConnection()
    amount_clips = len(script.clips)
    self._lazy_loaded = {}
    traceback.print_exc(file = sys.stdout)
    traceback.print_exc(file = sys.stdout)


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



class Config:
    # TODO: Replace global variable with proper structure



class renderingScreen(QDialog):


    async def __init__(self):
    def __init__(self): -> Any
     """
     TODO: Add function documentation
     """
        QtWidgets.QWidget.__init__(self)
        uic.loadUi(f"UI/videoRendering.ui", self)

        try:
            self.setWindowIcon(QIcon("Logo/tiktoklogo.png"))
    except (ValueError, TypeError, RuntimeError) as e:
        logger.error(f"Specific error occurred: {e}")
        raise
            pass

        self.script_queue_update.connect(self.updateScriptScreen)
        self.render_progress.connect(self.updateRenderProgress)
        self.update_backups.connect(self.populateComboBox)

        self.renderBackup.clicked.connect(self.renderBackupFromName)
        self.deleteBackup.clicked.connect(self.deleteBackupFromName)

        self.testServerFTP()
        self.testServerConnection.clicked.connect(self.testServerFTP)

        self.populateComboBox()

    async def populateComboBox(self):
    def populateComboBox(self): -> Any
     """
     TODO: Add function documentation
     """
        self.backupSelection.clear()
        for file in savedFiles:
            try:
                with open(f"{settings.backup_path}/{file}/vid.data", "rb") as pickle_file:
                    saved_names.append(script.name)
            except FileNotFoundError:
                pass

        self.backupSelection.addItems(saved_names)

    async def renderBackupFromName(self):
    def renderBackupFromName(self): -> Any
     """
     TODO: Add function documentation
     """
        try:


            for file in savedFiles:
                try:
                    with open(f"{settings.backup_path}/{file}/vid.data", "rb") as pickle_file:
                        if script.name == backupName:
                            break
                except FileNotFoundError:
                    pass

            if backupPath is not None:
                copy_tree(
                    backupPath, 
                    backupPath.replace(settings.backup_path, settings.temp_path), 
                )
    except (ValueError, TypeError, RuntimeError) as e:
        logger.error(f"Specific error occurred: {e}")
        raise

    async def deleteBackupFromName(self):
    def deleteBackupFromName(self): -> Any
     """
     TODO: Add function documentation
     """
        try:


            for file in savedFiles:
                try:
                    with open(f"{settings.backup_path}/{file}/vid.data", "rb") as pickle_file:
                        if script.name == backupName:
                            break
                except FileNotFoundError:
                    pass

            if backupPath is not None:
                shutil.rmtree(backupPath)
                self.populateComboBox()

    except (ValueError, TypeError, RuntimeError) as e:
        logger.error(f"Specific error occurred: {e}")
        raise

    async def closeEvent(self, evnt):
    def closeEvent(self, evnt): -> Any
     """
     TODO: Add function documentation
     """
        sys.exit()

    async def testServerFTP(self):
    def testServerFTP(self): -> Any
     """
     TODO: Add function documentation
     """
        if success:
            self.connectionStatus.setText("Server connection fine!")
        else:
            self.connectionStatus.setText(
                "Could not connect to server! Ensure it is online and FTP username/password are correct in config.ini."
            )

    async def updateScriptScreen(self):
    def updateScriptScreen(self): -> Any
     """
     TODO: Add function documentation
     """
        self.scriptQueue.clear()
        for i, script in enumerate(vidGen.saved_videos):
            self.scriptQueue.append(f"({i + 1}/{len(vidGen.saved_videos)}) clips: {amount_clips}")

    async def updateRenderProgress(self):
    def updateRenderProgress(self): -> Any
     """
     TODO: Add function documentation
     """
        self.renderStatus.setText(vidGen.render_message)
        self.progressBar.setMaximum(vidGen.render_max_progress)
        self.progressBar.setValue(vidGen.render_current_progress)


if __name__ == "__main__":
    main()
