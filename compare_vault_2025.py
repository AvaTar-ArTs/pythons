#!/usr/bin/env python3
"""Compare HISTORICAL_VAULT_2025 with local home folders. Report overlap by (size, filename)."""
import os
from pathlib import Path

FOLDERS = ["Pictures", "Documents", "Music", "Movies", "Downloads"]
LOCAL_BASE = Path("/Users/steven")
VAULT_BASE = Path("/Volumes/2T-Xx/HISTORICAL_VAULT_2025")

def get_inventory(path, max_files=None):
    """Build (size, name) -> count inventory. Optional max_files to limit work."""
    inv = {}
    n = 0
    if not path.exists():
        return inv
    for root, _, files in os.walk(path):
        for f in files:
            if f.startswith("."):
                continue
            p = Path(root) / f
            try:
                key = (p.stat().st_size, f)
                inv[key] = inv.get(key, 0) + 1
                n += 1
                if max_files and n >= max_files:
                    return inv
            except OSError:
                continue
    return inv

def compare_folder(folder):
    local_dir = LOCAL_BASE / folder
    vault_dir = VAULT_BASE / folder
    if not vault_dir.exists():
        return None
    vault_inv = get_inventory(vault_dir)
    local_inv = get_inventory(local_dir)
    matches = 0
    match_size = 0
    for key in local_inv:
        if key in vault_inv:
            matches += 1
            match_size += key[0]
    vault_files = sum(vault_inv.values())
    return {
        "folder": folder,
        "vault_files": vault_files,
        "local_files": sum(local_inv.values()),
        "matches": matches,
        "match_size_gb": match_size / (1024**3),
    }

def main():
    print("BATCH 1: Vault vs Local comparison (by size+filename)")
    print("Vault:", VAULT_BASE)
    print("Local:", LOCAL_BASE)
    print()
    for folder in FOLDERS:
        r = compare_folder(folder)
        if r is None:
            print(f"{folder}: vault path missing")
            continue
        print(f"{r['folder']:<12} | vault_files={r['vault_files']:<8} | matches={r['matches']:<8} | match_size={r['match_size_gb']:.2f} GB")
    print()
    print("Done.")

if __name__ == "__main__":
    main()
