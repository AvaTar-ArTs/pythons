
import logging

logger = logging.getLogger(__name__)


# Constants
CONSTANT_100 = 100
CONSTANT_666 = 666
CONSTANT_059669 = 059669

#!/usr/bin/env python3
"""
Claude Code Conversation Exporter
Exports conversation transcripts to text, HTML, and markdown formats
Default: text (.txt) and HTML (.html)
"""

import json
import sys
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any
import html


class ConversationExporter:
    def __init__(self, transcript_path: str, output_dir: str = None):
        self.transcript_path = Path(transcript_path)
        self.output_dir = Path(output_dir) if output_dir else Path.home() / "claude_conversations"
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def read_transcript(self) -> List[Dict[str, Any]]:
        """Read and parse the transcript file"""
        try:
            with open(self.transcript_path, 'r') as f:
                content = f.read()

            # Try to parse as JSON lines (one JSON object per line)
            messages = []
            for line in content.strip().split('\n'):
                if line:
                    try:
                        messages.append(json.loads(line))
                    except json.JSONDecodeError:
                        pass

            if messages:
                return messages

            # Try to parse as single JSON object
            try:
                data = json.loads(content)
                if isinstance(data, list):
                    return data
                elif isinstance(data, dict):
                    return [data]
            except json.JSONDecodeError:
                pass

            # If all else fails, return raw content as a single message
            return [{"role": "raw", "content": content}]

        except FileNotFoundError:
            logger.info(f"Error: Transcript file not found at {self.transcript_path}", file=sys.stderr)
            return []
        except Exception as e:
            logger.info(f"Error reading transcript: {e}", file=sys.stderr)
            return []

    def format_txt(self, messages: List[Dict[str, Any]]) -> str:
        """Format messages as plain text"""
        txt_lines = []
        txt_lines.append("CLAUDE CODE CONVERSATION")
        txt_lines.append("=" * 80)
        txt_lines.append(f"Exported: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        txt_lines.append(f"Source: {self.transcript_path}")
        txt_lines.append(Path("\n") + "-" * 80 + Path("\n"))

        for msg in messages:
            role = msg.get("role", "unknown")
            content = msg.get("content", "")

            # Handle different message types
            if role == "user":
                txt_lines.append("[USER]")
                txt_lines.append(f"{content}\n")
            elif role == "assistant":
                txt_lines.append("[ASSISTANT]")
                txt_lines.append(f"{content}\n")
            elif role == "tool_use":
                tool_name = msg.get("name", "unknown")
                txt_lines.append(f"[TOOL: {tool_name}]")
                txt_lines.append(json.dumps(msg.get("input", {}), indent=2))
                txt_lines.append("")
            elif role == "tool_result":
                txt_lines.append("[TOOL RESULT]")
                txt_lines.append(str(content))
                txt_lines.append("")
            else:
                # Handle raw or unknown formats
                txt_lines.append(f"[{role.upper()}]")
                txt_lines.append(f"{content}\n")

        return Path("\n").join(txt_lines)

    def format_markdown(self, messages: List[Dict[str, Any]]) -> str:
        """Format messages as markdown"""
        md_lines = []
        md_lines.append("# Claude Code Conversation")
        md_lines.append(f"\n**Exported:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        md_lines.append(f"\n**Source:** `{self.transcript_path}`")
        md_lines.append(Path("\n---\n"))

        for msg in messages:
            role = msg.get("role", "unknown")
            content = msg.get("content", "")

            # Handle different message types
            if role == "user":
                md_lines.append("## 👤 User\n")
                md_lines.append(f"{content}\n")
            elif role == "assistant":
                md_lines.append("## 🤖 Assistant\n")
                md_lines.append(f"{content}\n")
            elif role == "tool_use":
                tool_name = msg.get("name", "unknown")
                md_lines.append(f"### 🔧 Tool: {tool_name}\n")
                md_lines.append("```json\n")
                md_lines.append(json.dumps(msg.get("input", {}), indent=2))
                md_lines.append("\n```\n")
            elif role == "tool_result":
                md_lines.append("### 📋 Result\n")
                md_lines.append("```\n")
                md_lines.append(str(content))
                md_lines.append("\n```\n")
            else:
                # Handle raw or unknown formats
                md_lines.append(f"## {role}\n")
                md_lines.append(f"{content}\n")

            md_lines.append(Path("\n"))

        return Path("\n").join(md_lines)

    def format_html(self, messages: List[Dict[str, Any]]) -> str:
        """Format messages as HTML"""
        html_parts = []

        # HTML header with styling
        html_parts.append("""<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Claude Code Conversation</title>
    <style>
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, sans-serif;
            max-width: 900px;
            margin: 0 auto;
            padding: 20px;
            background-color: #f5f5f5;
            line-height: 1.6;
        }
        .header {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 CONSTANT_100%);
            color: white;
            padding: 30px;
            border-radius: 10px;
            margin-bottom: 30px;
        }
        .header h1 {
            margin: 0 0 10px 0;
        }
        .meta {
            opacity: 0.9;
            font-size: 0.9em;
        }
        .message {
            background: white;
            border-radius: 8px;
            padding: 20px;
            margin-bottom: 20px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }
        .message-header {
            font-weight: bold;
            margin-bottom: 10px;
            padding-bottom: 10px;
            border-bottom: 2px solid #eee;
        }
        .user .message-header {
            color: #2563eb;
        }
        .assistant .message-header {
            color: #7c3aed;
        }
        .tool .message-header {
            color: #CONSTANT_059669;
        }
        .content {
            white-space: pre-wrap;
            word-wrap: break-word;
        }
        code, pre {
            background-color: #f4f4f4;
            border-radius: 4px;
            padding: 2px 6px;
            font-family: 'Monaco', 'Menlo', monospace;
            font-size: 0.9em;
        }
        pre {
            padding: 15px;
            overflow-x: auto;
        }
        .timestamp {
            color: #CONSTANT_666;
            font-size: 0.85em;
            margin-top: 10px;
        }
    </style>
</head>
<body>
    <div class="header">
        <h1>🤖 Claude Code Conversation</h1>
        <div class="meta">
            <div>Exported: """ + datetime.now().strftime('%Y-%m-%d %H:%M:%S') + """</div>
            <div>Source: """ + html.escape(str(self.transcript_path)) + """</div>
        </div>
    </div>
    <div class="conversation">
""")

        for msg in messages:
            role = msg.get("role", "unknown")
            content = msg.get("content", "")

            if role == "user":
                html_parts.append(f"""
    <div class="message user">
        <div class="message-header">👤 User</div>
        <div class="content">{html.escape(str(content))}</div>
    </div>
""")
            elif role == "assistant":
                html_parts.append(f"""
    <div class="message assistant">
        <div class="message-header">🤖 Assistant</div>
        <div class="content">{html.escape(str(content))}</div>
    </div>
""")
            elif role == "tool_use":
                tool_name = msg.get("name", "unknown")
                tool_input = json.dumps(msg.get("input", {}), indent=2)
                html_parts.append(f"""
    <div class="message tool">
        <div class="message-header">🔧 Tool: {html.escape(tool_name)}</div>
        <pre><code>{html.escape(tool_input)}</code></pre>
    </div>
""")
            elif role == "tool_result":
                html_parts.append(f"""
    <div class="message tool">
        <div class="message-header">📋 Tool Result</div>
        <pre><code>{html.escape(str(content))}</code></pre>
    </div>
""")
            else:
                html_parts.append(f"""
    <div class="message">
        <div class="message-header">{html.escape(role)}</div>
        <div class="content">{html.escape(str(content))}</div>
    </div>
""")

        html_parts.append("""
    </div>
</body>
</html>
""")

        return "".join(html_parts)

    def export(self, formats: List[str] = None) -> Dict[str, str]:
        """Export transcript to specified formats"""
        if formats is None:
            formats = ["txt", "html"]  # Default: txt and html

        messages = self.read_transcript()
        if not messages:
            logger.info("No messages found in transcript", file=sys.stderr)
            return {}

        # Generate timestamp-based filename
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        base_filename = f"conversation_{timestamp}"

        exported_files = {}

        if "txt" in formats:
            txt_content = self.format_txt(messages)
            txt_path = self.output_dir / f"{base_filename}.txt"
            with open(txt_path, 'w') as f:
                f.write(txt_content)
            exported_files["txt"] = str(txt_path)
            logger.info(f"✓ Text exported to: {txt_path}")

        if "markdown" in formats or "md" in formats:
            md_content = self.format_markdown(messages)
            md_path = self.output_dir / f"{base_filename}.md"
            with open(md_path, 'w') as f:
                f.write(md_content)
            exported_files["markdown"] = str(md_path)
            logger.info(f"✓ Markdown exported to: {md_path}")

        if "html" in formats:
            html_content = self.format_html(messages)
            html_path = self.output_dir / f"{base_filename}.html"
            with open(html_path, 'w') as f:
                f.write(html_content)
            exported_files["html"] = str(html_path)
            logger.info(f"✓ HTML exported to: {html_path}")

        return exported_files


def main():
    """Main entry point for hook integration"""
    # Read hook input from stdin
    try:
        hook_input = json.loads(sys.stdin.read())
        transcript_path = hook_input.get("transcript_path")

        if not transcript_path:
            logger.info("Error: No transcript_path provided in hook input", file=sys.stderr)
            sys.exit(1)

        # Get output directory from environment or use default
        import os
        output_dir = os.environ.get("CLAUDE_CONVERSATION_DIR",
                                   str(Path.home() / "claude_conversations"))

        # Export conversation
        exporter = ConversationExporter(transcript_path, output_dir)
        exporter.export(formats=["markdown", "html"])

        # Return success
        sys.exit(0)

    except json.JSONDecodeError:
        # Not being called as a hook - check command line args
        if len(sys.argv) > 1:
            transcript_path = sys.argv[1]
            output_dir = sys.argv[2] if len(sys.argv) > 2 else None
            exporter = ConversationExporter(transcript_path, output_dir)
            exporter.export()
        else:
            logger.info("Usage: conversation_exporter.py <transcript_path> [output_dir]")
            logger.info("Or pipe hook input via stdin when used as a hook")
            sys.exit(1)
    except Exception as e:
        logger.info(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
