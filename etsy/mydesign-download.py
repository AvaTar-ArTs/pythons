"""
Mydesign Csv Download 1

This module provides functionality for mydesign csv download 1.

Author: Auto-generated
Date: 2025-11-01
"""

from pathlib import Path

import pandas as pd
import requests

import logging

logger = logging.getLogger(__name__)


# Function to sanitize the title to create a valid directory name
def sanitize_title(title):
    """sanitize_title function."""

    return title.replace(" ", "_").replace("/", "_").replace("|", "").replace(",", "")


# Read the original CSV file
csv_file = Path(Path("/Users/steven/Documents/python/x-python/mydesigns-export.CSV"))
df = pd.read_csv(csv_file)

# Directory where images will be downloaded
base_dir = Path(Path("/Users/steven/Pictures/etsy/mydesign"))
base_dir.mkdir(exist_ok=True)

# Process each row in the DataFrame
for index, row in df.iterrows():
    title = sanitize_title(row["TITLE"])
    description = row.get("DESCRIPTION", "")
    tags = row.get("TAGS", "")
    language = row.get("LANGUAGE", "EN")
    type_ = row.get("TYPE", "")
    color = row.get("COLOR", "")

    # Create a sub-directory for each title
    product_dir = base_dir / title
    product_dir.mkdir(exist_ok=True)

    # Define image_urls and initialize a list to hold image paths
    image_urls = [row[f"IMAGE{i}"] for i in range(1, 11) if pd.notna(row[f"IMAGE{i}"])]
    image_paths = []

    # Download images, update the DataFrame, and collect their paths
    for idx, url in enumerate(image_urls, start=1):
        try:
            response = requests.get(url)
            response.raise_for_status()

            # Constructing filename and saving the image
            filename = f"{title}_{idx}.jpg"
            file_path = product_dir / filename
            with open(file_path, "wb") as file:
                file.write(response.content)
            logger.info(f"Downloaded {filename}")

            # Update the DataFrame and append the path
            df.at[index, f"IMAGE{idx}"] = str(file_path)
            image_paths.append(str(file_path))

        except requests.RequestException as e:
            logger.info(f"Error downloading {url}: {e}")

    # Create a DataFrame with the image information for this product
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

# Save the updated DataFrame to a new Excel file
updated_excel_path = base_dir / "updated_image_paths.xlsx"
df.to_excel(updated_excel_path, index=False, engine="openpyxl")
logger.info(f"Updated Excel file saved to {updated_excel_path}")
