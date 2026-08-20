# `~/.qwen` and `~/.gemini` — review (helpful content & hygiene)

Date: 2026-05-09  
Scope: **navigation and value** — not full file duplication. **Credential files were not opened.**

```text
+ QWEN_HOME=/Users/steven/.qwen
+ GEMINI_HOME=/Users/steven/.gemini
```

---

## 1. Scale snapshot

| Root | Approx size | Approx file count | Character |
|------|-------------|-------------------|-----------|
| `~/.qwen` | ~650 MB | ~1,666 | **Curated control plane** — git-tracked root, manifests, mirrored skills, flow docs. |
| `~/.gemini` | ~1.4 GB | ~37,752 | **Extension-heavy** — most bytes/files live under `extensions/` (~26k files sampled); plus `tmp/`, `history`, hooks. |

---

## 2. `~/.qwen` — highest-leverage reads

### 2.1 Root markdown (orientation)

| File | Why open it |
|------|-------------|
| `README.md` | Entry narrative for this tree. |
| `QWEN.md` | Primary Qwen-oriented behavior / invocation notes. |
| `QWEN_SYSTEM_DEFINITION.md` | System shape and constraints. |
| `Working_Principles.md` / `Use_Cases_And_Triggers.md` | When automation vs manual; trigger vocabulary. |
| `Master_Recall_Index.md` | Fast recall / lookup across artifacts. |
| `IMPORT_MANIFEST.md` | What was imported from where (lineage). |
| `INTEGRATION_SUMMARY.md` | Cross-host integration snapshot. |
| `ECOSYSTEM_ANALYSIS.md` | Broader ecosystem framing (Feb snapshot — compare dates). |

### 2.2 `docs/` — operational truth for flows

| File | Why open it |
|------|-------------|
| **`docs/FLOWS_INDEX.md`** | **Start here** — orders `FLOWS_RUNTIME_MAP`, systematic debugging flow, dedupe guardrails, review artifacts. |
| `docs/FLOWS_RUNTIME_MAP.md` | Runtime roots, command resolution, skill load order. |
| `docs/FLOWS_SYSTEMATIC_DEBUGGING.md` | Activation path for debugging skill across Qwen/Gemini mirrors. |
| `docs/FLOWS_DEDUPE_GUARDRAILS.md` | Safe cleanup policy — use before deleting duplicates. |
| `docs/SOURCE_OF_TRUTH_AND_LAYERS.md` | **Layer model:** `.supremepower` baseline vs `~/.qwen` adaptation vs `~/.gemini/extensions/...` vs hook injectors — reduces “which copy do I edit?” |
| `docs/QWEN_CAPABILITY_REGISTRY.md` | Capability registry mental model (aligns with host tooling). |
| `docs/INSTALLATION_HOST_CROSSWALK.md` | Host-specific install paths. |
| `docs/learned-context.md` | Cached decisions/terms (check before contradicting past choices). |
| `docs/plans/*.md` | Dated plans (hook bootstrap, reliability loops, capability integration). |

### 2.3 Executable surfaces worth knowing

- **`agents/`** — many agent definitions (personas, routing).
- **`commands/`** — slash/command-style entry points.
- **`skills/`** — includes **`superpowers-*`** adapters (brainstorming, TDD, debugging, plans, etc.).
- **`integrations/supremepower/`** — mirrored SupremePower skills/docs/registry — **often the copy you edit when syncing Gemini/Qwen**.
- **`hookify/`**, **`new-hooks-system/`** — hook experiments and architecture notes (`new-hooks-system/findings-and-thoughts/`).
- **`.env` → `~/.env.d/llm-apis.env`** — **good pattern**: secrets centralized outside both dotdirs.

### 2.4 Sensitive / do-not-share blindly

Mode-sensitive or secret-adjacent filenames observed at top level: `oauth_creds.json`, `google_accounts.json`, `installation_id`, `.env` symlink target. **Treat tarball backups of `~/.qwen` like key material.**

---

