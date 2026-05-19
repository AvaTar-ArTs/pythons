#!/usr/bin/env python3
"""Generate removal scripts from merged analysis results."""

import csv
from pathlib import Path

# Load merged results
with open("merged_analysis_results.csv", "r") as f:
    reader = csv.DictReader(f)
    data = list(reader)

# Phase 1: Very High confidence, both methods
phase1 = [
    r
    for r in data
    if r["confidence"] == "Very High" and r["agreement"] == "Both methods"
]

# Phase 2: High confidence, both methods
phase2 = [
    r for r in data if r["confidence"] == "High" and r["agreement"] == "Both methods"
]

# Generate Phase 1 script
with open("remove_phase1_safe.sh", "w") as f:
    f.write("#!/bin/bash\n")
    f.write("# Phase 1: Very High Confidence - SAFE TO REMOVE\n")
    f.write("# Both methods agree - 100% code similarity\n")
    f.write("# Generated automatically from merged analysis\n\n")
    f.write("BACKUP_DIR=~/backups/pythons_cleanup_$(date +%Y%m%d)\n")
    f.write('mkdir -p "$BACKUP_DIR"\n')
    f.write("cd ~/pythons\n\n")
    f.write("echo '🟢 Phase 1: Removing Very High Confidence Duplicates (10 files)'\n")
    f.write(
        "echo '======================================================================'\n\n"
    )

    for r in phase1:
        filename = Path(r["file_to_remove"]).name
        keep_file = Path(r["keep_file"]).name
        similarity = r["similarity_score"]
        f.write(f"# {filename} -> {keep_file} (similarity: {similarity})\n")
        f.write(f'if [ -f "{filename}" ]; then\n')
        f.write(f'  cp "{filename}" "$BACKUP_DIR/"\n')
        f.write(f'  rm "{filename}"\n')
        f.write(f'  echo "✅ Removed: {filename}"\n')
        f.write("else\n")
        f.write(f'  echo "⚠️  Not found: {filename}"\n')
        f.write("fi\n\n")

    f.write('echo ""\n')
    f.write('echo "✅ Phase 1 Complete! Backed up to: $BACKUP_DIR"\n')

# Generate Phase 2 script
with open("remove_phase2_review.sh", "w") as f:
    f.write("#!/bin/bash\n")
    f.write("# Phase 2: High Confidence - REVIEW RECOMMENDED\n")
    f.write("# Both methods agree - review before removal\n")
    f.write("# Generated automatically from merged analysis\n\n")
    f.write("BACKUP_DIR=~/backups/pythons_cleanup_$(date +%Y%m%d)\n")
    f.write('mkdir -p "$BACKUP_DIR"\n')
    f.write("cd ~/pythons\n\n")
    f.write("echo '🟡 Phase 2: High Confidence Duplicates (Review Recommended)'\n")
    f.write(
        "echo '======================================================================'\n\n"
    )

    for r in phase2:
        filename = Path(r["file_to_remove"]).name
        keep_file = Path(r["keep_file"]).name
        similarity = r["similarity_score"]
        f.write(f"# {filename} -> {keep_file} (similarity: {similarity})\n")
        f.write(f'echo "Reviewing: {filename}"\n')
        f.write(f'if [ -f "{filename}" ]; then\n')
        f.write(f'  echo "  Keep file: {keep_file}"\n')
        f.write(f'  echo "  Similarity: {similarity}"\n')
        f.write('  read -p "  Remove this file? (y/n): " answer\n')
        f.write('  if [ "$answer" = "y" ]; then\n')
        f.write(f'    cp "{filename}" "$BACKUP_DIR/"\n')
        f.write(f'    rm "{filename}"\n')
        f.write(f'    echo "  ✅ Removed: {filename}"\n')
        f.write("  else\n")
        f.write(f'    echo "  ⏭️  Skipped: {filename}"\n')
        f.write("  fi\n")
        f.write("else\n")
        f.write(f'  echo "  ⚠️  Not found: {filename}"\n')
        f.write("fi\n")
        f.write('echo ""\n\n')

    f.write('echo "✅ Phase 2 Complete! Backed up to: $BACKUP_DIR"\n')

print("✅ Generated removal scripts:")
print(f"   - remove_phase1_safe.sh ({len(phase1)} files)")
print(f"   - remove_phase2_review.sh ({len(phase2)} files)")
