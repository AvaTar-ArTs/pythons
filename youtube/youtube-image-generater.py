"""
Youtube Image Generater

This module provides functionality for youtube image generater.

Author: Auto-generated
Date: 2025-11-01
"""


import logging

logger = logging.getLogger(__name__)

#!/usr/bin/env python3
"""
Script to add zombot-avatararts images to the City 16-9 Gallery
Following the dark patterns of the gallery system
"""

import os
import shutil
import json
from pathlib import Path
import city_gallery.common as cg_common


def copy_zombot_images():
    """
    Copy zombot-avatararts images to the gallery photos directory
    """
    source_dir = Path("/Users/steven/Pictures/zombot-avatararts")
    target_dir = Path("/Users/steven/tehSiTes/Gallery_Code_Project_Root/city-16-9/public/images/photos")
    
    # Ensure target directory exists
    cg_common.ensure_directory_exists(target_dir)
    
    # Get all image files from source directory
    image_extensions = ['.jpg', '.jpeg', '.png', '.gif', '.webp']
    copied_count = 0
    
    logger.info("🌃 Copying zombot-avatararts images to gallery...")
    
    for filename in os.listdir(source_dir):
        if any(filename.lower().endswith(ext) for ext in image_extensions):
            source_path = os.path.join(source_dir, filename)
            target_path = os.path.join(target_dir, filename)
            
            try:
                # Copy the image
                shutil.copy2(source_path, target_path)
                logger.info(f"✅ Copied: {filename}")
                copied_count += 1
            except Exception as e:
                logger.info(f"❌ Failed to copy {filename}: {e}")
    
    logger.info(f"\n🎉 Successfully copied {copied_count} images to the gallery!")
    return copied_count


def update_gallery_config():
    """
    Update the gallery configuration to include the new images
    """
    config_path = Path("/Users/steven/tehSiTes/Gallery_Code_Project_Root/city-16-9/gallery.json")
    
    # Read current config
    config = cg_common.read_gallery_config(config_path)
    if not config:
        logger.info("❌ Could not read gallery configuration")
        return False
    
    # Update title and description to reflect zombot theme
    config["title"] = "Zombot AvatarArts Collection"
    config["description"] = "A curated collection of AI-generated zombot artwork in high-resolution 16:9 format, showcasing the dark artistic vision of Λ∀ʌ†ʌʀ 🦄 ∆ʀ†s"
    config["url"] = "https://avatararts.org/zombot-gallery"
    
    # Save updated config
    if cg_common.write_gallery_config(config_path, config):
        logger.info("✅ Updated gallery configuration")
        return True
    else:
        logger.info("❌ Failed to update gallery configuration")
        return False


def generate_zombot_descriptions():
    """
    Generate urban-themed descriptions for zombot images
    """
    descriptions = [
        "AI-generated zombot in urban decay",
        "Mechanical entity in post-apocalyptic cityscape",
        "Robotic figure against industrial backdrop",
        "Zombot emerging from urban shadows",
        "Cybernetic being in metropolitan environment",
        "Artificial intelligence in concrete jungle",
        "Robotic entity in neon-lit streets",
        "Zombot in futuristic cityscape",
        "Mechanical creature in urban wasteland",
        "AI-generated being in city ruins",
        "Cybernetic zombie in metropolitan setting",
        "Robotic entity in post-urban landscape",
        "Zombot in industrial cityscape",
        "Mechanical being in urban decay",
        "AI-generated creature in city environment",
        "Cybernetic zombie in concrete world",
        "Robotic figure in metropolitan ruins",
        "Zombot in futuristic urban setting",
        "Mechanical entity in city shadows",
        "AI-generated being in urban landscape",
        "Cybernetic creature in post-apocalyptic city",
        "Robotic zombie in industrial environment",
        "Zombot in neon cityscape",
        "Mechanical being in urban wasteland",
        "AI-generated entity in metropolitan decay",
        "Cybernetic figure in city ruins",
        "Robotic creature in futuristic metropolis",
        "Zombot in concrete jungle",
        "Mechanical zombie in urban shadows",
        "AI-generated being in industrial cityscape"
    ]
    return descriptions


def main():
    """
    Main function to add zombot images to the gallery
    """
    logger.info("🤖 Adding Zombot AvatarArts Images to City 16-9 Gallery")
    logger.info("=" * 60)
    
    # Copy images
    copied_count = copy_zombot_images()
    
    if copied_count > 0:
        # Update configuration
        update_gallery_config()
        
        logger.info(f"\n🚀 Next steps:")
        logger.info(f"1. Run: cd /Users/steven/tehSiTes/Gallery_Code_Project_Root/city-16-9")
        logger.info(f"2. Run: python -m city_gallery.gallery_build")
        logger.info(f"3. Open: public/index.html in your browser")
        
        logger.info(f"\n✨ The zombot images have been successfully integrated into the gallery!")
        logger.info(f"   Total images added: {copied_count}")
    else:
        logger.info("❌ No images were copied. Please check the source directory.")


if __name__ == "__main__":
    main()