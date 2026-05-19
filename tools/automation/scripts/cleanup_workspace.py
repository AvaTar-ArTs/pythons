#!/usr/bin/env python3
"""
AVATARARTS Workspace Cleanup Script
Removes build artifacts and duplicate files safely
"""

import hashlib
import shutil
from collections import defaultdict
from datetime import datetime
from pathlib import Path


class WorkspaceCleanup:
    def __init__(self, root_dir="/Users/steven/AVATARARTS"):
        self.root = Path(root_dir)
        self.removed_items = []
        self.space_freed = 0
        self.errors = []

    def calculate_size(self, path):
        """Calculate total size of file or directory"""
        try:
            if path.is_file():
                return path.stat().st_size
            elif path.is_dir():
                total = 0
                for item in path.rglob("*"):
                    if item.is_file():
                        total += item.stat().st_size
                return total
        except:
            return 0
        return 0

    def find_build_artifacts(self):
        """Find build artifacts to remove"""
        print("🔍 Scanning for build artifacts...")

        artifacts = {
            "venv_dirs": [],
            "build_dirs": [],
            "cache_dirs": [],
            "pyc_files": [],
        }

        # Find .venv directories (excluding archive)
        for venv in self.root.rglob(".venv"):
            if "archive" not in str(venv):
                artifacts["venv_dirs"].append(venv)

        # Find _build directories
        for build in self.root.rglob("_build"):
            artifacts["build_dirs"].append(build)

        # Find __pycache__ directories
        for cache in self.root.rglob("__pycache__"):
            artifacts["cache_dirs"].append(cache)

        # Find .pyc files
        for pyc in self.root.rglob("*.pyc"):
            artifacts["pyc_files"].append(pyc)

        return artifacts

    def cleanup_build_artifacts(self, artifacts, dry_run=True):
        """Remove build artifacts"""
        print("\n🧹 Cleaning up build artifacts...")

        total_size = 0

        # Remove .venv directories
        if artifacts["venv_dirs"]:
            print(f"\n  📦 Virtual Environments ({len(artifacts['venv_dirs'])} found):")
            for venv in artifacts["venv_dirs"]:
                size = self.calculate_size(venv)
                total_size += size
                size_mb = size / (1024 * 1024)
                rel_path = venv.relative_to(self.root)

                if dry_run:
                    print(f"    🔍 Would remove: {rel_path} ({size_mb:.1f} MB)")
                else:
                    try:
                        shutil.rmtree(venv)
                        self.removed_items.append(("venv", str(rel_path), size))
                        print(f"    ✅ Removed: {rel_path} ({size_mb:.1f} MB)")
                    except Exception as e:
                        self.errors.append((str(rel_path), str(e)))
                        print(f"    ⚠️  Error removing {rel_path}: {e}")

        # Remove _build directories
        if artifacts["build_dirs"]:
            print(f"\n  🏗️  Build Directories ({len(artifacts['build_dirs'])} found):")
            for build in artifacts["build_dirs"]:
                size = self.calculate_size(build)
                total_size += size
                size_mb = size / (1024 * 1024)
                rel_path = build.relative_to(self.root)

                if dry_run:
                    print(f"    🔍 Would remove: {rel_path} ({size_mb:.1f} MB)")
                else:
                    try:
                        shutil.rmtree(build)
                        self.removed_items.append(("build", str(rel_path), size))
                        print(f"    ✅ Removed: {rel_path} ({size_mb:.1f} MB)")
                    except Exception as e:
                        self.errors.append((str(rel_path), str(e)))
                        print(f"    ⚠️  Error removing {rel_path}: {e}")

        # Remove __pycache__ directories
        if artifacts["cache_dirs"]:
            print(f"\n  💾 Cache Directories ({len(artifacts['cache_dirs'])} found):")
            for cache in artifacts["cache_dirs"]:
                size = self.calculate_size(cache)
                total_size += size
                size_mb = size / (1024 * 1024)
                rel_path = cache.relative_to(self.root)

                if dry_run:
                    print(f"    🔍 Would remove: {rel_path} ({size_mb:.2f} MB)")
                else:
                    try:
                        shutil.rmtree(cache)
                        self.removed_items.append(("cache", str(rel_path), size))
                        print(f"    ✅ Removed: {rel_path} ({size_mb:.2f} MB)")
                    except Exception as e:
                        self.errors.append((str(rel_path), str(e)))
                        print(f"    ⚠️  Error removing {rel_path}: {e}")

        # Remove .pyc files
        if artifacts["pyc_files"]:
            print(f"\n  🐍 Python Cache Files ({len(artifacts['pyc_files'])} found):")
            for pyc in artifacts["pyc_files"]:
                if not pyc.exists():
                    continue  # Already removed (e.g., when parent __pycache__ was removed)

                size = pyc.stat().st_size
                total_size += size
                rel_path = pyc.relative_to(self.root)

                if dry_run:
                    print(f"    🔍 Would remove: {rel_path}")
                else:
                    try:
                        pyc.unlink()
                        self.removed_items.append(("pyc", str(rel_path), size))
                        print(f"    ✅ Removed: {rel_path}")
                    except Exception as e:
                        self.errors.append((str(rel_path), str(e)))
                        print(f"    ⚠️  Error removing {rel_path}: {e}")

        if dry_run:
            print(
                f"\n  📊 Total space that would be freed: {total_size / (1024 * 1024):.1f} MB"
            )
        else:
            self.space_freed += total_size
            print(f"\n  📊 Space freed: {total_size / (1024 * 1024):.1f} MB")

        return total_size

    def calculate_file_hash(self, filepath):
        """Calculate MD5 hash of file (for files < 5MB)"""
        try:
            if filepath.stat().st_size > 5 * 1024 * 1024:
                return None
            with open(filepath, "rb") as f:
                return hashlib.md5(f.read()).hexdigest()
        except:
            return None

    def find_duplicates(self):
        """Find duplicate files based on content hash"""
        print("\n🔍 Scanning for duplicate files...")
        print("  (This may take a few minutes for large files...)")

        hash_to_files = defaultdict(list)
        files_scanned = 0

        # Scan all files
        for filepath in self.root.rglob("*"):
            if not filepath.is_file():
                continue

            # Skip build artifacts (we'll handle those separately)
            if any(
                x in str(filepath) for x in [".venv", "_build", "__pycache__", ".git"]
            ):
                continue

            # Skip files in archive (unless user wants to clean those too)
            if "archive" in str(filepath) and "archive/backups" not in str(filepath):
                continue

            files_scanned += 1
            if files_scanned % 1000 == 0:
                print(f"    Scanned {files_scanned} files...")

            file_hash = self.calculate_file_hash(filepath)
            if file_hash:
                hash_to_files[file_hash].append(filepath)

        print(f"  ✅ Scanned {files_scanned} files")

        # Filter to only groups with 2+ files
        duplicates = {h: files for h, files in hash_to_files.items() if len(files) > 1}

        return duplicates

    def cleanup_duplicates(self, duplicates, dry_run=True, keep_first=True):
        """Remove duplicate files, keeping the first one"""
        print("\n🔄 Cleaning up duplicate files...")

        total_size = 0
        groups_processed = 0

        # Sort by total size (largest first)
        sorted_dupes = sorted(
            duplicates.items(),
            key=lambda x: x[1][0].stat().st_size * len(x[1]),
            reverse=True,
        )

        print(f"  Found {len(sorted_dupes)} duplicate groups")

        for hash_val, files in sorted_dupes[:50]:  # Process top 50 groups
            if len(files) < 2:
                continue

            # Sort files by path (keep the shortest/most logical path)
            files_sorted = sorted(files, key=lambda x: (len(str(x)), str(x)))
            keep_file = files_sorted[0] if keep_first else files_sorted[-1]
            remove_files = files_sorted[1:] if keep_first else files_sorted[:-1]

            file_size = keep_file.stat().st_size
            group_size = file_size * len(remove_files)
            total_size += group_size

            groups_processed += 1
            rel_keep = keep_file.relative_to(self.root)

            print(f"\n  📦 Group {groups_processed}: {keep_file.name}")
            print(f"     Keep: {rel_keep}")
            print(
                f"     Size: {file_size / 1024:.1f} KB × {len(remove_files)} copies = {group_size / 1024:.1f} KB"
            )

            for remove_file in remove_files:
                rel_remove = remove_file.relative_to(self.root)

                if dry_run:
                    print(f"     🔍 Would remove: {rel_remove}")
                else:
                    try:
                        remove_file.unlink()
                        self.removed_items.append(
                            ("duplicate", str(rel_remove), file_size)
                        )
                        print(f"     ✅ Removed: {rel_remove}")
                    except Exception as e:
                        self.errors.append((str(rel_remove), str(e)))
                        print(f"     ⚠️  Error: {e}")

        if dry_run:
            print(
                f"\n  📊 Total space that would be freed: {total_size / (1024 * 1024):.1f} MB"
            )
        else:
            self.space_freed += total_size
            print(f"\n  📊 Space freed: {total_size / (1024 * 1024):.1f} MB")

        return total_size

    def generate_cleanup_log(self):
        """Generate log of cleanup actions"""
        log_path = (
            self.root
            / "docs"
            / "reports"
            / f"CLEANUP_LOG_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
        )

        with open(log_path, "w") as f:
            f.write("# Workspace Cleanup Log\n\n")
            f.write(f"**Date:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
            f.write("---\n\n")

            f.write("## Summary\n\n")
            f.write(f"- **Items Removed:** {len(self.removed_items)}\n")
            f.write(f"- **Space Freed:** {self.space_freed / (1024 * 1024):.1f} MB\n")
            f.write(f"- **Errors:** {len(self.errors)}\n\n")

            if self.removed_items:
                f.write("## Removed Items\n\n")
                by_type = defaultdict(list)
                for item_type, path, size in self.removed_items:
                    by_type[item_type].append((path, size))

                for item_type, items in by_type.items():
                    f.write(f"### {item_type.upper()} ({len(items)} items)\n\n")
                    for path, size in items:
                        size_mb = size / (1024 * 1024)
                        f.write(f"- `{path}` ({size_mb:.2f} MB)\n")
                    f.write("\n")

            if self.errors:
                f.write("## Errors\n\n")
                for path, error in self.errors:
                    f.write(f"- `{path}`: {error}\n")

        print(f"\n✅ Cleanup log saved: {log_path}")
        return log_path


def main():
    import sys

    dry_run = "--execute" not in sys.argv

    if dry_run:
        print("=" * 60)
        print("🔍 DRY RUN MODE - No files will be removed")
        print("=" * 60)
        print("Add --execute flag to actually remove files\n")
    else:
        print("=" * 60)
        print("⚡ EXECUTION MODE - Files will be removed")
        print("=" * 60)
        print()

    cleanup = WorkspaceCleanup()

    # Step 1: Find and remove build artifacts
    artifacts = cleanup.find_build_artifacts()
    cleanup.cleanup_build_artifacts(artifacts, dry_run=dry_run)

    # Step 2: Find and remove duplicates
    print("\n" + "=" * 60)
    duplicates = cleanup.find_duplicates()
    if duplicates:
        cleanup.cleanup_duplicates(duplicates, dry_run=dry_run)
    else:
        print("  ✅ No duplicate files found")

    # Step 3: Generate log
    if not dry_run:
        cleanup.generate_cleanup_log()

        print("\n" + "=" * 60)
        print("✅ CLEANUP COMPLETE!")
        print("=" * 60)
        print("\n📊 Summary:")
        print(f"   - Items removed: {len(cleanup.removed_items)}")
        print(f"   - Space freed: {cleanup.space_freed / (1024 * 1024):.1f} MB")
        if cleanup.errors:
            print(f"   - Errors: {len(cleanup.errors)}")
        print()
    else:
        print("\n" + "=" * 60)
        print("🔍 DRY RUN COMPLETE")
        print("=" * 60)
        print("\nTo execute these changes, run:")
        print("  python3 scripts/cleanup_workspace.py --execute\n")


if __name__ == "__main__":
    main()
