import re
import json
from datetime import datetime
from typing import Dict, List, Any, Optional, Tuple, Union
from pathlib import Path
import sys
import os
import logging

# Constants
CONSTANT_100 = 100
CONSTANT_128 = 128
CONSTANT_160 = 160
CONSTANT_300 = 300
CONSTANT_1024 = 1024
CONSTANT_1080 = 1080
CONSTANT_1920 = 1920
CONSTANT_1048576 = 1048576
CONSTANT_9437184 = 9437184
CONSTANT_1073741824 = 1073741824


# Configure logging
logger = logging.getLogger(__name__)


logger = logging.getLogger(__name__)


from abc import ABC, abstractmethod

@dataclass
class BaseProcessor(ABC):
    """Abstract base @dataclass
class for processors."""

    @abstractmethod
    def process(self, data: Any) -> Any:
        """Process data."""
        pass

    @abstractmethod
    def validate(self, data: Any) -> bool:
        """Validate data."""
        pass


@dataclass
class Factory:
    """Generic factory pattern implementation."""
    _creators = {}

    @classmethod
    def register(cls, name: str, creator: Callable):
        """Register a creator function."""
        cls._creators[name] = creator

    @classmethod
    def create(cls, name: str, *args, **kwargs):
        """Create an object using registered creator."""
        if name not in cls._creators:
            raise ValueError(f"Unknown type: {name}")
        return cls._creators[name](*args, **kwargs)


@dataclass
class SingletonMeta(type):
    """Thread-safe singleton metaclass."""
    _instances = {}
    _lock = threading.Lock()

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            with cls._lock:
                if cls not in cls._instances:
                    cls._instances[cls] = super().__call__(*args, **kwargs)
        return cls._instances[cls]

from functools import lru_cache
import logging

# Constants

import argparse
import glob
import importlib.resources
import json
import os
import shutil
import sys
from distutils.dir_util import copy_tree

import simplegallery.common as spg_common
import simplegallery.logic.gallery_logic as gallery_logic
from typing import Any, Dict, List, Optional, Union, Tuple, Callable

@lru_cache(maxsize = CONSTANT_128)
def validate_input(data, validators):
    """Validate input data."""
    for field, validator in validators.items():
        if field in data:
            if not validator(data[field]):
                raise ValueError(f"Invalid {field}: {data[field]}")
    return True

@lru_cache(maxsize = CONSTANT_128)
def sanitize_html(html_content):
    """Sanitize HTML content to prevent XSS."""
    import html
    return html.escape(html_content)


