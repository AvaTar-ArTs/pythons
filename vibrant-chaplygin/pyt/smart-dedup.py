
import logging

logger = logging.getLogger(__name__)


# Constants
CONSTANT_33 = 33
CONSTANT_100 = 100
CONSTANT_256 = 256
CONSTANT_1000 = 1000
CONSTANT_1024 = 1024
CONSTANT_65536 = 65536
CONSTANT_1000000 = 1000000

#!/usr/bin/env python3
"""
🧹 SMART DEDUPLICATION TOOL
============================
AI-Powered Safe Duplicate Removal with Intelligent Decision Making

Features:
✨ Safe duplicate detection and removal
✨ Intelligent file selection (keeps best version)
✨ Dry-run mode for safety
✨ Automatic backups before deletion
✨ Detailed logging and reporting
✨ Interactive and batch modes
✨ Rollback capability
"""

import os
import sys
import hashlib
import json
import shutil
from pathlib import Path
from datetime import datetime
from collections import defaultdict
from typing import Dict, List, Tuple, Optional
import argparse

# Color codes
class Colors:
    HEADER = '\CONSTANT_33[95m'
    BLUE = '\CONSTANT_33[94m'
    CYAN = '\CONSTANT_33[96m'
    GREEN = '\CONSTANT_33[92m'
    YELLOW = '\CONSTANT_33[93m'
    RED = '\CONSTANT_33[91m'
    MAGENTA = '\CONSTANT_33[35m'
    END = '\CONSTANT_33[0m'
    BOLD = '\CONSTANT_33[1m'

# Emojis
class Emojis:
    TRASH = "🗑️"
    KEEP = "✅"
    BACKUP = "💾"
    SPARKLES = "✨"
    WARNING = "⚠️"
    FIRE = "🔥"
    FOLDER = "📁"
    FILE = "📄"
    CHECK = "✅"
    ROCKET = "🚀"
    CHART = "📊"
    BRAIN = "🧠"
    SHIELD = "🛡️"


