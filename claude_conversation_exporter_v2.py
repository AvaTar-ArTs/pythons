#!/usr/bin/env python3
"""
Claude Code Conversation Exporter
Extracts and exports Claude Code conversations from .claude/ directory
Supports Markdown, HTML, and CSV output formats
"""

import json
import os
from pathlib import Path
from datetime import datetime
from collections import defaultdict
import csv
from typing import Dict, List, Any, Optional
import argparse
from dataclasses import dataclass
import re


@dataclass
class Conversation:
    """Represents a single conversation message"""
    timestamp: float
    model: str
    user_input: str
    assistant_response: str
    tokens: Optional[int] = None
    session_id: Optional[str] = None


def safe_timestamp(ts: Any) -> int:
    """Convert timestamp to integer, handling string values safely"""
    if isinstance(ts, str):
        try:
            return int(float(ts))
        except (ValueError, TypeError):
            return int(datetime.now().timestamp() * 1000)
    elif isinstance(ts, (int, float)):
        return int(ts)
    return int(datetime.now().timestamp() * 1000)


class ConversationExporter:
    """Exports Claude Code conversations to multiple formats"""

    def __init__(self, claude_dir: Path = None, output_dir: Path = None):
        """Initialize exporter with paths"""
        self.claude_dir = claude_dir or Path.home() / '.claude'
        self.output_dir = output_dir or Path.home() / 'AVATARARTS' / '05_DATA' / 'claude_conversations_export'
        self.conversations: List[Dict[str, Any]] = []
        self.sessions: Dict[str, List[Dict[str, Any]]] = defaultdict(list)
        self.statistics = {
            'total_messages': 0,
            'total_sessions': 0,
            'models': defaultdict(int),
            'date_range': {'start': None, 'end': None}
        }

    def find_jsonl_files(self) -> List[Path]:
        """Recursively find all JSONL files in .claude directory"""
        jsonl_files = []

        # Search in specific locations
        search_paths = [
            self.claude_dir / 'projects',
            self.claude_dir / 'history.jsonl',
        ]

        for search_path in search_paths:
            if search_path.is_file():
                jsonl_files.append(search_path)
            elif search_path.is_dir():
                jsonl_files.extend(search_path.glob('**/*.jsonl'))

        return jsonl_files

    def parse_jsonl_file(self, filepath: Path) -> List[Dict[str, Any]]:
        """Parse a single JSONL file, extracting conversation data"""
        conversations = []

        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                for line in f:
                    if not line.strip():
                        continue
                    try:
                        data = json.loads(line)
                        conversations.append(data)
                    except json.JSONDecodeError:
                        continue
        except (IOError, UnicodeDecodeError):
            pass

        return conversations

    def load_conversations(self):
        """Load all conversations from .claude directory"""
        jsonl_files = self.find_jsonl_files()
        print(f"Found {len(jsonl_files)} JSONL files")

        all_conversations = []

        for filepath in jsonl_files:
            print(f"  Processing: {filepath.relative_to(Path.home())}")
            conversations = self.parse_jsonl_file(filepath)
            all_conversations.extend(conversations)

        # Process and organize conversations
        for conv in all_conversations:
            self._process_conversation(conv)

        self.statistics['total_messages'] = len(self.conversations)
        self.statistics['total_sessions'] = len(self.sessions)

        print(f"\nLoaded {self.statistics['total_messages']} messages from {self.statistics['total_sessions']} sessions")
        return len(self.conversations) > 0

    def _process_conversation(self, conv: Dict[str, Any]):
        """Process a single conversation entry"""
        # Extract session ID if available
        session_id = conv.get('session_id') or conv.get('id', 'unknown')

        # Create processed record
        processed = {
            'session_id': session_id,
            'timestamp': safe_timestamp(conv.get('timestamp')),
            'model': conv.get('model', 'unknown'),
            'type': conv.get('type', 'message'),
            'content': conv,
        }

        # Track model usage
        if processed['model'] != 'unknown':
            self.statistics['models'][processed['model']] += 1

        # Organize by session
        self.sessions[session_id].append(processed)
        self.conversations.append(processed)

    def export_markdown(self, output_dir: Path = None):
        """Export conversations to Markdown format"""
        output_dir = output_dir or self.output_dir
        output_dir.mkdir(parents=True, exist_ok=True)

        md_file = output_dir / 'conversations.md'

        with open(md_file, 'w', encoding='utf-8') as f:
            f.write("# Claude Code Conversations Export\n\n")
            f.write(f"**Export Date**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"**Total Messages**: {self.statistics['total_messages']}\n")
            f.write(f"**Total Sessions**: {self.statistics['total_sessions']}\n\n")

            # Write model statistics
            f.write("## Model Usage\n\n")
            for model, count in sorted(self.statistics['models'].items(), key=lambda x: x[1], reverse=True):
                f.write(f"- **{model}**: {count} messages\n")
            f.write("\n---\n\n")

            # Write sessions
            for session_id, messages in sorted(self.sessions.items()):
                if not messages:
                    continue

                # Safe timestamp extraction for session header
                first_msg = messages[0]
                start_time = safe_timestamp(first_msg.get('timestamp'))

                try:
                    dt = datetime.fromtimestamp(start_time / 1000)
                    date_str = dt.strftime('%Y-%m-%d %H:%M:%S')
                except (ValueError, OSError, OverflowError):
                    date_str = "Unknown date"

                f.write(f"## Session: {session_id}\n")
                f.write(f"**Date**: {date_str}\n")
                f.write(f"**Messages**: {len(messages)}\n")
                f.write(f"**Primary Model**: {first_msg.get('model', 'unknown')}\n\n")

                for msg in messages:
                    content = msg.get('content', {})
                    f.write(f"### Message\n")

                    if isinstance(content, dict):
                        if 'user' in content:
                            f.write(f"**User**: {content['user']}\n\n")
                        if 'assistant' in content:
                            f.write(f"**Assistant**: {content['assistant']}\n\n")
                    else:
                        f.write(f"{content}\n\n")

                    f.write("---\n\n")

        print(f"✓ Markdown export: {md_file}")
        return md_file

    def export_html(self, output_dir: Path = None):
        """Export conversations to HTML format"""
        output_dir = output_dir or self.output_dir
        output_dir.mkdir(parents=True, exist_ok=True)

        html_file = output_dir / 'conversations.html'

        with open(html_file, 'w', encoding='utf-8') as f:
            f.write("""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Claude Code Conversations</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
               background: #1e1e1e; color: #e0e0e0; padding: 20px; }
        .container { max-width: 1200px; margin: 0 auto; }
        header { border-bottom: 2px solid #444; margin-bottom: 30px; padding-bottom: 20px; }
        h1 { color: #61dafb; margin-bottom: 10px; }
        .stats { display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
                 gap: 15px; margin-bottom: 20px; }
        .stat-box { background: #2d2d2d; padding: 15px; border-left: 3px solid #61dafb; }
        .stat-box strong { color: #61dafb; }
        .sessions { display: grid; gap: 30px; }
        .session { background: #2d2d2d; border-left: 4px solid #61dafb; padding: 20px; }
        .session-header { margin-bottom: 15px; }
        .session-header h2 { color: #61dafb; margin-bottom: 5px; }
        .message { margin: 15px 0; padding: 15px; background: #1a1a1a; border-radius: 5px; }
        .user { border-left: 3px solid #4caf50; }
        .assistant { border-left: 3px solid #ff9800; }
        .user-label { color: #4caf50; font-weight: bold; }
        .assistant-label { color: #ff9800; font-weight: bold; }
        code { background: #1a1a1a; padding: 2px 6px; border-radius: 3px;
               font-family: 'Courier New', monospace; }
        pre { background: #1a1a1a; padding: 10px; border-radius: 5px;
              overflow-x: auto; margin: 10px 0; }
    </style>
</head>
<body>
    <div class="container">
        <header>
            <h1>Claude Code Conversations Export</h1>
            <p>Exported: {export_date}</p>
        </header>

        <div class="stats">
            <div class="stat-box">
                <strong>Total Messages:</strong> {total_messages}
            </div>
            <div class="stat-box">
                <strong>Total Sessions:</strong> {total_sessions}
            </div>
            <div class="stat-box">
                <strong>Models Used:</strong> {model_count}
            </div>
        </div>

        <h2>Sessions</h2>
        <div class="sessions">
""")

            for session_id, messages in sorted(self.sessions.items()):
                if not messages:
                    continue

                first_msg = messages[0]
                start_time = safe_timestamp(first_msg.get('timestamp'))

                try:
                    dt = datetime.fromtimestamp(start_time / 1000)
                    date_str = dt.strftime('%Y-%m-%d %H:%M:%S')
                except (ValueError, OSError, OverflowError):
                    date_str = "Unknown date"

                f.write(f"""            <div class="session">
                <div class="session-header">
                    <h2>{session_id}</h2>
                    <p><strong>Date:</strong> {date_str}</p>
                    <p><strong>Messages:</strong> {len(messages)}</p>
                    <p><strong>Model:</strong> {first_msg.get('model', 'unknown')}</p>
                </div>
""")

                for msg in messages:
                    content = msg.get('content', {})

                    if isinstance(content, dict):
                        if 'user' in content:
                            user_text = str(content['user'])[:500]
                            f.write(f'<div class="message user"><span class="user-label">User:</span> {user_text}</div>\n')

                        if 'assistant' in content:
                            asst_text = str(content['assistant'])[:500]
                            f.write(f'<div class="message assistant"><span class="assistant-label">Assistant:</span> {asst_text}</div>\n')

                f.write("            </div>\n")

            f.write("""        </div>
    </div>
</body>
</html>
""".format(
                export_date=datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                total_messages=self.statistics['total_messages'],
                total_sessions=self.statistics['total_sessions'],
                model_count=len(self.statistics['models'])
            ))

        print(f"✓ HTML export: {html_file}")
        return html_file

    def export_csv(self, output_dir: Path = None):
        """Export conversations to CSV format"""
        output_dir = output_dir or self.output_dir
        output_dir.mkdir(parents=True, exist_ok=True)

        csv_file = output_dir / 'conversations.csv'

        with open(csv_file, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['Session ID', 'Timestamp', 'Date', 'Model', 'Message Type', 'Content Preview'])

            for conv in sorted(self.conversations, key=lambda x: x['timestamp']):
                session_id = conv.get('session_id', 'unknown')
                timestamp = conv.get('timestamp', 0)
                model = conv.get('model', 'unknown')
                msg_type = conv.get('type', 'message')

                # Safe timestamp conversion for CSV
                try:
                    ts_int = safe_timestamp(timestamp)
                    dt = datetime.fromtimestamp(ts_int / 1000)
                    date_str = dt.strftime('%Y-%m-%d %H:%M:%S')
                except (ValueError, OSError, OverflowError):
                    date_str = "Unknown"

                content = conv.get('content', {})
                if isinstance(content, dict):
                    preview = str(content).replace('\n', ' ')[:100]
                else:
                    preview = str(content)[:100]

                writer.writerow([session_id, timestamp, date_str, model, msg_type, preview])

        print(f"✓ CSV export: {csv_file}")
        return csv_file

    def export_json(self, output_dir: Path = None):
        """Export conversations to JSON format"""
        output_dir = output_dir or self.output_dir
        output_dir.mkdir(parents=True, exist_ok=True)

        json_file = output_dir / 'conversations.json'

        export_data = {
            'export_date': datetime.now().isoformat(),
            'statistics': {
                'total_messages': self.statistics['total_messages'],
                'total_sessions': self.statistics['total_sessions'],
                'models': dict(self.statistics['models']),
            },
            'conversations': self.conversations,
        }

        with open(json_file, 'w', encoding='utf-8') as f:
            json.dump(export_data, f, indent=2, default=str)

        print(f"✓ JSON export: {json_file}")
        return json_file

    def export_all(self):
        """Export to all supported formats"""
        print("\n" + "="*60)
        print("EXPORTING CONVERSATIONS TO ALL FORMATS")
        print("="*60 + "\n")

        self.export_markdown()
        self.export_html()
        self.export_csv()
        self.export_json()

        print("\n" + "="*60)
        print(f"Export complete! Files saved to: {self.output_dir}")
        print("="*60)


def main():
    parser = argparse.ArgumentParser(
        description='Export Claude Code conversations to multiple formats'
    )
    parser.add_argument(
        '--output',
        type=Path,
        help='Output directory for exports'
    )
    parser.add_argument(
        '--claude-dir',
        type=Path,
        help='Claude directory path (default: ~/.claude)'
    )
    parser.add_argument(
        '--format',
        choices=['all', 'markdown', 'html', 'csv', 'json'],
        default='all',
        help='Export format(s) to generate'
    )

    args = parser.parse_args()

    # Create exporter
    exporter = ConversationExporter(
        claude_dir=args.claude_dir,
        output_dir=args.output
    )

    # Load conversations
    print("Loading conversations...")
    if not exporter.load_conversations():
        print("No conversations found!")
        return 1

    # Export
    if args.format == 'all':
        exporter.export_all()
    elif args.format == 'markdown':
        exporter.export_markdown()
    elif args.format == 'html':
        exporter.export_html()
    elif args.format == 'csv':
        exporter.export_csv()
    elif args.format == 'json':
        exporter.export_json()

    return 0


if __name__ == '__main__':
    exit(main())
