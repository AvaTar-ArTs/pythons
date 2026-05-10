import json
import os

def summarize_tree(tree, depth=0, max_depth=2):
    summary_list = []
    
    if depth > max_depth:
        return summary_list

    rel_path = tree.get("path", ".")
    
    # Simple logic to guess purpose from path for L1 summary
    purpose = "General"
    if "py" in rel_path or "script" in rel_path: purpose = "Logic/Engineering"
    elif "AVATARARTS" in rel_path or "product" in rel_path: purpose = "Commercial/Business"
    elif "Workspace" in rel_path or "AI" in rel_path: purpose = "Research/RAG"
    elif "github" in rel_path or "repo" in rel_path: purpose = "Infrastructure"

    summary_list.append({
        "path": rel_path,
        "depth": depth,
        "purpose": purpose,
        "value": "N/A"
    })

    for child in tree.get("children", []):
        if child.get("type") == "directory":
            summary_list.extend(summarize_tree(child, depth + 1, max_depth))
            
    return summary_list

def count_stats(tree):
    dirs = 0
    files = 0
    types = {}
    
    if tree.get("type") == "directory":
        dirs += 1
        for child in tree.get("children", []):
            d, f, t = count_stats(child)
            dirs += d
            files += f
            for k, v in t.items():
                types[k] = types.get(k, 0) + v
    elif tree.get("type") == "file":
        files += 1
        ext = os.path.splitext(tree.get("name", ""))[1].lower() or "no_ext"
        types[ext] = types.get(ext, 0) + 1
        
    return dirs, files, types

try:
    with open("/Users/steven/scanned_tree_with_excludes.json", "r") as f:
        tree = json.load(f)

    d_total, f_total, t_total = count_stats(tree)
    structure = summarize_tree(tree)

    print(f"DIRS_COUNT: {d_total}")
    print(f"FILES_COUNT: {f_total}")
    print("TYPES_START")
    for ext, count in sorted(t_total.items(), key=lambda x: x[1], reverse=True)[:10]:
        print(f"{ext}:{count}")
    print("TYPES_END")

    print("STRUCT_START")
    # Only print first level directories for the table to keep it readable
    for item in structure:
        if item['depth'] <= 1:
            print(f"{item['path']}|{item['depth']}|{item['purpose']}|{item['value']}")
    print("STRUCT_END")
except Exception as e:
    print(f"ERROR: {e}")