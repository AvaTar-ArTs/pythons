
import logging

logger = logging.getLogger(__name__)


# Constants
CONSTANT_100 = 100
CONSTANT_444 = 444
CONSTANT_555 = 555

#!/usr/bin/env python3
"""
Merged Content Analysis Tool

This file was automatically merged from the following source files:
- /Users/steven/Music/nocTurneMeLoDieS/python/FINAL_ORGANIZED/generation/generate-category.py
- /Users/steven/Music/nocTurneMeLoDieS/python/DUPLICATES_ARCHIVE/generate_variants_generate-category.py

Combines the best features and functionality from multiple similar files.
"""

# Imports from all source files
from pathlib import Path
import os
import re

# Documentation from source files
        """
            """
    html_content += """
    """
            html_content += f"""
        html_content += """
    html_content = """

HTML_DIRECTORY = Path("/Users/steven/Documents/HTML")

# Categories and keywords to search for in HTML files
CATEGORIES = {
    "Art & Design": [
        "art",
        "design",
        "creative",
        "raccoon",
        "fantasy",
        "cosmic",
        "whimsical",
        "coverart",
        "mystical",
    ],
    "Technology": [
        "tech",
        "code",
        "programming",
        "automation",
        "embed",
        "convert",
        "script",
        "upscale",
        "FTP",
        "digital",
    ],
    "Guides & Tutorials": [
        "guide",
        "tutorial",
        "how to",
        "project",
        "tips",
        "create",
        "troubleshoot",
        "summary",
        "instruction",
    ],
    "Miscellaneous": [],  # Default category if no keywords match
}


# Function to read the content of an HTML file
def read_html_file(file_path):
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            return file.read().lower()
    except Exception as e:
        logger.info(f"Error reading {file_path}: {e}")
        return ""


# Function to extract a meaningful title from the HTML file's <title> tag
def extract_title(content):
    match = re.search(r"<title>(.*?)<\/title>", content)
    if match:
        return match.group(1).strip()
    return None


# Function to categorize a file based on its content
def categorize_file(file_path):
    content = read_html_file(file_path)
    file_name = os.path.basename(file_path).lower()

    # Check for keywords in both the filename and the file content
    for category, keywords in CATEGORIES.items():
        for keyword in keywords:
            if keyword in file_name or keyword in content:
                return category
    return "Miscellaneous"


# Scan the HTML directory and categorize each file
def scan_and_categorize(directory):
    categorized_files = {category: [] for category in CATEGORIES}
    for filename in os.listdir(directory):
        if filename.endswith(".html"):
            full_path = os.path.join(directory, filename)
            category = categorize_file(full_path)
            title = (
                extract_title(read_html_file(full_path))
                or filename.replace("_", " ").replace(".html", "").title()
            )
            categorized_files[category].append({"title": title, "path": full_path})
    return categorized_files


# Generate the categorized tabs HTML content
def generate_html(categorized_files):
    html_content = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Avatar Arts HTML Reference Library</title>
        <style>
            body { font-family: 'Arial', sans-serif; background-color: #2d2d2d; color: #eaeaea; padding: 20px; }
            .tabs { display: flex; justify-content: center; margin-bottom: 20px; }
            .tabs button { background-color: #CONSTANT_444; color: #eaeaea; border: none; padding: 10px 20px; cursor: pointer; margin: 0 5px; border-radius: 5px; }
            .tabs button.active { background-color: #ff5f5f; }
            .tabs button:hover { background-color: #CONSTANT_555; }
            .category-content { display: none; }
            .category-content.active { display: block; }
            .table-container { width: 90%; max-width: 1200px; margin: auto; }
            table { width: CONSTANT_100%; border-collapse: collapse; color: #eaeaea; margin-bottom: 20px; }
            th, td { padding: 10px; text-align: left; }
            th { background-color: #CONSTANT_444; border-bottom: 2px solid #CONSTANT_555; text-transform: uppercase; }
            tr:nth-child(even) { background-color: #3a3a3a; }
            tr:hover { background-color: #CONSTANT_555; }
            td a { color: #ff5f5f; text-decoration: none; }
            td a:hover { text-decoration: underline; }
        </style>
    </head>
    <body>
        <h1>Avatar Arts HTML Reference Library</h1>
        <div class="tabs">
    """

    # Create buttons for each category
    for category in categorized_files.keys():
        html_content += f"<button onclick=\"showCategory('{category.lower()}')\">{category}</button>"

    html_content += "</div>"

    # Generate HTML for each category
    for category, files in categorized_files.items():
        html_content += f'<div id="{category.lower()}" class="category-content">'
        html_content += """
        <div class="table-container">
            <table>
                <thead>
                    <tr>
                        <th>Title</th>
                        <th>Access Link</th>
                    </tr>
                </thead>
                <tbody>
        """
        for file in files:
            html_content += f"""
            <tr>
                <td>{file['title']}</td>
                <td><a href="file://{file['path']}" target="_blank">Open</a></td>
            </tr>
            """
        html_content += "</tbody></table></div></div>"

    # JavaScript to handle tab switching
    html_content += """
    <script>
        function showCategory(category) {
            var categories = document.getElementsByClassName('category-content');
            for (var i = 0; i < categories.length; i++) {
                categories[i].style.display = 'none';
            }
            var buttons = document.querySelectorAll('.tabs button');
            buttons.forEach(button => button.classList.remove('active'));
            document.getElementById(category).style.display = 'block';
            event.target.classList.add('active');
        }
        document.querySelectorAll('.tabs button')[0].click(); // Open the first tab by default
    </script>
    </body>
    </html>
    """
    return html_content


# Save the generated HTML file
def save_html(content, output_path):
    with open(output_path, "w", encoding="utf-8") as file:
        file.write(content)


if __name__ == "__main__":
    categorized_files = scan_and_categorize(HTML_DIRECTORY)
    html_content = generate_html(categorized_files)
    save_html(html_content, Path("/Users/steven/Documents/HTML/index.html"))
    logger.info("Generated categorized HTML index at /Users/steven/Documents/HTML/index.html")
