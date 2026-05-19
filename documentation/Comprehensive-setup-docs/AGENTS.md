# Repository Guidelines

## Project Structure & Module Organization
- Source code: `src/` with absolute imports.
- Tests: `tests/` mirrors `src/`; files `test_*.py`.
- Scripts/CLIs: `bin/` executable entry points.
- Config: `.env`, `pyproject.toml`, `ruff.toml`, `pytest.ini` at repo root.
- Assets: `assets/` (data), `examples/` (usage samples).

## Build, Test, and Development Commands
- Setup venv: `python -m venv .venv && source .venv/bin/activate`
- Install (dev): `pip install -U pip && pip install -e .[dev]`
- Lint/format: `ruff check .` and `ruff format .`
- Type check: `mypy src`
- Tests: `pytest -q` (use `--cov=src --cov-report=term-missing` for coverage)
- Run module: `python -m <package> [...args]`
- Codex CLI: `codex --provider openai` (auto-loads `.env`).

## Coding Style & Naming Conventions
- Python ≥ 3.10; prefer type hints (`from __future__ import annotations`).
- Indentation: 4 spaces; max line length 100.
- Naming: modules/functions `snake_case`, classes `PascalCase`, constants `UPPER_SNAKE`.
- Imports: stdlib → third‑party → local; avoid relative imports.
- Tools: Ruff (lint/format), MyPy (types). `ruff format` is Black‑compatible.

## Testing Guidelines
- Framework: `pytest` in `tests/` mirroring `src/`.
- Naming: files `test_*.py`; test functions `test_*`; use fixtures.
- Coverage: ≥ 90% on changed code/paths; add regression tests for fixes.
- Run locally before PRs: `pytest -q` (optionally with coverage flags).

## Commit & Pull Request Guidelines
- Commits: imperative, concise. Example: `feat(api): add async client`.
- Scopes: `feat`, `fix`, `docs`, `chore`, `refactor`, `test`, `perf`.
- PRs: summary, rationale, linked issues (`Closes #123`), and evidence (logs/screens). Confirm lint, types, tests.

## Security & Configuration Tips
- Do not commit secrets; use `.env` locally, env vars in CI.
- Providers: switch with `--provider` (e.g., `openrouter|azure|ollama|mistral|groq|deepseek|xai|gemini|arceeai`). Set API keys in `.env` or config.
- Validate inputs, least‑privilege file access, avoid executing untrusted code.

## Agent-Specific Notes
- Uses Codex CLI; `.env` auto-loads via dotenv/config. Prefer `--provider` to switch models. Keep scripts idempotent and safe for sandboxed runs.
