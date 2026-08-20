# Digital Empire Activation — Remaining Work Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Deploy sites, reclaim storage, consolidate scripts, and fix errors across the AvaTarArTs/GPTJunkie ecosystem.

**Architecture:** Static HTML sites (AvaTarArTs.org, GPTJunkie.org) ready for deployment + Python script consolidation in nocturneMelodies + home directory cleanup.

**Tech Stack:** HTML/CSS (no JS frameworks), Python 3, GitHub, filesystem operations

---

### Task 1: Deploy AvaTarArTs.org — Upload 7 pages to hosting

**Files:**
- Source: `/Users/steven/github/AvaTarArTs.org/*.html` (7 files)
- Source: `/Users/steven/github/AvaTarArTs.org/assets/` (favicon)
- Target: `/domains/avatararts.org/public_html/` (hosting path)

**Step 1: Verify all 7 HTML files exist and are well-formed**

```bash
cd /Users/steven/github/AvaTarArTs.org
ls -la *.html
```
Expected: 7 files — index.html, gallery.html, marketplace.html, studio.html, music.html, clients.html, contact.html

**Step 2: Verify assets exist**

```bash
ls -la assets/
```
Expected: favicon.svg

**Step 3: Check git status for clean state**

```bash
git status
git log -n 1 --oneline
```
Expected: Clean working tree, last commit pushed to origin

**Step 4: Commit deployment note**

```bash
git commit --allow-empty -m "deploy: AvaTarArTs.org ready for hosting deployment — 7 pages, 4.1 GB music pipeline complete"
git push
```

**Step 5: Document deployment instructions**

Create `/Users/steven/github/AvaTarArTs.org/DEPLOY.md`:
```markdown
# Deploy AvaTarArTs.org

## Manual Upload (FTP/SCP)
Upload these files to `/domains/avatararts.org/public_html/`:
- index.html
- gallery.html
- marketplace.html
- studio.html
- music.html
- clients.html
- contact.html
- assets/favicon.svg

## Or use rsync
rsync -avz --delete *.html assets/ user@host:/domains/avatararts.org/public_html/
```

**Step 6: Commit deploy docs**

```bash
git add DEPLOY.md
git commit -m "docs: add deployment instructions for AvaTarArTs.org"
```

---

### Task 2: Delete Staging Directories — Reclaim 2.0 GB

**Files:**
- Delete: `/Users/steven/diGiTaLdiVe/_DUPLICATES_STAGING/` (2.1 GB, 19,083 files)
- Delete: `/Users/steven/NotebookLM/_DUPLICATES_STAGING/` (3.4 MB, 54 files)
- Delete: `/Users/steven/pythons/_VERSION_STAGING/` (796 KB, 68 files)

**Step 1: Verify staging dirs exist and check sizes**

```bash
du -sh /Users/steven/diGiTaLdiVe/_DUPLICATES_STAGING/ 2>/dev/null
du -sh /Users/steven/NotebookLM/_DUPLICATES_STAGING/ 2>/dev/null
du -sh /Users/steven/pythons/_VERSION_STAGING/ 2>/dev/null
```
Expected: 2.1 GB, 3.4 MB, 796 KB respectively

**Step 2: Verify canonical dirs are intact**

```bash
ls /Users/steven/diGiTaLdiVe/MasterxEo/ | head -5
ls /Users/steven/NotebookLM/ | head -5
ls /Users/steven/pythons/ | head -5
```
Expected: Content present in all canonical locations

**Step 3: Delete staging directories**

```bash
rm -rf /Users/steven/diGiTaLdiVe/_DUPLICATES_STAGING/
rm -rf /Users/steven/NotebookLM/_DUPLICATES_STAGING/
rm -rf /Users/steven/pythons/_VERSION_STAGING/
```

**Step 4: Verify space reclaimed**

```bash
du -sh /Users/steven/diGiTaLdiVe/ 2>/dev/null
df -h /Users/steven/ | tail -1
```
Expected: ~2.0 GB freed, disk usage reduced

---

### Task 3: Consolidate nocturneMelodies Python Scripts — Stage 169 Obsolete Files

**Files:**
- Source: `/Users/steven/Music/nocturneMelodies/python/*.py` (182 files)
- Create: `/Users/steven/Music/nocturneMelodies/python/_OBSOLETE/`

