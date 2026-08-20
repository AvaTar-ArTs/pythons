# AI Platforms Review

Generated: 2026-05-18 08:24:24

Reviewed:

```text
/Users/steven/.ai-platforms
```

This was an inventory/review pass. No files were moved or deleted.

## Executive Summary

`/Users/steven/.ai-platforms` should stay lightweight: manifests, reports, docs, deploy/reference scripts, and curated references. It should **not** become a storage location for full live AI tool homes, logs, caches, session databases, or repeated backups.

Current main observations:

- `.ai-platforms/backups` is still the largest area and contains a remaining Supremepowers backup.
- Gemini backups were previously removed.
- `source/gemini` is currently missing, which is cleaner than a broken placeholder.
- `manifests/` and `reports/` hold useful history of the Gemini cleanup/migration attempts.
- `.gitignore` exists and should continue protecting backups/runtime/cache/secrets.

## Top-Level Sizes

```text
586M	/Users/steven/.ai-platforms/backups
168K	/Users/steven/.ai-platforms/.git
 24K	/Users/steven/.ai-platforms/manifests
 12K	/Users/steven/.ai-platforms/global
 12K	/Users/steven/.ai-platforms/docs
 12K	/Users/steven/.ai-platforms/.DS_Store
8.0K	/Users/steven/.ai-platforms/source
8.0K	/Users/steven/.ai-platforms/AI_PLATFORMS_REVIEW.md
4.0K	/Users/steven/.ai-platforms/reports
4.0K	/Users/steven/.ai-platforms/README.md
4.0K	/Users/steven/.ai-platforms/deploy
4.0K	/Users/steven/.ai-platforms/ai_platforms_review.csv
4.0K	/Users/steven/.ai-platforms/.gitignore
  0B	/Users/steven/.ai-platforms/registry
```

## Depth-2 Size Snapshot

```text
586M	/Users/steven/.ai-platforms/backups/supremepowers_pre_restructure_20260518
586M	/Users/steven/.ai-platforms/backups
168K	/Users/steven/.ai-platforms/.git
 64K	/Users/steven/.ai-platforms/.git/hooks
 28K	/Users/steven/.ai-platforms/.git/objects
 24K	/Users/steven/.ai-platforms/manifests
 24K	/Users/steven/.ai-platforms/.git/ai
 12K	/Users/steven/.ai-platforms/global
 12K	/Users/steven/.ai-platforms/docs
 12K	/Users/steven/.ai-platforms/backups/.DS_Store
 12K	/Users/steven/.ai-platforms/.git/logs
 12K	/Users/steven/.ai-platforms/.DS_Store
8.0K	/Users/steven/.ai-platforms/source/.DS_Store
8.0K	/Users/steven/.ai-platforms/source
8.0K	/Users/steven/.ai-platforms/global/.DS_Store
8.0K	/Users/steven/.ai-platforms/docs/GEMINI_AI_PLATFORMS_ARCHITECTURE_AND_CHANGELOG.md
8.0K	/Users/steven/.ai-platforms/AI_PLATFORMS_REVIEW.md
8.0K	/Users/steven/.ai-platforms/.git/refs
8.0K	/Users/steven/.ai-platforms/.git/.DS_Store
4.0K	/Users/steven/.ai-platforms/reports/gemini-source-vs-live-20260518_071503.md
4.0K	/Users/steven/.ai-platforms/reports
4.0K	/Users/steven/.ai-platforms/README.md
4.0K	/Users/steven/.ai-platforms/manifests/gemini.json
4.0K	/Users/steven/.ai-platforms/manifests/gemini-vanilla-live-migration-20260518_063252.md
4.0K	/Users/steven/.ai-platforms/manifests/gemini-specified-backups-removal-20260518_071025.md
4.0K	/Users/steven/.ai-platforms/manifests/gemini-source-prune-20260518_063319.md
4.0K	/Users/steven/.ai-platforms/manifests/gemini-redundant-backup-removal-20260518_070651.md
4.0K	/Users/steven/.ai-platforms/manifests/gemini-live-restore-20260518_064807.md
4.0K	/Users/steven/.ai-platforms/global/README.md
4.0K	/Users/steven/.ai-platforms/docs/CHANGELOG.md
4.0K	/Users/steven/.ai-platforms/deploy/gemini.sh
4.0K	/Users/steven/.ai-platforms/deploy
4.0K	/Users/steven/.ai-platforms/ai_platforms_review.csv
4.0K	/Users/steven/.ai-platforms/.gitignore
4.0K	/Users/steven/.ai-platforms/.git/info
4.0K	/Users/steven/.ai-platforms/.git/index
4.0K	/Users/steven/.ai-platforms/.git/HEAD
4.0K	/Users/steven/.ai-platforms/.git/description
4.0K	/Users/steven/.ai-platforms/.git/config
4.0K	/Users/steven/.ai-platforms/.git/COMMIT_EDITMSG
  0B	/Users/steven/.ai-platforms/registry
```

## Important Path Status

