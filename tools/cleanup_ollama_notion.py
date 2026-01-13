#!/usr/bin/env python3
"""
Cleanup Ollama duplicates and organize Notion exports
Searches Archives and Documents directories
"""
import os
import shutil
from pathlib import Path
from datetime import datetime

# Directories to search
SEARCH_DIRS = [
    Path("/Users/steven/Documents/Archives"),
    Path("/Users/steven/Documents"),
]

# Backup and organization directories
ARCHIVES = Path("/Users/steven/Documents/Archives")
BACKUP_DIR = ARCHIVES / "misc-archives" / f"cleanup-backup-{datetime.now().strftime('%Y%m%d_%H%M%S')}"
NOTION_DIR = ARCHIVES / "misc-archives" / "notion-exports"

def main():
    print("🧹 Ollama & Notion Cleanup")
    print("=" * 60)
    print()
    
    # Create directories
    BACKUP_DIR.mkdir(parents=True, exist_ok=True)
    NOTION_DIR.mkdir(parents=True, exist_ok=True)
    
    # 1. Ollama files
    print("📦 Processing Ollama config files...")
    KEEP_OLLAMA = "ollama-setup-kit-Intel-macOS.zip"
    ollama_files = []
    ollama_removed = 0
    
    for search_dir in SEARCH_DIRS:
        if search_dir.exists():
            # Find ollama*.zip files in top-level only
            for file in search_dir.glob("ollama*.zip"):
                if file.is_file() and file.parent == search_dir:
                    ollama_files.append(file)
    
    for file in ollama_files:
        if file.name != KEEP_OLLAMA:
            print(f"  📦 Moving to backup: {file.name}")
            print(f"     From: {file.parent}")
            try:
                shutil.move(str(file), str(BACKUP_DIR / file.name))
                ollama_removed += 1
            except Exception as e:
                print(f"     ⚠️  Error: {e}")
        else:
            print(f"  ✅ Keeping: {file.name}")
    
    if ollama_removed == 0 and len(ollama_files) == 0:
        print("  ℹ️  No Ollama files found")
    elif ollama_removed == 0:
        print(f"  ℹ️  Only keeping file found: {KEEP_OLLAMA}")
    else:
        print(f"  ✅ Removed {ollama_removed} Ollama duplicates")
    
    # 2. Notion exports
    print()
    print("📦 Processing Notion export files...")
    export_files = []
    
    for search_dir in SEARCH_DIRS:
        if search_dir.exists():
            # Pattern 1: *Export*.zip
            for file in search_dir.glob("*Export*.zip"):
                if file.is_file() and file.parent == search_dir:
                    export_files.append(file)
            
            # Pattern 2: UUID_Export*.zip (8 hex chars)
            for file in search_dir.glob("[0-9a-f][0-9a-f][0-9a-f][0-9a-f][0-9a-f][0-9a-f][0-9a-f][0-9a-f]-*.zip"):
                if file.is_file() and "Export" in file.name and file.parent == search_dir:
                    export_files.append(file)
    
    # Remove duplicates
    export_files = list(set(export_files))
    notion_count = 0
    
    for file in export_files:
        print(f"  📦 Moving: {file.name}")
        print(f"     From: {file.parent}")
        try:
            shutil.move(str(file), str(NOTION_DIR / file.name))
            notion_count += 1
        except Exception as e:
            print(f"     ⚠️  Error: {e}")
    
    if notion_count == 0:
        print("  ℹ️  No Notion export files found")
    else:
        print(f"  ✅ Organized {notion_count} Notion export files")
    
    # Summary
    print()
    print("=" * 60)
    print("✅ CLEANUP COMPLETE")
    print("=" * 60)
    print(f"📊 Summary:")
    print(f"   - Ollama duplicates removed: {ollama_removed}")
    print(f"   - Notion exports organized: {notion_count}")
    print(f"   - Backup location: {BACKUP_DIR}")
    print(f"   - Notion exports: {NOTION_DIR}")
    print()
    if ollama_removed > 0 or notion_count > 0:
        print("⚠️  Files backed up before removal. Review:")
        print(f"   ls -lh {BACKUP_DIR}")
        print(f"   ls -lh {NOTION_DIR}")

if __name__ == "__main__":
    main()