## 3. `~/.gemini` — highest-leverage reads

### 3.1 Root

| File | Why open it |
|------|-------------|
| **`GEMINI.md`** | **Layered instructions** (user norms, imported rules, workflow chains). May contain **personal identifiers and preferences** — do not paste into public repos wholesale; excerpt intentionally. |
| `GIT_AI.md` | Git/checkpoint habits for AI-assisted work. |
| `update.sh` | Maintenance script for this tree. |

### 3.2 `docs/` (home/ecosystem inventories)

Examples present on disk: `HOME-ECOSYSTEM-INVENTORY.md`, `EXTENSIONS-INVENTORY.md`, `ENABLED-EXTENSIONS.md`, `GEMINI-FILES-INDEX.md`, `TMP-REVIEW.md`, agent/hooks/MCP-focused notes. Use these when asking **“what is installed?”** without enumerating `extensions/` by hand.

### 3.3 Runtime directories

| Path | Role |
|------|------|
| `extensions/` | Bulk of disk — third-party MCP packs, skills, DB toolboxes, etc. |
| `skills/` (top-level) | Ten skill folders — quick surface besides extensions. |
| `hooks/` | Gemini CLI hook configs. |
| `history/` | Session/history artifacts (small file count vs extensions). |
| `tmp/` | Thousands of temp files — **prime cleanup candidate** when reclaiming disk (verify CLI closed first). |
| `backups/` / `extensions_backup/` | Recovery-oriented copies. |
| `antigravity/` | Separate product subtree (Google Antigravity integration). |

### 3.4 Sensitive / do-not-share blindly

`oauth_creds.json`, `google_accounts.json`, `extension_integrity.json`, `settings.json`, `trustedFolders.json` — **typically mode 600**. Same backup caution as `.qwen`.

---

## 4. How Qwen and Gemini **work together** (from your own docs)

`~/.qwen/docs/FLOWS_INDEX.md` explicitly cross-checks Gemini paths, e.g. verifying `systematic-debugging` skill presence under **both** `~/.gemini/extensions/...` and `~/.qwen/integrations/...`.

`SOURCE_OF_TRUTH_AND_LAYERS.md` states the intended discipline:

- **Baseline:** `~/.supremepower` (when used).
- **Adaptation:** `~/.qwen/superpowers/*`, `~/.qwen/skills/superpowers-*`, `~/.qwen/integrations/supremepower/*`.
- **Gemini mirror:** `~/.gemini/extensions/supremepower/skills/` (and `core/skills/`).

When you improve a skill, decide **which layer is canonical** for that edit, then propagate per your manifest/import pipeline — otherwise copies drift.

---

## 5. Recommended “first hour” navigation

1. Read **`~/.qwen/docs/FLOWS_INDEX.md`** → follow its numbered sequence.  
2. Read **`~/.qwen/docs/SOURCE_OF_TRUTH_AND_LAYERS.md`** → fix mental map of duplicates.  
3. Skim **`~/.gemini/docs/HOME-ECOSYSTEM-INVENTORY.md`** or **`EXTENSIONS-INVENTORY.md`** → know what extensions claim to do.  
4. Open **`~/.gemini/GEMINI.md`** locally only — extract **non-sensitive** rules you want in team docs; redact personal lines.

---

## 6. Optional maintenance commands (non-destructive)

```bash
qwen-sp status 2>/dev/null || true
ls -la ~/.qwen/docs/FLOWS_INDEX.md ~/.qwen/docs/SOURCE_OF_TRUTH_AND_LAYERS.md
ls ~/.gemini/docs | head
/usr/bin/find ~/.gemini/tmp -type f 2>/dev/null | wc -l   # tmp churn indicator
```

---

*For marketplace-wide AI roots, see `DOCUMENTATION/ECOSYSTEM_DEEP_REVIEW_MULTIROOT_2026-05-09.md`. For DeepTutor-specific guides, see `Guides/DeepTutor-ARCHITECTURE_MAP_MERMAID_AND_EXPLORATION.md`.*
