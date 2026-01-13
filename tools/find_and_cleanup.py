#!/usr/bin/env python3
"""
Find and cleanup Ollama duplicates and Notion exports
Searches in Archives and parent Documents directory
"""
import os
import shutil
from pathlib import Path
from datetime import datetime

ARCHIVES_DIR = Path("/Users/steven/Documents/Archives")
DOCUMENTS_DIR = Path("/Users/steven/Documents")
BACKUP_DIR = ARCHIVES_DIR / "misc-archives" / f"cleanup-backup-{datetime.now().strftime('%Y%m%d_%H%M%S')}"
NOTION_DIR = ARCHIVES_DIR / "misc-archives" / "notion-exports"

def find_files(directory, pattern):
    """Find files matching pattern"""
    files = []
    for path in directory.rglob(pattern):
        if path.is_file() and path.parent == directory:  # Only top-level
            files.append(path)
    return files

def main():
    print("🔍 Searching for files to cleanup...")
    print("")
    
    # Create directories
    BACKUP_DIR.mkdir(parents=True, exist_ok=True)
    NOTION_DIR.mkdir(parents=True, exist_ok=True)
    
    # Search in both Archives and Documents
    search_dirs = [ARCHIVES_DIR, DOCUMENTS_DIR]
    
    # 1. Find Ollama files
    print("📦 Searching for Ollama config files...")
    ollama_files = []
    for search_dir in search_dirs:
        ollama_files.extend(find_files(search_dir, "ollama*.zip"))
    
    KEEP_OLLAMA = "ollama-setup-kit-Intel-macOS.zip"
    ollama_removed = 0
    
    for file in ollama_files:
        if file.name != KEEP_OLLAMA:
            print(f"  Moving to backup: {file.name} (from {file.parent})")
            shutil.move(str(file), str(BACKUP_DIR / file.name))
            ollama_removed += 1
        else:
            print(f"  ✅ Keeping: {file.name} (most recent/specific)")
    
    if ollama_removed == 0:
        print("  ℹ️  No Ollama duplicates found or already cleaned")
    else:
        print(f"  ✅ Removed {ollama_removed} Ollama config duplicates")
    
    # 2. Find Notion exports
    print("")
    print("📦 Searching for Notion export files...")
    export_files = []
    for search_dir in search_dirs:
        # Pattern 1: *Export*.zip
        export_files.extend(find_files(search_dir, "*Export*.zip"))
        # Pattern 2: UUID_Export*.zip (8 hex chars, dash, then Export)
        for file in search_dir.glob("[0-9a-f][0-9a-f][0-9a-f][0-9a-f][0-9a-f][0-9a-f][0-9a-f][0-9a-f]-*.zip"):
            if file.is_file() and "Export" in file.name and file.parent == search_dir:
                export_files.append(file)
    
    # Remove duplicates
    export_files = list(set(export_files))
    notion_count = 0
    
    for file in export_files:
        print(f"  Moving: {file.name} (from {file.parent})")
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
    if ollama_removed > 0 or notion_count > 0:
        print("⚠️  Review the backup directory before permanently deleting:")
        print(f"   ls -lh {BACKUP_DIR}")
        print(f"   ls -lh {NOTION_DIR}")

if __name__ == "__main__":
    main()
