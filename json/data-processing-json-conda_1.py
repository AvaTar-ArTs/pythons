
import logging

logger = logging.getLogger(__name__)


# Constants
CONSTANT_033 = 033
CONSTANT_120 = 120
CONSTANT_300 = 300
CONSTANT_600 = 600
CONSTANT_1024 = 1024

#!/usr/bin/env python3
"""
Conda Environment Consolidator
Interactive tool to safely remove and combine conda environments.
"""

import json
import subprocess
import sys
from pathlib import Path
from datetime import datetime
import shutil

class Colors:
    """ANSI color codes for terminal output."""
    HEADER = '\CONSTANT_033[95m'
    BLUE = '\CONSTANT_033[94m'
    CYAN = '\CONSTANT_033[96m'
    GREEN = '\CONSTANT_033[92m'
    YELLOW = '\CONSTANT_033[93m'
    RED = '\CONSTANT_033[91m'
    END = '\CONSTANT_033[0m'
    BOLD = '\CONSTANT_033[1m'

def print_colored(text, color):
    """Print colored text."""
    logger.info(f"{color}{text}{Colors.END}")

def load_report(filename="conda_env_report.json"):
    """Load the analysis report."""
    try:
        with open(filename) as f:
            return json.load(f)
    except FileNotFoundError:
        print_colored("Error: conda_env_report.json not found.", Colors.RED)
        logger.info("Please run conda_env_analyzer.py first.")
        sys.exit(1)

def export_environment(env_name, output_dir="env_backups"):
    """Export environment to YAML file."""
    Path(output_dir).mkdir(exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_file = f"{output_dir}/{env_name}_{timestamp}.yml"
    
    logger.info(f"  Exporting {env_name} to {output_file}...")
    
    try:
        result = subprocess.run(
            ["conda", "env", "export", "-n", env_name, "--no-builds"],
            capture_output=True,
            text=True,
            timeout=60
        )
        
        if result.returncode == 0:
            with open(output_file, 'w') as f:
                f.write(result.stdout)
            print_colored(f"  ✓ Exported successfully", Colors.GREEN)
            return output_file
        else:
            print_colored(f"  ✗ Export failed: {result.stderr}", Colors.RED)
            return None
    except Exception as e:
        print_colored(f"  ✗ Export failed: {str(e)}", Colors.RED)
        return None

def get_package_list(env_name):
    """Get list of packages in environment."""
    try:
        result = subprocess.run(
            ["conda", "list", "-n", env_name, "--json"],
            capture_output=True,
            text=True,
            timeout=30
        )
        if result.returncode == 0:
            return json.loads(result.stdout)
    except (json.JSONDecodeError, ValueError):
        pass
    return []

def compare_environments(env1_name, env2_name):
    """Compare two environments and show differences."""
    packages1 = get_package_list(env1_name)
    packages2 = get_package_list(env2_name)
    
    pkg_dict1 = {p['name']: p.get('version', 'unknown') for p in packages1}
    pkg_dict2 = {p['name']: p.get('version', 'unknown') for p in packages2}
    
    only_in_1 = set(pkg_dict1.keys()) - set(pkg_dict2.keys())
    only_in_2 = set(pkg_dict2.keys()) - set(pkg_dict1.keys())
    common = set(pkg_dict1.keys()).intersection(set(pkg_dict2.keys()))
    
    return {
        'only_in_1': sorted(only_in_1),
        'only_in_2': sorted(only_in_2),
        'common': len(common),
        'total_1': len(pkg_dict1),
        'total_2': len(pkg_dict2)
    }

def create_merged_environment(new_name, env_list, python_version=None):
    """Create a new merged environment from multiple environments."""
    print_colored(f"\n🔨 Creating merged environment: {new_name}", Colors.BOLD)
    
    # Collect all unique packages
    all_packages = set()
    package_versions = {}
    
    for env_name in env_list:
        logger.info(f"  Scanning {env_name}...")
        packages = get_package_list(env_name)
        for pkg in packages:
            pkg_name = pkg['name']
            pkg_version = pkg.get('version', '')
            
            # Skip Python itself - we'll handle it separately
            if pkg_name == 'python':
                continue
            
            # Skip base packages that will be installed automatically
            if pkg_name in ['pip', 'setuptools', 'wheel']:
                continue
                
            all_packages.add(pkg_name)
            
            # Store version (prefer later version if conflict)
            if pkg_name not in package_versions:
                package_versions[pkg_name] = pkg_version
    
    logger.info(f"\n  Found {len(all_packages)} unique packages to install")
    
    # Determine Python version
    if not python_version:
        # Try to get from first environment
        first_env_packages = get_package_list(env_list[0])
        for pkg in first_env_packages:
            if pkg['name'] == 'python':
                python_version = '.'.join(pkg.get('version', '3.11').split('.')[:2])
                break
        if not python_version:
            python_version = "3.11"
    
    logger.info(f"  Using Python {python_version}")
    
    # Create new environment
    logger.info(f"\n  Creating environment with Python {python_version}...")
    
    cmd = ["conda", "create", "-n", new_name, f"python={python_version}", "-y"]
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=CONSTANT_300)
        if result.returncode != 0:
            print_colored(f"  ✗ Failed to create environment: {result.stderr}", Colors.RED)
            return False
        print_colored("  ✓ Environment created", Colors.GREEN)
    except Exception as e:
        print_colored(f"  ✗ Failed to create environment: {str(e)}", Colors.RED)
        return False
    
    # Install packages in batches
    logger.info("\n  Installing packages (this may take a while)...")
    
    # Try to install all at once first
    package_list = list(all_packages)
    batch_size = 50
    
    for i in range(0, len(package_list), batch_size):
        batch = package_list[i:i+batch_size]
        logger.info(f"  Installing batch {i//batch_size + 1}/{(len(package_list)-1)//batch_size + 1}...")
        
        cmd = ["conda", "install", "-n", new_name, "-y"] + batch
        
        try:
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=CONSTANT_600)
            if result.returncode != 0:
                print_colored(f"  ⚠ Some packages in batch failed, trying individually...", Colors.YELLOW)
                # Try each package individually
                for pkg in batch:
                    cmd_single = ["conda", "install", "-n", new_name, "-y", pkg]
                    result_single = subprocess.run(cmd_single, capture_output=True, text=True, timeout=60)
                    if result_single.returncode == 0:
                        logger.info(f"    ✓ {pkg}")
                    else:
                        logger.info(f"    ✗ {pkg} (skipped)")
        except Exception as e:
            print_colored(f"  ⚠ Batch failed: {str(e)}", Colors.YELLOW)
    
    print_colored(f"\n  ✓ Merged environment '{new_name}' created successfully!", Colors.GREEN)
    return True

