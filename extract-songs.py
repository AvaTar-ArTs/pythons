"""
Extract Songs

This module provides functionality for extract songs.

Author: Auto-generated
Date: 2025-11-01
"""

from pathlib import Path
import re
from bs4 import BeautifulSoup
import pandas as pd
import os

import logging

logger = logging.getLogger(__name__)


# Option A: Prompt for file paths
def prompt_for_files():
    """prompt_for_files function."""

    logger.info("Enter the file paths for the HTML files (comma-separated):")
    file_paths = input().split(",")
    return [file.strip() for file in file_paths]

    # Option B: Predefined file paths
    """predefined_file_paths function."""


def predefined_file_paths():
    return [
        Path("/Users/steven/Music/suno/1.html"),
        Path("/Users/steven/Music/suno/2.html"),
        Path("/Users/steven/Music/suno/3.html"),
        Path("/Users/steven/Music/suno/4.html"),
        Path("/Users/steven/Music/suno/5.html"),
        Path("/Users/steven/Music/suno/6.html"),
    ]

    """extract_song_details function."""


# Main function to process HTML files
def extract_song_details(file_paths):
    song_details = []

    # Adjusted regex pattern
    pattern = (
        r'src="([^"]+)".*?title="([^"]+)".*?href="([^"]+)".*?href="([^"]+)">([^<]+)'
    )

    for file_path in file_paths:
        if not os.path.exists(file_path):
            logger.info(f"File not found: {file_path}")
            continue

        with open(file_path, "r", encoding="utf-8") as file:
            html_content = file.read()

        # Use BeautifulSoup for structured data extraction
        soup = BeautifulSoup(html_content, "html.parser")
        for item in soup.find_all(
            "div", class_="css-79jxux"
        ):  # Adjust class names if needed
            title_element = item.find("span", class_="text-primary")
            song_url_element = item.find("a", href=True)
            cover_url_element = item.find_previous_sibling("img", src=True)
            genre_element = item.find("a", class_="hover:underline", href=True)
            time_element = item.find("span", class_="text-mono")

            # Regex for fallback extraction
            matches = re.findall(pattern, html_content)
            for match in matches:
                song_details.append(
                    {
                        "Song Title": (
                            match[1]
                            if match[1]
                            else (title_element["title"] if title_element else "")
                        ),
                        "Song URL": (
                            f"http://suno.com{match[2]}"
                            if match[2]
                            else (
                                f"http://suno.com{song_url_element['href']}"
                                if song_url_element
                                else ""
                            )
                        ),
                        "Cover Url": (
                            match[0]
                            if match[0]
                            else (cover_url_element["src"] if cover_url_element else "")
                        ),
                        "Genre": (
                            match[4]
                            if match[4]
                            else (genre_element.text.strip() if genre_element else "")
                        ),
                        "Time": time_element.text.strip() if time_element else "",
                        "Lyrics": "",  # Placeholder for Lyrics
                        "Info": "",  # Placeholder for Info
                        "Keys": "",  # Placeholder for Keys
                    }
                )

    return song_details

    """main function."""


# Execution starts here
def main():
    logger.info("Choose an option:")
    logger.info("1. Prompt for file paths")
    logger.info("2. Use predefined file paths")
    choice = input("Enter 1 or 2: ").strip()

    if choice == "1":
        file_paths = prompt_for_files()
    elif choice == "2":
        file_paths = predefined_file_paths()
    else:
        logger.info("Invalid choice. Exiting.")
        return

    song_details = extract_song_details(file_paths)
    if not song_details:
        logger.info("No song details extracted.")
        return

    # Save to CSV
    output_csv_path = "extracted_song_details.csv"
    df = pd.DataFrame(song_details)
    df.to_csv(output_csv_path, index=False)

    logger.info(f"Extracted song details saved to {output_csv_path}")


if __name__ == "__main__":
    main()
