"""
Tts Main

This module provides functionality for tts main.

Author: Auto-generated
Date: 2025-11-01
"""

import time

from polly_main import polly, tts_task_resp
from s3bucket import audio_down

import logging

logger = logging.getLogger(__name__)


def tts_start():
    """tts_start function."""

    audio_book_topic = input("enter audiobook name: ")
    audio_content = input(" enter audiobook content: \n")
    file_link = polly(audio_book_topic, audio_content)
    filename_to_save_local = audio_book_topic + file_link["SynthesisTask"]["TaskId"]
    logger.info("audio book generated: " + audio_book_topic)
    print(
        audio_book_topic, file_link["SynthesisTask"]["TaskId"], filename_to_save_local
    )
    file_to_download = file_link["SynthesisTask"]["TaskId"] + ".mp3"
    filename_to_save_local_with_ext = filename_to_save_local + ".mp3"
    s3_name = "qa-ai-bucket"
    logger.info(file_to_download, filename_to_save_local_with_ext)
    tts_task_status = tts_task_resp(file_link["SynthesisTask"]["TaskId"])

    while tts_task_status["SynthesisTask"]["TaskStatus"] == "scheduled":
        tts_task_status = tts_task_resp(file_link["SynthesisTask"]["TaskId"])
        logger.info(tts_task_status["SynthesisTask"]["TaskStatus"])
        time.sleep(4)

    if tts_task_status["SynthesisTask"]["TaskStatus"] == "completed":
        audio_down(
            s3_name, audio_book_topic, file_to_download, filename_to_save_local_with_ext
        )
