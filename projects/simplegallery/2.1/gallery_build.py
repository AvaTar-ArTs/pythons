"""
SimpleGallery 2.1 - Enhanced Gallery Builder
Advanced improvements: parallel processing, caching, better error handling
"""

import argparse
import os
import sys
import json
import jinja2
from collections import OrderedDict
from typing import Dict, Any

import simplegallery.common as spg_common
from simplegallery.logic.gallery_logic import get_gallery_logic

# Import 2.1 enhancements (with fallback)
try:
    from simplegallery.config_validator import ConfigValidator
    from simplegallery.logger import get_logger, LogLevel

    ENHANCED_LOGGING = True
except ImportError:
    # Fallback for compatibility
    ENHANCED_LOGGING = False
    ConfigValidator = None

    class LogLevel:
        INFO = "INFO"

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

            def critical(self, msg):
                print(f"CRITICAL: {msg}")

        return SimpleLogger()


def parse_args():
    """
    Configures the argument parser with enhanced options
    :return: Parsed arguments
    """
    description = """SimpleGallery 2.1 - Advanced Photo Gallery Builder
    Generates all files needed to display the gallery (thumbnails, image descriptions and HTML page).
    Enhanced with parallel processing, caching, and improved error handling."""

    parser = argparse.ArgumentParser(
        description=description, formatter_class=argparse.RawDescriptionHelpFormatter
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
        "--no-cache",
        dest="no_cache",
        action="store_true",
        help="Disable caching for this build",
    )

    parser.add_argument(
        "--no-parallel",
        dest="no_parallel",
        action="store_true",
        help="Disable parallel processing (use single-threaded mode)",
    )

    parser.add_argument(
        "--dry-run",
        dest="dry_run",
        action="store_true",
        help="Perform a dry run without making changes",
    )

    return parser.parse_args()


def build_html(gallery_config: Dict[str, Any], logger) -> None:
    """
    Generates the HTML file (index.html) of the gallery
    Enhanced with better error handling and validation

    :param gallery_config: Gallery configuration dictionary
    :param logger: Logger instance
    """
    try:
        # Load the images_data
        images_data_file = gallery_config["images_data_file"]
        if not os.path.exists(images_data_file):
            raise spg_common.SPGException(
                f"Images data file not found: {images_data_file}"
            )

        with open(images_data_file, "r", encoding="utf-8") as images_data_in:
            images_data = json.load(images_data_in, object_pairs_hook=OrderedDict)

        logger.debug(f"Loaded {len(images_data)} images from {images_data_file}")

        # Remove descriptions if the corresponding option is enabled
        if gallery_config.get("disable_captions", False):
            for image in images_data:
                images_data[image]["description"] = ""
            logger.debug("Captions disabled")

        images_data_list = [
            {**images_data[image], "name": image} for image in images_data.keys()
        ]

        # Find the first photo for the background if no background photo specified
        background_photo = gallery_config.get("background_photo", "")
        if not background_photo:
            for image in images_data:
                if images_data[image].get("type") == "image":
                    background_photo = image
                    break
            if background_photo:
                logger.debug(f"Auto-selected background photo: {background_photo}")

        # Extract parent folder name for title if title matches folder name
        gallery_root = os.path.dirname(gallery_config["images_data_file"])
        parent_folder_name = os.path.basename(os.path.abspath(gallery_root))

        # Use parent folder name as title if title matches folder name
        if gallery_config.get("title") == parent_folder_name:
            gallery_config["title"] = parent_folder_name

        # Set description to empty so it doesn't show in the <p> tag
        gallery_config["description"] = ""

        # Collect the information for a remote gallery attribution
        remote_data = {}
        if "remote_gallery_type" in gallery_config and "remote_link" in gallery_config:
            remote_data["link"] = gallery_config["remote_link"]

            if gallery_config["remote_gallery_type"] == "google":
                remote_data["text"] = "Google Photos album"
            elif gallery_config["remote_gallery_type"] == "onedrive":
                remote_data["text"] = "OneDrive album"
            else:
                remote_data["text"] = "shared album"

        # Setup the jinja2 environment
        templates_path = gallery_config["templates_path"]
        if not os.path.exists(templates_path):
            raise spg_common.SPGException(
                f"Templates path does not exist: {templates_path}"
            )

        file_loader = jinja2.FileSystemLoader(templates_path)
        env = jinja2.Environment(loader=file_loader)

        # Get template name (support for themes)
        template_name = gallery_config.get("template_theme", "index_template.jinja")
        if not template_name.endswith(".jinja"):
            template_name = f"{template_name}_template.jinja"
        if not os.path.exists(os.path.join(templates_path, template_name)):
            template_name = "index_template.jinja"  # Fallback to default

        logger.debug(f"Using template: {template_name}")

        # Render the HTML template
        template = env.get_template(template_name)
        html = template.render(
            images=images_data_list,
            gallery_config=gallery_config,
            background_photo=background_photo,
            remote_data=remote_data,
        )

        # Write the HTML file
        public_path = gallery_config["public_path"]
        os.makedirs(public_path, exist_ok=True)

        output_file = os.path.join(public_path, "index.html")
        with open(output_file, "w", encoding="utf-8") as out:
            out.write(html)

        logger.info(f"HTML generated successfully: {output_file}")

    except FileNotFoundError as e:
        raise spg_common.SPGException(f"File not found: {e}")
    except json.JSONDecodeError as e:
        raise spg_common.SPGException(f"Invalid JSON in images_data.json: {e}")
    except jinja2.TemplateNotFound as e:
        raise spg_common.SPGException(f"Template not found: {e}")
    except Exception as e:
        raise spg_common.SPGException(f"Error building HTML: {str(e)}")


