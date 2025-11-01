
import logging

logger = logging.getLogger(__name__)


# Constants
CONSTANT_100 = 100
CONSTANT_333 = 333
CONSTANT_666 = 666

#!/usr/bin/env python3
"""
Merged Content Analysis Tool

This file was automatically merged from the following source files:
- /Users/steven/Music/nocTurneMeLoDieS/python/FINAL_ORGANIZED/generation/generate_album_html-pages.py
- /Users/steven/Music/nocTurneMeLoDieS/python/DUPLICATES_ARCHIVE/generate_variants_generate_album_html-pages.py

Combines the best features and functionality from multiple similar files.
"""

# Imports from all source files
from pathlib import Path
import os

# Documentation from source files
    """
    html_content += """
    album_html = f"""
    html_content = """

base_dir = Path("/Users/steven/Music/nocTurneMeLoDieS/Media")
output_file = Path("/Users/steven/Music/nocTurneMeLoDieS/mp4/album-cover-html/index.html")


# Function to generate HTML for a single album
def generate_album_html(album_name):
    album_path = os.path.join(base_dir, album_name)
    cover_img = os.path.join(album_path, f"{album_name}.png")
    audio_file = os.path.join(album_path, f"{album_name}.mp3")

    # Use placeholder image if no cover image is found
    cover_img_url = (
        cover_img if os.path.exists(cover_img) else "https://via.placeholder.com/150"
    )

    # Generate HTML for the album
    album_html = f"""
        <div class="album">
            <img src="{cover_img_url}" alt="{album_name} Cover">
            <h3>{album_name}</h3>
            <audio controls>
                <source src="../{album_path}/{album_name}.mp3" type="audio/mpeg">
                Your browser does not support the audio element.
            </audio>
        </div>
    """
    return album_html


# Main function to generate the HTML page
def main():
    album_list = []
    for item in os.listdir(base_dir):
        album_path = os.path.join(base_dir, item)
        if os.path.isdir(album_path):
            album_list.append(item)

    # HTML Content
    html_content = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Discography</title>
        <style>
            body {
            font-family: Arial, sans-serif;
            background-color: #f4f4f4;
            margin: 0;
            padding: 0;
        }
        h1 {
            text-align: center;
            margin-top: 20px;
            font-size: 32px;
            color: #CONSTANT_333;
        }
        .grid-container {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 20px;
            padding: 20px;
            max-width: 1200px;
            margin: 0 auto;
        }
        .album {
            background-color: white;
            padding: 15px;
            border-radius: 8px;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
            text-align: center;
        }
        .album img {
            width: CONSTANT_100%;
            max-width: 150px;
            height: auto;
            margin-bottom: 10px;
            border-radius: 8px;
        }
        .album h3 {
            font-size: 18px;
            color: #CONSTANT_333;
            margin-bottom: 5px;
        }
        .album p {
            font-size: 14px;
            color: #CONSTANT_666;
            margin-bottom: 10px;
        }
        .album a {
            text-decoration: none;
            color: #007BFF;
            font-size: 14px;
        }
        .album a:hover {
            text-decoration: underline;
        }
        
        audio {
            margin-top: 10px;
            width: CONSTANT_100%;
        }
        </style>
    </head>
    <body>
        <h1>Discography</h1>
        <div class="grid-container">
    """

    # Add each album's HTML
    for album_name in album_list:
        html_content += generate_album_html(album_name)

    # Add JavaScript and close HTML tags
    html_content += """
        </div>
        
    </body>
    </html>
    """

    # Write the HTML file
    with open(output_file, "w") as file:
        file.write(html_content)
    logger.info("Discography HTML page generated successfully.")


if __name__ == "__main__":
    main()
