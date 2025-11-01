"""
Tiktok

This module provides functionality for tiktok.

Author: Auto-generated
Date: 2025-11-01
"""

import sys
import traceback
from time import sleep

import database
import scriptwrapper
import settings
from pymediainfo import MediaInfo
from TikTokAPI import TikTokAPI

import logging

logger = logging.getLogger(__name__)


# Constants
CONSTANT_1000 = 1000


cookie = {"s_v_web_id": settings.s_v_web_id, "tt_webid": settings.tt_webid}

api = TikTokAPI(cookie=cookie)

forceStop = False


def getAllClips(filter, amount, window):
    """getAllClips function."""

    global all_clips_found, forceStop
    # format the saved_ids by taking it out of tuple form

    bad_ids = []

    for id in database.getAllSavedClipIDs():
        bad_ids.append(id[0])

    clips = []

    filterName = filter[0]
    filterObject = filter[1]

    logger.info(f"Looking for all clips for filter {filterName}")

    oldIds = []

        """attemptAddScripts function."""

    def attemptAddScripts(results, typeofrequest):
        try:
            newIds = []
            amountJustAdded = 0
            parseType = "itemList" if typeofrequest == "Hashtag" else "items"
            for i, tiktok in enumerate(results[parseType]):
                # logger.info("downloading %s/%s" % (i+1, len(result)))
                # Prints the text of the tiktok
                videoURL = None
                author = None
                vidId = None
                createTime = None
                text = None
                diggCount = None
                shareCount = None
                playCount = None
                commentCount = None
                duration = None
                hashtags = None

                try:
                    videoURL = tiktok["video"]["downloadAddr"]
                    author = tiktok["music"]["authorName"]
                    vidId = tiktok["id"]
                    createTime = tiktok["createTime"]
                    text = tiktok["desc"]
                    diggCount = tiktok["stats"]["diggCount"]
                    shareCount = tiktok["stats"]["shareCount"]
                    playCount = tiktok["stats"]["playCount"]
                    commentCount = tiktok["stats"]["commentCount"]
                    duration = tiktok["video"]["duration"]
                except Exception as e:
                    logger.info("error parsing data")
                    continue

                newIds.append(vidId)

                if vidId in bad_ids:
                    continue

                if vidId in [newclip.id for newclip in clips]:
                    continue

                if filterObject.likeCount is not None:
                    if diggCount < filterObject.likeCount:
                        bad_ids.append(vidId)
                        continue

                if filterObject.shareCount is not None:
                    if shareCount < filterObject.shareCount:
                        bad_ids.append(vidId)
                        continue

                if filterObject.playCount is not None:
                    if playCount < filterObject.playCount:
                        bad_ids.append(vidId)
                        continue

                if filterObject.commentCount is not None:
                    if commentCount < filterObject.commentCount:
                        bad_ids.append(vidId)
                        continue

                tiktok_clip = scriptwrapper.ClipWrapper(
                    vidId,
                    videoURL,
                    author,
                    createTime,
                    text,
                    diggCount,
                    shareCount,
                    playCount,
                    commentCount,
                    duration,
                )
                clips.append(tiktok_clip)
                amountJustAdded += 1

            return newIds
        except Exception:
            logger.info("error occurred parsing: %s" % results)
            return None

    searchAmount = amount

    while True:
        try:
            # The Number of trending TikToks you want to be displayed

            new_ids = []

            if filterObject.searchType == "Hashtag":
                hashtags = filterObject.inputText
                count = int(searchAmount / len(hashtags))
                for hashtag in hashtags:
                    logger.info("Looking for %s clips for hashtag %s" % (count, hashtag))
                    results = api.getVideosByHashTag(hashtag, count)

                    new = attemptAddScripts(results, "Trending")
                    if new is None:
                        break
                    new_ids.append(new)

            elif filterObject.searchType == "Author":
                authors = filterObject.inputText
                count = int(searchAmount / len(authors))

                for author in authors:
                    logger.info("Looking for %s clips for author %s" % (count, author))
                    results = api.getVideosByUserName(author, count)

                    new = attemptAddScripts(results, "Trending")
                    if new is None:
                        break
                    new_ids.append(new)
            elif filterObject.searchType == "Trending":
                logger.info("Looking for %s trending clips" % searchAmount)

                results = api.getTrending(searchAmount)

                new = attemptAddScripts(results, "Trending")
                if new is None:
                    break
                new_ids.append(new)

            if new_ids == oldIds:
                print(
                    "Found exactly the same ids in two consecutive searches. Terminating search process"
                )
                break

            oldIds = new_ids

            logger.info(f"{len(clips)} unique {filterName} clips found")

            if len(clips) >= amount:
                logger.info("done")
                break
            else:
                searchAmount *= 2

            if forceStop:
                logger.info("Forced Stop Finding Process")
                forceStop = False
                break
        except Exception as e:
            traceback.print_exc(file=sys.stdout)

            logger.info(e)
            logger.info("exception occured downloading. waiting and retrying")
            sleep(5)

    logger.info(f"Found {len(clips)} unique clips")
    for clip in clips:
        database.addFoundClip(clip, filterName)

    logger.info("DONE!")
    return clips


    """autoDownloadClips function."""

def autoDownloadClips(filterName, clips, window):
    global forceStop
    # Downloading the clips with custom naming scheme
    # window.update_log_start_downloading_game.emit(filterName, len(clips))
    logger.info("Downloading...")
    for i, clip in enumerate(clips):
        logger.info("Downloading Clip %s/%s" % (i + 1, len(clips)))
        try:
            api.downloadVideoById(
                clip.id, f"{settings.vid_filepath}/{clip.author_name}-{clip.id}.mp4"
            )

            media_info = MediaInfo.parse(
                f"{settings.vid_filepath}/{clip.author_name}-{clip.id}.mp4"
            )
            duration = media_info.tracks[0].duration
            clip.vid_duration = float(duration) / CONSTANT_1000
            database.updateStatusWithClip(clip.id, "DOWNLOADED", clip)
        except Exception as e:
            logger.info(e)
            logger.info("Error downloading clip")
            database.updateStatusWithClip(clip.id, "BAD", clip)

        window.update_log_downloaded_clip.emit(i + 1)
        if forceStop:
            logger.info("Forced Stop Downloading Process")
            forceStop = False
            break
