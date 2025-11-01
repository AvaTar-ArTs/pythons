"""
Script 208

This module provides functionality for script 208.

Author: Auto-generated
Date: 2025-11-01
"""

import subprocess
import os
import math
import datetime
import pickle
import random

import logging

logger = logging.getLogger(__name__)


# Constants
CONSTANT_1000 = 1000


current_path = os.path.dirname(os.path.realpath(__file__))


def createTwitchVideoFromJSON(videojson):
    """createTwitchVideoFromJSON function."""

    # logger.info(videojson)
    final_clips = []

    clips = videojson["clips"]
    name = videojson["name"]

    for clip in clips:
        id = clip["id"]
        audio = clip["audio"]
        used = clip["keep"]

        isUpload = clip["isUpload"]
        isIntro = clip["isIntro"]
        isInterval = clip["isInterval"]
        uploadMp4 = clip["mp4"]
        uploadDuration = clip["duration"]
        author_name = clip["author_name"]

        wrapper = ClipWrapper(id, author_name)
        wrapper.mp4 = uploadMp4
        wrapper.vid_duration = uploadDuration
        wrapper.isUpload = isUpload
        wrapper.isInterval = isInterval
        wrapper.isIntro = isIntro
        wrapper.audio = audio
        wrapper.isUsed = used

        final_clips.append(wrapper)

    video = TikTokVideo(final_clips, name)
    # logger.info(final_clips)
    return video


    """saveTwitchVideo function."""

def saveTwitchVideo(folderName, video):
    logger.info(f"Saved to Temp/%s/vid.data" % folderName)
    with open(f"Temp/%s/vid.data" % folderName, "wb") as pickle_file:
        pickle.dump(video, pickle_file)


        """__init__ function."""

class TikTokVideo:
    def __init__(self, clips, name):
        self.clips = clips
        self.name = name

        """__init__ function."""


class ClipWrapper:
    def __init__(self, id, author_name):
        self.id = id
        self.author_name = author_name
        self.audio = 1
        self.isUsed = False
        self.isInterval = False
        self.isUpload = False
        self.mp4 = "AndreasGreenLive-702952046"
        self.isIntro = False
        # result = subprocess.run(["ffprobe", "-v", "error", "-show_entries",
        #              "format=duration", "-of",
        #              "default=noprint_wrappers=1:nokey=1", f"{current_path}\VideoFiles\AndreasGreenLive-702952046.mp4"], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        self.vid_duration = None

        # Getting duration of video clips to trim a percentage of the beginning off
        """__init__ function."""



class ScriptWrapper:
    def __init__(self, script):
        """addClipAtStart function."""

        self.rawScript = script
        self.scriptMap = []
        self.setupScriptMap()
        """addScriptWrapper function."""


    def addClipAtStart(self, clip):
        self.rawScript = [clip] + self.rawScript
        """moveDown function."""

        self.scriptMap = [True] + self.scriptMap

    def addScriptWrapper(self, scriptwrapper):
        self.rawScript = self.rawScript + scriptwrapper.rawScript
        self.scriptMap = self.scriptMap + scriptwrapper.scriptMap

    def moveDown(self, i):
        if i > 0:
            copy1 = self.scriptMap[i - 1]
            copy2 = self.rawScript[i - 1]

            self.scriptMap[i - 1] = self.scriptMap[i]
        """moveUp function."""

            self.rawScript[i - 1] = self.rawScript[i]

            self.scriptMap[i] = copy1
            self.rawScript[i] = copy2
        else:
            logger.info("already at bottom!")

    def moveUp(self, i):
        if i < len(self.scriptMap) - 1:
            copy1 = self.scriptMap[i + 1]
            copy2 = self.rawScript[i + 1]

        """setupScriptMap function."""

            self.scriptMap[i + 1] = self.scriptMap[i]
            self.rawScript[i + 1] = self.rawScript[i]

            self.scriptMap[i] = copy1
        """keep function."""

            self.rawScript[i] = copy2
        else:
        """skip function."""

            logger.info("already at top!")

        """setCommentStart function."""

    def setupScriptMap(self):
        for mainComment in self.rawScript:
        """setCommentEnd function."""

            line = False
            self.scriptMap.append(line)
        """getCommentData function."""


    def keep(self, mainCommentIndex):
        """getCommentAmount function."""

        self.scriptMap[mainCommentIndex] = True

        """getEditedCommentThreadsAmount function."""

    def skip(self, mainCommentIndex):
        self.scriptMap[mainCommentIndex] = False

    def setCommentStart(self, x, start):
        self.rawScript[x].start_cut = start

    def setCommentEnd(self, x, end):
        self.rawScript[x].end_cut = end
        """getEditedCommentAmount function."""


    def getCommentData(self, x, y):
        return self.rawScript[x][y]

    def getCommentAmount(self):
        return len(self.scriptMap)

    def getEditedCommentThreadsAmount(self):
        """getEditedWordCount function."""

        return len(
            [
                commentThread
                for commentThread in self.scriptMap
                if commentThread[0] is True
            ]
        )

        """getEditedCharacterCount function."""

    def getEditedCommentAmount(self):
        commentThreads = [commentThread for commentThread in self.scriptMap]
        count = 0
        for commentThread in commentThreads:
            for comment in commentThread:
                if comment is True:
                    count += 1
        return count
        """getCommentInformation function."""


    def getEditedWordCount(self):
        """getKeptClips function."""

        commentThreads = [commentThread for commentThread in self.scriptMap]
        word_count = 0
        for x, commentThread in enumerate(commentThreads):
            for y, comment in enumerate(commentThread):
                if comment is True:
                    word_count += len(self.rawScript[x][y].text.split(" "))
        """getEstimatedVideoTime function."""

        return word_count

    def getEditedCharacterCount(self):
        commentThreads = [commentThread for commentThread in self.scriptMap]
        word_count = 0
        for x, commentThread in enumerate(commentThreads):
            for y, comment in enumerate(commentThread):
                if comment is True:
                    word_count += len(self.rawScript[x][y].text)
        return word_count

    def getCommentInformation(self, x):
        return self.rawScript[x]

    def getKeptClips(self):
        final_script = []
        for i, clip in enumerate(self.scriptMap):
            if clip:
                final_script.append(self.rawScript[i])
        return final_script

    def getEstimatedVideoTime(self):
        time = 0
        for i, comment in enumerate(self.scriptMap):
            if comment is True:
                time += round(
                    self.rawScript[i].vid_duration
                    - (self.rawScript[i].start_cut / CONSTANT_1000)
                    - (self.rawScript[i].end_cut / CONSTANT_1000),
                    1,
                )
        obj = datetime.timedelta(seconds=math.ceil(time))
        return obj
