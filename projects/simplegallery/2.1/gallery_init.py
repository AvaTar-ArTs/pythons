"""
SimpleGallery 2.1 - Enhanced Gallery Initialization
With configuration wizard and better defaults
"""

import argparse
import os
import sys
import json
import shutil


# Import 2.1 enhancements
try:
    from simplegallery.config_validator import ConfigValidator
    from simplegallery.logger import get_logger

    ENHANCED = True
except ImportError:
    ENHANCED = False
    ConfigValidator = None

    def get_logger(verbose=False):
        class SimpleLogger:
            def debug(self, msg):
                pass

            def info(self, msg):
                print(msg)

            def warning(self, msg):
                print(f"WARNING: {msg}")

            def error(self, msg):
                print(f"ERROR: {msg}")

        return SimpleLogger()


def parse_args():
    """Parse command line arguments"""
    parser = argparse.ArgumentParser(
        description="SimpleGallery 2.1 - Initialize a new photo gallery"
    )

    parser.add_argument(
        "-p",
        "--path",
        dest="path",
        action="store",
        default=".",
        help="Path where the gallery should be created",
    )

    parser.add_argument(
        "--use-defaults",
        dest="use_defaults",
        action="store_true",
        help="Use default values for all configuration options",
    )

    parser.add_argument(
        "--force",
        dest="force",
        action="store_true",
        help="Overwrite existing gallery if it exists",
    )

    parser.add_argument(
        "-v",
        "--verbose",
        dest="verbose",
        action="store_true",
        help="Enable verbose logging",
    )

    parser.add_argument(
        "--wizard",
        dest="wizard",
        action="store_true",
        help="Run interactive configuration wizard",
    )

    return parser.parse_args()


def create_gallery_structure(gallery_root: str, logger) -> None:
    """
    Create gallery directory structure
    :param gallery_root: Root directory for gallery
    :param logger: Logger instance
    """
    directories = [
        "public",
        "public/images",
        "public/images/photos",
        "public/images/thumbnails",
        "templates",
        "public/css",
        "public/js",
    ]

    for directory in directories:
        dir_path = os.path.join(gallery_root, directory)
        os.makedirs(dir_path, exist_ok=True)
        logger.debug(f"Created directory: {directory}")


def copy_template_files(gallery_root: str, source_templates: str, logger) -> None:
    """
    Copy template files to gallery
    :param gallery_root: Gallery root directory
    :param source_templates: Source templates directory
    :param logger: Logger instance
    """
    templates_dest = os.path.join(gallery_root, "templates")

    # Copy template files
    template_files = [
        "index_template.jinja",
        "gallery_macros.jinja",
    ]

    for template_file in template_files:
        src = os.path.join(source_templates, template_file)
        dst = os.path.join(templates_dest, template_file)

        if os.path.exists(src):
            shutil.copy2(src, dst)
            logger.debug(f"Copied template: {template_file}")
        else:
            logger.warning(f"Template not found: {template_file}")


