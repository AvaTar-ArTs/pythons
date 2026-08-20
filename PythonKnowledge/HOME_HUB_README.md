# Guides (home hub) — full tables

**Path:** `/Users/steven/Guides` — this file lives in **`library/`** with the rest of the markdown bundle.

---

## Copied trees (under `~/Guides`)

Synced from `PYTHON_MARKETPLACE_MASTER` with `rsync -a` (re-run the same command to refresh).

| Directory | Source | Role |
|-----------|--------|------|
| [`My-Deep-Proprietary/`](../My-Deep-Proprietary) | symlink | Resolves to **`PYTHON_MARKETPLACE_MASTER/My-Deep-Proprietary`** (canonical). See [`MERGED_UNIFIED.md`](file:///Users/steven/PYTHON_MARKETPLACE_MASTER/My-Deep-Proprietary/MERGED_UNIFIED.md). |
| [`deeptutor-mimic/`](../deeptutor-mimic) | symlink | Same as `My-Deep-Proprietary`. |
| [`MY_SETUP/`](../MY_SETUP) | thin | Pointer README; `deeptutor-mimic` symlink → unified tree. |

**This directory (`library/`):** marketplace guides + MY_SETUP hub docs — moved here from `~/Guides/Guides/` and `~/Guides/` root to avoid `Guides/Guides` nesting.

**Upstream-style DeepTutor checkout (canonical on this Mac):** `/Users/steven/Downloads/Compressed/DeepTutor-main` — not duplicated under `~/Guides`.

---

## Canonical collections (original paths)

| Location | Role |
|----------|------|
| [`PYTHON_MARKETPLACE_MASTER/Guides`](file:///Users/steven/PYTHON_MARKETPLACE_MASTER/Guides) | Authoritative marketplace guides — refresh **`~/Guides/library/*.md`** with `rsync` when needed |
| [`my-supremepowers/docs`](file:///Users/steven/my-supremepowers/docs) | SupremePower framework — INDEX + Mermaid architecture doc |

---

## Start here (deep links)

| Doc | Path |
|-----|------|
| DeepTutor — **full guide** (layout, packaging, env, Docker, runtime logic, HTTP/CLI, tests) | [`DeepTutor-REPO_LAYOUT_FLOWS_AND_HOWTO.md`](file:///Users/steven/Guides/library/DeepTutor-REPO_LAYOUT_FLOWS_AND_HOWTO.md) |
| DeepTutor architecture (Mermaid + exploration) | **Local:** [`DeepTutor-ARCHITECTURE_MAP_MERMAID_AND_EXPLORATION.md`](file:///Users/steven/Guides/library/DeepTutor-ARCHITECTURE_MAP_MERMAID_AND_EXPLORATION.md) · **Upstream:** [`PYTHON_MARKETPLACE_MASTER/Guides/...`](file:///Users/steven/PYTHON_MARKETPLACE_MASTER/Guides/DeepTutor-ARCHITECTURE_MAP_MERMAID_AND_EXPLORATION.md) |
| Horizontal vs vertical + SupremePower × DeepTutor | [`SUPREMEPOWERS_AND_DEEPTUTOR_CROSS_MAP.md`](file:///Users/steven/Guides/library/SUPREMEPOWERS_AND_DEEPTUTOR_CROSS_MAP.md) |
| Horizontal vs vertical — **detailed factors** | [`HORIZONTAL_VERTICAL_FACTORS.md`](file:///Users/steven/Guides/library/HORIZONTAL_VERTICAL_FACTORS.md) |
| Qwen / Gemini home review | [`QWEN_AND_GEMINI_HOME_REVIEW_2026-05-09.md`](file:///Users/steven/Guides/library/QWEN_AND_GEMINI_HOME_REVIEW_2026-05-09.md) |
| Marketplace bundle index (short TOC) | [`MARKETPLACE_GUIDES_INDEX.md`](file:///Users/steven/Guides/library/MARKETPLACE_GUIDES_INDEX.md) |
| SupremePower — diagrams & narrative | [`.../ARCHITECTURE_MERMAID_AND_NARRATIVE.md`](file:///Users/steven/my-supremepowers/docs/ARCHITECTURE_MERMAID_AND_NARRATIVE.md) |
| MY_SETUP fundamentals (mirror) | [`MY_SETUP/FUNDAMENTALS.md`](../MY_SETUP/FUNDAMENTALS.md) |
| Ecosystem fundamentals (copy in library) | [`FUNDAMENTALS.md`](file:///Users/steven/Guides/library/FUNDAMENTALS.md) |

---

## Optional: rsync marketplace guides → `library/`

```bash
rsync -a --delete --exclude '.DS_Store' \
  "/Users/steven/PYTHON_MARKETPLACE_MASTER/Guides/"/*.md \
  "/Users/steven/Guides/library/"
```

Then restore local-only names if needed (`MARKETPLACE_GUIDES_INDEX.md` was renamed from upstream `README.md`). Prefer editing **`PYTHON_MARKETPLACE_MASTER/Guides`** for bundle files that should stay canonical.
