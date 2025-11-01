"""
Img2Gallery

This module provides functionality for img2gallery.

Author: Auto-generated
Date: 2025-11-01
"""

import os


def generate_html_gallery(image_folder, html_output_file):
    """generate_html_gallery function."""

    image_files = [
        f
        for f in os.listdir(image_folder)
        if f.endswith((".png", ".jpg", ".jpeg", ".tiff"))
    ]
    with open(html_output_file, "w") as file:
        file.write("<!DOCTYPE html>\n")
        file.write("<html>\n<head>\n<title>Photo Gallery</title>\n</head>\n<body>\n")
        file.write("<div style='display: flex; flex-wrap: wrap;'>\n")
        for image in image_files:
            file.write(
                f"<img src='{image_folder}/{image}' style='margin: 10px; width: 200px; height: auto;'>\n"
            )
        file.write("</div>\n</body>\n</html>")


# Usage
html_output_file = "path/to/output/gallery.html"
generate_html_gallery(output_folder, html_output_file)
