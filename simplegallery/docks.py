# docs.py
import csv
import os
import re
from datetime import datetime

# === CONFIGURATION ===
BASE_DIRECTORIES = [
    "/Users/steven/Documents/Python_backup",
    "/Users/steven/Documents/Python",
    "/Users/steven/Music/nocTurneMeLoDieS/lyrics-keys-indo",
    "/Users/steven/Music/nocTurneMeLoDieS/mp3-analyze-transcribe",
]

# === EXCLUDED PATTERNS (regex) ===
EXCLUDED_PATTERNS = [
    r"\/.?venv\/",
    r"\/lib\/",
    r"\/my_global_venv\/",
    r"\/simplegallery\/",
    r"\/avatararts\/",
    r"\/github\/",
    r"\/node\/",
    r"\/miniconda3\/",
    r"\/env\/",
    r"\/Library\/",
    r"\/\.config\/",
    r"\/\.spicetify\/",
    r"\/\.gem\/",
    r"\/\.zprofile\/",
    r"\/\..*",  # Hidden files/directories
]

# === FILE TYPES ===
FILE_CATEGORIES = {
    ".pdf": "Documents",
    ".csv": "Documents",
    ".html": "Documents",
    ".css": "Documents",
    ".js": "Documents",
    ".json": "Documents",
    ".sh": "Documents",
    ".md": "Documents",
    ".txt": "Documents",
    ".doc": "Documents",
    ".docx": "Documents",
    ".ppt": "Documents",
    ".pptx": "Documents",
    ".xlsx": "Documents",
    ".py": "Python Scripts",
    ".xml": "Documents",
}


# === HELPERS ===
def is_excluded(path):
    """Check if a path matches any excluded pattern."""
    for pattern in EXCLUDED_PATTERNS:
        if re.search(pattern, path):
            return True
    return False


def get_category(filename):
    """Determine the category of a file based on its extension."""
    ext = os.path.splitext(filename)[1].lower()
    return FILE_CATEGORIES.get(ext, "Other")


def scan_directory(base_dir):
    """Scan the directory for files and categorize them."""
    results = []
    for root, _, files in os.walk(base_dir):
        if is_excluded(root):
            continue
        for file in files:
            full_path = os.path.join(root, file)
            if is_excluded(full_path):
                continue
            category = get_category(file)
            size_kb = os.path.getsize(full_path) // 1024
            modified = datetime.fromtimestamp(os.path.getmtime(full_path)).strftime(
                "%Y-%m-%d %H:%M:%S"
            )
            results.append([file, full_path, category, size_kb, modified])
    return results


def save_to_csv(file_path, rows):
    """Save a list of rows to a CSV file."""
    with open(file_path, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["Filename", "Path", "Category", "Size (KB)", "Last Modified"])
        writer.writerows(rows)


# === MAIN ===
all_results = []
for base_dir in BASE_DIRECTORIES:
    print(f"🔍 Scanning: {base_dir}")
    results = scan_directory(base_dir)
    all_results.extend(results)
    csv_path = os.path.join(
        base_dir, f"scan_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
    )
    save_to_csv(csv_path, results)
    print(f"📄 Saved CSV for {base_dir} → {csv_path}")

# Save combined CSV
total_csv_path = (
    f"/Users/steven/Documents/Python/scan_TOTAL_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
)
save_to_csv(total_csv_path, all_results)
print(f"✅ Total summary CSV saved → {total_csv_path}")
