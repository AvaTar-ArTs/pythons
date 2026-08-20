# Backup Conversation Checkpoint

Created: 2026-07-09 04:51:09

Working area: `/Users/steven/pythons/clean`

Export directory: `/Users/steven/pythons/clean/export`

## User Goal

Create a practical Mac backup workflow for "everything not mac basic" using `rsync`, covering high-value user files, scripts, app bundles, selected application state in `~/Library`, and useful system-level non-OS assets. The backup target should be prompted, not fixed, with `/Volumes/bakUp/steven-nonmac-backup` as the default target.

## Key User Directives

- Use `eza` for directory review.
- Include `/Applications`.
- Test with a single Python file first.
- Use `~/steven-backup-test`, then `/Volumes/bakUp`.
- Test a real `.app` bundle, specifically `/Applications/Alfred 5.app` or `/Applications/MacCleaner Pro 3.app`.
- Apply the same thinking to app-related `~/Library` data.
- Search `~/` for `.py` and `.sh` backup scripts and review them.
- Create the new backup script in `~/scripts` or `~/pythons`.
- Research similar backup products to replicate useful product patterns.
- Treat `~/python/clean` as intended to mean the existing `/Users/steven/pythons/clean`; exact `/Users/steven/python/clean` does not exist.

## Tested Backup Behavior

### Single File Dry Run

Source:

```text
/Users/steven/pythons/scan-to-csv/doc-source-enriched.py
```

Initial dry run with `-aEvn` exposed AppleDouble sidecar errors:

```text
._steven
._doc-source-enriched.py
```

Using plain archive mode without extended attribute copying worked:

```bash
rsync -avvn --itemize-changes --relative /Users/steven/pythons/scan-to-csv/doc-source-enriched.py /Users/steven/steven-backup-test/
```

The same dry-run pattern worked against:

```text
/Volumes/bakUp/steven-backup-test/
```

### Application Bundle Test

Chosen app:

```text
/Applications/Alfred 5.app
```

Dry-run copy to:

```text
/Volumes/bakUp/steven-backup-test/Applications/Alfred 5.app/
```

Result:

- 386 total app bundle entries.
- 336 regular files transferred on actual copy.
- Total size copied: about 11.8 MB.
- Post-copy dry run showed no changes remaining.
- Source and destination entry counts both matched at 386.

### Alfred User Library State Test

Selected high-value Alfred restore paths:

```text
/Users/steven/Library/Application Support/Alfred/
/Users/steven/Library/Alfred/
/Users/steven/Library/Preferences/com.runningwithcrayons.Alfred-Preferences.plist
/Users/steven/Library/Preferences/com.runningwithcrayons.Alfred.plist
/Users/steven/Library/Preferences/mr.pennyworth.AlfredExtraPane.plist
```

Destination:

```text
/Volumes/bakUp/steven-backup-test/User-Library-Alfred/
```

Result:

- Actual copy completed after escalation because default sandbox blocked some `~/Library` reads.
- 971 entries considered.
- 562 regular files transferred.
- Total copied size: about 154 MB.
- Verification dry run showed no remaining changes.
- Non-`.DS_Store` source/destination counts matched at 938.

## Existing Backup Scripts Reviewed

Reviewed likely candidates under `~/scripts` and `~/pythons`:

```text
/Users/steven/scripts/full-home-backup.sh
/Users/steven/scripts/backup_dotfiles.sh
/Users/steven/scripts/rsync_icloud.sh
/Users/steven/scripts/rsync_sitesuck.sh
/Users/steven/scripts/backup-and-clean-brew-python.sh
/Users/steven/pythons/compare_home_backup.py
/Users/steven/pythons/backup-installations.py
```

Findings:

- `full-home-backup.sh` is the best rough starting point but hardcodes `/Volumes/macBaks/GPTJunkie`, skips some major user folders, and does not handle `/Applications` or selected `~/Library` app-state cleanly.
- `backup_dotfiles.sh` uses `--delete`, which is too risky as a general backup default.
- `rsync_sitesuck.sh` uses `--remove-source-files`, so it is an offload/migration script, not a backup script.
- `rsync_icloud.sh` uses `--ignore-existing`, so changed files may not update in future runs.
- `backup-and-clean-brew-python.sh` mixes backup inventory with cleanup/setup behavior and should be split.
- `compare_home_backup.py` is comparison-oriented and limited to a Pictures backup layout.

## New Script Created

Created executable script:

```text
/Users/steven/scripts/backup-nonmac-to-bakup.sh
```

Validation performed:

```bash
bash -n /Users/steven/scripts/backup-nonmac-to-bakup.sh
/Users/steven/scripts/backup-nonmac-to-bakup.sh --help
```

Core behavior:

- Dry-run by default.
- `--apply` required for actual copying.
- Prompts for target if not supplied.
- Default target is `/Volumes/bakUp/steven-nonmac-backup`.
- Allows `--target PATH`.
- Allows `--default-target`.
- Refuses unsafe targets such as `/`, `$HOME`, and `/Users/steven`.
- Allows targets under `/Volumes/*` or `$HOME/*`.
- Does not use `--delete` unless `--mirror-delete` is explicitly provided.
- Uses common dev/cache excludes.
- Copies:
  - high-value home folders
  - selected dot directories
  - selected root-level user files
  - `/Applications`
  - selected `~/Library` paths
  - selected `/Library`, `/usr/local`, and `/opt` paths
  - inventory files for Homebrew and pip during apply mode

## Product Research Created

Created:

```text
/Users/steven/pythons/clean/backup-product-research.md
```

Products reviewed:

- Carbon Copy Cloner
- ChronoSync
- SuperDuper
- Arq
- restic
- Kopia
- Duplicati
- Time Machine

Main replication recommendations:

- Add named profiles.
- Keep dry-run default.
- Keep delete behavior explicit and opt-in.
- Save logs and machine-readable manifests.
- Add verification modes.
- Add restore-preview and restore workflows.
- Use restic or Kopia if encrypted, deduplicated, versioned snapshots become necessary.

## Recommended Next Implementation

Evolve from a single hardcoded shell script into a profile-driven layout:

```text
~/scripts/backup-nonmac-to-bakup.sh
~/.config/steven-backup/
  profiles/
    nonmac.conf
    applications.conf
    library-state.conf
    python-clean.conf
  excludes/
    common.txt
    dev-cache.txt
    mac-runtime.txt
```

Next code changes:

1. Add `--profile NAME`.
2. Add `--log-dir PATH`.
3. Save each rsync invocation output to a timestamped log.
4. Emit final manifest at `$TARGET/inventory/backup-run-YYYYMMDD-HHMMSS.json`.
5. Add a `python-clean` profile pointing at `/Users/steven/pythons/clean`.
6. Add `--verify` with a fast size/time no-op rsync check after apply.

## Current Important Paths

```text
/Users/steven/scripts/backup-nonmac-to-bakup.sh
/Users/steven/pythons/clean/backup-product-research.md
/Users/steven/pythons/clean/export/backup-conversation-checkpoint-20260709-045109.md
/Volumes/bakUp/steven-backup-test/
/Volumes/bakUp/steven-nonmac-backup
```

## Open Cautions

- A full backup dry run may be very noisy because the script currently runs all phases and itemizes changes.
- `/Applications` and `~/Library` can include permission-sensitive files.
- `--delete` should remain opt-in only.
- Plain rsync backups are browsable and simple, but not encrypted, deduplicated, or versioned.
- AppleDouble/xattr behavior needs continued attention; `-aE` caused sidecar failures in the single-file test.
