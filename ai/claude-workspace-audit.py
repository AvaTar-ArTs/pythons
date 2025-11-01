"""
Claude Workspace Audit

This module provides functionality for claude workspace audit.

Author: Auto-generated
Date: 2025-11-01
"""

import logging

logger = logging.getLogger(__name__)


# Constants
CONSTANT_661 = 661
CONSTANT_1024 = 1024

#!/usr/bin/env python3
"""
Comprehensive Analysis of Claude Directory
Analyzes structure, duplicates, usage patterns, and organization
"""

import os
import json
import hashlib
from pathlib import Path
from collections import defaultdict
from datetime import datetime

CLAUDE_DIR = Path("/Users/steven/Documents/claude")


def get_file_hash(filepath):
    """Get MD5 hash of file"""
    try:
        with open(filepath, "rb") as f:
            return hashlib.md5(f.read()).hexdigest()
    except (OSError, IOError, FileNotFoundError):
        return None


def analyze_directory_structure():
    """Analyze directory structure and file types"""
    logger.info("=" * 80)
    logger.info("CLAUDE DIRECTORY ANALYSIS")
    logger.info("=" * 80)
    logger.info(f"Location: {CLAUDE_DIR}\n")

    if not CLAUDE_DIR.exists():
        logger.info("Directory not found!")
        return

    # Get all subdirectories
    subdirs = [d for d in CLAUDE_DIR.iterdir() if d.is_dir() and not d.name.startswith(".")]

    logger.info(f"📁 Found {len(subdirs)} main directories\n")

    # Analyze each subdirectory
    dir_stats = []

    for subdir in sorted(subdirs):
        files = list(subdir.rglob("*"))
        file_count = len([f for f in files if f.is_file()])
        dir_count = len([f for f in files if f.is_dir()])

        # Get total size
        total_size = sum(f.stat().st_size for f in files if f.is_file())
        size_mb = total_size / (CONSTANT_1024 * CONSTANT_1024)

        # Get file types
        extensions = defaultdict(int)
        for f in files:
            if f.is_file():
                ext = f.suffix.lower() or "no-ext"
                extensions[ext] += 1

        # Get most recent file
        file_times = [f.stat().st_mtime for f in files if f.is_file()]
        most_recent = max(file_times) if file_times else 0
        most_recent_date = datetime.fromtimestamp(most_recent).strftime("%Y-%m-%d") if most_recent else "N/A"

        dir_stats.append(
            {
                "name": subdir.name,
                "path": subdir,
                "files": file_count,
                "dirs": dir_count,
                "size_mb": size_mb,
                "extensions": dict(extensions),
                "last_modified": most_recent_date,
            }
        )

    # Print directory summary
    logger.info("📊 DIRECTORY SUMMARY")
    logger.info("-" * 80)

    total_files = sum(d["files"] for d in dir_stats)
    total_size = sum(d["size_mb"] for d in dir_stats)

    logger.info(f"Total Files: {total_files}")
    logger.info(f"Total Size: {total_size:.2f} MB")
    print()

    for stat in sorted(dir_stats, key=lambda x: -x["size_mb"]):
        logger.info(f"\n📁 {stat['name']}")
        logger.info(f"   Files: {stat['files']} | Dirs: {stat['dirs']} | Size: {stat['size_mb']:.2f} MB")
        logger.info(f"   Last Modified: {stat['last_modified']}")

        # Show top file types
        top_types = sorted(stat["extensions"].items(), key=lambda x: -x[1])[:5]
        if top_types:
            types_str = ", ".join([f"{ext}: {count}" for ext, count in top_types])
            logger.info(f"   Types: {types_str}")

    return dir_stats


def identify_duplicates():
    """Find duplicate files by hash"""
    logger.info(Path("\n") + "=" * 80)
    logger.info("🔍 DUPLICATE FILE ANALYSIS")
    logger.info("=" * 80)

    file_hashes = defaultdict(list)

    # Calculate hashes for all files
    all_files = list(CLAUDE_DIR.rglob("*"))
    files_to_check = [f for f in all_files if f.is_file() and not f.name.startswith(".")]

    logger.info(f"Checking {len(files_to_check)} files for duplicates...\n")

    for filepath in files_to_check:
        file_hash = get_file_hash(filepath)
        if file_hash:
            file_hashes[file_hash].append(filepath)

    # Find duplicates
    duplicates = {h: files for h, files in file_hashes.items() if len(files) > 1}

    if duplicates:
        logger.info(f"Found {len(duplicates)} sets of duplicate files:\n")

        total_wasted = 0
        for file_hash, files in sorted(duplicates.items(), key=lambda x: -x[1][0].stat().st_size):
            size = files[0].stat().st_size
            wasted = size * (len(files) - 1)
            total_wasted += wasted

            logger.info(f"📄 {files[0].name} ({size / CONSTANT_1024:.1f} KB) - {len(files)} copies")
            for f in files:
                rel_path = f.relative_to(CLAUDE_DIR)
                logger.info(f"   → {rel_path}")
            logger.info(f"   Wasted: {wasted / CONSTANT_1024:.1f} KB\n")

        logger.info(f"💾 Total wasted space: {total_wasted / (CONSTANT_1024 * CONSTANT_1024):.2f} MB")
    else:
        logger.info("✅ No duplicate files found!")

    return duplicates


