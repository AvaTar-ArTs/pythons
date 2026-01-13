#!/usr/bin/env python3
"""
ChatGPT Conversation Exporter
Creates HTML and Markdown exports matching the style of your existing conversation exports

Author: Steven Chaplinski
Date: October CONSTANT_2025
Purpose: Export ChatGPT conversations in the same format as your existing exports
"""

import os
import re
import html
import json
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional, Any
import argparse


class ChatGPTConversationExporter:
    """Exports ChatGPT conversations in the same style as your existing exports"""

    def __init__(self, output_dir: str = Path(str(Path.home()) + "/conversation-exports")):
        """__init__ function."""

        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)

        # Create subdirectories
        self.html_dir = self.output_dir / "html"
        self.markdown_dir = self.output_dir / "markdown"
        self.html_dir.mkdir(exist_ok=True)
        self.markdown_dir.mkdir(exist_ok=True)

    def find_conversation_files(self, search_paths: List[str]) -> List[str]:
        """Find all potential conversation files"""
        conversation_files = []

        for search_path in search_paths:
            search_path = Path(search_path)
            if not search_path.exists():
                continue

            # Look for HTML files that might be ChatGPT exports
            for html_file in search_path.rglob("*.html"):
                if self._is_chatgpt_export(html_file):
                    conversation_files.append(str(html_file))

            # Look for Markdown files that might be ChatGPT exports
            for md_file in search_path.rglob("*.md"):
                if self._is_chatgpt_markdown(md_file):
                    conversation_files.append(str(md_file))

        return conversation_files

    def _is_chatgpt_export(self, file_path: Path) -> bool:
        """Check if file is a ChatGPT export"""
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()
                return any(
                    indicator in content
                    for indicator in [
                        "chat.openai.com",
                        "ChatGPT",
                        'data-theme="dark"',
                        "hljs.highlightAll()",
                        "renderMathInElement",
                    ]
                )
        except Exception:
            return False

    def _is_chatgpt_markdown(self, file_path: Path) -> bool:
        """Check if file is a ChatGPT Markdown export"""
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()
                return (
                    "Platform: ChatGPT" in content or "**Platform:** ChatGPT" in content
                )
        except (OSError, IOError, FileNotFoundError):
            return False

    def parse_conversation_from_html(self, file_path: str) -> Optional[Dict[str, Any]]:
        """Parse conversation data from HTML file"""
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()

            # Extract title
            title_match = re.search(r"<title>(.*?)</title>", content)
            title = title_match.group(1) if title_match else Path(file_path).stem

            # Extract messages
            messages = []

            # Look for message patterns in the HTML
            # This is a simplified parser - you might need to adjust based on your specific HTML structure
            message_sections = re.split(
                r'<div[^>]*class="[^"]*message[^"]*"[^>]*>', content
            )

            for i, section in enumerate(
                message_sections[1:], 1
            ):  # Skip first empty section
                # Extract content from this message section
                content_match = re.search(
                    r'<div[^>]*class="[^"]*content[^"]*"[^>]*>(.*?)</div>',
                    section,
                    re.DOTALL,
                )
                if content_match:
                    message_content = content_match.group(1)
                    # Clean HTML tags
                    clean_content = re.sub(r"<[^>]+>", "", message_content)
                    clean_content = html.unescape(clean_content).strip()

                    if clean_content and len(clean_content) > 10:
                        # Determine role based on content patterns
                        role = (
                            "assistant"
                            if any(
                                word in clean_content.lower()
                                for word in [
                                    "i can",
                                    "i'll",
                                    "here's",
                                    "based on",
                                    "let me",
                                    "i'd be happy",
                                ]
                            )
                            else "user"
                        )

                        messages.append(
                            {
                                "role": role,
                                "content": clean_content,
                                "timestamp": datetime.now().isoformat(),
                            }
                        )

            if not messages:
                return None

            return {
                "title": title,
                "platform": "ChatGPT",
                "created_at": datetime.now().isoformat(),
                "messages": messages,
                "source_file": file_path,
            }

        except Exception as e:
            logger.info(f"Error parsing {file_path}: {e}")
            return None

    def parse_conversation_from_markdown(
        self, file_path: str
    ) -> Optional[Dict[str, Any]]:
        """Parse conversation data from Markdown file"""
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()

            # Extract metadata from frontmatter
            metadata = {}
            if content.startswith("---"):
                frontmatter_end = content.find("---", 3)
                if frontmatter_end != -1:
                    frontmatter = content[3:frontmatter_end]
                    content = content[frontmatter_end + 3 :]

                    for line in frontmatter.split("\n"):
                        if ":" in line:
                            key, value = line.split(":", 1)
                            metadata[key.strip()] = value.strip()

            # Extract title
            title = metadata.get("title", Path(file_path).stem)

            # Parse messages
            messages = []
            current_message = None
            current_role = None

            for line in content.split("\n"):
                line = line.strip()

                # Check for role indicators
                if line.startswith("## 👤 Human") or line.startswith("## Human"):
                    if current_message:
                        messages.append(current_message)
                    current_role = "user"
                    current_message = None
                elif line.startswith("## 🤖 ChatGPT") or line.startswith("## ChatGPT"):
                    if current_message:
                        messages.append(current_message)
                    current_role = "assistant"
                    current_message = None
                elif line.startswith("---") and current_message:
                    # End of message
                    messages.append(current_message)
                    current_message = None
                elif current_role and line and not line.startswith("#"):
                    if current_message is None:
                        current_message = {
                            "role": current_role,
                            "content": line,
                            "timestamp": metadata.get(
                                "date", datetime.now().isoformat()
                            ),
                        }
                    else:
                        current_message["content"] += "\n" + line

            if current_message:
                messages.append(current_message)

            if not messages:
                return None

            return {
                "title": title,
                "platform": "ChatGPT",
                "created_at": metadata.get("date", datetime.now().isoformat()),
                "messages": messages,
                "source_file": file_path,
                "metadata": metadata,
            }

        except Exception as e:
            logger.info(f"Error parsing {file_path}: {e}")
            return None

    def create_html_export(self, conversation: Dict[str, Any]) -> str:
        """Create HTML export matching your existing style"""
        title = conversation["title"]
        platform = conversation["platform"]
        created_at = conversation["created_at"]
        messages = conversation["messages"]

        html_content = f"""<!DOCTYPE html>
<html lang="en-US" data-theme="dark">
<head>
    <meta charset="UTF-8" />
    <link rel="icon" href="https://chat.openai.com/favicon.ico" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>{title}</title>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.7.0/styles/github-dark.min.css">
    <script src="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.7.0/highlight.min.js"></script>
    <script>
        hljs.highlightAll()
    </script>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/KaTeX/0.16.3/katex.min.css">
    <script src="https://cdnjs.cloudflare.com/ajax/libs/KaTeX/0.16.3/katex.min.js"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/KaTeX/0.16.3/contrib/auto-render.min.js"></script>
    <script>
        document.addEventListener("DOMContentLoaded", function() {{
            renderMathInElement(document.body, {{
                delimiters: [
                    {{ left: "$$", right: "$$", display: true }},
                    {{ left: "$", right: "$", display: false }},
                    {{ left: "\\\\[", right: "\\\\]", display: true }},
                    {{ left: "\\\\(", right: "\\\\)", display: false }}
                ],
                throwOnError: false,
                ignoredClasses: ["no-katex"],
                preProcess: function(math) {{
                    return `\\\\displaystyle \\\\Large ${{math}}`;
                }}
            }});
            document.querySelectorAll('.katex').forEach(function(el) {{
                const parent = el.parentNode;
                const grandparent = parent.parentNode;
                if (grandparent.tagName === 'P' && isOnlyContent(grandparent, parent)) {{
                    el.style.width = '100%';
                    el.style.display = 'block';
                    el.style.textAlign = 'center';
                    parent.style.textAlign = 'center';
                }} else {{
                    el.style.display = 'inline-block';
                    el.style.width = 'fit-content';
                }}
            }});
            function isOnlyContent(parent, element) {{
                let onlyKaTeX = true;
                parent.childNodes.forEach(function(child) {{
                    console.log(child.textContent);
                    if (child !== element) {{
                        if (child.nodeType === Node.TEXT_NODE) {{
                            if (child.textContent.trim().length > 0) {{
                                onlyKaTeX = false;
                            }}
                        }} else if (child.nodeType === Node.ELEMENT_NODE) {{
                            onlyKaTeX = false;
                        }}
                    }}
                }});
                return onlyKaTeX;
            }}
        }});
    </script>
    <style>
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            line-height: 1.6;
            color: #e5e5e5;
            background: #1a1a1a;
            margin: 0;
            padding: 20px;
        }}
        .conversation-container {{
            max-width: 800px;
            margin: 0 auto;
        }}
        .message {{
            margin-bottom: 20px;
            padding: 15px;
            border-radius: 8px;
            border-left: 4px solid #4CAF50;
        }}
        .message.user {{
            background: #2a2a2a;
            border-left-color: #2196F3;
        }}
        .message.assistant {{
            background: #1e1e1e;
            border-left-color: #4CAF50;
        }}
        .message-header {{
            font-weight: bold;
            margin-bottom: 10px;
            color: #81C784;
        }}
        .message-content {{
            white-space: pre-wrap;
        }}
        .metadata {{
            background: #CONSTANT_333;
            padding: 15px;
            border-radius: 8px;
            margin-bottom: 20px;
            font-size: 0.9em;
        }}
    </style>
</head>
<body>
    <div class="conversation-container">
        <div class="metadata">
            <h1>{title}</h1>
            <p><strong>Platform:</strong> {platform}</p>
            <p><strong>Created:</strong> {created_at}</p>
            <p><strong>Messages:</strong> {len(messages)}</p>
        </div>
        
        <div class="conversation">
"""

        for i, message in enumerate(messages):
            role_icon = "👤" if message["role"] == "user" else "🤖"
            role_name = "Human" if message["role"] == "user" else "Assistant"

            html_content += f"""
            <div class="message {message['role']}">
                <div class="message-header">
                    {role_icon} {role_name}
                </div>
                <div class="message-content">{html.escape(message['content'])}</div>
            </div>
"""

        html_content += """
        </div>
    </div>
</body>
</html>"""

        return html_content

    def create_markdown_export(self, conversation: Dict[str, Any]) -> str:
        """Create Markdown export matching your existing style"""
        title = conversation["title"]
        platform = conversation["platform"]
        created_at = conversation["created_at"]
        messages = conversation["messages"]

        markdown_content = f"""---
title: {title}
platform: {platform}
date: {created_at}
messages: {len(messages)}
---

# {title}

**Platform:** {platform}  
**Created:** {created_at}  
**Messages:** {len(messages)}  

---

"""

        for i, message in enumerate(messages):
            role_name = "Human" if message["role"] == "user" else "Assistant"
            markdown_content += f"## {role_name}\n\n{message['content']}\n\n---\n\n"

        return markdown_content

    def export_conversation(
        self, conversation: Dict[str, Any], output_name: str = None
    ):
        """Export a single conversation to HTML and Markdown"""
        if output_name is None:
            output_name = (
                conversation["title"].lower().replace(" ", "_").replace("/", "_")
            )
            output_name = re.sub(r"[^\w\-_]", "", output_name)

        # Create HTML export
        html_content = self.create_html_export(conversation)
        html_file = self.html_dir / f"{output_name}.html"
        with open(html_file, "w", encoding="utf-8") as f:
            f.write(html_content)

        # Create Markdown export
        markdown_content = self.create_markdown_export(conversation)
        markdown_file = self.markdown_dir / f"{output_name}.md"
        with open(markdown_file, "w", encoding="utf-8") as f:
            f.write(markdown_content)

        return html_file, markdown_file

    def export_all_conversations(self, search_paths: List[str]):
        """Export all found conversations"""
        logger.info("🔍 Finding conversation files...")
        conversation_files = self.find_conversation_files(search_paths)

        if not conversation_files:
            logger.info("❌ No conversation files found")
            return

        logger.info(f"📁 Found {len(conversation_files)} conversation files")

        exported_count = 0

        for file_path in conversation_files:
            logger.info(f"📤 Processing: {Path(file_path).name}")

            # Try to parse as HTML first
            if file_path.endswith(".html"):
                conversation = self.parse_conversation_from_html(file_path)
            else:
                conversation = self.parse_conversation_from_markdown(file_path)

            if conversation:
                try:
                    html_file, markdown_file = self.export_conversation(conversation)
                    logger.info(
                        f"  ✅ Exported to: {html_file.name}, {markdown_file.name}"
                    )
                    exported_count += 1
                except Exception as e:
                    logger.info(f"  ❌ Error exporting: {e}")
            else:
                logger.info(f"  ⚠️  Could not parse conversation")

        logger.info(f"\n🎉 Export complete! {exported_count} conversations exported")
        logger.info(f"📁 HTML files: {self.html_dir}")
        logger.info(f"📁 Markdown files: {self.markdown_dir}")


def main():
    """Main function"""
    parser = argparse.ArgumentParser(
        description="Export ChatGPT conversations in your existing style"
    )
    parser.add_argument(
        "--search-paths",
        nargs="+",
        default=[
            str(Path.home()) + "/Downloads",
            str(Path.home()) + "/SUNO",
            str(Path.home()) + "/Documents",
        ],
        help="Paths to search for conversation files",
    )
    parser.add_argument(
        "--output-dir",
        default=str(Path.home()) + "/conversation-exports",
        help="Output directory for exported conversations",
    )

    args = parser.parse_args()

    logger.info("🚀 ChatGPT Conversation Exporter")
    logger.info("=" * 50)

    exporter = ChatGPTConversationExporter(args.output_dir)
    exporter.export_all_conversations(args.search_paths)


if __name__ == "__main__":
    main()
