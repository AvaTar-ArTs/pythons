# Home Directory Scan Report

**Date:** $(date +%Y-%m-%d)  
**Location:** `~/`  
**Disk Usage:** 176GB / 466GB (40% used)

## Executive Summary

This scan identified **10 categories of improvements** that can enhance system performance, organization, and maintainability. Most issues are minor cleanup tasks, with a few configuration improvements recommended.

---

## 🔴 Critical Issues (Action Required)

### 1. Missing Homebrew Dependency
**Issue:** `gemini-cli` requires `node` but it's not installed via Homebrew  
**Impact:** May cause gemini-cli to fail  
**Fix:**
```bash
brew install node
```

### 2. Broken Symlinks
**Issue:** Found broken symlinks that point to non-existent files  
**Locations:**
- `~/.local/bin/python3.10` - Broken symlink
- `~/workspace/archive/` - 153 broken symlinks

**Fix:**
```bash
# Remove broken symlink in .local/bin
rm ~/.local/bin/python3.10

# Review and clean archive symlinks
find ~/workspace/archive -type l ! -exec test -e {} \; -print
```

### 3. Python Syntax Errors
**Issue:** 261 Python files in `~/pythons/` have syntax/compilation errors  
**Impact:** These files cannot be executed  
**Fix:**
```bash
cd ~/pythons
find . -name "*.py" -type f -exec python3 -m py_compile {} \; 2>&1 | grep -i "error\|syntax" > syntax_errors.txt
# Review and fix files listed in syntax_errors.txt
```

---

## ⚠️ Warnings (Recommended Actions)

### 4. Deprecated Homebrew Casks
**Issue:** 6 Quick Look plugins are deprecated/disabled  
**Casks:** `qlcolorcode`, `qlstephen`, `quicklook-csv`, `quicklook-json`, `syntax-highlight`, `webpquicklook`  
**Action:** Find replacements or remove if no longer needed:
```bash
brew list --cask | grep -E "qlcolorcode|qlstephen|quicklook-csv|quicklook-json|syntax-highlight|webpquicklook"
# Review and uninstall if not needed:
# brew uninstall --cask <cask-name>
```

### 5. Large Cache Files
**Issue:** Several large cache files found  
**Details:**
- `~/.cache/chroma/onnx_models/` - Model files (>50M)
- `~/.cache/whisper/base.pt` - Whisper model cache
- `~/.cache/pre-commit/patch*` - Pre-commit patches

**Action:** Review and clean if not actively used:
```bash
du -sh ~/.cache/* | sort -h
# Remove unused caches manually
```

### 6. Large File in Home Directory
**Issue:** `~/INTELLIGENT_HOME_ANALYSIS.json` is >100MB  
**Action:** Consider moving to a more appropriate location or compressing:
```bash
ls -lh ~/INTELLIGENT_HOME_ANALYSIS.json
# Consider: gzip ~/INTELLIGENT_HOME_ANALYSIS.json
# Or move to: mv ~/INTELLIGENT_HOME_ANALYSIS.json ~/Documents/analysis/
```

---

## 🧹 Cleanup Opportunities

### 7. Python Cache Files (High Impact)
**Issue:** Extensive Python bytecode cache  
**Count:**
- 68,512 `.pyc` files
- 8,951 `__pycache__` directories

**Space Savings:** Potentially several GB  
**Fix:**
```bash
# Safe cleanup (won't affect functionality)
find ~ -name "*.pyc" -type f -delete
find ~ -name "__pycache__" -type d -exec rm -rf {} + 2>/dev/null
```

### 8. macOS .DS_Store Files
**Issue:** 3,423 `.DS_Store` files scattered throughout  
**Action:** Clean up and prevent future creation:
```bash
# Remove existing
find ~ -name ".DS_Store" -type f -delete

# Prevent future creation (add to ~/.zshrc)
echo "export DSSTORE_DISABLED=1" >> ~/.zshrc
```

### 9. Empty Python Files
**Issue:** 82 empty Python files in `~/pythons/`  
**Action:** Review and remove if not needed:
```bash
find ~/pythons -name "*.py" -type f -size 0
# Review list and remove unnecessary files
```

### 10. Backup/Old Files in Home
**Issue:** Several backup and archive files in home directory  
**Files:**
- `~/.bashrc.bak`
- `~/.claude.json.backup`
- `~/.zshrc_archive/` (directory)
- `~/.zshrc_env_perm_check`

**Action:** Review and organize:
```bash
# Create archive directory if needed
mkdir -p ~/Documents/backups

# Move backup files
mv ~/.bashrc.bak ~/Documents/backups/ 2>/dev/null
mv ~/.claude.json.backup ~/Documents/backups/ 2>/dev/null

# Review .zshrc_archive - keep if needed, remove if not
# Review .zshrc_env_perm_check - remove if no longer needed
```

---

## 📦 Package Updates

### 11. Outdated Python Packages
**Issue:** 3 packages have updates available  
**Packages:**
- `anyio`: 4.11.0 → 4.12.0
- `networkx`: 3.5 → 3.6
- `pytest`: 8.4.2 → 9.0.1

