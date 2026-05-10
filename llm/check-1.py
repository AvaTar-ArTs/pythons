"""
Summary of check-1.py

This module is part of the AVATARARTS ecosystem.
For more information about the AVATARARTS project, see the main documentation.
"""

import sys
from pypdf import PdfReader

import logging

logger = logging.getLogger(__name__)


# Script for Claude to run to determine whether a PDF has fillable form fields. See forms.md.


reader = PdfReader(sys.argv[1])
if reader.get_fields():
    logger.info("This PDF has fillable form fields")
else:
    logger.info(
        "This PDF does not have fillable form fields; you will need to visually determine where to enter data"
    )
