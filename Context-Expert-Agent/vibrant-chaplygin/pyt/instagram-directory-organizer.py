#!/usr/bin/env python3
"""
Directory Organizer - Intelligently organize all folders

Consolidates backups, categorizes projects, and creates clean structure.
"""

import os
import shutil
from pathlib import Path
from datetime import datetime
import json


class DirectoryOrganizer:
    def __init__(self, target_dir: str):
        self.target_dir = Path(target_dir)
        self.timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

        # Define organization structure
        self.categories = {
            "BACKUPS": [],
            "01_CORE_TOOLS": [],
            "02_YOUTUBE_AUTOMATION": [],
            "03_AI_CREATIVE_TOOLS": [],
            "04_WEB_SCRAPING": [],
            "05_SOCIAL_MEDIA": [],
            "06_MEDIA_PROCESSING": [],
            "07_UTILITIES": [],
            "08_ANALYSIS_TOOLS": [],
            "09_DOCUMENTATION": [],
            "10_ARCHIVED_PROJECTS": [],
        }

        # Backup folder patterns
        self.backup_patterns = [
            "dedup_backup",
            "bare_except_backup",
            "deep_rename_backup",
            "automated_fixes_backup",
            "merge_backup",
            "merge_analysis",
        ]

        # Category mappings
        self.youtube_keywords = [
            "youtube",
            "yt-",
            "video-generator",
            "automated-yt",
            "auto-youtube",
            "shorts",
            "livestream",
        ]

        self.social_keywords = [
            "instagram",
            "instapy",
            "igbot",
            "tiktok",
            "reddit",
            "twitch",
            "facebook",
            "fb-script",
            "telegram",
            "tg-",
        ]

        self.ai_keywords = [
            "dalle",
            "leonardo",
            "gemini",
            "llm",
            "ai-",
            "gpt",
            "comics_generator",
            "manga",
            "sora",
        ]

        self.web_scraping_keywords = ["scrape", "scraper", "backlink", "seo-"]

        self.media_keywords = [
            "upscale",
            "photoshop",
            "image",
            "video",
            "audio",
            "spotify",
            "savify",
            "remove-bg",
        ]

        self.utility_keywords = [
            "rsync",
            "fdupes",
            "folder-file",
            "file-handling",
            "organizer",
            "sort",
            "clean",
        ]

    def categorize_folder(self, folder_name: str) -> str:
        """Determine category for a folder."""
        folder_lower = folder_name.lower()

        # Check if it's a backup
        if any(pattern in folder_lower for pattern in self.backup_patterns):
            return "BACKUPS"

        # Check documentation
        if any(
            x in folder_lower for x in ["docs", "documentation", "comprehensive_docs"]
        ):
            return "09_DOCUMENTATION"

        # Check YouTube
        if any(keyword in folder_lower for keyword in self.youtube_keywords):
            return "02_YOUTUBE_AUTOMATION"

        # Check Social Media
        if any(keyword in folder_lower for keyword in self.social_keywords):
            return "05_SOCIAL_MEDIA"

        # Check AI Tools
        if any(keyword in folder_lower for keyword in self.ai_keywords):
            return "03_AI_CREATIVE_TOOLS"

        # Check Web Scraping
        if any(keyword in folder_lower for keyword in self.web_scraping_keywords):
            return "04_WEB_SCRAPING"

        # Check Media Processing
        if any(keyword in folder_lower for keyword in self.media_keywords):
            return "06_MEDIA_PROCESSING"

        # Check Utilities
        if any(keyword in folder_lower for keyword in self.utility_keywords):
            return "07_UTILITIES"

        # Check if it's analysis/tools
        if any(x in folder_lower for x in ["analysis", "analyzer", "tools"]):
            return "08_ANALYSIS_TOOLS"

        # Check if already categorized (01_, 02_, etc.)
        if folder_name.startswith(("01_", "02_", "03_", "04_")):
            return "01_CORE_TOOLS"

        # Check special cases
        if folder_name in [
            "scripts",
            "_versions",
            "-p_segments",
            "github_improvements",
            "github_templates",
        ]:
            return "01_CORE_TOOLS"

        # Default to archived
        return "10_ARCHIVED_PROJECTS"

    def get_clean_name(self, folder_name: str) -> str:
        """Clean up folder names."""
        # Fix badly named folders
        if folder_name.startswith("this_script"):
            return "system-admin-script"

        if folder_name.startswith("This script"):
            return "flake8-processor"

        # Remove trailing dashes/underscores
        clean = folder_name.strip("-_")

        return clean

    def analyze_structure(self):
        """Analyze current directory structure."""
        print("\n🔍 Analyzing directory structure...\n")

        folders = [f for f in self.target_dir.iterdir() if f.is_dir()]
        folders = [f for f in folders if not f.name.startswith(".")]

        # Categorize each folder
        for folder in folders:
            category = self.categorize_folder(folder.name)
            self.categories[category].append(folder)

        # Print summary
        print("📊 CATEGORIZATION SUMMARY:\n")
        for category, folders in self.categories.items():
            if folders:
                print(f"{category}: {len(folders)} folders")
                for folder in sorted(folders)[:5]:
                    print(f"  - {folder.name}")
                if len(folders) > 5:
                    print(f"  ... and {len(folders) - 5} more")
                print()

        return self.categories

    def create_plan(self):
        """Create reorganization plan."""
        plan = {"timestamp": self.timestamp, "actions": []}

        # Plan 1: Consolidate backups
        backups = self.categories["BACKUPS"]
        if backups:
            backup_archive = self.target_dir / f"_ARCHIVED_BACKUPS_{self.timestamp}"
            plan["actions"].append(
                {
                    "type": "consolidate_backups",
                    "target": str(backup_archive),
                    "folders": [str(f) for f in backups],
                }
            )

        # Plan 2: Ensure category directories exist
        for category in self.categories.keys():
            if category != "BACKUPS" and not category.startswith("10_"):
                category_dir = self.target_dir / category.lower().replace("_", "-")
                if not category_dir.exists():
                    plan["actions"].append(
                        {"type": "create_category", "directory": str(category_dir)}
                    )

        # Plan 3: Move folders to categories
        for category, folders in self.categories.items():
            if category not in ["BACKUPS", "01_CORE_TOOLS"] and folders:
                target_category = self.target_dir / category.lower().replace("_", "-")
                for folder in folders:
                    # Skip if already in correct location
                    if folder.parent == target_category:
                        continue

                    clean_name = self.get_clean_name(folder.name)
                    new_path = target_category / clean_name

                    plan["actions"].append(
                        {
                            "type": "move_folder",
                            "source": str(folder),
                            "target": str(new_path),
                            "category": category,
                        }
                    )

        return plan

    def execute_plan(self, plan, dry_run=True):
        """Execute the reorganization plan."""
        mode = "DRY RUN" if dry_run else "LIVE"
        print(f"\n{'='*80}")
        print(f"🚀 EXECUTING REORGANIZATION PLAN - {mode}")
        print(f"{'='*80}\n")

        stats = {
            "backups_consolidated": 0,
            "categories_created": 0,
            "folders_moved": 0,
            "errors": 0,
        }

        for action in plan["actions"]:
            try:
                if action["type"] == "consolidate_backups":
                    print(
                        f"\n📦 Consolidating {len(action['folders'])} backup folders..."
                    )
                    if not dry_run:
                        Path(action["target"]).mkdir(exist_ok=True)
                        for folder in action["folders"]:
                            src = Path(folder)
                            dst = Path(action["target"]) / src.name
                            if src.exists():
                                shutil.move(str(src), str(dst))
                        stats["backups_consolidated"] = len(action["folders"])
                    else:
                        print(f"  Would move to: {action['target']}")

                elif action["type"] == "create_category":
                    print(f"\n📁 Creating category: {Path(action['directory']).name}")
                    if not dry_run:
                        Path(action["directory"]).mkdir(exist_ok=True)
                        stats["categories_created"] += 1

                elif action["type"] == "move_folder":
                    src = Path(action["source"])
                    dst = Path(action["target"])
                    print(f"\n➡️  Moving to {action['category']}:")
                    print(f"    {src.name} → {dst.parent.name}/{dst.name}")

                    if not dry_run:
                        dst.parent.mkdir(parents=True, exist_ok=True)
                        if src.exists():
                            shutil.move(str(src), str(dst))
                            stats["folders_moved"] += 1

            except Exception as e:
                print(f"❌ Error: {e}")
                stats["errors"] += 1

        # Generate report
        self.generate_report(plan, stats, dry_run)

        return stats

    def generate_report(self, plan, stats, dry_run):
        """Generate reorganization report."""
        report_path = (
            self.target_dir / f"DIRECTORY_ORGANIZATION_REPORT_{self.timestamp}.md"
        )

        with open(report_path, "w") as f:
            f.write("# 📁 Directory Organization Report\n\n")
            f.write(f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"**Mode:** {'DRY RUN' if dry_run else 'LIVE'}\n\n")

            f.write("## Statistics\n\n")
            f.write(f"- **Backups Consolidated:** {stats['backups_consolidated']}\n")
            f.write(f"- **Categories Created:** {stats['categories_created']}\n")
            f.write(f"- **Folders Moved:** {stats['folders_moved']}\n")
            f.write(f"- **Errors:** {stats['errors']}\n\n")

            f.write("## Final Structure\n\n")
            f.write("```\n")
            f.write(str(Path.home()) + "/Documents/python/\n")
            for category in sorted(self.categories.keys()):
                folder_name = category.lower().replace("_", "-")
                if category != "BACKUPS":
                    f.write(f"├── {folder_name}/\n")
            f.write("└── _archived_backups_*/\n")
            f.write("```\n")

        print(f"\n✅ Report saved: {report_path}\n")

    def run(self, dry_run=True):
        """Run the complete organization process."""
        print("\n{'='*80}")
        print("📁 DIRECTORY ORGANIZER")
        print("{'='*80}\n")

        # Step 1: Analyze
        self.analyze_structure()

        # Step 2: Create plan
        plan = self.create_plan()

        # Step 3: Execute
        stats = self.execute_plan(plan, dry_run)

        print(f"\n{'='*80}")
        print("✅ ORGANIZATION COMPLETE!")
        print(f"{'='*80}\n")
        print(f"Backups Consolidated: {stats['backups_consolidated']}")
        print(f"Categories Created: {stats['categories_created']}")
        print(f"Folders Moved: {stats['folders_moved']}")
        if stats["errors"] > 0:
            print(f"⚠️  Errors: {stats['errors']}")
        print()


def main():
    import argparse

    parser = argparse.ArgumentParser(description="Directory Organizer")
    parser.add_argument("--target", default=".", help="Target directory")
    parser.add_argument(
        "--live", action="store_true", help="Execute moves (default: dry run)"
    )

    args = parser.parse_args()

    organizer = DirectoryOrganizer(args.target)
    organizer.run(dry_run=not args.live)


if __name__ == "__main__":
    main()
