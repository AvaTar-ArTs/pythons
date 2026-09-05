# Repository Guidelines

## Project Structure & Module Organization
- Root contains overview docs and analysis reports; keep new docs in `documentation/` when possible.
- Domain scripts live in `apis/`, `data_processing/`, `file_operations/`, `media_processing/`, and `tools/`.
- Standalone apps and vendor code live in `projects/`; these may carry their own dependencies and test suites.
- Generated outputs and datasets are typically stored in `analysis/`, `data/`, `content/`, and `archives/`.
- Ad hoc tests and debugging helpers live in `testing/` or alongside the feature area.

## Build, Test, and Development Commands
- `python -m venv .venv && source .venv/bin/activate` to create a local environment.
- Use Python 3.9–3.12. `python -m pip install -e '.[dev]'` installs the standard-library launcher and development tools; standalone scripts have separate dependencies.
- `python file_operations/pythons_sort.py --help` to discover the framework CLI commands.
- List scripts with `python pythons_sort.py info --all`. Use `python pythons_sort.py run --dry-run <script.py> -- <script arguments>` to preview an exact command; see `documentation/CLI.md` before running legacy scripts.
- `pre-commit run --all-files` to apply Black, isort, Flake8, mypy, and security checks.

## Coding Style & Naming Conventions
- Follow `.editorconfig`: 4-space indents, LF endings, trim trailing whitespace; JSON/YAML use 2-space indents.
- Black is configured (line length 88); Flake8 and EditorConfig allow 100. When in doubt, run Black and isort.
- Prefer `snake_case.py` for new scripts and `test_*.py` for pytest tests; avoid spaces in filenames.
- Keep scripts focused and self-contained; place shared helpers in the closest relevant module folder.

## Testing Guidelines
- Pytest is the default runner; the top-level `tests/` directory covers bundle structure and launcher behavior. Run it with `python -m pytest tests`.
- Run tests scoped to the area you touch, for example `pytest media_processing/social_media/tests`.
- Some subprojects include their own suites, such as `pytest projects/frameworks/axolotl-main/tests`.
- Add regression coverage next to the module or subproject it validates.

## Commit & Pull Request Guidelines
- Commit history uses short, imperative summaries (sometimes with emojis or quoted workflow names). Use `Add`, `Update`, or `Fix` style messages.
- PRs should include a concise summary, list of touched directories, and any generated report outputs when reorganizing files.
- Link related issues and call out new dependencies or required environment variables.

## Security & Configuration Tips
- The launcher does not load `.env` or configure model providers. Set environment variables required by the selected script; use `.env.example` as a template and never commit real secrets.
- Pre-commit includes secret scanning; keep large binaries in `archives/` or `analysis/` when possible.
