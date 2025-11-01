# 🔧 BARE EXCEPT FIX REPORT

**Generated:** 2025-11-01 04:30:48
**Mode:** DRY RUN

---

## 📊 FIX SUMMARY

| Metric | Value |
|--------|-------|
| Files Scanned | 2,950 |
| Bare Excepts Found | 9 |
| Files Fixed | 6 |
| Fixes Applied | 9 |

## 🎯 FIXES BY CONTEXT TYPE

- **file**: 5 fixes
- **value**: 1 fixes
- **index**: 1 fixes
- **general**: 1 fixes
- **import**: 1 fixes

## 📝 DETAILED FIXES

### `scripts/ai_deep_analyzer.py`
**Fixes:** 2

**Line 240**
- Before: `except:`
- After: `except (ValueError, TypeError):`
- Context: value

**Line 228**
- Before: `except:`
- After: `except (IndexError, KeyError):`
- Context: index

### `scripts/analyze_codebase.py`
**Fixes:** 2

**Line 150**
- Before: `except:`
- After: `except Exception:`
- Context: general

**Line 122**
- Before: `except:`
- After: `except (ImportError, ModuleNotFoundError):`
- Context: import

### `scripts/content_aware_organizer.py`
**Fixes:** 1

**Line 91**
- Before: `except:`
- After: `except (OSError, IOError, FileNotFoundError):`
- Context: file

### `scripts/cross_directory_merger.py`
**Fixes:** 2

**Line 235**
- Before: `except:`
- After: `except (OSError, IOError, FileNotFoundError):`
- Context: file

**Line 74**
- Before: `except:`
- After: `except (OSError, IOError, FileNotFoundError):`
- Context: file

### `scripts/final_consolidator.py`
**Fixes:** 1

**Line 69**
- Before: `except:`
- After: `except (OSError, IOError, FileNotFoundError):`
- Context: file

### `scripts/intelligent_renamer.py`
**Fixes:** 1

**Line 174**
- Before: `except:`
- After: `except (OSError, IOError, FileNotFoundError):`
- Context: file

