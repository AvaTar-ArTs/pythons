"""
SimpleGallery 2.1 - Large Gallery Builder
Optimized for galleries with 2,500+ images
Features: Pagination, Search, Albums, Performance optimizations
"""

import argparse
import os
import sys
import json
import jinja2
from collections import OrderedDict
from typing import Dict, Any, List

import simplegallery.common as spg_common
from simplegallery.logic.gallery_logic import get_gallery_logic

# Import 2.1 enhancements
try:
    from simplegallery.config_validator import ConfigValidator
    from simplegallery.logger import get_logger

    ENHANCED_LOGGING = True
except ImportError:
    ENHANCED_LOGGING = False
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
    """Parse command line arguments for large gallery build"""
    parser = argparse.ArgumentParser(
        description="SimpleGallery 2.1 - Large Gallery Builder (2,500+ images)"
    )

    parser.add_argument(
        "-p",
        "--path",
        dest="path",
        action="store",
        default=".",
        help="Path to the folder containing the gallery.json file",
    )

    parser.add_argument(
        "-ft",
        "--force-thumbnails",
        dest="force_thumbnails",
        action="store_true",
        help="Forces the generation of the thumbnails even if they already exist",
    )

    parser.add_argument(
        "-v",
        "--verbose",
        dest="verbose",
        action="store_true",
        help="Enable verbose/debug logging",
    )

    parser.add_argument(
        "--images-per-page",
        dest="images_per_page",
        type=int,
        default=100,
        help="Number of images per page (default: 100)",
    )

    parser.add_argument(
        "--enable-search",
        dest="enable_search",
        action="store_true",
        default=True,
        help="Enable search functionality (default: True)",
    )

    parser.add_argument(
        "--enable-albums",
        dest="enable_albums",
        action="store_true",
        help="Enable album/category organization",
    )

    return parser.parse_args()


def create_albums_from_folders(:
    images_data: Dict[str, Any], images_path: str
) -> Dict[str, List[str]]:
    """
    Create albums based on folder structure
    :param images_data: Images data dictionary
    :param images_path: Path to images directory
    :return: Dictionary mapping album names to image lists
    """
    albums = {}

    # Group images by subdirectory if they exist
    for image_name, image_data in images_data.items():
        # Check if image has a subdirectory path
        if "/" in image_name:
            parts = image_name.split("/")
            if len(parts) > 1:
                album_name = parts[0]
                if album_name not in albums:
                    albums[album_name] = []
                albums[album_name].append(image_name)
        else:
            # Default album
            if "All Images" not in albums:
                albums["All Images"] = []
            albums["All Images"].append(image_name)

    return albums


