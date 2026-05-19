#!/usr/bin/env python3
"""Promote Archived Projects to Main Categories
Analyze directory-based projects in archived_items and move to proper categories
"""

import shutil
from pathlib import Path
from collections import defaultdict


class ArchivedProjectPromoter:
    """Promote useful archived projects to main categories"""

    def __init__(self, base_dir: Path):
        self.base_dir = base_dir
        self.experimental_dir = base_dir / "experiments/archived_items/experimental"

        # Manual intelligent mapping for archived projects
        self.project_map = {
            # AI Tools → AI_CONTENT
            "ai_tools/opus_clip": {
                "category": "AI_CONTENT/video/opus_clipper",
                "description": "Opus AI Video Clipper",
            },
            "ai_tools/voice_assistant": {
                "category": "AI_CONTENT/voice/assistant",
                "description": "AI Voice Assistant",
            },
            "ai_tools/prompt_pipeline": {
                "category": "AI_CONTENT/prompts/pipeline",
                "description": "AI Prompt Pipeline Tool",
            },
            # Audio Tools → MEDIA_PROCESSING
            "audio_tools/spicetify": {
                "category": "MEDIA_PROCESSING/audio/spotify",
                "description": "Spicetify Audio Tool",
            },
            # Bots → AUTOMATION_BOTS
            "bots/botty": {
                "category": "AUTOMATION_BOTS/social/botty",
                "description": "Botty Automation Tool",
            },
            "bots/spam_bot": {
                "category": "AUTOMATION_BOTS/social/spam_bot",
                "description": "Spam Bot Tool",
            },
        }

    def analyze_web_tools(self):
        """Analyze web_tools directory for promotable projects"""
        web_tools_dir = self.experimental_dir / "web_tools"
        if not web_tools_dir.exists():
            return []

        promotions = []

        # Check each project in web_tools
        for project_dir in web_tools_dir.iterdir():
            if not project_dir.is_dir() or project_dir.name.startswith("."):
                continue

            name_lower = project_dir.name.lower()

            # Categorize based on name patterns
            if any(word in name_lower for word in ["scraper", "scrape", "crawler"]):
                promotions.append(
                    {
                        "source": f"web_tools/{project_dir.name}",
                        "category": f"AUTOMATION_BOTS/web/scrapers/{project_dir.name}",
                        "description": f"Web Scraper: {project_dir.name}",
                    },
                )
            elif any(word in name_lower for word in ["downloader", "download"]):
                promotions.append(
                    {
                        "source": f"web_tools/{project_dir.name}",
                        "category": f"AUTOMATION_BOTS/web/downloaders/{project_dir.name}",
                        "description": f"Web Downloader: {project_dir.name}",
                    },
                )
            elif any(word in name_lower for word in ["bot", "automation"]):
                promotions.append(
                    {
                        "source": f"web_tools/{project_dir.name}",
                        "category": f"AUTOMATION_BOTS/web/bots/{project_dir.name}",
                        "description": f"Web Bot: {project_dir.name}",
                    },
                )

        return promotions

    def execute(self, dry_run=True):
        """Execute project promotion"""
        print("=" * 70)
        print(f"🚀 PROMOTE ARCHIVED PROJECTS {'(DRY RUN)' if dry_run else '(LIVE)'}")
        print("=" * 70)
        print()

        # Get web tools promotions
        web_promotions = self.analyze_web_tools()
        all_promotions = list(self.project_map.items()) + [
            (p["source"], p) for p in web_promotions
        ]

        if not all_promotions:
            print("✅ No archived projects found to promote!")
            return

        print(f"📦 Found {len(all_promotions)} projects to promote")
        print()

        moved_count = 0
        error_count = 0

        # Group by category
        by_category = defaultdict(list)
        for source_path, info in all_promotions:
            if isinstance(info, dict):
                category = info["category"].split("/")[0]  # Get main category
                by_category[category].append((source_path, info))

        for main_category, items in sorted(by_category.items()):
            print(f"📂 {main_category}/")

            for source_path, info in items:
                source = self.experimental_dir / source_path

                if not source.exists():
                    print(f"   ⚠️  Not found: {source_path}")
                    continue

                target = self.base_dir / info["category"]

                # Get project size
                try:
                    file_count = len(list(source.rglob("*"))) if source.is_dir() else 1
                    size_str = f"{file_count} items"
                except:
                    size_str = "unknown size"

                if dry_run:
                    print(f"   [DRY RUN] {source_path}")
                    print(f"           → {info['category']} ({size_str})")
                    print(f"              {info['description']}")
                else:
                    # Create target parent
                    target.parent.mkdir(parents=True, exist_ok=True)

                    # Handle conflicts
                    if target.exists():
                        from datetime import datetime

                        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                        new_name = f"{target.name}_{timestamp}"
                        target = target.parent / new_name

                    try:
                        shutil.move(str(source), str(target))
                        print(f"   ✅ {source_path}")
                        print(
                            f"      → {target.relative_to(self.base_dir)} ({size_str})",
                        )
                        moved_count += 1
                    except Exception as e:
                        print(f"   ❌ {source_path}")
                        print(f"      ERROR: {str(e)[:50]}")
                        error_count += 1

            print()

        print("=" * 70)
        print(f"{'Simulation' if dry_run else 'Promotion'} complete!")
        print(
            f"   Projects {'would be' if dry_run else ''} promoted: {moved_count if not dry_run else len(all_promotions)}",
        )
        if error_count > 0:
            print(f"   Errors: {error_count}")
        print("=" * 70)

        if dry_run:
            print("\n💡 To execute, run:")
            print("   python3 promote_archived_projects.py --execute")
        else:
            print("\n✨ Archived projects promoted!")
            print("   Useful tools moved to main categories")
            print("   Examples:")
            print("     • opus_clip → AI_CONTENT/video/opus_clipper/")
            print("     • voice_assistant → AI_CONTENT/voice/assistant/")
            print("     • botty → AUTOMATION_BOTS/social/botty/")


def main():
    import sys

    base_dir = Path("/Users/steven/Documents/python")
    dry_run = "--execute" not in sys.argv

    promoter = ArchivedProjectPromoter(base_dir)
    promoter.execute(dry_run=dry_run)


if __name__ == "__main__":
    main()
