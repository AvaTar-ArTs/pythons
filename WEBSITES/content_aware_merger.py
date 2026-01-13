#!/usr/bin/env python3
"""
🧠 CONTENT-AWARE DIFF, MERGE & REMOVE SYSTEM
Intelligently merges similar content and removes duplicates while preserving the best versions
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


class ContentAwareMerger:
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
                "keep_strategy": "newest_largest",  # newest_largest, newest, largest, most_complete
            },
            "html_files": {
                "similarity_threshold": 0.85,
                "merge_threshold": 0.95,
                "keep_strategy": "newest_largest",
            },
            "images": {
                "similarity_threshold": 1.0,  # Only exact duplicates for images
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

    def calculate_file_hash(self, filepath: Path) -> Optional[str]:
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
            # Completeness based on content length and structure
            lines = content.split("\n")
            non_empty_lines = [line for line in lines if line.strip()]
            score["completeness_score"] = len(non_empty_lines)

            # Bonus for structured content (headers, lists, etc.)
            if any(line.startswith("#") for line in lines):  # Markdown headers
                score["completeness_score"] += 10
            if any(
                line.startswith("-") or line.startswith("*") for line in lines
            ):  # Lists
                score["completeness_score"] += 5

        # Calculate total score (weighted)
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

        # Calculate quality scores
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

        # Sort by strategy
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

    def create_merged_content(self, files: List[Dict], content_type: str) -> str:
        """Create merged content from similar files"""
        if not files:
            return ""

        # Read all file contents
        contents = []
        for file_info in files:
            filepath = Path(file_info["path"])
            content = self.read_text_file(filepath)
            if content:
                contents.append(
                    {
                        "content": content,
                        "name": filepath.name,
                        "modified": file_info["modified"],
                    }
                )

        if not contents:
            return ""

        # Sort by modification date (newest first)
        contents.sort(key=lambda x: x["modified"], reverse=True)

        if content_type == "documents":
            return self.merge_document_content(contents)
        elif content_type == "html_files":
            return self.merge_html_content(contents)
        else:
            return contents[0]["content"]  # For images, just return the best one

    def merge_document_content(self, contents: List[Dict]) -> str:
        """Merge document content intelligently"""
        if len(contents) == 1:
            return contents[0]["content"]

        # Use the newest content as base
        base_content = contents[0]["content"]
        base_lines = base_content.split("\n")

        # Find unique content from other files
        merged_lines = base_lines.copy()
        added_content = set()

        for content_info in contents[1:]:
            other_content = content_info["content"]
            other_lines = other_content.split("\n")

            for line in other_lines:
                line_stripped = line.strip()
                if line_stripped and line_stripped not in added_content:
                    # Check if this line adds new information
                    if not any(line_stripped in base_line for base_line in base_lines):
                        merged_lines.append(
                            f"\n<!-- Added from {content_info['name']} -->"
                        )
                        merged_lines.append(line)
                        added_content.add(line_stripped)

        return "\n".join(merged_lines)

    def merge_html_content(self, contents: List[Dict]) -> str:
        """Merge HTML content intelligently"""
        if len(contents) == 1:
            return contents[0]["content"]

        # Use the newest content as base
        base_content = contents[0]["content"]

        # For HTML, we'll be more conservative and just keep the best version
        # unless they're very similar (95%+)
        similarities = []
        for content_info in contents[1:]:
            similarity = self.calculate_similarity(
                base_content, content_info["content"]
            )
            similarities.append(similarity)

        # If all are very similar, merge; otherwise keep the best
        if all(sim > 0.95 for sim in similarities):
            return self.merge_document_content(contents)
        else:
            return base_content

    def process_duplicate_group(self, group: Dict, content_type: str) -> Dict:
        """Process a group of duplicate files"""
        files = group["files"]
        strategy = self.merge_strategies[content_type]["keep_strategy"]
        merge_threshold = self.merge_strategies[content_type]["merge_threshold"]

        # Find the best file to keep
        best_file = self.find_best_file(files, strategy)

        # Check if we should merge or just remove duplicates
        should_merge = False
        if content_type in ["documents", "html_files"] and len(files) > 1:
            # Check similarity between files
            contents = []
            for file_info in files:
                filepath = Path(file_info["path"])
                content = self.read_text_file(filepath)
                if content:
                    contents.append(content)

            if contents:
                # Calculate average similarity
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
            "merged_content": None,
            "space_saved": sum(
                f["size"] for f in files if f["path"] != best_file["path"]
            ),
        }

        if should_merge:
            result["merged_content"] = self.create_merged_content(files, content_type)

        return result

    def execute_removal(self, action: Dict, content_type: str) -> bool:
        """Execute file removal/merging"""
        try:
            keep_file = Path(action["keep_file"]["path"])

            # If merging, update the kept file with merged content
            if action["action"] == "merge" and action["merged_content"]:
                with open(keep_file, "w", encoding="utf-8") as f:
                    f.write(action["merged_content"])
                print(f"   📝 Merged content into {keep_file.name}")

            # Remove duplicate files
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

            # Execute the action
            if self.execute_removal(action, content_type):
                stats["processed_groups"] += 1
                stats["total_space_saved"] += action["space_saved"]
                stats["total_files_removed"] += len(action["remove_files"])

        return stats

    def generate_merge_report(self, all_stats: Dict):
        """Generate comprehensive merge report"""
        report_lines = []
        report_lines.append("# 🧠 CONTENT-AWARE MERGE & REMOVAL REPORT")
        report_lines.append(
            f"\n**Merge Date:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
        )
        report_lines.append(f"\n---\n")

        # Summary
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

        # Detailed stats for each content type
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

        # Action log
        if self.merge_log:
            report_lines.append("## 📝 ACTION LOG\n")
            for entry in self.merge_log:
                report_lines.append(
                    f"- **{entry['timestamp']}**: {entry['action']} - Kept `{Path(entry['kept_file']).name}`, removed {entry['removed_count']} files, saved {round(entry['space_saved']/(1024*1024), 2)} MB"
                )

        # Save report
        report_path = self.base_path / "CONTENT_MERGE_REPORT.md"
        with open(report_path, "w", encoding="utf-8") as f:
            f.write("\n".join(report_lines))

        print(f"\n✅ Merge report saved to: {report_path}")

    def run_merge_operation(self, duplicate_data: Dict, dry_run: bool = False):
        """Run the complete merge operation"""
        print("=" * 60)
        print("🧠 STARTING CONTENT-AWARE MERGE OPERATION")
        print("=" * 60)

        if dry_run:
            print("🔍 DRY RUN MODE - No files will be modified")
        else:
            self.create_backup()

        all_stats = {}

        # Process each content type
        for content_type in ["images", "documents", "html_files"]:
            if content_type in duplicate_data and duplicate_data[content_type].get(
                "duplicates"
            ):
                duplicate_groups = duplicate_data[content_type]["duplicates"]

                if dry_run:
                    print(
                        f"\n🔍 DRY RUN: Would process {len(duplicate_groups)} {content_type} groups"
                    )
                    # Simulate stats
                    all_stats[content_type] = {
                        "total_groups": len(duplicate_groups),
                        "processed_groups": len(duplicate_groups),
                        "total_space_saved": sum(
                            group.get("total_wasted", 0) for group in duplicate_groups
                        ),
                        "total_files_removed": sum(
                            group.get("count", 0) - 1 for group in duplicate_groups
                        ),
                        "merged_files": 0,
                    }
                else:
                    stats = self.process_content_type(content_type, duplicate_groups)
                    all_stats[content_type] = stats

        # Generate report
        self.generate_merge_report(all_stats)

        print("\n" + "=" * 60)
        print("✅ MERGE OPERATION COMPLETE!")
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
        if not dry_run:
            print(f"   💾 Backup created at: {self.backup_path}")


if __name__ == "__main__":
    # Load the duplicate analysis results
    base_path = "/Users/steven/tehSiTes/New_Folder_With_Items_3_ORGANIZED"
    duplicate_report_path = Path(base_path) / "DUPLICATE_ANALYSIS_REPORT.json"

    if not duplicate_report_path.exists():
        print("❌ Duplicate analysis report not found. Please run the analysis first.")
        exit(1)

    # Load duplicate data
    with open(duplicate_report_path, "r", encoding="utf-8") as f:
        duplicate_data = json.load(f)

    # Create merger
    merger = ContentAwareMerger(base_path)

    # Ask user for confirmation
    print("🧠 CONTENT-AWARE MERGE & REMOVAL SYSTEM")
    print("=" * 50)
    print("This will:")
    print("1. Create a backup of all files")
    print("2. Remove exact duplicates (keeping the best version)")
    print("3. Merge similar content intelligently")
    print("4. Generate a detailed report")
    print()

    choice = input(
        "Choose an option:\n1. Dry run (preview only)\n2. Execute merge\n3. Cancel\nEnter choice (1-3): "
    ).strip()

    if choice == "1":
        merger.run_merge_operation(duplicate_data, dry_run=True)
    elif choice == "2":
        confirm = (
            input("⚠️  This will modify your files. Are you sure? (yes/no): ")
            .strip()
            .lower()
        )
        if confirm == "yes":
            merger.run_merge_operation(duplicate_data, dry_run=False)
        else:
            print("❌ Operation cancelled.")
    else:
        print("❌ Operation cancelled.")
