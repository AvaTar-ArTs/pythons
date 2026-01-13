# Cache & Local Directory Cleanup Analysis
**Generated:** 2025-11-25
**Total Size Analyzed:** 5.5 GB

---

## 📊 Directory Summary

| Directory | Size | Primary Contents |
|-----------|------|------------------|
| `~/.cache` | 2.3 GB | ML models, build caches, pre-commit hooks |
| `~/.local` | 2.0 GB | Python packages, IDE data, application state |
| `~/.ollama` | 1.2 GB | Ollama AI models |

---

## 🔍 Detailed Breakdown

### ~/.cache (2.3 GB)

#### High-Impact Items (Safe to Clean)
1. **HuggingFace Hub: 1.7 GB** ⚠️ LARGEST
   - `faster-whisper-medium`: 1.4 GB
   - `faster-whisper-base`: 141 MB
   - `faster-whisper-tiny`: 75 MB
   - `sentence-transformers/all-MiniLM-L6-v2`: Unknown size
   - **Impact:** Will re-download on next use
   - **Safe to remove:** YES (models will auto-download when needed)

2. **Pre-commit Hooks: 197 MB**
   - 10 git repositories cached
   - **Safe to remove:** YES (will auto-rebuild on next run)
   - **Command:** `pre-commit clean` or `rm -rf ~/.cache/pre-commit`

3. **Chroma ONNX Models: 166 MB**
   - Used for embeddings/vector search
   - **Safe to remove:** YES (will re-download)

4. **Whisper Cache: 139 MB**
   - Duplicate/older whisper cache?
   - **Safe to remove:** YES

#### Low-Impact Items
- **Node/Corepack: 25 MB** - Safe to clean
- **UV Cache: 19 MB** - Python package manager cache (safe)
- **VSCode Ripgrep: 1.6 MB** - Minimal
- **YouTube-DLP: 20 KB** - Minimal
- **Claude Dirs: 4 KB** - Minimal

---

### ~/.local (2.0 GB)

#### High-Impact Items (⚠️ Review Before Removing)
1. **Python 3.12 Packages: 1.1 GB**
   - Location: `~/.local/lib/python3.12`
   - **CAUTION:** Contains installed Python packages
   - **Safe to remove:** ONLY if not actively used
   - **Alternative:** Use virtual environments instead

2. **Claude Data: 331 MB**
   - Location: `~/.local/share/claude`
   - **CAUTION:** May contain conversations, settings, extensions
   - **Review before deleting**

3. **Cursor Agent: 330 MB**
   - Location: `~/.local/share/cursor-agent`
   - **CAUTION:** IDE extension data
   - **Safe to remove:** Only if not using Cursor

4. **Jupyter: 27 MB**
   - Kernels, extensions, config
   - **Safe to remove:** Only if not using Jupyter

#### Low-Impact Items
- **Bin: 86 MB** - User scripts/executables (review first)
- **State: 88 MB** - Various app states (generally safe)

---

### ~/.ollama (1.2 GB)

#### Models Installed
1. **gpt-oss:120b-cloud** - Cloud model (minimal local storage)
2. **qwen3-coder:480b-cloud** - Cloud model (minimal local storage)
3. **deepseek-v3.1:671b-cloud** - Cloud model (minimal local storage)
4. **llama3.2:1b** - Local model (~1.3 GB blob)

**Note:** Most storage is one large model blob (1.3 GB). Cloud models have minimal footprint.

**Safe to remove:**
- Use `ollama rm llama3.2:1b` to remove unused models
- **CAUTION:** Will need to re-pull if you use them

---

## 🎯 Recommended Cleanup Actions

### 🟢 SAFE CLEANUP (Conservative - ~2.2 GB)
**No risk to functionality - items will regenerate/re-download automatically**

