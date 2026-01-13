# Quick Look Plugin Management Tools

A comprehensive set of Python tools for managing Quick Look plugins on macOS.

## Tools Overview

### 1. `quicklook-plugin-manager.py`
Full-featured plugin management tool for installation, backup, and maintenance.

### 2. `quicklook-diagnostic.py`
Scans your system for Quick Look plugin issues and generates detailed reports.

### 3. `quicklook-fix.py`
Automatically fixes broken symlinks and reinstalls plugins.

## Quick Start

### Check Current Status
```bash
cd ~/pythons
python3 quicklook-diagnostic.py
```

### Fix Issues Automatically
```bash
python3 quicklook-fix.py
```

### List All Plugins
```bash
python3 quicklook-plugin-manager.py list all
```

### Backup All Plugins
```bash
python3 quicklook-plugin-manager.py backup all
```

## Usage Examples

### Plugin Manager

**List plugins:**
```bash
python3 quicklook-plugin-manager.py list user      # User plugins only
python3 quicklook-plugin-manager.py list system    # System plugins only
python3 quicklook-plugin-manager.py list all       # All plugins
```

**Install a plugin:**
```bash
python3 quicklook-plugin-manager.py install ~/Downloads/MyPlugin.qlgenerator user
```

**Uninstall a plugin:**
```bash
python3 quicklook-plugin-manager.py uninstall QLColorCode.qlgenerator user
```

**Backup plugins:**
```bash
python3 quicklook-plugin-manager.py backup all                    # Backup all
python3 quicklook-plugin-manager.py backup QLColorCode.qlgenerator user  # Single plugin
```

**Generate plugin inventory:**
```bash
python3 quicklook-plugin-manager.py generate-list
python3 quicklook-plugin-manager.py generate-list ~/my_plugins.txt
```

**Refresh Quick Look:**
```bash
python3 quicklook-plugin-manager.py refresh
python3 quicklook-plugin-manager.py restart-finder
```

### Diagnostic Tool

**Run full diagnostic:**
```bash
python3 quicklook-diagnostic.py
```

This will check for:
- Broken symlinks
- Circular symlink references
- Homebrew installation issues
- Permission problems
- Service status

### Fix Tool

**Preview what will be fixed (dry run):**
```bash
python3 quicklook-fix.py --dry-run
```

**Actually fix issues:**
```bash
python3 quicklook-fix.py
```

## Available Quick Look Plugins via Homebrew

Popular plugins you can install:

```bash
# Code & Text
brew install --cask qlcolorcode      # Syntax highlighting for code
brew install --cask qlstephen         # Preview text files without extension
brew install --cask quicklook-json    # JSON file preview
brew install --cask quicklook-csv    # CSV file preview

# Media
brew install --cask webpquicklook     # WebP image preview
brew install --cask avifquicklook     # AVIF image preview
brew install --cask quicklookase      # Adobe ASE color palette preview

# Development
brew install --cask ipynb-quicklook   # Jupyter notebook preview
brew install --cask quicklookapk      # Android APK preview
brew install --cask gltfquicklook     # 3D GLTF model preview

# Specialized
brew install --cask quicklook-pat     # Adobe PAT pattern preview
brew install --cask quicklook-pfm     # Font preview
brew install --cask receiptquicklook  # Receipt preview
```

After installing via Homebrew, verify with:
```bash
python3 quicklook-plugin-manager.py list all
python3 quicklook-diagnostic.py
```

## Common Issues & Solutions

### Broken Symlinks
**Symptom:** Plugins don't work, diagnostic shows broken symlinks

**Solution:**
```bash
python3 quicklook-fix.py
```

### Circular Symlinks
**Symptom:** Symlinks point to each other in a loop

**Solution:**
```bash
python3 quicklook-fix.py
```

### Plugin Not Working After Installation
1. Refresh Quick Look: `qlmanage -r`
2. Restart Finder: `killall Finder`
3. Or use: `python3 quicklook-plugin-manager.py refresh && python3 quicklook-plugin-manager.py restart-finder`

### Permission Denied
For system-wide plugins, you may need sudo:
```bash
sudo python3 quicklook-plugin-manager.py install plugin.qlgenerator system
```

## Backup & Restore

### Create Backup
```bash
python3 quicklook-plugin-manager.py backup all
```

Backups are stored in: `~/.quicklook_plugins_backup/`

### Backup Structure
```
~/.quicklook_plugins_backup/
├── all_plugins_20251127_143022/
│   ├── user/
│   │   ├── QLColorCode.qlgenerator/
│   │   └── ...
│   ├── system/
│   └── metadata.json
└── plugin_list_20251127.txt
```

## File Locations

- **User plugins:** `~/Library/QuickLook/`
- **System plugins:** `/Library/QuickLook/`
- **System built-in:** `/System/Library/QuickLook/` (read-only)
- **Backups:** `~/.quicklook_plugins_backup/`

## Integration with Homebrew

If you install plugins via Homebrew, they should automatically create symlinks in `~/Library/QuickLook/`. If they don't work:

1. Run diagnostic: `python3 quicklook-diagnostic.py`
2. If issues found, run fix: `python3 quicklook-fix.py`
3. Verify: `python3 quicklook-plugin-manager.py list all`

## Maintenance Schedule

Recommended regular maintenance:

1. **Weekly:** Run diagnostic
   ```bash
   python3 quicklook-diagnostic.py
   ```

2. **Monthly:** Backup all plugins
   ```bash
   python3 quicklook-plugin-manager.py backup all
   ```

3. **After system updates:** Verify plugins still work
   ```bash
   python3 quicklook-diagnostic.py
   python3 quicklook-plugin-manager.py refresh
   ```

## Troubleshooting

### Scripts won't run
Make sure they're executable:
```bash
chmod +x ~/pythons/quicklook-*.py
```

### Python not found
Ensure Python 3 is installed:
```bash
python3 --version
```

### Homebrew plugins not working
1. Check if Homebrew is in PATH: `which brew`
2. Reinstall the plugin: `brew reinstall --cask <plugin-name>`
3. Run fix script: `python3 quicklook-fix.py`

## Advanced Usage

### Custom Installation Location
The manager supports both user and system scopes. System scope requires sudo:
```bash
sudo python3 quicklook-plugin-manager.py install plugin.qlgenerator system
```

### Generate Reports
Create a detailed plugin inventory:
```bash
python3 quicklook-plugin-manager.py generate-list ~/Desktop/my_plugins.txt
```

### Combine Commands
```bash
# Backup, then fix, then verify
python3 quicklook-plugin-manager.py backup all && \
python3 quicklook-fix.py && \
python3 quicklook-diagnostic.py
```

## Support

For issues or questions:
1. Run diagnostic: `python3 quicklook-diagnostic.py`
2. Check the report: `~/pythons/QUICKLOOK_SCAN_REPORT.md`
3. Review backup directory: `~/.quicklook_plugins_backup/`

## License

These tools are provided as-is for personal use.
