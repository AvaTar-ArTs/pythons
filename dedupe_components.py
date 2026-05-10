import os
import hashlib
from pathlib import Path

# Configuration
TARGET_DIR = Path("/Volumes/2T-Xx/etsy/13_components_raw/")

def get_file_hash(file_path):
    """Calculate SHA-256 hash of a file."""
    sha256_hash = hashlib.sha256()
    with open(file_path, "rb") as f:
        # Read in chunks to handle large files
        for byte_block in iter(lambda: f.read(4096), b""):
            sha256_hash.update(byte_block)
    return sha256_hash.hexdigest()

def deduplicate():
    if not TARGET_DIR.exists():
        print(f"Directory not found: {TARGET_DIR}")
        return

    print(f"🚀 Scanning {TARGET_DIR} for exact duplicates...")
    
    hashes = {} # hash -> list of file paths
    files_processed = 0
    
    for f in TARGET_DIR.glob("*"):
        if f.is_file() and not f.name.startswith('.'):
            file_hash = get_file_hash(f)
            if file_hash in hashes:
                hashes[file_hash].append(f)
            else:
                hashes[file_hash] = [f]
            files_processed += 1

    duplicates_found = 0
    space_saved = 0
    
    print("\n--- DUPLICATE REPORT ---")
    for file_hash, paths in hashes.items():
        if len(paths) > 1:
            # Keep the first one, mark others for deletion
            keep = paths[0]
            dupes = paths[1:]
            
            print(f"KEEP: {keep.name}")
            for d in dupes:
                print(f"  DELETE: {d.name}")
                duplicates_found += 1
                space_saved += d.stat().st_size
                # Safe deletion
                os.remove(d)

    print(f"\n✅ Scan complete.")
    print(f"Files processed: {files_processed}")
    print(f"Duplicates deleted: {duplicates_found}")
    print(f"Space reclaimed: {space_saved / (1024*1024):.2f} MB")

if __name__ == "__main__":
    deduplicate()