def analyze_file_types():
    """Analyze file type distribution"""
    logger.info(Path("\n") + "=" * 80)
    logger.info("📋 FILE TYPE ANALYSIS")
    logger.info("=" * 80)

    extensions = defaultdict(lambda: {"count": 0, "size": 0})

    all_files = [f for f in CLAUDE_DIR.rglob("*") if f.is_file() and not f.name.startswith(".")]

    for filepath in all_files:
        ext = filepath.suffix.lower() or "no-extension"
        size = filepath.stat().st_size

        extensions[ext]["count"] += 1
        extensions[ext]["size"] += size

    logger.info(f"\nFound {len(extensions)} different file types:\n")

    # Sort by count
    sorted_exts = sorted(extensions.items(), key=lambda x: -x[1]["count"])

    logger.info("Top file types by count:")
    for ext, stats in sorted_exts[:15]:
        count = stats["count"]
        size_mb = stats["size"] / (CONSTANT_1024 * CONSTANT_1024)
        avg_size_kb = (stats["size"] / count) / CONSTANT_1024
        logger.info(f"  {ext:20s} {count:4d} files  {size_mb:8.2f} MB  (avg: {avg_size_kb:.1f} KB)")

    return extensions


def analyze_zip_files():
    """Analyze ZIP files that might need extraction"""
    logger.info(Path("\n") + "=" * 80)
    logger.info("📦 ZIP FILE ANALYSIS")
    logger.info("=" * 80)

    zip_files = list(CLAUDE_DIR.glob("*.zip"))

    if not zip_files:
        logger.info("\n✅ No ZIP files in root directory")
        return

    logger.info(f"\nFound {len(zip_files)} ZIP files:\n")

    for zip_file in zip_files:
        size = zip_file.stat().st_size / (CONSTANT_1024 * CONSTANT_1024)

        # Check if there's a corresponding directory
        base_name = zip_file.stem
        corresponding_dirs = [d for d in CLAUDE_DIR.iterdir() if d.is_dir() and base_name.lower() in d.name.lower()]

        status = "✅ EXTRACTED" if corresponding_dirs else "❌ NOT EXTRACTED"

        logger.info(f"{status} {zip_file.name} ({size:.2f} MB)")
        if corresponding_dirs:
            for d in corresponding_dirs:
                logger.info(f"         → {d.name}/")

    return zip_files


def identify_purposes():
    """Identify the purpose of each directory"""
    logger.info(Path("\n") + "=" * 80)
    logger.info("🎯 DIRECTORY PURPOSE ANALYSIS")
    logger.info("=" * 80)

    purposes = {
        "claude-code-action-main": {
            "type": "GitHub Action",
            "purpose": "CI/CD integration for Claude Code",
            "key_files": ["action.yml", ".github/workflows/"],
            "priority": "Medium",
            "notes": "Used for automating Claude Code in GitHub repos",
        },
        "claude-courses-master": {
            "type": "Educational",
            "purpose": "Prompt engineering courses and tutorials",
            "key_files": ["prompt_evaluations/", "courses/"],
            "priority": "High",
            "notes": "Learning materials - keep for reference",
        },
        "claude-quickstarts-main": {
            "type": "Demo/Tutorial",
            "purpose": "Quickstart guides and demos (computer use)",
            "key_files": ["computer-use-demo/", "README.md"],
            "priority": "Medium",
            "notes": "Examples and demos",
        },
        "claude-skills-main": {
            "type": "Skills/Plugins",
            "purpose": "Claude skills and capabilities",
            "key_files": ["skills/", "README.md"],
            "priority": "High",
            "notes": "Reusable skills for Claude Code",
        },
        "prompt-eng-interactive-tutorial-master": {
            "type": "Tutorial",
            "purpose": "Interactive prompt engineering tutorial",
            "key_files": ["notebooks/", "examples/"],
            "priority": "Medium",
            "notes": "Learning resource",
        },
        "config_files": {
            "type": "Configuration",
            "purpose": "JSON configuration files",
            "key_files": ["*.json"],
            "priority": "High",
            "notes": "May contain important settings",
        },
        "setup": {
            "type": "Scripts",
            "purpose": "Setup and installation scripts",
            "key_files": ["scripts/", "*.sh"],
            "priority": "High",
            "notes": "Setup automation",
        },
        "fix-macos": {
            "type": "Scripts",
            "purpose": "macOS-specific fixes and scripts",
            "key_files": ["*.sh"],
            "priority": "High",
            "notes": "Platform-specific utilities",
        },
    }

    print()
    for dir_name, info in purposes.items():
        dir_path = CLAUDE_DIR / dir_name
        exists = "✅" if dir_path.exists() else "❌"

        logger.info(f"\n{exists} {dir_name}")
        logger.info(f"   Type: {info['type']}")
        logger.info(f"   Purpose: {info['purpose']}")
        logger.info(f"   Priority: {info['priority']}")
        logger.info(f"   Notes: {info['notes']}")

    return purposes


