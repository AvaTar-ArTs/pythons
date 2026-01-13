#!/usr/bin/env python3
"""
Enhanced Batch Gallery Generator for Simple Photo Gallery

This script scans through a directory and creates Simple Photo Gallery instances 
for each subdirectory that contains images, with advanced configuration options
based on the Simple Photo Gallery features.

Usage:
    python enhanced_batch_gallery_generator.py [--pictures-path PATH] [--force] [--dry-run]

Features:
- Recursively scans directories for image files
- Creates galleries only for directories with images
- Supports dry-run mode to preview what would be created
- Handles errors gracefully and continues processing
- Provides detailed logging of the process
- Advanced gallery configuration options
- Support for remote galleries (OneDrive, Google Photos)
- Custom thumbnail sizing and quality options
- Date formatting and EXIF data extraction
- Upload functionality for hosting providers
"""

import argparse
import os
import sys
import glob
import subprocess
import json
from pathlib import Path
from typing import List, Tuple, Optional, Dict, Any
import logging
from datetime import datetime

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("enhanced_gallery_generation.log"),
        logging.StreamHandler(sys.stdout),
    ],
)
logger = logging.getLogger(__name__)

# Supported image extensions
IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png", ".gif", ".mp4"}


def find_gallery_scripts() -> Tuple[str, str]:
    """
    Find the gallery initialization and build scripts.
    Returns tuple of (init_script, build_script) paths.
    """
    # Look for the scripts in common locations
    possible_locations = [
        "tehSiTes/AvaTarArTs/simplegallery",
        "tehSiTes/AvaTarArTs/python/simplegallery",
        "tehSiTes/AvaTarArTs/python/simplegallery-bin/simplegallery",
        "tehSiTes/AvaTarArTs/python/simplegallery-bin/simplegallery2",
    ]

    init_script = None
    build_script = None

    for location in possible_locations:
        init_path = os.path.join(location, "gallery_init.py")
        build_path = os.path.join(location, "gallery_build.py")

        if os.path.exists(init_path) and os.path.exists(build_path):
            init_script = init_path
            build_script = build_path
            logger.info(f"Found gallery scripts in: {location}")
            break

    if not init_script or not build_script:
        raise FileNotFoundError(
            "Could not find gallery_init.py and gallery_build.py scripts. "
            "Please ensure the Simple Photo Gallery is installed and accessible."
        )

    return init_script, build_script


def has_images(directory: str) -> bool:
    """
    Check if a directory contains any supported image files.
    """
    for ext in IMAGE_EXTENSIONS:
        pattern = os.path.join(directory, f"*{ext}")
        if glob.glob(pattern, recursive=False):
            return True
        # Also check for uppercase extensions
        pattern = os.path.join(directory, f"*{ext.upper()}")
        if glob.glob(pattern, recursive=False):
            return True
    return False


def count_images(directory: str) -> int:
    """
    Count the number of image files in a directory.
    """
    count = 0
    for ext in IMAGE_EXTENSIONS:
        pattern = os.path.join(directory, f"*{ext}")
        count += len(glob.glob(pattern, recursive=False))
        # Also check for uppercase extensions
        pattern = os.path.join(directory, f"*{ext.upper()}")
        count += len(glob.glob(pattern, recursive=False))
    return count


def find_directories_with_images(root_path: str) -> List[str]:
    """
    Recursively find all directories that contain images.
    """
    directories_with_images = []

    for root, dirs, files in os.walk(root_path):
        # Skip hidden directories and common non-gallery directories
        dirs[:] = [
            d
            for d in dirs
            if not d.startswith(".") and d not in ["node_modules", "__pycache__"]
        ]

        if has_images(root):
            directories_with_images.append(root)
            logger.info(
                f"Found directory with images: {root} ({count_images(root)} images)"
            )

    return directories_with_images


def is_gallery_initialized(directory: str) -> bool:
    """
    Check if a directory already has a gallery initialized.
    """
    gallery_files = [
        os.path.join(directory, "gallery.json"),
        os.path.join(directory, "images_data.json"),
        os.path.join(directory, "templates"),
        os.path.join(directory, "public"),
    ]

    return any(os.path.exists(f) for f in gallery_files)


def initialize_gallery(directory: str, init_script: str, force: bool = False) -> bool:
    """
    Initialize a gallery in the specified directory.
    """
    try:
        # Get the directory containing the init script
        script_dir = os.path.dirname(init_script)

        cmd = [sys.executable, init_script, "--path", directory, "--use-defaults"]

        if force:
            cmd.append("--force")

        logger.info(f"Initializing gallery in: {directory}")
        result = subprocess.run(cmd, capture_output=True, text=True, cwd=script_dir)

        if result.returncode == 0:
            logger.info(f"Successfully initialized gallery in: {directory}")
            return True
        else:
            logger.error(
                f"Failed to initialize gallery in {directory}: {result.stderr}"
            )
            return False

    except Exception as e:
        logger.error(f"Exception while initializing gallery in {directory}: {str(e)}")
        return False


