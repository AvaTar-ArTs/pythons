# AI Configuration Migration: Safety & Verification Plan

## 1. Preparation
- **Full Backup**: Create a snapshot of `~/` and `~/.config/` before any changes.
- **Environment State Capture**: Record the current list of running processes and their associated open files (using `lsof`).
- **Registry Creation**: Create the `~/.ai-platforms/registry/` structure to document current associations *before* breaking them.

## 2. Verification Methodology
- **Dependency Mapping**: Run `grep -r` across your primary codebases (`~/iterm2/`, `~/XEO-Project/`, etc.) to find hardcoded references to `~/.gemini`, `~/.claude`, etc.
- **Dry Run Migration**: Simulate the move using a script that logs all planned filesystem changes (`mv`/`ln`) without executing them.
- **Validation Loop**:
    - After each individual platform migration (e.g., move `.claude` first):
        - Verify symlink integrity (`readlink`).
        - Perform a "Sanity Test": Run the CLI tool (e.g., `claude --version` or basic help command) to ensure configuration is correctly loaded.
        - Monitor error logs in `~/.agent_ops/` for unexpected "file not found" errors.

## 3. Rollback Procedure
- **Automated Restore**: A script (`rollback-configs.sh`) will:
    - Stop active agents.
    - Remove temporary symlinks.
    - Move configuration directories back to their original `~/` or `~/.config/` locations.
    - Restore from the backup snapshot if necessary.

## 4. Operational Guardrails
- **Execution Policy**: Never perform bulk operations. Migrate one platform at a time (e.g., only move `.gemini` first).
- **Interactive Approval**: The migration script must prompt for user confirmation between *each* platform move.
