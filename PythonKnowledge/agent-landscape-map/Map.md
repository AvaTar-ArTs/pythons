# Agent Landscape Mind-Map

## Overview
A functional map of the agent/skill ecosystem, aligned with canonical architectural documentation.

## Data Nodes

### 1. Horizontal Layer (Workflow/Tools)
- `~/.supremepower` (Canonical: Workflow framework, hooks, personas)
- `~/.gemini` (Canonical: Policies, history, core organizational assets)
- `~/.cline` / `~/.cursor` / `~/.qwen` (Runtime Contexts)

### 2. Vertical Layer (Product Stacks)
- `~/my-supremepowers` (Framework/Product stack development)
    - **Agents Inventory (Partial):**
        - `technical-writer.md`
        - `task-management.md`
        - `backend-architect.md`
        - `code-reviewer.md`
        - `tree-explorer.md`
        - `rule-definition.md`
        - `performance-engineer.md`
        - `filesystem-inventory.md`
        - `path-list-analyzer.md`
        - `notebooklm-enhancement-advisor.md`
        - `documentation-manager.md`
        - `ice-tracker-assistant.md`
        - `ecosystem-analyzer.md`
        - `testing-specialist.md`
        - `agent-creation-guidance.md`
- `PYTHON_MARKETPLACE_MASTER/` (Bundle/Upstream canonicals)
- `Downloads/Compressed/DeepTutor-main/` (DeepTutor product root)

## Mapping Logic
- **Horizontal** components (skills, agents, hooks) are dynamically loaded by **Hosts** (IDE/CLI agents).
- **Vertical** stacks (product code) are developed using the Horizontal tools.
- **`~/Guides/`** serves as the central documentation ledger.


---

## Functional Taxonomy (Capability-Based)

*Added [2026-05-14]: Concepts extracted from ~/.cline/CLINE.md and operational patterns.*

| Capability Concept | Operational Intent | Key Artifacts / Hubs |
| :--- | :--- | :--- |
| **Retention** | Ensuring knowledge/work never dies. | chat-history/, memory/ |
| **Reflection** | Improving the agent via self-analysis. | agents/self-evolution.md, memory/MEMORY.md |
| **Automation** | Orchestrating runtime lifecycle. | cron, launchd, scripts/ |
| **Discovery** | Searching across siloed platforms. | ai-search, ai-stats |

---

## Evolutionary Narrative

*Added [2026-05-14]: Evolving from a structural audit to a functional intent narrative.*

Your agent landscape is an emergent system. It began as functional silos (IDE context, product stacks), and is now transitioning toward a unified control plane. The infrastructure identified in the initial audits (e.g., ~/.cline, ~/.supremepower) are not mere storage—they are the *operational memory* of your agentic evolution. This map serves as the ledger for that evolution: tracing how independent tools developed their own 'minds' (agents/skills) and identifying the path toward centralizing intent without destroying local functionality.

### Agent: code-reviewer
- **Role:** Senior QA / Code Reviewer
- **Context:** ~/.cline (Horizontal)
- **Capability:** Quality Assurance & Governance
- **Operational Intent:** Categorizes findings into Critical, Important, and Suggestion levels to enforce architectural and quality standards.

## Scan Methodology

*Added [2026-05-14]: Insights from scan script analysis.*

The inventory generation is governed by all_for_csv.py, which uses a strict extension-to-category mapping (e.g., .md -> Doc, .sh -> Script) and broad regex exclusions defined in exclude_patterns.py to skip noise (build artifacts, version control, OS temp files). This ensures the landscape map reflects intended operational assets rather than system bloat.

---

## Evolutionary Taxonomy: Horizontal vs. Vertical

*Added [2026-05-14]: Re-structured based on validated architectural definitions.*

Following the definitions established in HORIZONTAL_VERTICAL_FACTORS.md, the landscape has been bifurcated:

### 1. Horizontal Layer (Breadth/Reuse)
*Assets intended to apply across many repositories, teams, or hosts.*
- **Frameworks/Habits:** ~/.supremepower, ~/.gemini (Policies, personas).
- **Runtime Tools:** ~/.cline, ~/.codex (CLI/IDE context).

### 2. Vertical Layer (Depth/Coherence)
*Assets wired through one product’s stack (UI -> API -> Domain).* 
- **Product Stacks:** ~/my-supremepowers, DeepTutor (Upstream canonicals).
- **Boundaries:** These are defined by repo/deployment unit, not shared habits.