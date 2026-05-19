#!/usr/bin/env python3
"""
Organize 2,173 loose files in Pictures root by analyzing their content
"""

import shutil
from pathlib import Path
from collections import defaultdict


class PicturesOrganizer:
    def __init__(self, pictures_dir):
        self.pictures_dir = Path(pictures_dir)
        self.organized = defaultdict(list)
        self.large_gifs = []

    def analyze_and_categorize(self):
        """Analyze all loose files and categorize them"""
        print("🔍 Analyzing 2,173 loose files...")

        # Category folders to create
        categories = {
            "leonardo": self.pictures_dir / "organized" / "leonardo-ai",
            "html_juice": self.pictures_dir / "organized" / "html-juice",
            "creature_tech": self.pictures_dir / "organized" / "creature-tech",
            "typography": self.pictures_dir / "organized" / "typography",
            "charts_graphs": self.pictures_dir / "organized" / "charts-graphs",
            "screenshots": self.pictures_dir / "organized" / "screenshots",
            "misc_images": self.pictures_dir / "organized" / "misc-images",
            "large_gifs": self.pictures_dir / "organized" / "large-gifs",
        }

        # Create folders
        for folder in categories.values():
            folder.mkdir(parents=True, exist_ok=True)

        # Scan and categorize loose files
        for item in self.pictures_dir.iterdir():
            if not item.is_file():
                continue

            if item.suffix.lower() not in [
                ".jpg",
                ".jpeg",
                ".png",
                ".gif",
                ".webp",
                ".svg",
                ".bmp",
            ]:
                continue

            name_lower = item.name.lower()
            size_mb = item.stat().st_size / (1024 * 1024)

            # Categorize
            if "leonardo" in name_lower or "300dpi" in name_lower:
                dest = categories["leonardo"]
            elif "html" in name_lower and "juice" in name_lower:
                dest = categories["html_juice"]
            elif "creature" in name_lower or "jungle" in name_lower:
                dest = categories["creature_tech"]
            elif "typography" in name_lower or "font" in name_lower:
                dest = categories["typography"]
            elif (
                "chart" in name_lower
                or "graph" in name_lower
                or "analyze" in name_lower
            ):
                dest = categories["charts_graphs"]
            elif (
                "screenshot" in name_lower
                or "aws" in name_lower
                or "lambda" in name_lower
            ):
                dest = categories["screenshots"]
            elif item.suffix == ".gif" and size_mb > 10:
                dest = categories["large_gifs"]
                self.large_gifs.append(item)
            else:
                dest = categories["misc_images"]

            self.organized[dest.name].append((item, size_mb))

        print(
            f"  ✅ Categorized {sum(len(files) for files in self.organized.values())} files\n"
        )

        # Show breakdown
        for category, files in sorted(self.organized.items(), key=lambda x: -len(x[1])):
            total_size = sum(size for _, size in files)
            print(f"  • {category}: {len(files)} files ({total_size:.1f} MB)")

    def move_files_to_categories(self):
        """Move files to their categorized folders"""
        print("\n📁 Moving files to organized folders...")

        moved = 0
        for category, files in self.organized.items():
            for file_path, size_mb in files:
                dest_folder = self.pictures_dir / "organized" / category
                try:
                    shutil.move(str(file_path), str(dest_folder / file_path.name))
                    moved += 1
                except Exception as e:
                    print(f"  ⚠️  Error moving {file_path.name}: {e}")

        print(f"  ✅ Moved {moved} files to organized folders")

    def generate_report(self):
        """Generate organization report"""
        report_path = self.pictures_dir / "PICTURES_ORGANIZATION_REPORT.md"

        with open(report_path, "w") as f:
            f.write("# 📸 PICTURES ORGANIZATION REPORT\n\n")
            f.write(f"**Date:** {Path.ctime(self.pictures_dir)}\n\n")
            f.write("---\n\n")

            f.write("## 📊 ORGANIZATION SUMMARY\n\n")
            total_files = sum(len(files) for files in self.organized.values())
            total_size = sum(
                sum(size for _, size in files) for files in self.organized.values()
            )

            f.write(f"**Total Files Organized:** {total_files}\n")
            f.write(f"**Total Size:** {total_size:.1f} MB\n\n")

            f.write("### Categories Created\n\n")
            f.write("| Category | Files | Size (MB) |\n")
            f.write("|----------|-------|----------|\n")

            for category, files in sorted(
                self.organized.items(), key=lambda x: -len(x[1])
            ):
                total_size = sum(size for _, size in files)
                f.write(f"| {category} | {len(files)} | {total_size:.1f} |\n")

            if self.large_gifs:
                f.write("\n## ⚠️ LARGE GIF FILES\n\n")
                f.write("These GIFs are very large and could be optimized:\n\n")
                for gif in self.large_gifs:
                    size_mb = gif.stat().st_size / (1024 * 1024)
                    f.write(f"- {gif.name} ({size_mb:.1f} MB)\n")
                f.write(
                    "\n**Recommendation:** Convert to MP4 for 80-90% size reduction\n"
                )

            f.write("\n## 📁 NEW STRUCTURE\n\n")
            f.write("All loose files have been organized into:\n")
            f.write("`~/Pictures/organized/`\n\n")
            f.write("With subfolders by category for easy access.\n")

        print(f"\n  ✅ Report saved to: {report_path}")


def main():
    pictures_dir = "/Users/steven/Pictures"

    print("=" * 70)
    print("📸 PICTURES COMPREHENSIVE ORGANIZER")
    print("=" * 70)
    print()

    organizer = PicturesOrganizer(pictures_dir)
    organizer.analyze_and_categorize()
    organizer.move_files_to_categories()
    organizer.generate_report()

    print("\n" + "=" * 70)
    print("✅ ORGANIZATION COMPLETE")
    print("=" * 70)
    print()


if __name__ == "__main__":
    main()
