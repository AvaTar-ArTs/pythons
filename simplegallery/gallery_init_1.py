import argparse
import importlib.resources
import os
import sys
import glob
import shutil
import json
from distutils.dir_util import copy_tree
import simplegallery.common as spg_common
import simplegallery.logic.gallery_logic as gallery_logic


def parse_args():
    """
    Configures the argument parser.
    :return: Parsed arguments
    """
    description = (
        "Initializes a new Simple Photo Gallery in the specified folder "
        "(default is the current folder).\n"
        "For detailed documentation please refer to "
        "https://github.com/haltakov/simple-photo-gallery"
    )

    parser = argparse.ArgumentParser(description=description)

    parser.add_argument(
        "remote_link",
        metavar="URL",
        nargs="?",
        default="",
        help=(
            "Link to a remote shared album "
            "(OneDrive or Google Photos supported)"
        ),
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
        help=(
            "Path to a directory from where the images should be copied "
            "into the gallery."
        ),
    )

    parser.add_argument(
        "--force",
        dest="force",
        action="store_true",
        help="Overrides existing config and template files files",
    )

    parser.add_argument(
        "--keep-gallery-config",
        dest="keep_gallery_config",
        action="store_true",
        help=(
            "Use to copy the template files only, without generating a "
            "gallery.json"
        ),
    )

    parser.add_argument(
        "--use-defaults",
        dest="use_defaults",
        action="store_true",
        help="Skip the questions on the console and use defaults",
    )

    return parser.parse_args()


def check_if_gallery_creation_possible(gallery_root):
    """
    Checks if a gallery can be created in the specified folder.
    :param gallery_root: Root of the new gallery
    :return: True if a new gallery can be created and false otherwise
    """
    if not os.path.exists(gallery_root):
        spg_common.log(
            f"The specified gallery path does not exist: {gallery_root}."
        )
        return False
    return True


def check_if_gallery_already_exists(gallery_root):
    """
    Checks if a gallery already exists in the specified folder.
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


def create_gallery_folder_structure(gallery_root, image_source):
    """
    Creates the gallery folder structure by copying all the gallery templates
    and moving all images and videos to the photos subfolder.
    :param gallery_root: Path to the gallery root
    """
    spg_common.log("Copying gallery template files...")
    copy_tree(
        importlib.resources.files("simplegallery") / "data/templates",
        os.path.join(gallery_root, "templates"),
    )
    copy_tree(
        importlib.resources.files("simplegallery") / "data/public",
        os.path.join(gallery_root, "public"),
    )

    photos_dir = os.path.join(gallery_root, "public", "images", "photos")
    spg_common.log(f"Moving all photos and videos to {photos_dir}...")

    only_copy = True
    if not image_source:
        image_source = gallery_root
        only_copy = False

    for path in glob.glob(os.path.join(image_source, "*")):
        basename_lower = os.path.basename(path).lower()
        if basename_lower.endswith((".jpg", ".jpeg", ".gif", ".mp4", ".png")):
            dest = os.path.join(photos_dir, os.path.basename(path))
            if only_copy:
                shutil.copy(path, dest)
            else:
                shutil.move(path, dest)


def create_gallery_json(gallery_root, remote_link, use_defaults=False):
    """
    Creates a new gallery.json file, based on settings specified by the user.
    :param gallery_root: Path to the gallery root
    :param remote_link: Optional link to a remote shared album containing the photos for the gallery
    :param use_defaults: If set to True, there will be no questions asked on the console
    """
    spg_common.log("Creating the gallery config...")
    spg_common.log(
        "You can answer the following questions in order to set some important "
        "gallery properties. You can also just press Enter to leave the default "
        "and change it later in the gallery.json file."
    )

    gallery_config = dict(
        images_data_file=os.path.join(gallery_root, "images_data.json"),
        public_path=os.path.join(gallery_root, "public"),
        templates_path=os.path.join(gallery_root, "templates"),
        images_path=os.path.join(gallery_root, "public", "images", "photos"),
        thumbnails_path=os.path.join(gallery_root, "public", "images", "thumbnails"),
        thumbnail_height=160,
        title="My Gallery",
        description="Default description of my gallery",
        background_photo="",
        url="",
        background_photo_offset=30,
        disable_captions=False,
    )

    if remote_link:
        remote_gallery_type = gallery_logic.get_gallery_type(remote_link)
        if not remote_gallery_type:
            raise spg_common.SPGException(
                "Cannot initialize remote gallery - please check the provided link."
            )
        gallery_config["remote_gallery_type"] = remote_gallery_type
        gallery_config["remote_link"] = remote_link

    default_title = os.path.basename(os.path.abspath(gallery_root))

    if not use_defaults:
        user_title = input(
            f'What is the title of your gallery? (default: "{default_title}")\n'
        ).strip()
        if not user_title:
            user_title = default_title
        gallery_config["title"] = user_title

        # Remove description and URL prompts for cleaner output
        gallery_config["description"] = ""
        gallery_config["url"] = ""
        gallery_config["background_photo"] = ""
        gallery_config["background_photo_offset"] = 30

    gallery_config_path = os.path.join(gallery_root, "gallery.json")
    with open(gallery_config_path, "w", encoding="utf-8") as out:
        json.dump(gallery_config, out, indent=4, separators=(",", ": "))

    spg_common.log("Gallery config stored in gallery.json")


def main():
    """
    Initializes a new Simple Photo Gallery in a specified folder.
    """
    args = parse_args()
    gallery_root = args.path
    image_source = args.image_source

    if not check_if_gallery_creation_possible(gallery_root):
        sys.exit(1)

    if check_if_gallery_already_exists(gallery_root):
        if not args.force:
            spg_common.log(
                "A Simple Photo Gallery already exists at the specified location. "
                "Set the --force parameter if you want to overwrite it."
            )
            sys.exit(0)
        else:
            spg_common.log(
                "A Simple Photo Gallery already exists at the specified location, "
                "but will be overwritten."
            )
    spg_common.log("Creating a Simple Photo Gallery...")

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