def main():
    """
    Main entry point for SimpleGallery 2.1 build process
    Enhanced with validation, better error handling, and progress tracking
    """
    # Parse arguments
    args = parse_args()

    # Initialize logger
    logger = get_logger(verbose=args.verbose)

    if args.dry_run:
        logger.info("🔍 DRY RUN MODE - No changes will be made")

    # Read the gallery config
    gallery_root = args.path
    gallery_config_path = os.path.join(gallery_root, "gallery.json")

    if not os.path.exists(gallery_config_path):
        logger.error(f"Gallery config not found: {gallery_config_path}")
        logger.info("💡 Tip: Run 'gallery-init' first to create a new gallery")
        sys.exit(1)

    gallery_config = spg_common.read_gallery_config(gallery_config_path)
    if not gallery_config:
        logger.error(f"Cannot load the gallery.json file ({gallery_config_path})!")
        sys.exit(1)

    # Migrate and validate configuration (if available)
    if ConfigValidator:
        logger.debug("Validating configuration...")
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
    else:
        # Basic validation fallback
        gallery_root_path = os.path.dirname(gallery_config["images_data_file"])
        parent_folder_name = os.path.basename(os.path.abspath(gallery_root_path))
        if gallery_config.get("title") == parent_folder_name:
            gallery_config["title"] = parent_folder_name
        gallery_config["description"] = ""

    # Apply CLI overrides
    if args.no_cache:
        gallery_config["cache_enabled"] = False
        logger.debug("Caching disabled via CLI")

    if args.no_parallel:
        gallery_config["parallel_processing"] = False
        logger.debug("Parallel processing disabled via CLI")

    if args.verbose:
        gallery_config["verbose"] = True

    logger.info("🚀 Building SimpleGallery 2.1...")
    logger.debug(f"Gallery root: {gallery_root}")
    logger.debug(f"Configuration: {json.dumps(gallery_config, indent=2)}")

    if args.dry_run:
        logger.info("✅ Dry run completed - configuration is valid")
        return

    # Get the gallery logic
    try:
        gallery_logic = get_gallery_logic(gallery_config)
        logger.debug("Gallery logic initialized")
    except Exception as e:
        logger.error(f"Failed to initialize gallery logic: {e}")
        sys.exit(1)

    # Generate thumbnails
    try:
        logger.info("📸 Generating thumbnails...")
        gallery_logic.create_thumbnails(args.force_thumbnails)
        logger.info("✅ Thumbnails generated successfully")
    except spg_common.SPGException as e:
        logger.error(f"❌ {e.message}")
        sys.exit(1)
    except Exception as e:
        logger.error(f"❌ Error generating thumbnails: {str(e)}")
        if args.verbose:
            import traceback

            logger.debug(traceback.format_exc())
        sys.exit(1)

    # Generate the images_data.json
    try:
        logger.info("📝 Generating images_data.json...")
        gallery_logic.create_images_data_file()
        logger.info("✅ Images data file generated successfully")
        logger.info("💡 Tip: Edit images_data.json to add custom descriptions")
    except spg_common.SPGException as e:
        logger.error(f"❌ {e.message}")
        sys.exit(1)
    except Exception as e:
        logger.error(f"❌ Error generating images_data.json: {str(e)}")
        if args.verbose:
            import traceback

            logger.debug(traceback.format_exc())
        sys.exit(1)

    # Build the HTML from the templates
    try:
        logger.info("🎨 Creating index.html...")
        build_html(gallery_config, logger)
        logger.info("✅ HTML generated successfully")
    except spg_common.SPGException as e:
        logger.error(f"❌ {e.message}")
        sys.exit(1)
    except Exception as e:
        logger.error(f"❌ Error generating HTML: {str(e)}")
        if args.verbose:
            import traceback

            logger.debug(traceback.format_exc())
        sys.exit(1)

    # Success message
    public_path = gallery_config.get(
        "public_path", os.path.join(gallery_root, "public")
    )
    index_path = os.path.join(public_path, "index.html")
    logger.info("")
    logger.info("🎉 Gallery built successfully!")
    logger.info(f"📂 Open {index_path} to view your gallery")
    logger.info("")


if __name__ == "__main__":
    main()
