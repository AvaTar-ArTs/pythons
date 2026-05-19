#!/usr/bin/env python3
"""
✨ FINAL POLISH CLEANUP
Fix the last 5 consolidation opportunities: 27 → 23 directories
"""

import shutil
from pathlib import Path
from datetime import datetime


class FinalPolish:
    def __init__(self, pythons_dir="/Users/steven/pythons"):
        self.pythons_dir = Path(pythons_dir)
        self.stats = {"moved": 0, "deleted": 0, "errors": []}

    def execute(self):
        """Execute final polish"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        archive_dir = self.pythons_dir / "_archive" / f"final-polish-{timestamp}"
        archive_dir.mkdir(parents=True, exist_ok=True)

        print("✨ EXECUTING FINAL POLISH CLEANUP")
        print("=" * 70 + "\n")

        # CONSOLIDATION 1: social_media/ → AUTOMATION_BOTS/social_media_automation/
        print("📱 CONSOLIDATION 1: Social Media")
        self._move_contents("social_media", "AUTOMATION_BOTS/social_media_automation")

        # CONSOLIDATION 2: Instagram-Bot/ → AUTOMATION_BOTS/social_media_automation/
        print("\n📸 CONSOLIDATION 2: Instagram-Bot")
        self._move_contents("Instagram-Bot", "AUTOMATION_BOTS/social_media_automation")

        # CONSOLIDATION 3: youtube/ → AUTOMATION_BOTS/youtube_bots/
        print("\n📺 CONSOLIDATION 3: YouTube")
        self._move_contents("youtube", "AUTOMATION_BOTS/youtube_bots")

        # CONSOLIDATION 4: scrapers/ → AUTOMATION_BOTS/web_scrapers/
        print("\n🕷️  CONSOLIDATION 4: Scrapers")
        self._move_contents("scrapers", "AUTOMATION_BOTS/web_scrapers")

        # CONSOLIDATION 5: Python/ subdirs → proper locations
        print("\n🐍 CONSOLIDATION 5: Python/ subdirectories")
        python_dir = self.pythons_dir / "Python"
        if python_dir.exists():
            self._move_subdir(
                "Python/simplegallery-MY-TEMPLATE 2", "MEDIA_PROCESSING/galleries"
            )
            self._move_subdir("Python/leonardo", "MEDIA_PROCESSING/image_tools")
            self._move_subdir("Python/DALLe", "MEDIA_PROCESSING/image_tools")
            self._move_subdir("Python/upscale", "MEDIA_PROCESSING/image_tools")
            self._move_subdir("Python/organize", "DATA_UTILITIES/organization_scripts")

            # Delete Python/ if empty or nearly empty
            remaining = list(python_dir.rglob("*"))
            if len(remaining) < 5:
                shutil.move(str(python_dir), str(archive_dir / "Python"))
                print("🗑️  Archived: Python/ (mostly empty)")
                self.stats["deleted"] += 1

        # DELETE 1: Python-organize/ (broken)
        print("\n🗑️  DELETION 1: Python-organize (broken script output)")
        broken_dir = self.pythons_dir / "Python-organize"
        if broken_dir.exists():
            shutil.move(str(broken_dir), str(archive_dir / "Python-organize"))
            print("✅ Deleted: Python-organize/ (archived)")
            self.stats["deleted"] += 1

        # SUMMARY
        print("\n" + "=" * 70)
        print("📊 FINAL POLISH SUMMARY")
        print("=" * 70)
        print(f"Items moved:       {self.stats['moved']}")
        print(f"Dirs archived:     {self.stats['deleted']}")
        print(f"Errors:            {len(self.stats['errors'])}")
        print("=" * 70)

        if self.stats["errors"]:
            print("\n⚠️  Errors:")
            for err in self.stats["errors"][:5]:
                print(f"  - {err}")

        print(f"\n📦 Archive: {archive_dir}")

        # Final count
        final_dirs = len(
            [
                d
                for d in self.pythons_dir.iterdir()
                if d.is_dir() and not d.name.startswith(".")
            ]
        )
        final_files = len(list(self.pythons_dir.glob("*.py")))

        print("\n🎉 FINAL RESULT:")
        print(f"  Directories: 131 → 27 → {final_dirs} ✨")
        print(f"  Root files:  77 → {final_files}")
        print("\n✅ ~/pythons/ IS NOW PERFECTLY ORGANIZED! 🎉")

    def _move_contents(self, source_name, target_path):
        """Move all contents of source directory to target"""
        source = self.pythons_dir / source_name
        target = self.pythons_dir / target_path

        if not source.exists():
            print(f"⚠️  Skip: {source_name}/ (not found)")
            return

        target.mkdir(parents=True, exist_ok=True)

        # Move entire directory into target
        final_target = target / source_name
        if final_target.exists():
            print(f"⚠️  Skip: {source_name}/ (already exists in {target_path})")
            return

        try:
            shutil.move(str(source), str(final_target))
            print(f"✅ {source_name}/ → {target_path}/{source_name}/")
            self.stats["moved"] += 1
        except Exception as e:
            self.stats["errors"].append(f"{source_name}: {e}")
            print(f"❌ Error: {source_name} - {e}")

    def _move_subdir(self, source_path, target_path):
        """Move a subdirectory to new location"""
        source = self.pythons_dir / source_path
        target = self.pythons_dir / target_path

        if not source.exists():
            print(f"⚠️  Skip: {source_path} (not found)")
            return

        target.mkdir(parents=True, exist_ok=True)

        source_name = source.name
        final_target = target / source_name

        if final_target.exists():
            print(f"⚠️  Skip: {source_name}/ (exists)")
            return

        try:
            shutil.move(str(source), str(final_target))
            print(f"✅ {source_path} → {target_path}/{source_name}/")
            self.stats["moved"] += 1
        except Exception as e:
            self.stats["errors"].append(f"{source_path}: {e}")
            print(f"❌ Error: {source_path} - {e}")


def main():
    print("""
╔═══════════════════════════════════════════════════════════════════╗
║        ✨ FINAL POLISH - THE LAST 5 FIXES                        ║
║        27 directories → 23 directories (PERFECTION!)             ║
╚═══════════════════════════════════════════════════════════════════╝
""")

    print("This will:")
    print("  ✅ Move social_media/ → AUTOMATION_BOTS/")
    print("  ✅ Move Instagram-Bot/ → AUTOMATION_BOTS/")
    print("  ✅ Move youtube/ → AUTOMATION_BOTS/")
    print("  ✅ Move scrapers/ → AUTOMATION_BOTS/")
    print("  ✅ Consolidate Python/ subdirs")
    print("  🗑️  Delete Python-organize/ (broken)")
    print("  🗑️  Archive Python/ (after moving contents)")
    print()

    confirm = input("Type 'POLISH' to execute: ")

    if confirm == "POLISH":
        polish = FinalPolish()
        polish.execute()
    else:
        print("\n❌ Cancelled")


if __name__ == "__main__":
    main()
