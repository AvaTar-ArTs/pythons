"""
File Management Organize Conversation Exporter 1

This module provides functionality for file management organize conversation exporter 1.

Author: Auto-generated
Date: 2025-11-01
"""

import logging

logger = logging.getLogger(__name__)


# Constants
CONSTANT_333 = 333
CONSTANT_2025 = 2025

#!/usr/bin/env python3
"""
Universal Conversation Exporter & Analyzer
Comprehensive tool for exporting and analyzing saved conversations from multiple platforms

Author: Steven Chaplinski
Date: October CONSTANT_2025
Purpose: Export, analyze, and organize conversations from ChatGPT, Claude, Perplexity, and other AI platforms
"""

import os
import json
import re
import html
from pathlib import Path
from datetime import datetime, timezone
from typing import Dict, List, Tuple, Optional, Any
import argparse
import csv
from dataclasses import dataclass, asdict
from collections import defaultdict, Counter
import hashlib
import base64


@dataclass
class ConversationMessage:
    """Represents a single message in a conversation"""

    role: str  # 'user', 'assistant', 'system'
    content: str
    timestamp: str
    message_id: str
    platform: str
    conversation_id: str
    metadata: Dict[str, Any] = None


@dataclass
class Conversation:
    """Represents a complete conversation"""

    id: str
    title: str
    platform: str
    created_at: str
    updated_at: str
    messages: List[ConversationMessage]
    metadata: Dict[str, Any] = None
    tags: List[str] = None
    category: str = None


