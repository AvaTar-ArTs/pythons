#!/usr/bin/env python3
"""
Comprehensive System Scanner for AvatarArts
Scans all directories recursively and creates detailed reports
"""

import csv
import hashlib
import json
import os
import sys
from collections import defaultdict
from datetime import datetime
from pathlib import Path


def calculate_file_hash(filepath):
    """Calculate SHA256 hash of file content"""
    try:
        hash_sha256 = hashlib.sha256()
        with open(filepath, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hash_sha256.update(chunk)
        return hash_sha256.hexdigest()
    except Exception:
        return None


def scan_all_directories(root_path, output_csv="results.csv"):
    """Scan all directories recursively and create detailed report"""
    print(f"🔍 Starting comprehensive scan of: {root_path}")

    results = []
    stats = {"total_files": 0, "total_size": 0, "file_types": defaultdict(int), "directories": 0}

    for root, dirs, files in os.walk(root_path):
        # Count directories
        stats["directories"] += len(dirs)

        for file in files:
            filepath = os.path.join(root, file)
            try:
                # Get file stats
                file_stat = os.stat(filepath)
                file_size = file_stat.st_size
                file_ext = Path(file).suffix.lower()

                # Calculate hash
                file_hash = calculate_file_hash(filepath)

                # Record file information
                results.append(
                    {
                        "path": filepath,
                        "filename": file,
                        "extension": file_ext,
                        "size_bytes": file_size,
                        "size_mb": round(file_size / (1024 * 1024), 2),
                        "modified": datetime.fromtimestamp(file_stat.st_mtime).isoformat(),
                        "directory": root,
                        "hash": file_hash,
                    }
                )

                # Update statistics
                stats["total_files"] += 1
                stats["total_size"] += file_size
                stats["file_types"][file_ext] += 1

                # Progress update
                if stats["total_files"] % 1000 == 0:
                    print(f"📊 Processed {stats['total_files']} files...")

            except Exception as e:
                print(f"⚠️  Error processing {filepath}: {e}")
                continue

    # Write results to CSV
    with open(output_csv, "w", newline="", encoding="utf-8") as csvfile:
        fieldnames = ["path", "filename", "extension", "size_bytes", "size_mb", "modified", "directory", "hash"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        for result in results:
            writer.writerow(result)

    # Write summary statistics
    summary_path = output_csv.replace(".csv", "_summary.json")
    summary = {
        "scan_timestamp": datetime.now().isoformat(),
        "root_path": root_path,
        "statistics": dict(stats),
        "output_file": output_csv,
    }

    with open(summary_path, "w") as f:
        json.dump(summary, f, indent=2)

    print("✅ Scan completed!")
    print(f"📁 Total files scanned: {stats['total_files']}")
    print(f"💽 Total size: {round(stats['total_size'] / (1024 * 1024 * 1024), 2)} GB")
    print(f"📂 Total directories: {stats['directories']}")
    print(f"📄 Results saved to: {output_csv}")
    print(f"📋 Summary saved to: {summary_path}")

    return results


if __name__ == "__main__":
    if len(sys.argv) > 1:
        root_path = sys.argv[1]
    else:
        root_path = os.path.expanduser("~")

    output_file = "results.csv" if len(sys.argv) <= 2 else sys.argv[2]

    scan_all_directories(root_path, output_file)
