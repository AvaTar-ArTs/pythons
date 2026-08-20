#!/usr/bin/env python3
"""
🔍 DEEP CONTENT-AWARE DUPLICATE ANALYZER
Analyzes documents, HTML files, and images for duplicates using content-awareness
"""

import difflib
import hashlib
import json
import os
from collections import defaultdict
from datetime import datetime
from pathlib import Path


class DeepDuplicateAnalyzer:
    def __init__(self, base_path):
        self.base_path = Path(base_path)
        self.results = {
            "documents": {"duplicates": [], "similar": [], "stats": {}},
            "html_files": {"duplicates": [], "similar": [], "stats": {}},
            "images": {"duplicates": [], "similar": [], "stats": {}},
            "summary": {},
        }

    def calculate_file_hash(self, filepath):
        """Calculate SHA256 hash of file"""
        sha256_hash = hashlib.sha256()
        try:
            with open(filepath, "rb") as f:
                for byte_block in iter(lambda: f.read(4096), b""):
                    sha256_hash.update(byte_block)
            return sha256_hash.hexdigest()
        except Exception as e:
            print(f"❌ Error hashing {filepath}: {e}")
            return None

    def calculate_content_hash(self, content):
        """Calculate hash of text content (normalized)"""
        # Normalize content: lowercase, strip whitespace
        normalized = " ".join(content.lower().split())
        return hashlib.sha256(normalized.encode()).hexdigest()

    def read_text_file(self, filepath):
        """Read text file with multiple encoding attempts"""
        encodings = ["utf-8", "latin-1", "cp1252", "iso-8859-1"]
        for encoding in encodings:
            try:
                with open(filepath, "r", encoding=encoding) as f:
                    return f.read()
            except UnicodeDecodeError:
                continue
            except Exception as e:
                print(f"❌ Error reading {filepath}: {e}")
                return None
        return None

    def calculate_similarity(self, text1, text2):
        """Calculate similarity ratio between two texts"""
        return difflib.SequenceMatcher(None, text1, text2).ratio()

    def analyze_images(self):
        """Analyze images folder for duplicate files"""
        print("📸 Analyzing images folder...")
        images_path = self.base_path / "images"

        if not images_path.exists():
            print("⚠️  Images folder not found")
            return

        hash_to_files = defaultdict(list)
        total_files = 0
        total_size = 0

        # Get all image files
        image_extensions = {".jpg", ".jpeg", ".png", ".gif", ".bmp", ".webp", ".svg"}
        image_files = []

        for ext in image_extensions:
            image_files.extend(list(images_path.glob(f"*{ext}")))
            image_files.extend(list(images_path.glob(f"*{ext.upper()}")))

        print(f"   Found {len(image_files)} image files")

        for i, filepath in enumerate(image_files):
            if i % 100 == 0 and i > 0:
                print(f"   Processed {i}/{len(image_files)} images...")

            total_files += 1
            file_size = filepath.stat().st_size
            total_size += file_size

            file_hash = self.calculate_file_hash(filepath)
            if file_hash:
                hash_to_files[file_hash].append(
                    {
                        "path": str(filepath),
                        "name": filepath.name,
                        "size": file_size,
                        "modified": datetime.fromtimestamp(
                            filepath.stat().st_mtime
                        ).isoformat(),
                    }
                )

        # Find duplicates
        duplicate_groups = []
        duplicate_count = 0
        wasted_space = 0

        for file_hash, files in hash_to_files.items():
            if len(files) > 1:
                duplicate_groups.append(
                    {
                        "hash": file_hash,
                        "count": len(files),
                        "size_each": files[0]["size"],
                        "total_wasted": files[0]["size"] * (len(files) - 1),
                        "files": files,
                    }
                )
                duplicate_count += len(files) - 1
                wasted_space += files[0]["size"] * (len(files) - 1)

        self.results["images"]["duplicates"] = sorted(
            duplicate_groups, key=lambda x: x["total_wasted"], reverse=True
        )
        self.results["images"]["stats"] = {
            "total_files": total_files,
            "total_size_mb": round(total_size / (1024 * 1024), 2),
            "unique_files": len(hash_to_files),
            "duplicate_groups": len(duplicate_groups),
            "duplicate_files": duplicate_count,
            "wasted_space_mb": round(wasted_space / (1024 * 1024), 2),
        }

        print(
            f"✅ Images analyzed: {total_files} files, {duplicate_count} duplicates found"
        )
        print(
            f"   💾 Wasted space: {self.results['images']['stats']['wasted_space_mb']} MB"
        )

    def analyze_documents(self):
        """Analyze documents folder for duplicate and similar content"""
        print("📄 Analyzing documents folder...")
        docs_path = self.base_path / "documents"

        if not docs_path.exists():
            print("⚠️  Documents folder not found")
            return

        # Categorize by extension
        text_extensions = {".txt", ".md"}
        doc_files = []

        for ext in text_extensions:
            doc_files.extend(list(docs_path.glob(f"*{ext}")))

        print(f"   Found {len(doc_files)} text documents")

        # Hash-based duplicate detection
        hash_to_files = defaultdict(list)
        content_hash_to_files = defaultdict(list)
        file_contents = {}

        total_files = 0
        total_size = 0

        for i, filepath in enumerate(doc_files):
            if i % 50 == 0 and i > 0:
                print(f"   Processed {i}/{len(doc_files)} documents...")

            total_files += 1
            file_size = filepath.stat().st_size
            total_size += file_size

            # Exact file hash
            file_hash = self.calculate_file_hash(filepath)

            # Content hash (normalized)
            content = self.read_text_file(filepath)
            if content:
                file_contents[str(filepath)] = content
                content_hash = self.calculate_content_hash(content)

                file_info = {
                    "path": str(filepath),
                    "name": filepath.name,
                    "size": file_size,
                    "modified": datetime.fromtimestamp(
                        filepath.stat().st_mtime
                    ).isoformat(),
                    "word_count": len(content.split()),
                }

                if file_hash:
                    hash_to_files[file_hash].append(file_info)
                content_hash_to_files[content_hash].append(file_info)

        # Find exact duplicates
        duplicate_groups = []
        duplicate_count = 0
        wasted_space = 0

        for content_hash, files in content_hash_to_files.items():
            if len(files) > 1:
                duplicate_groups.append(
                    {
                        "hash": content_hash,
                        "count": len(files),
                        "size_total": sum(f["size"] for f in files),
                        "files": files,
                    }
                )
                duplicate_count += len(files) - 1
                # Calculate wasted space (keep smallest file)
                sizes = [f["size"] for f in files]
                wasted_space += sum(sizes) - min(sizes)

        self.results["documents"]["duplicates"] = sorted(
            duplicate_groups, key=lambda x: x["count"], reverse=True
        )

        # Find similar documents (>80% similarity)
        print("   🔍 Checking for similar content...")
        similar_pairs = []
        checked_pairs = set()

        file_paths = list(file_contents.keys())
        for i, path1 in enumerate(file_paths):
            for path2 in file_paths[i + 1 :]:
                pair_key = tuple(sorted([path1, path2]))
                if pair_key in checked_pairs:
                    continue
                checked_pairs.add(pair_key)

                content1 = file_contents[path1]
                content2 = file_contents[path2]

                # Skip if already exact duplicates
                if self.calculate_content_hash(content1) == self.calculate_content_hash(
                    content2
                ):
                    continue

                similarity = self.calculate_similarity(content1, content2)
                if similarity > 0.80:  # 80% similarity threshold
                    similar_pairs.append(
                        {
                            "file1": Path(path1).name,
                            "file2": Path(path2).name,
                            "path1": path1,
                            "path2": path2,
                            "similarity": round(similarity * 100, 2),
                        }
                    )

        self.results["documents"]["similar"] = sorted(
            similar_pairs, key=lambda x: x["similarity"], reverse=True
        )

        self.results["documents"]["stats"] = {
            "total_files": total_files,
            "total_size_mb": round(total_size / (1024 * 1024), 2),
            "duplicate_groups": len(duplicate_groups),
            "duplicate_files": duplicate_count,
            "similar_pairs": len(similar_pairs),
            "wasted_space_mb": round(wasted_space / (1024 * 1024), 2),
        }

        print(f"✅ Documents analyzed: {total_files} files")
        print(f"   🔁 {duplicate_count} exact duplicates found")
        print(f"   ≈  {len(similar_pairs)} similar pairs found (>80% similarity)")

    def analyze_html_files(self):
        """Analyze HTML files for duplicates and similar content"""
        print("🌐 Analyzing HTML files...")
        html_path = self.base_path / "html_files"

        if not html_path.exists():
            print("⚠️  HTML files folder not found")
            return

        html_files = list(html_path.glob("*.html"))
        print(f"   Found {len(html_files)} HTML files")

        hash_to_files = defaultdict(list)
        content_hash_to_files = defaultdict(list)
        file_contents = {}

        total_files = 0
        total_size = 0

        for i, filepath in enumerate(html_files):
            if i % 50 == 0 and i > 0:
                print(f"   Processed {i}/{len(html_files)} HTML files...")

            total_files += 1
            file_size = filepath.stat().st_size
            total_size += file_size

            file_hash = self.calculate_file_hash(filepath)

            content = self.read_text_file(filepath)
            if content:
                file_contents[str(filepath)] = content
                content_hash = self.calculate_content_hash(content)

                file_info = {
                    "path": str(filepath),
                    "name": filepath.name,
                    "size": file_size,
                    "modified": datetime.fromtimestamp(
                        filepath.stat().st_mtime
                    ).isoformat(),
                }

                if file_hash:
                    hash_to_files[file_hash].append(file_info)
                content_hash_to_files[content_hash].append(file_info)

        # Find exact duplicates
        duplicate_groups = []
        duplicate_count = 0
        wasted_space = 0

        for content_hash, files in content_hash_to_files.items():
            if len(files) > 1:
                duplicate_groups.append(
                    {
                        "hash": content_hash,
                        "count": len(files),
                        "size_total": sum(f["size"] for f in files),
                        "files": files,
                    }
                )
                duplicate_count += len(files) - 1
                sizes = [f["size"] for f in files]
                wasted_space += sum(sizes) - min(sizes)

        self.results["html_files"]["duplicates"] = sorted(
            duplicate_groups, key=lambda x: x["count"], reverse=True
        )

        # Find similar HTML files
        print("   🔍 Checking for similar HTML content...")
        similar_pairs = []
        checked_pairs = set()

        file_paths = list(file_contents.keys())
        for i, path1 in enumerate(file_paths):
            for path2 in file_paths[i + 1 :]:
                pair_key = tuple(sorted([path1, path2]))
                if pair_key in checked_pairs:
                    continue
                checked_pairs.add(pair_key)

                content1 = file_contents[path1]
                content2 = file_contents[path2]

                if self.calculate_content_hash(content1) == self.calculate_content_hash(
                    content2
                ):
                    continue

                similarity = self.calculate_similarity(content1, content2)
                if similarity > 0.85:  # 85% similarity for HTML
                    similar_pairs.append(
                        {
                            "file1": Path(path1).name,
                            "file2": Path(path2).name,
                            "path1": path1,
                            "path2": path2,
                            "similarity": round(similarity * 100, 2),
                        }
                    )

        self.results["html_files"]["similar"] = sorted(
            similar_pairs, key=lambda x: x["similarity"], reverse=True
        )

        self.results["html_files"]["stats"] = {
            "total_files": total_files,
            "total_size_mb": round(total_size / (1024 * 1024), 2),
            "duplicate_groups": len(duplicate_groups),
            "duplicate_files": duplicate_count,
            "similar_pairs": len(similar_pairs),
            "wasted_space_mb": round(wasted_space / (1024 * 1024), 2),
        }

        print(f"✅ HTML analyzed: {total_files} files")
        print(f"   🔁 {duplicate_count} exact duplicates found")
        print(f"   ≈  {len(similar_pairs)} similar pairs found (>85% similarity)")

    def generate_report(self):
        """Generate comprehensive report"""
        total_wasted_mb = (
            self.results["images"]["stats"].get("wasted_space_mb", 0)
            + self.results["documents"]["stats"].get("wasted_space_mb", 0)
            + self.results["html_files"]["stats"].get("wasted_space_mb", 0)
        )

        total_duplicates = (
            self.results["images"]["stats"].get("duplicate_files", 0)
            + self.results["documents"]["stats"].get("duplicate_files", 0)
            + self.results["html_files"]["stats"].get("duplicate_files", 0)
        )

        self.results["summary"] = {
            "total_wasted_space_mb": round(total_wasted_mb, 2),
            "total_duplicate_files": total_duplicates,
            "analysis_timestamp": datetime.now().isoformat(),
        }

        # Save JSON report
        report_path = self.base_path / "DUPLICATE_ANALYSIS_REPORT.json"
        with open(report_path, "w", encoding="utf-8") as f:
            json.dump(self.results, f, indent=2, ensure_ascii=False)

        print(f"\n✅ JSON report saved to: {report_path}")

        # Generate human-readable report
        self.generate_markdown_report()

    def generate_markdown_report(self):
        """Generate markdown report"""
        report_lines = []
        report_lines.append("# 🔍 DEEP DUPLICATE ANALYSIS REPORT")
        report_lines.append(
            f"\n**Analysis Date:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
        )
        report_lines.append(f"\n---\n")

        # Executive Summary
        report_lines.append("## 📊 EXECUTIVE SUMMARY\n")
        report_lines.append(
            f"- **Total Duplicate Files:** {self.results['summary']['total_duplicate_files']}"
        )
        report_lines.append(
            f"- **Total Wasted Space:** {self.results['summary']['total_wasted_space_mb']} MB"
        )
        report_lines.append(
            f"- **Potential Space Savings:** {self.results['summary']['total_wasted_space_mb']} MB\n"
        )

        # Images Section
        report_lines.append("## 📸 IMAGES ANALYSIS\n")
        img_stats = self.results["images"]["stats"]
        report_lines.append(f"- **Total Files:** {img_stats.get('total_files', 0)}")
        report_lines.append(f"- **Total Size:** {img_stats.get('total_size_mb', 0)} MB")
        report_lines.append(f"- **Unique Files:** {img_stats.get('unique_files', 0)}")
        report_lines.append(
            f"- **Duplicate Groups:** {img_stats.get('duplicate_groups', 0)}"
        )
        report_lines.append(
            f"- **Duplicate Files:** {img_stats.get('duplicate_files', 0)}"
        )
        report_lines.append(
            f"- **Wasted Space:** {img_stats.get('wasted_space_mb', 0)} MB\n"
        )

        if self.results["images"]["duplicates"]:
            report_lines.append(
                "### 🔝 Top 10 Image Duplicate Groups (by wasted space):\n"
            )
            for i, group in enumerate(self.results["images"]["duplicates"][:10], 1):
                report_lines.append(
                    f"\n**{i}. Group {i}** - {group['count']} copies, {round(group['total_wasted']/(1024*1024), 2)} MB wasted"
                )
                for file in group["files"][:3]:  # Show first 3 files
                    report_lines.append(f"   - `{Path(file['path']).name}`")
                if len(group["files"]) > 3:
                    report_lines.append(f"   - ... and {len(group['files']) - 3} more")

        # Documents Section
        report_lines.append("\n## 📄 DOCUMENTS ANALYSIS\n")
        doc_stats = self.results["documents"]["stats"]
        report_lines.append(f"- **Total Files:** {doc_stats.get('total_files', 0)}")
        report_lines.append(f"- **Total Size:** {doc_stats.get('total_size_mb', 0)} MB")
        report_lines.append(
            f"- **Duplicate Groups:** {doc_stats.get('duplicate_groups', 0)}"
        )
        report_lines.append(
            f"- **Duplicate Files:** {doc_stats.get('duplicate_files', 0)}"
        )
        report_lines.append(
            f"- **Similar Pairs (>80%):** {doc_stats.get('similar_pairs', 0)}"
        )
        report_lines.append(
            f"- **Wasted Space:** {doc_stats.get('wasted_space_mb', 0)} MB\n"
        )

        if self.results["documents"]["duplicates"]:
            report_lines.append("### 🔝 Top 10 Document Duplicate Groups:\n")
            for i, group in enumerate(self.results["documents"]["duplicates"][:10], 1):
                report_lines.append(f"\n**{i}. Group {i}** - {group['count']} copies")
                for file in group["files"][:3]:
                    report_lines.append(f"   - `{file['name']}`")
                if len(group["files"]) > 3:
                    report_lines.append(f"   - ... and {len(group['files']) - 3} more")

        if self.results["documents"]["similar"]:
            report_lines.append("\n### 📝 Top 20 Similar Document Pairs:\n")
            for i, pair in enumerate(self.results["documents"]["similar"][:20], 1):
                report_lines.append(f"\n**{i}.** Similarity: {pair['similarity']}%")
                report_lines.append(f"   - `{pair['file1']}`")
                report_lines.append(f"   - `{pair['file2']}`")

        # HTML Section
        report_lines.append("\n## 🌐 HTML FILES ANALYSIS\n")
        html_stats = self.results["html_files"]["stats"]
        report_lines.append(f"- **Total Files:** {html_stats.get('total_files', 0)}")
        report_lines.append(
            f"- **Total Size:** {html_stats.get('total_size_mb', 0)} MB"
        )
        report_lines.append(
            f"- **Duplicate Groups:** {html_stats.get('duplicate_groups', 0)}"
        )
        report_lines.append(
            f"- **Duplicate Files:** {html_stats.get('duplicate_files', 0)}"
        )
        report_lines.append(
            f"- **Similar Pairs (>85%):** {html_stats.get('similar_pairs', 0)}"
        )
        report_lines.append(
            f"- **Wasted Space:** {html_stats.get('wasted_space_mb', 0)} MB\n"
        )

        if self.results["html_files"]["duplicates"]:
            report_lines.append("### 🔝 Top 10 HTML Duplicate Groups:\n")
            for i, group in enumerate(self.results["html_files"]["duplicates"][:10], 1):
                report_lines.append(f"\n**{i}. Group {i}** - {group['count']} copies")
                for file in group["files"][:3]:
                    report_lines.append(f"   - `{file['name']}`")
                if len(group["files"]) > 3:
                    report_lines.append(f"   - ... and {len(group['files']) - 3} more")

        if self.results["html_files"]["similar"]:
            report_lines.append("\n### 🌐 Top 20 Similar HTML Pairs:\n")
            for i, pair in enumerate(self.results["html_files"]["similar"][:20], 1):
                report_lines.append(f"\n**{i}.** Similarity: {pair['similarity']}%")
                report_lines.append(f"   - `{pair['file1']}`")
                report_lines.append(f"   - `{pair['file2']}`")

        # Recommendations
        report_lines.append("\n## 💡 RECOMMENDATIONS\n")
        report_lines.append(
            "1. **Remove Exact Duplicates:** Start with image duplicates (highest space savings)"
        )
        report_lines.append(
            "2. **Review Similar Files:** Manually check similar documents/HTML for potential merging"
        )
        report_lines.append("3. **Backup First:** Always backup before removing files")
        report_lines.append(
            "4. **Keep Best Version:** When removing duplicates, keep the most recently modified or largest file"
        )

        # Save markdown report
        report_path = self.base_path / "DUPLICATE_ANALYSIS_REPORT.md"
        with open(report_path, "w", encoding="utf-8") as f:
            f.write("\n".join(report_lines))

        print(f"✅ Markdown report saved to: {report_path}")

    def run_full_analysis(self):
        """Run complete analysis"""
        print("=" * 60)
        print("🚀 STARTING DEEP DUPLICATE ANALYSIS")
        print("=" * 60)

        self.analyze_images()
        print()
        self.analyze_documents()
        print()
        self.analyze_html_files()
        print()
        self.generate_report()

        print("\n" + "=" * 60)
        print("✅ ANALYSIS COMPLETE!")
        print("=" * 60)
        print(f"\n🎯 RESULTS:")
        print(
            f"   💾 Total wasted space: {self.results['summary']['total_wasted_space_mb']} MB"
        )
        print(
            f"   📁 Total duplicate files: {self.results['summary']['total_duplicate_files']}"
        )
        print(f"\n📊 Check the reports for detailed information!")


if __name__ == "__main__":
    base_path = "/Users/steven/tehSiTes/New_Folder_With_Items_3_ORGANIZED"
    analyzer = DeepDuplicateAnalyzer(base_path)
    analyzer.run_full_analysis()
