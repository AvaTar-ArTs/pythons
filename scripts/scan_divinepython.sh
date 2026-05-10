#!/usr/bin/env bash
set -euo pipefail

TARGET="/Volumes/macBaks/diVinePyTHon"
OUTDIR="/Users/steven/pythons/docs/inventory"
mkdir -p "$OUTDIR"

REPORT="$OUTDIR/divinepython-full-tree-2026-04-12.md"
TMPDIR_WORK=$(mktemp -d)
trap 'rm -rf "$TMPDIR_WORK"' EXIT

echo "=== Scanning $TARGET ==="

# ============================================================
# 1. Full recursive directory tree (up to 3 levels deep for readability)
# ============================================================
echo "[1/7] Generating full tree (3 levels)..."
tree -L 3 -a --dirsfirst "$TARGET" > "$TMPDIR_WORK/tree_3levels.txt" 2>/dev/null || {
  # fallback if tree not installed
  find "$TARGET" -maxdepth 3 -print | sed "s|$TARGET|.|; s|[^/]*/|  |g" | sort > "$TMPDIR_WORK/tree_3levels.txt"
}

# ============================================================
# 2. Full listing (all depths) for metrics
# ============================================================
echo "[2/7] Building full path listing..."
find "$TARGET" -mindepth 1 > "$TMPDIR_WORK/all_paths.txt"

TOTAL_ITEMS=$(wc -l < "$TMPDIR_WORK/all_paths.txt")
TOTAL_DIRS=$(find "$TARGET" -mindepth 1 -type d | wc -l | tr -d ' ')
TOTAL_FILES=$(find "$TARGET" -mindepth 1 -type f | wc -l | tr -d ' ')
TOTAL_SYMLINKS=$(find "$TARGET" -mindepth 1 -type l 2>/dev/null | wc -l | tr -d ' ' || echo "0")

# ============================================================
# 3. Total size
# ============================================================
echo "[3/7] Calculating total size..."
# Use du -sk for total (macOS compatible), result in KB
TOTAL_SIZE_KB=$(du -sk "$TARGET" 2>/dev/null | cut -f1)
TOTAL_SIZE_BYTES=$((TOTAL_SIZE_KB * 1024))
# Human readable
if (( TOTAL_SIZE_BYTES > 1073741824 )); then
  TOTAL_SIZE_HUMAN=$(awk "BEGIN {printf \"%.2f GB\", $TOTAL_SIZE_BYTES/1073741824}")
elif (( TOTAL_SIZE_BYTES > 1048576 )); then
  TOTAL_SIZE_HUMAN=$(awk "BEGIN {printf \"%.2f MB\", $TOTAL_SIZE_BYTES/1048576}")
else
  TOTAL_SIZE_HUMAN="${TOTAL_SIZE_BYTES} bytes"
fi

# ============================================================
# 4. File counts per directory (top-level and sub)
# ============================================================
echo "[4/7] Counting files per directory..."
# Per-directory: count direct children (files only), recurse for total
# For top-level dirs under TARGET:
find "$TARGET" -mindepth 1 -maxdepth 1 -type d | sort | while IFS= read -r dir; do
  name=$(basename "$dir")
  fcount=$(find "$dir" -type f 2>/dev/null | wc -l | tr -d ' ')
  dcount=$(find "$dir" -mindepth 1 -type d 2>/dev/null | wc -l | tr -d ' ')
  dsize_kb=$(du -sk "$dir" 2>/dev/null | cut -f1)
  dsize=$((dsize_kb * 1024))
  echo "${name}	${dcount}	${fcount}	${dsize}"
done > "$TMPDIR_WORK/dir_counts.tsv"

# ============================================================
# 5. Deep nesting (more than 3 levels deep from TARGET)
# ============================================================
echo "[5/7] Finding deep nesting (>3 levels)..."
TARGET_DEPTH=$(echo "$TARGET" | tr '/' '\n' | wc -l | tr -d ' ')
MAX_DEPTH_ALLOWED=$((TARGET_DEPTH + 3))
find "$TARGET" -mindepth 1 -type d | while IFS= read -r dir; do
  depth=$(echo "$dir" | tr '/' '\n' | wc -l | tr -d ' ')
  if [ "$depth" -gt "$MAX_DEPTH_ALLOWED" ]; then
    rel="${dir#$TARGET/}"
    rel_depth=$((depth - TARGET_DEPTH))
    echo "${rel_depth}	${rel}"
  fi
done | sort -t$'\t' -k1 -rn > "$TMPDIR_WORK/deep_dirs.txt"

