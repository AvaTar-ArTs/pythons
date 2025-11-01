"""
Organize 18

This module provides functionality for organize 18.

Author: Auto-generated
Date: 2025-11-01
"""

import logging

logger = logging.getLogger(__name__)


# Constants
CONSTANT_2025 = 2025

#!/usr/bin/env python3
"""
File Organization Script for AI Export Tools
Implements the recommendations from the analysis report
"""

import os
import shutil
from pathlib import Path
import re
from datetime import datetime


def organize_files(base_dir):
    """Organize files according to analysis recommendations"""
    base_path = Path(base_dir)

    # Create directory structure
    scripts_dir = base_path / "scripts"
    exports_dir = base_path / "exports"
    archive_dir = base_path / "archive"

    for dir_path in [scripts_dir, exports_dir, archive_dir]:
        dir_path.mkdir(exist_ok=True)

    logger.info("Created directory structure:")
    logger.info(f"  - {scripts_dir}")
    logger.info(f"  - {exports_dir}")
    logger.info(f"  - {archive_dir}")

    # Files to keep and their new names
    keep_files = {
        # Scripts to keep
        "2Universal AI Conversation & GPT Exporter-3.1.0.user.js": "scripts/2Universal-AI-Conversation-GPT-Exporter-v3.1.0.user.js",
        "Claude Project Files Extractor-3.0.user.js": "scripts/Claude-Project-Files-Extractor-v3.0.user.js",
        "Enhanced Grok Export v2.4-2.4.0.user.js": "scripts/Enhanced-Grok-Export-v2.4.user.js",
        # Exports to keep
        "chat-export.md": "exports/AI-Art-Prompt-Engineering-ChatGPT-CONSTANT_2025-10-17.md",
        "files.zip": "exports/As_A_Man_Thinketh_Narrative.zip",
    }

    # Files to archive (duplicates/obsolete)
    archive_files = [
        "ChatGPT对话Markdown导出-1.2.user.js",
        "Grok3对话Markdown导出-1.01.user.js",
        "Export ChatGPT-Gemini-Grok conversations as Markdown-1.1.1.user.js",
        "chat-export (1).md",
        "chat-export (2).md",
        "chat-export (3).md",
        "grok-FULL-conversation-1msgs-CONSTANT_2025-10-17T08-26-18.md",
        "grok-FULL-conversation-1msgs-CONSTANT_2025-10-17T08-56-30.md",
    ]

    # Move files to appropriate directories
    moved_count = 0
    archived_count = 0

    logger.info("\nMoving files to organized structure:")

    # Move files to keep
    for old_name, new_path in keep_files.items():
        old_path = base_path / old_name
        new_full_path = base_path / new_path

        if old_path.exists():
            # Ensure parent directory exists
            new_full_path.parent.mkdir(parents=True, exist_ok=True)

            shutil.move(str(old_path), str(new_full_path))
            logger.info(f"  ✓ Moved: {old_name} → {new_path}")
            moved_count += 1
        else:
            logger.info(f"  ✗ Not found: {old_name}")

    # Archive duplicate/obsolete files
    logger.info("\nArchiving duplicate/obsolete files:")
    for filename in archive_files:
        old_path = base_path / filename
        if old_path.exists():
            new_path = archive_dir / filename
            shutil.move(str(old_path), str(new_path))
            logger.info(f"  ✓ Archived: {filename}")
            archived_count += 1
        else:
            logger.info(f"  ✗ Not found: {filename}")

    # Create summary report
    create_summary_report(base_path, moved_count, archived_count)

    return moved_count, archived_count


