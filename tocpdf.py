"""
Utilities Misc Tocpdf 1

This module provides functionality for utilities misc tocpdf 1.

Author: Auto-generated
Date: 2025-11-01
"""

from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas


def create_toc_pdf(toc_items, output_path):
    """create_toc_pdf function."""

    c = canvas.Canvas(output_path, pagesize=letter)
    width, height = letter
    c.setFont("Helvetica", 12)

    y_position = height - 40
    for item in toc_items:
        text = f"{item['title']} ... {item['page']}"
        c.drawString(40, y_position, text)
        y_position -= 20

    c.save()


toc_items = [
    {"title": "Introduction", "page": 1},
    {"title": "Authentication", "page": 2},
    {"title": "Upload Image", "page": 3},
    # Add more items as needed
]

create_toc_pdf(toc_items, "toc.pdf")