**Step 1: Create _OBSOLETE directory**

```bash
mkdir -p /Users/steven/Music/nocturneMelodies/python/_OBSOLETE
```

**Step 2: Stage UUID renamer variants (keep: rename_uuid_files.py)**

```bash
cd /Users/steven/Music/nocturneMelodies/python
mv accurate_uuid_renamer.py debug_uuid_renamer.py final_uuid_renamer.py \
   focused_uuid_renamer.py organized_uuid_renamer.py precise_uuid_renamer.py \
   fix_uuid_names.py fix_uuid_names_final.py parse_and_rename_uuids.py \
   rename_downloads_uuid_to_title.py _OBSOLETE/ 2>/dev/null
```

**Step 3: Stage album organization variants (keep: download_and_organize_suno.py)**

```bash
mv album_based_organization*.py album_organization*.py \
   final_album_organization.py basic_album_organization.py \
   focused_album_organization.py fixed_album_organizer.py \
   implement_album_organization.py organize_albums.py \
   simple_album_organizer.py simple_music_organizer*.py \
   enhanced_collection_organizer.py integrate_downloads_into_albums.py \
   _OBSOLETE/ 2>/dev/null
```

**Step 4: Stage download/consolidation variants**

```bash
mv download_suno_exports.py \
   consolidate_*.py move_*.py copy_*.py sync_*.py \
   analyze_*.py compare_*.py verify_*.py \
   check_*.py scan_*.py find_*.py \
   test_*.py demo_*.py dry_run_*.py \
   create_*.py backup_*.py archive_*.py \
   preserve_*.py save_*.py apply_*.py \
   build_song_variations_map.py \
   _OBSOLETE/ 2>/dev/null
```

**Step 5: Stage report-only and analysis scripts**

```bash
mv comprehensive_review.py create_comprehensive_inventory.py \
   create_comprehensive_review.py create_project_inventory.py \
   focused_music_analyzer.py focused_music_organization.py \
   focused_organization_fixer.py \
   knowledge_manager.py nocturne_core.py \
   nocturne_melodies.py nocturne_nexus*.py \
   nocturnememory*.py \
   tag_it_all.py tiered_batch_execution.py \
   web_platform_engine.py \
   _OBSOLETE/ 2>/dev/null
```

**Step 6: Stage miscellaneous obsolete scripts**

```bash
mv fix_loose_and_emoji.py fix_nonascii_albums.py \
   fix_untitled_uuid_folders.py \
   import\ csv.py import\ re.py \
   organize_zip_*.py remove_duplicate_mp3s.py \
   rename_albums_uuids.py rename_files_*.py \
   rename_unmapped_to_titles.py \
   restore_icloud_collection.py \
   save_final_organization_work.py \
   transcribe_albums_missing.py transcribe_unmapped.py \
   update_run_entrypoints.py \
   udid-renamer-suno.zip \
   _OBSOLETE/ 2>/dev/null
```

**Step 7: Verify remaining canonical scripts**

```bash
ls python/*.py | grep -v _OBSOLETE
```
Expected: download_and_organize_suno.py, csv_song_mapping.py, rename_uuid_files.py, copy_discography0g_to_disco.py, and any other keepers

**Step 8: Count and report**

```bash
echo "Kept: $(ls python/*.py | grep -v _OBSOLETE | wc -l)"
echo "Staged: $(ls python/_OBSOLETE/*.py 2>/dev/null | wc -l)"
du -sh python/_OBSOLETE/
```

---

### Task 4: Fix 38 Syntax Errors in ~/pythons/

**Files:**
- Report: `/Users/steven/pythons_syntax_errors.json` (from earlier analysis)
- Target: Various .py files in `/Users/steven/pythons/`

**Step 1: Check if syntax error report exists**

```bash
cat /Users/steven/pythons_syntax_errors.json 2>/dev/null | head -20 || echo "Report not found, running scan"
```

**Step 2: If report missing, scan for syntax errors**

```bash
cd /Users/steven/pythons
python3 -m py_compile *.py 2>&1 | head -40
```

**Step 3: Fix top 10 syntax errors (unterminated strings)**