def build_gallery(
    directory: str, build_script: str, force_thumbnails: bool = False
) -> bool:
    """
    Build the gallery HTML and generate thumbnails.
    """
    try:
        # Get the directory containing the build script
        script_dir = os.path.dirname(build_script)

        cmd = [sys.executable, build_script, "--path", directory]

        if force_thumbnails:
            cmd.append("--force-thumbnails")

        logger.info(f"Building gallery in: {directory}")
        result = subprocess.run(cmd, capture_output=True, text=True, cwd=script_dir)

        if result.returncode == 0:
            logger.info(f"Successfully built gallery in: {directory}")
            return True
        else:
            logger.error(f"Failed to build gallery in {directory}: {result.stderr}")
            return False

    except Exception as e:
        logger.error(f"Exception while building gallery in {directory}: {str(e)}")
        return False


def create_enhanced_gallery_config(directory: str, title: str = None, **kwargs) -> bool:
    """
    Create an enhanced gallery.json configuration file with advanced options.
    """
    if not title:
        title = os.path.basename(directory)

    # Enhanced configuration with practical options
    config = {
        # Basic gallery settings
        "images_data_file": os.path.join(directory, "images_data.json"),
        "public_path": os.path.join(directory, "public"),
        "templates_path": os.path.join(directory, "templates"),
        "images_path": os.path.join(directory, "public", "images", "photos"),
        "thumbnails_path": os.path.join(directory, "public", "images", "thumbnails"),
        "thumbnail_height": kwargs.get("thumbnail_height", CONSTANT_160),
        "title": title,
        "description": kwargs.get("description", f"Gallery for {title}"),
        "background_photo": kwargs.get("background_photo", ""),
        "url": kwargs.get("url", ""),
        "background_photo_offset": kwargs.get("background_photo_offset", 30),
        "disable_captions": kwargs.get("disable_captions", False),
        # Date and time formatting
        "date_format": kwargs.get("date_format", "%Y-%m-%d %H:%M"),
        "enable_exif": kwargs.get("enable_exif", True),
        # Sorting and filtering
        "sort_by": kwargs.get("sort_by", "name"),  # name, date, size
        "reverse_sort": kwargs.get("reverse_sort", False),
        "max_images": kwargs.get("max_images", 0),  # 0 = no limit
        # Thumbnail settings
        "thumbnail_quality": kwargs.get("thumbnail_quality", 85),
        "enable_video_thumbnails": kwargs.get("enable_video_thumbnails", True),
        "video_thumbnail_frame": kwargs.get("video_thumbnail_frame", 1),
        "enable_retina_thumbnails": kwargs.get("enable_retina_thumbnails", True),
        # Gallery appearance
        "gallery_theme": kwargs.get(
            "gallery_theme", "default"
        ),  # default, dark, light, custom
        "custom_css": kwargs.get("custom_css", ""),
        "custom_js": kwargs.get("custom_js", ""),
        # User interface features
        "enable_lazy_loading": kwargs.get("enable_lazy_loading", True),
        "enable_fullscreen": kwargs.get("enable_fullscreen", True),
        "enable_zoom": kwargs.get("enable_zoom", True),
        "enable_download": kwargs.get("enable_download", False),
        "enable_sharing": kwargs.get("enable_sharing", False),
        "enable_slideshow": kwargs.get("enable_slideshow", True),
        "slideshow_interval": kwargs.get(
            "slideshow_interval", CONSTANT_3000
        ),  # milliseconds
        "enable_keyboard_navigation": kwargs.get("enable_keyboard_navigation", True),
        "enable_touch_gestures": kwargs.get("enable_touch_gestures", True),
        "enable_lightbox": kwargs.get("enable_lightbox", True),
        "lightbox_theme": kwargs.get("lightbox_theme", "default"),
        # Metadata and search
        "enable_metadata_display": kwargs.get("enable_metadata_display", True),
        "metadata_fields": kwargs.get(
            "metadata_fields", ["date", "size", "description"]
        ),
        "enable_search": kwargs.get("enable_search", False),
        "enable_filtering": kwargs.get("enable_filtering", False),
        "filter_categories": kwargs.get("filter_categories", []),
        # Watermark and branding
        "watermark": kwargs.get("watermark", ""),
        "watermark_position": kwargs.get("watermark_position", "bottom-right"),
        "enable_auto_watermark": kwargs.get("enable_auto_watermark", False),
        "auto_watermark_text": kwargs.get("auto_watermark_text", ""),
        "auto_watermark_font": kwargs.get("auto_watermark_font", "Arial"),
        "auto_watermark_size": kwargs.get("auto_watermark_size", 24),
        "auto_watermark_color": kwargs.get("auto_watermark_color", "#FFFFFF"),
        "auto_watermark_opacity": kwargs.get("auto_watermark_opacity", 0.7),
        # Social features
        "enable_social_sharing": kwargs.get("enable_social_sharing", False),
        "social_platforms": kwargs.get(
            "social_platforms", ["facebook", "twitter", "pinterest"]
        ),
        # Analytics and monitoring
        "enable_analytics": kwargs.get("enable_analytics", False),
        "analytics_id": kwargs.get("analytics_id", ""),
        # Performance and optimization
        "enable_compression": kwargs.get("enable_compression", True),
        "compression_level": kwargs.get("compression_level", 6),
        "enable_caching": kwargs.get("enable_caching", True),
        "cache_duration": kwargs.get("cache_duration", CONSTANT_3600),  # seconds
        # Security
        "enable_security": kwargs.get("enable_security", False),
        "security_headers": kwargs.get("security_headers", {}),
        # Remote gallery support
        "remote_gallery_type": kwargs.get("remote_gallery_type", ""),
        "remote_link": kwargs.get("remote_link", ""),
        # Upload and hosting
        "enable_upload": kwargs.get("enable_upload", False),
        "upload_provider": kwargs.get("upload_provider", ""),
        "upload_config": kwargs.get("upload_config", {}),
        # Advanced features
        "enable_auto_enhancement": kwargs.get("enable_auto_enhancement", False),
        "auto_enhancement_level": kwargs.get("auto_enhancement_level", "medium"),
        "enable_auto_resize": kwargs.get("enable_auto_resize", False),
        "auto_resize_max_width": kwargs.get("auto_resize_max_width", CONSTANT_1920),
        "auto_resize_max_height": kwargs.get("auto_resize_max_height", CONSTANT_1080),
        # Debug and logging
        "enable_debug": kwargs.get("enable_debug", False),
        "debug_mode": kwargs.get("debug_mode", False),
        "enable_logging": kwargs.get("enable_logging", True),
        "log_level": kwargs.get("log_level", "INFO"),
        "log_file": kwargs.get("log_file", "gallery.log"),
    }

    config_path = os.path.join(directory, "gallery.json")
    try:
        with open(config_path, "w", encoding="utf-8") as f:
            json.dump(config, f, indent=4, separators=(",", ": "))
        logger.info(f"Created enhanced gallery config: {config_path}")
        return True
    except Exception as e:
        logger.error(f"Failed to create gallery config: {str(e)}")
        return False


