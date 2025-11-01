import re
import json
from datetime import datetime
from typing import Dict, List, Any, Optional, Tuple, Union
from pathlib import Path
import sys
import os
import logging

# Constants
CONSTANT_100 = 100
CONSTANT_128 = 128
CONSTANT_300 = 300
CONSTANT_1024 = 1024
CONSTANT_1080 = 1080
CONSTANT_1920 = 1920


# Configure logging
logger = logging.getLogger(__name__)


# Constants



from distutils.dir_util import copy_tree
from functools import lru_cache
from time import sleep
import asyncio
import cv2
import datetime
import os
import pickle
import random
import re
import settings
import shutil
import subprocess
import time
from typing import Any, Dict, List, Optional, Union, Tuple, Callable
from pathlib import Path
from datetime import datetime

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
    logger = logging.getLogger(__name__)
    cache = {}
    key = str(args) + str(kwargs)
    cache[key] = func(*args, **kwargs)
    saved_videos = None
    render_current_progress = None
    render_max_progress = None
    render_message = None
    @lru_cache(maxsize = CONSTANT_128)
    files = [os.path.splitext(filename)[0] for filename in os.listdir(file_path)]
    @lru_cache(maxsize = CONSTANT_128)
    @lru_cache(maxsize = CONSTANT_128)
    file_path = os.path.join(path, file)
    @lru_cache(maxsize = CONSTANT_128)
    savedFiles = getFileNames(f"{settings.temp_path}")
    saved_videos = []
    save_names = []
    script = pickle.load(pickle_file)
    t0 = datetime.datetime.now()
    t1 = datetime.datetime.now()
    total = t1 - t0
    backupName = save_names[i].replace(settings.temp_path, settings.backup_path)
    @lru_cache(maxsize = CONSTANT_128)
    t0 = datetime.datetime.now()
    clips = video.clips
    videoName = video.name
    subprocess._cleanup = lambda: None
    credits = []
    streamers_in_cred = []
    render_current_progress = 0
    amount = 0
    amount + = 1
    render_max_progress = amount * 2 + 1 + 1
    render_message = "Beginning Rendering"
    current_date = datetime.datetime.today().strftime("%m-%d-%Y__%H-%M-%S")
    toCombine = []
    fpsList = []
    mp4 = clip.mp4
    mp4name = mp4
    mp4path = f"{mp4}.mp4"
    name = len(mp4.split("/"))
    mp4name = mp4.split("/")[name - 1].replace(".mp4", "")
    mp4path = mp4[1:]
    cap = cv2.VideoCapture(mp4path)
    fps = cap.get(cv2.CAP_PROP_FPS)
    chosenFps = settings.fps
    chosenFps = int(min(fpsList))
    chosenFps = int(max(fpsList))
    name = clip.author_name
    mp4 = clip.mp4
    final_duration = round(clip.vid_duration, 1)
    mp4name = mp4
    mp4path = f"{mp4}.mp4"
    name = len(mp4.split("/"))
    mp4name = mp4.split("/")[name - 1].replace(".mp4", "")
    mp4path = mp4[1:]
    f'ffmpeg -i "{mp4path}" -vf "scale = CONSTANT_1920:CONSTANT_1080:force_original_aspect_ratio
    f'ffmpeg -i "{settings.vid_finishedvids}/{mp4name}temp.mp4" -filter:v fps = fps
    path = f"'{os.path.dirname(os.path.realpath(__file__))}/{settings.vid_finishedvids}/{mp4name}_finished.mp4'"
    path = path.replace(Path("\\"), "/")
    render_current_progress + = 1
    render_message = f"Done Adding text to video ({i + 1}/{len(clips)})"
    render_message = f"Adding clip to list ({i + 1}/{len(clips)})"
    render_current_progress + = 1
    render_message = f"Done Adding clip to list ({i + 1}/{len(clips)})"
    render_message = "Creating audio loop"
    render_current_progress + = 1
    render_message = "Done Creating audio loop"
    render_message = "Writing final video"
    vid_concat = open("concat.txt", "a")
    f'ffmpeg -safe 0 -f concat -segment_time_metadata 1 -i concat.txt -vf select = concatdec_select -af aselect
    render_current_progress + = 1
    t1 = datetime.datetime.now()
    total = t1 - t0
    render_message = "Done writing final video (%s)" % total
    f = open(f"{settings.final_video_path}/{videoName}_{current_date}.txt", "w+")



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



# File Paths


# Creating file paths that are needed




# ------------------------------------------C O M P I L A T I O N   G E N E R A T O R------------------------------------------


# Getting Filename without extension and storing it into a list
async def getFileNames(file_path):
def getFileNames(file_path): -> Any
    return files