# ============================================================
# 6. Empty directories
# ============================================================
echo "[6/7] Finding empty directories..."
find "$TARGET" -mindepth 1 -type d -empty 2>/dev/null | sed "s|$TARGET/||" | sort > "$TMPDIR_WORK/empty_dirs.txt"

# ============================================================
# 7. Largest 30 files
# ============================================================
echo "[7/7] Finding largest files..."
find "$TARGET" -mindepth 1 -type f -exec stat -f '%z %N' {} + 2>/dev/null | sort -rn > "$TMPDIR_WORK/largest_files_all.txt"
head -30 "$TMPDIR_WORK/largest_files_all.txt" > "$TMPDIR_WORK/largest_files.txt"

# ============================================================
# 8. Duplicate directory names at different levels
# ============================================================
echo "[8/8] Finding duplicate directory names..."
find "$TARGET" -mindepth 1 -type d | sed "s|$TARGET/||" | awk -F'/' '{print $NF}' | sort | uniq -d > "$TMPDIR_WORK/dup_dirnames.txt"

# For each dup name, show where it appears
> "$TMPDIR_WORK/dup_dirnames_detail.txt"
while IFS= read -r dupname; do
  echo "--- $dupname ---" >> "$TMPDIR_WORK/dup_dirnames_detail.txt"
  find "$TARGET" -mindepth 1 -type d -name "$dupname" | sed "s|$TARGET/||" | sort >> "$TMPDIR_WORK/dup_dirnames_detail.txt"
  echo "" >> "$TMPDIR_WORK/dup_dirnames_detail.txt"
done < "$TMPDIR_WORK/dup_dirnames.txt"

# ============================================================
# Extension breakdown
# ============================================================
echo "  Computing extension breakdown..."
find "$TARGET" -mindepth 1 -type f | sed 's|.*\.||' | sort | uniq -c | sort -rn | head -20 > "$TMPDIR_WORK/extensions.txt"

# ============================================================
# Generate the markdown report
# ============================================================
echo "Generating report..."

cat > "$REPORT" << 'HEADER'
# 📁 DiVinePyTHon — Full Directory Tree Manifest

**Generated:** DATE_PLACEHOLDER
**Source:** `/Volumes/macBaks/diVinePyTHon/`
**Scan Type:** Read-only (no files modified)

HEADER

sed -i '' "s|DATE_PLACEHOLDER|$(date '+%Y-%m-%d %H:%M %Z')|" "$REPORT"

# --- Overview ---
cat >> "$REPORT" << EOF
## 1. Overview

| Metric | Value |
|---|---|
| **Total directories** | $TOTAL_DIRS |
| **Total files** | $TOTAL_FILES |
| **Total items** | $TOTAL_ITEMS |
| **Symlinks** | $TOTAL_SYMLINKS |
| **Total size** | $TOTAL_SIZE_HUMAN |
| **Total size (bytes)** | $TOTAL_SIZE_BYTES |

EOF

# --- Extension breakdown ---
cat >> "$REPORT" << 'EOF'
## 1.1 Top 20 File Extensions

| Count | Extension |
|------:|:----------|
EOF
awk '{ext=$2; count=$1; printf "| %s | `.%s` |\n", count, ext}' "$TMPDIR_WORK/extensions.txt" >> "$REPORT"
echo "" >> "$REPORT"

# --- Directory tree ---
cat >> "$REPORT" << 'EOF'
## 2. Full Directory Tree (3 Levels Deep)

\`\`\`
EOF
cat "$TMPDIR_WORK/tree_3levels.txt" >> "$REPORT"
echo '```' >> "$REPORT"
echo "" >> "$REPORT"

# --- File counts per directory ---
cat >> "$REPORT" << 'EOF'
## 3. File Counts & Sizes per Top-Level Directory

| Directory | Subdirs | Files | Size (bytes) | Size (human) |
|:----------|--------:|------:|-------------:|:-------------|
EOF
while IFS=$'\t' read -r name dcount fcount dsize; do
  if (( dsize > 1073741824 )); then
    shuman=$(awk "BEGIN {printf \"%.2f GB\", $dsize/1073741824}")
  elif (( dsize > 1048576 )); then
    shuman=$(awk "BEGIN {printf \"%.2f MB\", $dsize/1048576}")
  elif (( dsize > 1024 )); then
    shuman=$(awk "BEGIN {printf \"%.2f KB\", $dsize/1024}")
  else
    shuman="${dsize} B"
  fi
  printf "| %-30s | %7s | %6s | %12s | %s |\n" "$name" "$dcount" "$fcount" "$dsize" "$shuman" >> "$REPORT"
