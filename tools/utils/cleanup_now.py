import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
#!/usr/bin/env python3
"""
Cleanup Ollama duplicates and organize Notion exports
"""

import os
import shutil
from pathlib import Path
from datetime import datetime

ARCHIVES_DIR = Path("/Users/steven/Documents/Archives")
BACKUP_DIR = (
    ARCHIVES_DIR
    / "misc-archives"
    / f"cleanup-backup-{datetime.now().strftime('%Y%m%d_%H%M%S')}"
)
NOTION_DIR = ARCHIVES_DIR / "misc-archives" / "notion-exports"


def main():
    os.chdir(ARCHIVES_DIR)

    print("🧹 Starting Archives cleanup...")
    print("")

    # Create backup directory
    BACKUP_DIR.mkdir(parents=True, exist_ok=True)
    NOTION_DIR.mkdir(parents=True, exist_ok=True)

    # 1. Ollama config duplicates
    print("📦 Processing Ollama config duplicates...")
    KEEP_OLLAMA = "ollama-setup-kit-Intel-macOS.zip"
    ollama_removed = 0

    for file in ARCHIVES_DIR.glob("ollama*.zip"):
        if file.name != KEEP_OLLAMA:
            print(f"  Moving to backup: {file.name}")
            shutil.move(str(file), str(BACKUP_DIR / file.name))
            ollama_removed += 1
        else:
            print(f"  ✅ Keeping: {file.name} (most recent/specific)")

    if ollama_removed == 0:
        print("  ℹ️  No Ollama duplicates found or already cleaned")
    else:
        print(f"  ✅ Removed {ollama_removed} Ollama config duplicates")

    # 2. Organize Notion exports
    print("")
    print("📦 Organizing Notion exports...")
    notion_count = 0

    # Find Notion export files (pattern: *Export*.zip or UUID_Export*.zip)
    for file in ARCHIVES_DIR.glob("*Export*.zip"):
        print(f"  Moving: {file.name}")
        shutil.move(str(file), str(NOTION_DIR / file.name))
        notion_count += 1

    # Also check for UUID-named files
    for file in ARCHIVES_DIR.glob(
        "[0-9a-f][0-9a-f][0-9a-f][0-9a-f][0-9a-f][0-9a-f][0-9a-f][0-9a-f]-*.zip"
    ):
        if "Export" in file.name:
            print(f"  Moving: {file.name}")
            shutil.move(str(file), str(NOTION_DIR / file.name))
            notion_count += 1

    if notion_count == 0:
        print("  ℹ️  No Notion export files found")
    else:
        print(f"  ✅ Organized {notion_count} Notion export files to: {NOTION_DIR}")

    print("")
    print("✅ Cleanup complete!")
    print("")
    print("📊 Summary:")
    print(f"   - Ollama duplicates removed: {ollama_removed}")
    print(f"   - Notion exports organized: {notion_count}")
    print(f"   - Backup location: {BACKUP_DIR}")
    print("")
    print("⚠️  Review the backup directory before permanently deleting:")
    print(f"   ls -lh {BACKUP_DIR}")


try:
        main()
except KeyboardInterrupt:
    logger.info("Execution interrupted by user")
    sys.exit(1)
except Exception as e:
    logger.error(f"An error occurred: {e}", exc_info=True)
    sys.exit(1)