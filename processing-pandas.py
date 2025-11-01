"""
Data Processing Pandas Csv 1

This module provides functionality for data processing pandas csv 1.

Author: Auto-generated
Date: 2025-11-01
"""

from pathlib import Path

import pandas as pd
import requests

import logging

logger = logging.getLogger(__name__)


# Corrected CSV file path
csv_file = Path(str(Path.home()) + "/Downloads/NeAt/Misc/reformatted_mydesigns - Sheet1.csv")

df = pd.read_csv(csv_file)

# Base directory to save images and info
base_dir = Path(Path(str(Path.home()) + "/csv2/"))
base_dir.mkdir(exist_ok=True)

# Iterate through each row of the CSV and process the images and info
for index, row in df.iterrows():
    title = row["TITLE"]
    description = row["DESCRIPTION"]
    tags = row["TAGS"]
    language = row.get("LANGUAGE", "EN")  # Assuming 'EN' as default if not specified
    type_ = row.get("TYPE", "")  # Assuming empty string as default if not specified
    color = row.get("COLOR", "")  # Assuming empty string as default if not specified

    # Create a sub-directory for each title
    product_dir = base_dir / title.replace(" ", "_").replace("/", "_")  # Sanitize title
    product_dir.mkdir(exist_ok=True)

    # Define image_urls here, checking each IMAGE column in the CSV
    image_urls = [row[f"IMAGE{i}"] for i in range(1, 11) if pd.notna(row[f"IMAGE{i}"])]

    # Initialize a list to hold image paths
    image_paths = []

    # Download and save images, and collect their paths
    for idx, url in enumerate(image_urls, start=1):
        try:
            response = requests.get(url)
            response.raise_for_status()

            # Constructing filename
            filename = f"{title.replace(' ', '_').replace('/', '_')}_{idx}.jpg"
            file_path = product_dir / filename
            image_paths.append(str(file_path))

            with open(file_path, "wb") as file:
                file.write(response.content)
            logger.info(f"Downloaded {filename}")

        except requests.RequestException as e:
            logger.info(f"Error downloading {url}: {e}")

    # Create a DataFrame with the image information
    image_info_df = pd.DataFrame(
        {
            "Image Path": image_paths,
            "Language": [language] * len(image_paths),
            "Title": [title] * len(image_paths),
            "Description": [description] * len(image_paths),
            "Tags": [tags] * len(image_paths),
            "Type": [type_] * len(image_paths),
            "Color": [color] * len(image_paths),
        }
    )

    # Save the DataFrame as a CSV file in the product directory
    image_info_df.to_csv(product_dir / "image_info.csv", index=False)