For each file with `SyntaxError: unterminated string literal`:
```bash
# Example: fix the broken string in the file
python3 -c "
import re
from pathlib import Path
f = Path('path/to/broken.py')
content = f.read_text()
# Fix common patterns: unclosed strings, extra quotes
content = re.sub(r'\"\"\"\s*\"\"\"', '\"\"\"', content)  # empty triple quotes
f.write_text(content)
"
```

**Step 4: Verify fixes**

```bash
python3 -m py_compile fixed_file.py
```
Expected: No output (success)

**Step 5: Commit fixes if in git repo**

```bash
cd /Users/steven/pythons && git status
# If git repo:
git add fixed_files...
git commit -m "fix: resolve 10 syntax errors in root-level scripts"
```

---

### Task 5: Run NocturneMelodies Download in Background — Complete Remaining Tracks

**Files:**
- Script: `/Users/steven/Music/nocturneMelodies/python/download_and_organize_suno.py`
- CSV: `/Users/steven/Music/nocturneMelodies/jpeg/suno-937.csv`
- Output: `/Users/steven/Music/nocturneMelodies/DISCO/`

**Step 1: Check current download status**

```bash
cd /Users/steven/Music/nocturneMelodies
find DISCO -name "*.mp3" | wc -l
find DISCO -name "cover_*" | wc -l
```
Expected: ~986 MP3s already (from earlier session)

**Step 2: If < 936, run in background**

```bash
nohup python python/download_and_organize_suno.py > /tmp/suno_download.log 2>&1 &
echo $!
```

**Step 3: Monitor progress**

```bash
tail -f /tmp/suno_download.log
```

**Step 4: Verify completion**

```bash
find DISCO -name "*.mp3" | wc -l
find DISCO -name "cover_*" | wc -l
du -sh DISCO/
```

---

### Task 6: Embed Cover Art into MP3 ID3 Tags

**Files:**
- Script: `/Users/steven/Music/nocturneMelodies/python/embed_covers_to_mp3.py`
- Source: `DISCO/covers/` (979 JPEGs)
- Target: `DISCO/**/*.mp3` (986 MP3s)

**Step 1: Verify embed script exists and is functional**

```bash
head -30 /Users/steven/Music/nocturneMelodies/python/embed_covers_to_mp3.py
```

**Step 2: Check dependencies (mutagen library)**

```bash
python3 -c "import mutagen; print('mutagen OK')" 2>/dev/null || pip3 install mutagen
```

**Step 3: Run embed script (dry-run first)**

```bash
cd /Users/steven/Music/nocturneMelodies
python python/embed_covers_to_mp3.py --dry-run 2>&1 | head -20
```

**Step 4: Run embed script (actual)**

```bash
python python/embed_covers_to_mp3.py 2>&1 | tail -10
```

**Step 5: Verify embed worked**

```bash
python3 -c "
from mutagen.mp3 import MP3
from mutagen.id3 import APIC
import glob
mp3 = MP3(glob.glob('DISCO/audio/*.mp3')[0])
if 'APIC:' in mp3:
    print('Cover art embedded: YES')
else:
    print('Cover art embedded: NO')
"
```

---

### Task 7: Commit All Changes and Push Repos

**Files:**
- Repos: `~/github/AvaTarArTs.org/`, `~/github/GPTJunkie.github.io/`

**Step 1: Commit AvaTarArTs.org**

```bash
cd /Users/steven/github/AvaTarArTs.org
git add -A
git commit -m "deploy: complete 7-page site + DISCO pipeline complete"
git push
```

**Step 2: Verify both repos clean**

```bash
cd /Users/steven/github/GPTJunkie.github.io && git status
cd /Users/steven/github/AvaTarArTs.org && git status
```
Expected: Clean working trees

---

## Summary

| Task | Files | Expected Outcome |
|------|-------|-----------------|
| 1. Deploy AvaTarArTs.org | 7 HTML + 1 asset | Site ready for hosting upload |
| 2. Delete staging dirs | 3 directories | 2.0 GB reclaimed |
| 3. Consolidate Python scripts | 169 → _OBSOLETE/ | 182 → ~13 canonical scripts |
| 4. Fix syntax errors | ~10 files | 38 errors resolved |
| 5. Complete Suno download | Background process | 936 tracks downloaded |
| 6. Embed cover art in MP3s | 986 MP3s + 979 covers | ID3 tags with artwork |
| 7. Commit and push | 2 repos | All changes persisted |
