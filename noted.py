"""
Noted

This module provides functionality for noted.

Author: Auto-generated
Date: 2025-11-01
"""

from pathlib import Path
import re

import pandas as pd

import logging

logger = logging.getLogger(__name__)


def parse_markdown_to_table(md_file):
    """
    Parses a Markdown file to extract trends, designs, and tags into a structured table.
    """
    with open(md_file, "r") as file:
        content = file.read()

    # Regex patterns to match required components
    trend_pattern = r"\| (\d+)\s+\|"
    title_pattern = r"\| \[(.*?)\]\((.*?)\)"
    tags_pattern = r"\| ([^\|]+)\s*\|$"

    # Splitting lines to process each row
    lines = content.splitlines()
    data = []
    for line in lines:
        if line.startswith("|") and not line.startswith("| ---"):
            trend_match = re.search(trend_pattern, line)
            title_match = re.search(title_pattern, line)
            tags_match = re.search(tags_pattern, line)

            if trend_match and title_match and tags_match:
                trend = trend_match.group(1)
                title = title_match.group(1)
                product_url = title_match.group(2)
                tags = tags_match.group(1).strip()

                data.append(
                    {
                        "Trend": trend,
                        "Title/Name": title,
                        "Product URL": product_url,
                        "Keywords": tags,
                    }
                )

    # Convert to DataFrame
    return pd.DataFrame(data)


# Usage Example
md_file_path = Path(
    str(Path.home()) + "/Downloads/4.md"
)  # Replace with your Markdown file path
output_csv = Path(str(Path.home()) + "/Downloads/4.csv")

# Parse and save to CSV
df = parse_markdown_to_table(md_file_path)
df.to_csv(output_csv, index=False)

logger.info(f"Data compiled and saved to {output_csv}")