done < "$TMPDIR_WORK/dir_counts.tsv"
echo "" >> "$REPORT"

# --- Deep nesting ---
DEEP_COUNT=$(wc -l < "$TMPDIR_WORK/deep_dirs.txt" | tr -d ' ')
cat >> "$REPORT" << EOF
## 4. Deep Nesting (>3 levels from root)

**Total deeply nested directories:** $DEEP_COUNT

EOF
if [ "$DEEP_COUNT" -gt 0 ]; then
  echo "| Depth | Path (relative) |" >> "$REPORT"
  echo "|------:|:----------------|" >> "$REPORT"
  head -50 "$TMPDIR_WORK/deep_dirs.txt" | while IFS=$'\t' read -r depth relpath; do
    printf "| %s | \`%s\` |\n" "$depth" "$relpath" >> "$REPORT"
  done
  if [ "$DEEP_COUNT" -gt 50 ]; then
    echo "" >> "$REPORT"
    echo "*... and $(( DEEP_COUNT - 50 )) more (see full listing in analysis artifacts)*" >> "$REPORT"
  fi
else
  echo "✅ No directories exceed 3 levels of nesting." >> "$REPORT"
fi
echo "" >> "$REPORT"

# --- Empty directories ---
EMPTY_COUNT=$(wc -l < "$TMPDIR_WORK/empty_dirs.txt" | tr -d ' ')
cat >> "$REPORT" << EOF
## 5. Empty Directories

**Total empty directories:** $EMPTY_COUNT

EOF
if [ "$EMPTY_COUNT" -gt 0 ]; then
  echo "| Path (relative) |" >> "$REPORT"
  echo "|:----------------|" >> "$REPORT"
  while IFS= read -r relpath; do
    echo "| \`$relpath\` |" >> "$REPORT"
  done < "$TMPDIR_WORK/empty_dirs.txt"
else
  echo "✅ No empty directories found." >> "$REPORT"
fi
echo "" >> "$REPORT"

# --- Largest files ---
cat >> "$REPORT" << 'EOF'
## 6. Top 30 Largest Files

| Rank | Size (bytes) | Size (human) | Path (relative) |
|-----:|-------------:|:-------------|:----------------|
EOF
rank=0
while IFS= read -r line; do
  rank=$((rank + 1))
  size_bytes=$(echo "$line" | awk '{print $1}')
  fpath=$(echo "$line" | cut -d' ' -f2-)
  fpath_rel="${fpath#$TARGET/}"
  if (( size_bytes > 1073741824 )); then
    shuman=$(awk "BEGIN {printf \"%.2f GB\", $size_bytes/1073741824}")
  elif (( size_bytes > 1048576 )); then
    shuman=$(awk "BEGIN {printf \"%.2f MB\", $size_bytes/1048576}")
  elif (( size_bytes > 1024 )); then
    shuman=$(awk "BEGIN {printf \"%.2f KB\", $size_bytes/1024}")
  else
    shuman="${size_bytes} B"
  fi
  printf "| %2d | %12s | %s | \`%s\` |\n" "$rank" "$size_bytes" "$shuman" "$fpath_rel" >> "$REPORT"
done < "$TMPDIR_WORK/largest_files.txt"
echo "" >> "$REPORT"

# --- Duplicate directory names ---
DUP_COUNT=$(wc -l < "$TMPDIR_WORK/dup_dirnames.txt" | tr -d ' ')
cat >> "$REPORT" << EOF
## 7. Duplicate Directory Names at Different Levels

**Total duplicate names:** $DUP_COUNT

EOF
if [ "$DUP_COUNT" -gt 0 ]; then
  cat "$TMPDIR_WORK/dup_dirnames_detail.txt" >> "$REPORT"
else
  echo "✅ No duplicate directory names found at different levels." >> "$REPORT"
fi
echo "" >> "$REPORT"

# --- Footer ---
cat >> "$REPORT" << 'EOF'
---

*Report generated by read-only scan. No files were modified.*
EOF

echo ""
echo "=== REPORT WRITTEN TO: $REPORT ==="
echo "Total size: $TOTAL_SIZE_HUMAN"
echo "Files: $TOTAL_FILES | Dirs: $TOTAL_DIRS | Deep: $DEEP_COUNT | Empty: $EMPTY_COUNT | Dup names: $DUP_COUNT"
