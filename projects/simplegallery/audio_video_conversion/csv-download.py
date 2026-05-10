"""
Summary of csv-download.py

This module is part of the AVATARARTS ecosystem.
For more information about the AVATARARTS project, see the main documentation.
"""

import os

import pandas as pd
import requests


def read_csv():
    # Prompt the user for the path to the CSV file
    file_path = input("Enter the path to the CSV file: ")
    # Load the CSV data
    data = pd.read_csv(file_path, header=None, names=["date", "url"])
    return data


def download_images(data):
    # Prompt the user for the output directory
    output_directory = input("Enter the directory where images should be saved: ")
    for index, row in data.iterrows():
        url = row["url"]
        date = row["date"].replace(" ", "_").replace(":", "-")

        # Download the image
        response = requests.get(url)
        if response.status_code == 200:
            image_path = os.path.join(output_directory, f"{date}.png")
            with open(image_path, "wb") as file:
                file.write(response.content)
        else:
            print(f"Failed to download image from {url}")


# Continue from the previous code
data = read_csv()
download_images(data)
