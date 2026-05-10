import os
import hashlib
from pathlib import Path
from collections import defaultdict

# Configuration
TARGET_DIR = Path("/Users/steven/pythons")

def get_file_hash(file_path):
    """Calculate full SHA-256 hash."""
    sha256_hash = hashlib.sha256()
    try:
        with open(file_path, "rb") as f:
            for byte_block in iter(lambda: f.read(4096), b""):
                sha256_hash.update(byte_block)
        return sha256_hash.hexdigest()
    except:
        return None

def find_duplicates():
    if not TARGET_DIR.exists():
        print(f"Directory not found: {TARGET_DIR}")
        return

    print(f"🚀 Scanning {TARGET_DIR} for duplicates...")
    
    hashes = defaultdict(list)
    files_scanned = 0
    
    for root, _, files in os.walk(TARGET_DIR):
        for f in files:
            if f.endswith('.py') and not f.startswith('.'):
                file_path = Path(root) / f
                file_hash = get_file_hash(file_path)
                if file_hash:
                    hashes[file_hash].append(file_path)
                    files_scanned += 1
                
                if files_scanned % 500 == 0:
                    print(f"🔄 Scanned {files_scanned} scripts...")

    duplicates = {h: paths for h, paths in hashes.items() if len(paths) > 1}
    
    print("\n=== DUPLICATE CODE REPORT ===")
    print(f"Total Unique Scripts: {len(hashes)}")
    print(f"Total Redundant Copies: {sum(len(p)-1 for p in duplicates.values())}")
    
    print("\n--- Samples of Logic Sprawl (Duplicate Files) ---")
    count = 0
    for h, paths in duplicates.items():
        if count >= 15: break
        print(f"Group: {paths[0].name}")
        for p in paths:
            print(f"  - {p.relative_to(TARGET_DIR)}")
        count += 1

if __name__ == "__main__":
    find_duplicates()
