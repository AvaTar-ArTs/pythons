# notebooklm-py: Recovery & Polish Plan

> **For Hermes:** Use subagent-driven-development skill to implement this plan task-by-task.
> **TDD enforced:** Every code change begins with a failing test.

**Goal:** Recover corrupted scripts, fix metadata, polish docs, and integrate merged tooling.

**Architecture:** The project is a mature Python library (14K+ lines). We're doing surgical fixes — updating metadata for our fork, recovering 14 corrupted CLI scripts, fixing a git submodule issue, and polishing documentation. No architectural changes.

**Tech Stack:** Python 3.10+, Click, httpx, Hatchling build, pytest, ruff

---

## Phase 1: Corrupted Script Recovery (14 scripts)

All 14 scripts copied from the consolidation have collapsed line endings causing unterminated strings, merged statements, and syntax errors. They must be rewritten from scratch using the original logic as reference.

### Task 1.1: Recover ask_question.py

**Objective:** Rewrite `scripts/ask_question.py` — NotebookLM question interface via Playwright, with auth and follow-up reminders.

**Files:**
- Create: `tests/unit/test_ask_question.py`
- Modify: `scripts/ask_question.py` (complete rewrite)

**Reference:** Original intent visible in corrupted file (line 1-6 have intact docstring describing hybrid auth approach: persistent browser profile + manual cookie injection for Playwright bug workaround).

**Step 1: Write failing test**

```python
def test_ask_question_imports_and_structure():
    """Verify the module is importable and has expected API."""
    import importlib.util
    spec = importlib.util.spec_from_file_location(
        "ask_question", "scripts/ask_question.py"
    )
    mod = importlib.util.module_from_spec(spec)
    # Should at minimum define ask_notebooklm function and FOLLOW_UP_REMINDER
    spec.loader.exec_module(mod)
    assert hasattr(mod, "ask_notebooklm")
    assert hasattr(mod, "FOLLOW_UP_REMINDER")
    assert callable(mod.ask_notebooklm)
```

**Step 2: Run test to verify failure**

Run: `pytest tests/unit/test_ask_question.py::test_ask_question_imports_and_structure -v`
Expected: FAIL — SyntaxError on import

**Step 3: Write minimal implementation**

Rewrite `ask_question.py` with:
- Shebang + docstring
- argparse setup (--question, --url, --headless flags)
- `FOLLOW_UP_REMINDER` constant
- `ask_notebooklm(question, notebook_url, headless=True) -> str` stub using Playwright
- `if __name__ == "__main__"` entry point

**Step 4: Run test to verify pass**

Run: `pytest tests/unit/test_ask_question.py::test_ask_question_imports_and_structure -v`
Expected: PASS

**Step 5: Commit**

```bash
git add tests/unit/test_ask_question.py scripts/ask_question.py
git commit -m "fix: recover ask_question.py from corrupted source, add import test"
```

### Task 1.2: Recover batch_query.py

**Objective:** Rewrite `scripts/batch_query.py` — batch question interface for multiple notebooks.

**Files:**
- Create: `tests/unit/test_batch_query.py`
- Modify: `scripts/batch_query.py` (complete rewrite)

**Step 1: Write failing test**

```python
def test_batch_query_imports():
    import importlib.util
    spec = importlib.util.spec_from_file_location(
        "batch_query", "scripts/batch_query.py"
    )
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    assert hasattr(mod, "batch_query_notebooks")
    assert callable(mod.batch_query_notebooks)
```

**Step 2:** Run → FAIL (SyntaxError)
**Step 3:** Rewrite with argparse, `batch_query_notebooks()`, CSV output
**Step 4:** Run → PASS
**Step 5:** Commit

### Task 1.3: Recover remaining 12 scripts (batch)

**Objective:** Recover the remaining 12 corrupted scripts. All follow similar pattern — notebooklm automation tools using Playwright.

**Files per script:**
- Create: `tests/unit/test_<script>.py`
- Modify: `scripts/<script>.py` (complete rewrite)

**Scripts to recover:**
| Script | Purpose |
|--------|---------|
| conversation_logger.py | Log conversations to CSV |
| export_manager.py | Manage notebook exports |
| profile_manager.py | Browser profile management |
| query_history.py | Query history viewer |
| source_csv_extractor_test.py | CSV source extraction (test variant) |
| source_csv_extractor_v2.py | CSV source extraction v2 |
| source_csv_extractor_v3.py | CSV source extraction v3 |
| source_csv_extractor_v4.py | CSV source extraction v4 |
| source_diagnostic.py | Source diagnostics |
| source_extractor.py | Generic source extractor |
| source_live_observer.py | Live source observer |
| source_simple_reader.py | Simple source reader |

