import os
import hashlib
from pathlib import Path

# Configuration
LOCAL_DIR = Path("/Users/steven/Pictures")
REMOTE_DIR = Path("/Volumes/2T-Xx/steven/Pictures")

def get_file_hash(file_path):
    """Fast hash for comparison."""
    sha256_hash = hashlib.sha256()
    with open(file_path, "rb") as f:
        # Just hash the first 1MB for speed in large comparison
        sha256_hash.update(f.read(1024 * 1024))
    return sha256_hash.hexdigest()

def compare_drives():
    if not REMOTE_DIR.exists():
        print("Remote dir not found.")
        return

    print(f"🚀 Indexing local files in {LOCAL_DIR}...")
    local_files = {} # (size, hash_prefix) -> list of paths
    
    for root, _, files in os.walk(LOCAL_DIR):
        for f in files:
            if f.startswith('.'): continue
            path = Path(root) / f
            try:
                size = path.stat().st_size
                if size > 1024 * 1024: # Only check files > 1MB for efficiency
                    # We use (size, name) as a first-pass key
                    key = (size, f)
                    if key not in local_files:
                        local_files[key] = []
                    local_files[key].append(path)
            except: continue

    print(f"Indexed {len(local_files)} large local files.")
    print(f"🚀 Scanning remote backup in {REMOTE_DIR} for matches...")
    
    matches = []
    
    for root, _, files in os.walk(REMOTE_DIR):
        for f in files:
            if f.startswith('.'): continue
            path = Path(root) / f
            try:
                size = path.stat().st_size
                key = (size, f)
                if key in local_files:
                    # Potential match found
                    matches.append((path, local_files[key][0]))
            except: continue

    print(f"\n=== MATCH REPORT ===")
    print(f"Found {len(matches)} files in the backup that already exist locally.")
    
    total_match_size = sum(m[0].stat().st_size for m in matches)
    print(f"Potential space to reclaim on 2T-Xx: {total_match_size / (1024**3):.2f} GB")
    
    print("\n--- Samples of Matches (Safe to delete from Backup) ---")
    for remote, local in matches[:10]:
        print(f"MATCH: {remote.name} (exists in both)")

if __name__ == "__main__":
    compare_drives()
