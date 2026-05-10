#!/usr/bin/env python3
"""
Script to merge multiple export directories into a single PasTe-Export directory
"""

import os
import shutil
from pathlib import Path
import sys


def merge_directories():
    """Merge all specified directories into the PasTe-Export directory"""
    
    # Source directories to merge
    source_dirs = [
        "/Users/steven/Documents/cli-tools",
        "/Users/steven/Documents/enhanced-clipboard-tagged", 
        "/Users/steven/Documents/enhanced-paste-export",
        "/Users/steven/Documents/fresh-enhanced-export",
        "/Users/steven/Documents/md",
        "/Users/steven/Documents/paste-clipboard-export",
        "/Users/steven/Documents/paste-clipboard-FULL-export",
        "/Users/steven/Documents/pdf",
        "/Users/steven/Documents/png",
        "/Users/steven/Documents/Snippets",
        "/Users/steven/Documents/svg",
        "/Users/steven/Documents/txt",
        "/Users/steven/Documents/web_templates"
    ]
    
    # Target directory
    target_dir = Path("/Users/steven/Documents/PasTe-Export")
    
    # Create target directory if it doesn't exist
    target_dir.mkdir(exist_ok=True)
    
    print(f"Merging directories into: {target_dir}")
    print("="*60)
    
    for source_path in source_dirs:
        source = Path(source_path)
        
        if not source.exists():
            print(f"⚠️  Source directory does not exist: {source}")
            continue
            
        if not source.is_dir():
            print(f"⚠️  Source path is not a directory: {source}")
            continue
            
        # Get directory name for subfolder creation
        dir_name = source.name
        
        # Create subdirectory in target
        target_subdir = target_dir / dir_name
        target_subdir.mkdir(exist_ok=True)
        
        print(f"Processing: {source} -> {target_subdir}")
        
        # Copy all contents from source to target subdirectory
        items_copied = 0
        for item in source.iterdir():
            target_item = target_subdir / item.name
            
            try:
                if item.is_file():
                    shutil.copy2(item, target_item)
                    items_copied += 1
                elif item.is_dir():
                    if target_item.exists():
                        # If directory exists, merge contents
                        merge_directory_contents(item, target_item)
                    else:
                        shutil.copytree(item, target_item)
                    items_copied += 1
            except Exception as e:
                print(f"   ⚠️  Failed to copy {item}: {e}")
        
        print(f"   ✅ Copied {items_copied} items to {target_subdir}")
    
    print("="*60)
    print(f"✅ Merge completed! All directories merged into {target_dir}")
    
    # Show final structure
    print("\nFinal directory structure:")
    for item in sorted(target_dir.iterdir()):
        if item.is_dir():
            item_count = len(list(item.iterdir()))
            print(f"  📁 {item.name}/ ({item_count} items)")
        else:
            print(f"  📄 {item.name}")


def merge_directory_contents(source_dir, target_dir):
    """Recursively merge contents of source directory into target directory"""
    for item in source_dir.iterdir():
        target_item = target_dir / item.name
        
        if item.is_file():
            shutil.copy2(item, target_item)
        elif item.is_dir():
            if not target_item.exists():
                target_item.mkdir()
            merge_directory_contents(item, target_item)


def main():
    print("📋 Merging Export Directories")
    print("This script will merge the following directories into PasTe-Export:")
    print("- cli-tools")
    print("- enhanced-clipboard-tagged") 
    print("- enhanced-paste-export")
    print("- fresh-enhanced-export")
    print("- md")
    print("- paste-clipboard-export")
    print("- paste-clipboard-FULL-export")
    print("- pdf")
    print("- png")
    print("- Snippets")
    print("- svg")
    print("- txt")
    print("- web_templates")
    print()
    
    response = input("Continue? (y/N): ")
    if response.lower() != 'y':
        print("Cancelled.")
        return
    
    merge_directories()


if __name__ == "__main__":
    main()