```bash
# 1. Clean HuggingFace cache (1.7 GB)
# Remove specific models you don't need:
rm -rf ~/.cache/huggingface/hub/models--Systran--faster-whisper-medium  # 1.4 GB
rm -rf ~/.cache/huggingface/hub/models--Systran--faster-whisper-base    # 141 MB
# Keep tiny if you need whisper functionality

# 2. Clean pre-commit cache (197 MB)
pre-commit clean
# OR: rm -rf ~/.cache/pre-commit

# 3. Clean chroma cache (166 MB)
rm -rf ~/.cache/chroma

# 4. Clean old whisper cache (139 MB)
rm -rf ~/.cache/whisper

# 5. Clean node cache (25 MB)
rm -rf ~/.cache/node

# 6. Clean UV cache (19 MB)
rm -rf ~/.cache/uv
```

**Total Recovery: ~2.2 GB**

---

### 🟡 MODERATE CLEANUP (Review First - Additional ~1.5 GB)

```bash
# 1. Review and clean Python packages if using venvs instead
# ONLY if you use virtual environments and don't need global packages
du -sh ~/.local/lib/python3.12/site-packages/*/ | sort -rh | head -20
# Then selectively remove with: pip uninstall <package>

# 2. Review Cursor agent data (if not using Cursor)
ls -lh ~/.local/share/cursor-agent
# rm -rf ~/.local/share/cursor-agent  # 330 MB

# 3. Review Claude data (conversations, settings)
ls -lh ~/.local/share/claude
# Selectively remove old data if safe

# 4. Clean Jupyter if not using
rm -rf ~/.local/share/jupyter  # 27 MB
```

**Total Additional Recovery: ~400 MB - 1.5 GB**

---

### 🔴 AGGRESSIVE CLEANUP (Use with Caution - Additional ~1.2 GB)

```bash
# Remove Ollama models you don't actively use
ollama list  # Check what's installed
ollama rm llama3.2:1b  # ~1.3 GB

# Nuclear option: Remove all Ollama models
# rm -rf ~/.ollama/models  # 1.2 GB
# WARNING: Will need to re-pull all models
```

**Total Additional Recovery: ~1.2 GB**

---

## 📋 Quick Command Summary

### View Sizes Before Cleanup
```bash
# Check sizes before removing
du -sh ~/.cache/huggingface
du -sh ~/.cache/pre-commit
du -sh ~/.cache/chroma
du -sh ~/.cache/whisper
du -sh ~/.ollama/models
```

### Conservative One-Liner (Safe ~2.2 GB)
```bash
rm -rf ~/.cache/huggingface/hub/models--Systran--faster-whisper-medium \
       ~/.cache/huggingface/hub/models--Systran--faster-whisper-base \
       ~/.cache/pre-commit \
       ~/.cache/chroma \
       ~/.cache/whisper \
       ~/.cache/node \
       ~/.cache/uv && \
echo "✓ Cleaned ~2.2 GB safely"
```

### After Cleanup Verification
```bash
# Check new sizes
du -sh ~/.cache ~/.local ~/.ollama
```

---

## 💡 Best Practices Going Forward

1. **ML Models:** Use project-specific cache dirs or clean periodically
2. **Python Packages:** Use virtual environments instead of global installs
3. **Pre-commit:** Runs `pre-commit clean` periodically (or add to cron)
4. **Ollama Models:** Remove unused models promptly with `ollama rm`
5. **IDE Data:** Periodically review ~/.local/share for old IDE data

---

## ⚠️ Important Notes

- **HuggingFace models** will re-download automatically when needed (may take time)
- **Pre-commit hooks** will rebuild automatically on next run (adds ~30s)
- **Python packages** in ~/.local are NOT in virtual environments - be careful
- **Ollama models** must be explicitly re-pulled after removal
- **Always backup before aggressive cleanup** if unsure

---

## 🔧 Maintenance Commands

```bash
# Check cache sizes periodically
alias cache-check='du -sh ~/.cache ~/.local ~/.ollama'

# Clean pre-commit automatically
pre-commit clean

# List and clean old ollama models
ollama list
ollama rm <model-name>

# Find large files in caches
find ~/.cache -type f -size +100M -exec ls -lh {} \;
```

---

**Recommendation:** Start with the SAFE cleanup to recover ~2.2 GB, then evaluate if you need more space.
