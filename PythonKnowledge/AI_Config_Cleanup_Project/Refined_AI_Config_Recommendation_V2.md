# Refined AI Platform Configuration Management (V2)

## Overview
Building upon the original recommendation, this V2 document adds critical operational guardrails: **Version Control (Git)**, **Schema-based Registry**, and **Intelligent Configuration Merging**.

## Enhanced Architecture

```
~/.ai-platforms/                    # Central configuration repository (GIT REPO)
├── .git/                           # Version control tracking for all changes
├── global/                         # Shared platform configurations
│   ├── .claude/
│   ├── .cursor/
│   └── ...
├── registry/
│   ├── active-platforms.json       # Schema-validated platform map
│   └── migration-history.json      # Audit trail of moves/symlinks
└── scripts/
    ├── sync-global.sh              # Git push/pull to backup remote
    └── merge-overrides.py          # Intelligent JSON/YAML merge tool
```

## Key Improvements

### 1. Version Control as the Foundation
The `~/.ai-platforms/` directory **must** be a Git repository.
- **Why**: Allows one-command rollbacks, provides an audit log of "who changed what setting," and facilitates syncing across multiple machines via a private remote (e.g., GitHub private repo).
- **Security**: `.gitignore` must be strictly enforced for actual `oauth_creds.json` or `settings.json` keys, which should stay local or be handled via secret management (like `~/.env.d/`).

### 2. Intelligent Configuration Merging
Instead of simple symlinks, we propose a "Hydration" pattern for project-specific settings.
- **Global Base**: The base config in `~/.ai-platforms/global/.claude/settings.json`.
- **Project Layer**: `~/iterm2/project-platform-configs/claude-overrides.json`.
- **Merging**: A Python utility (`merge-overrides.py`) reads the base, applies the project layer, and optionally writes a temporary "Runtime Config" if the tool supports it, or updates the symlinked global config during project context switching.

### 3. Registry Schema
The `active-platforms.json` should track more than just paths:
```json
{
  "platforms": {
    "claude": {
      "status": "active",
      "canonical_path": "~/.ai-platforms/global/.claude",
      "symlink_location": "~/.claude",
      "last_migrated": "2026-05-18",
      "backup_integrity_hash": "sha256:..."
    }
  }
}
```

## Migration Phase Additions

### New Phase: "The Verification Burn-In"
Before final deletion of old project-specific configs (`~/iterm2/gemini/.gemini`):
1. **Redirect**: Point the project tool to the new global symlink.
2. **Observe**: Run for 48 hours in active use.
3. **Audit**: Check `.agent_ops` for any path-resolution warnings.
4. **Prune**: Only after 100% verification, delete the redundant project-level directory.

## Maintenance Commands
- `hermes sync`: Pulls latest global configs from git remote.
- `hermes diff <project>`: Shows how a project's overrides differ from the global baseline.
- `hermes checkpoint "message"`: Commits current global state to git.
