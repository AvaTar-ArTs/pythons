"""
Gallery initialization script for City 16-9 Gallery Generator
Following the dark architectural patterns of simplegallery
"""

import argparse
import os
import sys
import json
import glob
import shutil
from distutils.dir_util import copy_tree
from typing import Dict, Any
import common as cg_common


def parse_args():
    """
    Configures the argument parser with dark styling
    :return: Parsed arguments
    """
    description = """Initialize a new City 16-9 Gallery in the specified folder.
    For detailed documentation please refer to the dark arts of gallery generation."""

    parser = argparse.ArgumentParser(description=description)

    parser.add_argument(
        "remote_link",
        metavar="URL",
        nargs="?",
        default="",
        help="Link to a remote shared album (OneDrive or Google Photos supported)",
    )

    parser.add_argument(
        "-p",
        "--path",
        dest="path",
        action="store",
        default=".",
        help="Path to the folder which will be turned into a gallery",
    )

    parser.add_argument(
        "--image-source",
        dest="image_source",
        action="store",
        default=None,
        help="Path to a directory from where the images should be copied into the gallery.",
    )

    parser.add_argument(
        "--force",
        dest="force",
        action="store_true",
        help="Overrides existing config and template files",
    )

    parser.add_argument(
        "--keep-gallery-config",
        dest="keep_gallery_config",
        action="store_true",
        help="Use to copy the template files only, without generating a gallery.json",
    )

    parser.add_argument(
        "--use-defaults",
        dest="use_defaults",
        action="store_true",
        help="Skip the questions on the console and use defaults",
    )

    parser.add_argument(
        "--dark-theme",
        dest="dark_theme",
        action="store_true",
        default=True,
        help="Enable dark theme by default (default: True)",
    )

    return parser.parse_args()


def check_if_gallery_creation_possible(gallery_root: str) -> bool:
    """
    Checks if a gallery can be created in the specified folder
    :param gallery_root: Root of the new gallery
    :return: True if a new gallery can be created and false otherwise
    """
    if not os.path.exists(gallery_root):
        cg_common.log(f"The specified gallery path does not exist: {gallery_root}.")
        return False
    return True


def check_if_gallery_already_exists(gallery_root: str) -> bool:
    """
    Checks if a gallery already exists in the specified folder
    :param gallery_root: Root of the new gallery
    :return: True if a gallery exists and false otherwise
    """
    paths_to_check = [
        os.path.join(gallery_root, "gallery.json"),
        os.path.join(gallery_root, "images_data.json"),
        os.path.join(gallery_root, "templates"),
        os.path.join(gallery_root, "public"),
    ]

    for path in paths_to_check:
        if os.path.exists(path):
            return True
    return False


def create_gallery_folder_structure(gallery_root: str, image_source: str = None) -> None:
    """
    Creates the gallery folder structure by copying all the gallery templates
    :param gallery_root: Path to the gallery root
    :param image_source: Optional source directory for images
    """
    # Create directory structure
    directories = [
        os.path.join(gallery_root, "templates"),
        os.path.join(gallery_root, "public"),
        os.path.join(gallery_root, "public", "css"),
        os.path.join(gallery_root, "public", "js"),
        os.path.join(gallery_root, "public", "images"),
        os.path.join(gallery_root, "public", "images", "photos"),
        os.path.join(gallery_root, "public", "images", "thumbnails"),
    ]
    
    for directory in directories:
        cg_common.ensure_directory_exists(directory)

    # Copy template files (we'll create them)
    cg_common.log("Setting up gallery template files...")
    
    # Move all images and videos to the correct subfolder under public
    photos_dir = os.path.join(gallery_root, "public", "images", "photos")
    cg_common.log(f"Moving all photos and videos to {photos_dir}...")

    only_copy = True
    if not image_source:
        image_source = gallery_root
        only_copy = False
        
    for path in glob.glob(os.path.join(image_source, "*")):
        basename_lower = os.path.basename(path).lower()
        if (
            basename_lower.endswith(".jpg")
            or basename_lower.endswith(".jpeg")
            or basename_lower.endswith(".gif")
            or basename_lower.endswith(".mp4")
            or basename_lower.endswith(".png")
            or basename_lower.endswith(".webp")
        ):
            if only_copy:
                shutil.copy(path, os.path.join(photos_dir, os.path.basename(path)))
            else:
                shutil.move(path, os.path.join(photos_dir, os.path.basename(path)))


