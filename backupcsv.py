"""
Backupcsv

This module provides functionality for backupcsv.

Author: Auto-generated
Date: 2025-11-01
"""

from pathlib import Path
import os
import re
import subprocess
import pandas as pd

def generate_dry_run_csv(directories, csv_path):
    rows = []

    # Regex patterns for exclusions
    excluded_patterns = [
        r"^\..*",  # Hidden files and directories
        r".*/venv/.*",  # venv directories
        r".*/\.venv/.*",  # .venv directories
        r".*/my_global_venv/.*",  # my_global_venv directories
        r".*/simplegallery/.*",
        r".*/avatararts/.*",
        r".*/github/.*",
        r".*/Documents/gitHub/.*",  # Specific gitHub directory
        r".*/\.my_global_venv/.*",  # .my_global_venv directories
        r".*/node/.*",  # Any directory named node
        r".*/Movies/capcut/.*",
        r".*/miniconda3/.*",
        r".*/Movies/movavi/.*",
        r".*/env/.*",  # env directories
        r".*/\.env/.*",  # .env directories
        r".*/Library/.*",  # Library directories
        r".*/\.config/.*",  # .config directories
        r".*/\.spicetify/.*",  # .spicetify directories
        r".*/\.gem/.*",  # .gem directories
        r".*/\.zprofile/.*",  # .zprofile directories
        r"^.*\/\..*",  # Any file or directory starting with a dot
    ]
    def is_excluded(path):
        return any(re.match(pattern, path) for pattern in 
excluded_patterns)

    for directory in directories:
        for root, dirs, files in os.walk(directory):
            for name in dirs + files:
                path = os.path.join(root, name)
                if not is_excluded(path):
                    rows.append({
                        'Type': 'Directory' if os.path.isdir(path) else 
'File',
                        'Path': path
                    })

    df = pd.DataFrame(rows)
    df.to_csv(csv_path, index=False)

# Example usage
directories_to_backup = [
    os.path.expanduser("~/Documents"),
    os.path.expanduser("~/Pictures"),
    os.path.expanduser("~/Music"),
    os.path.expanduser("~/Library/Application Support"),
    os.path.expanduser("~/Library/Preferences"),
    os.path.expanduser("~/Library/Mail"),
]

csv_output_path = Path("/Users/steven/backup_dry_run.csv")

generate_dry_run_csv(directories_to_backup, csv_output_path)

