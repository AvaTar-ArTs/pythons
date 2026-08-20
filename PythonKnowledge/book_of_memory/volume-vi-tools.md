# Volume VI: The Toolchain

## git-ai — Universal Authorship Tracking

A git proxy that attributes every commit to the AI tool that authored it.

| Command | Purpose |
|---------|---------|
| `git-ai log --oneline -5` | Recent commits with AI attribution |
| `git-ai blame <file>` | Line-by-line AI authorship |
| `git-ai stats` | AI authorship statistics |
| `git-ai install-hooks` | Install/update hooks across all platforms |

**Tracked per commit**: AI tool, model, human author, prompts, accepted vs overridden lines.

**Platforms with hooks**: Claude Code, Codex, Cursor, VS Code, GitHub Copilot, OpenCode, Gemini, Windsurf

## Chat History Export System

Three-layer redundancy for session persistence:

| Layer | Mechanism | Interval |
|-------|-----------|----------|
| Primary | launchd (macOS native) | Every 5 min (Cline) / 6 min (Gemini) |
| Fallback | cron | Every hour |
| Manual | Shell aliases | On demand |

### Commands
- `ai-export-all` — Export all unexported from both platforms
- `ai-search <term>` — Search all chat history
- `ai-stats` — Show unified statistics
- `cline-export` / `gemini-export` — Platform-specific exports

### What's Captured
- User prompts, AI responses, thinking traces, tool calls, tool results
- Session metadata: model, provider, cost, tokens, timing

## Launchd Agents

| Label | Script | Interval |
|-------|--------|----------|
| `com.user.cline-chat-export` | `export-chat-history.py --all` | 300s |
| `com.user.gemini-chat-export` | `export-gemini-history.py --all` | 360s |

## Shell Aliases (in `~/.cline/aliases.zsh`)

Sourced from `~/.zshrc`:
```bash
[[ -f "$HOME/.cline/aliases.zsh" ]] && source "$HOME/.cline/aliases.zsh"
```
