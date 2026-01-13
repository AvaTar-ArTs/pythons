from pathlib import Path
import os
import pandas as pd

import logging

logger = logging.getLogger(__name__)


# Directory containing the CSV files
csv_directory = Path(str(Path.home()) + "/Pictures/mydesign")

# List to hold dataframes
dataframes = []

# Define the expected headers
expected_headers = [
    "ID",
    "Default_slot_file_name",
    "Default_slot_image_url",
    "Digital Image_slot_file_name",
    "Digital Image_slot_image_url",
    "Boy_slot_file_name",
    "Boy_slot_image_url",
    "VID_slot_file_name",
    "VID_slot_image_url",
    "Mockup 10_slot_file_name",
    "Mockup 10_slot_image_url",
    "boy size_slot_file_name",
    "boy size_slot_image_url",
    "girl size_slot_file_name",
    "girl size_slot_image_url",
    "Video mockup_slot_file_name",
    "Video mockup_slot_image_url",
    "boy-girl_slot_file_name",
    "boy-girl_slot_image_url",
    "dark_slot_file_name",
    "dark_slot_image_url",
    "light_slot_file_name",
    "light_slot_image_url",
    "Listing.Title",
    "Listing.Description",
    "Listing.Tags",
    "Inventory and Pricing.Price",
    "Inventory and Pricing.Quantity",
    "Keywords.Primary Keyword",
    "Keywords.Secondary Keyword",
]

# Loop through all files in the directory
for filename in os.listdir(csv_directory):
    if filename.endswith(".CSV") or filename.endswith(".csv"):
        file_path = os.path.join(csv_directory, filename)
        # Read the CSV file
        df = pd.read_csv(file_path)
        # Ensure the dataframe has the expected headers
        if list(df.columns) == expected_headers:
            dataframes.append(df)
        else:
            print(
                f"File {filename} does not have the expected headers and will be skipped."
            )

# Concatenate all dataframes
if dataframes:
    merged_df = pd.concat(dataframes, ignore_index=True)

    # Save the merged dataframe to a new CSV file
    merged_df.to_csv(os.path.join(csv_directory, "merged_output.csv"), index=False)

    logger.info("All CSV files have been merged successfully!")
else:
    logger.info("No files with the expected headers were found.")