def create_gallery_json(gallery_root: str, remote_link: str = "", use_defaults: bool = False) -> None:
    """
    Creates a new gallery.json file with dark urban theme defaults
    :param gallery_root: Path to the gallery root
    :param remote_link: Optional link to a remote shared album
    :param use_defaults: If set to True, there will be no questions asked
    """
    cg_common.log("Creating the gallery config...")
    
    # Initialize the gallery config with dark urban theme
    gallery_config = {
        "images_data_file": os.path.join(gallery_root, "images_data.json"),
        "public_path": os.path.join(gallery_root, "public"),
        "templates_path": os.path.join(gallery_root, "templates"),
        "images_path": os.path.join(gallery_root, "public", "images", "photos"),
        "thumbnails_path": os.path.join(gallery_root, "public", "images", "thumbnails"),
        "thumbnail_height": 160,
        "title": "City 16-9",
        "description": "Urban photography collection showcasing the beauty of city life in cinematic 16:9 format",
        "background_photo": "",
        "url": "",
        "background_photo_offset": 30,
        "disable_captions": False,
        "dark_theme": True,
        "urban_style": True,
    }

    # Initialize remote gallery configuration
    if remote_link:
        # Simple remote gallery type detection
        if "onedrive.live.com/" in remote_link or "1drv.ms/" in remote_link:
            gallery_config["remote_gallery_type"] = "onedrive"
        elif "photos.app.goo.gl/" in remote_link or "photos.google.com" in remote_link:
            gallery_config["remote_gallery_type"] = "google"
        else:
            gallery_config["remote_gallery_type"] = "unknown"
        
        gallery_config["remote_link"] = remote_link

    # Set configuration defaults
    default_title = "City 16-9"
    default_description = "Urban photography collection showcasing the beauty of city life in cinematic 16:9 format"

    # If defaults are not used, ask the user to provide input
    if not use_defaults:
        gallery_config["title"] = (
            input(f'What is the title of your gallery? (default: "{default_title}")\n')
            or gallery_config["title"]
        )

        gallery_config["description"] = (
            input(
                f'What is the description of your gallery? (default: "{default_description}")\n'
            )
            or gallery_config["description"]
        )

        gallery_config["background_photo"] = input(
            f'Which image should be used as background for the header? (default: "")\n'
        )

        gallery_config["url"] = input(
            f'What is your site URL? (default: "")\n'
        )

    # Save the configuration to a file
    gallery_config_path = os.path.join(gallery_root, "gallery.json")
    if cg_common.write_gallery_config(gallery_config_path, gallery_config):
        cg_common.log("Gallery config stored in gallery.json")
    else:
        raise cg_common.CityGalleryException("Failed to write gallery configuration")


def main():
    """
    Initializes a new City 16-9 Gallery in a specified folder
    """
    # Parse the arguments
    args = parse_args()

    # Get the gallery root from the arguments
    gallery_root = args.path

    # Get the image source directory
    image_source = args.image_source

    # Check if a gallery can be created at this location
    if not check_if_gallery_creation_possible(gallery_root):
        sys.exit(1)

    # Check if the specified gallery root already contains a gallery
    if check_if_gallery_already_exists(gallery_root):
        if not args.force:
            cg_common.log(
                "A City 16-9 Gallery already exists at the specified location. Set the --force parameter "
                "if you want to overwrite it."
            )
            sys.exit(0)
        else:
            cg_common.log(
                "A City 16-9 Gallery already exists at the specified location, but will be overwritten."
            )
    
    cg_common.log("Creating a City 16-9 Gallery...")

    # Create the gallery json file
    try:
        if not args.keep_gallery_config:
            create_gallery_json(gallery_root, args.remote_link, args.use_defaults)
    except cg_common.CityGalleryException as exception:
        cg_common.log(exception.message)
        sys.exit(1)
    except Exception as exception:
        cg_common.log(
            f"Something went wrong while creating the gallery.json file: {str(exception)}"
        )
        sys.exit(1)

    # Copy the template files to the gallery root
    try:
        create_gallery_folder_structure(gallery_root, image_source)
    except Exception as exception:
        cg_common.log(
            f"Something went wrong while generating the gallery structure: {str(exception)}"
        )
        sys.exit(1)

    cg_common.log("City 16-9 Gallery initialized successfully!")


if __name__ == "__main__":
    main()