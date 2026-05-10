# Security Audit: Dangerous `eval()`/`exec()` Usage

**Date:** April 12, 2026
**Scope:** `/Users/steven/pythons` — all Python files
**Auditor:** Senior Code Reviewer

---

## Summary

Fixed **4 high-priority files** containing dangerous `eval()`/`exec()` patterns that could allow
arbitrary code execution. Added security documentation for **6 framework files** in axolotl-main
that use `exec()` for legitimate metaprogramming.

## Changes Made

### 1. `config/crawl.py` — ✅ FIXED

**Issue:** `eval(checks["type"])(value)` and `eval(get_check_value("type", "False"))`
- If an attacker controls the `checks` dict (e.g., via a malicious TOML template),
  they can execute arbitrary Python code.

**Fix:** Replaced with `_SAFE_TYPE_MAP` dictionary + `_safe_type_convert()` helper.
- Whitelisted types: `str`, `int`, `float`, `bool`, `list`, `dict`, `tuple`
- Uses `ast.literal_eval` for complex types (list/dict/tuple)
- Unknown types fall back to `str` (safe coercion)

**Impact:** No functional change for legitimate configs. Malicious type strings now resolve
to `str` instead of executing arbitrary code.

---

### 2. `apis/settings.py` — ✅ FIXED (Full Rewrite)

**Issue:** File was severely corrupted — a malformed concatenation of multiple source files
containing:
- Duplicate `eval()` fragments copied from `crawl.py`
- Broken `async`/`def` syntax interleaving
- Nonsensical variable assignments and orphaned code blocks
- Multiple syntax errors preventing the file from being imported

**Fix:** Complete rewrite preserving the intended components:
- HTTP utilities (`async_request`, `process_urls`)
- Decorators (`timing_decorator`, `retry_decorator`)
- `BaseProcessor` abstract class
- `SingletonMeta` metaclass
- `Config` class with constants
- `validate_input()` and `memoize()` utilities
- Added security note referencing `config/crawl.py` for type conversion

**Impact:** File is now syntactically valid and importable. All original functionality
preserved in clean form.

---

### 3. `data_processing/unified-workflow-poc.py` — ✅ FIXED

**Issue:** `eval(condition, {"__builtins__": {}})` in `_evaluate_condition()`
- While `__builtins__` is stripped, attribute-access attacks still work:
  `().__class__.__bases__[0].__subclasses__()` can access any Python class
- Used to evaluate workflow step conditions like `media_type == 'audio'`

**Fix:** Replaced with `_safe_bool_eval()` — an AST-based expression evaluator that:
- Parses the condition into an AST tree
- Only allows `Compare` nodes with standard operators (`==`, `!=`, `>`, `<`, `>=`, `<=`)
- Rejects all function calls, attribute access, imports, and other dangerous node types
- Supports the same condition syntax: `media_type == 'audio'`, `count > 5`, etc.

**Impact:** Conditions like `media_type == 'audio'` evaluate identically. Malicious payloads
like `().__class__.__bases__` raise `ValueError: Unsupported AST node type`.

---

### 4. `apis/telegraph-download-images.py` — ✅ FIXED

**Issue:** Three `exec()` calls for dynamic thread management:
```python
exec(f"img{imgNumber} = threading.Thread(target=download, args=(imgNumber, imgUrl))")
exec(f"img{imgNumber}.start()")
exec(f"img{n + 1}.join()")
```
- If `imgUrl` contains crafted strings (e.g., from a malicious telegra.ph article),
  they could be injected into the exec'd code
- Completely unnecessary — proper thread management requires no `exec()`

**Fix:** Replaced with a simple `download_threads` list:
```python
download_threads = []
thread = threading.Thread(target=download, args=(imgNumber, imgUrl))
download_threads.append(thread)
thread.start()
# ... later ...
for thread in download_threads:
    thread.join()
```

**Impact:** Identical threading behavior. Cleaner, more readable, and completely safe.
File compiles successfully.

---

### 5. `projects/frameworks/axolotl-main/` — 📝 DOCUMENTED (No Code Changes)

**Issue:** 6 files use `exec()` for metaprogramming (monkeypatching HuggingFace Transformers).

**Assessment:** These are **intentional architectural patterns** — the framework inspects
library source code, modifies it as strings, and `exec()`s the result to patch behavior.
The code being exec'd comes from installed libraries, not user input.

**Action:** Created `SECURITY_NOTES.md` documenting:
- All 6 files and their purposes
- Risk assessment (Low when used as intended, Medium-High if misused)
- 5 recommendations for safe maintenance
- Clarification that `model.eval()` calls are unrelated (PyTorch eval mode)

---

## Verification

| File | Syntax Check | Functional Impact |
|------|-------------|-------------------|
| `config/crawl.py` | ⚠️ Pre-existing syntax errors (line 170, unrelated to fix) | No change to legitimate type conversion |
| `apis/settings.py` | ✅ Clean | File was broken; now importable |
| `data_processing/unified-workflow-poc.py` | ⚠️ Pre-existing syntax error (line 75, unrelated to fix) | Condition evaluation identical for safe inputs |
| `apis/telegraph-download-images.py` | ✅ Clean | Identical threading behavior |

---

## Recommendations for Future Work

1. **Fix pre-existing syntax errors** in `config/crawl.py` (line 170 string literal) and
   `unified-workflow-poc.py` (line 75 malformed function signature) — these are separate
   issues from the eval/exec fixes.

2. **Add a pre-commit hook** to flag new `eval()`/`exec()` usage:
   ```yaml
   - id: no-eval-exec
     name: 'No eval()/exec()'
     entry: 'grep -nE "\\b(eval|exec)\\s*\\(" --include="*.py"'
     language: system
     types: [python]
   ```

3. **Audit other directories** for similar patterns — this audit covered the 4 highest-priority
   files. A full-scan grep found 20+ additional `exec()` matches (mostly in axolotl-main).

4. **Consider AST-based code generation** for the axolotl monkeypatching instead of string
   manipulation + `exec()` — safer but more complex.
