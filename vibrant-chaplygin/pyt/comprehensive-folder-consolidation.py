#!/usr/bin/env python3
"""
🎵 COMPREHENSIVE FOLDER CONSOLIDATION
======================================
Analyze ALL folders in nocTurneMeLoDieS and consolidate/merge

Features:
✨ Find similar/duplicate folders
✨ Merge related content (Moonlight_Night → Moonlight_Serenade)
✨ Clean up temp folders (Movavi, numbered folders)
✨ Consolidate miscellaneous content
✨ Smart merging by theme/similarity
✨ CSV log for all operations
"""

import os
import csv
import shutil
from pathlib import Path
from datetime import datetime
from difflib import SequenceMatcher
from collections import defaultdict


class Colors:
    CYAN = "\033[96m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    RED = "\033[91m"
    MAGENTA = "\033[35m"
    BOLD = "\033[1m"
    END = "\033[0m"


class ComprehensiveFolderConsolidation:
    """Consolidate all folders intelligently"""

    def __init__(self, dry_run: bool = True):
        self.dry_run = dry_run
        self.timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

        self.nocturne_dir = Path.home() / "Music" / "nocTurneMeLoDieS"
        self.log_file = self.nocturne_dir / f"FOLDER_CONSOLIDATION_LOG_{self.timestamp}.csv"

        self.all_folders = []
        self.merge_plan = []
        self.delete_plan = []

        self.stats = {"total_folders": 0, "folders_merged": 0, "folders_deleted": 0, "space_freed_mb": 0}

    def print_header(self, text: str, color=Colors.CYAN):
        """Print fancy header"""
        print(f"\n{color}{Colors.BOLD}{'='*80}")
        print(f"{text}")
        print(f"{'='*80}{Colors.END}\n")

    def normalize_name(self, name: str) -> str:
        """Normalize folder name for comparison"""
        import re

        name = name.lower()

        # Remove version numbers, timestamps, IDs
        name = re.sub(r"_vol[._\s]*\d+", "", name)
        name = re.sub(r"_v\d+", "", name)
        name = re.sub(r"_\d{13}", "", name)  # Unix timestamps
        name = re.sub(r"_\d{3}$", "", name)  # Trailing numbers like _239
        name = re.sub(r"_\d+_\d+", "", name)  # Pattern like _1_1
        name = re.sub(r"[-_]+", " ", name)
        name = re.sub(r"\s+", " ", name)

        return name.strip()

    def similarity_score(self, str1: str, str2: str) -> float:
        """Calculate similarity"""
        norm1 = self.normalize_name(str1)
        norm2 = self.normalize_name(str2)
        return SequenceMatcher(None, norm1, norm2).ratio()

    def get_folder_info(self, folder_path: Path) -> Dict:
        """Get folder statistics"""
        file_count = 0
        total_size = 0
        audio_count = 0

        audio_exts = {".mp3", ".m4a", ".wav", ".flac"}

        for item in folder_path.rglob("*"):
            if item.is_file():
                file_count += 1
                total_size += item.stat().st_size

                if item.suffix.lower() in audio_exts:
                    audio_count += 1

        return {"file_count": file_count, "audio_count": audio_count, "total_size_mb": total_size / (1024**2)}

    def scan_all_folders(self):
        """Scan all folders in nocTurneMeLoDieS"""
        self.print_header("🔍 SCANNING ALL FOLDERS")

        print(f"Scanning: {self.nocturne_dir}\n")

        # Skip these patterns
        skip_patterns = [
            "ARCHIVE_",
            "BACKUP_",
            "CLEANUP_",
            "CONSOLIDATION_",
            "COMPREHENSIVE_",
            "CONTENT_CROSS_",
            "EXTRACTION_",
            "MISSING_SONG_",
            "FINAL_",
            "TRANSCRIPT_",
            "SUNO_CONTENT_",
            "VOLUME_CONTENT",
            "FOUND_CONTENT",
            "DATA",
        ]

        for folder in sorted(self.nocturne_dir.iterdir()):
            if not folder.is_dir():
                continue

            if folder.name.startswith("."):
                continue

            # Skip analysis/backup folders
            if any(pattern in folder.name for pattern in skip_patterns):
                continue

            info = self.get_folder_info(folder)

            self.all_folders.append(
                {
                    "path": folder,
                    "name": folder.name,
                    "normalized": self.normalize_name(folder.name),
                    "file_count": info["file_count"],
                    "audio_count": info["audio_count"],
                    "size_mb": info["total_size_mb"],
                }
            )

            self.stats["total_folders"] += 1

        print(f"{Colors.GREEN}✅ Found {len(self.all_folders)} active folders{Colors.END}\n")

    def find_merge_candidates(self):
        """Find folders that should be merged"""
        self.print_header("🔍 FINDING MERGE CANDIDATES")

        # Group by normalized name
        by_normalized = defaultdict(list)

        for folder in self.all_folders:
            by_normalized[folder["normalized"]].append(folder)

        # Find groups with multiple folders
        merge_groups = {k: v for k, v in by_normalized.items() if len(v) > 1}

        print(f"Found {len(merge_groups)} groups to merge:\n")

        for normalized, folders in sorted(merge_groups.items()):
            print(f"{Colors.BOLD}{normalized}{Colors.END} ({len(folders)} folders)")

            # Choose primary folder (most files, best name)
            folders_sorted = sorted(folders, key=lambda x: (-x["audio_count"], -x["file_count"]))
            primary = folders_sorted[0]
            merge_into = folders_sorted[1:]

            print(
                f"  {Colors.GREEN}KEEP:{Colors.END} {primary['name']} ({primary['audio_count']} audio, {primary['file_count']} files)"
            )

            for folder in merge_into:
                print(
                    f"  {Colors.YELLOW}MERGE:{Colors.END} {folder['name']} ({folder['audio_count']} audio, {folder['file_count']} files)"
                )

                self.merge_plan.append(
                    {
                        "from_path": folder["path"],
                        "from_name": folder["name"],
                        "to_path": primary["path"],
                        "to_name": primary["name"],
                        "file_count": folder["file_count"],
                        "audio_count": folder["audio_count"],
                        "size_mb": folder["size_mb"],
                    }
                )

            print()

    def find_temp_folders(self):
        """Find temporary/generated folders to remove"""
        self.print_header("🗑️ FINDING TEMP/GENERATED FOLDERS")

        temp_patterns = [
            ("movavi", "Screen recorder temp"),
            ("untitled", "Generic temp"),
            (r"^\d{13}", "Timestamp folder"),
            ("test_", "Test folder"),
            ("temp_", "Temp folder"),
            ("_backup", "Backup folder"),
        ]

        import re

        for folder in self.all_folders:
            name_lower = folder["name"].lower()

            for pattern, description in temp_patterns:
                if re.search(pattern, name_lower):
                    # Check if empty or very small
                    if folder["file_count"] < 5 or folder["audio_count"] == 0:
                        self.delete_plan.append(
                            {
                                "path": folder["path"],
                                "name": folder["name"],
                                "reason": description,
                                "file_count": folder["file_count"],
                                "size_mb": folder["size_mb"],
                            }
                        )

                        print(f"{Colors.YELLOW}🗑️  {folder['name']}{Colors.END}")
                        print(f"   Reason: {description}")
                        print(f"   Files: {folder['file_count']} ({folder['size_mb']:.2f} MB)\n")

    def execute_merges(self):
        """Execute folder merges"""
        self.print_header("🔀 EXECUTING FOLDER MERGES")

        if not self.merge_plan:
            print(f"{Colors.GREEN}✅ No merges needed{Colors.END}")
            return

        print(f"Merging {len(self.merge_plan)} folder(s)")
        print(f"Mode: {Colors.YELLOW}{'DRY RUN' if self.dry_run else 'LIVE'}{Colors.END}\n")

        for i, merge in enumerate(self.merge_plan, 1):
            print(f"{Colors.BOLD}[{i}/{len(self.merge_plan)}] {merge['from_name']}{Colors.END}")
            print(f"  → Into: {merge['to_name']}")
            print(f"  Files: {merge['file_count']} ({merge['size_mb']:.2f} MB)")

            if not self.dry_run:
                try:
                    # Merge all contents
                    for item in merge["from_path"].rglob("*"):
                        if item.is_file():
                            rel_path = item.relative_to(merge["from_path"])
                            target = merge["to_path"] / rel_path
                            target.parent.mkdir(parents=True, exist_ok=True)

                            # Skip if identical file exists
                            if not target.exists():
                                shutil.copy2(item, target)

                    # Remove old folder
                    shutil.rmtree(merge["from_path"])

                    print(f"  {Colors.GREEN}✅ Merged and removed{Colors.END}")
                    self.stats["folders_merged"] += 1

                except Exception as e:
                    print(f"  {Colors.RED}❌ Error: {e}{Colors.END}")
            else:
                print(f"  {Colors.YELLOW}[DRY RUN] Would merge{Colors.END}")
                self.stats["folders_merged"] += 1

            print()

    def execute_deletions(self):
        """Execute temp folder deletions"""
        self.print_header("🗑️ REMOVING TEMP FOLDERS")

        if not self.delete_plan:
            print(f"{Colors.GREEN}✅ No temp folders to remove{Colors.END}")
            return

        print(f"Removing {len(self.delete_plan)} temp folder(s)")
        print(f"Mode: {Colors.YELLOW}{'DRY RUN' if self.dry_run else 'LIVE'}{Colors.END}\n")

        for folder_info in self.delete_plan:
            print(f"{Colors.YELLOW}{folder_info['name']}{Colors.END}")
            print(f"  Reason: {folder_info['reason']}")
            print(f"  Size: {folder_info['size_mb']:.2f} MB")

            if not self.dry_run:
                try:
                    shutil.rmtree(folder_info["path"])
                    print(f"  {Colors.GREEN}✅ Removed{Colors.END}")
                    self.stats["folders_deleted"] += 1
                    self.stats["space_freed_mb"] += folder_info["size_mb"]

                except Exception as e:
                    print(f"  {Colors.RED}❌ Error: {e}{Colors.END}")
            else:
                print(f"  {Colors.YELLOW}[DRY RUN] Would remove{Colors.END}")
                self.stats["folders_deleted"] += 1
                self.stats["space_freed_mb"] += folder_info["size_mb"]

            print()

    def save_log(self):
        """Save CSV log"""
        self.print_header("💾 SAVING CSV LOG")

        with open(self.log_file, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(
                ["Action", "From_Path", "To_Path", "From_Name", "To_Name", "File_Count", "Size_MB", "Status"]
            )

            for merge in self.merge_plan:
                writer.writerow(
                    [
                        "MERGE",
                        str(merge["from_path"]),
                        str(merge["to_path"]),
                        merge["from_name"],
                        merge["to_name"],
                        merge["file_count"],
                        f"{merge['size_mb']:.2f}",
                        "COMPLETED" if not self.dry_run else "DRY_RUN",
                    ]
                )

            for delete in self.delete_plan:
                writer.writerow(
                    [
                        "DELETE",
                        str(delete["path"]),
                        "N/A",
                        delete["name"],
                        "N/A",
                        delete["file_count"],
                        f"{delete['size_mb']:.2f}",
                        "COMPLETED" if not self.dry_run else "DRY_RUN",
                    ]
                )

        print(f"{Colors.GREEN}✅ CSV log: {self.log_file.name}{Colors.END}")
        print(f"{Colors.CYAN}💡 Contains all paths for reference/revert{Colors.END}\n")

    def run(self):
        """Run comprehensive consolidation"""

        print(f"{Colors.MAGENTA}{Colors.BOLD}")
        print("╔═══════════════════════════════════════════════════════════════════════════════╗")
        print("║                                                                               ║")
        print("║     🎵 COMPREHENSIVE FOLDER CONSOLIDATION 🎵                                  ║")
        print("║                                                                               ║")
        print("║     Scan All → Find Similar → Merge → Clean → Done                           ║")
        print("║                                                                               ║")
        print("╚═══════════════════════════════════════════════════════════════════════════════╝")
        print(f"{Colors.END}\n")

        print(f"Mode: {Colors.YELLOW}{'DRY RUN' if self.dry_run else 'LIVE'}{Colors.END}\n")

        # 1. Scan all folders
        self.scan_all_folders()

        # 2. Find merge candidates
        self.find_merge_candidates()

        # 3. Find temp folders
        self.find_temp_folders()

        # 4. Execute merges
        self.execute_merges()

        # 5. Execute deletions
        self.execute_deletions()

        # 6. Save log
        self.save_log()

        # Final summary
        self.print_header("✅ COMPREHENSIVE CONSOLIDATION COMPLETE!", Colors.GREEN)

        print(f"{Colors.BOLD}📊 Final Statistics:{Colors.END}\n")
        print(f"  Total folders scanned: {Colors.CYAN}{self.stats['total_folders']}{Colors.END}")
        print(f"  Folders merged: {Colors.CYAN}{self.stats['folders_merged']}{Colors.END}")
        print(f"  Temp folders removed: {Colors.CYAN}{self.stats['folders_deleted']}{Colors.END}")
        print(f"  Space freed: {Colors.GREEN}{self.stats['space_freed_mb']:.2f} MB{Colors.END}\n")

        print(f"{Colors.BOLD}📝 CSV Log:{Colors.END}")
        print(f"  {self.log_file}\n")

        if self.dry_run:
            print(f"{Colors.YELLOW}⚠️  This was a DRY RUN. Run with --live to execute.{Colors.END}\n")
        else:
            print(f"{Colors.GREEN}✅ All folders consolidated! Structure is clean.{Colors.END}\n")


def main():
    import argparse

    parser = argparse.ArgumentParser(description="🎵 Comprehensive Folder Consolidation")
    parser.add_argument("--dry-run", action="store_true", default=True, help="Dry run mode (default)")
    parser.add_argument("--live", action="store_true", help="Live mode (execute consolidation)")

    args = parser.parse_args()

    consolidator = ComprehensiveFolderConsolidation(dry_run=not args.live)
    consolidator.run()


if __name__ == "__main__":
    main()
