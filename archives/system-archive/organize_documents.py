#!/usr/bin/env python3
"""
Organize ~/Documents based on fix.txt analysis
Categorizes and organizes files intelligently
"""

import shutil
from pathlib import Path
from collections import defaultdict


class DocumentsOrganizer:
    def __init__(self, docs_dir):
        self.docs_dir = Path(docs_dir)
        self.categories = defaultdict(list)

    def organize_files(self):
        """Organize all files from fix.txt list"""
        print("🔍 Analyzing Documents folder...")

        # Create organization structure
        org_structure = {
            "audio-analysis": self.docs_dir / "organized" / "audio-analysis",
            "transcripts": self.docs_dir / "organized" / "transcripts",
            "reports": self.docs_dir / "organized" / "reports",
            "strategies": self.docs_dir / "organized" / "strategies",
            "guides": self.docs_dir / "organized" / "guides",
            "templates": self.docs_dir / "organized" / "templates",
            "temp-files": self.docs_dir / "organized" / "temp-files",
            "configs": self.docs_dir / "organized" / "configs",
        }

        # Create folders
        for folder in org_structure.values():
            folder.mkdir(parents=True, exist_ok=True)

        moved_count = 0

        # Organize loose files in Documents root
        for item in self.docs_dir.iterdir():
            if not item.is_file():
                continue

            name_lower = item.name.lower()

            # Skip already organized or essential files
            if "fix.txt" in name_lower or "organize_documents" in name_lower:
                continue

            # Categorize
            if "_transcript.txt" in name_lower:
                dest = org_structure["transcripts"]
            elif "_analysis.txt" in name_lower:
                dest = org_structure["audio-analysis"]
            elif (
                "report" in name_lower
                or "summary" in name_lower
                or "analysis" in name_lower
            ):
                dest = org_structure["reports"]
            elif (
                "strategy" in name_lower
                or "plan" in name_lower
                or "roadmap" in name_lower
            ):
                dest = org_structure["strategies"]
            elif (
                "guide" in name_lower or "readme" in name_lower or "setup" in name_lower
            ):
                dest = org_structure["guides"]
            elif (
                "template" in name_lower
                or "invoice" in name_lower
                or "contract" in name_lower
            ):
                dest = org_structure["templates"]
            elif (
                name_lower.startswith("cat")
                or "pasted-content" in name_lower
                or item.suffix == ".txttxt"
            ):
                dest = org_structure["temp-files"]
            elif (
                item.suffix in [".json", ".csv", ".txt"] and item.stat().st_size < 10000
            ):
                dest = org_structure["configs"]
            else:
                # Keep in root if it's a major file
                continue

            # Move file
            try:
                shutil.move(str(item), str(dest / item.name))
                moved_count += 1
                self.categories[dest.name].append(item.name)
            except Exception as e:
                print(f"  ⚠️  Error moving {item.name}: {e}")

        print(f"  ✅ Organized {moved_count} files\n")

        # Show breakdown
        for category, files in sorted(
            self.categories.items(), key=lambda x: -len(x[1])
        ):
            print(f"  • {category}: {len(files)} files")

    def delete_duplicate_temp_files(self):
        """Delete obvious temp/duplicate files"""
        print("\n🗑️  Deleting temp files...")

        deleted = 0
        temp_patterns = ["cat*.txt", "*pasted-content*.txt", "*.txttxt.txt"]

        for pattern in temp_patterns:
            for temp_file in self.docs_dir.glob(pattern):
                try:
                    temp_file.unlink()
                    deleted += 1
                except:
                    pass

        print(f"  ✅ Deleted {deleted} temp files")

    def generate_report(self):
        """Generate organization report"""
        report = self.docs_dir / "DOCUMENTS_ORGANIZATION_COMPLETE.md"

        with open(report, "w") as f:
            f.write("# 📁 DOCUMENTS ORGANIZATION COMPLETE\n\n")
            f.write("**Date:** November 1, 2025\n\n")
            f.write("---\n\n")

            total_files = sum(len(files) for files in self.categories.values())

            f.write("## 📊 ORGANIZATION SUMMARY\n\n")
            f.write(f"**Total Files Organized:** {total_files}\n\n")

            f.write("### Categories Created\n\n")
            f.write("| Category | Files |\n")
            f.write("|----------|-------|\n")

            for category, files in sorted(
                self.categories.items(), key=lambda x: -len(x[1])
            ):
                f.write(f"| {category} | {len(files)} |\n")

            f.write("\n## 📁 NEW STRUCTURE\n\n")
            f.write("All files organized into: `~/Documents/organized/`\n\n")
            f.write("- **audio-analysis/** - Song analysis files\n")
            f.write("- **transcripts/** - Audio transcripts\n")
            f.write("- **reports/** - Analysis & summary reports\n")
            f.write("- **strategies/** - Planning & strategy docs\n")
            f.write("- **guides/** - How-to & setup guides\n")
            f.write("- **templates/** - Invoice, contract templates\n")
            f.write("- **temp-files/** - Temporary files (for review)\n")
            f.write("- **configs/** - Small config files\n")

        print(f"\n  ✅ Report saved to: {report}")


def main():
    docs_dir = "/Users/steven/Documents"

    print("=" * 70)
    print("📁 DOCUMENTS COMPREHENSIVE ORGANIZER")
    print("=" * 70)
    print()

    organizer = DocumentsOrganizer(docs_dir)
    organizer.organize_files()
    organizer.delete_duplicate_temp_files()
    organizer.generate_report()

    print("\n" + "=" * 70)
    print("✅ DOCUMENTS ORGANIZATION COMPLETE")
    print("=" * 70)
    print()


if __name__ == "__main__":
    main()