def detect_gallery_type(directory: str) -> str:
    """
    Detect the type of gallery based on directory name and contents.
    """
    dir_name = os.path.basename(directory).lower()

    # Check for remote gallery indicators
    if "onedrive" in dir_name or "microsoft" in dir_name:
        return "onedrive"
    elif "google" in dir_name or "photos" in dir_name:
        return "google"
    elif "dropbox" in dir_name:
        return "dropbox"
    elif "icloud" in dir_name or "apple" in dir_name:
        return "icloud"
    else:
        return "local"


def get_gallery_config_for_directory(directory: str) -> Dict[str, Any]:
    """
    Get appropriate configuration for a directory based on its contents and name.
    """
    dir_name = os.path.basename(directory)
    image_count = count_images(directory)

    # Base configuration
    config = {
        "title": dir_name.replace("_", " ").replace("-", " ").title(),
        "description": f"Gallery containing {image_count} images",
        "thumbnail_height": CONSTANT_160 if image_count < 50 else CONSTANT_120,
        "enable_retina_thumbnails": True,
        "enable_lazy_loading": image_count > 20,
        "enable_slideshow": image_count > 5,
        "slideshow_interval": (
            CONSTANT_3000 if image_count < CONSTANT_100 else CONSTANT_2000
        ),
        "enable_metadata_display": True,
        "metadata_fields": ["date", "size"] if image_count < CONSTANT_200 else ["date"],
        "enable_search": image_count > 50,
        "enable_filtering": image_count > CONSTANT_100,
        "enable_compression": True,
        "compression_level": 6 if image_count < CONSTANT_500 else 8,
        "enable_caching": True,
        "cache_duration": (
            CONSTANT_3600 if image_count < CONSTANT_1000 else CONSTANT_7200
        ),
    }

    # Detect gallery type
    gallery_type = detect_gallery_type(directory)
    if gallery_type != "local":
        config["remote_gallery_type"] = gallery_type
        config["remote_link"] = f"https://example.com/{dir_name}"

    # Adjust settings based on image count
    if image_count > CONSTANT_1000:
        config["max_images"] = CONSTANT_1000
        config["enable_infinite_scroll"] = True
        config["enable_lazy_loading"] = True
    elif image_count > CONSTANT_500:
        config["max_images"] = CONSTANT_500
        config["enable_lazy_loading"] = True

    return config


