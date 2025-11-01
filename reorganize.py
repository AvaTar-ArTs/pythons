"""
Reorganize

This module provides functionality for reorganize.

Author: Auto-generated
Date: 2025-11-01
"""

import logging

logger = logging.getLogger(__name__)

#!/usr/bin/env python3
"""
Reorganize to Exact Structure
Sort all content into the exact category structure with proper subcategories
"""

import ast
import shutil
from pathlib import Path
from collections import defaultdict


class ExactStructureReorganizer:
    """Reorganize to exact structure with specific subcategories"""

    def __init__(self, base_dir: Path):
        """__init__ function."""

        self.base_dir = base_dir
        self.moves = []

        # Define exact target structure
        self.structure = {
            "AUTOMATION_BOTS": {
                "weight": 0.35,
                "subcategories": {
                    "social_media_automation": [
                        "instagram",
                        "reddit",
                        "twitter",
                        "telegram",
                        "whatsapp",
                        "facebook",
                    ],
                    "youtube_reddit_content": [
                        "youtube",
                        "reddit",
                        "video_generator",
                        "content_maker",
                    ],
                    "bot_frameworks": [
                        "botty",
                        "selenium",
                        "playwright",
                        "automation_framework",
                    ],
                    "scrapers": ["scraper", "scrape", "crawler", "extract", "fetch"],
                },
            },
            "MEDIA_PROCESSING": {
                "weight": 0.25,
                "subcategories": {
                    "audio_video_conversion": [
                        "converter",
                        "ffmpeg",
                        "moviepy",
                        "transcode",
                        "encode",
                    ],
                    "image_upscaling": [
                        "upscale",
                        "enhance",
                        "super_resolution",
                        "enlarge",
                    ],
                    "gallery_generation": [
                        "gallery",
                        "album",
                        "slideshow",
                        "portfolio",
                    ],
                    "tts_generation": [
                        "text_to_speech",
                        "tts",
                        "voice",
                        "speech_synthesis",
                    ],
                },
            },
            "AI_CONTENT": {
                "weight": 0.20,
                "subcategories": {
                    "tts_engines": [
                        "tts",
                        "text_to_speech",
                        "voice_synthesis",
                        "speech",
                    ],
                    "image_generation": [
                        "image_gen",
                        "stable_diffusion",
                        "dalle",
                        "midjourney",
                        "ai_art",
                    ],
                    "prompt_engineering": [
                        "prompt",
                        "prompt_pipeline",
                        "prompt_optimization",
                    ],
                    "content_creation": [
                        "content_gen",
                        "article",
                        "blog",
                        "writer",
                        "generator",
                    ],
                },
            },
            "DATA_UTILITIES": {
                "weight": 0.15,
                "subcategories": {
                    "file_organization": [
                        "organizer",
                        "organize",
                        "sort",
                        "categorize",
                        "cleanup",
                    ],
                    "csv_processing": ["csv", "excel", "spreadsheet", "data_processor"],
                    "data_analysis": ["analyze", "analytics", "statistics", "metrics"],
                    "scrapers": ["download", "fetch", "retrieve", "web_scraper"],
                },
            },
            "documentation": {
                "weight": 0.05,
                "subcategories": {
                    "code_browsers": ["browser", "viewer", "explorer", "navigator"],
                    "tutorials": ["tutorial", "guide", "how_to", "example"],
                    "references": ["reference", "docs", "documentation", "wiki"],
                },
            },
        }

    def analyze_file_content(self, file_path: Path) -> dict:
        """Analyze file content for categorization"""
        try:
            content = file_path.read_text(encoding="utf-8", errors="ignore")
        except (OSError, IOError, FileNotFoundError):
            return {"keywords": set(), "imports": set()}

        content_lower = content.lower()
        keywords = set()
        imports = set()

        # Extract imports
        try:
            tree = ast.parse(content)
            for node in ast.walk(tree):
                if isinstance(node, ast.Import):
                    for alias in node.names:
                        imports.add(alias.name.split(".")[0])
                elif isinstance(node, ast.ImportFrom):
                    if node.module:
                        imports.add(node.module.split(".")[0])
        except (ImportError, ModuleNotFoundError):
            pass

        # Detect keywords from all subcategories
        for category, cat_data in self.structure.items():
            for subcat, keywords_list in cat_data["subcategories"].items():
                for keyword in keywords_list:
                    if keyword.replace("_", "").replace(
                        "-", ""
                    ) in content_lower.replace("_", "").replace("-", ""):
                        keywords.add(keyword)

        return {"keywords": keywords, "imports": imports}

    def categorize_item(self, item_path: Path) -> tuple:
        """Determine best category and subcategory for item"""

        # Analyze all Python files in item
        keyword_counts = defaultdict(lambda: defaultdict(int))

        if item_path.is_file() and item_path.suffix == ".py":
            analysis = self.analyze_file_content(item_path)
            # Count keyword matches for each category/subcategory
            for category, cat_data in self.structure.items():
                for subcat, keywords_list in cat_data["subcategories"].items():
                    for keyword in keywords_list:
                        if (
                            keyword in analysis["keywords"]
                            or keyword in analysis["imports"]
                        ):
                            keyword_counts[category][subcat] += 1

        elif item_path.is_dir():
            for py_file in item_path.rglob("*.py"):
                if "__pycache__" in str(py_file):
                    continue
                analysis = self.analyze_file_content(py_file)
                for category, cat_data in self.structure.items():
                    for subcat, keywords_list in cat_data["subcategories"].items():
                        for keyword in keywords_list:
                            if (
                                keyword in analysis["keywords"]
                                or keyword in analysis["imports"]
                            ):
                                keyword_counts[category][subcat] += 1

        # Find best match
        best_category = None
        best_subcat = None
        best_score = 0

        for category in keyword_counts:
            for subcat, score in keyword_counts[category].items():
                if score > best_score:
                    best_score = score
                    best_category = category
                    best_subcat = subcat

        # Fallback based on directory name
        if not best_category:
            item_name = item_path.name.lower()
            for category, cat_data in self.structure.items():
                for subcat, keywords_list in cat_data["subcategories"].items():
                    for keyword in keywords_list:
                        if keyword.replace("_", "") in item_name.replace(
                            "_", ""
                        ).replace("-", ""):
                            return (category, subcat, 5)

            # Default to DATA_UTILITIES
            return ("DATA_UTILITIES", "file_organization", 0)

        return (best_category, best_subcat, best_score)

    def scan_and_categorize(self):
        """Scan all content and build reorganization plan"""

        logger.info("=" * 70)
        logger.info("🔍 SCANNING FOR EXACT STRUCTURE REORGANIZATION")
        logger.info("=" * 70)
        print()

        # Get all top-level items in main categories
        for category_dir in [
            "AI_CONTENT",
            "AUTOMATION_BOTS",
            "DATA_UTILITIES",
            "MEDIA_PROCESSING",
            "documentation",
        ]:
            cat_path = self.base_dir / category_dir
            if not cat_path.exists():
                continue

            # Process each item in category
            for item in cat_path.iterdir():
                if item.name.startswith(".") or item.name == "__pycache__":
                    continue

                # Determine correct categorization
                target_category, target_subcat, score = self.categorize_item(item)

                # Build target path
                target_path = (
                    self.base_dir / target_category / target_subcat / item.name
                )

                # Skip if already in correct location
                if (
                    item.parent.parent == self.base_dir / target_category
                    and item.parent.name == target_subcat
                ):
                    continue

                self.moves.append(
                    {
                        "source": item,
                        "target": target_path,
                        "current_category": category_dir,
                        "target_category": target_category,
                        "target_subcat": target_subcat,
                        "score": score,
                    }
                )

        logger.info(f"📊 Found {len(self.moves)} items to reorganize")
        print()

    def execute(self, dry_run=True):
        """Execute reorganization"""

        self.scan_and_categorize()

        if not self.moves:
            logger.info("✅ Structure already matches exact specification!")
            return

        logger.info("=" * 70)
        logger.info(
            f"📝 EXACT STRUCTURE REORGANIZATION {'(DRY RUN)' if dry_run else '(LIVE)'}"
        )
        logger.info("=" * 70)
        print()

        # Group by target category
        by_category = defaultdict(list)
        for move in self.moves:
            by_category[move["target_category"]].append(move)

        moved_count = 0
        error_count = 0

        for category in sorted(by_category.keys()):
            items = by_category[category]
            logger.info(f"📂 {category}/ ({len(items)} items)")

            # Group by subcategory
            by_subcat = defaultdict(list)
            for item in items:
                by_subcat[item["target_subcat"]].append(item)

            for subcat in sorted(by_subcat.keys()):
                subcat_items = by_subcat[subcat]
                logger.info(f"   └─ {subcat}/ ({len(subcat_items)} items)")

                for move in subcat_items[:5]:  # Show first 5
                    rel_source = move["source"].relative_to(self.base_dir)

                    if dry_run:
                        logger.info(f"      [DRY RUN] {move['source'].name}")
                    else:
                        # Create target directory
                        move["target"].parent.mkdir(parents=True, exist_ok=True)

                        # Handle conflicts
                        target = move["target"]
                        if target.exists():
                            from datetime import datetime

                            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                            if move["source"].is_file():
                                new_name = f"{move['source'].stem}_{timestamp}{move['source'].suffix}"
                            else:
                                new_name = f"{move['source'].name}_{timestamp}"
                            target = target.parent / new_name

                        try:
                            shutil.move(str(move["source"]), str(target))
                            logger.info(f"      ✅ {move['source'].name}")
                            moved_count += 1
                        except Exception as e:
                            logger.info(f"      ❌ {move['source'].name} - ERROR")
                            error_count += 1

                if len(subcat_items) > 5:
                    logger.info(f"      ... and {len(subcat_items) - 5} more")

            print()

        logger.info("=" * 70)
        logger.info(f"{'Simulation' if dry_run else 'Execution'} complete!")
        if not dry_run:
            logger.info(f"   Moved: {moved_count}")
            logger.info(f"   Errors: {error_count}")
        logger.info("=" * 70)

        if not dry_run:
            print()
            logger.info("✨ Exact structure achieved!")
            print()
            logger.info("📊 Final structure:")
            logger.info("   ├── AUTOMATION_BOTS/ (35%)")
            logger.info("   │   ├── social_media_automation/")
            logger.info("   │   ├── youtube_reddit_content/")
            logger.info("   │   ├── bot_frameworks/")
            logger.info("   │   └── scrapers/")
            logger.info("   ├── MEDIA_PROCESSING/ (25%)")
            logger.info("   │   ├── audio_video_conversion/")
            logger.info("   │   ├── image_upscaling/")
            logger.info("   │   ├── gallery_generation/")
            logger.info("   │   └── tts_generation/")
            logger.info("   ├── AI_CONTENT/ (20%)")
            logger.info("   │   ├── tts_engines/")
            logger.info("   │   ├── image_generation/")
            logger.info("   │   ├── prompt_engineering/")
            logger.info("   │   └── content_creation/")
            logger.info("   ├── DATA_UTILITIES/ (15%)")
            logger.info("   │   ├── file_organization/")
            logger.info("   │   ├── csv_processing/")
            logger.info("   │   ├── data_analysis/")
            logger.info("   │   └── scrapers/")
            logger.info("   └── documentation/ (5%)")
            logger.info("       ├── code_browsers/")
            logger.info("       ├── tutorials/")
            logger.info("       └── references/")

        if dry_run:
            logger.info("\n💡 To execute, run:")
            logger.info("   python3 reorganize_to_exact_structure.py --execute")


def main():
    """main function."""

    import sys

    base_dir = Path(Path(str(Path.home()) + "/Documents/python"))
    dry_run = "--execute" not in sys.argv

    reorganizer = ExactStructureReorganizer(base_dir)
    reorganizer.execute(dry_run=dry_run)


if __name__ == "__main__":
    main()