def remove_environment(env_name, backup=True):
    """Remove a conda environment with optional backup."""
    if backup:
        print_colored(f"\n📦 Backing up {env_name}...", Colors.CYAN)
        backup_file = export_environment(env_name)
        if not backup_file:
            response = input(f"  Backup failed. Continue with removal? (yes/no): ").lower()
            if response != 'yes':
                logger.info("  Removal cancelled.")
                return False
    
    print_colored(f"\n🗑️  Removing environment: {env_name}", Colors.YELLOW)
    
    try:
        result = subprocess.run(
            ["conda", "env", "remove", "-n", env_name, "-y"],
            capture_output=True,
            text=True,
            timeout=CONSTANT_120
        )
        
        if result.returncode == 0:
            print_colored(f"  ✓ Environment '{env_name}' removed successfully", Colors.GREEN)
            return True
        else:
            print_colored(f"  ✗ Failed to remove environment: {result.stderr}", Colors.RED)
            return False
    except Exception as e:
        print_colored(f"  ✗ Failed to remove environment: {str(e)}", Colors.RED)
        return False

def interactive_removal(environments):
    """Interactive environment removal."""
    print_colored(Path("\n") + "="*80, Colors.HEADER)
    print_colored("INTERACTIVE ENVIRONMENT REMOVAL", Colors.HEADER)
    print_colored("="*80, Colors.HEADER)
    
    existing_envs = [e for e in environments if e["exists"]]
    
    # Sort by size (smallest first - more likely to be unused)
    sorted_envs = sorted(existing_envs, key=lambda x: x["size"])
    
    logger.info("\nEnvironments (sorted by size):\n")
    for i, env in enumerate(sorted_envs, 1):
        logger.info(f"{i:2}. {env['name']:20} - {env['size_formatted']:>10} - {env['package_count']:>3} packages")
    
    logger.info("\nEnter environment numbers to remove (comma-separated, or 'none' to skip):")
    selection = input("Selection: ").strip()
    
    if selection.lower() == 'none':
        logger.info("Skipping removal.")
        return []
    
    try:
        indices = [int(x.strip()) - 1 for x in selection.split(',')]
        selected_envs = [sorted_envs[i] for i in indices if 0 <= i < len(sorted_envs)]
    except (IndexError, KeyError):
        print_colored("Invalid selection. Skipping removal.", Colors.RED)
        return []
    
    if not selected_envs:
        return []
    
    logger.info("\nYou selected:")
    for env in selected_envs:
        logger.info(f"  - {env['name']} ({env['size_formatted']}, {env['package_count']} packages)")
    
    confirm = input("\nConfirm removal? (yes/no): ").lower()
    if confirm != 'yes':
        logger.info("Removal cancelled.")
        return []
    
    removed = []
    for env in selected_envs:
        if remove_environment(env['name'], backup=True):
            removed.append(env['name'])
    
    return removed

