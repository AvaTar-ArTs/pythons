import os
import ast
import hashlib
from pathlib import Path
from collections import defaultdict

# Configuration
TARGET_DIR = Path("/Users/steven/pythons")

def normalize_code(node):
    """Normalize function source by removing comments and standardizing whitespace."""
    try:
        return ast.unparse(node)
    except:
        return None

def find_logic_duplicates():
    print(f"🚀 Starting Deep Logic Audit of {TARGET_DIR}...")
    
    # logic_hash -> list of (file_path, function_name)
    function_vault = defaultdict(list)
    total_files = 0
    total_functions = 0

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
                            total_functions += 1
                            normalized = normalize_code(node)
                            if normalized:
                                # Hash the actual logic
                                logic_hash = hashlib.sha256(normalized.encode()).hexdigest()
                                function_vault[logic_hash].append((file_path.name, node.name))
                except:
                    continue
                
                if total_files % 500 == 0:
                    print(f"🔄 Audited logic in {total_files} scripts...")

    # Identify duplicates
    logic_duplicates = {h: data for h, data in function_vault.items() if len(data) > 1}
    
    print("\n=== LOGIC DUPLICATION REPORT ===")
    print(f"Total Scripts Analyzed: {total_files}")
    print(f"Total Functions Found: {total_functions}")
    print(f"Unique Logic Blocks: {len(function_vault)}")
    print(f"Redundant Logic Blocks: {len(logic_duplicates)}")

    print("\n--- Top 10 Most Copy-Pasted Functions ---")
    # Sort by number of occurrences
    sorted_dupes = sorted(logic_duplicates.items(), key=lambda x: len(x[1]), reverse=True)
    
    for h, data in sorted_dupes[:10]:
        func_name = data[0][1]
        count = len(data)
        print(f"Function: '{func_name}' is duplicated in {count} different files.")
        # Show a few sample filenames
        samples = ", ".join(set([d[0] for d in data[:5]]))
        print(f"  Samples: {samples}")

if __name__ == "__main__":
    find_logic_duplicates()
