#!/usr/bin/env python3
"""
Universal Conversation Exporter
Comprehensive tool for exporting conversations from multiple platforms in your existing style

Author: Steven Chaplinski
Date: October CONSTANT_2025
Purpose: Export conversations from ChatGPT, Claude, Perplexity, and other platforms
"""

import os
import re
import html
import json
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional, Any
import argparse
from collections import defaultdict, Counter


class UniversalConversationExporter:
    """Universal exporter for conversations from multiple platforms"""

    def __init__(self, output_dir: str = Path(str(Path.home()) + "/conversation-exports")):
        """__init__ function."""

        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)

        # Create subdirectories
        self.html_dir = self.output_dir / "html"
        self.markdown_dir = self.output_dir / "markdown"
        self.json_dir = self.output_dir / "json"
        self.analysis_dir = self.output_dir / "analysis"

        for dir_path in [
            self.html_dir,
            self.markdown_dir,
            self.json_dir,
            self.analysis_dir,
        ]:
            dir_path.mkdir(exist_ok=True)

        self.conversations = []
        self.export_stats = defaultdict(int)

    def scan_for_conversations(self, search_paths: List[str]) -> Dict[str, List[str]]:
        """Scan multiple paths for conversation files"""
        sources = {
            "chatgpt_html": [],
            "chatgpt_markdown": [],
            "claude_html": [],
            "claude_markdown": [],
            "perplexity_html": [],
            "perplexity_markdown": [],
            "generic_html": [],
            "generic_markdown": [],
            "json_exports": [],
        }

        logger.info("🔍 Scanning for conversation sources...")

        for search_path in search_paths:
            search_path = Path(search_path)
            if not search_path.exists():
                logger.info(f"⚠️  Path not found: {search_path}")
                continue

            logger.info(f"📁 Scanning: {search_path}")

            # Scan for HTML files
            for html_file in search_path.rglob("*.html"):
                if self._is_conversation_file(html_file):
                    platform = self._detect_platform(html_file)
                    if platform == "ChatGPT":
                        sources["chatgpt_html"].append(str(html_file))
                    elif platform == "Claude":
                        sources["claude_html"].append(str(html_file))
                    elif platform == "Perplexity":
                        sources["perplexity_html"].append(str(html_file))
                    else:
                        sources["generic_html"].append(str(html_file))

            # Scan for Markdown files
            for md_file in search_path.rglob("*.md"):
                if self._is_conversation_markdown(md_file):
                    platform = self._detect_markdown_platform(md_file)
                    if platform == "ChatGPT":
                        sources["chatgpt_markdown"].append(str(md_file))
                    elif platform == "Claude":
                        sources["claude_markdown"].append(str(md_file))
                    elif platform == "Perplexity":
                        sources["perplexity_markdown"].append(str(md_file))
                    else:
                        sources["generic_markdown"].append(str(md_file))

            # Scan for JSON exports
            for json_file in search_path.rglob("*.json"):
                if self._is_conversation_json(json_file):
                    sources["json_exports"].append(str(json_file))

        # Print summary
        total_files = sum(len(files) for files in sources.values())
        logger.info(f"📊 Found {total_files} conversation files:")
        for source_type, files in sources.items():
            if files:
                logger.info(f"  {source_type}: {len(files)} files")

        return sources

    def _is_conversation_file(self, file_path: Path) -> bool:
        """Check if file is a conversation export"""
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()
                return any(
                    indicator in content
                    for indicator in [
                        "chat.openai.com",
                        "ChatGPT",
                        "claude.ai",
                        "Claude",
                        "perplexity.ai",
                        "Perplexity",
                        "conversation",
                        "message",
                        'data-theme="dark"',
                        "hljs.highlightAll()",
                    ]
                )
        except (IndexError, KeyError):
            return False

    def _is_conversation_markdown(self, file_path: Path) -> bool:
        """Check if Markdown file is a conversation export"""
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()
                return any(
                    indicator in content
                    for indicator in [
                        "Platform: ChatGPT",
                        "**Platform:** ChatGPT",
                        "Platform: Claude",
                        "**Platform:** Claude",
                        "Platform: Perplexity",
                        "**Platform:** Perplexity",
                        "## Human",
                        "## Assistant",
                        "## 👤 Human",
                        "## 🤖",
                    ]
                )
        except Exception:
            return False

    def _is_conversation_json(self, file_path: Path) -> bool:
        """Check if JSON file contains conversation data"""
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                data = json.load(f)
                return isinstance(data, (list, dict)) and any(
                    key in str(data).lower()
                    for key in ["conversation", "messages", "chat", "dialogue"]
                )
        except (OSError, IOError, FileNotFoundError):
            return False

    def _detect_platform(self, file_path: Path) -> str:
        """Detect platform from HTML file"""
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()

                if "chat.openai.com" in content or "ChatGPT" in content:
                    return "ChatGPT"
                elif "claude.ai" in content or "Claude" in content:
                    return "Claude"
                elif "perplexity.ai" in content or "Perplexity" in content:
                    return "Perplexity"
                else:
                    return "Generic"
        except Exception:
            return "Generic"

    def _detect_markdown_platform(self, file_path: Path) -> str:
        """Detect platform from Markdown file"""
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()

                if "Platform: ChatGPT" in content or "**Platform:** ChatGPT" in content:
                    return "ChatGPT"
                elif "Platform: Claude" in content or "**Platform:** Claude" in content:
                    return "Claude"
                elif (
                    "Platform: Perplexity" in content
                    or "**Platform:** Perplexity" in content
                ):
                    return "Perplexity"
                else:
                    return "Generic"
        except Exception:
            return "Generic"

    def parse_conversation(
        self, file_path: str, platform: str
    ) -> Optional[Dict[str, Any]]:
        """Parse conversation from file based on platform"""
        file_path = Path(file_path)

        if platform == "ChatGPT":
            if file_path.suffix == ".html":
                return self._parse_chatgpt_html(file_path)
            else:
                return self._parse_chatgpt_markdown(file_path)
        elif platform == "Claude":
            if file_path.suffix == ".html":
                return self._parse_claude_html(file_path)
            else:
                return self._parse_claude_markdown(file_path)
        elif platform == "Perplexity":
            if file_path.suffix == ".html":
                return self._parse_perplexity_html(file_path)
            else:
                return self._parse_perplexity_markdown(file_path)
        else:
            # Generic parsing
            if file_path.suffix == ".html":
                return self._parse_generic_html(file_path)
            else:
                return self._parse_generic_markdown(file_path)

    def _parse_chatgpt_html(self, file_path: Path) -> Optional[Dict[str, Any]]:
        """Parse ChatGPT HTML export"""
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()

            # Extract title
            title_match = re.search(r"<title>(.*?)</title>", content)
            title = title_match.group(1) if title_match else file_path.stem

            # Extract messages
            messages = []

            # Look for message patterns
            message_patterns = [
                r'<div[^>]*class="[^"]*message[^"]*"[^>]*>(.*?)</div>',
                r'<div[^>]*class="[^"]*conversation[^"]*"[^>]*>(.*?)</div>',
                r'<p[^>]*class="[^"]*user[^"]*"[^>]*>(.*?)</p>',
                r'<p[^>]*class="[^"]*assistant[^"]*"[^>]*>(.*?)</p>',
            ]

            for pattern in message_patterns:
                matches = re.findall(pattern, content, re.DOTALL)
                for i, match in enumerate(matches):
                    clean_content = re.sub(r"<[^>]+>", "", match)
                    clean_content = html.unescape(clean_content).strip()

                    if clean_content and len(clean_content) > 10:
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
                "source_file": str(file_path),
                "format": "html",
            }

        except Exception as e:
            logger.info(f"Error parsing ChatGPT HTML {file_path}: {e}")
            return None

    def _parse_chatgpt_markdown(self, file_path: Path) -> Optional[Dict[str, Any]]:
        """Parse ChatGPT Markdown export"""
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()

            # Extract metadata
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

            title = metadata.get("title", file_path.stem)

            # Parse messages
            messages = []
            current_message = None
            current_role = None

            for line in content.split("\n"):
                line = line.strip()

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
                "source_file": str(file_path),
                "format": "markdown",
                "metadata": metadata,
            }

        except Exception as e:
            logger.info(f"Error parsing ChatGPT Markdown {file_path}: {e}")
            return None

    def _parse_claude_html(self, file_path: Path) -> Optional[Dict[str, Any]]:
        """Parse Claude HTML export"""
        # Similar to ChatGPT but with Claude-specific patterns
        return self._parse_generic_html(file_path, "Claude")

    def _parse_claude_markdown(self, file_path: Path) -> Optional[Dict[str, Any]]:
        """Parse Claude Markdown export"""
        # Similar to ChatGPT but with Claude-specific patterns
        return self._parse_generic_markdown(file_path, "Claude")

    def _parse_perplexity_html(self, file_path: Path) -> Optional[Dict[str, Any]]:
        """Parse Perplexity HTML export"""
        return self._parse_generic_html(file_path, "Perplexity")

    def _parse_perplexity_markdown(self, file_path: Path) -> Optional[Dict[str, Any]]:
        """Parse Perplexity Markdown export"""
        return self._parse_generic_markdown(file_path, "Perplexity")

    def _parse_generic_html(
        self, file_path: Path, platform: str = "Generic"
    ) -> Optional[Dict[str, Any]]:
        """Parse generic HTML file as conversation"""
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()

            title_match = re.search(r"<title>(.*?)</title>", content)
            title = title_match.group(1) if title_match else file_path.stem

            messages = []
            text_content = re.sub(r"<[^>]+>", " ", content)
            text_content = html.unescape(text_content)

            paragraphs = [
                p.strip()
                for p in text_content.split("\n")
                if p.strip() and len(p.strip()) > 20
            ]

            for i, para in enumerate(paragraphs[:10]):
                role = "assistant" if i % 2 == 1 else "user"
                messages.append(
                    {
                        "role": role,
                        "content": para,
                        "timestamp": datetime.now().isoformat(),
                    }
                )

            if not messages:
                return None

            return {
                "title": title,
                "platform": platform,
                "created_at": datetime.now().isoformat(),
                "messages": messages,
                "source_file": str(file_path),
                "format": "html",
            }

        except Exception as e:
            logger.info(f"Error parsing generic HTML {file_path}: {e}")
            return None

    def _parse_generic_markdown(
        self, file_path: Path, platform: str = "Generic"
    ) -> Optional[Dict[str, Any]]:
        """Parse generic Markdown file as conversation"""
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()

            title_match = re.search(r"^#\s+(.+)$", content, re.MULTILINE)
            title = title_match.group(1) if title_match else file_path.stem

            messages = []
            paragraphs = [
                p.strip()
                for p in content.split("\n\n")
                if p.strip() and len(p.strip()) > 20
            ]

            for i, para in enumerate(paragraphs[:10]):
                role = "assistant" if i % 2 == 1 else "user"
                messages.append(
                    {
                        "role": role,
                        "content": para,
                        "timestamp": datetime.now().isoformat(),
                    }
                )

            if not messages:
                return None

            return {
                "title": title,
                "platform": platform,
                "created_at": datetime.now().isoformat(),
                "messages": messages,
                "source_file": str(file_path),
                "format": "markdown",
            }

        except Exception as e:
            logger.info(f"Error parsing generic Markdown {file_path}: {e}")
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
        .source-info {{
            background: #CONSTANT_444;
            padding: 10px;
            border-radius: 5px;
            margin-top: 10px;
            font-size: 0.8em;
            color: #ccc;
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
            <div class="source-info">
                <strong>Source:</strong> {conversation.get('source_file', 'Unknown')}<br>
                <strong>Format:</strong> {conversation.get('format', 'Unknown')}
            </div>
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
source: {conversation.get('source_file', 'Unknown')}
format: {conversation.get('format', 'Unknown')}
---

# {title}

**Platform:** {platform}  
**Created:** {created_at}  
**Messages:** {len(messages)}  
**Source:** {conversation.get('source_file', 'Unknown')}  

---

"""

        for i, message in enumerate(messages):
            role_name = "Human" if message["role"] == "user" else "Assistant"
            markdown_content += f"## {role_name}\n\n{message['content']}\n\n---\n\n"

        return markdown_content

    def export_conversation(self, conversation: Dict[str, Any]):
        """Export a single conversation to all formats"""
        # Create safe filename
        safe_title = re.sub(r"[^\w\s-]", "", conversation["title"]).strip()
        safe_title = re.sub(r"[-\s]+", "_", safe_title)

        # Create HTML export
        html_content = self.create_html_export(conversation)
        html_file = self.html_dir / f"{safe_title}.html"
        with open(html_file, "w", encoding="utf-8") as f:
            f.write(html_content)

        # Create Markdown export
        markdown_content = self.create_markdown_export(conversation)
        markdown_file = self.markdown_dir / f"{safe_title}.md"
        with open(markdown_file, "w", encoding="utf-8") as f:
            f.write(markdown_content)

        # Create JSON export
        json_file = self.json_dir / f"{safe_title}.json"
        with open(json_file, "w", encoding="utf-8") as f:
            json.dump(conversation, f, indent=2, default=str)

        return html_file, markdown_file, json_file

    def export_all_conversations(self, search_paths: List[str]):
        """Export all found conversations"""
        logger.info("🚀 Universal Conversation Exporter")
        logger.info("=" * 50)

        # Scan for conversations
        sources = self.scan_for_conversations(search_paths)

        # Process each source type
        for source_type, files in sources.items():
            if not files:
                continue

            platform = source_type.split("_")[0].title()
            if platform == "Chatgpt":
                platform = "ChatGPT"

            logger.info(
                f"\n📤 Processing {platform} {source_type.split('_')[1]} files..."
            )

            for file_path in files:
                logger.info(f"  Processing: {Path(file_path).name}")

                conversation = self.parse_conversation(file_path, platform)
                if conversation:
                    try:
                        html_file, markdown_file, json_file = self.export_conversation(
                            conversation
                        )
                        self.conversations.append(conversation)
                        self.export_stats[platform] += 1
                        logger.info(f"    ✅ Exported to: {html_file.name}")
                    except Exception as e:
                        logger.info(f"    ❌ Error exporting: {e}")
                else:
                    logger.info(f"    ⚠️  Could not parse conversation")

        # Generate summary
        self._generate_summary_report()

    def _generate_summary_report(self):
        """Generate comprehensive summary report"""
        total_conversations = len(self.conversations)
        total_messages = sum(len(conv["messages"]) for conv in self.conversations)

        report_content = f"""# Universal Conversation Export Summary

**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}  
**Total Conversations:** {total_conversations}  
**Total Messages:** {total_messages}  

## Export Statistics by Platform

"""

        for platform, count in self.export_stats.items():
            report_content += f"- **{platform}:** {count} conversations\n"

        report_content += f"""
## File Locations
- **HTML exports:** `{self.html_dir}`
- **Markdown exports:** `{self.markdown_dir}`
- **JSON exports:** `{self.json_dir}`

## Exported Conversations

"""

        for i, conv in enumerate(self.conversations, 1):
            report_content += f"""
### {i}. {conv['title']}
- **Platform:** {conv['platform']}
- **Messages:** {len(conv['messages'])}
- **Source:** {conv.get('source_file', 'Unknown')}
- **Format:** {conv.get('format', 'Unknown')}
- **Created:** {conv['created_at']}

"""

        report_file = self.analysis_dir / "export_summary.md"
        with open(report_file, "w", encoding="utf-8") as f:
            f.write(report_content)

        logger.info(
            f"\n🎉 Export complete! {total_conversations} conversations exported"
        )
        logger.info(f"📁 HTML files: {self.html_dir}")
        logger.info(f"📁 Markdown files: {self.markdown_dir}")
        logger.info(f"📁 JSON files: {self.json_dir}")
        logger.info(f"📊 Summary report: {report_file}")


def main():
    """Main function"""
    parser = argparse.ArgumentParser(description="Universal conversation exporter")
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

    exporter = UniversalConversationExporter(args.output_dir)
    exporter.export_all_conversations(args.search_paths)


if __name__ == "__main__":
    main()
