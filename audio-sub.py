"""
Media Processing Audio Sub 1

This module provides functionality for media processing audio sub 1.

Author: Auto-generated
Date: 2025-11-01
"""


import logging

logger = logging.getLogger(__name__)


# Constants
CONSTANT_5242880 = 5242880

"""
This script is used to generate a transcript from an audio file using AssemblyAI api.
"""

from pathlib import Path
import os
import time

import config
import requests

upload_url = "https://api.assemblyai.com/v2/upload"
transcribe_url = "https://api.assemblyai.com/v2/transcript"
srt_endpoint = (
    "https://api.assemblyai.com/v2/transcript/"  # YOUR-TRANSCRIPT-ID-HERE/srt
)
headers = {"authorization": config.assemblyai}


# Read the audio file to verify
def read_file(filename, chunk_size=CONSTANT_5242880):
    with open(filename, "rb") as _file:
        while True:
            data = _file.read(chunk_size)
            if not data:
                break
            yield data


# Start upload the file
def uploadFile(filename):
    responseSubmit = requests.post(
        upload_url, headers=headers, data=read_file(filename)
    )
    # Receive upload URL
    return responseSubmit.json()["upload_url"]

def transcribe(filename):
    # Request for transcript
    audio = uploadFile(filename)
    json = {"audio_url": audio}

    responseReceive = requests.post(transcribe_url, json=json, headers=headers)
    return responseReceive.json()["id"]


def poll(transcript_id):
    polling_endpoint = transcribe_url + "/" + transcript_id
    polling_response = requests.get(polling_endpoint, headers=headers)
    return polling_response.json()


def get_transcription_result_url(url):
    transcribe_id = transcribe(url)
    while True:
        data = poll(transcribe_id)
        if data["status"] == "completed":
            return data, None
        elif data["status"] == "error":
            return data, data["error"]
        logger.info("Waiting for transcript (eta: 30 seconds)")
        time.sleep(30)


def save_transcript(url, title, exportPath="./"):
    logger.info("Generating transcript for {}...".format(url))

    if not os.path.exists(exportPath):
        logger.info("Creating directory...")
        os.makedirs(exportPath)

    # check if the file already exists in the exportPath with the same title - TESTING PURPOSES
    # if os.path.exists(exportPath + str(title) + '.srt'):
    #     logger.info("Using existed file...")
    #     return exportPath + str(title) + '.srt'

    data, error = get_transcription_result_url(url)

    if data:
        transcript = requests.get(srt_endpoint + data["id"] + Path("/srt"), headers=headers)
        filename = exportPath + str(title) + ".srt"
        with open(filename, "w") as f:
            f.write(transcript.text)
        logger.info("Transcript saved")
        return filename
    elif error:
        logger.info("Error!!!", error)


# save_transcript(filepath,'7', './result/')

res = uploadFile("./audio/0.mp3")
logger.info(res)
