import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
"""
Summary of category_flake8_1.py

This module is part of the AVATARARTS ecosystem.
For more information about the AVATARARTS project, see the main documentation.
"""

import re
from collections import defaultdict


def categorize_flake8_output(file_path):
    with open(file_path, "r") as file:
        lines = file.readlines()

    issues = defaultdict(list)

    for line in lines:
        match = re.match(r"(./[^:]+):(\d+):\d+: (\w\d+) (.+)", line)
        if match:
            file_name, line_number, code, message = match.groups()
            issues[code].append((file_name, line_number, message))

    return issues


def display_issues(issues):
    for code, details in sorted(issues.items()):
        print(f"\nIssues of type {code}:")
        for file_name, line_number, message in details:
            print(f"{file_name}:{line_number} - {message}")


try:
        flake8_output_path = "flake8_output.txt"  # Path to your flake8 output
except KeyboardInterrupt:
    logger.info("Execution interrupted by user")
    sys.exit(1)
except Exception as e:
    logger.error(f"An error occurred: {e}", exc_info=True)
    sys.exit(1)
file
issues = categorize_flake8_output(flake8_output_path)
display_issues(issues)
