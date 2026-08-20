# Home Directory Review

Generated: 2026-05-18

Reviewed:

```text
/Users/steven
```

This report is intentionally stored in:

```text
/Users/steven/guides/HOME_DIRECTORY_REVIEW.md
```

## Purpose

Use `/Users/steven/guides` as the permanent location for personal system guides, reviews, and operating notes.

## Current Organization Direction

Keep home cleaner by using stable zones:

```text
/Users/steven/github/              GitHub repos and maintained projects
/Users/steven/guides/              personal guides, reviews, and operating docs
/Users/steven/scripts/             local scripts/workspace
/Users/steven/.gemini/             live Gemini runtime/config
/Users/steven/.codex/              live Codex runtime/config
/Users/steven/.claude/             live Claude runtime/config
/Users/steven/.qwen/               live Qwen runtime/config
/Users/steven/.cline/              live Cline runtime/history
/Users/steven/.ai-platforms/       AI manifests/reports/reference material, kept lightweight
```

## High-Level Suggestions

1. Keep new GitHub repos under `/Users/steven/github/<owner>/<repo>`.
2. Keep long-lived docs and reviews under `/Users/steven/guides`.
3. Avoid creating more top-level project folders directly in `/Users/steven`.
4. Keep live AI tool homes as runtime homes, not source-control symlink targets unless intentionally cleaned.
5. Review backup directories before deleting; do not remove security/app-managed dot directories casually.

## Do Not Touch Casually

```text
/Users/steven/.ssh
/Users/steven/.gnupg
/Users/steven/.config
/Users/steven/.local
/Users/steven/.zshrc
/Users/steven/.zprofile
/Users/steven/.zshenv
/Users/steven/Library
```

## Good Next Reviews

- `/Users/steven/.ai-platforms/backups`
- `/Users/steven/.dotfile_trash`
- `/Users/steven/iterm2`
- duplicate AI tool copies and old archives

## eza Commands

```bash
eza -la --group-directories-first /Users/steven

eza -lah --sort=size --reverse /Users/steven/.ai-platforms/backups

eza -T -L 2 --group-directories-first /Users/steven/github

eza -lah --git --group-directories-first /Users/steven/github/AvaTar-ArTs/terminal-workflows
```
