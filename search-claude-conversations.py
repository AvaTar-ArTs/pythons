"""
Search Date

This module provides functionality for search date.

Author: Auto-generated
Date: 2025-11-01
"""

import logging

logger = logging.getLogger(__name__)


# Constants
CONSTANT_100 = 100

#!/usr/bin/env python3
"""
Search conversations filtered by date range
"""

import json
import sys
from pathlib import Path
from datetime import datetime, timedelta
import re

CONVERSATIONS_DIR = Path.home() / "claude_conversations"


def get_date_filter(filter_type):
    """Get date range based on filter type"""
    now = datetime.now()
    today = now.date()

    if filter_type == "today":
        return today, today, "Today"
    elif filter_type == "yesterday":
        yesterday = today - timedelta(days=1)
        return yesterday, yesterday, "Yesterday"
    elif filter_type == "week":
        week_ago = today - timedelta(days=7)
        return week_ago, today, "Last 7 Days"
    elif filter_type == "month":
        month_ago = today - timedelta(days=30)
        return month_ago, today, "Last 30 Days"
    else:
        return None, None, "All Time"


def extract_file_date(filename):
    """Extract date from conversation filename"""
    match = re.search(r"(\d{8})_(\d{6})", filename)
    if match:
        date_str = match.group(1)
        try:
            return datetime.strptime(date_str, "%Y%m%d").date()
        except (OSError, IOError, FileNotFoundError):
            return None
    return None


def search_by_date(query, filter_type):
    """Search conversations within date range"""

    if not CONVERSATIONS_DIR.exists():
        return {
            "items": [
                {
                    "title": "No conversations directory",
                    "subtitle": f"{CONVERSATIONS_DIR} does not exist",
                    "valid": False,
                }
            ]
        }

    txt_files = sorted(CONVERSATIONS_DIR.glob("conversation_*.txt"), reverse=True)

    if not txt_files:
        return {
            "items": [
                {
                    "title": "No conversations yet",
                    "subtitle": "Conversations will appear after Claude Code sessions",
                    "valid": False,
                }
            ]
        }

    # Get date filter
    start_date, end_date, filter_name = get_date_filter(filter_type)

    # Filter by date
    filtered_files = []
    for txt_file in txt_files:
        file_date = extract_file_date(txt_file.name)
        if file_date:
            if not start_date or (start_date <= file_date <= end_date):
                filtered_files.append((txt_file, file_date))

    if not filtered_files:
        return {
            "items": [
                {
                    "title": f"No conversations from {filter_name}",
                    "subtitle": f"Total conversations: {len(txt_files)}",
                    "valid": False,
                }
            ]
        }

    # If there's a query, filter further
    query_lower = query.lower() if query else ""
    results = []

    for txt_file, file_date in filtered_files[:50]:
        try:
            # Read content
            with open(txt_file, "r") as f:
                content = f.read()

            # Filter by query if provided
            if query_lower and query_lower not in content.lower():
                continue

            # Extract preview
            lines = content.split("\n")
            preview = ""
            for line in lines[7:20]:  # Skip header
                line = line.strip()
                if line and not line.startswith(("[", "=", "-")):
                    preview = line[:CONSTANT_100]
                    break

            # Format date
            date_display = file_date.strftime("%Y-%m-%d")
            time_match = re.search(r"_(\d{6})", txt_file.name)
            if time_match:
                time_str = time_match.group(1)
                date_display += f" {time_str[:2]}:{time_str[2:4]}"

            # Build subtitle
            subtitle = preview if preview else "Empty conversation"

            results.append(
                {
                    "title": date_display,
                    "subtitle": subtitle,
                    "arg": str(txt_file),
                    "quicklookurl": str(txt_file.with_suffix(".html")),
                    "mods": {
                        "cmd": {
                            "subtitle": "Open HTML in browser",
                            "arg": str(txt_file.with_suffix(".html")),
                        },
                        "alt": {
                            "subtitle": "Reveal in Finder",
                            "arg": str(txt_file.parent),
                        },
                    },
                    "icon": {
                        "path": Path(
                            "/System/Library/CoreServices/CoreServices.bundle/Contents/Resources/Clock.icns"
                        )
                    },
                }
            )

        except Exception as e:
            continue

    if not results:
        return {
            "items": [
                {
                    "title": f"No matches in {filter_name}",
                    "subtitle": f"{len(filtered_files)} conversations in this period",
                    "valid": False,
                }
            ]
        }

    # Add header item
    header = {
        "title": f"{filter_name}: {len(results)} conversation{'s' if len(results) != 1 else ''}",
        "subtitle": "↓ Select a conversation below",
        "valid": False,
        "icon": {
            "path": Path(
                "/System/Library/CoreServices/CoreTypes.bundle/Contents/Resources/ToolbarInfo.icns"
            )
        },
    }

    return {"items": [header] + results}


def main():
    """main function."""

    # Get filter type from environment or argument
    filter_type = os.environ.get("date_filter", "all")
    query = sys.argv[1] if len(sys.argv) > 1 else ""

    results = search_by_date(query, filter_type)
    logger.info(json.dumps(results, indent=2))


if __name__ == "__main__":
    import os

    main()