def create_gallery_config(:
    gallery_root: str, use_defaults: bool = False, wizard: bool = False, logger=None
) -> dict:
    """
    Create gallery configuration
    :param gallery_root: Gallery root directory
    :param use_defaults: Use default values
    :param wizard: Run interactive wizard
    :param logger: Logger instance
    :return: Configuration dictionary
    """
    default_title = os.path.basename(os.path.abspath(gallery_root))

    if use_defaults:
        config = {
            "images_data_file": os.path.join(gallery_root, "images_data.json"),
            "public_path": os.path.join(gallery_root, "public"),
            "templates_path": os.path.join(gallery_root, "templates"),
            "images_path": os.path.join(gallery_root, "public", "images", "photos"),
            "thumbnails_path": os.path.join(
                gallery_root, "public", "images", "thumbnails"
            ),
            "thumbnail_height": 160,
            "title": default_title,
            "description": "",
            "background_photo": "",
            "url": "",
            "background_photo_offset": 30,
            "disable_captions": False,
            "disable_right_click": False,
            "template_theme": "default",
            "parallel_processing": True,
            "cache_enabled": True,
        }
    else:
        # Interactive mode (simplified for now)
        config = {
            "images_data_file": os.path.join(gallery_root, "images_data.json"),
            "public_path": os.path.join(gallery_root, "public"),
            "templates_path": os.path.join(gallery_root, "templates"),
            "images_path": os.path.join(gallery_root, "public", "images", "photos"),
            "thumbnails_path": os.path.join(
                gallery_root, "public", "images", "thumbnails"
            ),
            "thumbnail_height": 160,
            "title": default_title,
            "description": "",
            "background_photo": "",
            "url": "",
            "background_photo_offset": 30,
            "disable_captions": False,
            "disable_right_click": False,
            "template_theme": "default",
            "parallel_processing": True,
            "cache_enabled": True,
        }

    # Apply defaults using validator if available
    if ConfigValidator:
        config = ConfigValidator.apply_defaults(config, gallery_root)

    return config


def main():
    """Main entry point for gallery initialization"""
    args = parse_args()
    logger = get_logger(verbose=args.verbose)

    gallery_root = os.path.abspath(args.path)

    # Check if gallery already exists
    gallery_json_path = os.path.join(gallery_root, "gallery.json")
    if os.path.exists(gallery_json_path) and not args.force:
        logger.error(f"A Simple Photo Gallery already exists at {gallery_root}")
        logger.info("Use --force to overwrite the existing gallery")
        sys.exit(1)

    logger.info("Creating a Simple Photo Gallery...")
    logger.debug(f"Gallery root: {gallery_root}")

    # Create directory structure
    logger.info("Creating gallery structure...")
    create_gallery_structure(gallery_root, logger)

    # Copy template files
    logger.info("Copying template files...")
    # Find source templates (from package or current directory)
    source_templates = None
    possible_paths = [
        os.path.join(os.path.dirname(__file__), "data", "templates"),
        os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "templates"),
        "data/templates",
    ]

    for path in possible_paths:
        if os.path.exists(path):
            source_templates = path
            break

    if source_templates:
        copy_template_files(gallery_root, source_templates, logger)
    else:
        logger.warning("Template files not found - you may need to copy them manually")

    # Create gallery configuration
    logger.info("Creating gallery config...")
    gallery_config = create_gallery_config(
        gallery_root, use_defaults=args.use_defaults, wizard=args.wizard, logger=logger
    )

    # Save configuration
    with open(gallery_json_path, "w", encoding="utf-8") as gallery_out:
        json.dump(gallery_config, gallery_out, indent=4, separators=(",", ": "))

    logger.info("Gallery config stored in gallery.json")

    # Move existing photos to public/images/photos
    photos_path = gallery_config["images_path"]
    existing_photos = []

    # Look for common image/video extensions
    extensions = [
        ".jpg",
        ".jpeg",
        ".png",
        ".gif",
        ".bmp",
        ".mp4",
        ".mov",
        ".avi",
        ".webm",
    ]

    for file in os.listdir(gallery_root):
        file_path = os.path.join(gallery_root, file)
        if os.path.isfile(file_path):
            _, ext = os.path.splitext(file.lower())
            if ext in extensions:
                existing_photos.append(file_path)

    if existing_photos:
        logger.info(f"Moving {len(existing_photos)} photos to {photos_path}...")
        for photo in existing_photos:
            dest = os.path.join(photos_path, os.path.basename(photo))
            shutil.move(photo, dest)
        logger.info("Photos moved successfully")

    logger.info("")
    logger.info("✅ Simple Photo Gallery initialized successfully!")
    logger.info(f"📂 Gallery location: {gallery_root}")
    logger.info("")
    logger.info("Next steps:")
    logger.info("  1. Add your photos to: public/images/photos/")
    logger.info("  2. Run: gallery-build -p " + gallery_root)
    logger.info("")


if __name__ == "__main__":
    main()
