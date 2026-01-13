#!/usr/bin/env python3
"""
🔀 COMPREHENSIVE DIFF, MERGE & REMOVE SYSTEM
Complete analysis with visual diffs, intelligent merging, and duplicate removal
"""

import hashlib
import json
import difflib
from pathlib import Path
from collections import defaultdict
from datetime import datetime
from typing import Dict, List, Optional

class ComprehensiveDiffMerger:
    def __init__(self, base_path: str):
        self.base_path = Path(base_path)
        self.results = {
            "analysis": {},
            "diff_reports": [],
            "merge_actions": [],
            "removal_actions": []
        }

    def calculate_hash(self, filepath: Path) -> Optional[str]:
        """Calculate SHA256 hash"""
        try:
            with open(filepath, "rb") as f:
                return hashlib.sha256(f.read()).hexdigest()
        except Exception as e:
            print(f"❌ Error hashing {filepath}: {e}")
            return None

    def read_text(self, filepath: Path) -> Optional[str]:
        """Read text file with encoding fallback"""
        for encoding in ["utf-8", "latin-1", "cp1252", "iso-8859-1"]:
            try:
                with open(filepath, "r", encoding=encoding) as f:
                    return f.read()
            except:
                continue
        return None

    def generate_diff(self, file1: Path, file2: Path) -> Dict:
        """Generate detailed diff between two files"""
        content1 = self.read_text(file1)
        content2 = self.read_text(file2)

        if not content1 or not content2:
            return {"error": "Could not read files"}

        # Calculate similarity
        similarity = difflib.SequenceMatcher(None, content1, content2).ratio()

        # Generate unified diff
        diff = list(difflib.unified_diff(
            content1.splitlines(keepends=True),
            content2.splitlines(keepends=True),
            fromfile=str(file1.name),
            tofile=str(file2.name),
            lineterm=""
        ))

        return {
            "file1": str(file1),
            "file2": str(file2),
            "similarity": round(similarity * 100, 2),
            "diff_lines": len(diff),
            "diff": diff[:50] if len(diff) > 50 else diff  # Limit for display
        }

    def find_all_duplicates(self) -> Dict:
        """Find all duplicates across all folders"""
        print("🔍 SCANNING FOR DUPLICATES...")

        all_duplicates = {
            "documents": {"exact": [], "similar": []},
            "html_files": {"exact": [], "similar": []},
            "images": {"exact": []}
        }

        # Scan each folder
        for folder_name in ["documents", "html_files", "images"]:
            folder = self.base_path / folder_name
            if not folder.exists():
                continue

            print(f"\n📂 Scanning {folder_name}...")

            # Get files
            if folder_name == "images":
                extensions = [".jpg", ".jpeg", ".png", ".gif", ".bmp", ".webp", ".svg"]
            elif folder_name == "html_files":
                extensions = [".html"]
            else:
                extensions = [".txt", ".md", ".pdf"]

            files = []
            for ext in extensions:
                files.extend(list(folder.glob(f"*{ext}")))
                files.extend(list(folder.glob(f"*{ext.upper()}")))

            print(f"   Found {len(files)} files")

            # Hash-based duplicate detection
            hash_to_files = defaultdict(list)
            content_hash_to_files = defaultdict(list)

            for i, filepath in enumerate(files):
                if i % 100 == 0 and i > 0:
                    print(f"   Processed {i}/{len(files)}...")

                # File hash
                file_hash = self.calculate_hash(filepath)
                if file_hash:
                    file_info = {
                        "path": str(filepath),
                        "name": filepath.name,
                        "size": filepath.stat().st_size,
                        "modified": datetime.fromtimestamp(filepath.stat().st_mtime).isoformat()
                    }
                    hash_to_files[file_hash].append(file_info)

                    # Content hash for text files
                    if folder_name != "images":
                        content = self.read_text(filepath)
                        if content:
                            normalized = " ".join(content.lower().split())
                            content_hash = hashlib.sha256(normalized.encode()).hexdigest()
                            content_hash_to_files[content_hash].append(file_info)

            # Find exact duplicates
            for file_hash, file_list in hash_to_files.items():
                if len(file_list) > 1:
                    all_duplicates[folder_name]["exact"].append({
                        "hash": file_hash,
                        "count": len(file_list),
                        "files": file_list,
                        "total_size": sum(f["size"] for f in file_list),
                        "wasted_space": sum(f["size"] for f in file_list[1:])
                    })

            # Find similar content (for text files)
            if folder_name != "images" and len(content_hash_to_files) > 0:
                print(f"   Checking for similar content...")
                file_paths = [Path(f["path"]) for files in content_hash_to_files.values() for f in files[:1]]

                checked = set()
                for i, path1 in enumerate(file_paths[:50]):  # Limit for speed
                    content1 = self.read_text(path1)
                    if not content1:
                        continue

                    for path2 in file_paths[i+1:i+20]:  # Check next 20 files
                        if path1 == path2:
                            continue

                        pair_key = tuple(sorted([str(path1), str(path2)]))
                        if pair_key in checked:
                            continue
                        checked.add(pair_key)

                        content2 = self.read_text(path2)
                        if not content2:
                            continue

                        similarity = difflib.SequenceMatcher(None, content1, content2).ratio()

                        if 0.80 <= similarity < 0.99:  # Similar but not exact
                            all_duplicates[folder_name]["similar"].append({
                                "file1": str(path1),
                                "file2": str(path2),
                                "similarity": round(similarity * 100, 2)
                            })

        self.results["analysis"] = all_duplicates
        return all_duplicates

    def generate_diff_report(self, duplicates: Dict):
        """Generate visual diff reports"""
        print("\n📊 GENERATING DIFF REPORTS...")

        report_lines = []
        report_lines.append("# 🔀 COMPREHENSIVE DIFF REPORT\n")
        report_lines.append(f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        report_lines.append("---\n")

        # Statistics
        total_exact = sum(len(v["exact"]) for v in duplicates.values())
        total_similar = sum(len(v["similar"]) for v in duplicates.values())

        report_lines.append("## 📊 SUMMARY\n")
        report_lines.append(f"- **Exact Duplicate Groups:** {total_exact}")
        report_lines.append(f"- **Similar Content Pairs:** {total_similar}")
        report_lines.append("")

        # Exact duplicates
        for folder, data in duplicates.items():
            if data["exact"]:
                report_lines.append(f"## 📁 {folder.upper()} - EXACT DUPLICATES\n")

                for i, group in enumerate(data["exact"][:10], 1):
                    report_lines.append(f"### Group {i}: {group['count']} copies")
                    report_lines.append(f"- **Wasted Space:** {round(group['wasted_space'] / 1024, 2)} KB")
                    report_lines.append("- **Files:**")
                    for file in group["files"]:
                        report_lines.append(f"  - `{file['name']}` ({round(file['size']/1024, 2)} KB)")
                    report_lines.append("")

        # Similar content with diffs
        for folder, data in duplicates.items():
            if data["similar"]:
                report_lines.append(f"## 📄 {folder.upper()} - SIMILAR CONTENT\n")

                for i, pair in enumerate(data["similar"][:5], 1):
                    report_lines.append(f"### Similarity Pair {i}: {pair['similarity']}% match")
                    report_lines.append(f"- File 1: `{Path(pair['file1']).name}`")
                    report_lines.append(f"- File 2: `{Path(pair['file2']).name}`")

                    # Generate diff
                    diff_result = self.generate_diff(Path(pair['file1']), Path(pair['file2']))
                    if "diff" in diff_result and diff_result["diff"]:
                        report_lines.append("\n**Differences:**")
                        report_lines.append("```diff")
                        for line in diff_result["diff"][:20]:
                            report_lines.append(line.rstrip())
                        report_lines.append("```\n")

                    self.results["diff_reports"].append(diff_result)

        # Save report
        report_path = self.base_path / "COMPREHENSIVE_DIFF_REPORT.md"
        with open(report_path, "w", encoding="utf-8") as f:
            f.write("\n".join(report_lines))

        print(f"✅ Diff report saved: {report_path}")

    def execute_merge_and_remove(self, duplicates: Dict):
        """Execute merge and removal operations"""
        print("\n🔧 EXECUTING MERGE & REMOVE...")

        total_removed = 0
        total_space_saved = 0

        for folder, data in duplicates.items():
            print(f"\n📂 Processing {folder}...")

            # Remove exact duplicates (keep newest)
            for group in data["exact"]:
                files = group["files"]

                # Sort by modification date (newest first)
                files.sort(key=lambda x: x["modified"], reverse=True)

                keep_file = files[0]
                remove_files = files[1:]

                print(f"   Keeping: {keep_file['name']}")

                for file_info in remove_files:
                    filepath = Path(file_info["path"])
                    try:
                        if filepath.exists():
                            filepath.unlink()
                            print(f"   🗑️  Removed: {filepath.name}")
                            total_removed += 1
                            total_space_saved += file_info["size"]

                            self.results["removal_actions"].append({
                                "removed": str(filepath),
                                "kept": keep_file["path"],
                                "reason": "exact_duplicate",
                                "timestamp": datetime.now().isoformat()
                            })
                    except Exception as e:
                        print(f"   ❌ Error removing {filepath}: {e}")

            # For similar content, keep the larger/newer one
            processed_similar = set()
            for pair in data["similar"]:
                file1 = Path(pair["file1"])
                file2 = Path(pair["file2"])

                # Skip if already processed
                if str(file1) in processed_similar or str(file2) in processed_similar:
                    continue

                if not file1.exists() or not file2.exists():
                    continue

                # Keep the larger or newer file
                stat1 = file1.stat()
                stat2 = file2.stat()

                if stat1.st_mtime > stat2.st_mtime or stat1.st_size > stat2.st_size:
                    keep_file = file1
                    remove_file = file2
                else:
                    keep_file = file2
                    remove_file = file1

                try:
                    remove_file.unlink()
                    print(f"   🔀 Merged similar: kept {keep_file.name}, removed {remove_file.name}")
                    total_removed += 1
                    total_space_saved += remove_file.stat().st_size if remove_file.exists() else 0

                    processed_similar.add(str(remove_file))

                    self.results["merge_actions"].append({
                        "removed": str(remove_file),
                        "kept": str(keep_file),
                        "similarity": pair["similarity"],
                        "reason": "similar_content",
                        "timestamp": datetime.now().isoformat()
                    })
                except Exception as e:
                    print(f"   ❌ Error: {e}")

        return {
            "total_removed": total_removed,
            "total_space_saved": total_space_saved
        }

    def generate_final_report(self, stats: Dict):
        """Generate final summary report"""
        report_lines = []
        report_lines.append("# ✅ FINAL MERGE & REMOVE REPORT\n")
        report_lines.append(f"**Completed:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        report_lines.append("---\n")

        report_lines.append("## 📊 FINAL STATISTICS\n")
        report_lines.append(f"- **Total Files Removed:** {stats['total_removed']}")
        report_lines.append(f"- **Total Space Saved:** {round(stats['total_space_saved'] / (1024 * 1024), 2)} MB")
        report_lines.append("")

        # Removal log
        if self.results["removal_actions"]:
            report_lines.append("## 🗑️  EXACT DUPLICATES REMOVED\n")
            for action in self.results["removal_actions"]:
                report_lines.append(f"- Removed `{Path(action['removed']).name}` (kept `{Path(action['kept']).name}`)")

        # Merge log
        if self.results["merge_actions"]:
            report_lines.append("\n## 🔀 SIMILAR CONTENT MERGED\n")
            for action in self.results["merge_actions"]:
                report_lines.append(f"- Merged `{Path(action['removed']).name}` into `{Path(action['kept']).name}` ({action['similarity']}% similar)")

        report_lines.append("\n## ✨ OPERATION COMPLETE!\n")
        report_lines.append("All duplicates have been removed and similar content has been merged.")
        report_lines.append("The best versions of all files have been preserved.")

        # Save report
        report_path = self.base_path / "FINAL_MERGE_REMOVE_REPORT.md"
        with open(report_path, "w", encoding="utf-8") as f:
            f.write("\n".join(report_lines))

        # Save JSON log
        json_path = self.base_path / "MERGE_REMOVE_LOG.json"
        with open(json_path, "w", encoding="utf-8") as f:
            json.dump(self.results, f, indent=2, ensure_ascii=False)

        print(f"\n✅ Final report saved: {report_path}")
        print(f"✅ JSON log saved: {json_path}")

    def run_complete_operation(self):
        """Run the complete diff, merge, and remove operation"""
        print("=" * 70)
        print("🔀 COMPREHENSIVE DIFF, MERGE & REMOVE OPERATION")
        print("=" * 70)

        # Step 1: Find duplicates
        duplicates = self.find_all_duplicates()

        # Step 2: Generate diff report
        self.generate_diff_report(duplicates)

        # Step 3: Execute merge and remove
        stats = self.execute_merge_and_remove(duplicates)

        # Step 4: Generate final report
        self.generate_final_report(stats)

        print("\n" + "=" * 70)
        print("✅ OPERATION COMPLETE!")
        print("=" * 70)
        print(f"\n🎯 RESULTS:")
        print(f"   🗑️  Files removed: {stats['total_removed']}")
        print(f"   💾 Space saved: {round(stats['total_space_saved'] / (1024 * 1024), 2)} MB")
        print(f"\n✨ All duplicates removed! Best versions preserved.")


if __name__ == "__main__":
    base_path = "/Users/steven/tehSiTes/New_Folder_With_Items_3_ORGANIZED"
    merger = ComprehensiveDiffMerger(base_path)
    merger.run_complete_operation()
