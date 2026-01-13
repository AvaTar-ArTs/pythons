import os
import sys
from threading import Thread

import server
import settings
import vidGen
import vidgenUI
from PyQt5 import QtWidgets

import logging

logger = logging.getLogger(__name__)


class App:
    def __init__(self):
        """__init__ function."""

        app = QtWidgets.QApplication(sys.argv)
        app.processEvents()
        renderingScreen = vidgenUI.renderingScreen()
        renderingScreen.show()
        Thread(target=vidGen.renderThread, args=(renderingScreen,)).start()
        Thread(target=server.sendThread).start()

        sys.exit(app.exec_())


if __name__ == "__main__":
    current_directory = os.path.dirname(os.path.realpath(__file__))
    os.chdir(current_directory)
    settings.generateConfigFile()

    if not os.path.exists(settings.temp_path):
        os.mkdir(f"{settings.temp_path}")

    if not os.path.exists(settings.final_video_path):
        os.mkdir(f"{settings.final_video_path}")

    if not os.path.exists(settings.vid_finishedvids):
        os.mkdir(f"{settings.vid_finishedvids}")

    if not os.path.exists(settings.backup_path):
        os.mkdir(f"{settings.backup_path}")

    start = True
    if settings.useMaximumFps and settings.useMinimumFps:
        print(
            "Selected max fps and minimum fps in the config file. Please only set one to true!"
        )
        start = False

    if start:
        vidGen.deleteAllFilesInPath(settings.vid_finishedvids)
        server.init()
        App()
