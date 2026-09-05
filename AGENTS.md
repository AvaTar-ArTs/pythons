# Repository Guidelines

This repository is a large, content-organized collection of standalone Python automation, analysis, media, API, and file-management scripts. The installable root package is a small launcher; most scripts and datasets remain checkout-local and may have independent dependencies.

## Project Structure & Module Organization
- Root contains overview docs and analysis reports; keep new docs in `documentation/` when possible.
- Domain scripts live in `apis/`, `data_processing/`, `file_operations/`, `media_processing/`, and `tools/`.
- Specialized collections include `AI_CONTENT/`, `AUTOMATION_BOTS/`, `seo_marketing/`, `websites/`, and `llm/`.
- Standalone apps and vendor code live in `projects/`; these may carry their own dependencies and test suites.
- Generated outputs and datasets are typically stored in `analysis/`, `data/`, `content/`, and `archives/`.
- Ad hoc tests and debugging helpers live in `testing/` or alongside the feature area. The launcher tests are in `tests/test_cli.py`.
- Use `README.md`, `INDEX.md`, `QUICK_REFERENCE.md`, and `MIGRATION_GUIDE.md` to navigate the content-based organization; filenames are not always reliable indicators of purpose.

## Build, Test, and Development Commands
- Use Python 3.9–3.12 (`pyproject.toml` requires `>=3.9,<3.13`). Create an environment with `python -m venv .venv && source .venv/bin/activate`.
- Install launcher plus development tools with `python -m pip install -e '.[dev]'`; CI installs the test-only extra with `python -m pip install '.[test]'`.
- Run the verified root suite with `python -m pytest tests` (pytest is configured with `testpaths = ["tests"]` and verbose output). Scope the launcher suite with `python -m pytest tests/test_cli.py`.
- The canonical launcher is `pythons_sort.py`; `file_operations/pythons_sort.py` delegates to it. `python file_operations/pythons_sort.py --help` is a valid compatibility invocation.
- List scripts with `pythons-sort info --all` or `python pythons_sort.py info --all`. Narrow discovery with `pythons-sort info --category scanners`.
- Preview or run an exact checkout-relative script with `pythons-sort run --dry-run path/to/script.py -- argument --option value` or `pythons-sort run path/to/script.py -- argument --option value`.
- An installed launcher can target another checkout with `pythons-sort --repository /path/to/pythons info --all`; `PYTHONS_REPOSITORY` provides the same default.
- Run the configured quality checks with `pre-commit run --all-files`. Hooks include trailing-whitespace/end-of-file/YAML/JSON checks, Black, Flake8, isort, Bandit, mypy, mdformat, and detect-secrets.

## Coding Style & Naming Conventions
- Follow `.editorconfig`: UTF-8, 4-space Python indents, LF endings, final newlines, and trimmed trailing whitespace; JSON/YAML use 2-space indents. Markdown intentionally permits trailing whitespace.
- Black is configured with line length 88; Flake8 and isort hooks use line length 100, with Flake8 ignoring E203 and W503. isort uses the Black profile.
- Prefer `snake_case.py` for new scripts and `test_*.py` for pytest tests; avoid spaces in filenames.
- Keep scripts focused and self-contained; place shared helpers in the closest relevant module folder. Existing scripts commonly use a top-level entry point guarded by `if __name__ == "__main__"`.
- For versioned files such as `script.py`, `script_1.py`, and `script_v2.py`, inspect both implementations and comments before selecting one; version numbers do not guarantee superiority.

## Testing Guidelines
- Pytest is the default runner; the top-level `tests/` directory covers launcher behavior, argument forwarding, exit codes, dry-run safety, path validation, and both entry points. Fixtures use temporary directories and do not run cleanup/renaming utilities.
- Some subprojects include their own suites, such as `python -m pytest axolotl-main/tests`; install that subproject's dependencies before using its tests.
- Add regression coverage next to the module or subproject it validates.

## Commit & Pull Request Guidelines
- Commit history uses short, imperative summaries (sometimes with emojis or quoted workflow names). Use `Add`, `Update`, or `Fix` style messages.
- PRs should include a concise summary, list of touched directories, and any generated report outputs when reorganizing files.
- Link related issues and call out new dependencies or required environment variables.

## Security & Configuration Tips
- The launcher does not load `.env`, install standalone-script dependencies, or configure model providers. Set environment variables required by the selected script; never commit real secrets.
- Service scripts in this checkout commonly read credentials from environment variables or `~/.env.d/`; do not print or inspect secret values. Root `.env` and `.env.d/` are ignored.
- The launcher runs only an exact `.py` path inside the selected repository, rejects external symlinks, and forwards arguments after `--` unchanged. Put launcher flags (including `--dry-run`) before the script path; flags after it belong to the script.
- The installed wheel contains the launcher, not the complete script collection or datasets. Some standalone scripts still use hardcoded paths and require their source-level interface and dependencies to be checked first.
- The old implicit `analyze`, `cleanup`, `dedup`, `organize`, `scan`, `rename`, and `pdf` launcher commands are retired and intentionally return a migration error; use `info` followed by explicit `run`.
- Avoid hand-editing generated build/cache artifacts (`build/`, `dist/`, `*.egg-info/`, `__pycache__/`, `.pytest_cache/`, `.tmp/`) or large analysis outputs unless the task explicitly targets them.
