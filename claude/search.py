"""
Ai Tools Claude Search 7

This module provides functionality for ai tools claude search 7.

Author: Auto-generated
Date: 2025-11-01
"""

import logging

logger = logging.getLogger(__name__)


# Constants
CONSTANT_100 = 100
CONSTANT_150 = 150
CONSTANT_1024 = 1024

#!/usr/bin/env python3
"""
Alfred Script Filter for Claude Code Conversations - Enhanced Version
- Intelligent caching for performance
- Better conversation previews
- Smart subtitle generation
"""

import json
import sys
import os
from pathlib import Path
from datetime import datetime, timedelta
import re
import hashlib

# Configuration
CONVERSATIONS_DIR = Path.home() / "claude_conversations"
MAX_RESULTS = 50
CACHE_DIR = Path.home() / ".cache" / "claude_conversations_alfred"
CACHE_TTL_SECONDS = 30  # Cache for 30 seconds


def get_cache_path():
    """Get cache file path"""
    CACHE_DIR.mkdir(parents=True, exist_ok=True)
    return CACHE_DIR / "conversation_cache.json"


def is_cache_valid():
    """Check if cache is still valid"""
    cache_path = get_cache_path()
    if not cache_path.exists():
        return False

    mtime = datetime.fromtimestamp(cache_path.stat().st_mtime)
    age = datetime.now() - mtime
    return age.total_seconds() < CACHE_TTL_SECONDS


def load_cache():
    """Load cached conversation data"""
    cache_path = get_cache_path()
    try:
        with open(cache_path, "r") as f:
            return json.load(f)
    except (OSError, IOError, FileNotFoundError):
        return None


def save_cache(data):
    """Save conversation data to cache"""
    cache_path = get_cache_path()
    try:
        with open(cache_path, "w") as f:
            json.dump(data, f)
    except (OSError, IOError, FileNotFoundError):
        pass


def extract_conversation_preview(file_path, max_length=CONSTANT_150):
    """Extract meaningful preview from conversation"""
    try:
        with open(file_path, "r") as f:
            lines = f.readlines()

        # Skip header (first 7 lines)
        content_lines = lines[7:] if len(lines) > 7 else lines

        # Find first substantive user message
        preview_parts = []
        current_role = None

        for line in content_lines[:50]:  # Look at first 50 lines
            line = line.strip()

            if line.startswith("[USER]"):
                current_role = "user"
                continue
            elif line.startswith("[ASSISTANT]"):
                current_role = "assistant"
                continue
            elif line.startswith("[TOOL"):
                current_role = None
                continue

            # Collect content
            if line and current_role and not line.startswith("["):
                preview_parts.append(line)
                if len(" ".join(preview_parts)) > max_length:
                    break

        preview = " ".join(preview_parts)

        # Truncate if too long
        if len(preview) > max_length:
            preview = preview[:max_length] + "..."

        return preview if preview else "Empty conversation"

    except Exception as e:
        return "Error reading conversation"


def parse_conversation_metadata(file_path):
    """Extract metadata with intelligent parsing"""
    try:
        with open(file_path, "r") as f:
            content = f.read()

        # Count different elements
        user_count = content.count("[USER]")
        assistant_count = content.count("[ASSISTANT]")
        tool_matches = re.findall(r"\[TOOL: ([^\]]+)\]", content)
        tool_count = len(tool_matches)

        # Extract unique tools used
        unique_tools = list(set(tool_matches))[:3]  # Top 3 tools

        # Get export date from header
        lines = content.split("\n")
        export_date = ""
        for line in lines[:5]:
            if line.startswith("Exported:"):
                export_date = line.replace("Exported:", "").strip()
                break

        # Get word count approximation
        word_count = len(content.split())

        # Extract first meaningful exchange
        preview = extract_conversation_preview(file_path)

        return {
            "export_date": export_date,
            "user_count": user_count,
            "assistant_count": assistant_count,
            "tool_count": tool_count,
            "unique_tools": unique_tools,
            "word_count": word_count,
            "preview": preview,
            "total_exchanges": user_count + assistant_count,
        }
    except Exception as e:
        return None


def build_smart_subtitle(metadata, query, matches=None):
    """Build intelligent subtitle based on context"""

    # If there's a query with matches, show matches
    if query and matches:
        return " | ".join(matches[:2])  # Show top 2 matches

    # Otherwise, show conversation preview
    parts = []

    # Add exchange count
    if metadata["user_count"] > 0:
        parts.append(f"💬 {metadata['total_exchanges']} messages")

    # Add tool info if present
    if metadata["tool_count"] > 0:
        tool_names = ", ".join(metadata["unique_tools"])
        parts.append(f"🔧 {tool_names}")

    # Add preview
    if metadata["preview"]:
        parts.append(metadata["preview"])

    return " | ".join(parts) if parts else "Empty conversation"


