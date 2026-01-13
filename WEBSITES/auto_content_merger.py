#!/usr/bin/env python3
"""
🤖 AUTO CONTENT-AWARE MERGER
Automatically merges and removes duplicates without user interaction
"""

import difflib
import hashlib
import json
import os
import shutil
from collections import defaultdict
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Tuple


class AutoContentMerger:
    def __init__(self, base_path: str, backup_path: Optional[str] = None):
        self.base_path = Path(base_path)
        self.backup_path = (
            Path(backup_path) if backup_path else self.base_path / "BACKUP_BEFORE_MERGE"
        )
        self.merge_log = []
        self.removal_log = []

        # Merge strategies
        self.merge_strategies = {
            "documents": {
                "similarity_threshold": 0.80,
                "merge_threshold": 0.90,
                "keep_strategy": "newest_largest",
            },
            "html_files": {
                "similarity_threshold": 0.85,
                "merge_threshold": 0.95,
                "keep_strategy": "newest_largest",
            },
            "images": {
                "similarity_threshold": 1.0,
                "merge_threshold": 1.0,
                "keep_strategy": "newest_largest",
            },
        }

    def create_backup(self):
        """Create backup before any operations"""
        if self.backup_path.exists():
            print(f"⚠️  Backup already exists at {self.backup_path}")
            return

        print(f"💾 Creating backup at {self.backup_path}...")
        self.backup_path.mkdir(exist_ok=True)

        # Backup each folder
        for folder in ["documents", "html_files", "images"]:
            src = self.base_path / folder
            dst = self.backup_path / folder
            if src.exists():
                shutil.copytree(src, dst)
                print(f"   ✅ Backed up {folder}/")

    def read_text_file(self, filepath: Path) -> Optional[str]:
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

    def calculate_similarity(self, text1: str, text2: str) -> float:
        """Calculate similarity ratio between two texts"""
        return difflib.SequenceMatcher(None, text1, text2).ratio()

    def get_file_quality_score(self, filepath: Path, content: str = None) -> Dict:
        """Calculate quality score for a file to determine which to keep"""
        stat = filepath.stat()

        score = {
            "path": str(filepath),
            "name": filepath.name,
            "size": stat.st_size,
            "modified": datetime.fromtimestamp(stat.st_mtime),
            "size_score": stat.st_size,
            "time_score": stat.st_mtime,
            "completeness_score": 0,
            "total_score": 0,
        }

        if content:
            lines = content.split("\n")
            non_empty_lines = [line for line in lines if line.strip()]
            score["completeness_score"] = len(non_empty_lines)

            if any(line.startswith("#") for line in lines):
                score["completeness_score"] += 10
            if any(line.startswith("-") or line.startswith("*") for line in lines):
                score["completeness_score"] += 5

        score["total_score"] = (
            score["size_score"] * 0.3
            + score["time_score"] * 0.4
            + score["completeness_score"] * 0.3
        )

        return score

    def find_best_file(
        self, files: List[Dict], strategy: str = "newest_largest"
    ) -> Dict:
        """Find the best file to keep based on strategy"""
        if not files:
            return None

        if len(files) == 1:
            return files[0]

        scored_files = []
        for file_info in files:
            filepath = Path(file_info["path"])
            content = (
                self.read_text_file(filepath)
                if filepath.suffix in [".txt", ".md", ".html"]
                else None
            )
            score = self.get_file_quality_score(filepath, content)
            scored_files.append({**file_info, **score})

        if strategy == "newest_largest":
            scored_files.sort(
                key=lambda x: (x["time_score"], x["size_score"]), reverse=True
            )
        elif strategy == "newest":
            scored_files.sort(key=lambda x: x["time_score"], reverse=True)
        elif strategy == "largest":
            scored_files.sort(key=lambda x: x["size_score"], reverse=True)
        elif strategy == "most_complete":
            scored_files.sort(key=lambda x: x["total_score"], reverse=True)

        return scored_files[0]

    def process_duplicate_group(self, group: Dict, content_type: str) -> Dict:
        """Process a group of duplicate files"""
        files = group["files"]
        strategy = self.merge_strategies[content_type]["keep_strategy"]
        merge_threshold = self.merge_strategies[content_type]["merge_threshold"]

        best_file = self.find_best_file(files, strategy)

        should_merge = False
        if content_type in ["documents", "html_files"] and len(files) > 1:
            contents = []
            for file_info in files:
                filepath = Path(file_info["path"])
                content = self.read_text_file(filepath)
                if content:
                    contents.append(content)

            if contents:
                similarities = []
                for i in range(len(contents)):
                    for j in range(i + 1, len(contents)):
                        sim = self.calculate_similarity(contents[i], contents[j])
                        similarities.append(sim)

                if similarities:
                    avg_similarity = sum(similarities) / len(similarities)
                    should_merge = avg_similarity >= merge_threshold

        result = {
            "action": "merge" if should_merge else "remove_duplicates",
            "keep_file": best_file,
            "remove_files": [f for f in files if f["path"] != best_file["path"]],
            "space_saved": sum(
                f["size"] for f in files if f["path"] != best_file["path"]
            ),
        }

        return result

    def execute_removal(self, action: Dict, content_type: str) -> bool:
        """Execute file removal"""
        try:
            keep_file = Path(action["keep_file"]["path"])

            for file_info in action["remove_files"]:
                filepath = Path(file_info["path"])
                if filepath.exists():
                    filepath.unlink()
                    print(f"   🗑️  Removed {filepath.name}")
                    self.removal_log.append(
                        {
                            "removed": str(filepath),
                            "kept": str(keep_file),
                            "action": action["action"],
                            "timestamp": datetime.now().isoformat(),
                        }
                    )

            self.merge_log.append(
                {
                    "kept_file": str(keep_file),
                    "removed_count": len(action["remove_files"]),
                    "space_saved": action["space_saved"],
                    "action": action["action"],
                    "timestamp": datetime.now().isoformat(),
                }
            )

            return True

        except Exception as e:
            print(f"❌ Error executing action: {e}")
            return False

    def process_content_type(
        self, content_type: str, duplicate_groups: List[Dict]
    ) -> Dict:
        """Process all duplicate groups for a content type"""
        print(f"\n🔧 Processing {content_type}...")

        stats = {
            "total_groups": len(duplicate_groups),
            "processed_groups": 0,
            "total_space_saved": 0,
            "total_files_removed": 0,
            "merged_files": 0,
        }

        for i, group in enumerate(duplicate_groups):
            print(f"   Processing group {i+1}/{len(duplicate_groups)}...")

            action = self.process_duplicate_group(group, content_type)

            if action["action"] == "merge":
                stats["merged_files"] += 1
                print(f"   🔀 Merging {len(group['files'])} files")
            else:
                print(f"   🗑️  Removing {len(action['remove_files'])} duplicates")

            if self.execute_removal(action, content_type):
                stats["processed_groups"] += 1
                stats["total_space_saved"] += action["space_saved"]
                stats["total_files_removed"] += len(action["remove_files"])

        return stats

    def generate_merge_report(self, all_stats: Dict):
        """Generate comprehensive merge report"""
        report_lines = []
        report_lines.append("# 🧠 AUTO CONTENT-AWARE MERGE & REMOVAL REPORT")
        report_lines.append(
            f"\n**Merge Date:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
        )
        report_lines.append(f"\n---\n")

        total_space_saved = sum(
            stats.get("total_space_saved", 0) for stats in all_stats.values()
        )
        total_files_removed = sum(
            stats.get("total_files_removed", 0) for stats in all_stats.values()
        )
        total_merged = sum(stats.get("merged_files", 0) for stats in all_stats.values())

        report_lines.append("## 📊 MERGE SUMMARY\n")
        report_lines.append(f"- **Total Files Removed:** {total_files_removed}")
        report_lines.append(f"- **Total Files Merged:** {total_merged}")
        report_lines.append(
            f"- **Total Space Saved:** {round(total_space_saved / (1024 * 1024), 2)} MB"
        )
        report_lines.append(f"- **Backup Location:** {self.backup_path}\n")

        for content_type, stats in all_stats.items():
            report_lines.append(f"## {content_type.upper().replace('_', ' ')} STATS\n")
            report_lines.append(
                f"- **Groups Processed:** {stats.get('processed_groups', 0)}/{stats.get('total_groups', 0)}"
            )
            report_lines.append(
                f"- **Files Removed:** {stats.get('total_files_removed', 0)}"
            )
            report_lines.append(f"- **Files Merged:** {stats.get('merged_files', 0)}")
            report_lines.append(
                f"- **Space Saved:** {round(stats.get('total_space_saved', 0) / (1024 * 1024), 2)} MB\n"
            )

        if self.merge_log:
            report_lines.append("## 📝 ACTION LOG\n")
            for entry in self.merge_log:
                report_lines.append(
                    f"- **{entry['timestamp']}**: {entry['action']} - Kept `{Path(entry['kept_file']).name}`, removed {entry['removed_count']} files, saved {round(entry['space_saved']/(1024*1024), 2)} MB"
                )

        report_path = self.base_path / "AUTO_MERGE_REPORT.md"
        with open(report_path, "w", encoding="utf-8") as f:
            f.write("\n".join(report_lines))

        print(f"\n✅ Auto merge report saved to: {report_path}")

    def run_auto_merge(self, duplicate_data: Dict):
        """Run the complete auto merge operation"""
        print("=" * 60)
        print("🤖 STARTING AUTO CONTENT-AWARE MERGE OPERATION")
        print("=" * 60)

        self.create_backup()

        all_stats = {}

        for content_type in ["images", "documents", "html_files"]:
            if content_type in duplicate_data and duplicate_data[content_type].get(
                "duplicates"
            ):
                duplicate_groups = duplicate_data[content_type]["duplicates"]
                stats = self.process_content_type(content_type, duplicate_groups)
                all_stats[content_type] = stats

        self.generate_merge_report(all_stats)

        print("\n" + "=" * 60)
        print("✅ AUTO MERGE OPERATION COMPLETE!")
        print("=" * 60)

        total_space_saved = sum(
            stats.get("total_space_saved", 0) for stats in all_stats.values()
        )
        total_files_removed = sum(
            stats.get("total_files_removed", 0) for stats in all_stats.values()
        )

        print(f"\n🎯 RESULTS:")
        print(
            f"   💾 Total space saved: {round(total_space_saved / (1024 * 1024), 2)} MB"
        )
        print(f"   🗑️  Total files removed: {total_files_removed}")
        print(f"   💾 Backup created at: {self.backup_path}")


if __name__ == "__main__":
    base_path = "/Users/steven/tehSiTes/New_Folder_With_Items_3_ORGANIZED"
    duplicate_report_path = Path(base_path) / "DUPLICATE_ANALYSIS_REPORT.json"

    if not duplicate_report_path.exists():
        print("❌ Duplicate analysis report not found. Please run the analysis first.")
        exit(1)

    with open(duplicate_report_path, "r", encoding="utf-8") as f:
        duplicate_data = json.load(f)

    merger = AutoContentMerger(base_path)
    merger.run_auto_merge(duplicate_data)
