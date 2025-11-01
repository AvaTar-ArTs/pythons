"""
Auto Image Gallery

This module provides functionality for auto image gallery.

Author: Auto-generated
Date: 2025-11-01
"""

from pathlib import Path
import csv

# Constants
CONSTANT_100 = 100
CONSTANT_333 = 333
CONSTANT_555 = 555



def csv_to_html(csv_file, output_html):
    """csv_to_html function."""

    # Start the HTML structure
    html_content = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Image Gallery</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                background-color: #f0f0f0;
                padding: 20px;
            }
            h1 {
                text-align: center;
                color: #CONSTANT_333;
            }
            .gallery {
                display: flex;
                flex-wrap: wrap;
                justify-content: space-around;
            }
            .image-card {
                margin: 15px;
                padding: 15px;
                background-color: #fff;
                border: 1px solid #ddd;
                box-shadow: 0 2px 4px rgba(0,0,0,0.1);
                width: 300px;
                text-align: center;
            }
            img {
                max-width: CONSTANT_100%;
                height: auto;
            }
            .description {
                margin-top: 10px;
                font-size: 0.9em;
                color: #CONSTANT_555;
                text-align: justify;
            }
        </style>
    </head>
    <body>
        <h1>Image Gallery</h1>
        <div class="gallery">
    """

    # Read the CSV file and append each image's HTML code
    with open(csv_file, "r") as file:
        reader = csv.DictReader(file)
        for row in reader:
            html_content += f"""
            <div class="image-card">
                <img id="{row['ID']}" src="{row['URL']}" alt="{row['Prompt']}">
                <div class="description">{row['Prompt']}</div>
            </div>
            """

    # Close the HTML structure
    html_content += """
        </div>
    </body>
    </html>
    """

    # Write the HTML content to an output file
    with open(output_html, "w") as html_file:
        html_file.write(html_content)


# Example usage:
csv_file = Path("/Users/steven/Music/NocTurnE-meLoDieS/Discography-Genre.csv")  # Replace with the path to your CSV file
output_html = "image_gallery.html"
csv_to_html(csv_file, output_html)
