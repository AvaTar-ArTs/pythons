# Repository Guidelines

## Project Structure & Module Organization
- Core Python scripts live in the repo root; most are single-purpose utilities named for their task (e.g., `batch-image-processor.py`, `instagram-*`, `openai-*`).
- Supporting assets and reports sit in underscored folders: `_analysis`, `_archives`, `_docs`, `_reports`, `_library`. Temporary caches land in `__pycache__`.
- Planning and status CSV/MD files (e.g., `FINAL_RENAME_PLAN_*.csv`, `SESSION_*`) track rename operations and audits; leave them intact.

## Build, Test, and Development Commands
- Run scripts directly with Python 3: `python script_name.py --help` to see options before executing.
- For lint/style checks (if available locally): `python -m pip install -r requirements-py.txt` then `python -m pip install black isort ruff` and run `ruff .` or `black --check .`.
- No central build; most tools are standalone. Dry-run flags are common (`--dry-run`, `--preview`)—prefer them before touching files.

## Coding Style & Naming Conventions
- Python 3.x, 4-space indentation, imports grouped stdlib/third-party/local.
- File naming follows action-oriented, hyphen-separated patterns (`verb-noun.py`); keep new scripts consistent.
- Favor pathlib over os.path; prefer argparse click-style CLIs with clear defaults. Include `if __name__ == "__main__":` entrypoints.
- Keep functions small, with explicit parameters; avoid hardcoded paths—accept CLI args or env vars.

## Testing Guidelines
- There is no unified test suite; validate changes with targeted script runs on sample data and dry-runs where provided.
- When adding tests, use `pytest` with concise names (`tests/test_<script>.py`) and include fixtures for file-based workflows.

## Commit & Pull Request Guidelines
- Write concise, imperative commit messages (`add rename helper`, `fix instagram pagination`). Group related changes per commit.
- PRs should describe scope, risks, and validation (commands run, sample outputs). Include before/after notes for renamers or movers and call out any destructive operations.

## Security & Configuration Tips
- Secrets belong in `.env`; scripts load it automatically (`dotenv/config`). Do not commit keys or tokens.
- Treat bulk rename/move scripts cautiously—run previews and keep generated CSV/MD plans for traceability. EOF
