import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
#!/usr/bin/env python3
"""
Convert scattered_python_files_scan.json to CSV
"""

import json
import csv
from pathlib import Path
import sys

def json_to_csv(json_file, csv_file):
    """Convert JSON scan results to CSV"""

    # Read JSON
    with open(json_file, 'r') as f:
        data = json.load(f)

    # Extract files
    files = data.get('files', [])

    if not files:
        print("❌ No files found in JSON")
        return

    # Write CSV
    fieldnames = [
        'path',
        'relative_path',
        'directory',
        'filename',
        'extension',
        'size',
        'size_kb',
        'size_mb'
    ]

    with open(csv_file, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()

        for file_info in files:
            size = file_info.get('size', 0)
            row = {
                'path': file_info.get('path', ''),
                'relative_path': file_info.get('relative_path', ''),
                'directory': file_info.get('directory', ''),
                'filename': Path(file_info.get('relative_path', '')).name,
                'extension': file_info.get('extension', ''),
                'size': size,
                'size_kb': f"{size/1024:.2f}" if size > 0 else "0",
                'size_mb': f"{size/(1024*1024):.2f}" if size > 1024*1024 else "0"
            }
            writer.writerow(row)

    print(f"✅ Converted {len(files)} files to CSV")
    print(f"📄 Output: {csv_file}")

try:
        json_file = Path.home() / "scattered_python_files_scan.json"
        csv_file = Path.home() / "scattered_python_files_scan.csv"
        if len(sys.argv) > 1:
            json_file = Path(sys.argv[1])
        if len(sys.argv) > 2:
            csv_file = Path(sys.argv[2])
        if not json_file.exists():
            print(f"❌ JSON file not found: {json_file}")
            sys.exit(1)
        json_to_csv(json_file, csv_file)
except KeyboardInterrupt:
    logger.info("Execution interrupted by user")
    sys.exit(1)
except Exception as e:
    logger.error(f"An error occurred: {e}", exc_info=True)
    sys.exit(1)