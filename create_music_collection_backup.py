#!/usr/bin/env python3
"""
Create backup of music collections before consolidation
"""

import datetime
import shutil
from pathlib import Path


def create_backups():
    """Create backups of source directories before moving content"""
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    base_path = Path("/Users/steven/Music/nocTurneMeLoDieS")
    backup_dir = base_path / "backups"
    backup_dir.mkdir(exist_ok=True)

    # Source directories to backup
    sources = [
        "/Users/steven/AVATARARTS/HEAVENLY_HANDS_PROJECT",
        "/Users/steven/AVATARARTS/DR_ADU_PROJECT",
    ]

    print("Creating backups of source directories...")

    for source in sources:
        source_path = Path(source)
        if source_path.exists():
            backup_name = f"{source_path.name}_backup_{timestamp}"
            backup_path = backup_dir / backup_name

            print(f"Backing up: {source} -> {backup_path}")
            shutil.copytree(source_path, backup_path, dirs_exist_ok=True)
            print(f"  ✓ Backup completed: {backup_path}")
        else:
            print(f"  ⚠ Source does not exist: {source}")

    print(f"\nBackups created in: {backup_dir}")
    print("You can safely proceed with consolidation now.")


if __name__ == "__main__":
    create_backups()
