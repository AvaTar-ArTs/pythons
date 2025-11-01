"""
Ai Tools Claude Check 30

This module provides functionality for ai tools claude check 30.

Author: Auto-generated
Date: 2025-11-01
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
    logger.info("This PDF does not have fillable form fields; you will need to visually determine where to enter data")
