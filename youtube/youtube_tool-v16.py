"""
Youtube Tool

This module provides functionality for youtube tool.

Author: Auto-generated
Date: 2025-11-01
"""

import os
import sys
from threading import Thread

import client
import clientUI
import settings
from PyQt5 import QtWidgets

import logging

logger = logging.getLogger(__name__)


current_path = os.path.dirname(os.path.realpath(__file__))
script = None
menu = None


class App:
    def __init__(self):
        """__init__ function."""

        global menu
        app = QtWidgets.QApplication(sys.argv)
        app.processEvents()

        login = clientUI.LoginWindow()
        login.show()

        Thread(target=client.VideoGeneratorRenderStatus).start()

        sys.exit(app.exec_())


def init():
    """init function."""

    app = App()


sys._excepthook = sys.excepthook


    """exception_hook function."""

def exception_hook(exctype, value, traceback):
    logger.info(exctype, value, traceback)
    sys._excepthook(exctype, value, traceback)
    sys.exit(1)


sys.excepthook = exception_hook

    """getFileNames function."""


def getFileNames(file_path):
    files = [os.path.splitext(filename)[0] for filename in os.listdir(file_path)]
    return files
    """deleteAllFilesInPath function."""



def deleteAllFilesInPath(path):
    for file in os.listdir(path):
        file_path = os.path.join(path, file)
        try:
            if os.path.isfile(file_path):
                os.unlink(file_path)
        except Exception as e:
            logger.info(e)


if __name__ == "__main__":
    current_directory = os.path.dirname(os.path.realpath(__file__))
    os.chdir(current_directory)
    settings.generateConfigFile()
    if not os.path.exists("TempClips"):
        os.mkdir("TempClips")
        os.mkdir("FirstClips")
        os.mkdir("Intros")
        os.mkdir("Outros")
        os.mkdir("Finished Videos")
        os.mkdir("Intervals")
        os.mkdir("Save Data")

    else:
        deleteAllFilesInPath("TempClips")

    client.requestGames()
    init()

    # requestGames()
    # requestClips("Warzone", 10)
    # connectFTP()

    pass
    #
    # while len(getFileNames(f'{current_path}/Assets/Music')) == 0:
    #     logger.info(f"No music files in directory: '{current_path}/Assets/Music'. Please add some!")
    #     sleep(5)
    #
    # while len(getFileNames(f'{current_path}/Assets/Intros')) == 0:
    #     logger.info(f"No intro videos in directory: '{current_path}/Assets/Intros'. Please add some!")
    #     sleep(5)
    #
    # while len(getFileNames(f'{current_path}/Assets/Intervals')) == 0:
    #     logger.info(f"No intro videos in directory: '{current_path}/Assets/Intervals'. Please add some!")
    #     sleep(5)
    #
    # init()
