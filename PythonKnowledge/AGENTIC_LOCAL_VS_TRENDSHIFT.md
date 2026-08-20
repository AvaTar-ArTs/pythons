# Local agentic stack vs [Trendshift](https://trendshift.io/) patterns — mimic map

**Intent:** Use [Trendshift](https://trendshift.io/) as a **radar** (topics like **AI agent**, **AI skills**, **AI coding assistant**, **AI infrastructure**, daily engagement rankings)—then map each **capability class** to what you **already run locally**, including DeepTutor-style agent-native tutoring. Goal is **functional mimicry** and honest gap spotting, not copying repos blindly.

```text
+ TRENDSHIFT=https://trendshift.io/
+ DEEPTUTOR_ON_TRENDSHIFT=https://trendshift.io/repositories/17099
+ MARKETPLACE_ROOT=/Users/steven/PYTHON_MARKETPLACE_MASTER
```

---

## 1. How to read this doc

| Layer | Role |
|-------|------|
| **Trendshift** | Discover **what the ecosystem is amplifying** (skills repos, MCP stacks, harnesses, infra). |
| **Your disk** | Often holds **multiple overlapping implementations** (`supremepowers`, `my-supremepowers`, `~/.qwen`, `~/.gemini`, marketplace pools, DeepTutor forks). |
| **Mimic** | Reproduce **behaviors**: tool registry + orchestration + skills + MCP + UI—not star counts. |

---

## 2. Capability classes ↔ local anchors

Rough alignment with tags you see on [Trendshift](https://trendshift.io/) listings (examples cited as archetypes, not exhaustive).

| Trendshift-style theme | What “good” looks like | Your local analogue (where to look first) |
|------------------------|-------------------------|-------------------------------------------|
| **Agent-native app** (tutoring, RAG, multi-mode UI) | One product: adapters → orchestrator → tools/capabilities | **`MY_DEEP_PROPRIETARY`** / **`DEEPTUTOR_CHECKOUT`** + `Guides/DeepTutor-ARCHITECTURE_MAP_MERMAID_AND_EXPLORATION.md`; public signal e.g. [HKUDS/DeepTutor on Trendshift](https://trendshift.io/repositories/17099). |
| **Skills frameworks** | Invoke gated workflows (brainstorm, plan, TDD, debug) | **`~/supremepowers`** (product), **`~/my-supremepowers`** (wide mirror), **`~/.qwen/skills/superpowers-*`**, **`~/.gemini/extensions/**`/top-level `skills/`; Trendshift examples include [obra/superpowers](https://github.com/obra/superpowers), [anthropics/skills](https://github.com/anthropics/skills). |
| **Agent harness / multi-agent workspace** | Sessions, tools, extensions | **Gemini CLI** tree (`~/.gemini`), **Qwen** hosts (`~/.qwen`), **Cursor**; Trendshift examples include [lobehub/lobehub](https://github.com/lobehub/lobehub) as “agent teammate” framing—you spread similar concerns across hosts + marketplace docs. |
| **Spec-driven / planning kits** | Plans before implementation | SupremePower **writing-plans**, **executing-plans**, Compound **ce-plan** patterns; archetype [github/spec-kit](https://github.com/github/spec-kit). |
| **MCP & data tools** | DB/API bridges for agents | **`~/.gemini/extensions/`** (e.g. MCP DB packs), Cursor MCP config—Trendshift often surfaces MCP-tagged repos. |
| **Design / UX intelligence for agents** | DESIGN.md-style system prompts | VoltAgent-style [**awesome-design-md**](https://github.com/VoltAgent/awesome-design-md) archetype ↔ your **cursor rules**, marketplace web generators, `n8n_workflows` content pipelines. |
| **Persistent agent memory** | Durable recall across sessions | DeepTutor **memory** surfaces + host-specific memory features; archetype [agentmemory](https://github.com/rohitg00/agentmemory)—audit whether you want explicit memory MVP vs many implicit logs (`~/.codex`, Cursor history). |
| **Script / SKU empire** | Many small sellable units | **`PYTHON_MARKETPLACE_MASTER`** category pools (`01_AI_LLM_TOOLS`, …)—different shape than one DeepTutor, same **commercial plane**. |

---

## 3. DeepTutor-specific mimic checklist

Use when you want **parity with DeepTutor’s mechanics** inside your own deliverables:

1. **Single turn context object** → mirror `UnifiedContext` idea (see DeepTutor atlas §9, §15).
2. **Registry + declared tools** → manifest ↔ runtime validation (DeepTutor startup drift check).
3. **Streaming bus** → SSE/WS/JSONL progress for long jobs (marketplace scripts rarely do this—upgrade path).
4. **Agent-operable surface** → root **`SKILL.md`** pattern for “how an agent drives the CLI.”
5. **Optional auth / multi-user** → only if you ship hosted; otherwise skip complexity.

---

## 4. Operating rhythm (Trendshift → local)

1. **Scan** [Trendshift](https://trendshift.io/) weekly or monthly—note **tags** (#AI agent, #AI skills, #AI infrastructure), not every repo.
2. **Classify** each interesting repo into the **table in §2** (one primary column).
3. **Diff:** Do you already cover that column? If yes, **document** the path (append `+` line to **`FUNDAMENTALS.md` §1** ledger). If no, **one** experiment branch or marketplace SKU—not fifteen clones.
4. **Canonical edits:** follow **`~/.qwen/docs/SOURCE_OF_TRUTH_AND_LAYERS.md`** so new skills land in the right layer.

---

## 5. Gap ledger (append yourself)

When Trendshift surfaces something you **don’t** cover, add a line—do not delete prior rows.

```text
+ (example) gap: dedicated agent-memory service — optional future SKU or MCP
```

---

*This file is strategy glue between **MY_SETUP**, **Guides/**, and external discovery—not a mirror of Trendshift data.*
