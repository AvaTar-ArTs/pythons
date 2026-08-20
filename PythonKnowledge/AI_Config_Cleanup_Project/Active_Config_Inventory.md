# AI Configuration Inventory & Activity Report

## Executive Summary
An audit of active process file handles (`lsof`) was conducted across major AI configuration directories in `~/`. 

## Activity Matrix
| Directory | Open File Handles | Status |
|-----------|-------------------|--------|
| `~/.claude/` | 2 | Inactive / Idle |
| `~/.cursor/` | 2 | Inactive / Idle |
| `~/.gemini/` | 2 | Inactive / Idle |
| `~/.grok/` | 2 | Inactive / Idle |
| `~/.qwen/` | 2 | Inactive / Idle |
| `~/.codex/` | 2 | Inactive / Idle |
| `~/.ollama/` | 2 | Inactive / Idle |
| `~/.crewai/` | 2 | Inactive / Idle |
| `~/.opencode/` | 2 | Inactive / Idle |
| `~/.hermes/` | 71 | **Active** (likely current session) |
| `~/.superpowers/` | 0 | Not Found / Moved |

## Observations
- **Low Risk Migration**: Most directories appear to be idle. Moving these to `~/.ai-platforms/global/` and symlinking back should be low-risk for the running environment.
- **High Risk**: `~/.hermes/` is actively being used. Any migration of this directory should only be performed when the agent is not running or during a controlled maintenance window.
- **Missing Paths**: `~/.superpowers/` does not exist in the home root. It may have already been moved or the canonical source is elsewhere (e.g., `~/iterm2/superpowers`).

## Next Steps
- Verify if any background daemons (like `ollama`, `pm2`, or `docker`) are using these paths despite the low `lsof` count.
- Proceed to refine the migration logic with version control integration.
