"""
Save Exit

This module provides functionality for save exit.

Author: Auto-generated
Date: 2025-11-01
"""

import logging

logger = logging.getLogger(__name__)

#!/usr/bin/env python3
"""
Auto-save conversation on exit keywords
Triggers conversation export when user types: exit, bye, save, done
"""

import json
import sys
import subprocess
import os
from pathlib import Path

# Keywords that trigger auto-save
SAVE_KEYWORDS = ["exit", "bye", "save", "done", "quit", "goodbye"]

# Path to conversation exporter
EXPORTER_PATH = Path(str(Path.home()) + "/Documents/python/conversation_exporter.py")


def should_save(user_message):
    """Check if user message contains save keywords"""
    message_lower = user_message.lower().strip()

    # Exact match
    if message_lower in SAVE_KEYWORDS:
        return True

    # Starts with keyword
    for keyword in SAVE_KEYWORDS:
        if message_lower.startswith(keyword):
            return True

    return False


def run_exporter(transcript_path):
    """Run the conversation exporter"""
    try:
        # Prepare input for exporter
        hook_input = json.dumps({"transcript_path": transcript_path})

        # Run exporter
        result = subprocess.run(
            ["python3", str(EXPORTER_PATH)],
            input=hook_input,
            capture_output=True,
            text=True,
            timeout=30,
        )

        if result.returncode == 0:
            return True, result.stdout
        else:
            return False, result.stderr

    except Exception as e:
        return False, str(e)


def main():
    """main function."""

    try:
        # Read hook input from stdin
        hook_input = json.loads(sys.stdin.read())

        # Get user message and transcript path
        user_message = hook_input.get("user_message", "")
        transcript_path = hook_input.get("transcript_path", "")

        # Check if we should save
        if should_save(user_message):
            if transcript_path:
                # Run exporter
                success, output = run_exporter(transcript_path)

                if success:
                    # Return success with message to user
                    response = {
                        "action": "allow",
                        "notification": {
                            "title": "💾 Conversation Saved!",
                            "message": "Exported to ~/claude/conversations/",
                        },
                    }
                    logger.info(json.dumps(response))
                    sys.exit(0)
                else:
                    # Failed but allow message through
                    response = {
                        "action": "allow",
                        "notification": {
                            "title": "⚠️ Save Failed",
                            "message": "Check exporter configuration",
                        },
                    }
                    logger.info(json.dumps(response))
                    sys.exit(0)

        # Not a save keyword, allow message through
        logger.info(json.dumps({"action": "allow"}))
        sys.exit(0)

    except Exception as e:
        # On error, allow message through
        logger.info(json.dumps({"action": "allow"}))
        sys.exit(1)


if __name__ == "__main__":
    main()
