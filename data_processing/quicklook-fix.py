#!/usr/bin/env python3
"""
Quick Look Plugin Fix Script
Fixes broken symlinks and reinstalls plugins properly
"""

import subprocess
import sys
from pathlib import Path


class QuickLookFixer:
    """Fixes Quick Look plugin issues"""

    USER_PLUGIN_DIR = Path.home() / "Library" / "QuickLook"

    def __init__(self, dry_run=False):
        self.dry_run = dry_run
        self.fixed = []
        self.errors = []

    def backup_broken_links(self):
        """Backup broken symlinks before fixing"""
        if not self.USER_PLUGIN_DIR.exists():
            return

        backup_dir = Path.home() / ".quicklook_plugins_backup" / "broken_links"
        backup_dir.mkdir(parents=True, exist_ok=True)

        broken_links = []
        for item in self.USER_PLUGIN_DIR.iterdir():
            if item.is_symlink():
                try:
                    target = item.readlink()
                    if not target.exists():
                        broken_links.append(item)
                except:
                    broken_links.append(item)

        if broken_links:
            print(f"📦 Backing up {len(broken_links)} broken symlinks...")
            for link in broken_links:
                backup_path = backup_dir / link.name
                if not self.dry_run:
                    # Just record the symlink target
                    try:
                        target = str(link.readlink())
                        with open(backup_path.with_suffix(".txt"), "w") as f:
                            f.write(f"Original symlink: {link}\n")
                            f.write(f"Target: {target}\n")
                    except:
                        pass
                print(f"  - {link.name}")

    def remove_broken_symlinks(self):
        """Remove broken symlinks"""
        if not self.USER_PLUGIN_DIR.exists():
            return

        print("\n🔧 Removing broken symlinks...")

        for item in self.USER_PLUGIN_DIR.iterdir():
            if item.is_symlink():
                try:
                    target = item.readlink()
                    if not target.exists():
                        print(f"  Removing: {item.name}")
                        if not self.dry_run:
                            item.unlink()
                            self.fixed.append(
                                {
                                    "action": "removed",
                                    "plugin": item.name,
                                    "reason": "broken_symlink",
                                }
                            )
                except Exception:
                    print(f"  Removing (error reading): {item.name}")
                    if not self.dry_run:
                        item.unlink()
                        self.fixed.append(
                            {
                                "action": "removed",
                                "plugin": item.name,
                                "reason": "broken_symlink_error",
                            }
                        )

    def reinstall_homebrew_plugins(self):
        """Reinstall Homebrew Quick Look plugins"""
        print("\n🍺 Reinstalling Homebrew Quick Look plugins...")

        quicklook_casks = [
            "qlcolorcode",
            "qlstephen",
            "quicklook-csv",
            "quicklook-json",
            "webpquicklook",
        ]

        for cask in quicklook_casks:
            print(f"\n  Processing: {cask}")

            # Check if installed
            try:
                result = subprocess.run(
                    ["brew", "list", "--cask", cask],
                    capture_output=True,
                    text=True,
                    timeout=10,
                )

                if result.returncode == 0:
                    print(f"    Reinstalling {cask}...")
                    if not self.dry_run:
                        reinstall_result = subprocess.run(
                            ["brew", "reinstall", "--cask", cask],
                            capture_output=True,
                            text=True,
                            timeout=60,
                        )

                        if reinstall_result.returncode == 0:
                            self.fixed.append(
                                {
                                    "action": "reinstalled",
                                    "plugin": cask,
                                    "method": "homebrew",
                                }
                            )
                            print("    ✅ Reinstalled successfully")
                        else:
                            self.errors.append(
                                {"plugin": cask, "error": reinstall_result.stderr}
                            )
                            print(f"    ❌ Failed: {reinstall_result.stderr}")
                else:
                    print("    ℹ️  Not installed via Homebrew")
            except subprocess.TimeoutExpired:
                self.errors.append(
                    {"plugin": cask, "error": "Timeout during reinstall"}
                )
                print("    ⚠️  Timeout")
            except Exception as e:
                self.errors.append({"plugin": cask, "error": str(e)})
                print(f"    ❌ Error: {e}")

    def refresh_quicklook(self):
        """Refresh Quick Look cache"""
        print("\n🔄 Refreshing Quick Look...")

        if not self.dry_run:
            try:
                subprocess.run(
                    ["qlmanage", "-r"], capture_output=True, check=True, timeout=5
                )
                print("  ✅ Quick Look cache refreshed")
            except Exception as e:
                print(f"  ⚠️  Warning: {e}")
        else:
            print("  [DRY RUN] Would refresh Quick Look cache")

    def restart_finder(self):
        """Restart Finder"""
        print("\n🔄 Restarting Finder...")

        if not self.dry_run:
            try:
                subprocess.run(
                    ["killall", "Finder"], capture_output=True, check=True, timeout=5
                )
                print("  ✅ Finder restarted")
            except Exception as e:
                print(f"  ⚠️  Warning: {e}")
        else:
            print("  [DRY RUN] Would restart Finder")

    def run_fix(self):
        """Run all fix operations"""
        print("=" * 60)
        print("Quick Look Plugin Fix")
        print("=" * 60)

        if self.dry_run:
            print("\n⚠️  DRY RUN MODE - No changes will be made\n")

        self.backup_broken_links()
        self.remove_broken_symlinks()
        self.reinstall_homebrew_plugins()
        self.refresh_quicklook()
        self.restart_finder()

        print("\n" + "=" * 60)
        print("FIX SUMMARY")
        print("=" * 60)
        print(f"  Fixed: {len(self.fixed)}")
        print(f"  Errors: {len(self.errors)}")

        if self.fixed:
            print("\n  Fixed items:")
            for item in self.fixed:
                print(f"    - {item['plugin']}: {item['action']}")

        if self.errors:
            print("\n  Errors:")
            for error in self.errors:
                print(f"    - {error['plugin']}: {error['error']}")

        print()


def main():
    import argparse

    parser = argparse.ArgumentParser(description="Fix Quick Look plugin issues")
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show what would be done without making changes",
    )

    args = parser.parse_args()

    fixer = QuickLookFixer(dry_run=args.dry_run)
    fixer.run_fix()

    if fixer.errors:
        sys.exit(1)
    else:
        sys.exit(0)


if __name__ == "__main__":
    main()
