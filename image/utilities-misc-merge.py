"""
Utilities Misc Toc Merge

This module provides functionality for utilities misc toc merge.

Author: Auto-generated
Date: 2025-11-01
"""

from pypdf import PdfReader as PdfReader_pypdf
from pypdf import PdfWriter as PdfWriter_pypdf
from PyPDF2 import PdfReader, PdfWriter
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

    """merge_pdfs function."""


def merge_pdfs(toc_path, main_pdf_path, output_path):
    toc_reader = PdfReader(toc_path)
    main_reader = PdfReader(main_pdf_path)
    writer = PdfWriter()

    # Add TOC pages
    for page in toc_reader.pages:
        writer.add_page(page)

    # Add main PDF pages
    for page in main_reader.pages:
        writer.add_page(page)

    with open(output_path, "wb") as output_file:
        writer.write(output_file)

    """add_bookmarks function."""


def add_bookmarks(output_path, toc_items):
    reader = PdfReader_pypdf(output_path)
    writer = PdfWriter_pypdf()

    for page in reader.pages:
        writer.add_page(page)

    for item in toc_items:
        title = item["title"]
        page_num = item["page"] - 1  # Page numbers are zero-indexed
        writer.add_outline_item(title, page_num)

    with open(output_path, "wb") as output_file:
        writer.write(output_file)


# Example TOC items
toc_items = [
    {"title": "Introduction", "page": 1},
    {"title": "Authentication", "page": 2},
    {"title": "Upload Image", "page": 3},
    # Add more items as needed
]

# Create TOC PDF
create_toc_pdf(toc_items, "toc.pdf")

# Merge TOC with main document
merge_pdfs("toc.pdf", "main_document.pdf", "final_document.pdf")

# Add bookmarks to the final document
add_bookmarks("final_document.pdf", toc_items)
