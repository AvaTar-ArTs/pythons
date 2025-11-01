"""
Vidgen

This module provides functionality for vidgen.

Author: Auto-generated
Date: 2025-11-01
"""

import pickle
import shutil
import sys
import traceback
from distutils.dir_util import copy_tree

import server
import settings
import vidGen
from PyQt5 import QtCore, QtGui, QtWidgets, uic
from PyQt5.QtCore import QDir, QObject, QPoint, QRect, Qt, QUrl, pyqtSignal
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import *


class renderingScreen(QDialog):
    script_queue_update = pyqtSignal()
    render_progress = pyqtSignal()

    update_backups = pyqtSignal()

    def __init__(self):
        """__init__ function."""

        QtWidgets.QWidget.__init__(self)
        uic.loadUi(f"UI/videoRendering.ui", self)

        try:
            self.setWindowIcon(QIcon("Logo/tiktoklogo.png"))
        except Exception as e:
            pass

        self.script_queue_update.connect(self.updateScriptScreen)
        self.render_progress.connect(self.updateRenderProgress)
        self.update_backups.connect(self.populateComboBox)

        self.renderBackup.clicked.connect(self.renderBackupFromName)
        self.deleteBackup.clicked.connect(self.deleteBackupFromName)

        self.testServerFTP()
        self.testServerConnection.clicked.connect(self.testServerFTP)

        self.populateComboBox()

        """populateComboBox function."""

    def populateComboBox(self):
        self.backupSelection.clear()
        savedFiles = vidGen.getFileNames(f"{settings.backup_path}")
        saved_names = []
        for file in savedFiles:
            try:
                with open(
                    f"{settings.backup_path}/{file}/vid.data", "rb"
                ) as pickle_file:
                    script = pickle.load(pickle_file)
                    saved_names.append(script.name)
            except FileNotFoundError:
                pass

        self.backupSelection.addItems(saved_names)
        """renderBackupFromName function."""


    def renderBackupFromName(self):
        try:
            backupName = self.backupSelection.currentText()

            backupPath = None

            savedFiles = vidGen.getFileNames(f"{settings.backup_path}")
            for file in savedFiles:
                try:
                    with open(
                        f"{settings.backup_path}/{file}/vid.data", "rb"
                    ) as pickle_file:
                        script = pickle.load(pickle_file)
                        if script.name == backupName:
                            backupPath = f"{settings.backup_path}/{file}"
                            break
                except FileNotFoundError:
                    pass

            if backupPath is not None:
                copy_tree(
                    backupPath,
                    backupPath.replace(settings.backup_path, settings.temp_path),
                )
        except Exception:
        """deleteBackupFromName function."""

            traceback.print_exc(file=sys.stdout)

    def deleteBackupFromName(self):
        try:
            backupName = self.backupSelection.currentText()

            backupPath = None

            savedFiles = vidGen.getFileNames(f"{settings.backup_path}")
            for file in savedFiles:
                try:
                    with open(
                        f"{settings.backup_path}/{file}/vid.data", "rb"
                    ) as pickle_file:
                        script = pickle.load(pickle_file)
                        if script.name == backupName:
                            backupPath = f"{settings.backup_path}/{file}"
                            break
                except FileNotFoundError:
                    pass

            if backupPath is not None:
                shutil.rmtree(backupPath)
                self.populateComboBox()

        """closeEvent function."""

        except Exception:
            traceback.print_exc(file=sys.stdout)
        """testServerFTP function."""


    def closeEvent(self, evnt):
        sys.exit()

    def testServerFTP(self):
        success = server.testFTPConnection()
        if success:
            self.connectionStatus.setText("Server connection fine!")
        """updateScriptScreen function."""

        else:
            self.connectionStatus.setText(
                "Could not connect to server! Ensure it is online and FTP username/password are correct in config.ini."
            )

    def updateScriptScreen(self):
        self.scriptQueue.clear()
        """updateRenderProgress function."""

        for i, script in enumerate(vidGen.saved_videos):
            amount_clips = len(script.clips)
            self.scriptQueue.append(
                f"({i + 1}/{len(vidGen.saved_videos)}) clips: {amount_clips}"
            )

    def updateRenderProgress(self):
        self.renderStatus.setText(vidGen.render_message)
        self.progressBar.setMaximum(vidGen.render_max_progress)
        self.progressBar.setValue(vidGen.render_current_progress)