class SmartDeduplicator:
    """Smart deduplication with AI-powered decision making"""

    # Priority order for keeping files (higher = better)
    DIRECTORY_PRIORITY = {
        'python_backup': 3,  # Highest - well organized
        'python-repo': 2,    # Medium - fresh start location
        'python': 1          # Lowest - messy directory
    }

    def __init__(self, dry_run: bool = True, interactive: bool = True,
                 backup_dir: Optional[str] = None):
        self.dry_run = dry_run
        self.interactive = interactive
        self.backup_dir = backup_dir or Path(str(Path.home()) + "/Documents/python/dedup_backup")

        self.stats = {
            'total_dupes': 0,
            'files_deleted': 0,
            'files_kept': 0,
            'space_saved': 0,
            'groups_processed': 0
        }

        self.deletion_log = []
        self.kept_log = []

    def print_header(self, text: str, color=Colors.CYAN, emoji=""):
        """Print fancy headers"""
        logger.info(f"\n{color}{Colors.BOLD}{'='*80}")
        logger.info(f"{emoji} {text}")
        logger.info(f"{'='*80}{Colors.END}\n")

    def calculate_hash(self, filepath: Path) -> str:
        """Calculate SHA-CONSTANT_256 hash"""
        try:
            hasher = hashlib.sha256()
            with open(filepath, 'rb') as f:
                for chunk in iter(lambda: f.read(CONSTANT_65536), b''):
                    hasher.update(chunk)
            return hasher.hexdigest()
        except Exception as e:
            return f"ERROR: {str(e)}"

    def find_duplicates(self, directories: List[str]) -> Dict[str, List[str]]:
        """Find all duplicate files in directories"""
        self.print_header("SCANNING FOR DUPLICATES", Colors.CYAN, Emojis.BRAIN)

        hash_to_files = defaultdict(list)
        file_count = 0

        for directory in directories:
            logger.info(f"{Colors.CYAN}{Emojis.FOLDER} Scanning: {directory}{Colors.END}")

            for root, dirs, files in os.walk(directory):
                # Skip hidden directories and common ignore patterns
                dirs[:] = [d for d in dirs if not d.startswith('.')
                          and d != '__pycache__' and d != 'node_modules']

                for filename in files:
                    # Skip hidden files and .DS_Store
                    if filename.startswith('.'):
                        continue

                    filepath = Path(root) / filename
                    try:
                        file_hash = self.calculate_hash(filepath)
                        if not file_hash.startswith("ERROR"):
                            hash_to_files[file_hash].append(str(filepath))
                            file_count += 1

                            if file_count % CONSTANT_100 == 0:
                                logger.info(f"{Colors.YELLOW}  Processed: {file_count} files...{Colors.END}", end='\r')
                    except Exception as e:
                        pass

        logger.info(f"\n{Colors.GREEN}{Emojis.CHECK} Scanned {file_count} files{Colors.END}")

        # Filter to only duplicates
        duplicates = {h: files for h, files in hash_to_files.items() if len(files) > 1}

        total_dupes = sum(len(files) - 1 for files in duplicates.values())
        self.stats['total_dupes'] = total_dupes

        logger.info(f"{Colors.GREEN}{Emojis.FIRE} Found {len(duplicates)} duplicate groups ({total_dupes} duplicate files){Colors.END}")

        return duplicates

    def get_directory_priority(self, filepath: str) -> int:
        """Get priority score for a file based on its directory"""
        for dir_name, priority in self.DIRECTORY_PRIORITY.items():
            if dir_name in filepath:
                return priority
        return 0

    def choose_file_to_keep(self, files: List[str]) -> Tuple[str, List[str]]:
        """
        Intelligently choose which file to keep

        Priority:
        1. Files in python_backup (well organized)
        2. Newest modification time
        3. Shortest path (less nested = easier to find)
        4. Better naming (no special chars, clear names)
        """

        file_scores = []

        for filepath in files:
            path = Path(filepath)
            score = 0

            # Priority 1: Directory priority
            score += self.get_directory_priority(filepath) * CONSTANT_1000

            # Priority 2: Modification time (newer is better)
            try:
                mtime = path.stat().st_mtime
                score += mtime / CONSTANT_1000000  # Normalize
            except Exception:
                pass

            # Priority 3: Path depth (shallower is better)
            depth = len(path.parts)
            score -= depth * 10

            # Priority 4: Clean filename (no special chars)
            clean_name = path.name.replace('_', '').replace('-', '').replace(' ', '')
            if clean_name.replace('.', '').isalnum():
                score += 50

            # Priority 5: Avoid backup/old/temp in name
            name_lower = path.name.lower()
            if any(word in name_lower for word in ['backup', 'old', 'temp', 'copy', 'bak']):
                score -= CONSTANT_100

            file_scores.append((score, filepath))

        # Sort by score (highest first)
        file_scores.sort(reverse=True, key=lambda x: x[0])

        keep_file = file_scores[0][1]
        delete_files = [f for _, f in file_scores[1:]]

        return keep_file, delete_files

    def create_backup(self, filepath: str) -> bool:
        """Create backup of file before deletion"""
        try:
            backup_path = Path(self.backup_dir) / Path(filepath).relative_to('/')
            backup_path.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(filepath, backup_path)
            return True
        except Exception as e:
            logger.info(f"{Colors.RED}{Emojis.WARNING} Backup failed for {filepath}: {e}{Colors.END}")
            return False

    def delete_file(self, filepath: str, backup: bool = True) -> bool:
        """Safely delete a file"""
        try:
            if backup:
                if not self.create_backup(filepath):
                    logger.info(f"{Colors.RED}{Emojis.WARNING} Skipping deletion (backup failed): {filepath}{Colors.END}")
                    return False

            if not self.dry_run:
                os.remove(filepath)

            return True
        except Exception as e:
            logger.info(f"{Colors.RED}{Emojis.WARNING} Deletion failed: {filepath}: {e}{Colors.END}")
            return False

    def process_duplicate_group(self, file_hash: str, files: List[str],
                                group_num: int, total_groups: int) -> None:
        """Process a single duplicate group"""

        # Get file size
        file_size = Path(files[0]).stat().st_size

        # Choose which to keep
        keep_file, delete_files = self.choose_file_to_keep(files)

        logger.info(f"\n{Colors.BOLD}Group #{group_num}/{total_groups}{Colors.END}")
        logger.info(f"Hash: {file_hash[:16]}...")
        logger.info(f"Files: {len(files)} | Size: {file_size:,} bytes\n")

        # Show keep decision
        logger.info(f"{Colors.GREEN}{Emojis.KEEP} KEEP:{Colors.END}")
        logger.info(f"  → {keep_file}")

        # Show deletions
        logger.info(f"\n{Colors.YELLOW}{Emojis.TRASH} DELETE ({len(delete_files)} files):{Colors.END}")
        for filepath in delete_files:
            logger.info(f"  ✗ {filepath}")

        # Interactive mode - ask for confirmation
        if self.interactive:
            logger.info(f"\n{Colors.CYAN}Proceed with this deletion?{Colors.END}")
            logger.info("  [y] Yes, delete these files")
            logger.info("  [n] No, skip this group")
            logger.info("  [k] Keep a different file")
            logger.info("  [q] Quit")

            choice = input(f"\n{Colors.BOLD}Choice: {Colors.END}").lower().strip()

            if choice == 'q':
                logger.info(f"{Colors.YELLOW}{Emojis.WARNING} Aborted by user{Colors.END}")
                sys.exit(0)
            elif choice == 'n':
                logger.info(f"{Colors.YELLOW}Skipped{Colors.END}")
                return
            elif choice == 'k':
                logger.info(f"\n{Colors.CYAN}Choose file to keep:{Colors.END}")
                for idx, filepath in enumerate(files, 1):
                    logger.info(f"  [{idx}] {filepath}")

                try:
                    keep_idx = int(input(f"\n{Colors.BOLD}Number: {Colors.END}")) - 1
                    keep_file = files[keep_idx]
                    delete_files = [f for f in files if f != keep_file]
                except (OSError, IOError, FileNotFoundError):
                    logger.info(f"{Colors.RED}Invalid selection, skipping{Colors.END}")
                    return

        # Perform deletions
        for filepath in delete_files:
            if self.delete_file(filepath, backup=True):
                self.stats['files_deleted'] += 1
                self.stats['space_saved'] += file_size
                self.deletion_log.append({
                    'file': filepath,
                    'hash': file_hash,
                    'size': file_size,
                    'kept_instead': keep_file,
                    'timestamp': datetime.now().isoformat()
                })

                if not self.dry_run:
                    logger.info(f"  {Colors.GREEN}{Emojis.CHECK} Deleted: {filepath}{Colors.END}")
                else:
                    logger.info(f"  {Colors.YELLOW}[DRY RUN] Would delete: {filepath}{Colors.END}")

        self.stats['files_kept'] += 1
        self.kept_log.append({
            'file': keep_file,
            'hash': file_hash,
            'duplicates_removed': len(delete_files)
        })

        self.stats['groups_processed'] += 1

    def generate_report(self) -> str:
        """Generate deduplication report"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        report_file = fstr(Path.home()) + "/Documents/python/DEDUPLICATION_REPORT_{timestamp}.md"

        with open(report_file, 'w', encoding='utf-8') as f:
            f.write("# 🧹 DEDUPLICATION REPORT\n\n")
            f.write(f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"**Mode:** {'DRY RUN' if self.dry_run else 'LIVE DELETION'}\n\n")
            f.write("---\n\n")

            # Statistics
            f.write("## 📊 STATISTICS\n\n")
            f.write(f"| Metric | Value |\n")
            f.write(f"|--------|-------|\n")
            f.write(f"| **Groups Processed** | {self.stats['groups_processed']:,} |\n")
            f.write(f"| **Files Deleted** | {self.stats['files_deleted']:,} |\n")
            f.write(f"| **Files Kept** | {self.stats['files_kept']:,} |\n")
            f.write(f"| **Space Saved** | {self.stats['space_saved'] / (CONSTANT_1024**2):.2f} MB |\n")
            f.write(f"| **Backup Location** | `{self.backup_dir}` |\n\n")

            # Deleted files
            f.write("## 🗑️ DELETED FILES\n\n")
            for entry in self.deletion_log:
                f.write(f"### {Path(entry['file']).name}\n")
                f.write(f"- **Path:** `{entry['file']}`\n")
                f.write(f"- **Size:** {entry['size']:,} bytes\n")
                f.write(f"- **Kept Instead:** `{entry['kept_instead']}`\n")
                f.write(f"- **Hash:** `{entry['hash'][:16]}...`\n\n")

            # Kept files
            f.write("## ✅ KEPT FILES (Originals)\n\n")
            for entry in self.kept_log:
                f.write(f"- `{entry['file']}` (removed {entry['duplicates_removed']} duplicates)\n")

            # Rollback instructions
            f.write("\n## 🔄 ROLLBACK INSTRUCTIONS\n\n")
            f.write("If you need to restore deleted files:\n\n")
            f.write("```bash\n")
            f.write(f"# All backups are in: {self.backup_dir}\n")
            f.write("# To restore a specific file:\n")
            f.write(f"# cp {self.backup_dir}/path/to/file /original/location\n")
            f.write("```\n\n")

        return report_file

    def run(self, directories: List[str]) -> None:
        """Run the deduplication process"""

        # Banner
        logger.info(f"{Colors.BOLD}{Colors.MAGENTA}")
        logger.info("╔═══════════════════════════════════════════════════════════════════════════════╗")
        logger.info("║                                                                               ║")
        logger.info("║                    🧹 SMART DEDUPLICATION TOOL 🛡️                            ║")
        logger.info("║                                                                               ║")
        logger.info("║                  AI-Powered Safe Duplicate Removal                           ║")
        logger.info("║                                                                               ║")
        logger.info("╚═══════════════════════════════════════════════════════════════════════════════╝")
        logger.info(f"{Colors.END}\n")

        # Show mode
        if self.dry_run:
            logger.info(f"{Colors.YELLOW}{Emojis.SHIELD} MODE: DRY RUN (no files will be deleted){Colors.END}")
        else:
            logger.info(f"{Colors.RED}{Emojis.WARNING} MODE: LIVE DELETION (files will be removed!){Colors.END}")

        logger.info(f"{Colors.CYAN}{Emojis.BACKUP} Backup Directory: {self.backup_dir}{Colors.END}")
        logger.info(f"{Colors.CYAN}Interactive: {'Yes' if self.interactive else 'No'}{Colors.END}\n")

        # Create backup directory
        Path(self.backup_dir).mkdir(parents=True, exist_ok=True)

        # Find duplicates
        duplicates = self.find_duplicates(directories)

        if not duplicates:
            logger.info(f"{Colors.GREEN}{Emojis.CHECK} No duplicates found! All clean!{Colors.END}")
            return

        # Process each duplicate group
        self.print_header("PROCESSING DUPLICATES", Colors.YELLOW, Emojis.FIRE)

        total_groups = len(duplicates)
        for idx, (file_hash, files) in enumerate(duplicates.items(), 1):
            self.process_duplicate_group(file_hash, files, idx, total_groups)

        # Generate report
        self.print_header("GENERATING REPORT", Colors.BLUE, Emojis.CHART)
        report_file = self.generate_report()

        # Final summary
        self.print_header("DEDUPLICATION COMPLETE!", Colors.GREEN, Emojis.ROCKET)

        logger.info(f"{Colors.BOLD}📊 FINAL STATISTICS:{Colors.END}\n")
        logger.info(f"  {Emojis.FIRE} Groups Processed: {Colors.CYAN}{self.stats['groups_processed']:,}{Colors.END}")
        logger.info(f"  {Emojis.TRASH} Files Deleted: {Colors.CYAN}{self.stats['files_deleted']:,}{Colors.END}")
        logger.info(f"  {Emojis.KEEP} Files Kept: {Colors.CYAN}{self.stats['files_kept']:,}{Colors.END}")
        logger.info(f"  💾 Space Saved: {Colors.CYAN}{self.stats['space_saved'] / (CONSTANT_1024**2):.2f} MB{Colors.END}\n")

        logger.info(f"{Colors.BOLD}📝 OUTPUTS:{Colors.END}\n")
        logger.info(f"  {Emojis.FILE} Report: {Colors.BLUE}{report_file}{Colors.END}")
        logger.info(f"  {Emojis.BACKUP} Backups: {Colors.BLUE}{self.backup_dir}{Colors.END}\n")

        if self.dry_run:
            logger.info(f"{Colors.YELLOW}{Emojis.WARNING} This was a DRY RUN. Re-run with --live to actually delete files.{Colors.END}\n")
        else:
            logger.info(f"{Colors.GREEN}{Emojis.CHECK} Deduplication complete! Backups saved for safety.{Colors.END}\n")


def main():
    """Main execution"""
    parser = argparse.ArgumentParser(
        description="🧹 Smart Deduplication Tool - AI-Powered Safe Duplicate Removal",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Dry run (safe, shows what would happen):
  python smart_deduplication_tool.py --dry-run

  # Interactive mode (asks for confirmation):
  python smart_deduplication_tool.py --interactive

  # Live deletion (actually removes files):
  python smart_deduplication_tool.py --live

  # Batch mode (no confirmation, dry run):
  python smart_deduplication_tool.py --dry-run --batch
        """
    )

    parser.add_argument('--dry-run', action='store_true', default=True,
                       help='Dry run mode (default, safe)')
    parser.add_argument('--live', action='store_true',
                       help='Live mode (actually deletes files)')
    parser.add_argument('--interactive', action='store_true', default=True,
                       help='Interactive mode (asks for confirmation, default)')
    parser.add_argument('--batch', action='store_true',
                       help='Batch mode (no confirmation)')
    parser.add_argument('--backup-dir', type=str,
                       help='Custom backup directory')
    parser.add_argument('--dirs', nargs='+',
                       help='Custom directories to scan (default: python dirs)')

    args = parser.parse_args()

    # Determine mode
    dry_run = not args.live
    interactive = not args.batch

    # Default directories
    directories = args.dirs or [
        Path(str(Path.home()) + "/Documents/python-repo"),
        Path(str(Path.home()) + "/Documents/python"),
        Path(str(Path.home()) + "/Documents/python_backup")
    ]

    # Create deduplicator
    dedup = SmartDeduplicator(
        dry_run=dry_run,
        interactive=interactive,
        backup_dir=args.backup_dir
    )

    # Run
    dedup.run(directories)


if __name__ == "__main__":
    main()
