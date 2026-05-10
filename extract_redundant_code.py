import os
import ast
from pathlib import Path
from collections import defaultdict

# Configuration
TARGET_DIR = Path("/Users/steven/pythons")

def get_source_of_function(file_path, target_func_name, target_hash):
    try:
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
            tree = ast.parse(content)
            for node in ast.walk(tree):
                if isinstance(node, ast.FunctionDef) and node.name == target_func_name:
                    # Check if hash matches
                    import hashlib
                    normalized = ast.unparse(node)
                    logic_hash = hashlib.sha256(normalized.encode()).hexdigest()[:16]
                    if logic_hash == target_hash:
                        return ast.unparse(node)
    except:
        return None
    return None

def extract_top_logic():
    # Load the top hashes from the map we just built
    # (Manually hardcoding the top discovered hashes for speed in this one-off audit)
    top_targets = [
        ("load_env_d", "293312509f91c606", 124),
        ("save_last_directory", "06cb26cb26cb26cb", 28), # Approximate hash for lookup
        ("get_unique_file_path", "a1b2c3d4e5f6g7h8", 24),
        ("fetch_video_details", "f1e2d3c4b5a69087", 15)
    ]
    
    # Actually, I'll just find the first instance of each top redundant function in the CSV
    # and pull its code.
    
    print("🚀 Extracting code content for top redundant functions...")
    
    # Dictionary to store found logic
    # function_name -> code
    logic_samples = {}
    
    # We'll walk the CSV directly or just search the filesystem
    import csv
    csv_path = Path("/Users/steven/LOGIC_REDUNDANCY_MAP.csv")
    
    if not csv_path.exists():
        print("CSV not found.")
        return

    with open(csv_path, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            name = row['Function Name']
            l_hash = row['Logic Hash']
            path = TARGET_DIR / row['Internal Path']
            
            if l_hash not in logic_samples:
                code = get_source_of_function(path, name, l_hash)
                if code:
                    logic_samples[l_hash] = (name, code, row['Occurrence Count'])
            
            if len(logic_samples) >= 10:
                break

    for l_hash, (name, code, count) in logic_samples.items():
        print(f"\n{'='*60}")
        print(f"FUNCTION: {name} (Used in {count} files)")
        print(f"HASH: {l_hash}")
        print(f"{'-'*60}")
        print(code)
        print(f"{'='*60}\n")

if __name__ == "__main__":
    extract_top_logic()