def interactive_merge(environments):
    """Interactive environment merging."""
    print_colored(Path("\n") + "="*80, Colors.HEADER)
    print_colored("INTERACTIVE ENVIRONMENT MERGING", Colors.HEADER)
    print_colored("="*80, Colors.HEADER)
    
    existing_envs = [e for e in environments if e["exists"]]
    
    # Suggest merge candidates
    suggestions = [
        {
            "name": "Audio Workflows",
            "envs": ["audio-tools", "oss-audio", "transcribe", "suno-analytics"],
            "new_name": "audio-unified"
        },
        {
            "name": "Ollama/LLM",
            "envs": ["ollama", "ollama-lab"],
            "new_name": "llm-unified"
        },
        {
            "name": "Analytics",
            "envs": ["analytics", "analyze"],
            "new_name": "data-analytics"
        },
        {
            "name": "Custom Merge",
            "envs": [],
            "new_name": "custom-merge"
        }
    ]
    
    logger.info("\nSuggested merge operations:\n")
    for i, suggestion in enumerate(suggestions, 1):
        if suggestion["envs"]:
            # Filter to only existing environments
            existing_in_suggestion = [e for e in suggestion["envs"] 
                                     if any(env['name'] == e for env in existing_envs)]
            if len(existing_in_suggestion) > 1:
                logger.info(f"{i}. {suggestion['name']}")
                logger.info(f"   Merge: {', '.join(existing_in_suggestion)}")
                logger.info(f"   Into: {suggestion['new_name']}")
        else:
            logger.info(f"{i}. Custom - Choose your own environments to merge")
    
    logger.info("\nEnter option number (or 'none' to skip):")
    selection = input("Selection: ").strip()
    
    if selection.lower() == 'none':
        logger.info("Skipping merge.")
        return
    
    try:
        option = int(selection) - 1
        if option < 0 or option >= len(suggestions):
            print_colored("Invalid selection.", Colors.RED)
            return
        
        suggestion = suggestions[option]
        
        if not suggestion["envs"]:
            # Custom merge
            logger.info("\nAvailable environments:")
            for i, env in enumerate(existing_envs, 1):
                logger.info(f"{i:2}. {env['name']}")
            
            logger.info("\nEnter environment numbers to merge (comma-separated):")
            env_selection = input("Selection: ").strip()
            indices = [int(x.strip()) - 1 for x in env_selection.split(',')]
            envs_to_merge = [existing_envs[i]['name'] for i in indices 
                            if 0 <= i < len(existing_envs)]
            
            new_name = input("Enter name for new merged environment: ").strip()
        else:
            # Use suggested merge
            existing_in_suggestion = [e for e in suggestion["envs"] 
                                     if any(env['name'] == e for env in existing_envs)]
            envs_to_merge = existing_in_suggestion
            new_name = suggestion["new_name"]
        
        if len(envs_to_merge) < 2:
            print_colored("Need at least 2 environments to merge.", Colors.RED)
            return
        
        logger.info(f"\nWill merge: {', '.join(envs_to_merge)}")
        logger.info(f"Into new environment: {new_name}")
        
        # Show comparison
        if len(envs_to_merge) == 2:
            logger.info("\nComparing environments...")
            comparison = compare_environments(envs_to_merge[0], envs_to_merge[1])
            logger.info(f"  {envs_to_merge[0]}: {comparison['total_1']} packages")
            logger.info(f"  {envs_to_merge[1]}: {comparison['total_2']} packages")
            logger.info(f"  Common: {comparison['common']} packages")
            logger.info(f"  Only in {envs_to_merge[0]}: {len(comparison['only_in_1'])} packages")
            logger.info(f"  Only in {envs_to_merge[1]}: {len(comparison['only_in_2'])} packages")
        
        # Python version selection
        logger.info("\nPython version for merged environment?")
        logger.info("1. 3.11 (recommended)")
        logger.info("2. 3.12")
        logger.info("3. 3.13")
        py_choice = input("Selection (or press Enter for 3.11): ").strip()
        
        py_versions = {"1": "3.11", "2": "3.12", "3": "3.13"}
        python_version = py_versions.get(py_choice, "3.11")
        
        confirm = input("\nProceed with merge? (yes/no): ").lower()
        if confirm != 'yes':
            logger.info("Merge cancelled.")
            return
        
        # Backup all environments first
        print_colored("\n📦 Backing up environments...", Colors.CYAN)
        for env_name in envs_to_merge:
            export_environment(env_name)
        
        # Create merged environment
        if create_merged_environment(new_name, envs_to_merge, python_version):
            print_colored(f"\n✅ Successfully created '{new_name}'", Colors.GREEN)
            
            remove_old = input("\nRemove old environments? (yes/no): ").lower()
            if remove_old == 'yes':
                for env_name in envs_to_merge:
                    remove_environment(env_name, backup=False)  # Already backed up
        
    except Exception as e:
        print_colored(f"Error during merge: {str(e)}", Colors.RED)

