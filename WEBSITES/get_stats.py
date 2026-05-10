import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
#!/usr/bin/env python3
"""
Get statistics about saved conversations
"""

import json
from pathlib import Path
from datetime import datetime

CONVERSATIONS_DIR = Path.home() / "claude" / "conversations"


def get_stats():
    """Get conversation statistics"""
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

    txt_files = list(CONVERSATIONS_DIR.glob("conversation_*.txt"))
    html_files = list(CONVERSATIONS_DIR.glob("conversation_*.html"))
    md_files = list(CONVERSATIONS_DIR.glob("conversation_*.md"))

    # Calculate total size
    total_size = sum(f.stat().st_size for f in txt_files)
    total_size_mb = total_size / (1024 * 1024)

    # Get date range
    if txt_files:
        oldest = min(f.stat().st_mtime for f in txt_files)
        newest = max(f.stat().st_mtime for f in txt_files)
        oldest_date = datetime.fromtimestamp(oldest).strftime("%Y-%m-%d")
        newest_date = datetime.fromtimestamp(newest).strftime("%Y-%m-%d")
        date_range = f"{oldest_date} to {newest_date}"
    else:
        date_range = "No conversations yet"

    # Count today's conversations
    today = datetime.now().date()
    today_count = sum(
        1
        for f in txt_files
        if datetime.fromtimestamp(f.stat().st_mtime).date() == today
    )

    items = [
        {
            "title": f"📊 {len(txt_files)} Total Conversations",
            "subtitle": f"{total_size_mb:.2f} MB total size | {date_range}",
            "arg": str(CONVERSATIONS_DIR),
            "icon": {
                "path": "/System/Library/CoreServices/CoreTypes.bundle/Contents/Resources/ProfileBackgroundColor.icns"
            },
        },
        {
            "title": f"📅 {today_count} Conversations Today",
            "subtitle": "Press Enter to view today's conversations",
            "arg": str(CONVERSATIONS_DIR),
            "valid": True,
            "icon": {
                "path": "/System/Library/CoreServices/CoreTypes.bundle/Contents/Resources/Clock.icns"
            },
        },
        {
            "title": f"📝 {len(txt_files)} Text Files",
            "subtitle": "Primary search format",
            "arg": str(CONVERSATIONS_DIR),
            "icon": {
                "path": "/System/Library/CoreServices/CoreTypes.bundle/Contents/Resources/DocumentIcon.icns"
            },
        },
        {
            "title": f"🎨 {len(html_files)} HTML Files",
            "subtitle": "Presentation format",
            "arg": str(CONVERSATIONS_DIR),
            "icon": {
                "path": "/System/Library/CoreServices/CoreTypes.bundle/Contents/Resources/BookmarkIcon.icns"
            },
        },
    ]

    if md_files:
        items.append(
            {
                "title": f"📋 {len(md_files)} Markdown Files",
                "subtitle": "Documentation format",
                "arg": str(CONVERSATIONS_DIR),
                "icon": {
                    "path": "/System/Library/CoreServices/CoreTypes.bundle/Contents/Resources/DocumentIcon.icns"
                },
            }
        )

    items.append(
        {
            "title": "📁 Open Conversations Folder",
            "subtitle": str(CONVERSATIONS_DIR),
            "arg": str(CONVERSATIONS_DIR),
            "icon": {
                "path": "/System/Library/CoreServices/CoreTypes.bundle/Contents/Resources/GenericFolderIcon.icns"
            },
        }
    )

    return {"items": items}


try:
        results = get_stats()
        print(json.dumps(results, indent=2))
except KeyboardInterrupt:
    logger.info("Execution interrupted by user")
    sys.exit(1)
except Exception as e:
    logger.error(f"An error occurred: {e}", exc_info=True)
    sys.exit(1)