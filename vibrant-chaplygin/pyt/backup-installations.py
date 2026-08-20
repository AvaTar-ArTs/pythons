import subprocess
import csv
import os

import logging

logger = logging.getLogger(__name__)


def run_command(command):
    """run_command function."""

    try:
        result = subprocess.check_output(command, shell=True, universal_newlines=True)
        return result.strip().split("\n")
    except subprocess.CalledProcessError as e:
        return [str(e)]


# Define the commands to gather information
commands = {
    "Python Installations": [
        "ls /usr/local/bin/python*",
        "ls /usr/bin/python*",
        "ls /Library/Frameworks/Python.framework/Versions/",
    ],
    "pip Installations": ["pip list", "pip3 list"],
    "Homebrew Installations": ["brew list"],
    "Poetry Installations": ["poetry show"],
    "Conda Environments and Packages": ["conda env list", "conda list"],
}

# Collect the data
data = {}
for category, cmds in commands.items():
    data[category] = []
    for cmd in cmds:
        result = run_command(cmd)
        data[category].extend(result)

# Write data to CSV
output_file = "installations_backup.csv"
with open(output_file, mode="w", newline="") as file:
    writer = csv.writer(file)
    writer.writerow(["Category", "Installation"])
    for category, installations in data.items():
        for installation in installations:
            writer.writerow([category, installation])

logger.info(f"Backup of installations written to {output_file}")