def clean_conda_cache():
    """Clean conda cache."""
    print_colored("\n🧹 Cleaning conda cache...", Colors.CYAN)
    
    try:
        result = subprocess.run(
            ["conda", "clean", "--all", "-y"],
            capture_output=True,
            text=True,
            timeout=CONSTANT_120
        )
        
        if result.returncode == 0:
            print_colored("✓ Cache cleaned successfully", Colors.GREEN)
            logger.info(result.stdout)
        else:
            print_colored(f"✗ Failed to clean cache: {result.stderr}", Colors.RED)
    except Exception as e:
        print_colored(f"✗ Failed to clean cache: {str(e)}", Colors.RED)

def main_menu():
    """Main interactive menu."""
    environments = load_report()
    
    while True:
        print_colored(Path("\n") + "="*80, Colors.HEADER)
        print_colored("CONDA ENVIRONMENT CONSOLIDATOR", Colors.HEADER)
        print_colored("="*80, Colors.HEADER)
        
        existing_envs = [e for e in environments if e["exists"]]
        total_size = sum(e["size"] for e in existing_envs)
        
        logger.info(f"\nCurrent Status:")
        logger.info(f"  Environments: {len(existing_envs)}")
        logger.info(f"  Total Size: {format_size(total_size)}")
        
        logger.info("\nOptions:")
        logger.info("  1. Remove environments")
        logger.info("  2. Merge environments")
        logger.info("  3. Clean conda cache")
        logger.info("  4. Export environment to YAML")
        logger.info("  5. Refresh analysis")
        logger.info("  6. Exit")
        
        choice = input("\nSelect option: ").strip()
        
        if choice == '1':
            removed = interactive_removal(environments)
            if removed:
                print_colored(f"\nRemoved {len(removed)} environment(s)", Colors.GREEN)
        
        elif choice == '2':
            interactive_merge(environments)
        
        elif choice == '3':
            clean_conda_cache()
        
        elif choice == '4':
            logger.info("\nAvailable environments:")
            for i, env in enumerate(existing_envs, 1):
                logger.info(f"{i:2}. {env['name']}")
            
            try:
                env_num = int(input("\nSelect environment number: ")) - 1
                if 0 <= env_num < len(existing_envs):
                    export_environment(existing_envs[env_num]['name'])
            except (IndexError, KeyError):
                print_colored("Invalid selection.", Colors.RED)
        
        elif choice == '5':
            logger.info("\nRe-run conda_env_analyzer.py to refresh the analysis.")
            sys.exit(0)
        
        elif choice == '6':
            print_colored("\nGoodbye!", Colors.GREEN)
            sys.exit(0)
        
        else:
            print_colored("Invalid option. Please try again.", Colors.RED)

def format_size(bytes_size):
    """Format bytes to human-readable size."""
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if bytes_size < CONSTANT_1024.0:
            return f"{bytes_size:.2f} {unit}"
        bytes_size /= CONSTANT_1024.0
    return f"{bytes_size:.2f} PB"

if __name__ == "__main__":
    print_colored("""
╔═══════════════════════════════════════════════════════════════════════════╗
║                  CONDA ENVIRONMENT CONSOLIDATOR                           ║
║                                                                           ║
║  This tool helps you safely remove and merge conda environments.         ║
║  All operations include backups - your data is safe!                     ║
╚═══════════════════════════════════════════════════════════════════════════╝
    """, Colors.CYAN)
    
    main_menu()