class ConversationExporter:
    """Main class for exporting and analyzing conversations"""

    def __init__(self, output_dir: str = Path("/Users/steven/conversation-exports")):
        """__init__ function."""

        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.conversations = []
        self.analysis_data = {}

        # Create subdirectories
        self.html_dir = self.output_dir / "html"
        self.markdown_dir = self.output_dir / "markdown"
        self.json_dir = self.output_dir / "json"
        self.csv_dir = self.output_dir / "csv"
        self.analysis_dir = self.output_dir / "analysis"

        for dir_path in [self.html_dir, self.markdown_dir, self.json_dir, self.csv_dir, self.analysis_dir]:
            dir_path.mkdir(exist_ok=True)

    def detect_conversation_sources(self, search_paths: List[str]) -> Dict[str, List[str]]:
        """Detect conversation files in various formats and locations"""
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
            "csv_exports": [],
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
                content = self._read_file_safe(html_file)
                if not content:
                    continue

                if self._is_chatgpt_export(content):
                    sources["chatgpt_html"].append(str(html_file))
                elif self._is_claude_export(content):
                    sources["claude_html"].append(str(html_file))
                elif self._is_perplexity_export(content):
                    sources["perplexity_html"].append(str(html_file))
                else:
                    sources["generic_html"].append(str(html_file))

            # Scan for Markdown files
            for md_file in search_path.rglob("*.md"):
                content = self._read_file_safe(md_file)
                if not content:
                    continue

                if self._is_chatgpt_markdown(content):
                    sources["chatgpt_markdown"].append(str(md_file))
                elif self._is_claude_markdown(content):
                    sources["claude_markdown"].append(str(md_file))
                elif self._is_perplexity_markdown(content):
                    sources["perplexity_markdown"].append(str(md_file))
                else:
                    sources["generic_markdown"].append(str(md_file))

            # Scan for JSON exports
            for json_file in search_path.rglob("*.json"):
                if self._is_conversation_json(json_file):
                    sources["json_exports"].append(str(json_file))

            # Scan for CSV exports
            for csv_file in search_path.rglob("*.csv"):
                if self._is_conversation_csv(csv_file):
                    sources["csv_exports"].append(str(csv_file))

        # Print summary
        total_files = sum(len(files) for files in sources.values())
        logger.info(f"📊 Found {total_files} conversation files:")
        for source_type, files in sources.items():
            if files:
                logger.info(f"  {source_type}: {len(files)} files")

        return sources

    def _read_file_safe(self, file_path: Path) -> Optional[str]:
        """Safely read a file with error handling"""
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                return f.read()
        except (UnicodeDecodeError, IOError) as e:
            logger.info(f"⚠️  Error reading {file_path}: {e}")
            return None

    def _is_chatgpt_export(self, content: str) -> bool:
        """Check if HTML content is a ChatGPT export"""
        chatgpt_indicators = [
            "chat.openai.com",
            "ChatGPT",
            'data-theme="dark"',
            "hljs.highlightAll()",
            "renderMathInElement",
        ]
        return any(indicator in content for indicator in chatgpt_indicators)

    def _is_claude_export(self, content: str) -> bool:
        """Check if HTML content is a Claude export"""
        claude_indicators = ["claude.ai", "Anthropic", "Claude", "claude-3"]
        return any(indicator in content for indicator in claude_indicators)

    def _is_perplexity_export(self, content: str) -> bool:
        """Check if HTML content is a Perplexity export"""
        perplexity_indicators = ["perplexity.ai", "Perplexity", "pplx.ai"]
        return any(indicator in content for indicator in perplexity_indicators)

    def _is_chatgpt_markdown(self, content: str) -> bool:
        """Check if Markdown content is a ChatGPT export"""
        return "Platform: ChatGPT" in content or "**Platform:** ChatGPT" in content

    def _is_claude_markdown(self, content: str) -> bool:
        """Check if Markdown content is a Claude export"""
        return "Platform: Claude" in content or "**Platform:** Claude" in content

    def _is_perplexity_markdown(self, content: str) -> bool:
        """Check if Markdown content is a Perplexity export"""
        return "Platform: Perplexity" in content or "**Platform:** Perplexity" in content

    def _is_conversation_json(self, file_path: Path) -> bool:
        """Check if JSON file contains conversation data"""
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                data = json.load(f)
                # Look for conversation-like structure
                return isinstance(data, (list, dict)) and any(
                    key in str(data).lower() for key in ["conversation", "messages", "chat", "dialogue"]
                )
        except (json.JSONDecodeError, ValueError):
            return False

    def _is_conversation_csv(self, file_path: Path) -> bool:
        """Check if CSV file contains conversation data"""
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                first_line = f.readline().lower()
                return any(key in first_line for key in ["message", "role", "content", "conversation"])
        except (OSError, IOError, FileNotFoundError):
            return False

    def parse_chatgpt_html(self, file_path: str) -> Optional[Conversation]:
        """Parse ChatGPT HTML export"""
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()

            # Extract title from HTML
            title_match = re.search(r"<title>(.*?)</title>", content)
            title = title_match.group(1) if title_match else Path(file_path).stem

            # Extract messages from HTML structure
            messages = []

            # Look for message patterns in the HTML
            message_patterns = [
                r'<div[^>]*class="[^"]*message[^"]*"[^>]*>(.*?)</div>',
                r'<div[^>]*class="[^"]*conversation[^"]*"[^>]*>(.*?)</div>',
                r'<p[^>]*class="[^"]*user[^"]*"[^>]*>(.*?)</p>',
                r'<p[^>]*class="[^"]*assistant[^"]*"[^>]*>(.*?)</p>',
            ]

            for pattern in message_patterns:
                matches = re.findall(pattern, content, re.DOTALL)
                for i, match in enumerate(matches):
                    # Clean HTML tags
                    clean_content = re.sub(r"<[^>]+>", "", match)
                    clean_content = html.unescape(clean_content).strip()

                    if clean_content and len(clean_content) > 10:
                        # Determine role based on content patterns
                        role = (
                            "assistant"
                            if any(word in clean_content.lower() for word in ["i can", "i'll", "here's", "based on"])
                            else "user"
                        )

                        message = ConversationMessage(
                            role=role,
                            content=clean_content,
                            timestamp=datetime.now().isoformat(),
                            message_id=f"msg_{i}",
                            platform="ChatGPT",
                            conversation_id=Path(file_path).stem,
                            metadata={"source_file": file_path},
                        )
                        messages.append(message)

            if not messages:
                return None

            return Conversation(
                id=Path(file_path).stem,
                title=title,
                platform="ChatGPT",
                created_at=datetime.now().isoformat(),
                updated_at=datetime.now().isoformat(),
                messages=messages,
                metadata={"source_file": file_path, "format": "html"},
                tags=self._extract_tags_from_content(content),
                category=self._categorize_conversation(messages),
            )

        except Exception as e:
            logger.info(f"⚠️  Error parsing ChatGPT HTML {file_path}: {e}")
            return None

    def parse_chatgpt_markdown(self, file_path: str) -> Optional[Conversation]:
        """Parse ChatGPT Markdown export"""
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
                        current_message = ConversationMessage(
                            role=current_role,
                            content=line,
                            timestamp=metadata.get("date", datetime.now().isoformat()),
                            message_id=f"msg_{len(messages)}",
                            platform="ChatGPT",
                            conversation_id=Path(file_path).stem,
                            metadata={"source_file": file_path},
                        )
                    else:
                        current_message.content += "\n" + line

            if current_message:
                messages.append(current_message)

            if not messages:
                return None

            return Conversation(
                id=Path(file_path).stem,
                title=title,
                platform="ChatGPT",
                created_at=metadata.get("date", datetime.now().isoformat()),
                updated_at=datetime.now().isoformat(),
                messages=messages,
                metadata={"source_file": file_path, "format": "markdown", **metadata},
                tags=self._extract_tags_from_content(content),
                category=self._categorize_conversation(messages),
            )

        except Exception as e:
            logger.info(f"⚠️  Error parsing ChatGPT Markdown {file_path}: {e}")
            return None

    def _extract_tags_from_content(self, content: str) -> List[str]:
        """Extract relevant tags from conversation content"""
        tags = []

        # Common AI/tech tags
        tech_keywords = [
            "python",
            "javascript",
            "html",
            "css",
            "api",
            "automation",
            "ai",
            "machine learning",
            "data analysis",
        ]
        creative_keywords = ["design", "art", "creative", "visual", "story", "narrative", "branding"]
        business_keywords = ["seo", "marketing", "strategy", "business", "analytics", "conversion"]

        content_lower = content.lower()

        for keyword in tech_keywords:
            if keyword in content_lower:
                tags.append(f"tech-{keyword.replace(' ', '-')}")

        for keyword in creative_keywords:
            if keyword in content_lower:
                tags.append(f"creative-{keyword.replace(' ', '-')}")

        for keyword in business_keywords:
            if keyword in content_lower:
                tags.append(f"business-{keyword.replace(' ', '-')}")

        return list(set(tags))

    def _categorize_conversation(self, messages: List[ConversationMessage]) -> str:
        """Categorize conversation based on content analysis"""
        all_content = " ".join([msg.content for msg in messages]).lower()

        if any(word in all_content for word in ["python", "code", "script", "programming"]):
            return "technical"
        elif any(word in all_content for word in ["design", "art", "creative", "visual"]):
            return "creative"
        elif any(word in all_content for word in ["seo", "marketing", "business", "strategy"]):
            return "business"
        elif any(word in all_content for word in ["ai", "machine learning", "automation"]):
            return "ai-research"
        else:
            return "general"

    def export_conversation_html(self, conversation: Conversation) -> str:
        """Export conversation to HTML format matching the style of your examples"""
        html_content = f"""<!DOCTYPE html>
<html lang="en-US" data-theme="dark">
<head>
    <meta charset="UTF-8" />
    <link rel="icon" href="https://chat.openai.com/favicon.ico" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>{conversation.title}</title>
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
        .tags {{
            margin-top: 10px;
        }}
        .tag {{
            display: inline-block;
            background: #4CAF50;
            color: white;
            padding: 2px 8px;
            border-radius: 12px;
            font-size: 0.8em;
            margin-right: 5px;
        }}
    </style>
</head>
<body>
    <div class="conversation-container">
        <div class="metadata">
            <h1>{conversation.title}</h1>
            <p><strong>Platform:</strong> {conversation.platform}</p>
            <p><strong>Created:</strong> {conversation.created_at}</p>
            <p><strong>Messages:</strong> {len(conversation.messages)}</p>
            <p><strong>Category:</strong> {conversation.category}</p>
            {f'<div class="tags"><strong>Tags:</strong> ' + " ".join([f'<span class="tag">{tag}</span>' for tag in conversation.tags]) + '</div>' if conversation.tags else ''}
        </div>
        
        <div class="conversation">
"""

        for i, message in enumerate(conversation.messages):
            role_icon = "👤" if message.role == "user" else "🤖"
            role_name = "Human" if message.role == "user" else "Assistant"

            html_content += f"""
            <div class="message {message.role}">
                <div class="message-header">
                    {role_icon} {role_name}
                </div>
                <div class="message-content">{html.escape(message.content)}</div>
            </div>
"""

        html_content += """
        </div>
    </div>
</body>
</html>"""

        return html_content

    def export_conversation_markdown(self, conversation: Conversation) -> str:
        """Export conversation to Markdown format"""
        markdown_content = f"""---
title: {conversation.title}
platform: {conversation.platform}
date: {conversation.created_at}
messages: {len(conversation.messages)}
category: {conversation.category}
tags: {', '.join(conversation.tags) if conversation.tags else 'none'}
---

# {conversation.title}

**Platform:** {conversation.platform}  
**Created:** {conversation.created_at}  
**Messages:** {len(conversation.messages)}  
**Category:** {conversation.category}  

---

"""

        for i, message in enumerate(conversation.messages):
            role_name = "Human" if message.role == "user" else "Assistant"
            markdown_content += f"## {role_name}\n\n{message.content}\n\n---\n\n"

        return markdown_content

    def export_conversation_json(self, conversation: Conversation) -> str:
        """Export conversation to JSON format"""
        return json.dumps(asdict(conversation), indent=2, default=str)

    def analyze_conversations(self) -> Dict[str, Any]:
        """Analyze all conversations and generate insights"""
        if not self.conversations:
            return {}

        analysis = {
            "total_conversations": len(self.conversations),
            "total_messages": sum(len(conv.messages) for conv in self.conversations),
            "platforms": Counter(conv.platform for conv in self.conversations),
            "categories": Counter(conv.category for conv in self.conversations),
            "tags": Counter(tag for conv in self.conversations for tag in conv.tags),
            "message_lengths": [],
            "conversation_lengths": [],
            "date_range": {
                "earliest": min(conv.created_at for conv in self.conversations),
                "latest": max(conv.created_at for conv in self.conversations),
            },
        }

        # Calculate message and conversation lengths
        for conv in self.conversations:
            conv_length = sum(len(msg.content) for msg in conv.messages)
            analysis["conversation_lengths"].append(conv_length)

            for msg in conv.messages:
                analysis["message_lengths"].append(len(msg.content))

        # Calculate averages
        analysis["avg_message_length"] = (
            sum(analysis["message_lengths"]) / len(analysis["message_lengths"]) if analysis["message_lengths"] else 0
        )
        analysis["avg_conversation_length"] = (
            sum(analysis["conversation_lengths"]) / len(analysis["conversation_lengths"])
            if analysis["conversation_lengths"]
            else 0
        )

        return analysis

    def generate_analysis_report(self) -> str:
        """Generate comprehensive analysis report"""
        analysis = self.analyze_conversations()

        if not analysis:
            return "No conversations to analyze."

        report = f"""# Conversation Analysis Report

**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}  
**Total Conversations:** {analysis['total_conversations']}  
**Total Messages:** {analysis['total_messages']}  

## Platform Distribution
"""

        for platform, count in analysis["platforms"].most_common():
            report += f"- **{platform}:** {count} conversations\n"

        report += "\n## Category Distribution\n"
        for category, count in analysis["categories"].most_common():
            report += f"- **{category}:** {count} conversations\n"

        report += "\n## Top Tags\n"
        for tag, count in analysis["tags"].most_common(10):
            report += f"- **{tag}:** {count} occurrences\n"

        report += f"""
## Statistics
- **Average Message Length:** {analysis['avg_message_length']:.0f} characters
- **Average Conversation Length:** {analysis['avg_conversation_length']:.0f} characters
- **Date Range:** {analysis['date_range']['earliest']} to {analysis['date_range']['latest']}

## Insights
- Most active platform: {analysis['platforms'].most_common(1)[0][0]}
- Most common category: {analysis['categories'].most_common(1)[0][0]}
- Most used tag: {analysis['tags'].most_common(1)[0][0] if analysis['tags'] else 'None'}
"""

        return report

    def export_all_conversations(self, sources: Dict[str, List[str]]) -> List[Conversation]:
        """Export all conversations from detected sources"""
        logger.info("📤 Exporting conversations...")

        # Process ChatGPT HTML files
        for file_path in sources.get("chatgpt_html", []):
            conv = self.parse_chatgpt_html(file_path)
            if conv:
                self.conversations.append(conv)
                self._save_conversation_files(conv)

        # Process ChatGPT Markdown files
        for file_path in sources.get("chatgpt_markdown", []):
            conv = self.parse_chatgpt_markdown(file_path)
            if conv:
                self.conversations.append(conv)
                self._save_conversation_files(conv)

        # Process other formats (add more parsers as needed)
        for file_path in sources.get("generic_html", []):
            # Try to parse as generic conversation
            conv = self._parse_generic_html(file_path)
            if conv:
                self.conversations.append(conv)
                self._save_conversation_files(conv)

        for file_path in sources.get("generic_markdown", []):
            # Try to parse as generic conversation
            conv = self._parse_generic_markdown(file_path)
            if conv:
                self.conversations.append(conv)
                self._save_conversation_files(conv)

        logger.info(f"✅ Exported {len(self.conversations)} conversations")
        return self.conversations

    def _parse_generic_html(self, file_path: str) -> Optional[Conversation]:
        """Parse generic HTML file as conversation"""
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()

            # Extract title
            title_match = re.search(r"<title>(.*?)</title>", content)
            title = title_match.group(1) if title_match else Path(file_path).stem

            # Simple message extraction
            messages = []
            # Look for any text content that might be messages
            text_content = re.sub(r"<[^>]+>", " ", content)
            text_content = html.unescape(text_content)

            # Split into potential messages
            paragraphs = [p.strip() for p in text_content.split("\n") if p.strip() and len(p.strip()) > 20]

            for i, para in enumerate(paragraphs[:10]):  # Limit to first 10 paragraphs
                role = "assistant" if i % 2 == 1 else "user"
                message = ConversationMessage(
                    role=role,
                    content=para,
                    timestamp=datetime.now().isoformat(),
                    message_id=f"msg_{i}",
                    platform="Generic",
                    conversation_id=Path(file_path).stem,
                    metadata={"source_file": file_path},
                )
                messages.append(message)

            if not messages:
                return None

            return Conversation(
                id=Path(file_path).stem,
                title=title,
                platform="Generic",
                created_at=datetime.now().isoformat(),
                updated_at=datetime.now().isoformat(),
                messages=messages,
                metadata={"source_file": file_path, "format": "html"},
                tags=[],
                category="general",
            )

        except Exception as e:
            logger.info(f"⚠️  Error parsing generic HTML {file_path}: {e}")
            return None

    def _parse_generic_markdown(self, file_path: str) -> Optional[Conversation]:
        """Parse generic Markdown file as conversation"""
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()

            # Extract title from first heading
            title_match = re.search(r"^#\s+(.+)$", content, re.MULTILINE)
            title = title_match.group(1) if title_match else Path(file_path).stem

            # Simple message extraction
            messages = []
            paragraphs = [p.strip() for p in content.split("\n\n") if p.strip() and len(p.strip()) > 20]

            for i, para in enumerate(paragraphs[:10]):  # Limit to first 10 paragraphs
                role = "assistant" if i % 2 == 1 else "user"
                message = ConversationMessage(
                    role=role,
                    content=para,
                    timestamp=datetime.now().isoformat(),
                    message_id=f"msg_{i}",
                    platform="Generic",
                    conversation_id=Path(file_path).stem,
                    metadata={"source_file": file_path},
                )
                messages.append(message)

            if not messages:
                return None

            return Conversation(
                id=Path(file_path).stem,
                title=title,
                platform="Generic",
                created_at=datetime.now().isoformat(),
                updated_at=datetime.now().isoformat(),
                messages=messages,
                metadata={"source_file": file_path, "format": "markdown"},
                tags=[],
                category="general",
            )

        except Exception as e:
            logger.info(f"⚠️  Error parsing generic Markdown {file_path}: {e}")
            return None

    def _save_conversation_files(self, conversation: Conversation):
        """Save conversation in all formats"""
        # Save HTML
        html_content = self.export_conversation_html(conversation)
        html_file = self.html_dir / f"{conversation.id}.html"
        with open(html_file, "w", encoding="utf-8") as f:
            f.write(html_content)

        # Save Markdown
        markdown_content = self.export_conversation_markdown(conversation)
        markdown_file = self.markdown_dir / f"{conversation.id}.md"
        with open(markdown_file, "w", encoding="utf-8") as f:
            f.write(markdown_content)

        # Save JSON
        json_content = self.export_conversation_json(conversation)
        json_file = self.json_dir / f"{conversation.id}.json"
        with open(json_file, "w", encoding="utf-8") as f:
            f.write(json_content)

    def save_analysis_report(self):
        """Save analysis report to file"""
        report = self.generate_analysis_report()
        report_file = self.analysis_dir / f"conversation_analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
        with open(report_file, "w", encoding="utf-8") as f:
            f.write(report)
        logger.info(f"📊 Analysis report saved: {report_file}")
        return report_file

    def export_to_csv(self):
        """Export conversation data to CSV for analysis"""
        csv_file = self.csv_dir / f"conversations_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"

        with open(csv_file, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["conversation_id", "title", "platform", "created_at", "category", "message_count", "tags"])

            for conv in self.conversations:
                writer.writerow(
                    [
                        conv.id,
                        conv.title,
                        conv.platform,
                        conv.created_at,
                        conv.category,
                        len(conv.messages),
                        ", ".join(conv.tags),
                    ]
                )

        logger.info(f"📊 CSV export saved: {csv_file}")
        return csv_file