**Pattern for each:**
1. Write failing import test → FAIL (SyntaxError)
2. Rewrite script from reference logic → PASS
3. Commit individually

---

## Phase 2: Fix Project Metadata

### Task 2.1: Update pyproject.toml authors

**Objective:** Update author metadata to reflect our maintainership while preserving original credit.

**Files:**
- Modify: `pyproject.toml:8-10`

**Step 1: Read current authors**
Current: `{name = "Teng Lin", email = "teng.lin@gmail.com"}`

**Step 2: Patch** — append our authorship:
```toml
authors = [
    {name = "Teng Lin", email = "teng.lin@gmail.com"},
    {name = "Steven Chaplinski / AvaTar-ArTs"},
]
```

**Step 3: Verify** — `uv run python -c "from importlib.metadata import metadata; print(metadata('notebooklm-py')['Author'])"`
**Step 4: Commit**

### Task 2.2: Update README URLs

**Objective:** Update GitHub URLs to point to our fork instead of `teng-lin/notebooklm-py`.

**Files:**
- Modify: `README.md` (lines 2, 8-11, 16)
- Modify: `pyproject.toml` (lines 31-34)

**Changes:**
- Logo URL: `teng-lin/notebooklm-py/main/` → `AvaTar-ArTs/pythons/main/notebooklm-py/`
- Badge URLs: Update PyPI version badge, tests badge to point to our CI
- Homepage/Repository: `teng-lin/notebooklm-py` → `AvaTar-ArTs/pythons` (tree path to notebooklm-py)
- fancy-pypi-readme substitutions: update all `teng-lin/notebooklm-py` references

**Step 1: Verify current URL** — `grep -n "teng-lin" README.md pyproject.toml`
**Step 2: Patch all occurrences**
**Step 3: Verify** — `grep "teng-lin" README.md pyproject.toml` should show zero matches
**Step 4: Commit**

---

## Phase 3: Fix Consolidate Repo Submodule

### Task 3.1: Fix notebooklm-skill submodule ref

**Objective:** Replace git mode 160000 (submodule pointer) with real directory content in `AvaTar-ArTs/notebooklm-mine`.

**Files:**
- Modify: `/Volumes/bakUp/NotebookLM/.gitmodules` (remove if exists)
- Modify: index in `/Volumes/bakUp/NotebookLM/.git/`

**Step 1: Check current state**
```bash
cd /Volumes/bakUp/NotebookLM
git ls-files -s notebooklm-skill
# Expected: 160000 <sha> 0<TAB>notebooklm-skill
```

**Step 2: Fix**
```bash
git rm --cached notebooklm-skill
git add notebooklm-skill/
git status  # Should show real files, not submodule
```

**Step 3: Verify**
```bash
git ls-files -s notebooklm-skill/ | head -3
# Expected: 100644 (normal file mode), not 160000
```

**Step 4: Commit and push**

---

## Phase 4: Polish README + Project Docs

### Task 4.1: Add install instructions for our fork

**Objective:** Add clear pip install instructions that work from our repo.

**Files:**
- Modify: `README.md`

**Add after the intro paragraph:**

```markdown
## Installation

```bash
pip install notebooklm-py
```

For development:
```bash
git clone https://github.com/AvaTar-ArTs/pythons.git
cd pythons/notebooklm-py
uv sync --extra dev --extra browser
```

### Task 4.2: Add scripts documentation

**Objective:** Document the 17 scripts in `scripts/` directory.

**Files:**
- Create: `docs/scripts.md`

**Content:** Table listing each script with purpose, usage example, and status (✓ stable / ⚠ needs tests).

### Task 4.3: Verify all doc links resolve

**Objective:** Ensure no broken relative links in docs.

**Files:**
- Check: All `docs/*.md` files

**Step 1: Find all relative links**
```bash
grep -r '\[.*\](\.\.\/\|\.\/\|docs\/)' docs/ README.md CONTRIBUTING.md
```

**Step 2: Verify each target exists**
**Step 3: Fix any broken links**

---

## Phase 5: CI/CD Pipeline (Future)

> **Deferred.** Requires GitHub Actions secrets (PyPI token). Document the plan for later.

### Task 5.1: Create CI workflow (future)

**Files to create:**
- `.github/workflows/test.yml` — pytest + ruff + mypy on push/PR
- `.github/workflows/publish.yml` — build + publish to PyPI on tag

---

## Execution Order

```
Phase 1 (Tasks 1.1-1.3) → 14 script recoveries
Phase 2 (Tasks 2.1-2.2) → Metadata updates
Phase 3 (Task 3.1)      → Submodule fix
Phase 4 (Tasks 4.1-4.3) → Docs polish
Phase 5                 → Deferred
```

Each task independently verifiable. Commit after each. TDD: test before code.
