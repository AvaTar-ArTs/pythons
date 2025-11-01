"""
Database Clients Extract 9

This module provides functionality for database clients extract 9.

Author: Auto-generated
Date: 2025-11-01
"""

import logging

logger = logging.getLogger(__name__)


# Constants
CONSTANT_100 = 100
CONSTANT_200 = 200
CONSTANT_1000 = 1000

#!/usr/bin/env python3
"""
Automated Conversation Archive System
Captures and updates conversation data in real-time
"""

import json
import os
import sqlite3
import time
from datetime import datetime
from pathlib import Path
import shutil


class ConversationArchiver:
    def __init__(self, base_dir=Path("/Users/steven")):
        """__init__ function."""

        self.base_dir = Path(base_dir)
        self.archive_dir = self.base_dir / "conversation_archive"
        self.archive_dir.mkdir(exist_ok=True)

        # Database for storing conversation data
        self.db_path = self.archive_dir / "conversations.db"
        self.init_database()

        # Cursor chat directory
        self.cursor_chats = self.base_dir / ".cursor" / "chats"
        self.prompt_history = self.base_dir / ".cursor" / "prompt_history.json"

    def init_database(self):
        """Initialize SQLite database for conversation storage"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS conversations (
                id TEXT PRIMARY KEY,
                title TEXT,
                date TEXT,
                preview TEXT,
                tags TEXT,
                messages TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """
        )

        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS current_session (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                role TEXT,
                content TEXT,
                timestamp TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """
        )

        conn.commit()
        conn.close()

    def extract_cursor_conversations(self):
        """Extract conversations from Cursor's chat database"""
        conversations = []

        if not self.cursor_chats.exists():
            return conversations

        # Get all chat directories
        chat_dirs = [d for d in self.cursor_chats.iterdir() if d.is_dir()]

        for chat_dir in chat_dirs:
            try:
                # Get metadata
                db_path = chat_dir / "store.db"
                if not db_path.exists():
                    continue

                conn = sqlite3.connect(db_path)
                cursor = conn.cursor()

                # Get metadata
                meta_data = cursor.execute(
                    "SELECT value FROM meta WHERE key = '0'"
                ).fetchone()
                if meta_data:
                    import base64

                    meta_json = base64.b64decode(meta_data[0]).decode("utf-8")
                    meta = json.loads(meta_json)

                    # Extract conversation info
                    conv_id = meta.get("agentId", str(chat_dir.name))
                    conv_name = meta.get("name", "Untitled Conversation")
                    created_at = meta.get("createdAt", int(time.time() * CONSTANT_1000))

                    # Convert timestamp to readable date
                    conv_date = datetime.fromtimestamp(
                        created_at / CONSTANT_1000
                    ).strftime("%Y-%m-%d")

                    conversations.append(
                        {
                            "id": conv_id,
                            "title": conv_name,
                            "date": conv_date,
                            "preview": f"Conversation from {conv_date}",
                            "tags": self.extract_tags_from_name(conv_name),
                            "messages": [],  # Would need more complex extraction for full messages
                        }
                    )

                conn.close()

            except Exception as e:
                logger.info(f"Error processing {chat_dir}: {e}")
                continue

        return conversations

    def extract_tags_from_name(self, name):
        """Extract relevant tags from conversation name"""
        tags = []
        name_lower = name.lower()

        if "document" in name_lower or "file" in name_lower:
            tags.append("file-management")
        if "website" in name_lower or "web" in name_lower:
            tags.append("web-development")
        if "seo" in name_lower or "marketing" in name_lower:
            tags.append("seo")
        if "python" in name_lower or "code" in name_lower:
            tags.append("python")
        if "business" in name_lower:
            tags.append("business")
        if "ai" in name_lower or "gpt" in name_lower:
            tags.append("ai")

        return tags if tags else ["general"]

    def load_prompt_history(self):
        """Load recent prompts from Cursor's prompt history"""
        if not self.prompt_history.exists():
            return []

        try:
            with open(self.prompt_history, "r") as f:
                prompts = json.load(f)
            return prompts[-50:]  # Last 50 prompts
        except Exception as e:
            logger.info(f"Error loading prompt history: {e}")
            return []

    def create_conversation_from_prompts(self, prompts):
        """Create conversation entries from prompt history"""
        conversations = []

        # Group prompts by date
        daily_prompts = {}
        for prompt in prompts:
            # Use current date as we don't have timestamps in prompt history
            date = datetime.now().strftime("%Y-%m-%d")
            if date not in daily_prompts:
                daily_prompts[date] = []
            daily_prompts[date].append(prompt)

        # Create conversation entries
        for date, day_prompts in daily_prompts.items():
            if not day_prompts:
                continue

            # Determine conversation title based on content
            title = self.generate_title_from_prompts(day_prompts)
            preview = (
                day_prompts[0][:CONSTANT_100] + "..."
                if len(day_prompts[0]) > CONSTANT_100
                else day_prompts[0]
            )
            tags = self.extract_tags_from_prompts(day_prompts)

            conversations.append(
                {
                    "id": f"prompt-{date}",
                    "title": title,
                    "date": date,
                    "preview": preview,
                    "tags": tags,
                    "messages": [
                        {"role": "user", "content": p, "time": "N/A"}
                        for p in day_prompts[:10]
                    ],  # Limit to 10 messages
                }
            )

        return conversations

    def generate_title_from_prompts(self, prompts):
        """Generate a meaningful title from a list of prompts"""
        # Look for common patterns
        first_prompt = prompts[0].lower()

        if "document" in first_prompt or "file" in first_prompt:
            return "Document Organization & File Management"
        elif "website" in first_prompt or "web" in first_prompt:
            return "Website Development & SEO"
        elif "python" in first_prompt or "code" in first_prompt:
            return "Python Development & Coding"
        elif "business" in first_prompt:
            return "Business Development & Strategy"
        elif "analyze" in first_prompt:
            return "Data Analysis & Research"
        else:
            return f"Conversation - {datetime.now().strftime('%B %d, %Y')}"

    def extract_tags_from_prompts(self, prompts):
        """Extract tags from a list of prompts"""
        all_text = " ".join(prompts).lower()
        tags = []

        tag_keywords = {
            "file-management": ["document", "file", "folder", "organize", "sort"],
            "web-development": ["website", "web", "html", "css", "javascript"],
            "seo": ["seo", "search", "optimize", "ranking", "marketing"],
            "python": ["python", "code", "script", "programming"],
            "business": ["business", "client", "invoice", "freelance"],
            "ai": ["ai", "gpt", "chat", "assistant", "automation"],
            "automation": ["automate", "script", "batch", "process"],
            "data-analysis": ["analyze", "data", "csv", "export", "report"],
        }

        for tag, keywords in tag_keywords.items():
            if any(keyword in all_text for keyword in keywords):
                tags.append(tag)

        return tags if tags else ["general"]

    def save_conversations(self, conversations):
        """Save conversations to database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        for conv in conversations:
            cursor.execute(
                """
                INSERT OR REPLACE INTO conversations 
                (id, title, date, preview, tags, messages, updated_at)
                VALUES (?, ?, ?, ?, ?, ?, CURRENT_TIMESTAMP)
            """,
                (
                    conv["id"],
                    conv["title"],
                    conv["date"],
                    conv["preview"],
                    json.dumps(conv["tags"]),
                    json.dumps(conv["messages"]),
                ),
            )

        conn.commit()
        conn.close()

    def load_conversations(self):
        """Load conversations from database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT id, title, date, preview, tags, messages, updated_at
            FROM conversations
            ORDER BY updated_at DESC
        """
        )

        conversations = []
        for row in cursor.fetchall():
            conversations.append(
                {
                    "id": row[0],
                    "title": row[1],
                    "date": row[2],
                    "preview": row[3],
                    "tags": json.loads(row[4]),
                    "messages": json.loads(row[5]),
                }
            )

        conn.close()
        return conversations

    def update_current_session(self, role, content):
        """Update current session with new message"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute(
            """
            INSERT INTO current_session (role, content, timestamp)
            VALUES (?, ?, ?)
        """,
            (role, content, datetime.now().strftime("%H:%M")),
        )

        conn.commit()
        conn.close()

    def get_current_session(self):
        """Get current session messages"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT role, content, timestamp
            FROM current_session
            ORDER BY created_at DESC
            LIMIT 20
        """
        )

        messages = []
        for row in cursor.fetchall():
            messages.append({"role": row[0], "content": row[1], "time": row[2]})

        conn.close()
        return list(reversed(messages))  # Reverse to show chronological order

    def generate_html_archive(self):
        """Generate updated HTML archive"""
        conversations = self.load_conversations()
        current_messages = self.get_current_session()

        # Read the HTML template
        html_path = self.base_dir / "conversation_archive.html"
        if not html_path.exists():
            logger.info("HTML template not found. Please run the initial setup first.")
            return

        with open(html_path, "r") as f:
            html_content = f.read()

        # Update the JavaScript data
        conversations_js = json.dumps(conversations, indent=2)
        current_messages_js = json.dumps(current_messages, indent=2)

        # Replace placeholders in HTML
        html_content = html_content.replace(
            "const conversations = [];", f"const conversations = {conversations_js};"
        )
        html_content = html_content.replace(
            "const currentMessages = [];",
            f"const currentMessages = {current_messages_js};",
        )

        # Write updated HTML
        with open(html_path, "w") as f:
            f.write(html_content)

        logger.info(f"✅ HTML archive updated with {len(conversations)} conversations")

    def generate_markdown_archive(self):
        """Generate markdown archive"""
        conversations = self.load_conversations()
        current_messages = self.get_current_session()

        markdown = f"""# AI Conversation Archive

Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## Current Session

"""

        for msg in current_messages:
            markdown += (
                f"**{msg['role'].upper()} ({msg['time']}):** {msg['content']}\n\n"
            )

        markdown += "\n---\n\n## Conversation History\n\n"

        for conv in conversations:
            markdown += f"### {conv['title']}\n\n"
            markdown += f"**Date:** {conv['date']}\n"
            markdown += f"**Tags:** {', '.join(conv['tags'])}\n\n"
            markdown += f"**Preview:** {conv['preview']}\n\n"

            if conv["messages"]:
                markdown += "#### Messages\n\n"
                for msg in conv["messages"][:5]:  # Limit to first 5 messages
                    markdown += f"**{msg['role'].upper()}:** {msg['content'][:CONSTANT_200]}...\n\n"

            markdown += "---\n\n"

        # Save markdown file
        md_path = (
            self.archive_dir
            / f"conversation-archive-{datetime.now().strftime('%Y-%m-%d')}.md"
        )
        with open(md_path, "w") as f:
            f.write(markdown)

        logger.info(f"✅ Markdown archive saved to {md_path}")
        return md_path

    def run_archive_update(self):
        """Main function to update the archive"""
        logger.info("🔄 Updating conversation archive...")

        # Extract conversations from Cursor
        cursor_conversations = self.extract_cursor_conversations()

        # Load prompt history
        prompts = self.load_prompt_history()
        prompt_conversations = self.create_conversation_from_prompts(prompts)

        # Combine all conversations
        all_conversations = cursor_conversations + prompt_conversations

        # Remove duplicates based on ID
        unique_conversations = {}
        for conv in all_conversations:
            unique_conversations[conv["id"]] = conv

        conversations = list(unique_conversations.values())

        # Save to database
        self.save_conversations(conversations)

        # Generate archives
        self.generate_html_archive()
        md_path = self.generate_markdown_archive()

        logger.info(f"✅ Archive update complete!")
        logger.info(f"📊 Total conversations: {len(conversations)}")
        logger.info(f"📄 HTML: {self.base_dir / 'conversation_archive.html'}")
        logger.info(f"📄 Markdown: {md_path}")

        return conversations


def main():
    """Main execution function"""
    archiver = ConversationArchiver()

    # Update current session with this conversation
    archiver.update_current_session(
        "user",
        "create into md or html type files that are like an archive style blog or something, and then automate the update as we converse",
    )
    archiver.update_current_session(
        "assistant",
        "I'll create an automated archive system that captures our conversations and updates in real-time...",
    )

    # Run the archive update
    conversations = archiver.run_archive_update()

    logger.info("\n🎉 Archive system is now active!")
    logger.info(
        "The system will automatically capture and organize your conversations."
    )


if __name__ == "__main__":
    main()
