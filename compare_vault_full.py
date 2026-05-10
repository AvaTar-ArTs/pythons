import os
from pathlib import Path

FOLDERS = ["Documents", "Music", "Movies", "Downloads"]
LOCAL_BASE = Path("/Users/steven")
REMOTE_BASE = Path("/Volumes/2T-Xx/steven")

def get_dir_inventory(base_path):
    inventory = {} # (size, name) -> path
    if not base_path.exists():
        return inventory
    
    for root, _, files in os.walk(base_path):
        for f in files:
            if f.startswith('.'): continue
            p = Path(root) / f
            try:
                # Store by (size, name) for fast lookup
                stat = p.stat()
                key = (stat.st_size, f)
                inventory[key] = p
            except: continue
    return inventory

def compare_all():
    print(f"{'Folder':<15} | {'Local Size':<10} | {'Vault Size':<10} | {'Overlap (GB)':<12} | {'Uniqueness'}")
    print("-" * 75)
    
    for folder in FOLDERS:
        local_dir = LOCAL_BASE / folder
        remote_dir = REMOTE_BASE / folder
        
        # Get sizes
        def get_size(p):
            return sum(f.stat().st_size for f in p.rglob('*') if f.is_file()) if p.exists() else 0
        
        l_size = get_size(local_dir)
        r_size = get_size(remote_dir)
        
        # Inventory remote
        remote_inv = get_dir_inventory(remote_dir)
        
        # Check matches in local
        match_size = 0
        if local_dir.exists():
            for root, _, files in os.walk(local_dir):
                for f in files:
                    p = Path(root) / f
                    try:
                        key = (p.stat().st_size, f)
                        if key in remote_inv:
                            match_size += p.stat().st_size
                    except: continue
        
        overlap_gb = match_size / (1024**3)
        unique_remote_gb = (r_size - match_size) / (1024**3)
        
        print(f"{folder:<15} | {l_size/(1024**3):>8.1f}GB | {r_size/(1024**3):>8.1f}GB | {overlap_gb:>10.2f}GB | {unique_remote_gb:>8.2f}GB Unique in Vault")

if __name__ == "__main__":
    compare_all()
