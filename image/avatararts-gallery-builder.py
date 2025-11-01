"""
Avatararts Gallery Builder

This module provides functionality for avatararts gallery builder.

Author: Auto-generated
Date: 2025-11-01
"""

import logging

logger = logging.getLogger(__name__)

#!/usr/bin/env python3
"""
Script to generate different layout versions of the Zombot AvatarArts Gallery
"""

import os
import json
import jinja2
from pathlib import Path


def generate_layout(layout_name, template_name, css_name, js_name):
    """
    Generate a specific layout version of the gallery
    """
    logger.info(f"🎨 Generating {layout_name} layout...")

    # Load gallery configuration
    with open("gallery.json", "r") as f:
        gallery_config = json.load(f)

    # Load images data
    with open("images_data.json", "r") as f:
        images_data = json.load(f)

    images_data_list = [{**images_data[image], "name": image} for image in images_data.keys()]

    # Find background photo
    background_photo = gallery_config.get("background_photo", "")
    if not background_photo:
        for image in images_data:
            if images_data[image]["type"] == "image":
                background_photo = image
                break

    # Setup Jinja2 environment
    file_loader = jinja2.FileSystemLoader("templates")
    env = jinja2.Environment(loader=file_loader)

    # Render the template
    template = env.get_template(template_name)
    html = template.render(
        images=images_data_list, gallery_config=gallery_config, background_photo=background_photo, remote_data={}
    )

    # Write to public directory
    output_path = f"public/index_{layout_name}.html"
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(html)

    logger.info(f"✅ Generated {output_path}")


def main():
    """
    Generate all layout versions
    """
    logger.info("🌃 Generating Zombot AvatarArts Gallery Layouts")
    logger.info("=" * 50)

    # Ensure public directory exists
    os.makedirs("public", exist_ok=True)

    # Generate different layouts
    layouts = [
        {
            "name": "minimal",
            "template": "index_minimal.jinja",
            "css": "minimal.css",
            "js": "minimal.js",
            "description": "Clean, minimal design with grid layout",
        },
        {
            "name": "masonry",
            "template": "index_masonry.jinja",
            "css": "masonry.css",
            "js": "masonry.js",
            "description": "Pinterest-style masonry layout with filters",
        },
        {
            "name": "cinematic",
            "template": "index_cinematic.jinja",
            "css": "cinematic.css",
            "js": "cinematic.js",
            "description": "Full-screen cinematic experience",
        },
    ]

    for layout in layouts:
        try:
            generate_layout(layout["name"], layout["template"], layout["css"], layout["js"])
            logger.info(f"   Description: {layout['description']}")
        except Exception as e:
            logger.info(f"❌ Failed to generate {layout['name']}: {e}")

    logger.info(f"\n🎉 Layout generation complete!")
    logger.info(f"\n📁 Generated files:")
    logger.info(f"   • public/index_minimal.html - Minimal clean layout")
    logger.info(f"   • public/index_masonry.html - Masonry/Pinterest layout")
    logger.info(f"   • public/index_cinematic.html - Cinematic full-screen layout")
    logger.info(f"   • public/index.html - Original layout")

    logger.info(f"\n🚀 To view the galleries:")
    logger.info(f"   • Open public/index_minimal.html in your browser")
    logger.info(f"   • Open public/index_masonry.html in your browser")
    logger.info(f"   • Open public/index_cinematic.html in your browser")


if __name__ == "__main__":
    main()
