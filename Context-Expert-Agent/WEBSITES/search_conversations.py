#!/usr/bin/env python3
"""
Alfred Script Filter for Claude Code Conversations
Searches through saved conversation .txt files
"""

import json
import sys
import os
from pathlib import Path
from datetime import datetime
import re

# Configuration
CONVERSATIONS_DIR = Path.home() / "claude" / "conversations"
MAX_RESULTS = 50


def parse_conversation_metadata(file_path):
    """Extract metadata from conversation file"""
    try:
        with open(file_path, 'r') as f:
            lines = f.readlines()

        # Extract export date (line 3)
        export_date = ""
        if len(lines) > 2:
            match = re.search(r'Exported: (.+)', lines[2])
            if match:
                export_date = match.group(1)

        # Extract source (line 4)
        source = ""
        if len(lines) > 3:
            match = re.search(r'Source: (.+)', lines[3])
            if match:
                source = match.group(1)

        # Count messages
        content = ''.join(lines)
        user_count = content.count('[USER]')
        assistant_count = content.count('[ASSISTANT]')
        tool_count = content.count('[TOOL:')

        # Get first user message as preview
        preview = ""
        for line in lines:
            if line.strip() and not line.startswith(('CLAUDE', '===', 'Exported', 'Source', '---', '[USER]', '[ASSISTANT]', '[TOOL')):
                preview = line.strip()[:100]
                break

        return {
            'export_date': export_date,
            'source': source,
            'user_count': user_count,
            'assistant_count': assistant_count,
            'tool_count': tool_count,
            'preview': preview
        }
    except Exception as e:
        return None


def search_conversations(query):
    """Search through conversations and return matches"""
    if not CONVERSATIONS_DIR.exists():
        return {
            "items": [{
                "title": "No conversations found",
                "subtitle": f"Directory {CONVERSATIONS_DIR} does not exist",
                "valid": False
            }]
        }

    txt_files = sorted(CONVERSATIONS_DIR.glob("conversation_*.txt"), reverse=True)

    if not txt_files:
        return {
            "items": [{
                "title": "No conversations saved yet",
                "subtitle": "Conversations will appear here after your first Claude Code session ends",
                "valid": False
            }]
        }

    results = []
    query_lower = query.lower() if query else ""

    for txt_file in txt_files[:MAX_RESULTS]:
        try:
            with open(txt_file, 'r') as f:
                content = f.read()

            # If query is provided, check if it matches
            if query_lower:
                if query_lower not in content.lower():
                    continue

                # Find matching lines for context
                matches = []
                for line in content.split('\n'):
                    if query_lower in line.lower():
                        matches.append(line.strip()[:100])
                        if len(matches) >= 3:  # Limit to 3 matches
                            break

                match_text = " | ".join(matches) if matches else ""
            else:
                match_text = ""

            # Get metadata
            metadata = parse_conversation_metadata(txt_file)

            # Format filename for display
            filename = txt_file.stem
            date_match = re.search(r'(\d{8})_(\d{6})', filename)
            if date_match:
                date_str = date_match.group(1)
                time_str = date_match.group(2)
                formatted_date = f"{date_str[:4]}-{date_str[4:6]}-{date_str[6:8]} {time_str[:2]}:{time_str[2:4]}:{time_str[4:6]}"
            else:
                formatted_date = filename

            # Build subtitle
            if query_lower and match_text:
                subtitle = match_text
            elif metadata:
                subtitle = f"💬 {metadata['user_count']} user, {metadata['assistant_count']} assistant"
                if metadata['tool_count'] > 0:
                    subtitle += f", 🔧 {metadata['tool_count']} tools"
                if metadata['preview']:
                    subtitle += f" | {metadata['preview']}"
            else:
                subtitle = str(txt_file)

            # Get file size
            file_size = txt_file.stat().st_size
            size_kb = file_size / 1024

            results.append({
                "title": formatted_date,
                "subtitle": subtitle,
                "arg": str(txt_file),
                "quicklookurl": str(txt_file.with_suffix('.html')),
                "mods": {
                    "cmd": {
                        "subtitle": f"Open HTML version in browser ({size_kb:.1f}KB)",
                        "arg": str(txt_file.with_suffix('.html'))
                    },
                    "alt": {
                        "subtitle": "Reveal in Finder",
                        "arg": str(txt_file.parent)
                    },
                    "ctrl": {
                        "subtitle": f"Copy file path: {txt_file}",
                        "arg": str(txt_file)
                    }
                },
                "icon": {
                    "path": "/System/Library/CoreServices/CoreTypes.bundle/Contents/Resources/DocumentIcon.icns"
                },
                "text": {
                    "copy": str(txt_file),
                    "largetype": f"{formatted_date}\n\n{subtitle}"
                }
            })

        except Exception as e:
            continue

    if not results and query_lower:
        return {
            "items": [{
                "title": f"No conversations found matching '{query}'",
                "subtitle": f"Searched {len(txt_files)} conversations",
                "valid": False
            }]
        }

    return {"items": results}


def main():
    query = sys.argv[1] if len(sys.argv) > 1 else ""
    results = search_conversations(query)
    print(json.dumps(results, indent=2))


if __name__ == "__main__":
    main()