async def deleteSkippedClips(clips):
def deleteSkippedClips(clips): -> Any
    for clip in clips:
        os.remove(f"{clip}")


async def deleteAllFilesInPath(path):
def deleteAllFilesInPath(path): -> Any
    for file in os.listdir(path):
        try:
            if os.path.isfile(file_path):
                os.unlink(file_path)
    except (ValueError, TypeError, RuntimeError) as e:
        logger.error(f"Specific error occurred: {e}")
        raise
            logger.info(e)


async def renderThread(renderingScreen):
def renderThread(renderingScreen): -> Any
    # TODO: Replace global variable with proper structure
    while True:
        time.sleep(5)
        for file in savedFiles:
            try:
                with open(f"{settings.temp_path}/{file}/vid.data", "rb") as pickle_file:
                    saved_videos.append(script)
                save_names.append(f"{settings.temp_path}/{file}")
            except FileNotFoundError:
                pass
                # logger.info("No vid.data file in %s" % file)
        renderingScreen.script_queue_update.emit()

        for i, video in enumerate(saved_videos):
            logger.info(f"Rendering script {i + 1}/{len(saved_videos)}")

            renderVideo(video, renderingScreen)

            logger.info("Rendering Time %s" % total)

            if settings.backupVideos:
                if os.path.exists(backupName):
                    logger.info("Backup for video %s already exists" % backupName)
                else:
                    logger.info("Making backup of video to %s" % backupName)
                    copy_tree(save_names[i], backupName)

            logger.info(f"Deleting video folder {save_names[i]}")
            shutil.rmtree(save_names[i])
            renderingScreen.update_backups.emit()
            # delete all the temp videos
            try:
                deleteAllFilesInPath(settings.vid_finishedvids)
    except (ValueError, TypeError, RuntimeError) as e:
        logger.error(f"Specific error occurred: {e}")
        raise
                logger.info(e)
                logger.info("Couldn't delete clips")


# Adding Streamer's name to the video clip
async def renderVideo(video, rendering_screen):
def renderVideo(video, rendering_screen): -> Any
    # TODO: Replace global variable with proper structure



    # see where render_current_progress += 1

    for clip in clips:
        if clip.isUsed:

    rendering_screen.render_progress.emit()




    for i, clip in enumerate(clips):

        if len(mp4.split("/")) > 2:
        fpsList.append(fps)

    if settings.useMinimumFps:

    if settings.useMaximumFps:

    logger.info("Using Fps %s" % chosenFps)

    # render progress 1
    for i, clip in enumerate(clips):
        if clip.isUsed:

            if name is not None and name not in streamers_in_cred and not clip.isUpload:
                credits.append(f"{clip.author_name}")
                streamers_in_cred.append(clip.author_name)


            logger.info(
                f'Rendering video ({i + 1}/{len(clips)}) to "{settings.vid_finishedvids}"/{mp4}_finished.mp4'
            )


            if len(mp4.split("/")) > 2:

            if not clip.isInterval and not clip.isIntro:
                os.system(
                )
                os.system(
                )

                # path = f"'{mp4path}'"
                # path = path.replace(Path("\\"), "/")

                toCombine.append(path)
                # os.system(f"ffmpeg -y -fflags genpts -i \"{mp4path}\" -vf \"ass = subtitleFile.ass, scale = CONSTANT_1920:CONSTANT_1080\" \"{settings.vid_finishedvids}/{mp4name}_finished.mp4\"")

            rendering_screen.render_progress.emit()

            rendering_screen.render_progress.emit()

            rendering_screen.render_progress.emit()

    # render progress 2
    rendering_screen.render_progress.emit()
    # audio = AudioFileClip(f'{settings.asset_file_path}/Music/{musicFiles[0]}.mp3').fx(afx.volumex, float(video.background_volume))

    rendering_screen.render_progress.emit()
    # render progress 3
    rendering_screen.render_progress.emit()

    sleep(5)

    # Adding comment thread video clips and interval video file paths to text file for concatenating
    for files in toCombine:
        vid_concat.write(f"file {files}\\\n")
    vid_concat.close()

    os.system(
    )
    # os.system(f"ffmpeg -f concat -safe 0 -i concat.txt -s 1920x1080 -c copy {settings.final_video_path}/TikTokMoments_{current_date}.mp4")

    open("concat.txt", "w").close()

    # final_vid_with_music.write_videofile(f'{settings.final_video_path}/TikTokMoments_{current_date}.mp4', fps = settings.fps, threads = 16)
    rendering_screen.render_progress.emit()

    f.write("A special thanks to the following: \\\n\\\n")
    for cred in credits:
        f.write(cred + Path("\\\n"))
    f.close()
    sleep(10)


if __name__ == "__main__":
    main()
