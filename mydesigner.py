import os
from datetime import datetime

import pandas as pd
import requests

import logging

logger = logging.getLogger(__name__)


# Constants
CONSTANT_200 = 200


# Ensure that CSV and output directories exist based on the user prompt
def ensure_directories(base_dir):
    """ensure_directories function."""

    output_dir = os.path.join(base_dir, "processed_images")
    os.makedirs(output_dir, exist_ok=True)
    return output_dir

    # Function to download an image
    """download_image function."""


def download_image(url, filename):
    try:
        response = requests.get(url, timeout=10)
        if response.status_code == CONSTANT_200:
            with open(filename, "wb") as f:
                f.write(response.content)
            logger.info(f"✅ Downloaded: {filename}")
            return True
        else:
            logger.info(
                f"⚠️ Failed to download: {filename} (Status: {response.status_code})"
            )
            return False
    except Exception as e:
        logger.info(f"❌ Error downloading {filename}: {e}")
        return False

    """process_images function."""


# Process images based on image URLs in DataFrame
def process_images(df, output_dir):
    image_columns = [col for col in df.columns if "image_url" in col]
    download_log = []

    for idx, row in df.iterrows():
        listing_title = (
            row.get("Listing.Title", f"item_{idx}")
            .replace(" ", "_")
            .replace("/", "_")[:50]
        )
        for col in image_columns:
            url = row[col]
            if pd.notnull(url) and isinstance(url, str) and url.startswith("https"):
                # Determine filename
                extension = url.split("?")[0].split(".")[-1][
                    :4
                ]  # Trim to 4 characters for safety
                filename = f"{listing_title}_{col.replace(' ', '_')}_{idx}.{extension}"
                filepath = os.path.join(output_dir, filename)
                success = download_image(url, filepath)
                download_log.append(
                    {
                        "Filename": filename,
                        "Status": "Downloaded" if success else "Failed",
                    }
                )
    return download_log

    """write_log_to_csv function."""


# Function to write the log to a CSV file
def write_log_to_csv(log, csv_output_path):
    log_df = pd.DataFrame(log)
    log_df.to_csv(csv_output_path, index=False)
    logger.info(f"✅ Log written to {csv_output_path}")
    """main function."""


# Main function
def main():
    # Get source directory
    source_directory = input(
        "Enter the path to the source directory containing the CSV file: "
    ).strip()
    if not os.path.isdir(source_directory):
        logger.info("❌ Source directory does not exist.")
        return

    # Construct file paths
    csv_file_path = os.path.join(source_directory, "mydl.csv")
    if not os.path.isfile(csv_file_path):
        logger.info("❌ CSV file not found in the directory.")
        return

    # Load data and ensure output directory is set up
    df = pd.read_csv(csv_file_path)
    output_directory = ensure_directories(source_directory)

    # Process images and log results
    download_log = process_images(df, output_directory)

    # Write log to CSV
    timestamp = datetime.now().strftime("%m%d%Y")
    csv_output_path = os.path.join(
        source_directory, f"image_processing_log_{timestamp}.csv"
    )
    write_log_to_csv(download_log, csv_output_path)


# Entry point
if __name__ == "__main__":
    main()
