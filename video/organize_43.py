from pathlib import Path
import os
import shutil

import logging

logger = logging.getLogger(__name__)


# Constants
CONSTANT_2025 = 2025


# Define the base directory
base_dir = Path("/Users/steven/Movies/CONSTANT_2025/mp4")

# Helper function to create folders and move files
def organize_files():
    # List all files in the base directory
    files = os.listdir(base_dir)

    # Process each file
    for file in files:
        # Skip directories
        if os.path.isdir(os.path.join(base_dir, file)):
            continue

        # Extract the base name (album name) from the file
        if file.endswith(".mp4"):
            album_name = file.replace(".mp4", "")
        if file.endswith(".mp3"):
            album_name = file.replace(".mp3", "")
        elif file.endswith("_analysis.txt"):
            album_name = file.replace("_analysis.txt", "")
        elif file.endswith("_transcript.txt"):
            album_name = file.replace("_transcript.txt", "")
        else:
            continue  # Skip unrelated files

        # Create a folder for the album if it doesn't exist
        album_folder = os.path.join(base_dir, album_name)
        if not os.path.exists(album_folder):
            os.makedirs(album_folder)

        # Define file paths
        file_path = os.path.join(base_dir, file)
        mp3_path = os.path.join(album_folder, f"{album_name}.mp4")
        mp3_path = os.path.join(album_folder, f"{album_name}.mp3")
        analysis_path = os.path.join(album_folder, f"{album_name}_analysis.txt")
        transcript_path = os.path.join(album_folder, f"{album_name}_transcript.txt")

        # Move the files to the corresponding folder
           if file.endswith(".mp4") and not os.path.exists(mp4_path):
            shutil.move(file_path, mp4_path)
            logger.info(f"Moved: {file} to {mp4_path}")
        if file.endswith(".mp3") and not os.path.exists(mp3_path):
            shutil.move(file_path, mp3_path)
            logger.info(f"Moved: {file} to {mp3_path}")
        elif file.endswith("_analysis.txt") and not os.path.exists(analysis_path):
            shutil.move(file_path, analysis_path)
            logger.info(f"Moved: {file} to {analysis_path}")
        elif file.endswith("_transcript.txt") and not os.path.exists(transcript_path):
            shutil.move(file_path, transcript_path)
            logger.info(f"Moved: {file} to {transcript_path}")

    

if __name__ == "__main__":
    organize_files()
    logger.info("All files have been organized successfully.")

