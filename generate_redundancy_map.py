import os
import ast
import hashlib
import csv
from pathlib import Path
from collections import defaultdict

# Configuration
TARGET_DIR = Path("/Users/steven/pythons")
OUTPUT_CSV = Path("/Users/steven/LOGIC_REDUNDANCY_MAP.csv")

def normalize_code(node):
    """Normalize function source for hashing."""
    try:
        return ast.unparse(node)
    except:
        return None

def generate_redundancy_map():
    print(f"🚀 Generating Logic Redundancy Map for {TARGET_DIR}...")
    
    # logic_hash -> list of {file_name, file_path, func_name}
    function_vault = defaultdict(list)
    total_files = 0

    for root, _, files in os.walk(TARGET_DIR):
        for f in files:
            if f.endswith('.py') and not f.startswith('.'):
                total_files += 1
                file_path = Path(root) / f
                
                try:
                    with open(file_path, 'r', encoding='utf-8', errors='ignore') as source_file:
                        tree = ast.parse(source_file.read())
                        
                    for node in ast.walk(tree):
                        if isinstance(node, ast.FunctionDef):
                            normalized = normalize_code(node)
                            if normalized:
                                logic_hash = hashlib.sha256(normalized.encode()).hexdigest()
                                function_vault[logic_hash].append({
                                    "func_name": node.name,
                                    "file_name": f,
                                    "file_path": str(file_path.relative_to(TARGET_DIR))
                                })
                except:
                    continue
                
                if total_files % 500 == 0:
                    print(f"🔄 Processed {total_files} scripts...")

    # Filter for redundancies (hash appears in > 1 file)
    redundant_map = []
    for logic_hash, occurrences in function_vault.items():
        if len(occurrences) > 1:
            for occ in occurrences:
                redundant_map.append({
                    "Function Name": occ["func_name"],
                    "Occurrence Count": len(occurrences),
                    "File Name": occ["file_name"],
                    "Internal Path": occ["file_path"],
                    "Logic Hash": logic_hash[:16] # Short hash for readability
                })

    # Sort by count (most redundant first)
    redundant_map.sort(key=lambda x: x["Occurrence Count"], reverse=True)

    # Write to CSV
    with open(OUTPUT_CSV, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=["Function Name", "Occurrence Count", "File Name", "Internal Path", "Logic Hash"])
        writer.writeheader()
        writer.writerows(redundant_map)

    print(f"\n✅ Redundancy Map generated!")
    print(f"📊 Total Redundant Rows: {len(redundant_map)}")
    print(f"📁 Saved to: {OUTPUT_CSV}")

if __name__ == "__main__":
    generate_redundancy_map()
