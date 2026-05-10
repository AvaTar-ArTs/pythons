import os
from datetime import datetime
import re

def summarize_chaos_manifest(file_path):
    total_entries = 0
    file_stats = []  # (size, timestamp, path)
    extension_counts = {}

    with open(file_path, 'r') as f:
        for line in f:
            total_entries += 1
            # Expected format: "path size timestamp"
            parts = line.strip().split()
            if len(parts) >= 3:
                path = parts[0]
                try:
                    size = int(parts[1])
                    timestamp = datetime.fromtimestamp(int(parts[2]))
                except ValueError:
                    # Skip lines that don't conform to expected size/timestamp format
                    continue
                
                file_stats.append((size, timestamp, path))
                
                # Extract extension
                if os.path.isfile(path):
                    ext = os.path.splitext(path)[1].lower()
                    extension_counts[ext] = extension_counts.get(ext, 0) + 1
            elif len(parts) == 1 and os.path.isdir(parts[0]):
                # Handle directories, they don't have size/timestamp from this stat command
                pass
            
    # Sort by size for largest files
    file_stats.sort(key=lambda x: x[0], reverse=True)
    top_5_largest = file_stats[:5]

    # Sort by timestamp for oldest/newest files
    file_stats.sort(key=lambda x: x[1])
    oldest_5 = file_stats[:5]
    newest_5 = file_stats[-5:]

    # Sort extensions by count
    top_10_extensions = sorted(extension_counts.items(), key=lambda x: x[1], reverse=True)[:10]

    return {
        "total_entries": total_entries,
        "top_5_largest": top_5_largest,
        "oldest_5_files": oldest_5,
        "newest_5_files": newest_5,
        "top_10_extensions": top_10_extensions
    }

if __name__ == "__main__":
    manifest_file = os.path.expanduser("~/pythons_chaos_manifest.txt")
    summary = summarize_chaos_manifest(manifest_file)

    print(f"Total entries (files/directories): {summary['total_entries']}")

    print("\nTop 5 Largest Files:")
    for size, _, path in summary['top_5_largest']:
        print(f"  {path} ({size} bytes)")

    print("\nOldest 5 Files:")
    for _, timestamp, path in summary['oldest_5_files']:
        print(f"  {path} (Modified: {timestamp})")

    print("\nNewest 5 Files:")
    for _, timestamp, path in summary['newest_5_files']:
        print(f"  {path} (Modified: {timestamp})")

    print("\nTop 10 Most Common Extensions:")
    for ext, count in summary['top_10_extensions']:
        print(f"  {ext}: {count} files")