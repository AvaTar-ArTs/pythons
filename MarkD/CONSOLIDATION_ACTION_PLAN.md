# Python Scripts Consolidation Action Plan

## Executive Summary

**Repository Status:**
- 10,655 Python files across 3,634 directories (1.54 GB total)
- 237 actual content duplicates (1.13 MB wasted)
- 2,575 variant files with naming patterns (_1, _2, _v2, etc.)
- 27 .history directories (130 MB of edit history)
- **Consolidation Potential: 131+ MB recovery**

**Timeline:** This week (5-7 days)

---

## Phase 1: Low-Risk Cleanup (Day 1-2) — ~130 MB Savings

### Step 1.1: Remove .history Directories

**Risk Level:** ✅ **ZERO RISK** - These are auto-generated editor backups

```bash
# Find all .history directories
find /Users/steven/pythons -type d -name ".history*" | head -20

# Count total .history files
find /Users/steven/pythons -type d -name ".history*" | wc -l

# Estimate size
du -sh /Users/steven/pythons/*/.history* 2>/dev/null | tail -5

# Strategy: Move to archive first (safe recovery)
mkdir -p /Users/steven/pythons/.archive_history_$(date +%Y%m%d)

# Move .history directories to archive
find /Users/steven/pythons -maxdepth 2 -type d -name ".history*" -exec \
  mv {} /Users/steven/pythons/.archive_history_$(date +%Y%m%d)/ \; 2>/dev/null

# Verify before deletion
du -sh /Users/steven/pythons/.archive_history_*

# After confirming no issues, DELETE archive (or keep for 1 week)
# rm -rf /Users/steven/pythons/.archive_history_*
```

**Expected Recovery:** 130 MB

---

### Step 1.2: Clean Up .venv and Virtual Environments

**Risk Level:** ✅ **LOW RISK** - Can be regenerated from requirements.txt

```bash
# Find virtual environments
find /Users/steven/pythons -name ".venv" -o -name "venv" -o -name "env" | head -10

# Remove them
find /Users/steven/pythons -maxdepth 2 -type d -name ".venv" -o -name "venv" | xargs rm -rf

# Remove any dependency lock files that duplicate info
find /Users/steven/pythons -name "poetry.lock" -o -name "Pipfile.lock" | head -5
```

**Expected Recovery:** 10-50 MB (varies by project)

---

### Step 1.3: Remove Cache Directories

**Risk Level:** ✅ **LOW RISK** - These regenerate automatically

```bash
# Python caches
find /Users/steven/pythons -type d -name "__pycache__" | wc -l
find /Users/steven/pythons -type d -name "__pycache__" | xargs rm -rf

# Ruff cache
rm -rf /Users/steven/pythons/.ruff_cache

# pytest cache
find /Users/steven/pythons -type d -name ".pytest_cache" | xargs rm -rf

# aider cache
rm -rf /Users/steven/pythons/.aider.tags.cache.v4
```

**Expected Recovery:** 5-10 MB

---

## Phase 2: Content Deduplication (Day 2-3) — ~1.13 MB Savings

### Step 2.1: Find Identical File Content

