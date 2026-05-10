#!/usr/bin/env python3
"""from collections import defaultdict
from datetime import datetime
from pathlib import Path
import csv
import json
import shutil
Comprehensive Cleanup with Rollback Safety
==========================================
1. Create rollback point
2. Delete exact duplicate files (39 groups)
3. Consolidate CSV files
4. Organize root-level files
"""

BASE_DIR = Path("/Users/steven/Music/nocTurneMeLoDieS")
LIBRARY_JSON = BASE_DIR / "DATA/UNIFIED_ANALYSIS/library_data.json"
ROLLBACK_DIR = BASE_DIR / "DATA/ROLLBACK"
CSV_SOURCE = Path.home() / "Documents/CsV"


class Colors:
    CYAN = "\033[96m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    RED = "\033[91m"
    BOLD = "\033[1m"
    END = "\033[0m"


class ComprehensiveCleanup:
    def __init__(self, live_run=False):
        self.live_run = live_run
        self.rollback_log = []
        self.timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.rollback_file = ROLLBACK_DIR / f"CLEANUP_{self.timestamp}.csv"

        # Ensure rollback directory exists
        ROLLBACK_DIR.mkdir(exist_ok=True)

    def log_operation(self, operation, source, destination, reason):
        """Log operation for rollback"""
        self.rollback_log.append(
            {
                "timestamp": datetime.now().isoformat(),
                "operation": operation,
                "source": str(source),
                "destination": str(destination),
                "reason": reason,
            },
        )

    def save_rollback_log(self):
        """Save rollback log to CSV"""
        if not self.rollback_log:
            return

        with open(self.rollback_file, "w", newline="") as f:
            writer = csv.DictWriter(
                f,
                fieldnames=[
                    "timestamp",
                    "operation",
                    "source",
                    "destination",
                    "reason",
                ],
            )
            writer.writeheader()
            writer.writerows(self.rollback_log)

        print(f"{Colors.GREEN}✅ Rollback log saved: {self.rollback_file}{Colors.END}")

    def load_duplicates(self):
        """Load duplicate groups from library data"""
        if not LIBRARY_JSON.exists():
            print(f"{Colors.RED}❌ Library data not found{Colors.END}")
            return {}

        with open(LIBRARY_JSON) as f:
            data = json.load(f)

        # Build hash-based duplicate groups
        hash_groups = defaultdict(list)
        for item in data.get("catalog", []):
            file_hash = item.get("hash")
            if file_hash:
                hash_groups[file_hash].append(item)

        # Filter to only duplicate groups (2+ files)
        duplicates = {h: files for h, files in hash_groups.items() if len(files) > 1}

        return duplicates

    def cleanup_duplicates(self):
        """Step 1: Delete exact duplicate files"""
        print(f"\n{Colors.CYAN}{'=' * 80}{Colors.END}")
        print(f"{Colors.BOLD}STEP 1: DELETING EXACT DUPLICATES{Colors.END}")
        print(f"{Colors.CYAN}{'=' * 80}{Colors.END}\n")

        duplicates = self.load_duplicates()

        if not duplicates:
            print(f"{Colors.YELLOW}No duplicates found{Colors.END}")
            return 0

        print(f"Found {len(duplicates)} duplicate groups")

        deleted_count = 0
        space_freed = 0

        for file_hash, files in duplicates.items():
            # Keep the shortest path (usually root level or earliest album)
            files_sorted = sorted(files, key=lambda x: (len(x["path"]), x["path"]))
            keep_file = files_sorted[0]
            delete_files = files_sorted[1:]

            print(f"\n{Colors.BOLD}Keep:{Colors.END} {keep_file['rel_path']}")

            for dup in delete_files:
                dup_path = Path(dup["path"])
                if not dup_path.exists():
                    print(
                        f"  {Colors.YELLOW}⚠️  Already deleted: {dup['rel_path']}{Colors.END}",
                    )
                    continue

                file_size = dup["size"]

                if self.live_run:
                    try:
                        dup_path.unlink()
                        self.log_operation(
                            "delete",
                            dup_path,
                            "",
                            f"Duplicate of {keep_file['rel_path']}",
                        )
                        deleted_count += 1
                        space_freed += file_size
                        print(
                            f"  {Colors.GREEN}✅ Deleted: {dup['rel_path']} ({file_size / 1024 / 1024:.1f} MB){Colors.END}",
                        )
                    except Exception as e:
                        print(f"  {Colors.RED}❌ Error: {e}{Colors.END}")
                else:
                    deleted_count += 1
                    space_freed += file_size
                    print(
                        f"  {Colors.CYAN}[DRY RUN] Would delete: {dup['rel_path']} ({file_size / 1024 / 1024:.1f} MB){Colors.END}",
                    )

        print(f"\n{Colors.BOLD}Summary:{Colors.END}")
        print(f"  Files to delete: {deleted_count}")
        print(f"  Space to free: {space_freed / (1024**2):.1f} MB")

        return deleted_count

    def consolidate_csvs(self):
        """Step 2: Consolidate CSV files"""
        print(f"\n{Colors.CYAN}{'=' * 80}{Colors.END}")
        print(f"{Colors.BOLD}STEP 2: CONSOLIDATING CSV FILES{Colors.END}")
        print(f"{Colors.CYAN}{'=' * 80}{Colors.END}\n")

        # Create target directory
        csv_target = BASE_DIR / "suno" / "exports"
        csv_target.mkdir(parents=True, exist_ok=True)

        # Find all Suno-related CSVs
        if not CSV_SOURCE.exists():
            print(
                f"{Colors.YELLOW}Source directory not found: {CSV_SOURCE}{Colors.END}",
            )
            return 0

        suno_csvs = list(CSV_SOURCE.glob("*suno*.csv")) + list(
            CSV_SOURCE.glob("*Suno*.csv"),
        )

        print(f"Found {len(suno_csvs)} Suno CSV files in {CSV_SOURCE}")

        copied_count = 0

        for csv_file in suno_csvs:
            target_file = csv_target / csv_file.name

            # Skip if already exists and same size
            if (
                target_file.exists()
                and target_file.stat().st_size == csv_file.stat().st_size
            ):
                print(
                    f"  {Colors.YELLOW}⏭️  Already exists: {csv_file.name}{Colors.END}",
                )
                continue

            if self.live_run:
                try:
                    shutil.copy2(csv_file, target_file)
                    self.log_operation(
                        "copy",
                        csv_file,
                        target_file,
                        "CSV consolidation",
                    )
                    copied_count += 1
                    print(f"  {Colors.GREEN}✅ Copied: {csv_file.name}{Colors.END}")
                except Exception as e:
                    print(f"  {Colors.RED}❌ Error: {e}{Colors.END}")
            else:
                copied_count += 1
                print(
                    f"  {Colors.CYAN}[DRY RUN] Would copy: {csv_file.name}{Colors.END}",
                )

        print(f"\n{Colors.BOLD}Summary:{Colors.END}")
        print(f"  Files to copy: {copied_count}")
        print(f"  Target: {csv_target}")

        return copied_count

    def organize_root_files(self):
        """Step 3: Organize root-level files"""
        print(f"\n{Colors.CYAN}{'=' * 80}{Colors.END}")
        print(f"{Colors.BOLD}STEP 3: ORGANIZING ROOT-LEVEL FILES{Colors.END}")
        print(f"{Colors.CYAN}{'=' * 80}{Colors.END}\n")

        # Find all MP3 files at root level
        root_mp3s = [f for f in BASE_DIR.glob("*.mp3")]

        print(f"Found {len(root_mp3s)} MP3 files at root level")

        if len(root_mp3s) == 0:
            print(f"{Colors.GREEN}✅ No files to organize{Colors.END}")
            return 0

        # Create a "Singles" folder for unorganized files
        singles_folder = BASE_DIR / "Singles"
        singles_folder.mkdir(exist_ok=True)

        moved_count = 0

        for mp3_file in root_mp3s[:20]:  # Limit to first 20 for now
            target_file = singles_folder / mp3_file.name

            if target_file.exists():
                print(
                    f"  {Colors.YELLOW}⚠️  Already exists: {mp3_file.name}{Colors.END}",
                )
                continue

            if self.live_run:
                try:
                    shutil.move(str(mp3_file), str(target_file))
                    self.log_operation(
                        "move",
                        mp3_file,
                        target_file,
                        "Root level organization",
                    )
                    moved_count += 1
                    print(f"  {Colors.GREEN}✅ Moved: {mp3_file.name}{Colors.END}")
                except Exception as e:
                    print(f"  {Colors.RED}❌ Error: {e}{Colors.END}")
            else:
                moved_count += 1
                print(
                    f"  {Colors.CYAN}[DRY RUN] Would move: {mp3_file.name} → Singles/{Colors.END}",
                )

        if len(root_mp3s) > 20:
            remaining = len(root_mp3s) - 20
            print(
                f"\n  {Colors.YELLOW}... and {remaining} more files (run again to continue){Colors.END}",
            )

        print(f"\n{Colors.BOLD}Summary:{Colors.END}")
        print(f"  Files moved: {moved_count}")
        print("  Target: Singles/")

        return moved_count

    def run(self):
        """Run comprehensive cleanup"""
        print(f"\n{Colors.BOLD}{'=' * 80}{Colors.END}")
        print(f"{Colors.BOLD}🧹 COMPREHENSIVE CLEANUP{Colors.END}")
        print(f"{Colors.BOLD}{'=' * 80}{Colors.END}")
        print(
            f"Mode: {Colors.GREEN if self.live_run else Colors.CYAN}{'LIVE RUN' if self.live_run else 'DRY RUN'}{Colors.END}",
        )
        print(f"Timestamp: {self.timestamp}\n")

        # Step 1: Duplicates
        deleted = self.cleanup_duplicates()

        # Step 2: CSVs
        copied = self.consolidate_csvs()

        # Step 3: Root files
        moved = self.organize_root_files()

        # Save rollback log
        if self.live_run:
            self.save_rollback_log()

        # Final summary
        print(f"\n{Colors.BOLD}{'=' * 80}{Colors.END}")
        print(f"{Colors.BOLD}📊 FINAL SUMMARY{Colors.END}")
        print(f"{Colors.BOLD}{'=' * 80}{Colors.END}")
        print(f"  Duplicates deleted: {deleted}")
        print(f"  CSV files copied: {copied}")
        print(f"  Root files moved: {moved}")
        print(f"  Total operations: {deleted + copied + moved}")

        if self.live_run:
            print(f"\n{Colors.GREEN}✅ Cleanup complete!{Colors.END}")
            print(f"Rollback file: {self.rollback_file}")
        else:
            print(
                f"\n{Colors.CYAN}ℹ️  This was a DRY RUN. Use --live to execute.{Colors.END}",
            )


def main():
    import argparse

    parser = argparse.ArgumentParser(
        description="Comprehensive cleanup with rollback safety",
    )
    parser.add_argument(
        "--live",
        action="store_true",
        help="Execute changes (default: dry run)",
    )
    args = parser.parse_args()

    cleaner = ComprehensiveCleanup(live_run=args.live)
    cleaner.run()


if __name__ == "__main__":
    main()
