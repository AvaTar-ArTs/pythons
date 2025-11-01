"""
Utilities File Operations Archive 1

This module provides functionality for utilities file operations archive 1.

Author: Auto-generated
Date: 2025-11-01
"""

import logging

logger = logging.getLogger(__name__)


# Constants
CONSTANT_300 = 300

#!/usr/bin/env python3
"""
Real-time Conversation Archive Automation
Monitors and automatically updates conversation archives
"""

import time
import os
import json
from datetime import datetime
from pathlib import Path
from conversation_capture import ConversationArchiver
import threading
import subprocess


class AutoArchiver:
    def __init__(self, base_dir=Path("/Users/steven")):
        """__init__ function."""

        self.base_dir = Path(base_dir)
        self.archiver = ConversationArchiver(base_dir)
        self.running = False
        self.update_interval = 30  # seconds
        self.last_update = None

    def start_monitoring(self):
        """Start the automatic monitoring and updating"""
        logger.info("🚀 Starting automatic conversation archive monitoring...")
        logger.info(f"📁 Monitoring: {self.base_dir}")
        logger.info(f"⏱️  Update interval: {self.update_interval} seconds")
        logger.info("Press Ctrl+C to stop")

        self.running = True

        try:
            while self.running:
                self.check_and_update()
                time.sleep(self.update_interval)
        except KeyboardInterrupt:
            logger.info("\n🛑 Stopping automatic archiving...")
            self.running = False

    def check_and_update(self):
        """Check for changes and update archive if needed"""
        try:
            # Check if Cursor prompt history has been updated
            prompt_history_path = self.base_dir / ".cursor" / "prompt_history.json"
            if prompt_history_path.exists():
                stat = prompt_history_path.stat()
                if self.last_update is None or stat.st_mtime > self.last_update:
                    logger.info(f"📝 Detected changes in prompt history at {datetime.now().strftime('%H:%M:%S')}")
                    self.update_archive()
                    self.last_update = stat.st_mtime

            # Check for new chat directories
            cursor_chats = self.base_dir / ".cursor" / "chats"
            if cursor_chats.exists():
                chat_dirs = [d for d in cursor_chats.iterdir() if d.is_dir()]
                for chat_dir in chat_dirs:
                    # Check if this is a new chat directory
                    if self.is_new_chat_directory(chat_dir):
                        logger.info(f"💬 Detected new chat directory: {chat_dir.name}")
                        self.update_archive()
                        break

        except Exception as e:
            logger.info(f"❌ Error during monitoring: {e}")

    def is_new_chat_directory(self, chat_dir):
        """Check if a chat directory is new (created in last 5 minutes)"""
        try:
            stat = chat_dir.stat()
            age_seconds = time.time() - stat.st_mtime
            return age_seconds < CONSTANT_300  # 5 minutes
        except Exception:
            return False

    def update_archive(self):
        """Update the conversation archive"""
        try:
            logger.info("🔄 Updating archive...")
            conversations = self.archiver.run_archive_update()
            logger.info(f"✅ Archive updated successfully! ({len(conversations)} conversations)")
        except Exception as e:
            logger.info(f"❌ Error updating archive: {e}")

    def add_current_message(self, role, content):
        """Add a message to the current session"""
        self.archiver.update_current_session(role, content)
        logger.info(f"💬 Added {role} message to current session")

    def force_update(self):
        """Force an immediate archive update"""
        logger.info("🔄 Forcing archive update...")
        self.update_archive()


def create_systemd_service():
    """Create a systemd service file for Linux systems"""
    service_content = f"""[Unit]
Description=Auto Conversation Archiver
After=network.target

[Service]
Type=simple
User={os.getenv('USER')}
WorkingDirectory={os.getcwd()}
ExecStart=/usr/bin/python3 {os.path.abspath(__file__)}
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
"""

    service_path = Path.home() / ".config" / "systemd" / "user" / "conversation-archiver.service"
    service_path.parent.mkdir(parents=True, exist_ok=True)

    with open(service_path, "w") as f:
        f.write(service_content)

    logger.info(f"📄 Systemd service created: {service_path}")
    logger.info("To enable: systemctl --user enable conversation-archiver.service")
    logger.info("To start: systemctl --user start conversation-archiver.service")


def create_launchd_plist():
    """Create a LaunchAgent plist for macOS"""
    plist_content = f"""<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.conversation.archiver</string>
    <key>ProgramArguments</key>
    <array>
        <string>/usr/bin/python3</string>
        <string>{os.path.abspath(__file__)}</string>
    </array>
    <key>WorkingDirectory</key>
    <string>{os.getcwd()}</string>
    <key>RunAtLoad</key>
    <true/>
    <key>KeepAlive</key>
    <true/>
    <key>StandardOutPath</key>
    <string>/tmp/conversation-archiver.log</string>
    <key>StandardErrorPath</key>
    <string>/tmp/conversation-archiver.error.log</string>
</dict>
</plist>"""

    plist_path = Path.home() / "Library" / "LaunchAgents" / "com.conversation.archiver.plist"
    plist_path.parent.mkdir(parents=True, exist_ok=True)

    with open(plist_path, "w") as f:
        f.write(plist_content)

    logger.info(f"📄 LaunchAgent plist created: {plist_path}")
    logger.info("To load: launchctl load ~/Library/LaunchAgents/com.conversation.archiver.plist")
    logger.info("To unload: launchctl unload ~/Library/LaunchAgents/com.conversation.archiver.plist")


def create_cron_job():
    """Create a cron job for periodic updates"""
    cron_entry = f"*/5 * * * * cd {os.getcwd()} && /usr/bin/python3 {os.path.abspath(__file__)} --cron"

    logger.info("📅 Add this to your crontab:")
    logger.info(f"crontab -e")
    logger.info(f"Then add: {cron_entry}")


def main():
    """Main execution function"""
    import sys

    if len(sys.argv) > 1 and sys.argv[1] == "--cron":
        # Run in cron mode (single update)
        archiver = ConversationArchiver()
        archiver.run_archive_update()
        return

    if len(sys.argv) > 1 and sys.argv[1] == "--setup":
        # Setup system service
        if os.name == "posix" and os.uname().sysname == "Darwin":  # macOS
            create_launchd_plist()
        elif os.name == "posix":  # Linux
            create_systemd_service()

        create_cron_job()
        return

    # Run in monitoring mode
    auto_archiver = AutoArchiver()

    # Add current conversation
    auto_archiver.add_current_message(
        "user",
        "create into md or html type files that are like an archive style blog or something, and then automate the update as we converse",
    )
    auto_archiver.add_current_message(
        "assistant",
        "I'll create an automated archive system that captures our conversations and updates in real-time...",
    )

    # Start monitoring
    auto_archiver.start_monitoring()


if __name__ == "__main__":
    main()
