# DeepTutor — How-To (local setup)

**Using-superpowers:** **Structured walkthrough** (phases, no guessing). Matches upstream [`README.md`](file:///Users/steven/Downloads/Compressed/DeepTutor-main/README.md) **Option A / B / C**. Use this pattern for **any** serious local setup doc: prerequisites → enter tree → env → install profile → secrets → run → verify → optional Docker.

**Standalone copy (recommended hub):**

```text
+ DEEPTUTOR_STANDALONE=/Users/steven/PYTHON_MARKETPLACE_MASTER/MY_SETUP/deeptutor-mimic
```

**Other checkouts on this machine:**

```text
+ DEEPTUTOR_DOWNLOADS=/Users/steven/Downloads/Compressed/DeepTutor-main
+ MY_DEEP_PROPRIETARY=/Users/steven/PYTHON_MARKETPLACE_MASTER/My-Deep-Proprietary
```

Hub docs: **[deeptutor-mimic/MIMIC_OVERVIEW.md](./deeptutor-mimic/MIMIC_OVERVIEW.md)** — phased steps in **[deeptutor-mimic/RUNBOOK.md](./deeptutor-mimic/RUNBOOK.md)** (upstream **[README.md](./deeptutor-mimic/README.md)** remains the product readme).

---

## 0. Prerequisites (once)

| Check | Requirement |
|--------|--------------|
| `python3 --version` | **Python 3.11+** |
| `node --version` | **Node 20.9+** (local **web** UI) |
| `npm --version` | Comes with Node |
| Money/key | At least one **LLM API key** (tour or `.env`) |

Windows: Visual Studio Build Tools per upstream README.

---

## 1. Go to the project

**Standalone** (full tree under `MY_SETUP`):

```bash
cd /Users/steven/PYTHON_MARKETPLACE_MASTER/MY_SETUP/deeptutor-mimic
```

Or another checkout:

```bash
cd /Users/steven/Downloads/Compressed/DeepTutor-main
# or
cd /Users/steven/PYTHON_MARKETPLACE_MASTER/My-Deep-Proprietary
```

(Optional: `python scripts/update.py` when using git.)

---

## 2. Create and activate a Python environment

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
```

(Windows / Conda variants: same as repo [`How-To.md`](file:///Users/steven/Downloads/Compressed/DeepTutor-main/How-To.md) in the checkout.)

---

## 3. Install software — choose **one** path

### Path **A — Setup Tour** (recommended)

```bash
python scripts/start_tour.py
```

Pick **Web app (recommended)** → then **step 5**.

### Path **B — Manual**

```bash
python -m pip install -e ".[server]"
```

Optional:

```bash
python -m pip install -e ".[tutorbot]"
# python -m pip install -e ".[tutorbot,matrix]"
# python -m pip install -e ".[math-animator]"
# python -m pip install -e ".[all]"
```

```bash
cd web && npm install && cd ..
```

---

## 4. Configure `.env`

```bash
cp .env.example .env
```

Chat: `LLM_BINDING`, `LLM_MODEL`, `LLM_API_KEY`, `LLM_HOST`. RAG: `EMBEDDING_*`; **`EMBEDDING_HOST`** = full embeddings URL (v1.3.0+). See **`.env.example`** at the repo root (standalone copy includes it). Optional duplicate: **[deeptutor-mimic/bundled/env.example](./deeptutor-mimic/bundled/env.example)**.

Ports default: **8001** / **3782**.

---

## 5. Start the app (browser UI)

```bash
python scripts/start_web.py
```

→ [http://localhost:3782](http://localhost:3782) (unless ports changed).

Split: `python -m deeptutor.api.run_server` and `cd web && npm run dev -- -p 3782`.

**Via `mimic-scripts`** (defaults `DEEPTUTOR_ROOT` to the standalone folder):

```bash
cd ~/PYTHON_MARKETPLACE_MASTER/MY_SETUP/deeptutor-mimic
source mimic-scripts/set-root.sh
./mimic-scripts/start-full-stack.sh
```

---

## 6. Quick CLI sanity check (optional)

```bash
deeptutor run chat "Say OK in one word."
```

[`SKILL.md`](file:///Users/steven/Downloads/Compressed/DeepTutor-main/SKILL.md), [`AGENTS.md`](file:///Users/steven/Downloads/Compressed/DeepTutor-main/AGENTS.md) in the active repo root.

---

## 7. Docker instead (Option C)

```bash
docker compose -f docker-compose.ghcr.yml up -d
# or
docker compose up -d
```

---

## Mental model

| Layer | Role |
|------|------|
| `deeptutor/` | Backend + orchestration + APIs |
| `deeptutor_cli/` | CLI |
| `web/` | Next.js UI |
| `.env` | Providers, ports, auth |
| `scripts/start_web.py` | Backend + frontend |

Architecture atlas: `PYTHON_MARKETPLACE_MASTER/Guides/DeepTutor-ARCHITECTURE_MAP_MERMAID_AND_EXPLORATION.md`.

---

## Related `MY_SETUP` docs

| Doc | Purpose |
|-----|---------|
| [WALKTHROUGH_PATTERN.md](./WALKTHROUGH_PATTERN.md) | Generic phased-doc pattern (reuse for non–DeepTutor projects) |
| [FUNDAMENTALS.md](./FUNDAMENTALS.md) | Path ledger |
| [deeptutor-mimic/RUNBOOK.md](./deeptutor-mimic/RUNBOOK.md) | Full phased steps + mimic shortcuts |
