"""
Citygallerylogic

This module provides functionality for citygallerylogic.

Author: Auto-generated
Date: 2025-11-01
"""

# Constants
CONSTANT_160 = 160

"""
City gallery logic implementation for City 16-9 Gallery Generator
Following the dark patterns of simplegallery with urban photography focus
"""

import os
import glob
from typing import Dict, Any, List
from PIL import Image
import common as cg_common
from .base_gallery_logic import BaseCityGalleryLogic


class CityGalleryLogic(BaseCityGalleryLogic):
    """
    Logic for local files gallery with urban photography focus
    """

    def create_thumbnails(self, force: bool = False) -> None:
        """
        Create thumbnails for all images in the gallery
        :param force: Forces generation of thumbnails if set to true
        """
        images_path = self.gallery_config["images_path"]
        thumbnails_path = self.gallery_config["thumbnails_path"]
        thumbnail_height = self.gallery_config.get("thumbnail_height", CONSTANT_160)

        # Ensure thumbnails directory exists
        cg_common.ensure_directory_exists(thumbnails_path)

        # Get all image files
        image_extensions = ["*.jpg", "*.jpeg", "*.png", "*.gif", "*.webp"]
        image_files = []
        for ext in image_extensions:
            image_files.extend(glob.glob(os.path.join(images_path, ext)))
            image_files.extend(glob.glob(os.path.join(images_path, ext.upper())))

        cg_common.log(f"Found {len(image_files)} images to process")

        for image_path in image_files:
            filename = os.path.basename(image_path)
            thumbnail_path = os.path.join(thumbnails_path, filename)

            # Skip if thumbnail exists and not forcing
            if os.path.exists(thumbnail_path) and not force:
                continue

            try:
                # Create thumbnail
                with Image.open(image_path) as img:
                    # Convert to RGB if necessary
                    if img.mode in ("RGBA", "P"):
                        img = img.convert("RGB")

                    # Calculate thumbnail size
                    width, height = img.size
                    aspect_ratio = width / height
                    thumbnail_width = int(thumbnail_height * aspect_ratio)

                    # Resize image
                    thumbnail = img.resize((thumbnail_width, thumbnail_height), Image.Resampling.LANCZOS)

                    # Save thumbnail
                    thumbnail.save(thumbnail_path, "JPEG", quality=85, optimize=True)

                cg_common.log(f"Created thumbnail: {filename}")

            except Exception as e:
                cg_common.log(f"Failed to create thumbnail for {filename}: {e}")

    def generate_images_data(self, images_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate metadata for each image in the gallery
        :param images_data: existing images data dictionary
        :return: updated images data dictionary
        """
        images_path = self.gallery_config["images_path"]
        thumbnails_path = self.gallery_config["thumbnails_path"]
        thumbnail_height = self.gallery_config.get("thumbnail_height", CONSTANT_160)

        # Get all image files
        image_extensions = ["*.jpg", "*.jpeg", "*.png", "*.gif", "*.webp"]
        image_files = []
        for ext in image_extensions:
            image_files.extend(glob.glob(os.path.join(images_path, ext)))
            image_files.extend(glob.glob(os.path.join(images_path, ext.upper())))

        for image_path in image_files:
            filename = os.path.basename(image_path)

            # Skip if already processed
            if filename in images_data:
                continue

            try:
                # Get image metadata
                metadata = cg_common.get_image_metadata(image_path)

                # Calculate thumbnail size
                thumbnail_size = self.calculate_thumbnail_size(metadata["width"], metadata["height"], thumbnail_height)

                # Determine image type
                image_type = "image"
                if filename.lower().endswith((".mp4", ".webm", ".mov")):
                    image_type = "video"

                # Create image data entry
                images_data[filename] = {
                    "src": f"images/photos/{filename}",
                    "thumbnail": f"images/thumbnails/{filename}",
                    "size": [metadata["width"], metadata["height"]],
                    "thumbnail_size": list(thumbnail_size),
                    "type": image_type,
                    "description": self._generate_urban_description(filename),
                    "date": "",
                    "alt": self._generate_alt_text(filename),
                }

                cg_common.log(f"Processed image: {filename}")

            except Exception as e:
                cg_common.log(f"Failed to process {filename}: {e}")

        return images_data

    def _generate_urban_description(self, filename: str) -> str:
        """
        Generate urban-themed description for image
        :param filename: name of the image file
        :return: description string
        """
        # Extract number from filename if it exists
        import re

        number_match = re.search(r"(\d+)", filename)
        if number_match:
            number = int(number_match.group(1))
            descriptions = [
                "Urban cityscape with modern architecture",
                "Neon-lit street at night",
                "City skyline at sunset",
                "Urban intersection with traffic",
                "Modern building facade",
                "City park with urban backdrop",
                "Underground subway station",
                "Aerial view of city district",
                "Urban waterfront at dawn",
                "City street with pedestrians",
                "Modern office buildings",
                "Urban bridge over water",
                "City square with fountain",
                "Urban market scene",
                "City skyline at night",
                "Urban construction site",
                "City street with shops",
                "Urban park with benches",
                "City intersection with lights",
                "Urban residential area",
                "City center plaza",
                "Urban street with cafes",
                "City skyline at sunrise",
                "Urban transportation hub",
                "City street with street art",
                "Urban waterfront promenade",
                "City district with mixed architecture",
                "Urban skyline with mountains",
                "City center with historic buildings",
                "Urban street with trees",
                "City intersection with traffic lights",
                "Urban residential complex",
                "City street with public transport",
                "Urban park with playground",
                "City center with shopping district",
                "Urban street with restaurants",
                "City skyline with clouds",
                "Urban waterfront with boats",
                "City street with street vendors",
                "Urban residential street",
                "City center with monuments",
                "Urban street with cyclists",
                "City district with modern towers",
                "Urban intersection with pedestrians",
                "City street with street performers",
                "Urban waterfront with bridge",
                "City center with public square",
                "Urban street with cafes and shops",
                "City skyline with sunset colors",
                "Urban district with mixed architecture",
            ]
            return descriptions[(number - 1) % len(descriptions)]

        return "Urban photography in 16:9 format"

    def _generate_alt_text(self, filename: str) -> str:
        """
        Generate alt text for image
        :param filename: name of the image file
        :return: alt text string
        """
        return self._generate_urban_description(filename)


def get_city_gallery_logic(gallery_config: Dict[str, Any]) -> BaseCityGalleryLogic:
    """
    Factory function that returns the appropriate gallery logic
    :param gallery_config: gallery config dictionary
    :return: gallery logic object
    """
    return CityGalleryLogic(gallery_config)