```bash
# Script to find all duplicate files by content
cat > find_duplicates.py << 'EOF'
#!/usr/bin/env python3
import os
import hashlib
from collections import defaultdict
from pathlib import Path

def get_file_hash(filepath):
    """Get SHA256 hash of file content"""
    try:
        with open(filepath, 'rb') as f:
            return hashlib.sha256(f.read()).hexdigest()
    except:
        return None

# Find all Python files
py_files = list(Path('/Users/steven/pythons').rglob('*.py'))
print(f"Found {len(py_files)} Python files")

# Group by hash
hash_map = defaultdict(list)
for f in py_files:
    if '.history' in str(f) or '__pycache__' in str(f):
        continue
    h = get_file_hash(f)
    if h:
        hash_map[h].append(str(f))

# Find duplicates (same content, multiple files)
duplicates = {h: files for h, files in hash_map.items() if len(files) > 1}
print(f"\nFound {len(duplicates)} sets of duplicate content:")

# Sort by file size (largest first)
dup_list = [(Path(files[0]).stat().st_size, files) for files in duplicates.values()]
dup_list.sort(reverse=True)

for size, files in dup_list[:20]:
    print(f"\n{size:,} bytes - {len(files)} copies:")
    for f in sorted(files):
        print(f"  {f}")

# Save report
with open('/Users/steven/pythons/DUPLICATES_REPORT.txt', 'w') as out:
    out.write(f"Duplicate Files Report\n")
    out.write(f"Found {len(duplicates)} sets of duplicate content\n\n")
    for size, files in dup_list:
        out.write(f"\n{size:,} bytes - {len(files)} copies:\n")
        for f in sorted(files):
            out.write(f"  {f}\n")

print(f"\nReport saved to DUPLICATES_REPORT.txt")
EOF

python3 find_duplicates.py
```

**Output:** DUPLICATES_REPORT.txt with all duplicates listed

### Step 2.2: Merge Identified Duplicates

**Example 1: Consolidate resize-img.py duplicates**

```bash
# Before: 3 identical copies
ls -la /Users/steven/pythons/resize-img*.py

# Keep the root version (most accessible)
KEEP="/Users/steven/pythons/resize-img.py"
DELETE=(
  "/Users/steven/pythons/resize-img_1.py"
  "/Users/steven/pythons/documentation/resize-img_1.py"
)

# Verify they're identical
diff /Users/steven/pythons/resize-img.py /Users/steven/pythons/resize-img_1.py

# Delete duplicates
for file in "${DELETE[@]}"; do
  rm "$file"
  echo "Deleted: $file"
done
```

**Example 2: Consolidate enhanced_content_analyzer.py**

```bash
# Find all enhanced_content_analyzer variants
find /Users/steven/pythons -name "*enhanced_content_analyzer*" -type f

# Keep main version, remove others
rm /Users/steven/pythons/AI_CONTENT/content_creation/enhanced_content_analyzer_from_data-analyzer.py
rm /Users/steven/pythons/AI_CONTENT/content_creation/enhanced_content_analyzer_1.py

# Update imports if needed
grep -r "from enhanced_content_analyzer_from_data-analyzer" /Users/steven/pythons/ || echo "No imports found"
```

### Step 2.3: Script to Remove All Content Duplicates

```bash
# Create a safe deletion script
cat > remove_duplicates.sh << 'EOF'
#!/bin/bash

echo "Removing confirmed duplicate files..."

# Duplicates to remove (from DUPLICATES_REPORT.txt analysis)
duplicates=(
  "/Users/steven/pythons/resize-img_1.py"
  "/Users/steven/pythons/transcribe 1.py"
  "/Users/steven/pythons/AI_CONTENT/content_creation/enhanced_content_analyzer_from_data-analyzer.py"
  # Add all identified duplicates here from the report
)

REMOVED=0
for file in "${duplicates[@]}"; do
  if [ -f "$file" ]; then
    mv "$file" "$file.backup"  # Rename first as safety
    echo "Marked for deletion: $file"
    ((REMOVED++))
  fi
done

echo "Marked $REMOVED files for deletion (renamed to .backup)"
echo "Review and then delete with: find /Users/steven/pythons -name '*.backup' -delete"
EOF

chmod +x remove_duplicates.sh
./remove_duplicates.sh
```

**Expected Recovery:** 1.13 MB

---

## Phase 3: Consolidate Variant Files (Day 3-4) — ~0.7 MB Savings

### Step 3.1: Identify Files with Most Variants

