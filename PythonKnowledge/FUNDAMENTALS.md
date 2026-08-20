# Fundamentals — marketplace, DeepTutor, and your AI control plane

**Scope:** How the big pieces connect on this Mac. For architecture depth, follow links—don’t duplicate them here.

---

## 1. Reference ledger (canonical paths)

```text
+ MARKETPLACE_ROOT=/Users/steven/PYTHON_MARKETPLACE_MASTER
+ MY_SETUP=MARKETPLACE_ROOT/MY_SETUP
+ GUIDES=MARKETPLACE_ROOT/Guides
+ DOCUMENTATION=MARKETPLACE_ROOT/DOCUMENTATION
+ DEEPTUTOR_CHECKOUT=/Users/steven/Downloads/Compressed/DeepTutor-main
+ MY_DEEP_PROPRIETARY=MARKETPLACE_ROOT/My-Deep-Proprietary
+ AVATAR_HUB=/Users/steven/AvaTar-ArTs
+ MY_SUPREMEPOWERS=/Users/steven/my-supremepowers
+ HOME_QWEN=/Users/steven/.qwen
+ HOME_GEMINI=/Users/steven/.gemini
+ DEEPTUTOR_MIMIC=MARKETPLACE_ROOT/MY_SETUP/deeptutor-mimic
+ DEEPTUTOR_STANDALONE=DEEPTUTOR_MIMIC
```

---

## 2. Five fundamentals

1. **Marketplace (`PYTHON_MARKETPLACE_MASTER`)** — Inventory, SKUs, category pools, HTML/CSV companions, and **`DOCUMENTATION/`** churn logs. Deep dive economics live here.
2. **Guides (`Guides/`)** — Long-lived **cross-repo** references (DeepTutor Mermaid atlas, Qwen/Gemini home review). Prefer **`Guides/`** over burying the same material inside one product’s `docs/`.
3. **DeepTutor** — **`DEEPTUTOR_CHECKOUT`** = upstream-style tree; **`MY_DEEP_PROPRIETARY`** = full replica + overlay. Same patterns, different legal/ops envelope.
4. **Hub (`AvaTar-ArTs`)** — Thin map: symlinks under `projects/`, **`PROJECTS.md`**, **`HOME-REVIEW.md`** — not the heavyweight product tree.
5. **Daily AI hosts (`~/.qwen`, `~/.gemini`) + `my-supremepowers`** — **How you work** (flows, skills, layers). **`SOURCE_OF_TRUTH_AND_LAYERS`** in `~/.qwen/docs/` explains which copy of a skill is canonical.

---

## 3. Where to read next

| Question | Go to |
|----------|--------|
| DeepTutor flows, Mermaid, framework reuse | `GUIDES/DeepTutor-ARCHITECTURE_MAP_MERMAID_AND_EXPLORATION.md` |
| `~/.qwen` / `~/.gemini` helpful docs & sensitivity | `GUIDES/QWEN_AND_GEMINI_HOME_REVIEW_2026-05-09.md` |
| DeepTutor vs proprietary parity | `DOCUMENTATION/DEEPTUTOR_TREE_FOCUS_UPSTREAM_VS_PROPRIETARY_2026-05-09.md` |
| Multi-root ecosystem snapshot | `DOCUMENTATION/ECOSYSTEM_DEEP_REVIEW_MULTIROOT_2026-05-09.md` |
| Hub symlink table | `AVATAR_HUB/PROJECTS.md` |
| Trendshift-style agentic mimic map (local parity) | **MY_SETUP/** [`AGENTIC_LOCAL_VS_TRENDSHIFT.md`](./AGENTIC_LOCAL_VS_TRENDSHIFT.md) |
| DeepTutor standalone tree + mimic helpers | **MY_SETUP/** [`deeptutor-mimic/MIMIC_OVERVIEW.md`](./deeptutor-mimic/MIMIC_OVERVIEW.md) |
| Generic phased how-to template (any repo) | **MY_SETUP/** [`WALKTHROUGH_PATTERN.md`](./WALKTHROUGH_PATTERN.md) |

---

## 4. Editing rules (for Guides + this folder)

- **Reference paths / aliases:** append with fenced `-` / `+` ledgers (see **§18–§23** in the DeepTutor atlas).
- **Single section clarity:** replacing **one** § or diagram wholesale is allowed when it reads better.
- **Secrets:** never commit `.env`, OAuth JSON, or API exports into **`MY_SETUP`** or public markdown.

---

## 5. Optional commands

```bash
ls "$HOME/PYTHON_MARKETPLACE_MASTER/Guides"
ls "$HOME/PYTHON_MARKETPLACE_MASTER/MY_SETUP"
```

---

## 6. Trendshift radar vs local depth

[Trendshift](https://trendshift.io/) ranks **rising GitHub engagement** across topics (**AI agent**, **AI skills**, **MCP**, **infrastructure**, etc.). Your machine often already implements **the same capability classes** under different packaging: DeepTutor-class apps in **`MY_DEEP_PROPRIETARY`**, skills orchestration in **`supremepowers` / `my-supremepowers` / `~/.qwen` / `~/.gemini`**, SKU density in **`PYTHON_MARKETPLACE_MASTER`**.

For a **row-by-row mimic map** (DeepTutor + Trendshift archetypes ↔ disk paths), use **[`AGENTIC_LOCAL_VS_TRENDSHIFT.md`](./AGENTIC_LOCAL_VS_TRENDSHIFT.md)**.

---

*Expand this file by appending new `+` lines to §1 or new numbered sections below—keep §2 “five fundamentals” aligned when your mental model changes.*
