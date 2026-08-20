# Horizontal vs vertical logic — flows, Mermaid, and examples

**Path:** `/Users/steven/Guides/HORIZONTAL_VERTICAL_FLOWS_AND_EXAMPLES.md`

**Deep dives:** [`HORIZONTAL_LOGIC_COMPREHENSIVE.md`](./HORIZONTAL_LOGIC_COMPREHENSIVE.md) · [`VERTICAL_LOGIC_COMPREHENSIVE.md`](./VERTICAL_LOGIC_COMPREHENSIVE.md)  
**Companion (factor tables and long analysis):** [`PYTHON_MARKETPLACE_MASTER/Guides/HORIZONTAL_VERTICAL_FACTORS.md`](file:///Users/steven/PYTHON_MARKETPLACE_MASTER/Guides/HORIZONTAL_VERTICAL_FACTORS.md)  
**Cross-map (SupremePower × DeepTutor):** [`PYTHON_MARKETPLACE_MASTER/Guides/SUPREMEPOWERS_AND_DEEPTUTOR_CROSS_MAP.md`](file:///Users/steven/PYTHON_MARKETPLACE_MASTER/Guides/SUPREMEPOWERS_AND_DEEPTUTOR_CROSS_MAP.md)

This file is the **operational lens**: how horizontal and vertical **logic** show up in decisions, runtime, and tooling — with **diagrams** and **worked examples**. It does not replace the factor matrix; it **routes** you to it when you need depth.

---

## 1. Two sentences

- **Horizontal logic** answers: *“What should stay true no matter which repo or host I am in?”* — habits, skills, patterns, MCP contracts, checklists, naming rules.
- **Vertical logic** answers: *“What must stay true inside this one product boundary so the stack does not lie?”* — orchestration, types, persistence, auth, migrations, one deployable unit.

---

## 2. One picture — breadth vs depth

```mermaid
flowchart LR
  subgraph H ["Horizontal plane"]
    A1["Skill A"]
    A2["Skill B"]
    A3["Agent rule"]
    A4["MCP tool"]
    A1 --- A2 --- A3 --- A4
  end

  subgraph V ["Vertical stack (one product)"]
    direction TB
    B1["UI / CLI"]
    B2["API + WS"]
    B3["Orchestrator"]
    B4["Domain + data"]
    B1 --> B2 --> B3 --> B4
  end

  H -->|"informs how you build"| V
  V -->|"produces lessons you lift"| H
```

**How to read it:** Horizontal items **fan out** across many contexts. Vertical items **stack** inside one boundary. Good teams **spiral**: vertical work produces horizontal lessons; horizontal discipline speeds vertical delivery.

---

## 3. Where “logic” actually applies

```mermaid
flowchart TB
  subgraph apply ["Where decisions bind"]
    D1["Strategy: what we sell / who we serve"]
    D2["Architecture: boundaries and contracts"]
    D3["Process: how we change code safely"]
    D4["Runtime: what executes on a request"]
  end

  D1 --> D2 --> D3 --> D4

  Hnote["Horizontal bias: principles portable across repos"]
  Vnote["Vertical bias: invariants inside one deployable"]

  D1 -.-> Hnote
  D4 -.-> Vnote
```

| Layer | Horizontal logic tends to… | Vertical logic tends to… |
|-------|-----------------------------|-----------------------------|
| **Strategy** | Reuse positioning (“agent-native”, “verification-first”) | Pick one product’s scope and roadmap |
| **Architecture** | Plugin shapes, MCP tool schemas, façade pattern as *idea* | `UnifiedContext`, registries, DB schema, Docker compose |
| **Process** | Brainstorm → plan → verify skills | CI, migrations, release notes, API versioning |
| **Runtime** | Host picks which skill runs | App picks capability + tools for one turn |

---

## 4. Request / turn flow — vertical spine (example: DeepTutor)

Vertical logic **binds** at runtime: one message becomes one coherent execution path inside the product.

```mermaid
sequenceDiagram
  participant U as User / client
  participant A as Adapter (CLI / HTTP / WS)
  participant F as Facade (DeepTutorApp)
  participant O as ChatOrchestrator
  participant C as Capability
  participant T as Tools + services

  U->>A: message + session context
  A->>F: TurnRequest-shaped payload
  F->>O: handle(UnifiedContext)
  O->>C: run(context, stream)
  C->>T: tool calls, RAG, LLM
  T-->>C: structured results
  C-->>U: streamed events
```

**Vertical invariants here:** one orchestrator choke point; manifests must match `ToolRegistry`; session and KB semantics are **owned by this app**, not by the IDE.

---

## 5. Same human hour — horizontal dispatch (example: host + skills)

Horizontal logic **does not** own the tutoring stack; it **coordinates how many stacks get touched** with consistent quality.

```mermaid
flowchart TB
  subgraph host ["Host (Cursor / Claude Code / CLI)"]
    R["Rules + skills index"]
    P["Plan / verify habits"]
  end

  subgraph repos ["Many repos over time"]
    X1["Repo X"]
    X2["Repo Y"]
    X3["Repo Z"]
  end

  R --> P
  P --> X1
  P --> X2
  P --> X3
```

**Horizontal invariants here:** same verification bar before “done”; same pattern for MCP tool naming; same “read AGENTS.md before edit” habit — **each repo may implement differently**, the **habit** is portable.

---

## 6. Decision flow — “is this change horizontal or vertical?”

```mermaid
flowchart TD
  Q1{"Does it import product types\nor touch deploy artifacts?"}
  Q1 -->|yes| V["Treat as vertical:\nrepo tests, migrations, API"]
  Q1 -->|no| Q2{"Should every future repo\nget the same behavior?"}
  Q2 -->|yes| H["Treat as horizontal:\nskill, rule, template, hook"]
  Q2 -->|maybe| B["Hybrid:\nlibrary package or shared submodule\nwith its own vertical CI"]
```

---

## 7. Interaction — horizontal guardrails on vertical work

```mermaid
flowchart LR
  subgraph Hg ["Horizontal guards"]
    G1["Code review checklist"]
    G2["Security: no secrets in docs"]
    G3["TDD / verify-before-done skill"]
  end

  subgraph Vw ["Vertical work unit"]
    W1["Feature branch"]
    W2["Tests + build"]
    W3["Release"]
  end

  G1 --> W1
  G3 --> W2
  G2 --> W3
```

**Example:** Adding a DeepTutor capability is **vertical**; running **verification-before-completion** before you merge is **horizontal** — it does not live inside DeepTutor’s wheelhouse, but it **shapes** how safely you change vertical code.

---

## 8. Worked examples (concrete)

| Situation | Mostly horizontal | Mostly vertical |
|-----------|---------------------|------------------|
| **New “always grep before refactor” habit** | Skill or rule in `my-supremepowers` / Cursor rules | N/A |
| **New DeepTutor capability `foo`** | Optional: document pattern in Guides atlas | `deeptutor/capabilities/`, manifests, `validate_tool_consistency` |
| **MCP server wrapping an API** | Tool schema style, naming, “how to document tools” | Actual server code, auth, rate limits in **that** server repo |
| **`MY_SETUP` fundamentals + ledgers** | Canonical paths, how marketplace connects | N/A (meta-repo layout, not one app runtime) |
| **TutorBot channel** | “Bots are optional extras” as a pattern doc | `deeptutor/tutorbot/`, deps in `pyproject.toml` extras |
| **Copy `SKILL.md` into another product** | Same *shape* of operator doc | Content must be rewritten for **that** product’s CLI |
| **Docker compose for DeepTutor** | “Always use `.env.example` as template” rule | `docker-compose.yml`, healthchecks, ports in **this** repo |

---

## 9. Anti-patterns (quick)

| Anti-pattern | Why it hurts |
|--------------|--------------|
| **Vertical sprawl in rules** | Cursor rules that import product-specific paths break when you switch repos. |
| **Horizontal sermon in hot paths** | 500-line “how to think” inside `orchestrator.py` — belongs in docs/skills, not runtime. |
| **Two sources of truth** | Same policy written in **both** a skill and `CONTRIBUTING.md` without sync — pick one canonical and link. |
| **Horizontal CI theater** | Pre-commit everywhere but **no** tests on the product — vertical quality still fails. |

---

## 10. When to open which doc

| Need | Open |
|------|------|
| **Matrices, factors, anti-patterns in depth** | `HORIZONTAL_VERTICAL_FACTORS.md` |
| **SupremePower vs DeepTutor mapping** | `SUPREMEPOWERS_AND_DEEPTUTOR_CROSS_MAP.md` |
| **Flows + examples + decision lens (this file)** | `HORIZONTAL_VERTICAL_FLOWS_AND_EXAMPLES.md` |
| **DeepTutor runtime wiring** | `DeepTutor-ARCHITECTURE_MAP_MERMAID_AND_EXPLORATION.md` |

---

*Edit this file for new diagrams and examples; extend the factor matrix in `HORIZONTAL_VERTICAL_FACTORS.md` when you add new **dimensions**, not duplicate paragraphs here.*
