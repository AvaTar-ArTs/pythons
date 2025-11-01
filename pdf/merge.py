"""
Pdf Merge

This module provides functionality for pdf merge.

Author: Auto-generated
Date: 2025-11-01
"""

from pathlib import Path
import os

from PyPDF2 import PdfMerger

import logging

logger = logging.getLogger(__name__)


# Directory containing the PDF files
pdf_dir = Path("/Users/steven/Documents/project2025/book")

# Output file name
output_file = "merged_document.pdf"

# Create a PdfMerger object
merger = PdfMerger()

# Iterate through the files in the directory in order from ch1.pdf to ch30.pdf
for i in range(1, 31):
    pdf_file = f"ch{i}.pdf"
    pdf_path = os.path.join(pdf_dir, pdf_file)
    if os.path.isfile(pdf_path):
        merger.append(pdf_path)
    else:
        logger.info(f"Warning: {pdf_path} does not exist")

# Write the merged PDF to a file
merger.write(os.path.join(pdf_dir, output_file))
merger.close()

logger.info(f"Merged PDF saved as {output_file}")