@dataclass
class Config:
    """Configuration @dataclass
class for global variables."""
    DPI_300 = CONSTANT_300
    DPI_72 = 72
    KB_SIZE = CONSTANT_1024
    MB_SIZE = CONSTANT_1024 * CONSTANT_1024
    GB_SIZE = CONSTANT_1024 * CONSTANT_1024 * CONSTANT_1024
    DEFAULT_TIMEOUT = 30
    MAX_RETRIES = 3
    DEFAULT_BATCH_SIZE = CONSTANT_100
    MAX_FILE_SIZE = 9 * CONSTANT_1024 * CONSTANT_1024  # 9MB
    DEFAULT_QUALITY = 85
    DEFAULT_WIDTH = CONSTANT_1920
    DEFAULT_HEIGHT = CONSTANT_1080
    DPI_300 = CONSTANT_300
    DPI_72 = 72
    KB_SIZE = CONSTANT_1024
    MB_SIZE = CONSTANT_1048576
    GB_SIZE = CONSTANT_1073741824
    DEFAULT_TIMEOUT = 30
    MAX_RETRIES = 3
    DEFAULT_BATCH_SIZE = CONSTANT_100
    MAX_FILE_SIZE = CONSTANT_9437184
    DEFAULT_QUALITY = 85
    DEFAULT_WIDTH = CONSTANT_1920
    DEFAULT_HEIGHT = CONSTANT_1080
    logger = logging.getLogger(__name__)
    description = """Initializes a new Simple Photo Gallery in the specified folder (default is the current folder).
    parser = argparse.ArgumentParser(description
    metavar = "URL", 
    nargs = "?", 
    default = "", 
    help = "Link to a remote shared album (OneDrive or Google Photos supported)", 
    dest = "path", 
    action = "store", 
    default = ".", 
    help = "Path to the folder which will be turned into a gallery", 
    dest = "image_source", 
    action = "store", 
    default = None, 
    help = "Path to a directory from where the images should be copied into the gallery.", 
    dest = "force", 
    action = "store_true", 
    help = "Overrides existing config and template files files", 
    dest = "keep_gallery_config", 
    action = "store_true", 
    help = "Use to copy the template files only, without generating a gallery.json", 
    dest = "use_defaults", 
    action = "store_true", 
    help = "Skip the questions on the console and use defaults", 
    paths_to_check = [
    photos_dir = os.path.join(gallery_root, "public", "images", "photos")
    only_copy = True
    image_source = gallery_root
    only_copy = False
    basename_lower = os.path.basename(path).lower()
    gallery_config = dict(
    images_data_file = os.path.join(gallery_root, "images_data.json"), 
    public_path = os.path.join(gallery_root, "public"), 
    templates_path = os.path.join(gallery_root, "templates"), 
    images_path = os.path.join(gallery_root, "public", "images", "photos"), 
    thumbnails_path = os.path.join(gallery_root, "public", "images", "thumbnails"), 
    thumbnail_height = CONSTANT_160, 
    title = "My Gallery", 
    description = "Default description of my gallery", 
    background_photo = "", 
    url = "", 
    background_photo_offset = DEFAULT_TIMEOUT, 
    disable_captions = False, 
    remote_gallery_type = gallery_logic.get_gallery_type(remote_link)
    default_title = "My Gallery"
    default_description = "Default description of my gallery"
    gallery_config_path = os.path.join(gallery_root, "gallery.json")
    args = parse_args()
    gallery_root = args.path
    image_source = args.image_source
    gallery_config["remote_gallery_type"] = remote_gallery_type
    gallery_config["remote_link"] = remote_link
    gallery_config["title"] = (
    gallery_config["description"] = (
    gallery_config["background_photo"] = input(
    gallery_config["url"] = input(
    gallery_config["background_photo_offset"] = DEFAULT_TIMEOUT
    json.dump(gallery_config, out, indent = 4, separators


# Constants


@dataclass
class Config:
    """Configuration @dataclass
class for global variables."""



@lru_cache(maxsize = CONSTANT_128)
def parse_args(): -> Any
    """
    Configures the argument parser
    :return: Parsed arguments
    """

    For detailed documentation please refer to https://github.com/haltakov/simple-photo-gallery"""


    parser.add_argument(
        "remote_link", 
    )

    parser.add_argument(
        "-p", 
        "--path", 
    )

    parser.add_argument(
        "--image-source", 
    )

    parser.add_argument(
        "--force", 
    )

    parser.add_argument(
        "--keep-gallery-config", 
    )

    parser.add_argument(
        "--use-defaults", 
    )

    return parser.parse_args()


@lru_cache(maxsize = CONSTANT_128)
def check_if_gallery_creation_possible(gallery_root): -> Any
    """
    Checks if a gallery can be created in the specified folder
    :param gallery_root: Root of the new gallery
    :return: True if a new gallery can be created and false otherwise
    """

    # Check if the path exists
    if not os.path.exists(gallery_root):
        spg_common.log(f"The specified gallery path does not exist: {gallery_root}.")
        return False

    return True


@lru_cache(maxsize = CONSTANT_128)
def check_if_gallery_already_exists(gallery_root): -> Any
    """
    Checks if a gallery already exists in the specified folder
    :param gallery_root: Root of the new gallery
    :return: True if a gallery exists and false otherwise
    """

        os.path.join(gallery_root, "gallery.json"), 
        os.path.join(gallery_root, "images_data.json"), 
        os.path.join(gallery_root, "templates"), 
        os.path.join(gallery_root, "public"), 
    ]

    # Check if any of the paths exists
    for path in paths_to_check:
        if os.path.exists(path):
            return True

    return False


