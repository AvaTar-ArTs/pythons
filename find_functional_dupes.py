import os
import ast
import hashlib
from pathlib import Path
from collections import defaultdict

# Configuration
TARGET_DIR = Path("/Users/steven/pythons")

def get_logic_signature(file_path):
    """Generates a signature based on the logic of all functions in the file."""
    try:
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            tree = ast.parse(f.read())
        
        # Extract and normalize all function bodies
        function_logics = []
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                function_logics.append(ast.unparse(node))
        
        if not function_logics:
            return None
            
        # Combine and hash
        combined_logic = "".join(sorted(function_logics))
        return hashlib.sha256(combined_logic.encode()).hexdigest()
    except:
        return None

def find_functional_duplicates():
    print(f"🚀 Finding Functionally Identical Files in {TARGET_DIR}...")
    
    # signature -> list of file paths
    signature_map = defaultdict(list)
    total_files = 0

    for root, _, files in os.walk(TARGET_DIR):
        for f in files:
            if f.endswith('.py') and not f.startswith('.'):
                total_files += 1
                file_path = Path(root) / f
                
                sig = get_logic_signature(file_path)
                if sig:
                    signature_map[sig].append(file_path)
                
                if total_files % 500 == 0:
                    print(f"🔄 Processed {total_files} scripts...")

    # Identify duplicates
    functional_dupes = {sig: paths for sig, paths in signature_map.items() if len(paths) > 1}
    
    print("\n=== FUNCTIONAL DUPLICATE REPORT ===")
    print(f"Total Unique Logic Signatures: {len(signature_map)}")
    print(f"Total Sets of Identical Files: {len(functional_dupes)}")
    
    total_redundant = sum(len(p)-1 for p in functional_dupes.values())
    print(f"Total Files that can be safely DELETED: {total_redundant}")

    print("\n--- Top 10 Sets of Identical Files (Different Names, Same Logic) ---")
    count = 0
    for sig, paths in functional_dupes.items():
        if count >= 10: break
        print(f"Set {count+1}: ({len(paths)} files)")
        for p in paths:
            print(f"  - {p.relative_to(TARGET_DIR)}")
        count += 1

if __name__ == "__main__":
    find_functional_duplicates()
