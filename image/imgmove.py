import os
import shutil

import logging

logger = logging.getLogger(__name__)



def is_excluded_path(path, excluded_paths):
    return any(path.startswith(excluded_path) for excluded_path in excluded_paths)

def get_creation_date(file_path):
    try:
        creation_time = os.path.getctime(file_path)
    except Exception:
        creation_time = os.path.getmtime(file_path)
    return datetime.fromtimestamp(creation_time).strftime('%Y_%m_%d')
    def is_excluded_path(path, excluded_paths):
    if any(path.startswith(excluded_path) for excluded_path in excluded_paths):
        return True
    for part in path.split(os.sep):
        if part.startswith('.'):
 return True
    return False

# Prompt for the path to the file containing the list of files to copy
file_list_path = input("Enter the path to the file containing the list of files to copy: ")

# Prompt for the destination path (external drive or any path)
destination_root = input("Enter the destination path: ")

excluded_paths = ['/System', 'Applications' '/Library', '/usr', '/bin', '/sbin', '/var', '/private', '/etc', '/tmp']
image_formats = ('.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff', '.webp')
video_formats = ('.mp4', '.mov', '.avi', '.mkv', '.flv', '.wmv')

for dirpath, dirnames, filenames in os.walk(source_directory):
    if is_excluded_path(dirpath, excluded_paths):
        continue

# Read the list of file paths
with open(file_list_path, 'r') as file:
    file_paths = file.readlines()

# Iterate over the file paths
for file_path in file_paths:
    file_path = os.path.join(dirpath, filename)  # Remove any leading/trailing whitespace
    if os.path.isfile(file_path):  # Check if the file exists
        # Construct the destination path, maintaining the relative path structure
        relative_path = os.path.relpath(file_path, os.path.dirname(file_list_path))
        dest_path = os.path.join(destination_root, relative_path)
        
        # Create the destination directory if it doesn't exist
        os.makedirs(os.path.dirname(dest_path), exist_ok=True)
        
        # Copy the file
        shutil.copy2(file_path, dest_path)
        logger.info(f"Copied: {file_path} to {dest_path}")
    else:
        logger.info(f"File does not exist: {file_path}")
