import ast
import csv
import os
import hashlib
from collections import defaultdict

def get_script_dna(filepath):
    """Extracts the structural DNA of a script: functions, classes, and imports."""
    try:
        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
        
        tree = ast.parse(content)
        
        functions = []
        classes = []
        imports = []
        
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                functions.append(node.name)
            elif isinstance(node, ast.ClassDef):
                classes.append(node.name)
            elif isinstance(node, ast.Import):
                for alias in node.names:
                    imports.append(alias.name)
            elif isinstance(node, ast.ImportFrom):
                imports.append(node.module or '')

        # Create a unique signature based on sorted structures
        # This identifies scripts with the same 'abilities' even if variables/comments differ
        dna_parts = [
            "f:" + ",".join(sorted(set(functions))),
            "c:" + ",".join(sorted(set(classes))),
            "i:" + ",".join(sorted(set(imports)))
        ]
        dna_string = "|".join(dna_parts)
        return hashlib.sha256(dna_string.encode()).hexdigest(), dna_string
    except Exception:
        return None, None

input_file = 'real_python_scripts.csv'
output_file = 'structural_dedupe_report.csv'

clusters = defaultdict(list)
dna_details = {}

print("🧬 Analyzing script structure (this may take a minute)...")

if not os.path.exists(input_file):
    print(f"Error: {input_file} not found.")
    exit(1)

count = 0
with open(input_file, 'r') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        path = row['Path']
        if not os.path.exists(path):
            continue
            
        dna_hash, dna_string = get_script_dna(path)
        if dna_hash:
            clusters[dna_hash].append(path)
            dna_details[dna_hash] = dna_string
            count += 1
            if count % 500 == 0:
                print(f"   Processed {count} scripts...")

# Write the structural dedupe report
with open(output_file, 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['DNA_Hash', 'Occurrences', 'Paths', 'Abilities_Summary'])
    
    for dna_hash, paths in clusters.items():
        summary = dna_details[dna_hash]
        writer.writerow([
            dna_hash,
            len(paths),
            "; ".join(paths),
            summary[:200] + ("..." if len(summary) > 200 else "")
        ])

print(f"✅ Structural analysis complete. Found {len(clusters)} unique 'Ability' signatures across {count} scripts.")
print(f"Saved report to {output_file}")
