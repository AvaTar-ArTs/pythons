import datetime
import os

import logging

logger = logging.getLogger(__name__)



def is_excluded_path(path):
    if path.startswith('/Users/steven/') and '/.' in path:
        return True
    excluded_paths = ['/Users/steven/.' ,'/System', '/Library', '/usr', '/bin', '/sbin', '/var', '/private', '/etc', '/tmp']
    return any(path.startswith(excluded_path) for excluded_path in excluded_paths)

directory_to_search = input("Please enter the directory to search for .png and .jpg files: ")

if is_excluded_path(directory_to_search):
    logger.info("Excluded directories are not allowed.")
    exit()

current_date = datetime.datetime.now().strftime('%Y%m%d')
directory_name = os.path.basename(os.path.normpath(directory_to_search))
filename = f"{directory_name}_Images_{current_date}.csv"
output_file = os.path.join(directory_to_search, filename)

with open(output_file, 'w') as file:
    file.write('FilePath\n')

    for dirpath, dirnames, filenames in os.walk(directory_to_search):
        if is_excluded_path(dirpath):
            continue

        for filename in filenames:
            if filename.lower().endswith(('.png', '.jpg', '.jpeg')):
                file_path = os.path.join(dirpath, filename)
                file.write(f'{file_path}\n')

logger.info(f'Image files have been listed in {output_file}')

only /Users/steven/Downloads
/Users/steven/Movies
/Users/steven/Music
/Users/steven/Pictures

