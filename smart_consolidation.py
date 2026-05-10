#!/usr/bin/env python3
"""
Smart Content-Aware AVATARARTS Consolidation Script

Implements the consolidation strategy with safety checks and verification.
"""

import os
import shutil
import json
from pathlib import Path
from typing import Dict, List, Any, Tuple
from datetime import datetime
import hashlib

class SmartConsolidator:
    def __init__(self, home_dir: str = "/Users/steven", dry_run: bool = True):
        self.home_dir = Path(home_dir)
        self.avatararts_main = self.home_dir / "AVATARARTS"
        self.dry_run = dry_run
        self.log_file = self.home_dir / "consolidation_log.json"
        self.backup_manifest = self.home_dir / "consolidation_backup_manifest.txt"

        # Ensure target directories exist
        self.ensure_directories()

    def ensure_directories(self):
        """Ensure all target directories exist."""
        dirs_to_create = [
            "docs",
            "data/master-databases",
            "archives",
            "development/ecosystem",
            "business/enterprise",
            "development/scripts",
            "consolidation/scattered"
        ]

        for dir_path in dirs_to_create:
            full_path = self.avatararts_main / dir_path
            if not full_path.exists():
                if not self.dry_run:
                    full_path.mkdir(parents=True, exist_ok=True)
                print(f"📁 {'Would create' if self.dry_run else 'Created'} directory: {full_path}")

    def get_file_hash(self, file_path: Path) -> str:
        """Get SHA256 hash of file."""
        try:
            hash_obj = hashlib.sha256()
            with open(file_path, 'rb') as f:
                for chunk in iter(lambda: f.read(4096), b''):
                    hash_obj.update(chunk)
            return hash_obj.hexdigest()
        except:
            return None

    def check_for_duplicates(self, source_path: Path, target_dir: Path) -> List[Path]:
        """Check if source content duplicates anything in target directory."""
        duplicates = []

        if source_path.is_file():
            source_hash = self.get_file_hash(source_path)
            if source_hash:
                try:
                    for root, dirs, files in os.walk(target_dir):
                        for file in files:
                            file_path = Path(root) / file
                            try:
                                if file_path.exists() and file_path.stat().st_size == source_path.stat().st_size:
                                    file_hash = self.get_file_hash(file_path)
                                    if file_hash == source_hash:
                                        duplicates.append(file_path.relative_to(self.avatararts_main))
                            except (OSError, FileNotFoundError):
                                continue  # Skip files that can't be accessed
                except (OSError, FileNotFoundError):
                    pass  # Skip directories that can't be walked
        else:
            # For directories, check if a similar directory already exists
            try:
                source_name = source_path.name.lower().replace('avatararts', '').replace('-', '').strip()
                for item in target_dir.iterdir():
                    if item.is_dir():
                        target_name = item.name.lower().replace('avatararts', '').replace('-', '').strip()
                        if source_name and target_name and source_name in target_name:
                            duplicates.append(item.relative_to(self.avatararts_main))
            except (OSError, FileNotFoundError):
                pass  # Skip if target directory can't be read

        return duplicates

    def safe_move(self, source_path: Path, target_dir: Path, reason: str) -> Tuple[bool, str]:
        """Safely move an item with verification."""
        if not source_path.exists():
            return False, f"Source does not exist: {source_path}"

        target_path = target_dir / source_path.name

        # Check for naming conflicts
        if target_path.exists():
            # If it's the same file/directory, skip
            if source_path.samefile(target_path):
                return False, f"Source and target are the same: {target_path}"
            else:
                # Rename to avoid conflict
                counter = 1
                stem = target_path.stem
                suffix = target_path.suffix
                while target_path.exists():
                    target_path = target_dir / f"{stem}_{counter}{suffix}"
                    counter += 1

        # Check for duplicates
        duplicates = self.check_for_duplicates(source_path, target_dir)
        if duplicates:
            return False, f"Content duplicates found in target: {', '.join(str(d) for d in duplicates)}"

        if self.dry_run:
            print(f"🔍 Would move: {source_path} → {target_path} ({reason})")
            return True, f"Would move (dry run): {source_path} → {target_path}"
        else:
            try:
                shutil.move(str(source_path), str(target_path))
                print(f"✅ Moved: {source_path} → {target_path}")
                return True, f"Successfully moved: {source_path} → {target_path}"
            except Exception as e:
                return False, f"Move failed: {e}"

    def get_consolidation_plan(self) -> List[Dict[str, Any]]:
        """Get the consolidation plan based on our analysis."""
        return [
            {
                'source': '.avatararts_memory.md',
                'target': 'docs/',
                'category': 'Documentation',
                'reason': 'Memory/documentation files belong in docs'
            },
            {
                'source': '2T_Xx_AVATARARTS_CONSOLIDATION_PLAN.md',
                'target': 'docs/',
                'category': 'Documentation',
                'reason': 'Consolidation plans are documentation'
            },
            {
                'source': 'avatararts.db',
                'target': 'data/master-databases/',
                'category': 'Database',
                'reason': 'Database files should be consolidated'
            },
            {
                'source': 'AVATARARTS-Database-System',
                'target': 'data/master-databases/',
                'category': 'Database System',
                'reason': 'Database systems should be consolidated'
            },
            {
                'source': 'AVATARARTS.backup.2026-02-03.tar.gz',
                'target': 'archives/',
                'category': 'Backup',
                'reason': 'Backup archives should be archived'
            },
            {
                'source': 'avatararts-v2',
                'target': 'development/ecosystem/',
                'category': 'Development',
                'reason': 'Development versions belong in ecosystem'
            },
            {
                'source': 'avatararts-advanced-organization',
                'target': 'development/ecosystem/',
                'category': 'Development',
                'reason': 'Advanced organization tools belong in ecosystem'
            },
            {
                'source': 'avatararts-website',
                'target': 'business/enterprise/',
                'category': 'Web Project',
                'reason': 'Web projects belong in business section'
            },
            {
                'source': 'quick_avatararts_analysis.py',
                'target': 'development/scripts/',
                'category': 'Script',
                'reason': 'Analysis scripts belong in development area'
            },
            # Items requiring review - move to scattered for manual inspection
            {
                'source': '.avatararts',
                'target': 'consolidation/scattered/',
                'category': 'Project Component',
                'reason': 'Hidden directory needs manual review'
            },
            {
                'source': 'avatararts.org',
                'target': 'consolidation/scattered/',
                'category': 'Project Component',
                'reason': 'Complex project needs manual review'
            },
            {
                'source': 'avatararts-ftp.txt',
                'target': 'consolidation/scattered/',
                'category': 'Other',
                'reason': 'FTP config needs manual categorization'
            }
        ]

    def execute_consolidation(self, phase: str = None) -> Dict[str, Any]:
        """Execute the consolidation plan."""
        plan = self.get_consolidation_plan()
        results = {
            'timestamp': datetime.now().isoformat(),
            'dry_run': self.dry_run,
            'phase': phase or 'all',
            'total_items': len(plan),
            'successful_moves': 0,
            'failed_moves': 0,
            'skipped_moves': 0,
            'moves': []
        }

        # Phase filtering
        if phase == 'safe':
            plan = [item for item in plan if item['category'] in ['Documentation', 'Script', 'Backup']]
        elif phase == 'structured':
            plan = [item for item in plan if item['category'] in ['Database', 'Database System', 'Web Project', 'Development']]
        elif phase == 'review':
            plan = [item for item in plan if item['category'] in ['Project Component', 'Other']]

        print(f"🚀 Starting {'DRY RUN' if self.dry_run else 'LIVE'} consolidation (Phase: {results['phase']})")
        print(f"📋 Processing {len(plan)} items...")

        for item in plan:
            source_path = self.home_dir / item['source']
            target_dir = self.avatararts_main / item['target']

            success, message = self.safe_move(source_path, target_dir, item['reason'])

            move_result = {
                'item': item['source'],
                'category': item['category'],
                'target': item['target'],
                'success': success,
                'message': message
            }

            results['moves'].append(move_result)

            if success:
                results['successful_moves'] += 1
            elif 'Would move' in message or 'Content duplicates' in message:
                results['skipped_moves'] += 1
            else:
                results['failed_moves'] += 1

        # Save results
        with open(self.log_file, 'w') as f:
            json.dump(results, f, indent=2)

        print(f"\n📊 Consolidation Results:")
        print(f"✅ Successful: {results['successful_moves']}")
        print(f"⏭️  Skipped: {results['skipped_moves']}")
        print(f"❌ Failed: {results['failed_moves']}")
        print(f"📝 Log saved to: {self.log_file}")

        return results

def main():
    import argparse

    parser = argparse.ArgumentParser(description='Smart AVATARARTS Consolidation')
    parser.add_argument('--live', action='store_true', help='Execute live moves (default is dry run)')
    parser.add_argument('--phase', choices=['safe', 'structured', 'review'], help='Consolidation phase')
    parser.add_argument('--all', action='store_true', help='Run all phases')

    args = parser.parse_args()

    dry_run = not args.live
    consolidator = SmartConsolidator(dry_run=dry_run)

    if args.all:
        # Run all phases
        phases = ['safe', 'structured', 'review']
        all_results = {}
        for phase in phases:
            print(f"\n{'='*50}")
            print(f"PHASE: {phase.upper()}")
            print('='*50)
            all_results[phase] = consolidator.execute_consolidation(phase)
        print(f"\n🎉 All phases completed! Check {consolidator.log_file} for details.")
    else:
        phase = args.phase
        results = consolidator.execute_consolidation(phase)

        if dry_run:
            print(f"\n🔍 This was a DRY RUN. To execute live moves, run with --live")
        else:
            print(f"\n✅ Consolidation completed! Review {consolidator.log_file} for details.")

if __name__ == "__main__":
    main()