"""
Base gallery logic class for City 16-9 Gallery Generator
Following the dark architectural patterns of simplegallery
"""

import os
import json
from typing import Dict, Any, List
from collections import OrderedDict
import common as cg_common


class BaseCityGalleryLogic:
    """
    Base class for defining city gallery logic. 
    Derived classes should implement the methods create_thumbnails and
    generate_images_data to define the specific logic.
    """

    def __init__(self, gallery_config: Dict[str, Any]):
        """
        Initializes the city gallery logic
        :param gallery_config: Gallery config dictionary as read from the gallery.json
        """
        self.gallery_config = gallery_config
        self._validate_config()

    def _validate_config(self) -> None:
        """
        Validate the gallery configuration
        """
        required_keys = [
            "images_data_file", "public_path", "templates_path",
            "images_path", "thumbnails_path", "title", "description"
        ]
        
        for key in required_keys:
            if key not in self.gallery_config:
                raise cg_common.CityGalleryException(
                    f"Missing required configuration key: {key}"
                )

    def create_thumbnails(self, force: bool = False) -> None:
        """
        Checks if every image has an existing thumbnail and generates it if needed
        :param force: Forces generation of thumbnails if set to true
        """
        pass

    def generate_images_data(self, images_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate the metadata for each image
        :param images_data: Images data dictionary containing the existing metadata
        :return: updated images data dictionary
        """
        return images_data

    def create_images_data_file(self) -> None:
        """
        Creates or updates the images_data.json file with metadata for each image
        """
        images_data_path = self.gallery_config["images_data_file"]
        
        # Ensure directory exists
        os.makedirs(os.path.dirname(images_data_path), exist_ok=True)

        # Load the existing file or create an empty dict
        if os.path.exists(images_data_path):
            with open(images_data_path, "r", encoding="utf-8") as images_data_in:
                images_data = json.load(images_data_in, object_pairs_hook=OrderedDict)
        else:
            images_data = OrderedDict()

        # Generate the images data
        images_data = self.generate_images_data(images_data)

        # Write the data to the JSON file
        with open(images_data_path, "w", encoding="utf-8") as images_out:
            json.dump(images_data, images_out, indent=4, separators=(",", ": "))

    def get_gallery_images(self) -> List[Dict[str, Any]]:
        """
        Get list of all gallery images with their metadata
        :return: list of image dictionaries
        """
        images_data_path = self.gallery_config["images_data_file"]
        
        if not os.path.exists(images_data_path):
            return []
            
        with open(images_data_path, "r", encoding="utf-8") as images_data_in:
            images_data = json.load(images_data_in, object_pairs_hook=OrderedDict)
            
        return [
            {**images_data[image], "name": image} 
            for image in images_data.keys()
        ]

    def calculate_thumbnail_size(self, width: int, height: int, target_height: int = 160) -> tuple:
        """
        Calculate thumbnail size maintaining aspect ratio
        :param width: original width
        :param height: original height
        :param target_height: target thumbnail height
        :return: tuple of (width, height)
        """
        aspect_ratio = width / height
        thumbnail_width = int(target_height * aspect_ratio)
        return (thumbnail_width, target_height)