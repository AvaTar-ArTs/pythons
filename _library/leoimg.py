import os
import requests
from tqdm import tqdm
from colorama import Fore, Style

import logging

logger = logging.getLogger(__name__)


# Constants
CONSTANT_200 = 200
CONSTANT_8192 = 8192


def download_images(source_file, destination_dir):
    """download_images function."""

    # Ensure destination directory exists
    os.makedirs(destination_dir, exist_ok=True)

    # Read URLs from the source file
    with open(source_file, "r") as file:
        urls = [line.strip() for line in file if line.strip()]

    # Download each image with a progress bar
    for url in tqdm(
        urls,
        desc="Downloading",
        bar_format="{l_bar}" + Fore.GREEN + "{bar}" + Style.RESET_ALL + "{r_bar}",
    ):
        try:
            response = requests.get(url, stream=True)
            if response.status_code == CONSTANT_200:
                filename = os.path.join(destination_dir, os.path.basename(url))
                with open(filename, "wb") as f:
                    for chunk in response.iter_content(chunk_size=CONSTANT_8192):
                        f.write(chunk)
        except Exception as e:
            logger.info(Fore.RED + f"Error downloading {url}: {e}" + Style.RESET_ALL)


# Prompt for source file and destination directory
source_file = input("Enter the path to the source file: ")
destination_dir = input("Enter the destination directory for downloads: ")

download_images(source_file, destination_dir)
