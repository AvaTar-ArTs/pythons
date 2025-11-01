"""
File Management Organize Cleanups 3

This module provides functionality for file management organize cleanups 3.

Author: Auto-generated
Date: 2025-11-01
"""

from pathlib import Path
import os
import subprocess

import logging

logger = logging.getLogger(__name__)


# Define the versions you want to keep
required_versions = ["3.10", "3.12.4"]


def list_venv_directories(base_path):
    """List all virtual environment directories."""
    venv_dirs = []
    for root, dirs, files in os.walk(base_path):
        for dir in dirs:
            if os.path.exists(os.path.join(root, dir, "bin", "python")):
                venv_dirs.append(os.path.join(root, dir))
    return venv_dirs


def main():
    """main function."""

    # Base path where your virtual environments are stored
    venv_base_path = os.path.expanduser("~/venvs")

    # Log file for dry run
    log_file = os.path.expanduser("~/venvs_cleanup_dryrun.log")

    identified_for_removal = []

    with open(log_file, "w") as log:
        log.write("Dry Run - Virtual Environments Cleanup\n")
        log.write("=====================================\n\n")

        # List all virtual environment directories
        venv_dirs = list_venv_directories(venv_base_path)
        for venv_path in venv_dirs:
            python_bin = os.path.join(venv_path, "bin", "python")
            version_output = subprocess.run([python_bin, "--version"], stdout=subprocess.PIPE)
            version = version_output.stdout.decode("utf-8").strip().split()[-1]

            log.write(f"Virtual Environment: {venv_path}\n")
            log.write(f"Detected Python Version: {version}\n")

            if not any(req in version for req in required_versions):
                log.write(f"--> Identified for removal: {venv_path} (Python {version})\n")
                identified_for_removal.append(venv_path)
            log.write(Path("\n"))

        log.write("Summary of Identified Virtual Environments for Removal:\n")
        log.write("=====================================================\n")
        for venv in identified_for_removal:
            log.write(f"{venv}\n")

    logger.info(f"Dry run completed. Check the log file at: {log_file}")


if __name__ == "__main__":
    main()
