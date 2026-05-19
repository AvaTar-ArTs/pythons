import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
#!/usr/bin/env python3
"""
Simple Enhanced Gallery Builder
Creates galleries with folder name as title, no description/URL headers
"""

import os
import sys
import argparse
import json


def create_simple_gallery_config(gallery_path):
    """Create a simple gallery config using folder name as title"""
    gallery_name = os.path.basename(os.path.abspath(gallery_path))

    config = {
        "images_data_file": "images_data.json",
        "public_path": "public",
        "templates_path": "templates",
        "images_path": "public/images/photos",
        "thumbnails_path": "public/images/thumbnails",
        "thumbnail_height": 160,
        "title": gallery_name,
        "description": "",
        "background_photo": "",
        "url": "",
        "background_photo_offset": 30,
        "disable_captions": False,
        "enhanced": True,
        "template": "enhanced",
    }

    config_path = os.path.join(gallery_path, "gallery.json")
    with open(config_path, "w") as f:
        json.dump(config, f, indent=2)

    print(f"Created gallery config for: {gallery_name}")
    return config


def ensure_directory_structure(gallery_path):
    """Ensure the required directory structure exists"""
    dirs = [
        "public/css",
        "public/js",
        "public/images/photos",
        "public/images/thumbnails",
        "templates",
    ]

    for dir_path in dirs:
        full_path = os.path.join(gallery_path, dir_path)
        os.makedirs(full_path, exist_ok=True)

    print("Directory structure created")


def main():
    parser = argparse.ArgumentParser(description="Simple Enhanced Gallery Builder")
    parser.add_argument("path", help="Path to gallery directory")
    parser.add_argument("--ai", action="store_true", help="Enable AI analysis")
    parser.add_argument(
        "--force-thumbnails", action="store_true", help="Force thumbnail regeneration"
    )

    args = parser.parse_args()

    gallery_path = os.path.abspath(args.path)

    if not os.path.exists(gallery_path):
        print(f"Error: Gallery path does not exist: {gallery_path}")
        sys.exit(1)

    print(f"Building enhanced gallery for: {os.path.basename(gallery_path)}")

    # Ensure directory structure
    ensure_directory_structure(gallery_path)

    # Create simple config
    create_simple_gallery_config(gallery_path)

    # Build the gallery
    build_cmd = [
        sys.executable,
        "-m",
        "simplegallery.enhanced_gallery_build",
        "--enhanced",
        "--path",
        gallery_path,
    ]

    if args.ai:
        build_cmd.append("--ai-analysis")

    if args.force_thumbnails:
        build_cmd.append("--force-thumbnails")

    print("Building gallery...")
    import subprocess

    result = subprocess.run(build_cmd)

    if result.returncode == 0:
        print("✓ Gallery built successfully!")
        print(f"Open: {os.path.join(gallery_path, 'public', 'index.html')}")
    else:
        print("✗ Gallery build failed")
        sys.exit(1)


try:
        main()
except KeyboardInterrupt:
    logger.info("Execution interrupted by user")
    sys.exit(1)
except Exception as e:
    logger.error(f"An error occurred: {e}", exc_info=True)
    sys.exit(1)