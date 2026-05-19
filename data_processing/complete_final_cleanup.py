#!/usr/bin/env python3
"""
Complete Final Cleanup - Handle ALL remaining root items
"""

import shutil
from collections import defaultdict
from pathlib import Path


class CompleteFinalCleanup:
    """Comprehensive cleanup of all remaining root items"""

    def __init__(self, base_dir: Path):
        self.base_dir = base_dir

        # Comprehensive mapping for ALL remaining items
        self.cleanup_map = {
            # Remaining reorganization scripts → experiments/reorganization_tools
            "analyze_workflows.py": "experiments/reorganization_tools",
            "conversation_exporter.py": "experiments/reorganization_tools",
            "enhanced_intelligent_categorizer.py": "experiments/reorganization_tools",
            "execute_deep_reorganization.py": "experiments/reorganization_tools",
            "execute_enhanced_reorganization.py": "experiments/reorganization_tools",
            "final_duplicate_merge.py": "experiments/reorganization_tools",
            "ultimate_deep_reorganization.py": "experiments/reorganization_tools",
            # Analysis plans → experiments/analysis_artifacts
            "deep_reorganization_plan_20251026_033602.json": "experiments/analysis_artifacts",
            "enhanced_reorganization_plan_20251026_034934.json": "experiments/analysis_artifacts",
            # Documentation → DOCUMENTATION/project_docs
            "FINAL_TRANSFORMATION_SUMMARY.md": "DOCUMENTATION/project_docs",
            "IMPROVEMENTS_SUMMARY.md": "DOCUMENTATION/project_docs",
            "SETUP_GUIDE.md": "DOCUMENTATION/project_docs",
            # Setup scripts → experiments/setup_tools
            "setup_conversation_hook.sh": "experiments/setup_tools",
            # Automation bots → AUTOMATION_BOTS/legacy_categories
            "reddit-to-instagram-bot": "AUTOMATION_BOTS/legacy_categories/reddit-to-instagram-bot",
            "Twitch-Best-Of": "AUTOMATION_BOTS/legacy_categories/Twitch-Best-Of",
            "Twitch-TikTok-Youtube-Viewbot": "AUTOMATION_BOTS/legacy_categories/Twitch-TikTok-Youtube-Viewbot",
            "TwitchClipGenerator-main": "AUTOMATION_BOTS/legacy_categories/TwitchClipGenerator-main",
            "TwitchCompilationCreator": "AUTOMATION_BOTS/legacy_categories/TwitchCompilationCreator",
            # Media/Audio tools → MEDIA_PROCESSING/legacy_categories
            "savify": "MEDIA_PROCESSING/legacy_categories/savify",
            "SpotifyMP3": "MEDIA_PROCESSING/legacy_categories/SpotifyMP3",
            "spicetify-themes": "MEDIA_PROCESSING/legacy_categories/spicetify-themes",
            "voices": "MEDIA_PROCESSING/legacy_categories/voices",
            # Development/Tools → DATA_UTILITIES/legacy_categories
            "storyboarder_adaptive_setup": "DATA_UTILITIES/legacy_categories/storyboarder_adaptive_setup",
            "url-image-downloader": "DATA_UTILITIES/legacy_categories/url-image-downloader",
            "types": "DATA_UTILITIES/legacy_categories/types",
            "work": "DATA_UTILITIES/legacy_categories/work",
            # Git-related → _archived_cleanup/git_artifacts
            "refs": "_archived_cleanup/git_artifacts",
            "remotes": "_archived_cleanup/git_artifacts",
            # Misc/Unclear → _archived_cleanup/misc
            "run": "_archived_cleanup/misc",
            "test_export": "_archived_cleanup/misc",
            "ultimate": "_archived_cleanup/misc",
            "uml": "_archived_cleanup/misc",
            "Untitled": "_archived_cleanup/misc",
        }

    def get_all_root_items(self):
        '\''Get all items in root directory that aren't part of main structure"""
        protected_dirs = {
            "AI_CONTENT",
            "AUTOMATION_BOTS",
            "DATA_UTILITIES",
            "MEDIA_PROCESSING",
            "DOCUMENTATION",
            "experiments",
            "notebooks",
            "tests",
            "_archived_cleanup",
            "_organized_root_files",
            "documentation",  # lowercase version
        }

        root_items = []
        for item in self.base_dir.iterdir():
            if item.name.startswith("."):
                continue
            if item.name in protected_dirs:
                continue
            root_items.append(item.name)

        return sorted(root_items)

    def execute(self, dry_run=True):
        """Execute comprehensive cleanup'\''

        print("=" * 70)
        print(f"🧹 COMPLETE FINAL CLEANUP {'(DRY RUN)' if dry_run else '(LIVE)'}")
        print("=" * 70)
        print()

        # Get all items that need organizing
        all_items = self.get_all_root_items()

        # Add any unmapped items to the cleanup map
        for item in all_items:
            if item not in self.cleanup_map:
                # Auto-classify based on characteristics
                item_path = self.base_dir / item

                if item.endswith(".py"):
                    self.cleanup_map[item] = "experiments/reorganization_tools"
                elif item.endswith(".json"):
                    self.cleanup_map[item] = "experiments/analysis_artifacts"
                elif item.endswith(".md"):
                    self.cleanup_map[item] = "DOCUMENTATION/project_docs"
                elif item.endswith(".sh"):
                    self.cleanup_map[item] = "experiments/setup_tools"
                elif item_path.is_dir():
                    # Check directory name for hints
                    item_lower = item.lower()
                    if any(
                        word in item_lower
                        for word in [
                            "bot",
                            "automation",
                            "scraper",
                            "reddit",
                            "instagram",
                            "twitch",
                            "youtube",
                        ]
                    ):
                        self.cleanup_map[item] = (
                            "AUTOMATION_BOTS/legacy_categories/" + item
                        )
                    elif any(
                        word in item_lower
                        for word in [
                            "video",
                            "audio",
                            "media",
                            "music",
                            "spotify",
                            "mp3",
                            "voice",
                        ]
                    ):
                        self.cleanup_map[item] = (
                            "MEDIA_PROCESSING/legacy_categories/" + item
                        )
                    else:
                        self.cleanup_map[item] = "_archived_cleanup/misc/" + item
                else:
                    self.cleanup_map[item] = "_archived_cleanup/misc"

        moved_count = 0
        skipped_count = 0
        error_count = 0

        # Group by destination
        by_destination = defaultdict(list)
        for item in all_items:
            if item in self.cleanup_map:
                dest = self.cleanup_map[item]
                by_destination[dest].append(item)

        for dest, items in sorted(by_destination.items()):
            print(f"📂 {dest}/")

            for item in items:
                source = self.base_dir / item

                if not source.exists():
                    skipped_count += 1
                    continue

                # Determine target path
                if dest.endswith("/" + item):
                    # Destination already includes the item name
                    target = self.base_dir / dest
                else:
                    target_dir = self.base_dir / dest
                    target = target_dir / source.name

                # Get size info
                try:
                    if source.is_file():
                        size_kb = source.stat().st_size / 1024
                        size_str = f"{size_kb:.1f} KB"
                    else:
                        try:
                            file_count = len(list(source.rglob("*")))
                            size_str = f"{file_count} items"
                        except:
                            size_str = "dir"
                except:
                    size_str = "unknown"

                if dry_run:
                    print(f"   [DRY RUN] {source.name:<50} ({size_str})")
                else:
                    # Create target directory
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

                    # Move
                    try:
                        shutil.move(str(source), str(target))
                        print(f"   ✅ {source.name:<50} ({size_str})")
                        moved_count += 1
                    except Exception as e:
                        print(f"   ❌ {source.name:<50} ERROR: {str(e)[:30]}")
                        error_count += 1

            print()

        print("=" * 70)
        print(f"{'Simulation' if dry_run else 'Cleanup'} complete!")
        print(f"   Items {'would be' if dry_run else ''} moved: {moved_count}")
        if skipped_count > 0:
            print(f"   Already organized: {skipped_count}")
        if error_count > 0:
            print(f"   Errors: {error_count}")
        print("=" * 70)

        if dry_run:
            print("\n💡 To execute, run:")
            print("   python3 complete_final_cleanup.py --execute")
        else:
            print("\n✨ Complete cleanup finished!")
            print("\n📊 Final root directory structure:")
            print("   ├── AI_CONTENT/")
            print("   ├── AUTOMATION_BOTS/")
            print("   ├── DATA_UTILITIES/")
            print("   ├── MEDIA_PROCESSING/")
            print("   ├── DOCUMENTATION/")
            print("   ├── experiments/")
            print("   ├── notebooks/")
            print("   ├── tests/")
            print("   ├── _archived_cleanup/")
            print("   └── _organized_root_files/")
            print()
            print(f"   Check: ls -la {self.base_dir}/")


def main():
    import sys

    base_dir = Path("/Users/steven/Documents/python")
    dry_run = "--execute" not in sys.argv

    cleanup = CompleteFinalCleanup(base_dir)
    cleanup.execute(dry_run=dry_run)


if __name__ == "__main__":
    main()
