#!/usr/bin/env python3
"""
Simple Content-Aware AVATARARTS Consolidation

Direct implementation of the consolidation strategy without complex duplicate checking.
"""

import os
import shutil
from pathlib import Path
from datetime import datetime

class SimpleConsolidator:
    def __init__(self, home_dir: str = "/Users/steven", dry_run: bool = True):
        self.home_dir = Path(home_dir)
        self.avatararts_main = self.home_dir / "AVATARARTS"
        self.dry_run = dry_run

    def ensure_directories(self):
        """Ensure target directories exist."""
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
                    print(f"📁 Created directory: {full_path}")
                else:
                    print(f"📁 Would create directory: {full_path}")

    def safe_move(self, source: str, target_dir: str, description: str) -> bool:
        """Safely move an item."""
        source_path = self.home_dir / source
        target_path = self.avatararts_main / target_dir / source

        if not source_path.exists():
            print(f"⚠️  Source not found: {source_path}")
            return False

        # Handle naming conflicts
        if target_path.exists():
            if source_path.is_file():
                stem = target_path.stem
                suffix = target_path.suffix
                counter = 1
                while target_path.exists():
                    target_path = target_path.parent / f"{stem}_{counter}{suffix}"
                    counter += 1
            else:
                counter = 1
                original_name = target_path.name
                while target_path.exists():
                    target_path = target_path.parent / f"{original_name}_{counter}"
                    counter += 1

        if self.dry_run:
            print(f"🔍 Would move: {source_path} → {target_path} ({description})")
            return True
        else:
            try:
                shutil.move(str(source_path), str(target_path))
                print(f"✅ Moved: {source_path} → {target_path}")
                return True
            except Exception as e:
                print(f"❌ Failed to move {source_path}: {e}")
                return False

    def execute_phase(self, phase: str) -> int:
        """Execute a specific consolidation phase."""
        moves = {
            'safe': [
                ('.avatararts_memory.md', 'docs/', 'Documentation'),
                ('2T_Xx_AVATARARTS_CONSOLIDATION_PLAN.md', 'docs/', 'Documentation'),
                ('quick_avatararts_analysis.py', 'development/scripts/', 'Script'),
                ('AVATARARTS.backup.2026-02-03.tar.gz', 'archives/', 'Backup'),
            ],
            'structured': [
                ('avatararts.db', 'data/master-databases/', 'Database'),
                ('AVATARARTS-Database-System', 'data/master-databases/', 'Database System'),
                ('avatararts-v2', 'development/ecosystem/', 'Development'),
                ('avatararts-advanced-organization', 'development/ecosystem/', 'Development'),
                ('avatararts-website', 'business/enterprise/', 'Web Project'),
            ],
            'review': [
                ('.avatararts', 'consolidation/scattered/', 'Hidden directory'),
                ('avatararts.org', 'consolidation/scattered/', 'Complex project'),
                ('avatararts-ftp.txt', 'consolidation/scattered/', 'FTP config'),
            ]
        }

        if phase not in moves:
            print(f"Unknown phase: {phase}")
            return 0

        print(f"\n🚀 Executing Phase: {phase.upper()}")
        successful = 0

        for source, target, desc in moves[phase]:
            if self.safe_move(source, target, desc):
                successful += 1

        return successful

    def execute_all_phases(self) -> dict:
        """Execute all consolidation phases."""
        self.ensure_directories()

        results = {
            'timestamp': datetime.now().isoformat(),
            'dry_run': self.dry_run,
            'phases': {}
        }

        phases = ['safe', 'structured', 'review']
        total_successful = 0

        for phase in phases:
            successful = self.execute_phase(phase)
            results['phases'][phase] = successful
            total_successful += successful

        print(f"\n📊 Consolidation Summary:")
        print(f"{'DRY RUN' if self.dry_run else 'LIVE EXECUTION'} completed")
        for phase, count in results['phases'].items():
            print(f"  {phase.upper()}: {count} items")
        print(f"Total: {total_successful} items processed")

        return results

def main():
    import sys

    dry_run = '--live' not in sys.argv

    consolidator = SimpleConsolidator(dry_run=dry_run)
    results = consolidator.execute_all_phases()

    if dry_run:
        print(f"\n🔍 This was a DRY RUN. To execute live moves, run with --live")
    else:
        print(f"\n✅ Live consolidation completed!")

if __name__ == "__main__":
    main()