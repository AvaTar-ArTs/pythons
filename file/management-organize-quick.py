"""
File Management Organize Quick 2

This module provides functionality for file management organize quick 2.

Author: Auto-generated
Date: 2025-11-01
"""

import logging

logger = logging.getLogger(__name__)

#!/usr/bin/env python3
"""
Quick Categorization Tool for Markdown Files
Move files into organized folders based on content analysis
"""

import os
import shutil
from pathlib import Path
import re


class QuickCategorizer:
    def __init__(self, directory_path):
        """__init__ function."""

        self.directory_path = Path(directory_path)
        self.categories = {
            "01_business_strategy": [],
            "02_ai_automation": [],
            "03_technical_docs": [],
            "04_creative_projects": [],
            "05_avatar_arts": [],
            "06_quantum_forge": [],
            "07_gptjunkie": [],
            "08_tutorials": [],
            "09_templates": [],
            "10_general": [],
        }

    def categorize_file(self, filename, content):
        """Categorize a file based on filename and content"""
        filename_lower = filename.lower()
        content_lower = content.lower()

        # Business Strategy
        if any(
            word in filename_lower
            for word in ["strategy", "brand", "seo", "analytics", "domain", "business", "marketing"]
        ):
            return "01_business_strategy"
        if any(word in content_lower for word in ["business strategy", "seo", "marketing", "brand", "analytics"]):
            return "01_business_strategy"

        # AI & Automation
        if any(word in filename_lower for word in ["ai", "automation", "python", "script", "gpt", "machine learning"]):
            return "02_ai_automation"
        if any(
            word in content_lower
            for word in ["artificial intelligence", "automation", "python", "ai", "machine learning"]
        ):
            return "02_ai_automation"

        # Technical Documentation
        if any(word in filename_lower for word in ["api", "code", "technical", "analysis", "script", "function"]):
            return "03_technical_docs"
        if any(word in content_lower for word in ["api", "code", "function", "class", "import", "technical"]):
            return "03_technical_docs"

        # Avatar Arts
        if any(word in filename_lower for word in ["avatar", "arts", "music", "creative", "art"]):
            return "05_avatar_arts"
        if any(word in content_lower for word in ["avatar arts", "music", "creative", "art", "visual"]):
            return "05_avatar_arts"

        # Quantum Forge Labs
        if any(word in filename_lower for word in ["quantum", "forge", "labs"]):
            return "06_quantum_forge"
        if any(word in content_lower for word in ["quantum", "forge labs", "quantumforge"]):
            return "06_quantum_forge"

        # GPTJunkie
        if any(word in filename_lower for word in ["gpt", "junkie"]):
            return "07_gptjunkie"
        if any(word in content_lower for word in ["gptjunkie", "gpt junkie"]):
            return "07_gptjunkie"

        # Tutorials & Guides
        if any(word in filename_lower for word in ["guide", "tutorial", "how", "setup", "course", "learn"]):
            return "08_tutorials"
        if any(word in content_lower for word in ["tutorial", "guide", "how to", "step by step", "learn"]):
            return "08_tutorials"

        # Templates
        if any(word in filename_lower for word in ["template", "refund", "policy", "terms"]):
            return "09_templates"

        # Default
        return "10_general"

    def create_category_folders(self):
        """Create category folders if they don't exist"""
        for category in self.categories.keys():
            folder_path = self.directory_path / category
            folder_path.mkdir(exist_ok=True)
            logger.info(f"📁 Created folder: {category}")

    def organize_files(self, dry_run=True):
        """Organize files into categories"""
        logger.info(f"🔍 Scanning {self.directory_path} for markdown files...")

        md_files = list(self.directory_path.glob("*.md"))
        logger.info(f"Found {len(md_files)} markdown files")

        # Create category folders
        self.create_category_folders()

        for file_path in md_files:
            try:
                # Read file content
                with open(file_path, "r", encoding="utf-8") as f:
                    content = f.read()

                # Categorize file
                category = self.categorize_file(file_path.name, content)

                # Add to category list
                self.categories[category].append(file_path.name)

                if not dry_run:
                    # Move file to category folder
                    dest_path = self.directory_path / category / file_path.name
                    shutil.move(str(file_path), str(dest_path))
                    logger.info(f"📄 Moved {file_path.name} → {category}/")
                else:
                    logger.info(f"📄 Would move {file_path.name} → {category}/")

            except Exception as e:
                logger.info(f"❌ Error processing {file_path.name}: {e}")

        # Print summary
        logger.info(Path("\n") + "=" * 50)
        logger.info("📊 ORGANIZATION SUMMARY")
        logger.info("=" * 50)
        for category, files in self.categories.items():
            if files:
                logger.info(f"{category}: {len(files)} files")
                for file in files[:3]:  # Show first 3 files
                    logger.info(f"  - {file}")
                if len(files) > 3:
                    logger.info(f"  ... and {len(files) - 3} more")
                print()

    def create_index_file(self):
        """Create an index file with all organized files"""
        index_content = "# Markdown Files Index\n\n"

        for category, files in self.categories.items():
            if files:
                index_content += f"## {category.replace('_', ' ').title()}\n\n"
                for file in files:
                    index_content += f"- [{file}]({category}/{file})\n"
                index_content += Path("\n")

        index_path = self.directory_path / "INDEX.md"
        with open(index_path, "w", encoding="utf-8") as f:
            f.write(index_content)

        logger.info(f"📄 Created index file: {index_path}")


def main():
    """main function."""

    import argparse

    parser = argparse.ArgumentParser(description="Organize markdown files into categories")
    parser.add_argument("--dry-run", action="store_true", help="Show what would be moved without actually moving files")
    parser.add_argument("--organize", action="store_true", help="Actually move the files")
    parser.add_argument("--index", action="store_true", help="Create an index file")

    args = parser.parse_args()

    categorizer = QuickCategorizer(".")

    if args.dry_run:
        logger.info("🔍 DRY RUN - No files will be moved")
        categorizer.organize_files(dry_run=True)
    elif args.organize:
        logger.info("🚀 ORGANIZING FILES - Files will be moved")
        categorizer.organize_files(dry_run=False)
        categorizer.create_index_file()
    elif args.index:
        logger.info("📄 Creating index file only")
        categorizer.organize_files(dry_run=True)
        categorizer.create_index_file()
    else:
        logger.info("Usage:")
        logger.info("  python quick_categorize.py --dry-run    # See what would be moved")
        logger.info("  python quick_categorize.py --organize   # Actually move files")
        logger.info("  python quick_categorize.py --index      # Create index file only")


if __name__ == "__main__":
    main()
