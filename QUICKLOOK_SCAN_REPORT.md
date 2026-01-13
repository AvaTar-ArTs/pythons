# Quick Look Plugin System Scan Report

**Date:** Generated automatically  
**Location:** `/Users/steven/pythons/`

## Summary

Scanned the root filesystem (`/`) for Quick Look plugin issues and found **5 critical issues** that need attention.

## Issues Found

### ❌ Critical Issues (5)

1. **Broken Symlinks** - All Homebrew-installed Quick Look plugins have broken symlinks:
   - `QuickLookJSON.qlgenerator` → Points to non-existent `/usr/local/Caskroom/quicklook-json/2,1.0/QuickLookJSON.qlgenerator`
   - `QLStephen.qlgenerator` → Points to non-existent `/usr/local/Caskroom/qlstephen/1.5.1/QLStephen.qlgenerator`
   - `QLColorCode.qlgenerator` → Points to non-existent `/usr/local/Caskroom/qlcolorcode/4.1.0/QLColorCode.qlgenerator`
   - `WebpQuickLook.qlgenerator` → Points to non-existent `/usr/local/Caskroom/webpquicklook/1.0/WebpQuickLook.qlgenerator`
   - `QuickLookCSV.qlgenerator` → Points to non-existent `/usr/local/Caskroom/quicklook-csv/1.3/QuickLookCSV.qlgenerator`

**Root Cause:** The Homebrew caskroom directories contain symlinks that point back to `~/Library/QuickLook/`, creating circular references. The actual plugin directories don't exist.

### ⚠️ Warnings (1)

- `qlvideo` cask installed but no plugin found in caskroom

## System Status

### Plugin Directories
- **User plugins:** `~/Library/QuickLook/` - 6 plugins found (5 broken, 1 working)
- **System plugins:** `/Library/QuickLook/` - 0 plugins
- **System built-in:** `/System/Library/QuickLook/` - 20 plugins (working)

### Working Plugins
- `TypeScript.qlgenerator` - Working directory plugin (135.12 KB)

### Additional Plugins Found
The scan found plugins embedded in applications:
- Screenium Quick Look Plugin (in Screenium 3.app)
- DEVONthink Quick Look (in DEVONthink 3.app)
- Markdown Quicklook Plugin (in File Cabinet Pro.app)
- QuickLookPlugin (in Transmission.app)
- Paper.qlgenerator (in Setapp/Paper.app)
- BetterZipQL (in BetterZip.app)

### Quick Look Service
✅ Quick Look service is running and accessible

## Tools Created

Three Python scripts have been created in `~/pythons/`:

1. **`quicklook-plugin-manager.py`** - Full plugin management tool
   - List, install, uninstall plugins
   - Backup and restore
   - Generate plugin inventory

2. **`quicklook-diagnostic.py`** - Diagnostic scanner
   - Detects broken symlinks
   - Checks Homebrew installations
   - Validates plugin structure
   - Reports all issues

3. **`quicklook-fix.py`** - Automated fix tool
   - Removes broken symlinks
   - Reinstalls Homebrew plugins
   - Refreshes Quick Look cache
   - Restarts Finder

## Recommended Actions

### Immediate Fix

Run the fix script to automatically resolve issues:

```bash
cd ~/pythons
python3 quicklook-fix.py
```

Or run in dry-run mode first to preview changes:

```bash
python3 quicklook-fix.py --dry-run
```

### Manual Fix (Alternative)

If you prefer to fix manually:

1. **Backup current state:**
   ```bash
   python3 ~/pythons/quicklook-plugin-manager.py backup all
   ```

2. **Remove broken symlinks:**
   ```bash
   rm ~/Library/QuickLook/QuickLookJSON.qlgenerator
   rm ~/Library/QuickLook/QLStephen.qlgenerator
   rm ~/Library/QuickLook/QLColorCode.qlgenerator
   rm ~/Library/QuickLook/WebpQuickLook.qlgenerator
   rm ~/Library/QuickLook/QuickLookCSV.qlgenerator
   ```

3. **Reinstall Homebrew plugins:**
   ```bash
   brew reinstall --cask qlcolorcode qlstephen quicklook-csv quicklook-json webpquicklook
   ```

4. **Refresh Quick Look:**
   ```bash
   qlmanage -r
   killall Finder
   ```

### Verification

After fixing, verify the installation:

```bash
python3 ~/pythons/quicklook-diagnostic.py
python3 ~/pythons/quicklook-plugin-manager.py list all
```

## Prevention

To avoid this issue in the future:

1. **Use the management tools** to track plugin installations
2. **Backup regularly** using: `python3 ~/pythons/quicklook-plugin-manager.py backup all`
3. **Run diagnostics periodically**: `python3 ~/pythons/quicklook-diagnostic.py`
4. **When installing via Homebrew**, verify the installation worked:
   ```bash
   brew list --cask <plugin-name>
   ls -la ~/Library/QuickLook/
   ```

## Notes

- The `TypeScript.qlgenerator` plugin is working correctly (not installed via Homebrew)
- System built-in plugins are all functioning normally
- Application-embedded plugins are working (they don't use symlinks)
