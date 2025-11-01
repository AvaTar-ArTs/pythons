"""
Utilities File Operations Comprehensive 9

This module provides functionality for utilities file operations comprehensive 9.

Author: Auto-generated
Date: 2025-11-01
"""

import logging

logger = logging.getLogger(__name__)


# Constants
CONSTANT_1024 = 1024

#!/usr/bin/env python3
"""
Comprehensive Experiments Promotion
Analyze ALL experiments content and promote to main categories
Exclude libraries folder, intelligently categorize everything else
"""

import shutil
from pathlib import Path
from collections import defaultdict


class ComprehensiveExperimentsPromoter:
    """Comprehensively promote all useful experiments content"""

    def __init__(self, base_dir: Path):
        """__init__ function."""

        self.base_dir = base_dir
        self.experiments_dir = base_dir / "experiments"
        self.promotions = []

    def build_promotion_map(self):
        """Build comprehensive promotion map for all experiments content"""

        # AI Tools → AI_CONTENT
        ai_tools = self.experiments_dir / "archived_items/experimental/ai_tools"
        if ai_tools.exists():
            for project in ai_tools.iterdir():
                if project.is_dir() and not project.name.startswith("."):
                    self.promotions.append(
                        {"source": project, "category": f"AI_CONTENT/tools/{project.name}", "type": "AI Tool"}
                    )

        # Audio Tools → MEDIA_PROCESSING
        audio_tools = self.experiments_dir / "archived_items/experimental/audio_tools"
        if audio_tools.exists():
            for project in audio_tools.iterdir():
                if project.is_dir() and not project.name.startswith("."):
                    self.promotions.append(
                        {"source": project, "category": f"MEDIA_PROCESSING/audio/{project.name}", "type": "Audio Tool"}
                    )

        # Bots → AUTOMATION_BOTS
        bots_dir = self.experiments_dir / "archived_items/experimental/bots"
        if bots_dir.exists():
            for project in bots_dir.iterdir():
                if project.is_dir() and not project.name.startswith("."):
                    self.promotions.append(
                        {"source": project, "category": f"AUTOMATION_BOTS/experimental/{project.name}", "type": "Bot"}
                    )

        # Web Tools → AUTOMATION_BOTS
        web_tools = self.experiments_dir / "archived_items/experimental/web_tools"
        if web_tools.exists():
            for project in web_tools.iterdir():
                if project.is_dir() and not project.name.startswith("."):
                    name_lower = project.name.lower()
                    if "download" in name_lower:
                        category = f"DATA_UTILITIES/web_tools/{project.name}"
                    else:
                        category = f"AUTOMATION_BOTS/web_tools/{project.name}"

                    self.promotions.append({"source": project, "category": category, "type": "Web Tool"})

        # Misc projects → Categorize by content
        misc_dir = self.experiments_dir / "archived_items/experimental/misc"
        if misc_dir.exists():
            for project in misc_dir.iterdir():
                if project.is_dir() and not project.name.startswith("."):
                    name_lower = project.name.lower()

                    if "gallery" in name_lower:
                        category = f"MEDIA_PROCESSING/gallery/{project.name}"
                        type_name = "Gallery Tool"
                    elif "editor" in name_lower or "tui" in name_lower:
                        category = f"DATA_UTILITIES/editors/{project.name}"
                        type_name = "Editor Tool"
                    else:
                        category = f"DATA_UTILITIES/misc/{project.name}"
                        type_name = "Utility"

                    self.promotions.append({"source": project, "category": category, "type": type_name})

        # AI Agents (loose files) → AI_CONTENT
        ai_agents = self.experiments_dir / "ai_agents"
        if ai_agents.exists():
            for file in ai_agents.iterdir():
                if file.is_file() and file.suffix == ".py":
                    self.promotions.append(
                        {"source": file, "category": f"AI_CONTENT/agents/{file.name}", "type": "AI Agent Script"}
                    )

        # Clipboard Tools → DATA_UTILITIES
        clipboard_tools = self.experiments_dir / "clipboard_tools"
        if clipboard_tools.exists():
            for file in clipboard_tools.iterdir():
                if file.is_file() and file.suffix == ".py":
                    self.promotions.append(
                        {"source": file, "category": f"DATA_UTILITIES/clipboard/{file.name}", "type": "Clipboard Tool"}
                    )

        # Download Tools → DATA_UTILITIES
        download_tools = self.experiments_dir / "download_tools"
        if download_tools.exists():
            for file in download_tools.iterdir():
                if file.is_file() and file.suffix == ".py":
                    self.promotions.append(
                        {"source": file, "category": f"DATA_UTILITIES/downloaders/{file.name}", "type": "Download Tool"}
                    )

        # Media Tools → MEDIA_PROCESSING
        media_tools = self.experiments_dir / "media_tools"
        if media_tools.exists():
            # Process subdirectories
            for subdir in media_tools.iterdir():
                if subdir.is_dir() and not subdir.name.startswith("."):
                    for file in subdir.rglob("*.py"):
                        rel_path = file.relative_to(media_tools)
                        self.promotions.append(
                            {
                                "source": file,
                                "category": f"MEDIA_PROCESSING/{rel_path.parent}/{file.name}",
                                "type": "Media Tool",
                            }
                        )

        # Reorganization Tools → Keep only essential, move to DATA_UTILITIES
        reorg_tools = self.experiments_dir / "reorganization_tools"
        if reorg_tools.exists():
            essential_tools = [
                "context_fluid_reorganizer.py",
                "context_fluid_organizer.py",
                "next_gen_content_analyzer.py",
            ]
            for file in reorg_tools.iterdir():
                if file.is_file() and file.suffix == ".py" and file.name in essential_tools:
                    self.promotions.append(
                        {
                            "source": file,
                            "category": f"DATA_UTILITIES/organization_tools/{file.name}",
                            "type": "Organization Tool",
                        }
                    )

    def execute(self, dry_run=True):
        """Execute comprehensive promotion"""

        logger.info("=" * 70)
        logger.info(f"🚀 COMPREHENSIVE EXPERIMENTS PROMOTION {'(DRY RUN)' if dry_run else '(LIVE)'}")
        logger.info("=" * 70)
        print()

        # Build promotion map
        self.build_promotion_map()

        if not self.promotions:
            logger.info("✅ No items to promote!")
            return

        logger.info(f"📦 Found {len(self.promotions)} items to promote")
        print()

        # Group by main category
        by_category = defaultdict(list)
        for promo in self.promotions:
            main_cat = promo["category"].split("/")[0]
            by_category[main_cat].append(promo)

        moved_count = 0
        error_count = 0

        for main_cat, items in sorted(by_category.items()):
            logger.info(f"📂 {main_cat}/ ({len(items)} items)")

            for promo in items:
                source = promo["source"]
                target = self.base_dir / promo["category"]

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

                rel_source = source.relative_to(self.experiments_dir)

                if dry_run:
                    logger.info(f"   [DRY RUN] {rel_source}")
                    logger.info(f"           → {promo['category']} ({size_str})")
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
                        logger.info(f"      → {target.relative_to(self.base_dir)} ({size_str})")
                        moved_count += 1
                    except Exception as e:
                        logger.info(f"   ❌ {rel_source}")
                        logger.info(f"      ERROR: {str(e)[:50]}")
                        error_count += 1

            print()

        logger.info("=" * 70)
        logger.info(f"{'Simulation' if dry_run else 'Promotion'} complete!")
        logger.info(
            f"   Items {'would be' if dry_run else ''} promoted: {moved_count if not dry_run else len(self.promotions)}"
        )
        if error_count > 0:
            logger.info(f"   Errors: {error_count}")
        logger.info("=" * 70)

        if not dry_run:
            # Clean up empty directories
            print()
            logger.info("🧹 Cleaning up empty directories...")
            self.cleanup_empty_dirs()

            print()
            logger.info("✨ Comprehensive promotion complete!")
            print()
            logger.info("📊 Summary:")
            for main_cat, items in sorted(by_category.items()):
                logger.info(f"   {main_cat}: {len(items)} items")

        if dry_run:
            logger.info("\n💡 To execute, run:")
            logger.info("   python3 comprehensive_experiments_promotion.py --execute")

    def cleanup_empty_dirs(self):
        """Remove empty directories after promotion"""

        # Remove experimental subdirectories if empty
        experimental_dir = self.experiments_dir / "archived_items/experimental"
        if experimental_dir.exists():
            for subdir in ["ai_tools", "audio_tools", "bots", "web_tools", "misc"]:
                dir_path = experimental_dir / subdir
                if dir_path.exists():
                    try:
                        # Remove empty subdirs recursively
                        for item in sorted(dir_path.rglob("*"), reverse=True):
                            if item.is_dir() and not any(item.iterdir()):
                                item.rmdir()
                                logger.info(f"   ✓ Removed empty: {item.relative_to(self.experiments_dir)}")

                        # Remove main dir if empty
                        if not any(dir_path.iterdir()):
                            dir_path.rmdir()
                            logger.info(f"   ✓ Removed empty: {dir_path.relative_to(self.experiments_dir)}")
                    except (ValueError, TypeError):
                        pass

        # Remove empty tool directories in experiments
        for tool_dir in ["ai_agents", "clipboard_tools", "download_tools", "media_tools"]:
            dir_path = self.experiments_dir / tool_dir
            if dir_path.exists():
                try:
                    if not any(dir_path.iterdir()):
                        dir_path.rmdir()
                        logger.info(f"   ✓ Removed empty: {tool_dir}/")
                except (ValueError, TypeError):
                    pass


def main():
    """main function."""

    import sys

    base_dir = Path(Path("/Users/steven/Documents/python"))
    dry_run = "--execute" not in sys.argv

    promoter = ComprehensiveExperimentsPromoter(base_dir)
    promoter.execute(dry_run=dry_run)


if __name__ == "__main__":
    main()
