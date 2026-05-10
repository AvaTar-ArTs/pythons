import os
import csv
import re
from pathlib import Path
from datetime import datetime

# Configuration
HOME = Path(os.path.expanduser("~"))
OUTPUT_FILE = HOME / "gemini_context_audit_v2.csv"
TARGET_FILENAME = "GEMINI.md"

def get_file_metadata(path):
    """Extracts system metadata."""
    stat = path.stat()
    return {
        "path": str(path),
        "size_bytes": stat.st_size,
        "last_modified": datetime.fromtimestamp(stat.st_mtime).strftime("%Y-%m-%d %H:%M:%S")
    }

def parse_markdown_intent(path):
    """
    Parses the Markdown content to extract the 'Identity' of the file.
    """
    try:
        with open(path, "r", encoding="utf-8") as f:
            content = f.read()
    except Exception as e:
        return {"title": "Error Reading", "north_star": str(e), "is_universal": False}

    # 1. Extract Title (First H1)
    title_match = re.search(r'^#\s+(.*?)$', content, re.MULTILINE)
    title = title_match.group(1).strip() if title_match else "Untitled Context"

    # 2. Extract "North Star" or "Strategic Directive"
    north_star = "N/A"
    ns_patterns = [
        r'\*\*"?North Star"?\*\*:\s*(.*?)(?:\n|\*)',
        r'##\s+.*?North Star.*?\n(.*?)(?=\n#)',
        r'Core Objective:\s*(.*?)(?:\n|$)',
        r'Purpose:\s*(.*?)(?:\n|$)'
    ]

    for pattern in ns_patterns:
        match = re.search(pattern, content, re.IGNORECASE | re.DOTALL)
        if match:
            north_star = match.group(1).strip()[:150].replace("\n", " ").replace("\r", "")
            break

    # 3. Detect compliance with the new Universal standards
    is_universal = any(x in content for x in ["Universal v2.0", "Functional Hub", "XEO-DEO", "V3.0", "V3.2"])

    return {
        "title": title,
        "north_star": north_star,
        "is_universal": is_universal
    }

def classify_tier(path_str):
    """Determines the organizational tier based on path."""
    p = str(path_str)
    if p == str(HOME / "GEMINI.md"):
        return "TIER 1 (ROOT MASTER)"
    elif ".gemini/extensions" in p:
        return "TIER 3 (EXTENSION)"
    elif ".gemini/" in p:
        return "TIER 2 (SYSTEM MEMORY)"
    elif "Downloads" in p:
        return "LEGACY / ARCHIVE"
    elif "MasterxEo" in p:
        return "RESEARCH / REPO"
    elif "AVATARARTS" in p:
        return "TIER 2 (PRODUCTION HUB)"
    else:
        return "ORPHAN / UNCLASSIFIED"

def audit_system():
    results = []
    print(f"🚀 Starting Context Audit V2...")
    print(f"Scanning {HOME} for {TARGET_FILENAME}...")

    # Walk the filesystem
    for root, dirs, files in os.walk(HOME):
        # Pruning heavy/irrelevant dirs for efficiency
        if any(skip in root for skip in ["Library", ".Trash", "node_modules", ".git", "venv", ".venv"]):
            continue

        if TARGET_FILENAME in files:
            full_path = Path(root) / TARGET_FILENAME
            
            try:
                meta = get_file_metadata(full_path)
                intent = parse_markdown_intent(full_path)
                tier = classify_tier(full_path)
                
                entry = {**meta, **intent, "tier": tier}
                results.append(entry)
                print(f"Found: {tier.ljust(25)} | {full_path.name} at {full_path.parent.name}/")
            except Exception as e:
                print(f"Error processing {full_path}: {e}")

    # Write CSV
    headers = ["tier", "title", "last_modified", "is_universal", "north_star", "path", "size_bytes"]
    
    with open(OUTPUT_FILE, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=headers)
        writer.writeheader()
        writer.writerows(results)

    print(f"\n✅ Audit V2 Complete. Report generated at: {OUTPUT_FILE}")
    print(f"Total Context Files Found: {len(results)}")

if __name__ == "__main__":
    audit_system()