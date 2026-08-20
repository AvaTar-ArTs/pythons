# Backup Product Research For Local Replication

Research date: 2026-07-09

Target project: `/Users/steven/scripts/backup-nonmac-to-bakup.sh`

Working location note: `~/python/clean` does not exist. This brief lives in `/Users/steven/pythons/clean`.

## Product Set

### Carbon Copy Cloner

Source: https://bombich.com/

Strong patterns to replicate:

- Guided task model: source, destination, filters, schedule, verification.
- Clear preview of what will be backed up before the real run.
- Smart incremental copy: only changed files are copied.
- Resume interrupted copy work.
- Snapshot-style restore points where the destination filesystem supports it.
- Backup health checks and post-copy verification.
- Backup audit trail showing exactly what changed and why.
- Pre/post shell hooks for customized workflows.
- Handling for cloud-only files before local backup.

Fit for our script:

- High. Our rsync-based backup already has source/destination/filter concepts and dry-run mode.
- Add manifest, logs, verification, named tasks, and optional APFS snapshot management before considering a GUI.

### ChronoSync

Source: https://www.econtechnologies.com/chronosync/overview.html

Strong patterns to replicate:

- Backup and synchronization as separate modes.
- One-way and two-way folder synchronization.
- External, network, cloud, SFTP, and remote-agent destinations.
- Auto-mount network volumes for scheduled tasks.
- Stealth/background scheduled runs.
- Free support/documentation posture: make the tool understandable from its own logs and help output.

Fit for our script:

- Medium-high. We should support one-way backup first. Two-way sync should be a separate command because it carries higher deletion/conflict risk.
- Add `--mode backup|mirror|sync-preview` before adding any destructive sync behavior.

### SuperDuper

Source: https://www.shirt-pocket.com/SuperDuper/SuperDuperDescription.html

Strong patterns to replicate:

- Very simple main flow: choose source, choose destination, choose script, copy.
- Smart Update behavior for fast refreshes of an existing backup.
- Copy scripts for advanced include/exclude behavior.
- Human-readable confirmations before risky operations.
- Explicit checkpoint/sandbox use case before OS or app upgrades.
- Safety around deletes, including logic intended to reduce disk-full failures.

Fit for our script:

- High. This maps well to shell profiles like `nonmac`, `apps`, `library-state`, `project-root`, and `pre-upgrade-checkpoint`.
- Add named profile files instead of hardcoding every path in one long script.

### Arq

Source: https://www.arqbackup.com/

Strong patterns to replicate:

- Versioned backups, not just latest mirror state.
- Compression, deduplication, and block-level incrementals.
- Ransomware-oriented point-in-time recovery.
- Restore from the app/tool, not by manually reconstructing paths.
- Configurable network, battery, bandwidth, retention, and exclusion rules.
- Open/documented backup format.

Fit for our script:

- Medium. Rsync to a plain folder is intentionally transparent, but it is not deduplicated or block-versioned.
- If versioning becomes important, layer restic or Kopia beside rsync rather than rebuilding content-addressed backup storage ourselves.

### restic

Source: https://restic.net/

Strong patterns to replicate:

- Single executable, simple setup.
- Many storage backends.
- Only changed file parts are transferred.
- Cryptographic security throughout.
- Verifiable restore readiness.
- Open-source and repository-format compatibility discipline.

Fit for our script:

- High as a companion engine, not a replacement for all plain rsync copies.
- Use rsync for browsable local restore and restic for encrypted/versioned offsite or external-disk archives.

### Kopia

Source: https://kopia.io/

Strong patterns to replicate:

- GUI and CLI both operating over the same backup model.
- Encrypted, compressed, deduplicated snapshots.
- Policies for snapshot creation and restore.
- Cross-platform destination model.

Fit for our script:

- Medium-high as a future optional backend if we want policy-driven snapshots without writing our own repository engine.

### Duplicati

Source: https://duplicati.com/

Strong patterns to replicate:

- Bring-your-own-storage model.
- Local-to-local, local-to-cloud, cloud-to-local archive patterns.
- Centralized policies and schedule/retention controls.
- Changed-block transfer to reduce bandwidth.
- Local encryption before storage.
- Dashboard/alert-center thinking.

Fit for our script:

- Medium. The centralized console is overkill for this local Mac backup, but policy files, alerting, and retention rules are useful.

### Time Machine

Source: https://support.apple.com/en-us/104984

Strong patterns to replicate:

- Native expected baseline for Mac users.
- Simple restore story.
- Works best as system-native complement, not a replacement for selective non-Mac backups.

Fit for our script:

- Low as an implementation model, high as a baseline expectation. Our tool should clearly say what it covers that Time Machine may not make obvious: selected dotfiles, scripts, app bundles, application state, and browsable external backups.

## Product Requirements To Replicate First

### Phase 1: Robust CLI Backup Product

- Named backup profiles: `nonmac`, `applications`, `library-state`, `python-clean`, `project-root`.
- Prompted destination with safe defaults and target validation.
- Dry-run by default.
- Apply mode requiring explicit `--apply`.
- No deletes unless `--mirror-delete` is explicitly requested.
- Rsync itemized change logs saved under `logs/`.
- Machine-readable manifest saved as JSON or CSV.
- Human-readable summary at the end: copied count, skipped count, bytes, errors.
- Verification modes:
  - `--verify-size-time` for fast checks.
  - `--verify-checksum` for slower high-confidence checks.
- Config file support:
  - `~/.config/steven-backup/profiles/*.conf`
  - project-local profile files for special roots.

### Phase 2: Product-Grade Safety

- Preflight checks:
  - destination mounted and writable
  - enough free space estimate
  - target is not source
  - target is not home root
  - target is not `/`
- Cloud-file warnings for iCloud/Drive/Dropbox roots.
- Error classifier for common macOS failures:
  - permissions
  - AppleDouble/xattr issues
  - vanished files
  - unreadable cloud placeholders
  - path too long or weird characters
- Resume-friendly logs.
- `--continue-from-log` or at least clear re-run guidance.

### Phase 3: Restore UX

- `list` command: show available backup roots and runs.
- `find` command: search destination for a file.
- `restore-preview` command: dry-run restore of selected path.
- `restore` command: explicit copy back with conflict handling.
- Restore conflict policy:
  - skip existing
  - overwrite
  - restore beside with timestamp

### Phase 4: Optional Versioned Backend

- Keep rsync plain-folder backup as the default.
- Add optional restic or Kopia backend for encrypted, deduplicated, versioned backups.
- Do not try to reimplement dedupe/snapshot storage in Bash.

## Suggested Next Implementation

The current script should evolve from one hardcoded shell script into:

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

Immediate next code changes:

1. Add `--profile NAME`.
2. Add `--log-dir PATH`.
3. Save each rsync invocation output to a timestamped log.
4. Emit a final manifest at `$TARGET/inventory/backup-run-YYYYMMDD-HHMMSS.json`.
5. Add `python-clean` profile pointing at `/Users/steven/pythons/clean`.
6. Add `--verify` with a fast size/time dry-run after apply.

## What Not To Replicate

- Bootable clone management: too system-sensitive for this selective non-Mac backup script.
- Two-way sync as a default: too much risk of unwanted deletes/conflicts.
- Proprietary snapshot/repository format: use restic or Kopia if this becomes necessary.
- Cloud account management: keep local first, with cloud tools as optional backends.
