from pathlib import Path
import csv

import logging

logger = logging.getLogger(__name__)


# Constants
CONSTANT_100 = 100
CONSTANT_333 = 333


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
                background-color: #1a1a1a;
                color: #fff;
                margin: 0;
                padding: 0;
            }
            h1 {
                text-align: center;
                padding: 20px;
                color: #f0a500;
            }
            .gallery {
                display: flex;
                flex-wrap: wrap;
                justify-content: center;
                margin: 0 auto;
                max-width: 1200px;
                gap: 20px;
            }
            .image-card {
                background-color: #2a2a2a;
                border-radius: 10px;
                overflow: hidden;
                box-shadow: 0 4px 8px rgba(0, 0, 0, 0.3);
                width: 280px;
                text-align: center;
                transition: transform 0.3s, box-shadow 0.3s;
            }
            .image-card:hover {
                transform: scale(1.05);
                box-shadow: 0 6px 12px rgba(0, 0, 0, 0.4);
            }
            img {
                width: CONSTANT_100%;
                height: auto;
                display: block;
                border-bottom: 1px solid #CONSTANT_333;
            }
            .description {
                padding: 15px;
                font-size: 0.9em;
                color: #bbb;
                text-align: left;
            }
            .description strong {
                color: #f0a500;
            }
            @media (max-width: 768px) {
                .gallery {
                    flex-direction: column;
                    align-items: center;
                }
                .image-card {
                    width: 90%;
                }
            }
        </style>
    </head>
    <body>
        <h1>Leonardo Image Gallery</h1>
        <div class="gallery">
    """

    # Read the CSV file and append each image's HTML code
    with open(csv_file, "r") as file:
        reader = csv.DictReader(file)
        for row in reader:
            html_content += f"""
            <div class="image-card">
                <img id="{row['id']}" src="{row['image_url']}" alt="{row['prompt']}">
                <div class="description">
                    <strong>Prompt:</strong> {row['prompt']}<br>
                    <strong>Created At:</strong> {row['createdAt']}
                </div>
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


if __name__ == "__main__":
    # Example usage:
    csv_file = Path(str(Path.home()) + "/Pictures/leodowns/leonardo_urls.csv")  # Path to your CSV
    output_html = Path(
        str(Path.home()) + "/Pictures/leodowns/image_gallery.html"
    )  # Output HTML path
    csv_to_html(csv_file, output_html)

    logger.info(f"HTML gallery created at {output_html}")