def get_conversations_metadata():
    """Get or build metadata for all conversations"""

    # Check cache first
    if is_cache_valid():
        cached = load_cache()
        if cached:
            return cached

    if not CONVERSATIONS_DIR.exists():
        return {}

    txt_files = list(CONVERSATIONS_DIR.glob("conversation_*.txt"))
    metadata_map = {}

    for txt_file in txt_files:
        metadata = parse_conversation_metadata(txt_file)
        if metadata:
            metadata_map[str(txt_file)] = metadata

    # Save to cache
    save_cache(metadata_map)

    return metadata_map


def search_conversations(query):
    """Search through conversations with intelligent ranking"""

    if not CONVERSATIONS_DIR.exists():
        return {
            "items": [
                {
                    "title": "No conversations found",
                    "subtitle": f"Directory {CONVERSATIONS_DIR} does not exist",
                    "valid": False,
                    "icon": {
                        "path": Path(
                            "/System/Library/CoreServices/CoreTypes.bundle/Contents/Resources/AlertCautionIcon.icns"
                        )
                    },
                }
            ]
        }

    txt_files = sorted(CONVERSATIONS_DIR.glob("conversation_*.txt"), reverse=True)

    if not txt_files:
        return {
            "items": [
                {
                    "title": "No conversations saved yet",
                    "subtitle": "Start a Claude Code session and conversations will auto-save here",
                    "valid": False,
                    "icon": {
                        "path": Path(
                            "/System/Library/CoreServices/CoreTypes.bundle/Contents/Resources/BookmarkIcon.icns"
                        )
                    },
                }
            ]
        }

    # Get metadata (cached or fresh)
    metadata_map = get_conversations_metadata()

    results = []
    query_lower = query.lower() if query else ""

    for txt_file in txt_files[:MAX_RESULTS]:
        try:
            # Get cached metadata
            metadata = metadata_map.get(str(txt_file))
            if not metadata:
                metadata = parse_conversation_metadata(txt_file)

            # If query provided, search content
            matches = []
            if query_lower:
                with open(txt_file, "r") as f:
                    content = f.read()

                if query_lower not in content.lower():
                    continue

                # Find matching lines for context
                for line in content.split("\n"):
                    if query_lower in line.lower() and not line.startswith(
                        ("[", "=", "-", "CLAUDE", "Exported", "Source")
                    ):
                        clean_line = line.strip()[:CONSTANT_100]
                        if clean_line:
                            matches.append(clean_line)
                            if len(matches) >= 2:
                                break

            # Format filename for display
            filename = txt_file.stem
            date_match = re.search(r"(\d{8})_(\d{6})", filename)
            if date_match:
                date_str = date_match.group(1)
                time_str = date_match.group(2)
                formatted_date = f"{date_str[:4]}-{date_str[4:6]}-{date_str[6:8]} {time_str[:2]}:{time_str[2:4]}"
            else:
                formatted_date = filename

            # Build smart subtitle
            subtitle = build_smart_subtitle(metadata, query_lower, matches)

            # Get file info
            file_size_kb = txt_file.stat().st_size / CONSTANT_1024
            html_path = txt_file.with_suffix(".html")

            # Build result
            result = {
                "title": formatted_date,
                "subtitle": subtitle,
                "arg": str(txt_file),
                "quicklookurl": str(html_path) if html_path.exists() else str(txt_file),
                "mods": {
                    "cmd": {
                        "subtitle": f"Open HTML in browser • {file_size_kb:.1f}KB • {metadata['word_count']} words",
                        "arg": str(html_path) if html_path.exists() else str(txt_file),
                    },
                    "alt": {
                        "subtitle": "Reveal in Finder",
                        "arg": str(txt_file.parent),
                    },
                    "ctrl": {
                        "subtitle": f"Copy: {txt_file.name}",
                        "arg": str(txt_file),
                    },
                    "shift": {
                        "subtitle": f"Preview: {metadata['total_exchanges']} exchanges, {metadata['tool_count']} tools",
                        "arg": str(txt_file),
                    },
                },
                "icon": {
                    "path": Path(
                        "/System/Library/CoreServices/CoreTypes.bundle/Contents/Resources/DocumentIcon.icns"
                    )
                },
                "text": {
                    "copy": str(txt_file),
                    "largetype": f"{formatted_date}\n\n{subtitle}",
                },
                "variables": {
                    "tool_count": str(metadata["tool_count"]),
                    "message_count": str(metadata["total_exchanges"]),
                },
            }

            results.append(result)

        except Exception as e:
            continue

    if not results and query_lower:
        return {
            "items": [
                {
                    "title": f"No matches for '{query}'",
                    "subtitle": f"Searched {len(txt_files)} conversations",
                    "valid": False,
                    "icon": {
                        "path": Path(
                            "/System/Library/CoreServices/CoreTypes.bundle/Contents/Resources/FinderIcon.icns"
                        )
                    },
                }
            ]
        }

    return {"items": results}


def main():
    """main function."""

    query = sys.argv[1] if len(sys.argv) > 1 else ""
    results = search_conversations(query)
    logger.info(json.dumps(results, indent=2))


if __name__ == "__main__":
    main()
