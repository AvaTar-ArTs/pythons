"""
Utilities Cli Tools Gallery 33

This module provides functionality for utilities cli tools gallery 33.

Author: Auto-generated
Date: 2025-11-01
"""

import logging

logger = logging.getLogger(__name__)


# Constants
CONSTANT_100 = 100
CONSTANT_107 = 107
CONSTANT_255 = 255
CONSTANT_600 = 600
CONSTANT_700 = 700
CONSTANT_1080 = 1080
CONSTANT_1920 = 1920

#!/usr/bin/env python3
"""
Enhanced Gallery System - Merging simplegallery and city-16-9 features
Combines the best of both projects with advanced features
"""

import os
import json
import jinja2
import argparse
from pathlib import Path
from typing import Dict, Any, List
from collections import OrderedDict
import common as cg_common
from logic.city_gallery_logic import get_city_gallery_logic


class EnhancedGalleryBuilder:
    """
    Enhanced gallery builder that combines features from both projects
    """

    def __init__(self, config_path: str = "gallery.json"):
        """__init__ function."""

        self.config_path = config_path
        self.gallery_config = self.load_config()
        self.images_data = {}
        self.layouts = {
            "minimal": {
                "template": "enhanced_minimal.jinja",
                "css": "enhanced_minimal.css",
                "js": "enhanced_minimal.js",
                "description": "Clean minimal design with neon accents",
            },
            "masonry": {
                "template": "enhanced_masonry.jinja",
                "css": "enhanced_masonry.css",
                "js": "enhanced_masonry.js",
                "description": "Pinterest-style with advanced filters",
            },
            "cinematic": {
                "template": "enhanced_cinematic.jinja",
                "css": "enhanced_cinematic.css",
                "js": "enhanced_cinematic.js",
                "description": "Full-screen cinematic experience",
            },
            "neon": {
                "template": "enhanced_neon.jinja",
                "css": "enhanced_neon.css",
                "js": "enhanced_neon.js",
                "description": "Cyberpunk neon aesthetic",
            },
        }

    def load_config(self) -> Dict[str, Any]:
        """Load gallery configuration"""
        config = cg_common.read_gallery_config(self.config_path)
        if not config:
            raise Exception(f"Cannot load gallery config from {self.config_path}")
        return config

    def load_images_data(self) -> None:
        """Load images data from JSON file"""
        images_data_path = self.gallery_config.get(
            "images_data_file", "images_data.json"
        )
        try:
            with open(images_data_path, "r") as f:
                self.images_data = json.load(f, object_pairs_hook=OrderedDict)
        except FileNotFoundError:
            logger.info(f"⚠️  Images data file not found: {images_data_path}")
            self.images_data = {}

    def generate_enhanced_images_data(self) -> List[Dict[str, Any]]:
        """Generate enhanced images data with additional metadata"""
        images_list = []

        for image_name, image_data in self.images_data.items():
            enhanced_data = {
                **image_data,
                "name": image_name,
                "id": image_name.replace(".", "_").replace("-", "_"),
                "category": self._determine_category(image_name, image_data),
                "tags": self._generate_tags(image_name, image_data),
                "mood": self._determine_mood(image_data),
                "color_palette": self._extract_color_palette(image_data),
                "aspect_ratio": self._calculate_aspect_ratio(image_data),
                "is_featured": self._is_featured(image_name),
                "neon_glow": self._should_have_neon_glow(image_data),
            }
            images_list.append(enhanced_data)

        return images_list

    def _determine_category(self, name: str, data: Dict) -> str:
        """Determine image category based on filename and data"""
        name_lower = name.lower()
        if "neon" in name_lower or "night" in name_lower:
            return "neon"
        elif "street" in name_lower or "urban" in name_lower:
            return "street"
        elif "skyline" in name_lower or "city" in name_lower:
            return "skyline"
        elif "architecture" in name_lower or "building" in name_lower:
            return "architecture"
        else:
            return "general"

    def _generate_tags(self, name: str, data: Dict) -> List[str]:
        """Generate tags for the image"""
        tags = []
        name_lower = name.lower()

        if "300dpi" in name_lower:
            tags.append("high-res")
        if "stn" in name_lower:
            tags.append("standard")

        # Add category-based tags
        category = self._determine_category(name, data)
        tags.append(category)

        # Add mood-based tags
        mood = self._determine_mood(data)
        tags.append(mood)

        return tags

    def _determine_mood(self, data: Dict) -> str:
        """Determine the mood of the image"""
        description = data.get("description", "").lower()
        if "night" in description or "neon" in description:
            return "dark"
        elif "sunset" in description or "dawn" in description:
            return "warm"
        elif "urban" in description or "city" in description:
            return "urban"
        else:
            return "neutral"

    def _extract_color_palette(self, data: Dict) -> List[str]:
        """Extract color palette hints from image data"""
        # This would ideally use image analysis, but for now we'll use heuristics
        description = data.get("description", "").lower()
        colors = []

        if "neon" in description:
            colors.extend(["#ff0080", "#00ffff", "#ffff00"])
        elif "night" in description:
            colors.extend(["#000000", "#1a1a2e", "#16213e"])
        elif "sunset" in description:
            colors.extend(["#ff6b6b", "#ee5a24", "#feca57"])
        else:
            colors.extend(["#667eea", "#764ba2", "#f093fb"])

        return colors

    def _calculate_aspect_ratio(self, data: Dict) -> str:
        """Calculate aspect ratio string"""
        size = data.get("size", [CONSTANT_1920, CONSTANT_1080])
        width, height = size[0], size[1]

        if width > height:
            return "landscape"
        elif height > width:
            return "portrait"
        else:
            return "square"

    def _is_featured(self, name: str) -> bool:
        """Determine if image should be featured"""
        # Featured images get special treatment
        featured_names = [
            "stn-HTkVH2EG61cHOzS4pB2F9QPQTjRj2YGX9uyxJqqa",
            "stn-mQQQuSNadzNCFN3xgCVJdL3kWw69gdnsudZinwBH",
        ]
        return any(feat in name for feat in featured_names)

    def _should_have_neon_glow(self, data: Dict) -> bool:
        """Determine if image should have neon glow effect"""
        description = data.get("description", "").lower()
        return "neon" in description or "night" in description or "lit" in description

    def build_layout(self, layout_name: str) -> None:
        """Build a specific layout"""
        if layout_name not in self.layouts:
            raise ValueError(f"Unknown layout: {layout_name}")

        layout_config = self.layouts[layout_name]
        logger.info(f"🎨 Building {layout_name} layout...")

        # Load images data
        self.load_images_data()
        images_list = self.generate_enhanced_images_data()

        # Find background photo
        background_photo = self.gallery_config.get("background_photo", "")
        if not background_photo and images_list:
            background_photo = images_list[0]["name"]

        # Setup Jinja2 environment
        file_loader = jinja2.FileSystemLoader("templates")
        env = jinja2.Environment(loader=file_loader)

        # Render template
        template = env.get_template(layout_config["template"])
        html = template.render(
            images=images_list,
            gallery_config=self.gallery_config,
            background_photo=background_photo,
            layout_config=layout_config,
            remote_data={},
            total_images=len(images_list),
            categories=list(set(img["category"] for img in images_list)),
            moods=list(set(img["mood"] for img in images_list)),
        )

        # Write output
        output_path = f"public/index_{layout_name}.html"
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(html)

        logger.info(f"✅ Generated {output_path}")

    def build_all_layouts(self) -> None:
        """Build all available layouts"""
        logger.info("🌃 Building Enhanced Zombot Gallery - All Layouts")
        logger.info("=" * 60)

        for layout_name in self.layouts.keys():
            try:
                self.build_layout(layout_name)
                logger.info(
                    f"   Description: {self.layouts[layout_name]['description']}"
                )
            except Exception as e:
                logger.info(f"❌ Failed to build {layout_name}: {e}")

        logger.info(f"\n🎉 Enhanced gallery generation complete!")
        logger.info(f"\n📁 Generated files:")
        for layout_name, config in self.layouts.items():
            logger.info(
                f"   • public/index_{layout_name}.html - {config['description']}"
            )

    def create_layout_switcher(self) -> None:
        """Create a layout switcher page"""
        switcher_html = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Zombot Gallery - Layout Switcher</title>
    <style>
        body {
            font-family: 'Inter', sans-serif;
            background: linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 CONSTANT_100%);
            color: white;
            margin: 0;
            padding: 2rem;
            min-height: 100vh;
        }
        .container {
            max-width: 1200px;
            margin: 0 auto;
        }
        h1 {
            text-align: center;
            font-size: 3rem;
            margin-bottom: 3rem;
            background: linear-gradient(135deg, #ff6b6b 0%, #ee5a24 CONSTANT_100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
        }
        .layouts-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 2rem;
        }
        .layout-card {
            background: rgba(CONSTANT_255, CONSTANT_255, CONSTANT_255, 0.1);
            backdrop-filter: blur(10px);
            border-radius: 20px;
            padding: 2rem;
            text-align: center;
            transition: all 0.3s ease;
            border: 1px solid rgba(CONSTANT_255, CONSTANT_255, CONSTANT_255, 0.2);
        }
        .layout-card:hover {
            transform: translateY(-10px);
            box-shadow: 0 20px 40px rgba(0, 0, 0, 0.3);
        }
        .layout-title {
            font-size: 1.5rem;
            font-weight: CONSTANT_700;
            margin-bottom: 1rem;
        }
        .layout-description {
            color: rgba(CONSTANT_255, CONSTANT_255, CONSTANT_255, 0.8);
            margin-bottom: 2rem;
        }
        .layout-btn {
            background: linear-gradient(135deg, #ff6b6b 0%, #ee5a24 CONSTANT_100%);
            color: white;
            border: none;
            padding: 1rem 2rem;
            border-radius: 50px;
            font-size: 1rem;
            font-weight: CONSTANT_600;
            cursor: pointer;
            transition: all 0.3s ease;
            text-decoration: none;
            display: inline-block;
        }
        .layout-btn:hover {
            transform: translateY(-2px);
            box-shadow: 0 10px 25px rgba(CONSTANT_255, CONSTANT_107, CONSTANT_107, 0.4);
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>Zombot AvatarArts Gallery</h1>
        <div class="layouts-grid">
            <div class="layout-card">
                <div class="layout-title">Minimal</div>
                <div class="layout-description">Clean minimal design with neon accents</div>
                <a href="index_minimal.html" class="layout-btn">View Minimal</a>
            </div>
            <div class="layout-card">
                <div class="layout-title">Masonry</div>
                <div class="layout-description">Pinterest-style with advanced filters</div>
                <a href="index_masonry.html" class="layout-btn">View Masonry</a>
            </div>
            <div class="layout-card">
                <div class="layout-title">Cinematic</div>
                <div class="layout-description">Full-screen cinematic experience</div>
                <a href="index_cinematic.html" class="layout-btn">View Cinematic</a>
            </div>
            <div class="layout-card">
                <div class="layout-title">Neon</div>
                <div class="layout-description">Cyberpunk neon aesthetic</div>
                <a href="index_neon.html" class="layout-btn">View Neon</a>
            </div>
        </div>
    </div>
</body>
</html>
        """

        with open("public/index.html", "w", encoding="utf-8") as f:
            f.write(switcher_html)

        logger.info("✅ Created layout switcher at public/index.html")


def main():
    """Main function"""
    parser = argparse.ArgumentParser(description="Enhanced Gallery Builder")
    parser.add_argument("--layout", help="Build specific layout")
    parser.add_argument("--all", action="store_true", help="Build all layouts")
    parser.add_argument(
        "--switcher", action="store_true", help="Create layout switcher"
    )

    args = parser.parse_args()

    try:
        builder = EnhancedGalleryBuilder()

        if args.layout:
            builder.build_layout(args.layout)
        elif args.all:
            builder.build_all_layouts()
        elif args.switcher:
            builder.create_layout_switcher()
        else:
            # Default: build all layouts and create switcher
            builder.build_all_layouts()
            builder.create_layout_switcher()

    except Exception as e:
        logger.info(f"❌ Error: {e}")
        return 1

    return 0


if __name__ == "__main__":
    exit(main())