def suggest_organization():
    """Suggest directory reorganization"""
    logger.info(Path("\n") + "=" * 80)
    logger.info("💡 ORGANIZATION SUGGESTIONS")
    logger.info("=" * 80)

    suggestions = [
        {
            "priority": "High",
            "action": "Delete ZIP files",
            "reason": "Already extracted - wasting CONSTANT_661 KB",
            "command": "rm /Users/steven/Documents/claude/*.zip",
        },
        {
            "priority": "High",
            "action": "Consolidate config files",
            "reason": "config_files/ should be moved to setup/ or renamed",
            "command": "mv config_files/ setup/configs/",
        },
        {
            "priority": "High",
            "action": "Organize scripts",
            "reason": "Multiple script directories (setup/, fix-macos/)",
            "command": "Consolidate into single scripts/ directory",
        },
        {
            "priority": "Medium",
            "action": "Create directory structure",
            "reason": "Better organization by purpose",
            "structure": """
            claude/
            ├── learning/          (courses, tutorials)
            ├── tools/            (quickstarts, actions)
            ├── skills/           (claude-skills-main)
            ├── scripts/          (setup, fix-macos)
            └── config/           (config_files)
            """,
        },
        {
            "priority": "Medium",
            "action": "Add README.md",
            "reason": "Document what each directory contains",
            "command": "Create main README.md with directory index",
        },
        {
            "priority": "Low",
            "action": "Archive old files",
            "reason": "Some files not modified since Oct 9",
            "command": "Move to archive/ if not actively used",
        },
    ]

    for suggestion in suggestions:
        priority_icon = (
            "🔴" if suggestion["priority"] == "High" else "🟡" if suggestion["priority"] == "Medium" else "🟢"
        )

        logger.info(f"\n{priority_icon} {suggestion['priority']} Priority:")
        logger.info(f"   Action: {suggestion['action']}")
        logger.info(f"   Reason: {suggestion['reason']}")

        if "command" in suggestion:
            logger.info(f"   Command: {suggestion['command']}")

        if "structure" in suggestion:
            logger.info(f"   Proposed:{suggestion['structure']}")

    return suggestions


def main():
    """main function."""

    # Run all analyses
    dir_stats = analyze_directory_structure()
    duplicates = identify_duplicates()
    file_types = analyze_file_types()
    zip_files = analyze_zip_files()
    purposes = identify_purposes()
    suggestions = suggest_organization()

    # Final summary
    logger.info(Path("\n") + "=" * 80)
    logger.info("📊 FINAL SUMMARY")
    logger.info("=" * 80)

    total_files = sum(stat["files"] for stat in dir_stats)
    total_size = sum(stat["size_mb"] for stat in dir_stats)

    print(
        f"""
Overview:
  • Total Directories: {len(dir_stats)}
  • Total Files: {total_files}
  • Total Size: {total_size:.2f} MB
  • Duplicate Sets: {len(duplicates) if duplicates else 0}
  • ZIP Files: {len(zip_files) if zip_files else 0}

Key Findings:
  • Directory structure is flat - could benefit from categorization
  • Multiple script directories exist (setup/, fix-macos/)
  • Config files are isolated in config_files/
  • Several GitHub repos (likely downloaded/cloned)
  • Mix of learning resources and tools

Recommendations:
  1. Delete extracted ZIP files (save ~CONSTANT_661 KB)
  2. Reorganize into logical categories (learning, tools, scripts, config)
  3. Create central README.md documenting directory purposes
  4. Consolidate script directories
  5. Consider moving to ~/claude/ for consistency with conversation system
    """
    )

    logger.info(Path("\n") + "=" * 80)


if __name__ == "__main__":
    main()
