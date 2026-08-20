# Why You Have Both ~/.local and ~/Library/Python

## The Problem

You have Python packages installed in **two different locations**:

1. **`~/.local/lib/python*/site-packages`** - Linux/Unix standard (2.5 GB)
2. **`~/Library/Python/*/lib/python/site-packages`** - macOS standard (2.3 GB)

This is **wasting space** because:
- Packages might be duplicated in both locations
- Python might be looking in the wrong place
- You're maintaining two separate package installations

## Why This Happened

### macOS Default Behavior
On macOS, Python uses `~/Library/Python/X.Y/lib/python/site-packages` as the default user site-packages directory. This is the **correct** location for macOS.

### How `.local` Got Created
The `~/.local` directory was likely created because:
1. **PYTHONUSERBASE environment variable** was set to `~/.local`
2. **pip install --user --prefix ~/.local** was used
3. **Some installer or script** explicitly set the user base to `.local`
4. **Cross-platform tools** that default to `.local` (Linux standard)

## Current Situation

### Python 3.12
- **Active location**: `~/Library/Python/3.12/lib/python/site-packages` ✅ (correct)
- **Unused location**: `~/.local/lib/python3.12/site-packages` ❌ (waste)

### Python 3.11  
- **Active location**: `~/Library/Python/3.11/lib/python/site-packages` ✅ (correct)
- **Unused location**: `~/.local/lib/python3.11/site-packages` ❌ (waste)

## The Solution

Since Python is using `~/Library/Python` (the macOS standard), the `~/.local/lib/python*/site-packages` directories are likely **not being used** and can be safely removed.

**You can safely delete:**
```bash
rm -rf ~/.local/lib/python3.11/site-packages  # ~2.5 GB
rm -rf ~/.local/lib/python3.12/site-packages  # (if exists)
```

This would save **~2.5 GB** immediately!

## Verification

To check which location Python actually uses:
```bash
python3.12 -m site
python3.11 -m site
```

Look for `USER_SITE` - that's where Python installs packages with `pip install --user`.

## Recommendation

1. **Delete `~/.local/lib/python*/site-packages`** - These aren't being used
2. **Keep `~/Library/Python`** - This is the active location
3. **Keep `~/.local/bin`** - This might have useful scripts
4. **Keep `~/.local/share`** - This has application data (Claude, Cursor, etc.)

This should free up **~2.5 GB** immediately!
