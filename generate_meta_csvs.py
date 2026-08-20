#!/usr/bin/env python3
"""
Generate Fantastic Meta CSVs from your consolidated ecosystem.
Run: python3 ~/generate_meta_csvs.py
"""

import csv
import os
import re
import json
from pathlib import Path
from datetime import datetime
from collections import defaultdict

# ---- CONFIG ----
HOME = Path(os.environ.get("HOME", "/Users/steven"))
OUTPUT_DIR = HOME / "studio" / "meta"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# ---- 1. LOAD EXISTING enriched-Guides.csv (if present) ----
guides_csv = HOME / "Guides" / "enriched-Guides.csv"
guides_data = []
if guides_csv.exists():
    with open(guides_csv, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            guides_data.append(row)
    print(f"📂 Loaded {len(guides_data)} records from enriched-Guides.csv")
else:
    print("⚠️  enriched-Guides.csv not found – skipping knowledge base load.")

# ---- 2. GENERATE: knowledge_base.csv (re‑categorised) ----
def classify_knowledge(row):
    """Re‑classify using the same logic as our reorganise script."""
    fname = row.get("filename", "").lower()
    category = row.get("intelligent_category", "").lower()
    if "marketplace" in fname or "seo" in fname or "etsy" in fname or "gumroad" in fname or "platform" in fname:
        return "research"
    if "deeptutor" in fname or "automation" in fname or "agentic" in fname or "flow" in fname:
        return "development"
    if "index" in fname or "readme" in fname or "manifest" in fname or "checklist" in fname:
        return "reference"
    if ".jpg" in fname or ".png" in fname:
        return "assets"
    if ".jsonl" in fname or "session" in fname or "command" in fname or row.get("file_extension") == ".txt":
        return "logs"
    return "reference"  # fallback

knowledge_rows = []
for row in guides_data:
    new_row = {
        "filename": row.get("filename"),
        "original_path": row.get("original_path"),
        "size_kb": row.get("file_size", "0").replace(" KB", "").strip(),
        "creation_date": row.get("creation_date"),
        "intelligent_category": row.get("intelligent_category", ""),
        "new_category": classify_knowledge(row),
        "business_value": row.get("predicted_business_value", "0.0"),
        "integration_potential": row.get("integration_potential", "False"),
        "agent_affinity": row.get("agent_affinity", ""),
        "skill_affinity": row.get("skill_affinity", ""),
    }
    knowledge_rows.append(new_row)

# ---- 3. GENERATE: tools_inventory.csv (from AVATARARTS, diGiTaLdiVe, scripts) ----
# We build this from known high‑value paths and the audit logs.
tools = []

# Function to safely get file stats
def get_file_meta(path):
    if not path.exists():
        return None
    try:
        stat = path.stat()
        return {
            "size_bytes": stat.st_size,
            "size_kb": round(stat.st_size / 1024, 1),
            "mtime": datetime.fromtimestamp(stat.st_mtime).isoformat(),
        }
    except:
        return None

# High‑value Python scripts from AVATARARTS (from your logs)
avatar_scripts = [
    ("avatararts_automation_suite.py", "AVATARARTS/code/avatararts/"),
    ("avatararts_revenue_automation.py", "AVATARARTS/code/avatararts/"),
    ("ai_art_generator.py", "AVATARARTS/code/avatararts/"),
    ("ai_receptionist.py", "AVATARARTS/code/gptjunkie/"),
    ("heavenly_hands_call_center_agent.py", "AVATARARTS/code/gptjunkie/"),
    ("INTELLIGENT_ENVIRONMENT_ANALYZER.py", "AVATARARTS/code/gptjunkie/"),
    ("autotagger.py", "diGiTaLdiVe/AutoTagger/current/"),
]

for fname, rel_path in avatar_scripts:
    full = HOME / rel_path / fname
    meta = get_file_meta(full)
    tools.append({
        "filename": fname,
        "source_path": str(rel_path),
        "full_path": str(full),
        "type": "python",
        "size_kb": meta["size_kb"] if meta else "0",
        "pii_detected": "Yes" if meta and "/Users/steven" in open(full, errors="ignore").read() else "No",
        "business_score": "0.55" if "automation" in fname or "revenue" in fname else "0.45",
        "category": "automation" if "automation" in fname else "ai" if "ai" in fname or "reception" in fname else "tagger",
    })

# Add n8n workflows (count + metadata)
n8n_dir = HOME / "diGiTaLdiVe" / "n8n_workflows"
if n8n_dir.exists():
    n8n_files = list(n8n_dir.rglob("*.json"))
    tools.append({
        "filename": "n8n_workflow_collection",
        "source_path": "diGiTaLdiVe/n8n_workflows/",
        "full_path": str(n8n_dir),
        "type": "n8n",
        "size_kb": "N/A (40+ files)",
        "pii_detected": "Unknown (check manually)",
        "business_score": "0.70",
        "category": "automation",
    })

# ---- 4. GENERATE: skills_registry.csv (merged from .agents + my-supremepowers) ----
skill_sources = [
    HOME / "my-supremepowers" / "skills",
    HOME / ".agents" / "skills",
]
skills = []
seen = set()
for src in skill_sources:
    if not src.exists():
        continue
    for md in src.rglob("*.md"):
        if md.name in seen:
            continue
        seen.add(md.name)
        # Detect tier from path or content
        tier = "Tier-0" if "supremepowers" in str(md) else "Tier-1"
        # Read first 10 lines for description
        desc = ""
        try:
            with open(md, "r", errors="ignore") as f:
                lines = f.readlines()[:10]
                for line in lines:
                    if line.startswith("description:") or line.startswith("desc:"):
                        desc = line.strip()
                        break
        except:
            pass
        skills.append({
            "skill_name": md.stem,
            "source_path": str(md.parent.relative_to(HOME)),
            "filename": md.name,
            "tier": tier,
            "description_preview": desc[:80] if desc else "N/A",
            "agent_affinity": "system-architect" if "architect" in str(md) else "studio-coach",
        })

# ---- 5. GENERATE: products_manifest.csv (from Claude-Products and instant-revenue) ----
products = []
prod_base = HOME / "Guides" / "instant-revenue" / "Claude-Products"
if prod_base.exists():
    for f in prod_base.glob("*.zip"):
        products.append({
            "product_name": f.stem,
            "type": "zip",
            "path": str(f.relative_to(HOME)),
            "size_kb": round(f.stat().st_size / 1024, 1),
            "status": "Ready" if "v1.1" in f.name else "Needs Review",
            "estimated_price_usd": "47" if "avatararts" in f.name else "27",
        })
    for f in prod_base.glob("GUMROAD_*.md"):
        products.append({
            "product_name": f.stem.replace("GUMROAD_", ""),
            "type": "gumroad_listing",
            "path": str(f.relative_to(HOME)),
            "size_kb": round(f.stat().st_size / 1024, 1),
            "status": "Copy Ready",
            "estimated_price_usd": "17" if "fabric" in f.name else "37",
        })

# ---- 6. GENERATE: pii_cleanup_tracker.csv ----
# We infer PII from the enriched CSV (where pii_files was mentioned)
pii_list = []
for row in guides_data:
    # In the old CSV, pii_files was a separate column? We'll simulate based on path.
    path = row.get("original_path", "")
    if "/Users/steven" in path:
        pii_list.append({
            "file": row.get("filename", "unknown"),
            "full_path": path,
            "pii_type": "hardcoded_path",
            "status": "pending",
            "action": "sed -i '' 's|/Users/steven|$HOME|g'",
        })

# Also add the avatar scripts (if we detected PII above)
for t in tools:
    if t.get("pii_detected") == "Yes":
        pii_list.append({
            "file": t["filename"],
            "full_path": t["full_path"],
            "pii_type": "hardcoded_path",
            "status": "pending",
            "action": "sed -i '' 's|/Users/steven|$HOME|g'",
        })

# ---- 7. GENERATE: duplicate_report.csv (from enriched CSV) ----
dup_map = defaultdict(list)
for row in guides_data:
    fname = row.get("filename", "")
    size = row.get("file_size", "")
    if size and fname:
        dup_map[(fname, size)].append(row.get("original_path", ""))

duplicates = []
for (fname, size), paths in dup_map.items():
    if len(paths) > 1:
        duplicates.append({
            "filename": fname,
            "size": size,
            "occurrences": len(paths),
            "paths": " | ".join(paths),
        })

# ---- WRITE ALL CSVS ----
print("📝 Writing Meta CSVs...")

with open(OUTPUT_DIR / "knowledge_base.csv", "w", newline="", encoding="utf-8") as f:
    if knowledge_rows:
        writer = csv.DictWriter(f, fieldnames=knowledge_rows[0].keys())
        writer.writeheader()
        writer.writerows(knowledge_rows)
        print(f"  ✅ knowledge_base.csv ({len(knowledge_rows)} rows)")

with open(OUTPUT_DIR / "tools_inventory.csv", "w", newline="", encoding="utf-8") as f:
    if tools:
        writer = csv.DictWriter(f, fieldnames=tools[0].keys())
        writer.writeheader()
        writer.writerows(tools)
        print(f"  ✅ tools_inventory.csv ({len(tools)} rows)")

with open(OUTPUT_DIR / "skills_registry.csv", "w", newline="", encoding="utf-8") as f:
    if skills:
        writer = csv.DictWriter(f, fieldnames=skills[0].keys())
        writer.writeheader()
        writer.writerows(skills)
        print(f"  ✅ skills_registry.csv ({len(skills)} rows)")

with open(OUTPUT_DIR / "products_manifest.csv", "w", newline="", encoding="utf-8") as f:
    if products:
        writer = csv.DictWriter(f, fieldnames=products[0].keys())
        writer.writeheader()
        writer.writerows(products)
        print(f"  ✅ products_manifest.csv ({len(products)} rows)")

with open(OUTPUT_DIR / "pii_cleanup_tracker.csv", "w", newline="", encoding="utf-8") as f:
    if pii_list:
        writer = csv.DictWriter(f, fieldnames=pii_list[0].keys())
        writer.writeheader()
        writer.writerows(pii_list)
        print(f"  ✅ pii_cleanup_tracker.csv ({len(pii_list)} rows)")

with open(OUTPUT_DIR / "duplicate_report.csv", "w", newline="", encoding="utf-8") as f:
    if duplicates:
        writer = csv.DictWriter(f, fieldnames=duplicates[0].keys())
        writer.writeheader()
        writer.writerows(duplicates)
        print(f"  ✅ duplicate_report.csv ({len(duplicates)} rows)")

print(f"\n🎉 All CSVs written to: {OUTPUT_DIR}")
print("📂 You can now open these in any spreadsheet app or load into a database.")