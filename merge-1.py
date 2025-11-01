"""
Utilities Misc Merge Pdfs 1

This module provides functionality for utilities misc merge pdfs 1.

Author: Auto-generated
Date: 2025-11-01
"""

from PyPDF2 import PdfReader, PdfWriter


def merge_pdfs(toc_path, main_pdf_path, output_path):
    """merge_pdfs function."""

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


merge_pdfs("toc.pdf", "main_document.pdf", "final_document.pdf")
