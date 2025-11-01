"""
Pdf2Html

This module provides functionality for pdf2html.

Author: Auto-generated
Date: 2025-11-01
"""

import fitz  # Import PyMuPDF
import os

import logging

logger = logging.getLogger(__name__)


def extract_images_from_pdf(pdf_path, output_folder):
    """extract_images_from_pdf function."""

    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    doc = fitz.open(pdf_path)
    for page_num in range(len(doc)):
        for img_index, img in enumerate(doc.get_page_images(page_num)):
            xref = img[0]
            base_image = doc.extract_image(xref)
            image_bytes = base_image["image"]
            image_ext = base_image["ext"]
            image_filename = f"{output_folder}/image_{page_num+1}_{img_index+1}.{image_ext}"
            with open(image_filename, "wb") as img_file:
                img_file.write(image_bytes)
    doc.close()

    """generate_html_gallery function."""

def generate_html_gallery(image_folder, html_output_file):
    image_files = [f for f in os.listdir(image_folder) if f.endswith(('.png', '.jpg', '.jpeg', '.tiff'))]
    with open(html_output_file, 'w') as file:
        file.write("<!DOCTYPE html>\n")
        file.write("<html>\n<head>\n<title>Photo Gallery</title>\n</head>\n<body>\n")
        file.write("<div style='display: flex; flex-wrap: wrap;'>\n")
        for image in image_files:
            file.write(f"<img src='{image_folder}/{image}' style='margin: 10px; width: 200px; height: auto;'>\n")
        file.write("</div>\n</body>\n</html>")
    """main function."""


def main():
    source_path = input("Enter the path to the PDF file or directory: ")
    if os.path.isfile(source_path):
        output_folder = os.path.join(os.path.dirname(source_path), os.path.splitext(os.path.basename(source_path))[0] + '_images')
        extract_images_from_pdf(source_path, output_folder)
        html_output_file = os.path.join(output_folder, "gallery.html")
        generate_html_gallery(output_folder, html_output_file)
    else:
        logger.info("Invalid file path. Please enter a valid path to a PDF file.")

if __name__ == "__main__":
    main()
