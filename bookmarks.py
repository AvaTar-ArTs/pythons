"""
Bookmarks

This module provides functionality for bookmarks.

Author: Auto-generated
Date: 2025-11-01
"""

from pypdf import PdfReader, PdfWriter


def add_bookmarks(output_path, toc_items):
    """add_bookmarks function."""

    reader = PdfReader(output_path)
    writer = PdfWriter()

    for page in reader.pages:
        writer.add_page(page)

    for item in toc_items:
        title = item["title"]
        page_num = item["page"] - 1  # Page numbers are zero-indexed
        writer.add_outline_item(title, page_num)

    with open(output_path, "wb") as output_file:
        writer.write(output_file)


toc_items = [
    {"title": "Introduction", "page": 1},
    {"title": "Authentication", "page": 2},
    {"title": "Upload Image", "page": 3},
    # Add more items as needed
]

add_bookmarks("final_document.pdf", toc_items)
