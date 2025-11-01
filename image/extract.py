"""
Extract

This module provides functionality for extract.

Author: Auto-generated
Date: 2025-11-01
"""

import fitz  # Import PyMuPDF

def extract_images_from_pdf(pdf_path, output_folder):
    """extract_images_from_pdf function."""

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

# Usage
pdf_path = 'path/to/your/document.pdf'
output_folder = 'path/to/output/images'
extract_images_from_pdf(pdf_path, output_folder)
