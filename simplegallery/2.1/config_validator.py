"""
Configuration validation and management for SimpleGallery 2.1
"""

import json
import os
from typing import Dict, Any, Optional, List
from pathlib import Path


class ConfigValidator:
    """Validates and manages gallery configuration"""
    
    REQUIRED_FIELDS = [
        "images_data_file",
        "public_path",
        "templates_path",
        "images_path",
        "thumbnails_path",
        "thumbnail_height",
        "title",
    ]
    
    OPTIONAL_FIELDS = {
        "description": "",
        "background_photo": "",
        "url": "",
        "background_photo_offset": 30,
        "disable_captions": False,
        "disable_right_click": False,
        "template_theme": "default",
        "parallel_processing": True,
        "cache_enabled": True,
        "verbose": False,
    }
    
    @staticmethod
    def validate_config(config: Dict[str, Any], gallery_root: str) -> tuple[bool, List[str]]:
        """
        Validate gallery configuration
        :param config: Configuration dictionary
        :param gallery_root: Root directory of the gallery
        :return: (is_valid, list_of_errors)
        """
        errors = []
        
        # Check required fields
        for field in ConfigValidator.REQUIRED_FIELDS:
            if field not in config:
                errors.append(f"Missing required field: {field}")
        
        # Validate paths
        if "images_path" in config:
            if not os.path.exists(config["images_path"]):
                errors.append(f"Images path does not exist: {config['images_path']}")
        
        if "templates_path" in config:
            if not os.path.exists(config["templates_path"]):
                errors.append(f"Templates path does not exist: {config['templates_path']}")
        
        # Validate thumbnail_height
        if "thumbnail_height" in config:
            try:
                height = int(config["thumbnail_height"])
                if height < 50 or height > 1000:
                    errors.append(f"thumbnail_height must be between 50 and 1000, got {height}")
            except (ValueError, TypeError):
                errors.append(f"thumbnail_height must be an integer, got {config['thumbnail_height']}")
        
        return len(errors) == 0, errors
    
    @staticmethod
    def apply_defaults(config: Dict[str, Any], gallery_root: str) -> Dict[str, Any]:
        """
        Apply default values to configuration
        :param config: Configuration dictionary
        :param gallery_root: Root directory of the gallery
        :return: Configuration with defaults applied
        """
        # Apply optional defaults
        for key, default_value in ConfigValidator.OPTIONAL_FIELDS.items():
            if key not in config:
                config[key] = default_value
        
        # Auto-detect parent folder name for title if not set
        if not config.get("title") or config.get("title") == os.path.basename(gallery_root):
            config["title"] = os.path.basename(os.path.abspath(gallery_root))
        
        # Auto-detect parent folder name for description if default
        if not config.get("description") or config.get("description") == "Default description of my gallery":
            parent_folder = os.path.basename(os.path.abspath(gallery_root))
            config["description"] = ""  # Empty by default in 2.1
        
        return config
    
    @staticmethod
    def migrate_config(config: Dict[str, Any], from_version: str = "2.0") -> Dict[str, Any]:
        """
        Migrate configuration from older versions
        :param config: Configuration dictionary
        :param from_version: Version to migrate from
        :return: Migrated configuration
        """
        # Add new 2.1 fields if missing
        if "template_theme" not in config:
            config["template_theme"] = "default"
        
        if "parallel_processing" not in config:
            config["parallel_processing"] = True
        
        if "cache_enabled" not in config:
            config["cache_enabled"] = True
        
        return config