def create_summary_report(base_path, moved_count, archived_count):
    """Create a summary report of the organization"""
    report_path = base_path / "organization_summary.md"

    with open(report_path, "w", encoding="utf-8") as f:
        f.write("# File Organization Summary\n\n")
        f.write(f"**Date:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"**Files Moved:** {moved_count}\n")
        f.write(f"**Files Archived:** {archived_count}\n\n")

        f.write("## Directory Structure\n\n")
        f.write("```\n")
        f.write("SUNO/10-14/\n")
        f.write("├── scripts/                    # Active user scripts\n")
        f.write("│   ├── 2Universal-AI-Conversation-GPT-Exporter-v3.1.0.user.js\n")
        f.write("│   ├── Claude-Project-Files-Extractor-v3.0.user.js\n")
        f.write("│   └── Enhanced-Grok-Export-v2.4.user.js\n")
        f.write("├── exports/                    # Exported conversations\n")
        f.write("│   ├── AI-Art-Prompt-Engineering-ChatGPT-CONSTANT_2025-10-17.md\n")
        f.write("│   └── As_A_Man_Thinketh_Narrative.zip\n")
        f.write("├── archive/                    # Duplicate/obsolete files\n")
        f.write("│   ├── ChatGPT对话Markdown导出-1.2.user.js\n")
        f.write("│   ├── Grok3对话Markdown导出-1.01.user.js\n")
        f.write("│   ├── Export ChatGPT-Gemini-Grok conversations as Markdown-1.1.1.user.js\n")
        f.write("│   ├── chat-export (1).md\n")
        f.write("│   ├── chat-export (2).md\n")
        f.write("│   ├── chat-export (3).md\n")
        f.write("│   ├── grok-FULL-conversation-1msgs-CONSTANT_2025-10-17T08-26-18.md\n")
        f.write("│   └── grok-FULL-conversation-1msgs-CONSTANT_2025-10-17T08-56-30.md\n")
        f.write("├── analysis_report.md          # Detailed analysis\n")
        f.write("├── organize_files.py           # This script\n")
        f.write("└── organization_summary.md     # This summary\n")
        f.write("```\n\n")

        f.write("## Scripts Kept (Active)\n\n")
        f.write("1. **2Universal AI Conversation & GPT Exporter v3.1.0**\n")
        f.write("   - Most comprehensive multi-platform exporter\n")
        f.write("   - Supports ChatGPT, Claude, DeepSeek, Bard, 元宝\n")
        f.write("   - Advanced features and UI\n\n")

        f.write("2. **Claude Project Files Extractor v3.0**\n")
        f.write("   - Unique functionality for Claude projects\n")
        f.write("   - ZIP file extraction capabilities\n")
        f.write("   - Specialized for Claude.ai\n\n")

        f.write("3. **Enhanced Grok Export v2.4**\n")
        f.write("   - Best Grok-specific features\n")
        f.write("   - Auto-scroll and social sharing\n")
        f.write("   - Multiple export formats\n\n")

        f.write("## Files Archived\n\n")
        f.write("- **3 duplicate scripts** with overlapping functionality\n")
        f.write("- **4 duplicate markdown files** (exact copies)\n")
        f.write("- **2 empty Grok conversations** with no content\n\n")

        f.write("## Benefits of Organization\n\n")
        f.write("1. **Reduced clutter** - Removed 7 duplicate/empty files\n")
        f.write("2. **Clear structure** - Separated scripts from exports\n")
        f.write("3. **Better naming** - Descriptive, date-stamped filenames\n")
        f.write("4. **Preserved functionality** - Kept the 3 best scripts\n")
        f.write("5. **Easy maintenance** - Clear organization for future updates\n")

    logger.info(f"\nCreated organization summary: {report_path}")


def main():
    """main function."""

    base_dir = Path("/Users/steven/SUNO/10-14")

    logger.info("AI Export Tools Organization Script")
    logger.info("=" * 40)

    # Check if we're in the right directory
    if not Path(base_dir).exists():
        logger.info(f"Error: Directory {base_dir} does not exist")
        return

    # Organize files
    moved_count, archived_count = organize_files(base_dir)

    logger.info(f"\nOrganization Complete!")
    logger.info(f"✓ Files moved to organized structure: {moved_count}")
    logger.info(f"✓ Files archived: {archived_count}")
    logger.info(f"✓ Total files processed: {moved_count + archived_count}")


if __name__ == "__main__":
    main()
