from pathlib import Path
import os
import shutil
from datetime import datetime

import logging

logger = logging.getLogger(__name__)


# Set the source directory where your images are stored
source_dir = Path("/path/to/your/images")

# Loop through each file in the source directory
for filename in os.listdir(source_dir):
    if filename.lower().endswith((".png", ".jpg", ".jpeg", ".gif", ".bmp")):
        # Get the full path to the file
        file_path = os.path.join(source_dir, filename)

        # Get the creation time and convert it to a year
        creation_time = os.path.getctime(file_path)
        year = datetime.fromtimestamp(creation_time).strftime("%Y")

        # Define the destination directory based on the year
        dest_dir = os.path.join(source_dir, year)

        # Create the destination directory if it doesn't exist
        if not os.path.exists(dest_dir):
            os.makedirs(dest_dir)

        # Move the file to the destination directory
        shutil.move(file_path, os.path.join(dest_dir, filename))

logger.info("Images have been sorted.")