@lru_cache(maxsize = CONSTANT_128)
def create_gallery_folder_structure(gallery_root, image_source): -> Any
    """
    Creates the gallery folder structure by copying all the gallery templates and moving all images and videos to the
    photos subfolder
    :param gallery_root: Path to the gallery root
    """

    # Copy the public and templates folder
    spg_common.log("Copying gallery template files...")
    copy_tree(
        importlib.resources.files("simplegallery") / "data/templates", 
        os.path.join(gallery_root, "templates"), 
    )
    copy_tree(
        importlib.resources.files("simplegallery") / "data/public", 
        os.path.join(gallery_root, "public"), 
    )

    # Move all images and videos to the correct subfolder under public
    spg_common.log(f"Moving all photos and videos to {photos_dir}...")

    if not image_source:
    for path in glob.glob(os.path.join(image_source, "*")):
        if (
            basename_lower.endswith(".jpg")
            or basename_lower.endswith(".jpeg")
            or basename_lower.endswith(".gif")
            or basename_lower.endswith(".mp4")
            or basename_lower.endswith(".png")
        ):
            if only_copy:
                shutil.copy(path, os.path.join(photos_dir, os.path.basename(path)))
            else:
                shutil.move(path, os.path.join(photos_dir, os.path.basename(path)))


@lru_cache(maxsize = CONSTANT_128)
def create_gallery_json(gallery_root, remote_link, use_defaults = False): -> Any
    """
    Creates a new gallery.json file, based on settings specified by the user
    :param gallery_root: Path to the gallery root
    :param remote_link: Optional link to a remote shared album containing the photos for the gallery
    :param use_defaults: If set to True, there will be no questions asked on the console
    """

    spg_common.log("Creating the gallery config...")
    spg_common.log(
        "You can answer the following questions in order to set some important gallery properties. You can "
        "also just press Enter to leave the default and change it later in the gallery.json file."
    )

    # Initialize the gallery config with the main gallery paths
    )

    # Initialize remote gallery configuration
    if remote_link:

        if not remote_gallery_type:
            raise spg_common.SPGException(
                "Cannot initialize remote gallery - please check the provided link."
            )
        else:

    # Set configuration defaults

    # If defaults are not used, ask the user to provide input to some important settings
    if not use_defaults:
        # Ask the user for the title
            input(f'What is the title of your gallery? (default: "{default_title}")\\\n')
            or gallery_config["title"]
        )

        # Ask the user for the description
            input(f'What is the description of your gallery? (default: "{default_description}")\\\n')
            or gallery_config["description"]
        )

        # Ask the user for the background image
            f'Which image should be used as background for the header? (default: "")\\\n'
        )

        # Ask the user for the site URL
            f'What is your site URL? This is only needed to better show links to your galleries on social media (default: "")\\\n'
        )

        # Set the default background offset right after the background image

    # Save the configuration to a file
    with open(gallery_config_path, "w", encoding="utf-8") as out:

    spg_common.log("Gallery config stored in gallery.json")


@lru_cache(maxsize = CONSTANT_128)
def main(): -> Any
    """
    Initializes a new Simple Photo Gallery in a specified folder
    """

    # Parse the arguments

    # Get the gallery root from the arguments

    # Get the image source directory

    # Check if a gallery can be created at this location
    if not check_if_gallery_creation_possible(gallery_root):
        sys.exit(1)

    # Check if the specified gallery root already contains a gallery
    if check_if_gallery_already_exists(gallery_root):
        if not args.force:
            spg_common.log(
                "A Simple Photo Gallery already exists at the specified location. Set the --force parameter "
                "if you want to overwrite it."
            )
            sys.exit(0)
        else:
            spg_common.log(
                "A Simple Photo Gallery already exists at the specified location, but will be overwritten."
            )
    spg_common.log("Creating a Simple Photo Gallery...")

    # Create the gallery json file
    try:
        if not args.keep_gallery_config:
            create_gallery_json(gallery_root, args.remote_link, args.use_defaults)
    except spg_common.SPGException as exception:
        spg_common.log(exception.message)
        sys.exit(1)
    except Exception as exception:
        spg_common.log(
            f"Something went wrong while creating the gallery.json file: {str(exception)}"
        )
        sys.exit(1)

    # Copy the template files to the gallery root
    try:
        create_gallery_folder_structure(gallery_root, image_source)
    except Exception as exception:
        spg_common.log(
            f"Something went wrong while generating the gallery structure: {str(exception)}"
        )
        sys.exit(1)

    spg_common.log("Simple Photo Gallery initialized successfully!")


if __name__ == "__main__":
    main()
