"""
This script is used to generate a transcript from an audio file using AssemblyAI api.
"""

# Load API keys from ~/.env.d/ (best practice - handles export statements, quotes, comments)
from pathlib import Path as PathLib


def load_env_d():
    """Load all .env files from ~/.env.d directory (sophisticated pattern from youtube-load.py)"""
    env_d_path = PathLib.home() / ".env.d"
    if env_d_path.exists():
        for env_file in env_d_path.glob("*.env"):
            try:
                with open(env_file) as f:
                    for line in f:
                        line = line.strip()
                        if line and not line.startswith("#") and "=" in line:
                            # Handle export statements
                            if line.startswith("export "):
                                line = line[7:]
                            key, value = line.split("=", 1)
                            key = key.strip()
                            value = value.strip().strip("'").strip("'")
                            # Skip source statements
                            if not key.startswith("source"):
                                os.environ[key] = value
            except Exception as e:
                # Logger not initialized yet, use print
                print(f"Warning: Error loading {env_file}: {e}")


load_env_d()

# Also load from ~/.env as fallback using dotenv
try:
    from dotenv import load_dotenv

    load_dotenv(os.path.expanduser("~/.env"))
except ImportError:
    pass

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
        transcript = requests.get(
            srt_endpoint + data["id"] + Path("/srt"), headers=headers
        )
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
