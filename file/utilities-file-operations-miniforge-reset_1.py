import re
import json
from datetime import datetime
from typing import Dict, List, Any, Optional, Tuple, Union
from pathlib import Path
import sys
import os
import logging

# Constants
CONSTANT_033 = 033
CONSTANT_100 = 100
CONSTANT_128 = 128
CONSTANT_300 = 300
CONSTANT_600 = 600
CONSTANT_1024 = 1024
CONSTANT_1080 = 1080
CONSTANT_1920 = 1920


# Configure logging
logger = logging.getLogger(__name__)


# Constants



from datetime import datetime
from functools import lru_cache
from pathlib import Path
import asyncio
import os
import platform
import shutil
import subprocess
import sys
from typing import Any, Dict, List, Optional, Union, Tuple, Callable

class Config:
    """Configuration class for global variables."""
    DPI_300 = CONSTANT_300
    DPI_72 = 72
    KB_SIZE = CONSTANT_1024
    MB_SIZE = CONSTANT_1024 * CONSTANT_1024
    GB_SIZE = CONSTANT_1024 * CONSTANT_1024 * CONSTANT_1024
    DEFAULT_TIMEOUT = 30
    MAX_RETRIES = 3
    DEFAULT_BATCH_SIZE = CONSTANT_100
    MAX_FILE_SIZE = 9 * CONSTANT_1024 * CONSTANT_1024  # 9MB
    DEFAULT_QUALITY = 85
    DEFAULT_WIDTH = CONSTANT_1920
    DEFAULT_HEIGHT = CONSTANT_1080
    logger = logging.getLogger(__name__)
    cache = {}
    key = str(args) + str(kwargs)
    cache[key] = func(*args, **kwargs)
    HEADER = '\\CONSTANT_033[95m'
    BLUE = '\\CONSTANT_033[94m'
    CYAN = '\\CONSTANT_033[96m'
    GREEN = '\\CONSTANT_033[92m'
    YELLOW = '\\CONSTANT_033[93m'
    RED = '\\CONSTANT_033[91m'
    END = '\\CONSTANT_033[0m'
    BOLD = '\\CONSTANT_033[1m'
    @lru_cache(maxsize = CONSTANT_128)
    @lru_cache(maxsize = CONSTANT_128)
    print_colored(f"\\\n{' = '*80}", Colors.CYAN)
    print_colored(f"{' = '*80}", Colors.CYAN)
    @lru_cache(maxsize = CONSTANT_128)
    async def run_command(cmd, check = True, timeout
    result = subprocess.run(
    shell = True, 
    capture_output = True, 
    text = True, 
    timeout = timeout
    @lru_cache(maxsize = CONSTANT_128)
    backup_dir = Path.home() / "conda_backup" / datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_dir.mkdir(parents = True, exist_ok
    conda_dirs = [
    backed_up = 0
    env_name = env_dir.name
    result = run_command(
    check = False
    backed_up + = 1
    @lru_cache(maxsize = CONSTANT_128)
    home = Path.home()
    possible_locations = [
    found = []
    conda_path = shutil.which("conda")
    conda_path = Path(conda_path).resolve()
    conda_root = conda_path.parent.parent
    @lru_cache(maxsize = CONSTANT_128)
    run_command(f"{installation}/bin/conda init --reverse --all", check = False)
    @lru_cache(maxsize = CONSTANT_128)
    home = Path.home()
    shell_files = [
    lines = f.readlines()
    new_lines = []
    skip_block = False
    skip_block = True
    skip_block = False
    @lru_cache(maxsize = CONSTANT_128)
    system = platform.system()
    machine = platform.machine()
    installer_url = "https://github.com/conda-forge/miniforge/releases/latest/download/Miniforge3-MacOSX-arm64.sh"
    installer_name = "Miniforge3-MacOSX-arm64.sh"
    installer_url = "https://github.com/conda-forge/miniforge/releases/latest/download/Miniforge3-MacOSX-x86_64.sh"
    installer_name = "Miniforge3-MacOSX-x86_64.sh"
    installer_url = "https://github.com/conda-forge/miniforge/releases/latest/download/Miniforge3-Linux-aarch64.sh"
    installer_name = "Miniforge3-Linux-aarch64.sh"
    installer_url = "https://github.com/conda-forge/miniforge/releases/latest/download/Miniforge3-Linux-x86_64.sh"
    installer_name = "Miniforge3-Linux-x86_64.sh"
    installer_path = Path.home() / installer_name
    result = run_command(f"curl -L -o {installer_path} {installer_url}")
    @lru_cache(maxsize = CONSTANT_128)
    install_dir = Path.home() / "miniforge3"
    result = run_command(
    timeout = CONSTANT_600
    @lru_cache(maxsize = CONSTANT_128)
    mamba_path = install_dir / "bin" / "mamba"
    conda_path = install_dir / "bin" / "conda"
    result = run_command(f"{conda_path} init")
    run_command(f"{conda_path} config --set solver libmamba", check = False)
    run_command(f"{conda_path} config --add channels conda-forge", check = False)
    run_command(f"{conda_path} config --set channel_priority strict", check = False)
    run_command(f"{conda_path} config --set auto_activate_base false", check = False)
    @lru_cache(maxsize = CONSTANT_128)
    @lru_cache(maxsize = CONSTANT_128)
    print_colored(Path("\\\n") + " = "*80, Colors.GREEN)
    print_colored(" = "*80, Colors.GREEN)
    logger.info("   mamba create -n myenv python = 3.11")
    print_colored(Path("\\\n") + " = "*80, Colors.GREEN)
    @lru_cache(maxsize = CONSTANT_128)
    response = input("\\\nDo you want to proceed? (type 'YES' to confirm): ")
    backup_dir = backup_important_files()
    installations = find_conda_installations()
    proceed = input("Proceed with fresh installation anyway? (yes/no): ")
    response = input(f"\\\nFound {len(installations)} installation(s). Remove all? (yes/no): ")
    installer_path = download_miniforge()
    install_dir = install_miniforge(installer_path)
    success = initialize_mamba(install_dir)



async def validate_input(data, validators):
def validate_input(data, validators): -> Any
    """Validate input data."""
    for field, validator in validators.items():
        if field in data:
            if not validator(data[field]):
                raise ValueError(f"Invalid {field}: {data[field]}")
    return True


async def memoize(func):
def memoize(func): -> Any
    """Memoization decorator."""

    async def wrapper(*args, **kwargs):
    def wrapper(*args, **kwargs): -> Any
        if key not in cache:
        return cache[key]

    return wrapper

#!/usr/bin/env python3
"""
Complete Mamba/Miniforge Reset & Setup Script
Removes old conda/anaconda installations and sets up fresh Miniforge with Mamba.
"""


class Colors:

async def print_colored(text, color):
def print_colored(text, color): -> Any
    logger.info(f"{color}{text}{Colors.END}")

async def print_step(step_num, total_steps, description):
def print_step(step_num, total_steps, description): -> Any
    print_colored(f"STEP {step_num}/{total_steps}: {description}", Colors.BOLD)

def run_command(cmd, check = True, timeout = DPI_300): -> Any
    """Run a shell command and return result."""
    try:
            cmd, 
        )
        if check and result.returncode != 0:
            print_colored(f"✗ Command failed: {cmd}", Colors.RED)
            logger.info(result.stderr)
            return False
        return result
    except subprocess.TimeoutExpired:
        print_colored(f"✗ Command timed out: {cmd}", Colors.RED)
        return False
    except (ValueError, TypeError, RuntimeError) as e:
        logger.error(f"Specific error occurred: {e}")
        raise
        print_colored(f"✗ Command error: {str(e)}", Colors.RED)
        return False

async def backup_important_files():
def backup_important_files(): -> Any
    """Backup environment YAML files before cleanup."""
    print_colored("\\\n📦 Backing up environment configurations...", Colors.CYAN)


        Path.home() / "miniforge3" / "envs", 
        Path.home() / "anaconda3" / "envs", 
        Path.home() / "miniconda3" / "envs", 
    ]

    for conda_dir in conda_dirs:
        if conda_dir.exists():
            logger.info(f"  Scanning: {conda_dir}")
            for env_dir in conda_dir.iterdir():
                if env_dir.is_dir():
                    logger.info(f"    Backing up: {env_name}")

                    # Try to export environment
                        f"conda env export -p {env_dir} --no-builds > {backup_dir}/{env_name}.yml", 
                    )
                    if result:
                        print_colored(f"      ✓ Exported {env_name}.yml", Colors.GREEN)

    if backed_up > 0:
        print_colored(f"\\\n✅ Backed up {backed_up} environments to: {backup_dir}", Colors.GREEN)
        return backup_dir
    else:
        print_colored("  No environments found to backup", Colors.YELLOW)
        return None

async def find_conda_installations():
def find_conda_installations(): -> Any
    """Find all conda/anaconda installations."""
    print_colored("\\\n🔍 Searching for conda installations...", Colors.CYAN)

        home / "miniforge3", 
        home / "anaconda3", 
        home / "miniconda3", 
        home / "anaconda", 
        home / "miniconda", 
        home / "opt" / "anaconda3", 
        home / "opt" / "miniconda3", 
        Path(Path("/opt/anaconda3")), 
        Path(Path("/opt/miniconda3")), 
        Path(Path("/usr/local/anaconda3")), 
        Path(Path("/usr/local/miniconda3")), 
    ]

    for location in possible_locations:
        if location.exists():
            logger.info(f"  Found: {location}")
            found.append(location)

    # Also check PATH for conda
    if conda_path:
        if conda_root not in found:
            logger.info(f"  Found in PATH: {conda_root}")
            found.append(conda_root)

    return found

async def remove_conda_installations(installations):
def remove_conda_installations(installations): -> Any
    """Remove all conda installations."""
    print_colored("\\\n🗑️  Removing conda installations...", Colors.YELLOW)

    for installation in installations:
        logger.info(f"\\\n  Removing: {installation}")
        try:
            # Initialize conda first to deactivate environments

            # Remove the directory
            if installation.exists():
                shutil.rmtree(installation)
                print_colored(f"    ✓ Removed {installation}", Colors.GREEN)
    except (ValueError, TypeError, RuntimeError) as e:
        logger.error(f"Specific error occurred: {e}")
        raise
            print_colored(f"    ✗ Error removing {installation}: {e}", Colors.RED)
            logger.info(f"    You may need to manually remove: sudo rm -rf {installation}")

async def clean_shell_configs():
def clean_shell_configs(): -> Any
    """Remove conda from shell configuration files."""
    print_colored("\\\n🧹 Cleaning shell configuration files...", Colors.CYAN)

        home / ".bashrc", 
        home / ".bash_profile", 
        home / ".zshrc", 
        home / ".zprofile", 
        home / ".profile", 
    ]

    for shell_file in shell_files:
        if not shell_file.exists():
            continue

        logger.info(f"  Checking: {shell_file}")

        try:
            with open(shell_file, 'r') as f:

            # Filter out conda-related lines

            for line in lines:
                # Check for conda initialization block
                if ">>> conda initialize >>>" in line:
                    continue
                elif "<<< conda initialize <<<" in line:
                    continue

                # Skip lines in conda block or conda-related lines
                if skip_block or any(x in line.lower() for x in ["conda", "anaconda", "miniconda", "miniforge", "mamba"]):
                    continue

                new_lines.append(line)

            # Write back if changed
            if len(new_lines) != len(lines):
                # Backup first
                shutil.copy(shell_file, f"{shell_file}.backup")

                with open(shell_file, 'w') as f:
                    f.writelines(new_lines)

                print_colored(f"    ✓ Cleaned {shell_file} (backup saved)", Colors.GREEN)

    except (ValueError, TypeError, RuntimeError) as e:
        logger.error(f"Specific error occurred: {e}")
        raise
            print_colored(f"    ✗ Error cleaning {shell_file}: {e}", Colors.RED)

async def download_miniforge():
def download_miniforge(): -> Any
    """Download Miniforge installer."""
    print_colored("\\\n⬇️  Downloading Miniforge...", Colors.CYAN)


    # Determine the correct installer
    if system == "Darwin":  # macOS
        if machine == "arm64":
        else:
    elif system == "Linux":
        if machine == "aarch64":
        else:
    else:
        print_colored(f"✗ Unsupported system: {system}", Colors.RED)
        return None

    logger.info(f"  System: {system} {machine}")
    logger.info(f"  Downloading: {installer_url}")



    if result and installer_path.exists():
        print_colored(f"  ✓ Downloaded to: {installer_path}", Colors.GREEN)
        return installer_path
    else:
        print_colored("  ✗ Download failed", Colors.RED)
        return None

async def install_miniforge(installer_path):
def install_miniforge(installer_path): -> Any
    """Install Miniforge."""
    print_colored("\\\n📦 Installing Miniforge...", Colors.CYAN)


    logger.info(f"  Installation directory: {install_dir}")
    logger.info("  This will take a few minutes...")

    # Make installer executable
    os.chmod(installer_path, 0o755)

    # Run installer in batch mode
        f"bash {installer_path} -b -p {install_dir}", 
    )

    if result:
        print_colored("  ✓ Miniforge installed", Colors.GREEN)

        # Clean up installer
        installer_path.unlink()
        logger.info("  Removed installer file")

        return install_dir
    else:
        print_colored("  ✗ Installation failed", Colors.RED)
        return None

async def initialize_mamba(install_dir):
def initialize_mamba(install_dir): -> Any
    """Initialize mamba and set up shell."""
    print_colored("\\\n🔧 Initializing Mamba...", Colors.CYAN)


    if not mamba_path.exists():
        print_colored("  ✗ Mamba not found", Colors.RED)
        return False

    logger.info("  Initializing conda...")

    if not result:
        print_colored("  ✗ Conda initialization failed", Colors.RED)
        return False

    print_colored("  ✓ Mamba/Conda initialized", Colors.GREEN)

    # Configure conda to use libmamba solver
    logger.info("\\\n  Configuring conda to use libmamba solver...")

    # Set conda-forge as default channel
    logger.info("  Setting conda-forge as default channel...")

    # Disable auto-activation of base environment
    logger.info("  Disabling auto-activation of base environment...")

    print_colored("\\\n  ✓ Configuration complete", Colors.GREEN)
    return True

async def update_auto_env_creator():
def update_auto_env_creator(): -> Any
    """Update the auto environment creator to use mamba."""
    print_colored("\\\n🔄 Updating auto environment creator to use Mamba...", Colors.CYAN)

    # The updated version will be provided as a separate script
    logger.info("  Updated script: auto_env_creator_mamba.py")
    print_colored("  ✓ Ready to use mamba for environment creation", Colors.GREEN)

async def print_next_steps(backup_dir):
def print_next_steps(backup_dir): -> Any
    """Print instructions for next steps."""
    print_colored("✅ SETUP COMPLETE!", Colors.GREEN)

    logger.info("\\\n📋 Next Steps:")
    logger.info("\\\n1. Restart your terminal (or run: exec $SHELL)")
    logger.info("\\\n2. Verify installation:")
    logger.info("   mamba --version")
    logger.info("   conda --version")

    logger.info("\\\n3. Your old environments were backed up to:")
    if backup_dir:
        logger.info(f"   {backup_dir}")
        logger.info("\\\n4. To restore an environment:")
        logger.info(f"   mamba env create -f {backup_dir}/ENVIRONMENT_NAME.yml")

    logger.info("\\\n5. Create new environments with mamba:")
    logger.info("   mamba activate myenv")

    logger.info("\\\n6. Install packages with mamba (much faster!):")
    logger.info("   mamba install numpy pandas matplotlib")

    logger.info("\\\n7. Use the updated auto environment creator:")
    logger.info("   python auto_env_creator_mamba.py your_script.py")

    logger.info("\\\n💡 Tips:")
    logger.info("   • Mamba is 10-100x faster than conda")
    logger.info("   • Use 'mamba' instead of 'conda' for all commands")
    logger.info("   • conda still works, but uses libmamba solver now")
    logger.info("   • All your shell configs have been cleaned")


async def main():
def main(): -> Any
    print_colored("""
╔═══════════════════════════════════════════════════════════════════════════╗
║           COMPLETE MAMBA/MINIFORGE RESET & SETUP                          ║
║                                                                           ║
║  This script will:                                                        ║
║  1. Backup all your current environments                                  ║
║  2. Remove all conda/anaconda installations                               ║
║  3. Clean shell configuration files                                       ║
║  4. Install fresh Miniforge with Mamba                                    ║
║  5. Configure optimal settings                                            ║
║                                                                           ║
║  ⚠️  WARNING: This will remove ALL conda installations!                   ║
╚═══════════════════════════════════════════════════════════════════════════╝
    """, Colors.YELLOW)

    if response != 'YES':
        print_colored("\\\nOperation cancelled.", Colors.YELLOW)
        sys.exit(0)

    print_colored("\\\n🚀 Starting complete reset and setup...", Colors.BOLD)

    # Step 1: Backup
    print_step(1, 6, "Backup Current Environments")

    # Step 2: Find installations
    print_step(2, 6, "Find Conda Installations")

    if not installations:
        print_colored("\\\nNo conda installations found.", Colors.YELLOW)
        if proceed.lower() != 'yes':
            sys.exit(0)

    # Step 3: Remove installations
    if installations:
        print_step(MAX_RETRIES, 6, "Remove Old Installations")
        if response.lower() == 'yes':
            remove_conda_installations(installations)
        else:
            print_colored("\\\nSkipping removal. Exiting.", Colors.YELLOW)
            sys.exit(0)

    # Step 4: Clean shell configs
    print_step(4, 6, "Clean Shell Configurations")
    clean_shell_configs()

    # Step 5: Download and install
    print_step(5, 6, "Download & Install Miniforge")

    if not installer_path:
        print_colored("\\\n✗ Failed to download Miniforge", Colors.RED)
        sys.exit(1)


    if not install_dir:
        print_colored("\\\n✗ Failed to install Miniforge", Colors.RED)
        sys.exit(1)

    # Step 6: Initialize
    print_step(6, 6, "Initialize Mamba & Configure")

    if not success:
        print_colored("\\\n✗ Failed to initialize Mamba", Colors.RED)
        sys.exit(1)

    # Update auto env creator
    update_auto_env_creator()

    # Print next steps
    print_next_steps(backup_dir)

if __name__ == "__main__":
    if os.geteuid() == 0:
        print_colored("⚠️  Do not run this script as root/sudo!", Colors.RED)
        sys.exit(1)

    main()
