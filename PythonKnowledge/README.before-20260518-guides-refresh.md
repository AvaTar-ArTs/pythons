# Guides — home folder

**Path:** `/Users/steven/Guides`

- **Python envs (general, any repo):** [`Python-environment-setup-how-to.md`](Python-environment-setup-how-to.md) — venv, uv, Miniforge+mamba, micromamba, conda.
- **Long-form docs + mirrors index:** [`library/HOME_HUB_README.md`](library/HOME_HUB_README.md) (tables, deep links, rsync notes).
- **Library bundle (atlases, MY_SETUP prose, inventory JSON):** [`library/`](library/) — see [`library/MARKETPLACE_GUIDES_INDEX.md`](library/MARKETPLACE_GUIDES_INDEX.md) for the marketplace-guide subset.

**Trees on disk**

| Path | Role |
|------|------|
| [`library/`](library/) | Documentation bundle (atlases, hub tables). |
| [`My-Deep-Proprietary/`](My-Deep-Proprietary/) | **Symlink** → [`PYTHON_MARKETPLACE_MASTER/My-Deep-Proprietary`](file:///Users/steven/PYTHON_MARKETPLACE_MASTER/My-Deep-Proprietary) (canonical unified tree: DeepTutor + overlay + mimic + `docs/my-setup-hub/`). [`MERGED_UNIFIED.md`](file:///Users/steven/PYTHON_MARKETPLACE_MASTER/My-Deep-Proprietary/MERGED_UNIFIED.md). |
| [`deeptutor-mimic/`](deeptutor-mimic/) | **Symlink** → `My-Deep-Proprietary` (same checkout). |
| [`MY_SETUP/`](MY_SETUP/) | **Thin pointer** + **`deeptutor-mimic/`** symlink → `My-Deep-Proprietary`. Hub files merged into proprietary; re-sync from `PYTHON_MARKETPLACE_MASTER/MY_SETUP` if you refresh the marketplace copy. |

**Canonical DeepTutor checkout:** `/Users/steven/Downloads/Compressed/DeepTutor-main`

**Concepts — horizontal / vertical:**  
[Flows + quick examples](HORIZONTAL_VERTICAL_FLOWS_AND_EXAMPLES.md) · [Horizontal — comprehensive](HORIZONTAL_LOGIC_COMPREHENSIVE.md) · [Vertical — comprehensive](VERTICAL_LOGIC_COMPREHENSIVE.md) · [Factor matrix](file:///Users/steven/PYTHON_MARKETPLACE_MASTER/Guides/HORIZONTAL_VERTICAL_FACTORS.md)

**Agent path inventory:** [Index + review](AGENT_ECOSYSTEM_INDEX_AND_REVIEW.md) · [path list `_agent_paths_inventory.txt`](./_agent_paths_inventory.txt) (203 paths, classified) · [Subset compare — “this is / that is”](AGENT_SUBSET_PATHS_COMPARE.md) · [CSV gap analysis (`docs-05-09-21:57.csv`)](AGENT_PATHS_DOCS_CSV_GAP_ANALYSIS.md) · [Dotfolders & dotfiles (Cursor, Claude, Codex, …)](AGENT_DOTFILES_AND_DOTFOLDERS.md) · [Comprehensive rollup CSV](AGENT_ECOSYSTEM_COMPREHENSIVE_2026-05-09.csv) (`path`, `path_type`, `taxonomy_tags`, drift notes, `secrets_risk`).
