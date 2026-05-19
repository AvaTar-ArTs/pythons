import os
import hashlib
from pathlib import Path

# Configuration: Target Pillars on 2T-Xx
BASE_DIR = Path("/Volumes/2T-Xx/etsy")
PILLARS = ["halloween_designs", "animal_designs", "holiday_designs"]

def get_file_hash(file_path):
    """Calculate SHA-256 hash of a file."""
    sha256_hash = hashlib.sha256()
    try:
        with open(file_path, "rb") as f:
            for byte_block in iter(lambda: f.read(4096), b""):
                sha256_hash.update(byte_block)
        return sha256_hash.hexdigest()
    except Exception as e:
        return None

def compare_and_dedupe():
    hashes = {} # hash -> list of absolute paths
    files_scanned = 0
    
    print("🚀 Starting Deep Content Comparison across pillars...")
    
    for pillar in PILLARS:
        pillar_path = BASE_DIR / pillar
        if not pillar_path.exists():
            print(f"⚠️ Pillar not found: {pillar}")
            continue
            
        print(f"Scanning {pillar}...")
        for root, _, files in os.walk(pillar_path):
            for f in files:
                if f.startswith('.') or f.endswith('.txt') or f.endswith('.md'):
                    continue
                
                file_path = Path(root) / f
                if not file_path.is_file():
                    continue
                    
                file_hash = get_file_hash(file_path)
                if file_hash:
                    if file_hash in hashes:
                        hashes[file_hash].append(file_path)
                    else:
                        hashes[file_hash] = [file_path]
                    files_scanned += 1

    duplicates_found = 0
    space_saved = 0
    
    print("\n--- DUPLICATE CONTENT REPORT ---")
    for file_hash, paths in hashes.items():
        if len(paths) > 1:
            # Keep the one with the "shortest" name (least amount of 300dpi prefixes)
            paths.sort(key=lambda x: len(x.name))
            keep = paths[0]
            dupes = paths[1:]
            
            print(f"KEEPING: {keep.name} (Size: {keep.stat().st_size / 1024 / 1024:.2f} MB)")
            for d in dupes:
                print(f"  DUPLICATE FOUND: {d.name}")
                duplicates_found += 1
                space_saved += d.stat().st_size
                # Safe deletion
                try:
                    os.remove(d)
                except Exception as e:
                    print(f"  ❌ Error deleting {d.name}: {e}")

    print(f"\n✅ Content Comparison Complete.")
    print(f"Total Files Scanned: {files_scanned}")
    print(f"Duplicates Removed: {duplicates_found}")
    print(f"Space Reclaimed: {space_saved / (1024*1024):.2f} MB")

if __name__ == "__main__":
    compare_and_dedupe()