```text
--- /Users/steven/.ai-platforms/backups
drwxr-xr-x - steven 18 May 07:10 /Users/steven/.ai-platforms/backups
586M	/Users/steven/.ai-platforms/backups
--- /Users/steven/.ai-platforms/source
drwxr-xr-x - steven 18 May 07:52 /Users/steven/.ai-platforms/source
8.0K	/Users/steven/.ai-platforms/source
--- /Users/steven/.ai-platforms/global
drwxr-xr-x - steven 18 May 06:32 /Users/steven/.ai-platforms/global
 12K	/Users/steven/.ai-platforms/global
--- /Users/steven/.ai-platforms/manifests
drwxr-xr-x - steven 18 May 07:10 /Users/steven/.ai-platforms/manifests
 24K	/Users/steven/.ai-platforms/manifests
--- /Users/steven/.ai-platforms/reports
drwxr-xr-x - steven 18 May 07:15 /Users/steven/.ai-platforms/reports
4.0K	/Users/steven/.ai-platforms/reports
--- /Users/steven/.ai-platforms/deploy
drwxr-xr-x - steven 18 May 06:32 /Users/steven/.ai-platforms/deploy
4.0K	/Users/steven/.ai-platforms/deploy
--- /Users/steven/.ai-platforms/.gitignore
.rw-r--r-- 752 steven 18 May 06:33 /Users/steven/.ai-platforms/.gitignore
4.0K	/Users/steven/.ai-platforms/.gitignore
--- /Users/steven/.ai-platforms/README.md
.rw-r--r-- 699 steven 18 May 06:32 /Users/steven/.ai-platforms/README.md
4.0K	/Users/steven/.ai-platforms/README.md
--- /Users/steven/.ai-platforms/AI_PLATFORMS_REVIEW.md
.rw-r--r-- 6.5k steven 18 May 06:14 /Users/steven/.ai-platforms/AI_PLATFORMS_REVIEW.md
8.0K	/Users/steven/.ai-platforms/AI_PLATFORMS_REVIEW.md
--- /Users/steven/.ai-platforms/ai_platforms_review.csv
.rw-r--r-- 3.7k steven 18 May 06:14 /Users/steven/.ai-platforms/ai_platforms_review.csv
4.0K	/Users/steven/.ai-platforms/ai_platforms_review.csv
```

## Backup Inventory

```text
586M	/Users/steven/.ai-platforms/backups/supremepowers_pre_restructure_20260518
 12K	/Users/steven/.ai-platforms/backups/.DS_Store
```

## Manifest and Report Inventory

```text
/Users/steven/.ai-platforms/manifests/gemini-live-restore-20260518_064807.md
/Users/steven/.ai-platforms/manifests/gemini-redundant-backup-removal-20260518_070651.md
/Users/steven/.ai-platforms/manifests/gemini-source-prune-20260518_063319.md
/Users/steven/.ai-platforms/manifests/gemini-specified-backups-removal-20260518_071025.md
/Users/steven/.ai-platforms/manifests/gemini-vanilla-live-migration-20260518_063252.md
/Users/steven/.ai-platforms/manifests/gemini.json
/Users/steven/.ai-platforms/reports/gemini-source-vs-live-20260518_071503.md
```

## Git Status / Ignored Snapshot

```text
M .gitignore
?? AI_PLATFORMS_REVIEW.md
?? README.md
?? ai_platforms_review.csv
?? deploy/
?? docs/
?? global/
?? manifests/
?? reports/
!! .DS_Store
!! backups/
!! global/.DS_Store
!! source/
```

## Potential Sensitive / Runtime Names

These are names only. Contents were not read.

```text
/Users/steven/.ai-platforms/.git/ai/logs
/Users/steven/.ai-platforms/.git/logs
/Users/steven/.ai-platforms/backups/supremepowers_pre_restructure_20260518/.git/logs
/Users/steven/.ai-platforms/backups/supremepowers_pre_restructure_20260518/logs
```

## Recommendations

### Keep

```text
/Users/steven/.ai-platforms/manifests
/Users/steven/.ai-platforms/reports
/Users/steven/.ai-platforms/deploy
/Users/steven/.ai-platforms/README.md
/Users/steven/.ai-platforms/.gitignore
```

These support auditability and explain what happened.

### Review First

```text
/Users/steven/.ai-platforms/backups/supremepowers_pre_restructure_20260518
```

This is the remaining large backup-like item. Do not delete until you confirm it is duplicated elsewhere or no longer needed.

### Consider Cleaning

```text
/Users/steven/.ai-platforms/.DS_Store
/Users/steven/.ai-platforms/global/.DS_Store
/Users/steven/.ai-platforms/source/.DS_Store
```

These are macOS metadata files and are already normally safe to ignore/remove if desired.

### Avoid Reintroducing

Avoid adding these under `.ai-platforms` unless intentionally curated:

```text
full ~/.gemini copies
full ~/.codex copies
full ~/.qwen copies
full ~/.claude copies
sessions/
logs/
history/
tmp/
cache/
node_modules/
*.sqlite
*.jsonl
auth/token/oauth/credential files
```

## Suggested Target Role

```text
.ai-platforms = lightweight AI management/reference layer
```

Good contents:

```text
manifests/
reports/
deploy/
docs or README notes
small curated source snippets
review CSV/MD files
```

Bad contents:

```text
large runtime homes
chat/session databases
logs/caches/temp folders
large duplicate backups
secrets/auth material
```

## Next Actions

1. Decide whether to keep or remove `backups/supremepowers_pre_restructure_20260518`.
2. Keep `source/gemini` absent unless you intentionally recreate it as a clean curated source directory.
3. Keep general reviews in `/Users/steven/Guides`; keep `.ai-platforms` focused on AI-platform-specific records.
4. If committing `.ai-platforms`, inspect `git status --ignored` carefully first.
5. Do not symlink live tool homes into `.ai-platforms` without a very clear reason.

## Useful eza Commands

```bash
eza -la --git --group-directories-first /Users/steven/.ai-platforms

eza -lah --sort=size --reverse /Users/steven/.ai-platforms/backups

eza -T -L 2 --group-directories-first /Users/steven/.ai-platforms
```
