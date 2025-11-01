"""
Utilities Misc Pdfcsv 1

This module provides functionality for utilities misc pdfcsv 1.

Author: Auto-generated
Date: 2025-11-01
"""

import tabula

filename = input("Enter File Path: ")
df = tabula.read_pdf(filename, encoding="utf-8", spreadsheet=True, pages="1")

df.to_csv("output.csv")