```bash
# Find files with multiple versions
python3 << 'EOF'
from pathlib import Path
from collections import defaultdict

# Find all Python files
py_files = list(Path('/Users/steven/pythons').rglob('*.py'))

# Group by basename (removing _N, _v2, etc. suffixes)
import re

base_names = defaultdict(list)
for f in py_files:
    if '.history' in str(f) or '__pycache__' in str(f):
        continue

    # Remove version patterns
    name = f.name
    base = re.sub(r'(_\d+|_v\d+| \d+|\(\d+\)|_test|_backup|_old)\.py', '.py', name)
    base_names[base].append(str(f))

# Find files with 5+ variants
variants = {name: files for name, files in base_names.items() if len(files) >= 5}
print(f"Found {len(variants)} files with 5+ variants\n")

for name in sorted(variants.keys(), key=lambda x: len(variants[x]), reverse=True)[:20]:
    files = variants[name]
    print(f"{name}: {len(files)} variants")
    for f in sorted(files)[:5]:
        print(f"  {f}")
    if len(files) > 5:
        print(f"  ... and {len(files) - 5} more")
    print()
EOF
```

### Step 3.2: Archive Old Timestamp Versions

```bash
# Find timestamp-versioned files (e.g., batch_upscaler_v2_20251201*.py)
find /Users/steven/pythons -type f -name "*_202512*" -o -name "*_202511*" | head -20

# Create archive
mkdir -p /Users/steven/pythons/.archive_timestamp_variants_$(date +%Y%m%d)

# Move old versions (keep only most recent)
# For each file, keep the one with the latest timestamp
python3 << 'EOF'
from pathlib import Path
from collections import defaultdict
import re

archive_dir = Path('/Users/steven/pythons/.archive_timestamp_variants')

# Find timestamp files
timestamp_files = list(Path('/Users/steven/pythons').rglob('*_202[45]*.py'))

# Group by base name and move older versions
grouped = defaultdict(list)
for f in timestamp_files:
    match = re.search(r'_(\d{8}_\d{6})', f.name)
    if match:
        timestamp = match.group(1)
        base = f.name.split('_')[0]
        grouped[base].append((timestamp, f))

# Keep latest, archive older
for base, files in grouped.items():
    if len(files) > 1:
        files.sort(reverse=True)  # Latest first
        for timestamp, old_file in files[1:]:  # Skip the latest
            archive_dir.mkdir(exist_ok=True)
            new_path = archive_dir / old_file.name
            print(f"Moving: {old_file} → {new_path}")
            # Uncomment to actually move:
            # old_file.rename(new_path)
EOF
```

### Step 3.3: Rename Conflicting Filenames

```bash
# Files that appear in 10+ directories with same name should be renamed

# Create renaming script
cat > rename_conflicts.sh << 'EOF'
#!/bin/bash

# These files have the same name in multiple directories
# Need to rename for clarity

RENAMES=(
  # [original]=[new_name]
  "analyze.py:content_analyzer.py"
  "base.py:base_bot.py"
  "process.py:audio_processor.py"
  "upload.py:content_upload.py"
)

for rename in "${RENAMES[@]}"; do
  IFS=':' read -r original new <<< "$rename"

  echo "Would rename: $original → $new"

  # Find and rename in each directory
  find /Users/steven/pythons -maxdepth 3 -name "$original" -type f | while read -r file; do
    dir=$(dirname "$file")
    newfile="$dir/$new"

    # Check if we should rename this one
    # (only if there's clear context about what it does)
    if grep -q "class.*Bot" "$file" 2>/dev/null; then
      echo "  Renaming: $file → $newfile"
      # mv "$file" "$newfile"
    fi
  done
done
EOF

chmod +x rename_conflicts.sh
# Review first before running: ./rename_conflicts.sh
```

---

## Phase 4: Create Shared Modules Structure (Day 4-5) — Better Organization

### Step 4.1: Create shared_modules Directory

```bash
mkdir -p /Users/steven/pythons/shared_modules/{utils,config,helpers,api_clients}

cat > /Users/steven/pythons/shared_modules/__init__.py << 'EOF'
"""Shared modules for common functionality"""
from . import utils
from . import config
from . import helpers

__all__ = ['utils', 'config', 'helpers']
EOF
```

### Step 4.2: Consolidate Common Utilities

