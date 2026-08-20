# Guides

**Canonical path:** `/Users/steven/Guides`

This is the permanent home for personal guides, reviews, operating notes, ecosystem maps, and durable reference documents.

Use this directory for long-lived documentation instead of scattering review docs across runtime/tool directories like `.gemini`, `.codex`, `.qwen`, or temporary project folders.

## Current Policy

- Use uppercase `~/Guides` as canonical.
- Do not create new general-purpose review docs in lowercase `~/guides`.
- Keep runtime/tool docs inside tool homes only when they are specifically about that tool.
- Keep broad system, home-directory, AI-ecosystem, workflow, and project review docs here.
- Prefer adding a clear index/changelog entry when creating a durable guide.

See also:

- [`GUIDES_POLICY.md`](GUIDES_POLICY.md)
- [`CHANGELOG.md`](CHANGELOG.md)

## Recent / Active Guides

| Guide | Purpose |
|---|---|
| [`HOME_DIRECTORY_REVIEW.md`](HOME_DIRECTORY_REVIEW.md) | Current home-directory organization recommendations and safe zones. |
| [`GUIDES_POLICY.md`](GUIDES_POLICY.md) | Canonical location and policy for guides. |
| [`QWEN_AND_GEMINI_HOME_REVIEW_2026-05-09.md`](QWEN_AND_GEMINI_HOME_REVIEW_2026-05-09.md) | Earlier Qwen/Gemini home review. |
| [`PYTHONS_ECOSYSTEM_REVIEW.md`](PYTHONS_ECOSYSTEM_REVIEW.md) | Python ecosystem review. |
| [`MULTI_AGENT_HYGIENE.md`](MULTI_AGENT_HYGIENE.md) | Multi-agent hygiene notes. |
| [`NOTEBOOKLM_ECOSYSTEM_GUIDE.md`](NOTEBOOKLM_ECOSYSTEM_GUIDE.md) | NotebookLM ecosystem guide. |
| [`NOTEBOOKLM_FRACTAL_ANALYSIS.md`](NOTEBOOKLM_FRACTAL_ANALYSIS.md) | NotebookLM fractal analysis. |
| [`Python-environment-setup-how-to.md`](Python-environment-setup-how-to.md) | Python environment setup notes. |
| [`Ecosystem-Unified-Organization-2026-05-15.md`](Ecosystem-Unified-Organization-2026-05-15.md) | Ecosystem organization notes. |

## Agent / AI Ecosystem References

| Guide | Purpose |
|---|---|
| [`AGENT_ECOSYSTEM_INDEX_AND_REVIEW.md`](AGENT_ECOSYSTEM_INDEX_AND_REVIEW.md) | Agent ecosystem index and review. |
| [`AGENT_DOTFILES_AND_DOTFOLDERS.md`](AGENT_DOTFILES_AND_DOTFOLDERS.md) | Dotfolder/dotfile review for Cursor, Claude, Codex, and related tools. |
| [`AGENT_PATHS_DOCS_CSV_GAP_ANALYSIS.md`](AGENT_PATHS_DOCS_CSV_GAP_ANALYSIS.md) | Gap analysis for documented paths. |
| [`AGENT_SUBSET_PATHS_COMPARE.md`](AGENT_SUBSET_PATHS_COMPARE.md) | Subset path comparison. |
| [`AGENT_ECOSYSTEM_COMPREHENSIVE_2026-05-09.csv`](AGENT_ECOSYSTEM_COMPREHENSIVE_2026-05-09.csv) | Comprehensive agent ecosystem CSV. |
| [`_agent_paths_inventory.txt`](_agent_paths_inventory.txt) | Agent path inventory. |

## Concept / Architecture Guides

| Guide | Purpose |
|---|---|
| [`HORIZONTAL_VERTICAL_FLOWS_AND_EXAMPLES.md`](HORIZONTAL_VERTICAL_FLOWS_AND_EXAMPLES.md) | Horizontal/vertical flows and examples. |
| [`HORIZONTAL_LOGIC_COMPREHENSIVE.md`](HORIZONTAL_LOGIC_COMPREHENSIVE.md) | Horizontal logic reference. |
| [`VERTICAL_LOGIC_COMPREHENSIVE.md`](VERTICAL_LOGIC_COMPREHENSIVE.md) | Vertical logic reference. |
| [`HORIZONTAL_VERTICAL_FACTORS.md`](HORIZONTAL_VERTICAL_FACTORS.md) | Horizontal/vertical factor matrix. |
| [`SUPREMEPOWERS_AND_DEEPTUTOR_CROSS_MAP.md`](SUPREMEPOWERS_AND_DEEPTUTOR_CROSS_MAP.md) | SupremePowers and DeepTutor cross-map. |

## Directories

| Directory | Purpose |
|---|---|
| [`agent-landscape-map/`](agent-landscape-map/) | Agent landscape mapping materials. |
| [`AI_Config_Cleanup_Project/`](AI_Config_Cleanup_Project/) | AI configuration cleanup project notes. |
| [`book_of_memory/`](book_of_memory/) | Book of memory materials. |
| [`cline/`](cline/) | Cline-related guide materials. |
| [`plans/`](plans/) | Planning documents. |

## Archive / Bundle Files

These are present but should be reviewed before expanding or relying on them:

```text
Archive.zip
book_of_memory.zip
cline.zip
```

## Relationship to Tool Runtime Docs

Some tool-specific docs currently live in tool runtime homes, for example:

```text
/Users/steven/.gemini/docs
```

That is fine for tool-specific Gemini notes. General system reviews should live here in:

```text
/Users/steven/Guides
```

## Home Organization Direction

Preferred high-level zones:

```text
/Users/steven/github/              GitHub repos and maintained projects
/Users/steven/Guides/              personal guides, reviews, and operating docs
/Users/steven/scripts/             local scripts/workspace
/Users/steven/.gemini/             live Gemini runtime/config
/Users/steven/.codex/              live Codex runtime/config
/Users/steven/.claude/             live Claude runtime/config
/Users/steven/.qwen/               live Qwen runtime/config
/Users/steven/.cline/              live Cline runtime/history
/Users/steven/.ai-platforms/       AI manifests/reports/reference material, kept lightweight
```

## Useful `eza` Commands

```bash
eza -la --group-directories-first /Users/steven/Guides

eza -lah --sort=modified --reverse /Users/steven/Guides

eza -T -L 2 --group-directories-first /Users/steven/Guides
```

## Maintenance Notes

- Keep this README current when adding major guides.
- Avoid duplicate `README.md` / `Readme.md` drift. On this macOS filesystem they may refer to the same file depending on case-sensitivity behavior.
- Prefer descriptive filenames with dates for reviews.
- Keep broad guides here; keep ephemeral logs, cache, and runtime state out.