def create_search_index(images_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Create search index for fast image lookup
    :param images_data: Images data dictionary
    :return: Search index dictionary
    """
    index = {"by_name": {}, "by_date": {}, "by_description": {}, "all_names": []}

    for image_name, image_data in images_data.items():
        # Index by name
        name_lower = image_name.lower()
        for i in range(len(name_lower)):
            prefix = name_lower[: i + 1]
            if prefix not in index["by_name"]:
                index["by_name"][prefix] = []
            index["by_name"][prefix].append(image_name)

        # Index by date
        if image_data.get("date"):
            date_key = image_data["date"][:7]  # YYYY-MM
            if date_key not in index["by_date"]:
                index["by_date"][date_key] = []
            index["by_date"][date_key].append(image_name)

        # Index by description
        if image_data.get("description"):
            desc_lower = image_data["description"].lower()
            words = desc_lower.split()
            for word in words:
                if len(word) > 2:  # Only index words longer than 2 chars
                    if word not in index["by_description"]:
                        index["by_description"][word] = []
                    index["by_description"][word].append(image_name)

        index["all_names"].append(image_name)

    return index


def paginate_images(:
    images_data_list: List[Dict], images_per_page: int = 100
) -> List[List[Dict]]:
    """
    Paginate images into chunks
    :param images_data_list: List of image data dictionaries
    :param images_per_page: Number of images per page
    :return: List of pages (each page is a list of images)
    """
    pages = []
    for i in range(0, len(images_data_list), images_per_page):
        pages.append(images_data_list[i : i + images_per_page])
    return pages


def build_large_gallery_html(:
    gallery_config: Dict[str, Any],
    logger,
    images_per_page: int = 100,
    enable_search: bool = True,
    enable_albums: bool = False,
) -> None:
    """
    Build HTML for large gallery with pagination and search
    :param gallery_config: Gallery configuration
    :param logger: Logger instance
    :param images_per_page: Images per page
    :param enable_search: Enable search functionality
    :param enable_albums: Enable album organization
    """
    try:
        # Load images data
        images_data_file = gallery_config["images_data_file"]
        if not os.path.exists(images_data_file):
            raise spg_common.SPGException(
                f"Images data file not found: {images_data_file}"
            )

        with open(images_data_file, "r", encoding="utf-8") as f:
            images_data = json.load(f, object_pairs_hook=OrderedDict)

        logger.info(f"Loaded {len(images_data)} images")

        # Convert to list format
        images_data_list = [
            {**images_data[image], "name": image} for image in images_data.keys()
        ]

        # Create search index
        search_index = None
        if enable_search:
            logger.info("Creating search index...")
            search_index = create_search_index(images_data)
            logger.info("Search index created")

        # Create albums if enabled
        albums = None
        if enable_albums:
            logger.info("Creating albums from folder structure...")
            albums = create_albums_from_folders(
                images_data, gallery_config["images_path"]
            )
            logger.info(f"Created {len(albums)} albums")

        # Paginate images
        logger.info(f"Paginating images ({images_per_page} per page)...")
        pages = paginate_images(images_data_list, images_per_page)
        logger.info(f"Created {len(pages)} pages")

        # Extract parent folder name for title
        gallery_root = os.path.dirname(gallery_config["images_data_file"])
        parent_folder_name = os.path.basename(os.path.abspath(gallery_root))

        if gallery_config.get("title") == parent_folder_name:
            gallery_config["title"] = parent_folder_name

        gallery_config["description"] = ""

        # Find background photo
        background_photo = gallery_config.get("background_photo", "")
        if not background_photo:
            for image in images_data:
                if images_data[image].get("type") == "image":
                    background_photo = image
                    break

        # Remote gallery data
        remote_data = {}
        if "remote_gallery_type" in gallery_config and "remote_link" in gallery_config:
            remote_data["link"] = gallery_config["remote_link"]
            if gallery_config["remote_gallery_type"] == "google":
                remote_data["text"] = "Google Photos album"
            elif gallery_config["remote_gallery_type"] == "onedrive":
                remote_data["text"] = "OneDrive album"
            else:
                remote_data["text"] = "shared album"

        # Setup Jinja2 environment
        templates_path = gallery_config["templates_path"]
        if not os.path.exists(templates_path):
            raise spg_common.SPGException(
                f"Templates path does not exist: {templates_path}"
            )

        file_loader = jinja2.FileSystemLoader(templates_path)
        env = jinja2.Environment(loader=file_loader)

        # Use large gallery template if available, fallback to default
        template_name = "large_gallery_template.jinja"
        if not os.path.exists(os.path.join(templates_path, template_name)):
            template_name = "index_template.jinja"

        logger.debug(f"Using template: {template_name}")

        # Render HTML
        template = env.get_template(template_name)
        html = template.render(
            images=images_data_list,  # All images for search/index
            pages=pages,  # Paginated images
            gallery_config=gallery_config,
            background_photo=background_photo,
            remote_data=remote_data,
            search_index=search_index,
            albums=albums,
            images_per_page=images_per_page,
            enable_search=enable_search,
            enable_albums=enable_albums,
            total_images=len(images_data_list),
            total_pages=len(pages),
        )

        # Write HTML file
        public_path = gallery_config["public_path"]
        os.makedirs(public_path, exist_ok=True)

        output_file = os.path.join(public_path, "index.html")
        with open(output_file, "w", encoding="utf-8") as out:
            out.write(html)

        # Save search index as JSON for client-side use
        if search_index and enable_search:
            search_index_file = os.path.join(public_path, "search_index.json")
            with open(search_index_file, "w", encoding="utf-8") as f:
                json.dump(search_index, f, indent=2)
            logger.info(f"Search index saved: {search_index_file}")

        # Save albums as JSON
        if albums and enable_albums:
            albums_file = os.path.join(public_path, "albums.json")
            with open(albums_file, "w", encoding="utf-8") as f:
                json.dump(albums, f, indent=2)
            logger.info(f"Albums saved: {albums_file}")

        logger.info(f"✅ Large gallery HTML generated: {output_file}")

    except Exception as e:
        raise spg_common.SPGException(f"Error building large gallery HTML: {str(e)}")


def main():
    """Main entry point for large gallery build"""
    args = parse_args()
    logger = get_logger(verbose=args.verbose)

    # Read gallery config
    gallery_root = args.path
    gallery_config_path = os.path.join(gallery_root, "gallery.json")

    if not os.path.exists(gallery_config_path):
        logger.error(f"Gallery config not found: {gallery_config_path}")
        sys.exit(1)

    gallery_config = spg_common.read_gallery_config(gallery_config_path)
    if not gallery_config:
        logger.error(f"Cannot load gallery.json: {gallery_config_path}")
        sys.exit(1)

    # Migrate and validate
    if ConfigValidator:
        gallery_config = ConfigValidator.migrate_config(
            gallery_config, from_version="2.0"
        )
        gallery_config = ConfigValidator.apply_defaults(gallery_config, gallery_root)
        is_valid, errors = ConfigValidator.validate_config(gallery_config, gallery_root)
        if not is_valid:
            logger.error("Configuration validation failed:")
            for error in errors:
                logger.error(f"  - {error}")
            sys.exit(1)

    logger.info("🚀 Building Large Gallery (2,500+ images optimized)...")

    # Get gallery logic
    try:
        gallery_logic = get_gallery_logic(gallery_config)
    except Exception as e:
        logger.error(f"Failed to initialize gallery logic: {e}")
        sys.exit(1)

    # Generate thumbnails
    try:
        logger.info("📸 Generating thumbnails...")
        gallery_logic.create_thumbnails(args.force_thumbnails)
        logger.info("✅ Thumbnails generated")
    except spg_common.SPGException as e:
        logger.error(f"❌ {e.message}")
        sys.exit(1)
    except Exception as e:
        logger.error(f"❌ Error generating thumbnails: {str(e)}")
        if args.verbose:
            import traceback

            logger.debug(traceback.format_exc())
        sys.exit(1)

    # Generate images_data.json
    try:
        logger.info("📝 Generating images_data.json...")
        gallery_logic.create_images_data_file()
        logger.info("✅ Images data generated")
    except Exception as e:
        logger.error(f"❌ Error generating images_data.json: {e}")
        sys.exit(1)

    # Build large gallery HTML
    try:
        logger.info("🎨 Creating large gallery HTML...")
        build_large_gallery_html(
            gallery_config,
            logger,
            images_per_page=args.images_per_page,
            enable_search=args.enable_search,
            enable_albums=args.enable_albums,
        )
        logger.info("✅ Large gallery HTML generated")
    except Exception as e:
        logger.error(f"❌ Error generating HTML: {e}")
        sys.exit(1)

    logger.info("")
    logger.info("🎉 Large gallery built successfully!")
    logger.info(f"📂 Open {gallery_config['public_path']}/index.html to view")
    logger.info("")


if __name__ == "__main__":
    main()