```bash
# Create consolidated utils module by examining existing utils files
python3 << 'EOF'
from pathlib import Path
import ast

# Find all utils.py files
utils_files = list(Path('/Users/steven/pythons').rglob('utils.py'))
print(f"Found {len(utils_files)} utils.py files:\n")

# Analyze what each contains
for uf in sorted(utils_files)[:10]:
    try:
        with open(uf) as f:
            tree = ast.parse(f.read())

        functions = [node.name for node in ast.walk(tree) if isinstance(node, ast.FunctionDef)]
        classes = [node.name for node in ast.walk(tree) if isinstance(node, ast.ClassDef)]

        print(f"{uf}:")
        if functions:
            print(f"  Functions: {', '.join(functions[:5])}")
        if classes:
            print(f"  Classes: {', '.join(classes[:3])}")
        print()
    except:
        pass
EOF
```

### Step 4.3: Unified Config System

```bash
# Create central config module
cat > /Users/steven/pythons/shared_modules/config/config.py << 'EOF'
"""Unified configuration system for all scripts"""
import os
from pathlib import Path
from dotenv import load_dotenv
import json

# Load environment variables
env_file = Path.home() / '.env.d' / 'llm-apis.env'
if env_file.exists():
    load_dotenv(env_file)

class Config:
    """Central configuration"""

    # API Keys
    OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
    ANTHROPIC_API_KEY = os.getenv('ANTHROPIC_API_KEY')
    GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
    GROQ_API_KEY = os.getenv('GROQ_API_KEY')

    # Paths
    PYTHONS_ROOT = Path('/Users/steven/pythons')
    AI_CONTENT_DIR = PYTHONS_ROOT / 'AI_CONTENT'
    DATA_UTILS_DIR = PYTHONS_ROOT / 'DATA_UTILITIES'
    MEDIA_PROCESSING_DIR = PYTHONS_ROOT / 'MEDIA_PROCESSING'

    # Output
    OUTPUT_DIR = PYTHONS_ROOT / 'output'
    CACHE_DIR = PYTHONS_ROOT / '.cache'

    def __init__(self):
        self.OUTPUT_DIR.mkdir(exist_ok=True)
        self.CACHE_DIR.mkdir(exist_ok=True)

config = Config()
EOF
```

---

## Phase 5: Create Consolidation Inventory (Day 5) — Documentation

### Step 5.1: Generate Master Inventory

```bash
# Create comprehensive script inventory
python3 << 'EOF'
#!/usr/bin/env python3
from pathlib import Path
import json
from datetime import datetime

inventory = {
    "timestamp": datetime.now().isoformat(),
    "summary": {},
    "by_directory": {},
    "duplicates_merged": [],
    "files_to_archive": []
}

# Count files by type
root = Path('/Users/steven/pythons')
for d in root.iterdir():
    if d.is_dir() and not d.name.startswith('.'):
        py_files = list(d.rglob('*.py'))
        if py_files:
            inventory["by_directory"][d.name] = {
                "file_count": len(py_files),
                "size_mb": sum(f.stat().st_size for f in py_files) / 1024 / 1024
            }

# Save inventory
with open(root / 'SCRIPT_INVENTORY.json', 'w') as f:
    json.dump(inventory, f, indent=2)

print("Inventory saved to SCRIPT_INVENTORY.json")
EOF
```

### Step 5.2: Create Consolidation Report