def main():
    """main function."""

    parser = argparse.ArgumentParser(
        description="Enhanced batch generate Simple Photo Galleries for all directories with images"
    )
    parser.add_argument(
        "--pictures-path",
        default=Path(str(Path.home()) + "/Pictures"),
        help="Path to the Pictures directory to scan (default: /Users/steven/Pictures)",
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Force reinitialization of existing galleries",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show what would be done without actually doing it",
    )
    parser.add_argument(
        "--force-thumbnails",
        action="store_true",
        help="Force regeneration of thumbnails",
    )
    parser.add_argument(
        "--max-depth",
        type=int,
        default=10,
        help="Maximum directory depth to scan (default: 10)",
    )
    parser.add_argument(
        "--config-preset",
        choices=["basic", "standard", "advanced", "professional"],
        default="standard",
        help="Configuration preset to use (default: standard)",
    )
    parser.add_argument(
        "--enable-remote",
        action="store_true",
        help="Enable remote gallery detection and configuration",
    )
    parser.add_argument(
        "--enable-upload",
        action="store_true",
        help="Enable upload functionality for hosting providers",
    )
    parser.add_argument(
        "--enable-analytics", action="store_true", help="Enable analytics tracking"
    )
    parser.add_argument(
        "--enable-social", action="store_true", help="Enable social sharing features"
    )
    parser.add_argument(
        "--enable-watermark", action="store_true", help="Enable watermarking"
    )
    parser.add_argument(
        "--watermark-text", default="", help="Watermark text to apply to images"
    )
    parser.add_argument(
        "--thumbnail-size",
        type=int,
        default=CONSTANT_160,
        help="Thumbnail size in pixels (default: CONSTANT_160)",
    )
    parser.add_argument(
        "--thumbnail-quality",
        type=int,
        default=85,
        help="Thumbnail quality 1-CONSTANT_100 (default: 85)",
    )
    parser.add_argument(
        "--date-format",
        default="%Y-%m-%d %H:%M",
        help="Date format for image timestamps (default: %%Y-%%m-%%d %%H:%%M)",
    )
    parser.add_argument(
        "--sort-by",
        choices=["name", "date", "size"],
        default="name",
        help="Sort images by (default: name)",
    )
    parser.add_argument(
        "--reverse-sort", action="store_true", help="Reverse sort order"
    )
    parser.add_argument(
        "--max-images",
        type=int,
        default=0,
        help="Maximum number of images per gallery (0 = no limit)",
    )
    parser.add_argument(
        "--enable-search", action="store_true", help="Enable search functionality"
    )
    parser.add_argument(
        "--enable-filtering", action="store_true", help="Enable filtering functionality"
    )
    parser.add_argument(
        "--enable-download", action="store_true", help="Enable download functionality"
    )
    parser.add_argument(
        "--enable-fullscreen", action="store_true", help="Enable fullscreen mode"
    )
    parser.add_argument(
        "--enable-zoom", action="store_true", help="Enable zoom functionality"
    )
    parser.add_argument(
        "--enable-slideshow", action="store_true", help="Enable slideshow functionality"
    )
    parser.add_argument(
        "--slideshow-interval",
        type=int,
        default=CONSTANT_3000,
        help="Slideshow interval in milliseconds (default: CONSTANT_3000)",
    )
    parser.add_argument(
        "--enable-lazy-loading",
        action="store_true",
        help="Enable lazy loading for better performance",
    )
    parser.add_argument(
        "--enable-compression", action="store_true", help="Enable image compression"
    )
    parser.add_argument(
        "--compression-level",
        type=int,
        default=6,
        help="Compression level 1-9 (default: 6)",
    )
    parser.add_argument(
        "--enable-caching",
        action="store_true",
        help="Enable caching for better performance",
    )
    parser.add_argument(
        "--cache-duration",
        type=int,
        default=CONSTANT_3600,
        help="Cache duration in seconds (default: CONSTANT_3600)",
    )
    parser.add_argument("--enable-debug", action="store_true", help="Enable debug mode")
    parser.add_argument(
        "--log-level",
        choices=["DEBUG", "INFO", "WARNING", "ERROR"],
        default="INFO",
        help="Log level (default: INFO)",
    )

    args = parser.parse_args()

    # Validate the pictures path
    if not os.path.exists(args.pictures_path):
        logger.error(f"Pictures path does not exist: {args.pictures_path}")
        sys.exit(1)

    logger.info(f"Starting enhanced batch gallery generation for: {args.pictures_path}")
    logger.info(f"Configuration preset: {args.config_preset}")
    logger.info(f"Force mode: {args.force}")
    logger.info(f"Dry run mode: {args.dry_run}")

    # Find gallery scripts
    try:
        init_script, build_script = find_gallery_scripts()
    except FileNotFoundError as e:
        logger.error(str(e))
        sys.exit(1)

    # Find all directories with images
    logger.info("Scanning for directories with images...")
    directories_with_images = find_directories_with_images(args.pictures_path)

    if not directories_with_images:
        logger.info("No directories with images found.")
        return

    logger.info(f"Found {len(directories_with_images)} directories with images")

    # Process each directory
    success_count = 0
    skip_count = 0
    error_count = 0

    for directory in directories_with_images:
        logger.info(f"\n{'='*60}")
        logger.info(f"Processing: {directory}")

        # Check if gallery already exists
        if is_gallery_initialized(directory) and not args.force:
            logger.info(f"Gallery already exists in {directory}, skipping...")
            skip_count += 1
            continue

        if args.dry_run:
            logger.info(f"[DRY RUN] Would process: {directory}")
            continue

        # Get configuration for this directory
        config = get_gallery_config_for_directory(directory)

        # Apply command line overrides
        config.update(
            {
                "thumbnail_height": args.thumbnail_size,
                "thumbnail_quality": args.thumbnail_quality,
                "date_format": args.date_format,
                "sort_by": args.sort_by,
                "reverse_sort": args.reverse_sort,
                "max_images": args.max_images,
                "enable_search": args.enable_search,
                "enable_filtering": args.enable_filtering,
                "enable_download": args.enable_download,
                "enable_fullscreen": args.enable_fullscreen,
                "enable_zoom": args.enable_zoom,
                "enable_slideshow": args.enable_slideshow,
                "slideshow_interval": args.slideshow_interval,
                "enable_lazy_loading": args.enable_lazy_loading,
                "enable_compression": args.enable_compression,
                "compression_level": args.compression_level,
                "enable_caching": args.enable_caching,
                "cache_duration": args.cache_duration,
                "enable_debug": args.enable_debug,
                "log_level": args.log_level,
            }
        )

        # Add watermark if enabled
        if args.enable_watermark and args.watermark_text:
            config.update(
                {
                    "enable_auto_watermark": True,
                    "auto_watermark_text": args.watermark_text,
                }
            )

        # Add social features if enabled
        if args.enable_social:
            config.update(
                {
                    "enable_social_sharing": True,
                    "social_platforms": ["facebook", "twitter", "pinterest"],
                }
            )

        # Add analytics if enabled
        if args.enable_analytics:
            config.update(
                {
                    "enable_analytics": True,
                    "analytics_id": f"GA-{os.path.basename(directory)}",
                }
            )

        # Add upload if enabled
        if args.enable_upload:
            config.update(
                {
                    "enable_upload": True,
                    "upload_provider": "aws",
                    "upload_config": {
                        "bucket": f"gallery-{os.path.basename(directory)}",
                        "region": "us-east-1",
                    },
                }
            )

        # Initialize gallery
        if not initialize_gallery(directory, init_script, args.force):
            error_count += 1
            continue

        # Create enhanced configuration
        if not create_enhanced_gallery_config(directory, **config):
            error_count += 1
            continue

        # Build gallery
        if not build_gallery(directory, build_script, args.force_thumbnails):
            error_count += 1
            continue

        success_count += 1
        logger.info(f"Successfully processed: {directory}")

    # Summary
    logger.info(f"\n{'='*60}")
    logger.info("ENHANCED BATCH PROCESSING COMPLETE")
    logger.info(f"Successfully processed: {success_count}")
    logger.info(f"Skipped (already exists): {skip_count}")
    logger.info(f"Errors: {error_count}")
    logger.info(f"Total directories found: {len(directories_with_images)}")

    if error_count > 0:
        logger.warning(f"Some galleries failed to process. Check the log for details.")
        sys.exit(1)
    else:
        logger.info("All galleries processed successfully!")


if __name__ == "__main__":
    main()