def main():
    """Main function to run the conversation exporter"""
    parser = argparse.ArgumentParser(description="Export and analyze conversations from multiple platforms")
    parser.add_argument(
        "--search-paths",
        nargs="+",
        default=["/Users/steven/Downloads", "/Users/steven/SUNO", "/Users/steven/Documents"],
        help="Paths to search for conversation files",
    )
    parser.add_argument(
        "--output-dir", default="/Users/steven/conversation-exports", help="Output directory for exported conversations"
    )

    args = parser.parse_args()

    logger.info("🚀 Starting Conversation Exporter...")
    logger.info("=" * 50)

    exporter = ConversationExporter(args.output_dir)

    # Detect conversation sources
    sources = exporter.detect_conversation_sources(args.search_paths)

    # Export all conversations
    conversations = exporter.export_all_conversations(sources)

    if conversations:
        # Generate analysis report
        report_file = exporter.save_analysis_report()

        # Export to CSV
        csv_file = exporter.export_to_csv()

        logger.info(Path("\n") + "=" * 50)
        logger.info("EXPORT COMPLETE")
        logger.info("=" * 50)
        logger.info(f"✅ Exported {len(conversations)} conversations")
        logger.info(f"📁 HTML files: {exporter.html_dir}")
        logger.info(f"📁 Markdown files: {exporter.markdown_dir}")
        logger.info(f"📁 JSON files: {exporter.json_dir}")
        logger.info(f"📊 Analysis report: {report_file}")
        logger.info(f"📊 CSV export: {csv_file}")
    else:
        logger.info("❌ No conversations found to export")


if __name__ == "__main__":
    main()
