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
                            value = value.strip().strip('"').strip("'")
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

import os
import time

import requests

import logging

logger = logging.getLogger(__name__)


# Constants
CONSTANT_200 = 200


# Get the API key from the environment variable
API_KEY = os.getenv("VANCEAI_API_KEY")
API_URL = "https://api-service.vanceai.com/web_api/v1/removebg"
PROGRESS_URL = "https://api-service.vanceai.com/web_api/v1/progress"


def remove_background(input_path, output_path):
    """remove_background function."""

    with open(input_path, "rb") as file:
        response = requests.post(
            API_URL, files={"image_file": file}, headers={"api_key": API_KEY}
        )

    if response.status_code == CONSTANT_200:
        result = response.json()
        trans_id = result["trans_id"]
        download_result(trans_id, output_path)
    else:
        logger.info(f"Error: {response.status_code}")
        logger.info(response.text)

    """download_result function."""


def download_result(trans_id, output_path):
    while True:
        response = requests.get(
            f"{PROGRESS_URL}?trans_id={trans_id}&api_token={API_KEY}"
        )

        if response.status_code == CONSTANT_200:
            progress_result = response.json()
            status = progress_result["data"]["status"]
            if status == "finish":
                image_url = progress_result["data"]["image_url"]
                image_response = requests.get(image_url)
                if image_response.status_code == CONSTANT_200:
                    with open(output_path, "wb") as out_file:
                        out_file.write(image_response.content)
                    logger.info(f"Background removed and saved to {output_path}")
                else:
                    logger.info(
                        f"Error downloading image: {image_response.status_code}"
                    )
                break
            elif status == "fatal":
                logger.info("Image processing failed.")
                break
            else:
                logger.info(f"Current status: {status}. Checking again in 2 seconds.")
                time.sleep(2)
        else:
            logger.info(f"Request failed: {response.status_code}")
            break

    """process_directory function."""


def process_directory(input_dir):
    output_dir = os.path.join(input_dir, "output")
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    for filename in os.listdir(input_dir):
        if filename.lower().endswith((".png", ".jpg", ".jpeg")):
            input_path = os.path.join(input_dir, filename)
            output_path = os.path.join(
                output_dir, f"{os.path.splitext(filename)[0]}.png"
            )
            remove_background(input_path, output_path)


if __name__ == "__main__":
    input_directory = input("Enter the path to the source directory: ")
    if os.path.isdir(input_directory):
        process_directory(input_directory)
    else:
        logger.info("The specified directory does not exist.")
