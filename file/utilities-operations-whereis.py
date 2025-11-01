"""
Utilities File Operations Whereis 1

This module provides functionality for utilities file operations whereis 1.

Author: Auto-generated
Date: 2025-11-01
"""

import logging

logger = logging.getLogger(__name__)

#!/usr/bin/env python3
"""
Quick Script Locator - whereis.py
Simple command-line tool to find Python scripts
Usage: python whereis.py <script_name>
"""

import sys
import os
from pathlib import Path


def find_script(script_name):
    """Find a script by name."""
    base_path = Path(Path("/Users/steven/Documents/python"))

    # Search for the script
    matches = list(base_path.rglob(f"*{script_name}*"))
    py_matches = [f for f in matches if f.suffix == ".py"]

    if not py_matches:
        logger.info(f"❌ No Python script found matching '{script_name}'")
        return

    logger.info(f"🔍 Found {len(py_matches)} script(s) matching '{script_name}':")
    logger.info("=" * 60)

    for i, script in enumerate(py_matches, 1):
        rel_path = script.relative_to(base_path)
        logger.info(f"\n{i}. {script.name}")
        logger.info(f"   📁 Location: {rel_path}")
        logger.info(f"   🔗 Full path: {script}")

        # Show category context
        path_parts = rel_path.parts
        if len(path_parts) >= 2:
            category = path_parts[0]
            subcategory = path_parts[1] if len(path_parts) > 1 else "root"
            logger.info(f"   📂 Category: {category}/{subcategory}")


def show_categories():
    """Show all categories and their contents."""
    base_path = Path(Path("/Users/steven/Documents/python"))

    logger.info("📁 PYTHON SCRIPT CATEGORIES")
    logger.info("=" * 40)

    for category_dir in sorted(base_path.glob("[0-9]*")):
        if category_dir.is_dir():
            py_files = list(category_dir.rglob("*.py"))
            logger.info(f"\n{category_dir.name}/ ({len(py_files)} scripts)")

            # Show subcategories
            for subdir in sorted(category_dir.iterdir()):
                if subdir.is_dir():
                    sub_py_files = list(subdir.rglob("*.py"))
                    if sub_py_files:
                        logger.info(f"  📂 {subdir.name}/ ({len(sub_py_files)} scripts)")

                        # Show first 5 scripts as examples
                        for script in sorted(sub_py_files)[:5]:
                            logger.info(f"    📄 {script.name}")

                        if len(sub_py_files) > 5:
                            logger.info(f"    ... and {len(sub_py_files) - 5} more")


def main():
    """Main function."""
    if len(sys.argv) < 2:
        logger.info("🐍 Python Script Locator")
        logger.info("=" * 30)
        logger.info("Usage:")
        logger.info("  python whereis.py <script_name>     - Find specific script")
        logger.info("  python whereis.py --categories      - Show all categories")
        logger.info("  python whereis.py --help            - Show this help")
        return

    command = sys.argv[1]

    if command == "--help":
        logger.info("🐍 Python Script Locator")
        logger.info("=" * 30)
        logger.info("Usage:")
        logger.info("  python whereis.py <script_name>     - Find specific script")
        logger.info("  python whereis.py --categories      - Show all categories")
        logger.info("  python whereis.py --help            - Show this help")
        print()
        logger.info("Examples:")
        logger.info("  python whereis.py analyze")
        logger.info("  python whereis.py transcription")
        logger.info("  python whereis.py youtube")
        logger.info("  python whereis.py convert")
    elif command == "--categories":
        show_categories()
    else:
        find_script(command)


if __name__ == "__main__":
    main()
