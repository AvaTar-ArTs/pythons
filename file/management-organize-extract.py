"""
File Management Organize Extract 16

This module provides functionality for file management organize extract 16.

Author: Auto-generated
Date: 2025-11-01
"""

from pathlib import Path
import os
import re
from difflib import unified_diff

import logging

logger = logging.getLogger(__name__)


# List of files to merge
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

# Output file
output_file = Path("/Users/steven/Documents/podcast/merged_unique_output.md")


# Function to extract headers and their content
def extract_sections(file_content):
    """extract_sections function."""

    sections = {}
    current_header = None
    for line in file_content.splitlines():
        header_match = re.match(r"^(#+)\s*(.*)", line)
        if header_match:
            current_header = header_match.group(2).strip()
            sections[current_header] = []
        elif current_header:
            sections[current_header].append(line.strip())
    return sections

    # Function to compare and keep only unique content between sections
    """get_unique_sections function."""


def get_unique_sections(file_sections):
    combined_sections = {}
    for header, content in file_sections.items():
        # Create a combined version for each unique header
        content_str = Path("\n").join(content)
        if header in combined_sections:
            # Compare content to keep only unique differences
            combined_str = Path("\n").join(combined_sections[header])
            diff = list(unified_diff(combined_str.splitlines(), content_str.splitlines()))
            if diff:
                combined_sections[header].append(f"\n--- Changes from {header} ---")
                combined_sections[header].extend(diff)
        else:
            combined_sections[header] = content
    return combined_sections

    """merge_files function."""


# Function to merge files and keep non-identical aspects only
def merge_files(file_list, output):
    combined_sections = {}

    for file in file_list:
        if os.path.exists(file):
            with open(file, "r") as infile:
                content = infile.read()
                file_sections = extract_sections(content)
                unique_sections = get_unique_sections(file_sections)
                # Combine all unique sections
                for header, lines in unique_sections.items():
                    if header not in combined_sections:
                        combined_sections[header] = lines
                    else:
                        combined_sections[header].extend(lines)
        else:
            logger.info(f"File not found: {file}")

    # Write merged content into the output file, organized by headers
    with open(output, "w") as outfile:
        for header, content in combined_sections.items():
            outfile.write(f"# {header}\n")
            outfile.write(Path("\n").join(content))
            outfile.write(Path("\n\n"))

    logger.info(f"Merged unique content saved to: {output}")


# Merge the files
merge_files(files_to_merge, output_file)
