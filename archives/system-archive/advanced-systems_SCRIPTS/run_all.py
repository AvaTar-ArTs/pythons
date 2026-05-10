#!/usr/bin/env python3
"""
Master Runner Script for All Media File Organizers

This script provides a convenient way to run all media file organizer scripts
with proper configuration and error handling.
"""

import os
import sys
import subprocess
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# Script paths
SCRIPTS = {
    "videos": "/Users/steven/clean/vids/vids.py",
    "audio": "/Users/steven/clean/audio/audio_combined.py",
    "images": "/Users/steven/clean/img/img_combined.py",
    "documents": "/Users/steven/clean/docs/docs_combined.py",
}


def check_script_exists(script_path):
    """Check if a script file exists."""
    if not os.path.exists(script_path):
        logger.error(f"Script not found: {script_path}")
        return False
    return True


def run_script(script_name, script_path, async_mode=False):
    """Run a single script."""
    logger.info(f"Running {script_name} script...")

    if not check_script_exists(script_path):
        return False

    try:
        cmd = ["python3", script_path]
        if async_mode:
            cmd.append("--async")

        result = subprocess.run(cmd, capture_output=True, text=True, timeout=300)

        if result.returncode == 0:
            logger.info(f"{script_name} script completed successfully")
            if result.stdout:
                logger.info(f"Output: {result.stdout}")
            return True
        else:
            logger.error(
                f"{script_name} script failed with return code {result.returncode}"
            )
            if result.stderr:
                logger.error(f"Error: {result.stderr}")
            return False

    except subprocess.TimeoutExpired:
        logger.error(f"{script_name} script timed out after 5 minutes")
        return False
    except Exception as e:
        logger.error(f"Error running {script_name} script: {e}")
        return False


def run_all_scripts(async_mode=False):
    """Run all scripts in sequence."""
    logger.info("Starting all media file organizer scripts...")

    results = {}
    for script_name, script_path in SCRIPTS.items():
        results[script_name] = run_script(script_name, script_path, async_mode)

    # Summary
    successful = sum(1 for success in results.values() if success)
    total = len(results)

    logger.info("\n=== SUMMARY ===")
    logger.info(f"Successfully completed: {successful}/{total} scripts")

    for script_name, success in results.items():
        status = "✓ SUCCESS" if success else "✗ FAILED"
        logger.info(f"{script_name}: {status}")

    return results


def run_single_script(script_name, async_mode=False):
    """Run a single script by name."""
    if script_name not in SCRIPTS:
        logger.error(f"Unknown script: {script_name}")
        logger.info(f"Available scripts: {', '.join(SCRIPTS.keys())}")
        return False

    script_path = SCRIPTS[script_name]
    return run_script(script_name, script_path, async_mode)


def main():
    """Main function."""
    import argparse

    parser = argparse.ArgumentParser(description="Run media file organizer scripts")
    parser.add_argument(
        "--script", choices=list(SCRIPTS.keys()), help="Run a specific script"
    )
    parser.add_argument(
        "--async-mode", action="store_true", help="Run scripts in async mode"
    )
    parser.add_argument("--list", action="store_true", help="List available scripts")

    args = parser.parse_args()

    if args.list:
        print("Available scripts:")
        for name, path in SCRIPTS.items():
            status = "✓" if os.path.exists(path) else "✗"
            print(f"  {status} {name}: {path}")
        return

    if args.script:
        success = run_single_script(args.script, getattr(args, "async_mode", False))
        sys.exit(0 if success else 1)
    else:
        results = run_all_scripts(getattr(args, "async_mode", False))
        # Exit with error code if any script failed
        sys.exit(0 if all(results.values()) else 1)


if __name__ == "__main__":
    main()