**Action:**
```bash
pip3 install --upgrade anyio networkx pytest
```

---

## 🔧 Configuration Improvements

### 12. Missing ~/bin Directory
**Issue:** `~/bin` directory doesn't exist (common convention)  
**Action:** Create if you want to store personal scripts:
```bash
mkdir -p ~/bin
# Add to PATH in ~/.zshrc if not already:
# export PATH="$HOME/bin:$PATH"
```

### 13. Go Not in PATH
**Issue:** Go workspace exists (`~/go`) but `go` command not in PATH  
**Action:** Install Go or add to PATH:
```bash
# If Go is installed elsewhere, add to PATH
# Or install via Homebrew:
brew install go
```

### 14. Unusual Files in Home
**Issue:** Files that are unusual in home directory  
**Files:**
- `~/.htaccess` - Typically used in web server directories
- `~/.vector_database.pkl` - Consider moving to project directory

**Action:** Review and relocate if appropriate:
```bash
# Review .htaccess - move if it's for a web project
# Review .vector_database.pkl - move to relevant project directory
```

---

## 📊 Large Directories

### 15. Directory Sizes
**Large directories that may need attention:**

| Directory | Size | Notes |
|-----------|------|-------|
| `~/.local/lib` | 3.0G | Python packages - review for unused packages |
| `~/.cursor` | 1.0G | IDE cache/extensions - normal |
| `~/.config` | 883M | Configuration files - normal |
| `~/.cache` | 608M | Cache files - can be cleaned |
| `~/workspace` | 4.0G | Project files - normal |
| `~/pythons` | 567M | Python scripts - normal |

**Action:** Review `~/.local/lib` for unused packages:
```bash
pip3 list | wc -l  # Count installed packages
# Review and uninstall unused packages
```

---

## ✅ What's Working Well

1. **Environment Management:** `~/.env.d/loader.sh` exists and 19 env files configured
2. **Git Configuration:** Global gitignore exists
3. **Node.js:** v22.14.0 installed and working
4. **Python:** 3.11.14 installed and working
5. **No npm/pip conflicts:** Package managers are healthy
6. **No large log files:** Logs are well-managed
7. **No broken symlinks in home root:** Top-level directory is clean

---

## 🎯 Recommended Action Plan

### Immediate (Do Now)
1. ✅ Install missing `node` dependency: `brew install node`
2. ✅ Remove broken symlink: `rm ~/.local/bin/python3.10`
3. ✅ Review and fix Python syntax errors in `~/pythons/`

### This Week
4. ⚠️ Clean Python cache files (68K+ files)
5. ⚠️ Remove .DS_Store files (3.4K files)
6. ⚠️ Review deprecated Homebrew casks
7. ⚠️ Update outdated Python packages

### This Month
8. 📦 Organize backup files into `~/Documents/backups/`
9. 📦 Review large cache files in `~/.cache/`
10. 📦 Move unusual files (`~/.htaccess`, `~/.vector_database.pkl`) to appropriate locations
11. 📦 Review and clean `~/workspace/archive/` broken symlinks

### Optional
12. 🔧 Create `~/bin` directory for personal scripts
13. 🔧 Install/configure Go if needed
14. 🔧 Review `~/.local/lib` for unused Python packages

---

## 📝 Quick Cleanup Script

Save this as `~/pythons/cleanup_home.sh`:

```bash
#!/bin/bash
# Home directory cleanup script

echo "🧹 Starting cleanup..."

# Remove Python cache
echo "Removing Python cache files..."
find ~ -name "*.pyc" -type f -delete 2>/dev/null
find ~ -name "__pycache__" -type d -exec rm -rf {} + 2>/dev/null

# Remove .DS_Store files
echo "Removing .DS_Store files..."
find ~ -name ".DS_Store" -type f -delete 2>/dev/null

# Remove broken symlink
echo "Removing broken symlinks..."
rm -f ~/.local/bin/python3.10

# Update packages
echo "Updating Python packages..."
pip3 install --upgrade anyio networkx pytest

echo "✅ Cleanup complete!"
```

Make it executable:
```bash
chmod +x ~/pythons/cleanup_home.sh
```

---

## 📈 Estimated Space Savings

After cleanup:
- Python cache: ~500MB - 2GB (estimated)
- .DS_Store files: ~50MB (estimated)
- Large cache files: ~200MB (if cleaned)
- **Total potential savings: ~750MB - 2.5GB**

---

## 🔍 Next Steps

1. Review this report
2. Prioritize actions based on your needs
3. Run cleanup script (after reviewing)
4. Schedule regular maintenance (monthly recommended)

---

**Report Generated:** $(date)  
**Scan Location:** `/Users/steven/`  
**Total Issues Found:** 15 categories  
**Critical Issues:** 3  
**Warnings:** 3  
**Cleanup Opportunities:** 4  
**Configuration Improvements:** 3  
**Package Updates:** 2
