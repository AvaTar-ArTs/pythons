"""
Alphabet Html Gall

This module provides functionality for alphabet html gall.

Author: Auto-generated
Date: 2025-11-01
"""

from pathlib import Path
import os

import logging

logger = logging.getLogger(__name__)


# Constants
CONSTANT_100 = 100
CONSTANT_333 = 333


def generate_grouped_gallery(folder_path, output_html, group_size=4):
    """
    Generates an HTML gallery grouped alphabetically by sets of images and MP4s.
    """
    # Get all valid files
    valid_extensions = (".jpg", ".jpeg", ".png", ".mp4")
    all_files = [
        f for f in os.listdir(folder_path) if f.lower().endswith(valid_extensions)
    ]

    # Sort files alphabetically
    all_files.sort()

    # Group files into sets of the specified size
    grouped_files = [
        all_files[i : i + group_size] for i in range(0, len(all_files), group_size)
    ]

    # Start the HTML structure
    html_content = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Grouped Image and Video Gallery</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                background-color: #1a1a1a;
                color: #fff;
                margin: 0;
                padding: 20px;
            }
            h1 {
                text-align: center;
                color: #f0a500;
                margin-bottom: 40px;
            }
            .group {
                margin-bottom: 40px;
                padding: 20px;
                background-color: #2a2a2a;
                border-radius: 10px;
                box-shadow: 0 4px 8px rgba(0, 0, 0, 0.3);
            }
            .gallery {
                display: flex;
                flex-wrap: wrap;
                justify-content: center;
                gap: 20px;
            }
            .media-card {
                background-color: #CONSTANT_333;
                border-radius: 10px;
                overflow: hidden;
                box-shadow: 0 4px 8px rgba(0, 0, 0, 0.3);
                width: 280px;
                text-align: center;
                transition: transform 0.3s, box-shadow 0.3s;
            }
            .media-card:hover {
                transform: scale(1.05);
                box-shadow: 0 6px 12px rgba(0, 0, 0, 0.4);
            }
            img, video {
                width: CONSTANT_100%;
                height: auto;
                display: block;
                border-bottom: 1px solid #CONSTANT_333;
            }
            .description {
                padding: 15px;
                font-size: 0.9em;
                color: #bbb;
                text-align: center;
            }
        </style>
    </head>
    <body>
        <h1>Grouped Image and Video Gallery</h1>
    """

    # Add each group to the HTML
    for group_index, group in enumerate(grouped_files):
        html_content += (
            f'<div class="group"><h2>Group {group_index + 1}</h2><div class="gallery">'
        )
        for filename in group:
            file_path = os.path.join(folder_path, filename)
            if filename.lower().endswith((".jpg", ".jpeg", ".png")):
                # Add image
                html_content += f"""
                <div class="media-card">
                    <img src="{file_path}" alt="{filename}" loading="lazy">
                    <div class="description">{filename}</div>
                </div>
                """
            elif filename.lower().endswith(".mp4"):
                # Add video
                html_content += f"""
                <div class="media-card">
                    <video controls>
                        <source src="{file_path}" type="video/mp4">
                        Your browser does not support the video tag.
                    </video>
                    <div class="description">{filename}</div>
                </div>
                """
        html_content += "</div></div>"

    # Close the HTML structure
    html_content += """
    </body>
    </html>
    """

    # Write the HTML content to an output file
    with open(output_html, "w") as html_file:
        html_file.write(html_content)
    logger.info(f"Grouped gallery saved at {output_html}")


# Example usage
folder_path = Path(str(Path.home()) + "/Pictures/leodowns/")  # Replace with your folder path
output_html = Path(
    str(Path.home()) + "/Pictures/leodowns/grouped_gallery.html"
)  # Output HTML path
generate_grouped_gallery(folder_path, output_html)
