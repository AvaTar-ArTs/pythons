"""
File Management Organize Pods 2

This module provides functionality for file management organize pods 2.

Author: Auto-generated
Date: 2025-11-01
"""

from pathlib import Path
import os
import re
from difflib import unified_diff

import logging

logger = logging.getLogger(__name__)


# Files to merge and analyze
files_to_merge = [
    "/Users/steven/Documents/podcast/14-16-45-Podcast_Production_Assistance copy 2.md",
    Path("/Users/steven/Documents/podcast/ChatGPT-Project_2025_Imagery_Design.html"),
    "/Users/steven/Documents/podcast/14-16-45-Podcast_Production_Assistance copy.md",
    "/Users/steven/Documents/podcast/Content Plan & Strategy.md",
    Path("/Users/steven/Documents/podcast/JusticeThomas.md"),
    Path("/Users/steven/Documents/podcast/podcast-palyerzs.md"),
    Path("/Users/steven/Documents/podcast/Podcast-Trump.md"),
    "/Users/steven/Documents/podcast/Transition from Donald Trump to The Messiah of Mar-a-Lago.md",
]

# Output file path
output_file = Path("/Users/steven/Documents/podcast/merged_unique_output.md")


# Function to extract headers and corresponding content
def extract_sections(file_content):
    """extract_sections function."""

    sections = {}
    current_header = None
    current_content = []

    for line in file_content.splitlines():
        header_match = re.match(r"^(#+)\s*(.*)", line)
        if header_match:
            # Save the previous section if it exists
            if current_header:
                sections[current_header] = Path("\n").join(current_content).strip()
            # Start a new section
            current_header = header_match.group(2).strip()
            current_content = []
        else:
            current_content.append(line.strip())

    # Add the last section
    if current_header:
        sections[current_header] = Path("\n").join(current_content).strip()

    return sections

    # Function to compare sections and return only non-identical parts
    """compare_sections function."""


def compare_sections(sections1, sections2):
    unique_sections = {}

    for header, content1 in sections1.items():
        if header in sections2:
            content2 = sections2[header]
            diff = list(unified_diff(content1.splitlines(), content2.splitlines()))
            if diff:
                unique_sections[header] = Path("\n").join(diff)
        else:
            unique_sections[header] = content1

    # Include sections unique to the second file
    for header, content2 in sections2.items():
        if header not in sections1:
            unique_sections[header] = content2

    return unique_sections

    """merge_files function."""


# Function to merge and categorize based on episodes/themes
def merge_files(file_list, output):
    merged_sections = {}

    for file in file_list:
        if os.path.exists(file):
            with open(file, "r") as infile:
                content = infile.read()
                sections = extract_sections(content)

                if merged_sections:
                    # Compare the new sections with the already merged ones
                    merged_sections = compare_sections(merged_sections, sections)
                else:
                    merged_sections = sections
        else:
            logger.info(f"File not found: {file}")

    # Write organized output based on headers (like episodes/themes)
    with open(output, "w") as outfile:
        for header, content in merged_sections.items():
            outfile.write(f"# {header}\n")
            outfile.write(f"{content}\n\n")

    logger.info(f"Merged content saved to: {output}")


# Run the script
merge_files(files_to_merge, output_file)
