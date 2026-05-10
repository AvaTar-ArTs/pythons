#!/usr/bin/env python3
"""
Deep Structure Cleanup Script
Cleans up Python virtual environments, package management, and development tools
that create excessive directory depth
"""

import logging
import os
import shutil
import subprocess
import time
from datetime import datetime
from pathlib import Path

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


class DeepStructureCleanup:
    def __init__(self, home_dir):
        self.home_dir = Path(home_dir).expanduser()
        self.cleanup_log = []
        self.space_saved = 0
        self.files_removed = 0
        self.dirs_removed = 0
        self.start_time = time.time()

    def log_action(self, action, path, size_mb=0):
        """Log cleanup actions"""
        self.cleanup_log.append(
            {
                "action": action,
                "path": str(path),
                "size_mb": size_mb,
                "timestamp": datetime.now().isoformat(),
            }
        )
        logger.info(f"{action}: {path} ({size_mb:.2f} MB)")

    def get_directory_size(self, path):
        """Get directory size in MB"""
        try:
            result = subprocess.run(
                ["du", "-sm", str(path)], capture_output=True, text=True, timeout=30
            )
            if result.returncode == 0:
                return int(result.stdout.split()[0])
            return 0
        except:
            return 0

    def clean_xcmd_cache(self):
        """Clean up x-cmd package cache and temp files"""
        logger.info("Cleaning x-cmd cache...")

        xcmd_root = self.home_dir / ".x-cmd.root"
        if not xcmd_root.exists():
            logger.info("No x-cmd root directory found")
            return

        # Get size before cleanup
        size_before = self.get_directory_size(xcmd_root)

        # Clean cache directories
        cache_dirs = [
            xcmd_root / "local" / "cache",
            xcmd_root / "local" / "tmp",
            xcmd_root / "local" / "data" / "pkg" / "sphere",
        ]

        for cache_dir in cache_dirs:
            if cache_dir.exists():
                try:
                    shutil.rmtree(cache_dir)
                    self.log_action("REMOVED_CACHE", cache_dir)
                except Exception as e:
                    logger.error(f"Error removing {cache_dir}: {e}")

        # Get size after cleanup
        size_after = self.get_directory_size(xcmd_root)
        space_saved = size_before - size_after

        if space_saved > 0:
            self.space_saved += space_saved
            self.log_action("XCMD_CACHE_CLEANED", xcmd_root, space_saved)
            logger.info(f"x-cmd cache cleanup saved {space_saved} MB")

    def clean_conda_environments(self):
        """Clean up conda/miniconda environments"""
        logger.info("Cleaning conda environments...")

        # Find conda installations
        conda_paths = [
            self.home_dir / "miniforge3",
            self.home_dir / "miniconda3",
            self.home_dir / "anaconda3",
            self.home_dir / ".conda",
        ]

        for conda_path in conda_paths:
            if conda_path.exists():
                size_before = self.get_directory_size(conda_path)

                # Clean conda cache
                try:
                    subprocess.run(
                        ["conda", "clean", "--all", "--yes"],
                        cwd=str(conda_path),
                        timeout=300,
                    )
                    self.log_action("CONDA_CLEANED", conda_path)
                except Exception as e:
                    logger.error(f"Error cleaning conda: {e}")

                # Remove old environments
                envs_dir = conda_path / "envs"
                if envs_dir.exists():
                    for env_dir in envs_dir.iterdir():
                        if env_dir.is_dir():
                            try:
                                env_size = self.get_directory_size(env_dir)
                                shutil.rmtree(env_dir)
                                self.space_saved += env_size
                                self.log_action("REMOVED_ENV", env_dir, env_size)
                            except Exception as e:
                                logger.error(f"Error removing env {env_dir}: {e}")

                size_after = self.get_directory_size(conda_path)
                space_saved = size_before - size_after
                if space_saved > 0:
                    self.space_saved += space_saved
                    logger.info(f"Conda cleanup saved {space_saved} MB")

    def clean_virtual_environments(self):
        """Clean up Python virtual environments"""
        logger.info("Cleaning virtual environments...")

        # Find all .venv directories
        venv_dirs = []
        for root, dirs, files in os.walk(self.home_dir):
            if ".venv" in dirs:
                venv_path = Path(root) / ".venv"
                venv_dirs.append(venv_path)

        logger.info(f"Found {len(venv_dirs)} virtual environments")

        for venv_dir in venv_dirs:
            try:
                size_before = self.get_directory_size(venv_dir)

                # Check if it's actively used
                if self.is_venv_active(venv_dir):
                    logger.info(f"Keeping active venv: {venv_dir}")
                    continue

                # Remove the virtual environment
                shutil.rmtree(venv_dir)
                self.space_saved += size_before
                self.files_removed += len(list(venv_dir.rglob("*")))
                self.dirs_removed += 1

                self.log_action("REMOVED_VENV", venv_dir, size_before)
                logger.info(f"Removed venv: {venv_dir} ({size_before} MB)")

            except Exception as e:
                logger.error(f"Error removing venv {venv_dir}: {e}")

    def is_venv_active(self, venv_path):
        """Check if virtual environment is actively used"""
        try:
            # Check for recent activity (files modified in last 30 days)
            recent_files = []
            for file_path in venv_path.rglob("*"):
                if file_path.is_file():
                    if file_path.stat().st_mtime > time.time() - (30 * 24 * 60 * 60):
                        recent_files.append(file_path)
                        if (
                            len(recent_files) > 10
                        ):  # If many recent files, consider active
                            return True

            # Check if it's in a git repository (likely active project)
            git_dir = venv_path.parent / ".git"
            if git_dir.exists():
                return True

            return False
        except:
            return False

    def clean_python_cache(self):
        """Clean up Python cache files"""
        logger.info("Cleaning Python cache files...")

        cache_patterns = [
            "**/__pycache__",
            "**/*.pyc",
            "**/*.pyo",
            "**/*.pyd",
            "**/.pytest_cache",
            "**/.mypy_cache",
            "**/.coverage",
        ]

        for pattern in cache_patterns:
            for cache_path in self.home_dir.glob(pattern):
                try:
                    if cache_path.is_file():
                        size = cache_path.stat().st_size / (1024 * 1024)
                        cache_path.unlink()
                        self.space_saved += size
                        self.files_removed += 1
                        self.log_action("REMOVED_CACHE_FILE", cache_path, size)
                    elif cache_path.is_dir():
                        size = self.get_directory_size(cache_path)
                        shutil.rmtree(cache_path)
                        self.space_saved += size
                        self.dirs_removed += 1
                        self.log_action("REMOVED_CACHE_DIR", cache_path, size)
                except Exception as e:
                    logger.error(f"Error removing cache {cache_path}: {e}")

    def clean_node_modules(self):
        """Clean up node_modules directories"""
        logger.info("Cleaning node_modules directories...")

        for node_modules in self.home_dir.rglob("node_modules"):
            try:
                size = self.get_directory_size(node_modules)
                shutil.rmtree(node_modules)
                self.space_saved += size
                self.dirs_removed += 1
                self.log_action("REMOVED_NODE_MODULES", node_modules, size)
                logger.info(f"Removed node_modules: {node_modules} ({size} MB)")
            except Exception as e:
                logger.error(f"Error removing node_modules {node_modules}: {e}")

    def clean_empty_directories(self):
        """Remove empty directories"""
        logger.info("Cleaning empty directories...")

        # Find empty directories (bottom-up)
        for root, dirs, files in os.walk(self.home_dir, topdown=False):
            for dir_name in dirs:
                dir_path = Path(root) / dir_name
                try:
                    if not any(dir_path.iterdir()):  # Directory is empty
                        dir_path.rmdir()
                        self.dirs_removed += 1
                        self.log_action("REMOVED_EMPTY_DIR", dir_path)
                except Exception as e:
                    logger.error(f"Error removing empty dir {dir_path}: {e}")

    def create_cleanup_report(self):
        """Create cleanup report"""
        report_file = self.home_dir / "DEEP_STRUCTURE_CLEANUP_REPORT.txt"

        with open(report_file, "w") as f:
            f.write("=== DEEP STRUCTURE CLEANUP REPORT ===\n\n")
            f.write(f"Cleanup Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"Total Time: {time.time() - self.start_time:.2f} seconds\n\n")

            f.write("=== SUMMARY ===\n")
            f.write(f"Space Saved: {self.space_saved:.2f} MB\n")
            f.write(f"Files Removed: {self.files_removed:,}\n")
            f.write(f"Directories Removed: {self.dirs_removed:,}\n\n")

            f.write("=== ACTIONS TAKEN ===\n")
            for action in self.cleanup_log:
                f.write(
                    f"{action['timestamp']} | {action['action']} | "
                    f"{action['path']} | {action['size_mb']:.2f} MB\n"
                )

            f.write("\n=== RECOMMENDATIONS ===\n")
            f.write("1. Regularly clean virtual environments\n")
            f.write("2. Use conda clean --all periodically\n")
            f.write("3. Remove unused development tools\n")
            f.write("4. Consider using lighter alternatives to heavy IDEs\n")
            f.write("5. Use .gitignore to exclude build artifacts\n")

        logger.info(f"Cleanup report saved to {report_file}")

    def run_cleanup(self):
        """Run the complete cleanup process"""
        logger.info("Starting deep structure cleanup...")

        self.clean_xcmd_cache()
        self.clean_conda_environments()
        self.clean_virtual_environments()
        self.clean_python_cache()
        self.clean_node_modules()
        self.clean_empty_directories()
        self.create_cleanup_report()

        logger.info("Deep structure cleanup completed!")
        logger.info(f"Total space saved: {self.space_saved:.2f} MB")
        logger.info(f"Files removed: {self.files_removed:,}")
        logger.info(f"Directories removed: {self.dirs_removed:,}")


if __name__ == "__main__":
    home_dir = "~"
    cleaner = DeepStructureCleanup(home_dir)
    cleaner.run_cleanup()