```bash
cat > /Users/steven/pythons/CONSOLIDATION_REPORT.md << 'EOF'
# Script Consolidation Report
Generated: $(date)

## Actions Taken

### Phase 1: Low-Risk Cleanup
- [ ] Removed .history directories: 130 MB saved
- [ ] Removed .venv directories: XX MB saved
- [ ] Removed __pycache__ and caches: XX MB saved

### Phase 2: Content Deduplication
- [ ] Removed 237 duplicate files: 1.13 MB saved
- [ ] Consolidated: [list of consolidated files]

### Phase 3: Variant Consolidation
- [ ] Archived timestamp variants: 0.7 MB saved
- [ ] Renamed conflicting filenames: XX files renamed

### Phase 4: Shared Modules
- [ ] Created shared_modules directory
- [ ] Consolidated utils.py
- [ ] Consolidated config.py
- [ ] Consolidated helpers.py

## Results

Total Space Recovered: XXX MB
Files Consolidated: XXX
Files Archived: XXX
Status: Complete ✓

## New Structure

/Users/steven/pythons/
├── AI_CONTENT/              (consolidated)
├── DATA_UTILITIES/          (consolidated)
├── MEDIA_PROCESSING/        (consolidated)
├── shared_modules/          (new - common code)
│   ├── utils/
│   ├── config/
│   ├── helpers/
│   └── api_clients/
└── .archive/                (old/duplicate files)
EOF
```

---

## Phase 6: Verification & Cleanup (Day 6) — Testing

### Step 6.1: Verify Key Scripts Still Work

```bash
# Test critical scripts
python3 << 'EOF'
import subprocess
from pathlib import Path

critical_scripts = [
    '/Users/steven/pythons/AI_CONTENT/text_generation/prompt_engineering/generate_prompts.py',
    '/Users/steven/pythons/AI_CONTENT/voice_synthesis/tts_engines/simple_tts_generator.py',
    '/Users/steven/pythons/MEDIA_PROCESSING/image_tools/batch_image_seo_pipeline.py',
]

for script in critical_scripts:
    p = Path(script)
    if p.exists():
        print(f"✓ {p.name} exists")
        # Test import if possible
        try:
            with open(p) as f:
                compile(f.read(), str(p), 'exec')
            print(f"  ✓ Syntax OK")
        except SyntaxError as e:
            print(f"  ✗ Syntax Error: {e}")
    else:
        print(f"✗ {p.name} MISSING - may have been deleted")
EOF
```

### Step 6.2: Remove Backup Files

```bash
# After verification, remove .backup files
find /Users/steven/pythons -name "*.backup" -type f | head -10

# Delete after confirming no errors
# find /Users/steven/pythons -name "*.backup" -delete
```

### Step 6.3: Final Space Check

```bash
# Compare before/after
echo "Current size:"
du -sh /Users/steven/pythons

echo "\nBreakdown:"
du -sh /Users/steven/pythons/*/ | sort -h
```

---

## Summary of Actions

| Phase | Action | Risk | Savings | Effort |
|-------|--------|------|---------|--------|
| 1 | Remove .history | ✅ None | 130 MB | 5 min |
| 1 | Remove .venv | ✅ Low | 10-50 MB | 5 min |
| 1 | Remove caches | ✅ None | 5-10 MB | 5 min |
| 2 | Remove duplicates | ✅ Low | 1.13 MB | 30 min |
| 3 | Archive variants | ⚠️ Medium | 0.7 MB | 1 hour |
| 4 | Create shared modules | ✅ Low | 0 | 2 hours |
| 5 | Documentation | ✅ None | 0 | 1 hour |
| 6 | Verification | ✅ None | 0 | 1 hour |
| | **TOTAL** | | **147 MB** | **6 hours** |

---

## Timeline

- **Day 1:** Phase 1 (cleanup)
- **Day 2-3:** Phase 2 (deduplication)
- **Day 3-4:** Phase 3 (variants)
- **Day 4-5:** Phase 4 (shared modules)
- **Day 5:** Phase 5 (documentation)
- **Day 6:** Phase 6 (verification)

---

## Recommendations for Future

1. **Use Git** instead of `file_1.py`, `file_2.py` patterns
2. **Establish naming conventions** (no generic `main.py`, `utils.py`)
3. **Regular cleanup** - monthly duplication scan
4. **Centralize configs** - use shared_modules/config/
5. **Archive old versions** - don't keep 16 timestamp variants

---

**Status: Ready to Execute**

Would you like to proceed with Phase 1 (low-risk cleanup)?
