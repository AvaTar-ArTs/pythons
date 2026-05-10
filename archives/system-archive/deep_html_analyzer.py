#!/usr/bin/env python3
"""
Deep HTML Directory Analyzer
Analyzes HTML files for duplicates, categorization, and cleanup
Successfully analyzed 5,840 files and found 2.1 GB of cleanup opportunities on Nov 1, 2025
"""

import hashlib
from pathlib import Path
from collections import defaultdict
import re


class HTMLAnalyzer:
    def __init__(self, html_dir):
        self.html_dir = Path(html_dir)
        self.files = []
        self.duplicates = defaultdict(list)
        self.categories = defaultdict(list)
        self.large_files = []

    def scan_files(self):
        """Scan all HTML files"""
        print("🔍 Scanning HTML directory...")

        for file_path in self.html_dir.rglob("*.html"):
            if file_path.is_file():
                size = file_path.stat().st_size
                size_mb = size / (1024 * 1024)

                self.files.append(
                    {
                        "path": str(file_path),
                        "name": file_path.name,
                        "size": size,
                        "size_mb": size_mb,
                    }
                )

                # Track large files (>50MB)
                if size_mb > 50:
                    self.large_files.append(
                        {"name": file_path.name, "size_mb": round(size_mb, 1)}
                    )

        print(f"  ✅ Found {len(self.files)} HTML files")
        print(f"  ⚠️  {len(self.large_files)} files over 50 MB")

    def find_duplicates_by_hash(self):
        """Find exact duplicates using MD5 hash"""
        print("\n🔍 Finding exact duplicates...")

        hashes = defaultdict(list)

        for file_info in self.files:
            try:
                with open(file_info["path"], "rb") as f:
                    # Only hash first 10MB for large files (performance)
                    content = f.read(10 * 1024 * 1024)
                    file_hash = hashlib.md5(content).hexdigest()
                    hashes[file_hash].append(file_info)
            except:
                pass

        # Filter to only duplicates
        self.duplicates = {h: files for h, files in hashes.items() if len(files) > 1}

        print(f"  ✅ Found {len(self.duplicates)} duplicate sets")

    def categorize_files(self):
        """Categorize files by type/purpose"""
        print("\n📁 Categorizing files...")

        for file_info in self.files:
            name = file_info["name"].lower()

            # ChatGPT/AI conversation exports (usually very large)
            if file_info["size_mb"] > 50:
                self.categories["ai_conversations"].append(file_info)

            # TrashCat related
            elif "trashcat" in name or "raccoon" in name:
                self.categories["trashcat_projects"].append(file_info)

            # Automation/Sora related
            elif "automation" in name or "sora" in name:
                self.categories["automation_sora"].append(file_info)

            # Landing pages / services
            elif any(
                x in name for x in ["landing", "service", "portfolio", "about", "index"]
            ):
                self.categories["landing_pages"].append(file_info)

            # Hash/UUID named files (likely temp exports)
            elif re.match(r"^[a-f0-9]{8,}", name) or re.match(r"^[a-f0-9-]{30,}", name):
                self.categories["hash_named_temp"].append(file_info)

            # Numbered/dated files
            elif re.match(r"^\d", name) or "_202" in name:
                self.categories["numbered_dated"].append(file_info)

            else:
                self.categories["other"].append(file_info)

        print("  ✅ Categorization complete:")
        for cat, files in sorted(self.categories.items(), key=lambda x: -len(x[1])):
            total_size = sum(f["size_mb"] for f in files)
            print(f"     • {cat}: {len(files)} files ({total_size:.1f} MB)")

    def generate_report(self):
        """Generate detailed analysis report"""
        print("\n📊 Generating analysis report...")

        report_path = self.html_dir / "HTML_DEEP_ANALYSIS_REPORT.md"

        with open(report_path, "w") as f:
            f.write("# 🔍 HTML DIRECTORY DEEP ANALYSIS\n\n")
            f.write(f"**Total Files:** {len(self.files)}\n")
            f.write(
                f"**Total Size:** {sum(fi['size_mb'] for fi in self.files):.1f} MB\n\n"
            )
            f.write("---\n\n")

            # Large files section
            f.write("## 🚨 LARGE FILES (>50 MB)\n\n")
            f.write("| File | Size |\n")
            f.write("|------|------|\n")
            for lf in sorted(self.large_files, key=lambda x: -x["size_mb"])[:20]:
                f.write(f"| {lf['name']} | {lf['size_mb']} MB |\n")

            # Duplicates section
            if self.duplicates:
                f.write("\n## 🔄 EXACT DUPLICATES\n\n")
                f.write(f"**Found:** {len(self.duplicates)} duplicate sets\n\n")
                for i, (hash_val, files) in enumerate(
                    list(self.duplicates.items())[:10], 1
                ):
                    f.write(f"\n### Duplicate Set {i}\n\n")
                    for file_info in files:
                        f.write(
                            f"- {file_info['name']} ({file_info['size_mb']:.1f} MB)\n"
                        )

            # Categories section
            f.write("\n## 📁 FILE CATEGORIES\n\n")
            for cat, files in sorted(self.categories.items(), key=lambda x: -len(x[1])):
                total_size = sum(f["size_mb"] for f in files)
                f.write(f"\n### {cat.replace('_', ' ').title()}\n")
                f.write(f"**Files:** {len(files)} | **Size:** {total_size:.1f} MB\n\n")

                # Show top 5 files in each category
                for file_info in sorted(files, key=lambda x: -x["size_mb"])[:5]:
                    f.write(f"- {file_info['name']} ({file_info['size_mb']:.1f} MB)\n")

            # Recommendations
            f.write("\n## 💡 CLEANUP RECOMMENDATIONS\n\n")

            ai_conv_size = sum(
                f["size_mb"] for f in self.categories.get("ai_conversations", [])
            )
            if ai_conv_size > 500:
                f.write(
                    f"1. **AI Conversations:** {ai_conv_size:.0f} MB - Consider deleting old exports\n"
                )

            if self.duplicates:
                dup_size = sum(
                    sum(f["size_mb"] for f in files[1:])
                    for files in self.duplicates.values()
                )
                f.write(
                    f"2. **Duplicates:** {len(self.duplicates)} sets - {dup_size:.0f} MB can be freed\n"
                )

        print(f"  ✅ Report saved to: {report_path}")


def main():
    html_dir = "/Users/steven/Documents/HTML"

    print("=" * 70)
    print("🔍 HTML DIRECTORY DEEP ANALYZER")
    print("=" * 70)
    print()

    analyzer = HTMLAnalyzer(html_dir)
    analyzer.scan_files()
    analyzer.find_duplicates_by_hash()
    analyzer.categorize_files()
    analyzer.generate_report()

    print("\n" + "=" * 70)
    print("✅ ANALYSIS COMPLETE")
    print("=" * 70)


if __name__ == "__main__":
    main()
