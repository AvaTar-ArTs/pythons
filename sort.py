"""
Intelligent Sort

This module provides functionality for intelligent sort.

Author: Auto-generated
Date: 2025-11-01
"""

import logging

logger = logging.getLogger(__name__)


# Constants
CONSTANT_1024 = 1024

#!/usr/bin/env python3
"""
Final Intelligent Sort
Use advanced content-awareness to sort all remaining items into 4 main categories
"""

import ast
import shutil
from pathlib import Path
from collections import defaultdict


class FinalIntelligentSorter:
    """Intelligently sort all remaining content into main 4 categories"""

    def __init__(self, base_dir: Path):
        """__init__ function."""

        self.base_dir = base_dir
        self.moves = []

    def analyze_python_file(self, file_path: Path):
        """Analyze Python file for categorization"""
        try:
            content = file_path.read_text(encoding="utf-8", errors="ignore")
        except (OSError, IOError, FileNotFoundError):
            return "DATA_UTILITIES"

        content_lower = content.lower()

        # AI/ML detection
        ai_keywords = [
            "openai",
            "anthropic",
            "claude",
            "gpt",
            "llm",
            "ai",
            "agent",
            "chat",
            "model",
        ]
        if any(kw in content_lower for kw in ai_keywords):
            return "AI_CONTENT"

        # Bot/Automation detection
        bot_keywords = [
            "selenium",
            "playwright",
            "bot",
            "automation",
            "scrape",
            "instagram",
            "reddit",
            "twitter",
        ]
        if any(kw in content_lower for kw in bot_keywords):
            return "AUTOMATION_BOTS"

        # Media detection
        media_keywords = [
            "video",
            "audio",
            "image",
            "gallery",
            "mp4",
            "mp3",
            "jpg",
            "png",
            "moviepy",
            "pydub",
            "pillow",
        ]
        if any(kw in content_lower for kw in media_keywords):
            return "MEDIA_PROCESSING"

        # Default to data utilities
        return "DATA_UTILITIES"

    def analyze_directory(self, dir_path: Path):
        """Analyze directory contents to determine category"""

        # Count Python files by category
        category_counts = defaultdict(int)

        for py_file in dir_path.rglob("*.py"):
            if "__pycache__" in str(py_file):
                continue
            category = self.analyze_python_file(py_file)
            category_counts[category] += 1

        # Return most common category, or DATA_UTILITIES if no Python files
        if category_counts:
            return max(category_counts.items(), key=lambda x: x[1])[0]
        return "DATA_UTILITIES"

    def build_sort_plan(self):
        """Build intelligent sorting plan"""

        # Analysis artifacts → DATA_UTILITIES
        analysis_dir = self.base_dir / "analysis_artifacts"
        if analysis_dir.exists():
            self.moves.append(
                {
                    "source": analysis_dir,
                    "category": "DATA_UTILITIES/analysis_artifacts",
                    "type": "Analysis outputs & maps",
                    "reason": "Data analysis artifacts",
                }
            )

        # Archived items → Analyze and distribute
        archived_dir = self.base_dir / "archived_items"
        if archived_dir.exists():
            # Check experimental subdirs
            experimental_dir = archived_dir / "experimental"
            if experimental_dir.exists():
                # Libraries go to DATA_UTILITIES
                libraries_dir = experimental_dir / "libraries"
                if libraries_dir.exists():
                    self.moves.append(
                        {
                            "source": libraries_dir,
                            "category": "DATA_UTILITIES/external_libraries",
                            "type": "External libraries",
                            "reason": "Third-party code libraries",
                        }
                    )

        # Documentation → Keep but analyze subdirs
        doc_dir = self.base_dir / "documentation"
        if doc_dir.exists():
            # Web resources (HTML files) can stay in documentation or move based on content
            # For now, keep documentation as is but could analyze further
            pass

        # Notebooks → AI_CONTENT (Jupyter notebooks are typically for ML/data science)
        notebooks_dir = self.base_dir / "notebooks"
        if notebooks_dir.exists():
            self.moves.append(
                {
                    "source": notebooks_dir,
                    "category": "AI_CONTENT/notebooks",
                    "type": "Jupyter notebooks",
                    "reason": "ML/Data science notebooks",
                }
            )

        # Old versions → DATA_UTILITIES
        old_versions_dir = self.base_dir / "old_versions"
        if old_versions_dir.exists():
            self.moves.append(
                {
                    "source": old_versions_dir,
                    "category": "DATA_UTILITIES/old_versions",
                    "type": "Old file versions",
                    "reason": "Version history",
                }
            )

        # Reorganization tools → DATA_UTILITIES
        reorg_dir = self.base_dir / "reorganization_tools"
        if reorg_dir.exists():
            self.moves.append(
                {
                    "source": reorg_dir,
                    "category": "DATA_UTILITIES/organization_tools",
                    "type": "Organization scripts",
                    "reason": "File organization utilities",
                }
            )

        # Setup tools → DATA_UTILITIES
        setup_dir = self.base_dir / "setup_tools"
        if setup_dir.exists():
            self.moves.append(
                {
                    "source": setup_dir,
                    "category": "DATA_UTILITIES/setup_tools",
                    "type": "Setup scripts",
                    "reason": "Environment setup utilities",
                }
            )

        # Test data → DATA_UTILITIES
        test_data_dir = self.base_dir / "test_data"
        if test_data_dir.exists():
            self.moves.append(
                {
                    "source": test_data_dir,
                    "category": "DATA_UTILITIES/test_data",
                    "type": "Test data",
                    "reason": "Testing resources",
                }
            )

        # Testing → Analyze content to categorize
        testing_dir = self.base_dir / "testing"
        if testing_dir.exists():
            # Analyze subdirectories
            for subdir in testing_dir.iterdir():
                if subdir.is_dir() and not subdir.name.startswith("."):
                    category = self.analyze_directory(subdir)
                    self.moves.append(
                        {
                            "source": subdir,
                            "category": f"{category}/testing/{subdir.name}",
                            "type": f"Test suite: {subdir.name}",
                            "reason": f"Tests for {category.lower()} functionality",
                        }
                    )

            # Move loose test files
            for test_file in testing_dir.glob("*.py"):
                category = self.analyze_python_file(test_file)
                self.moves.append(
                    {
                        "source": test_file,
                        "category": f"{category}/testing/{test_file.name}",
                        "type": "Test file",
                        "reason": f"Test for {category.lower()}",
                    }
                )

        # Utilities → Analyze and distribute
        utilities_dir = self.base_dir / "utilities"
        if utilities_dir.exists():
            for util_file in utilities_dir.rglob("*.py"):
                if "__pycache__" in str(util_file):
                    continue
                category = self.analyze_python_file(util_file)
                rel_path = util_file.relative_to(utilities_dir)
                self.moves.append(
                    {
                        "source": util_file,
                        "category": f"{category}/utilities/{rel_path}",
                        "type": "Utility script",
                        "reason": f"Utility for {category.lower()}",
                    }
                )

        # README.md → Keep in root (documentation)
        # requirements.txt → Keep in root (dependencies)
        # These stay at root level

    def execute(self, dry_run=True):
        """Execute intelligent sorting"""

        logger.info("=" * 70)
        logger.info(f"🧠 FINAL INTELLIGENT SORT {'(DRY RUN)' if dry_run else '(LIVE)'}")
        logger.info("=" * 70)
        print()

        self.build_sort_plan()

        if not self.moves:
            logger.info("✅ Nothing to sort!")
            return

        logger.info(f"📦 Found {len(self.moves)} items to categorize")
        print()

        # Group by category
        by_category = defaultdict(list)
        for move in self.moves:
            main_cat = move["category"].split("/")[0]
            by_category[main_cat].append(move)

        moved_count = 0
        error_count = 0

        for main_cat, items in sorted(by_category.items()):
            logger.info(f"📂 {main_cat}/ ({len(items)} items)")

            for move in items:
                source = move["source"]
                target = self.base_dir / move["category"]

                # Get size info
                try:
                    if source.is_file():
                        size_kb = source.stat().st_size / CONSTANT_1024
                        size_str = f"{size_kb:.1f} KB"
                    else:
                        file_count = len(list(source.rglob("*")))
                        size_str = f"{file_count} items"
                except (OSError, IOError, FileNotFoundError):
                    size_str = "unknown"

                rel_source = (
                    source.relative_to(self.base_dir)
                    if source.is_relative_to(self.base_dir)
                    else source.name
                )

                if dry_run:
                    logger.info(f"   [DRY RUN] {rel_source}")
                    logger.info(f"           → {move['category']} ({size_str})")
                    logger.info(f"              {move['reason']}")
                else:
                    # Create target parent
                    target.parent.mkdir(parents=True, exist_ok=True)

                    # Handle conflicts
                    if target.exists():
                        from datetime import datetime

                        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                        if source.is_file():
                            new_name = f"{source.stem}_{timestamp}{source.suffix}"
                        else:
                            new_name = f"{source.name}_{timestamp}"
                        target = target.parent / new_name

                    try:
                        shutil.move(str(source), str(target))
                        logger.info(f"   ✅ {rel_source}")
                        logger.info(
                            f"      → {target.relative_to(self.base_dir)} ({size_str})"
                        )
                        moved_count += 1
                    except Exception as e:
                        logger.info(f"   ❌ {rel_source}")
                        logger.info(f"      ERROR: {str(e)[:50]}")
                        error_count += 1

            print()

        logger.info("=" * 70)
        logger.info(f"{'Simulation' if dry_run else 'Sort'} complete!")
        logger.info(
            f"   Items {'would be' if dry_run else ''} sorted: {moved_count if not dry_run else len(self.moves)}"
        )
        if error_count > 0:
            logger.info(f"   Errors: {error_count}")
        logger.info("=" * 70)

        if not dry_run:
            # Clean up empty directories
            print()
            logger.info("🧹 Cleaning up empty directories...")
            for dir_name in [
                "testing",
                "utilities",
                "archived_items",
                "analysis_artifacts",
                "old_versions",
                "reorganization_tools",
                "setup_tools",
                "test_data",
                "notebooks",
            ]:
                dir_path = self.base_dir / dir_name
                if dir_path.exists():
                    try:
                        # Remove empty subdirs
                        for item in sorted(dir_path.rglob("*"), reverse=True):
                            if item.is_dir() and not any(item.iterdir()):
                                item.rmdir()

                        # Remove main dir if empty
                        if not any(dir_path.iterdir()):
                            dir_path.rmdir()
                            logger.info(f"   ✓ Removed empty: {dir_name}/")
                    except (ValueError, TypeError):
                        pass

            print()
            logger.info("✨ Final intelligent sort complete!")
            print()
            logger.info("📊 Final structure:")
            logger.info("   ├── AI_CONTENT/")
            logger.info("   ├── AUTOMATION_BOTS/")
            logger.info("   ├── DATA_UTILITIES/")
            logger.info("   ├── MEDIA_PROCESSING/")
            logger.info("   ├── documentation/")
            logger.info("   ├── README.md")
            logger.info("   └── requirements.txt")

        if dry_run:
            logger.info("\n💡 To execute, run:")
            logger.info("   python3 final_intelligent_sort.py --execute")


def main():
    """main function."""

    import sys

    base_dir = Path(Path(str(Path.home()) + "/Documents/python"))
    dry_run = "--execute" not in sys.argv

    sorter = FinalIntelligentSorter(base_dir)
    sorter.execute(dry_run=dry_run)


if __name__ == "__main__":
    main()
