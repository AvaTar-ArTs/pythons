#!/usr/bin/env python3
"""
Super Aggressive Flattener

Flattens EVERYTHING - moves all Python files to root with context-aware names.
Only keeps essential folders: scripts, _data, _docs, _backups
"""

import os
import shutil
from pathlib import Path
from datetime import datetime


class SuperFlattener:
    def __init__(self, target_dir: str):
        self.target_dir = Path(target_dir)
        self.timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

        # Folders to preserve (don't flatten their contents)
        self.preserve_folders = {
            "scripts",
            "_data",
            "_docs",
            "_backups",
            "_reports",
            "_scripts",
            "_media",
            "_temp",
        }

        # Folders to exclude entirely
        self.exclude_patterns = [
            "_ARCHIVED_BACKUPS",
            "dedup_backup",
            "bare_except_backup",
            "deep_rename_backup",
            "automated_fixes_backup",
            "__pycache__",
            ".git",
            "node_modules",
            "myenv",
            "venv",
            "site-packages",
        ]

        self.stats = {"files_moved": 0, "folders_removed": 0, "errors": 0}

    def should_exclude(self, path: Path) -> bool:
        """Check if path should be excluded."""
        path_str = str(path)
        return any(pattern in path_str for pattern in self.exclude_patterns)

    def create_flat_name(self, file_path: Path) -> str:
        """Create smart flat name using full path context."""
        # Get relative path from target
        try:
            rel_path = file_path.relative_to(self.target_dir)
            parts = list(rel_path.parts[:-1])  # All folders except filename

            # Filter out generic names
            generic = {
                "src",
                "lib",
                "test",
                "tests",
                "bin",
                "code",
                "files",
                "data",
                "scripts",
            }
            meaningful = [
                p for p in parts if p.lower() not in generic and not p.startswith(".")
            ]

            # Get filename
            filename = file_path.stem
            ext = file_path.suffix

            # Build name
            if meaningful:
                # Use all meaningful parts, limit to last 3
                context_parts = meaningful[-3:] if len(meaningful) > 3 else meaningful
                context = "-".join(context_parts).lower()
                context = context.replace("_", "-").replace(" ", "-")

                # Remove category prefixes (01-, 02-, etc.)
                context = (
                    context.replace("01-", "").replace("02-", "").replace("03-", "")
                )
                context = (
                    context.replace("04-", "").replace("05-", "").replace("06-", "")
                )
                context = (
                    context.replace("07-", "").replace("08-", "").replace("09-", "")
                )
                context = context.replace("10-", "")

                # If filename doesn't have context, prepend it
                if not any(part.lower() in filename.lower() for part in context_parts):
                    new_name = f"{context}--{filename}{ext}"
                else:
                    new_name = f"{filename}{ext}"
            else:
                new_name = f"{filename}{ext}"

            return new_name

        except ValueError:
            return file_path.name

    def find_all_python_files(self):
        """Find all Python files in all subdirectories."""
        print("\n🔍 Finding all Python files...\n")

        all_files = []

        for root, dirs, files in os.walk(self.target_dir):
            root_path = Path(root)

            # Skip excluded directories
            if self.should_exclude(root_path):
                dirs.clear()
                continue

            # Skip preserved folders
            folder_name = root_path.name
            if folder_name in self.preserve_folders:
                dirs.clear()
                continue

            # Collect Python files
            for file in files:
                if file.endswith(".py"):
                    file_path = root_path / file

                    # Skip if already in root
                    if file_path.parent == self.target_dir:
                        continue

                    all_files.append(file_path)

        print(f"✅ Found {len(all_files)} Python files to flatten\n")
        return all_files

    def flatten_all(self, dry_run=True):
        """Flatten all Python files to root."""
        print(f"\n{'='*80}")
        print("🚀 SUPER AGGRESSIVE FLATTENING")
        print(f"{'='*80}\n")
        print(f"Mode: {'DRY RUN' if dry_run else 'LIVE'}\n")

        # Find all files
        files_to_move = self.find_all_python_files()

        # Create flat names
        moves = []
        for file_path in files_to_move:
            flat_name = self.create_flat_name(file_path)
            target_path = self.target_dir / flat_name

            # Handle duplicates
            counter = 1
            original_target = target_path
            while target_path.exists() or target_path in [m["target"] for m in moves]:
                stem = original_target.stem
                ext = original_target.suffix
                target_path = self.target_dir / f"{stem}-{counter}{ext}"
                counter += 1

            moves.append(
                {
                    "source": file_path,
                    "target": target_path,
                    "original_name": file_path.name,
                    "new_name": target_path.name,
                }
            )

        # Show preview
        print(f"📊 FLATTENING PLAN:\n")
        print(f"Total files to move: {len(moves)}\n")

        if moves:
            print("Sample moves:")
            for move in moves[:10]:
                rel_source = move["source"].relative_to(self.target_dir)
                print(f"  {rel_source}")
                print(f"    → {move['new_name']}\n")

            if len(moves) > 10:
                print(f"  ... and {len(moves) - 10} more files\n")

        # Execute moves
        if not dry_run:
            print(f"\n🚀 Executing moves...\n")

            for i, move in enumerate(moves, 1):
                if i % 100 == 0:
                    print(f"Progress: {i}/{len(moves)}...")

                try:
                    shutil.move(str(move["source"]), str(move["target"]))
                    self.stats["files_moved"] += 1
                except Exception as e:
                    print(f"❌ Error: {move['source'].name}: {e}")
                    self.stats["errors"] += 1

            # Remove empty folders
            print(f"\n🗑️ Removing empty folders...\n")
            self.remove_empty_folders()

        # Final summary
        print(f"\n{'='*80}")
        print("✅ SUPER FLATTENING COMPLETE!")
        print(f"{'='*80}\n")
        print(f"Files Moved: {len(moves) if dry_run else self.stats['files_moved']}")
        if not dry_run:
            print(f"Folders Removed: {self.stats['folders_removed']}")
            if self.stats["errors"] > 0:
                print(f"Errors: {self.stats['errors']}")
        print()

    def remove_empty_folders(self):
        """Remove all empty folders after flattening."""
        folders_to_check = []

        for root, dirs, files in os.walk(self.target_dir, topdown=False):
            root_path = Path(root)

            # Skip preserved folders
            if root_path.name in self.preserve_folders:
                continue

            # Skip excluded
            if self.should_exclude(root_path):
                continue

            # Check if empty
            try:
                if not list(root_path.iterdir()):
                    root_path.rmdir()
                    self.stats["folders_removed"] = (
                        self.stats.get("folders_removed", 0) + 1
                    )
            except:
                pass


def main():
    import argparse

    parser = argparse.ArgumentParser(description="Super Aggressive Flattener")
    parser.add_argument("--target", default=".", help="Target directory")
    parser.add_argument("--live", action="store_true", help="Execute flattening")

    args = parser.parse_args()

    flattener = SuperFlattener(args.target)
    flattener.flatten_all(dry_run=not args.live)


if __name__ == "__main__":
    main()
