"""
Summary of python-lint-complexity.py

This module is part of the AVATARARTS ecosystem.
For more information about the AVATARARTS project, see the main documentation.
"""

import logging
import os
import subprocess
from io import StringIO

from pylint.lint import Run
from radon.complexity import cc_visit

logger = logging.getLogger(__name__)


# Function to auto-format code with black
def format_with_black(filepath):
    """format_with_black function."""
    try:
        subprocess.run(["black", filepath], check=True)
        logger.info(f"Formatted {filepath} with black.")
    except subprocess.CalledProcessError as e:
        logger.info(f"Error formatting {filepath}: {e}")

    # Function to auto-sort imports with isort
    """sort_imports_with_isort function."""


def sort_imports_with_isort(filepath):
    try:
        subprocess.run(["isort", filepath], check=True)
        logger.info(f"Sorted imports in {filepath} with isort.")
    except subprocess.CalledProcessError as e:
        logger.info(f"Error sorting imports for {filepath}: {e}")

    """analyze_script function."""


# Analyze script with linting, complexity, and formatting
def analyze_script(filepath):
    analysis = {}
    analysis["Filename"] = os.path.basename(filepath)

    # Format and sort imports
    format_with_black(filepath)
    sort_imports_with_isort(filepath)

    # Run pylint
    pylint_output = StringIO()
    Run([filepath], reporter=TextReporter(pylint_output), exit=False)
    analysis["Pylint Issues"] = pylint_output.getvalue().strip()

    # Calculate cyclomatic complexity
    with open(filepath) as file:
        code = file.read()
        complexity = cc_visit(code)
        analysis["Complexity"] = ", ".join(
            [f"{x.name}: {x.complexity}" for x in complexity],
        )

    return analysis
