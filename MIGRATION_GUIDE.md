# 🔄 Migration Guide - Updating After Reorganization

## 📋 Overview

This guide helps you update your code after the reorganization. **1,303 files** were moved to new locations.

---

## 🔍 Finding Moved Files

### Method 1: Check CSV Files

**Use PARENT_AWARE_ANALYSIS.csv**:
```bash
# Find where a file moved
grep "filename.py" PARENT_AWARE_ANALYSIS.csv

# Find all files that moved from root
grep "^ROOT," PARENT_AWARE_ANALYSIS.csv | grep "apis\|data_processing\|file_operations"
```

### Method 2: Search File System

```bash
# Find a specific file
find . -name "filename.py" -type f

# Find files by pattern
find . -name "*instagram*" -type f
find . -name "*youtube*" -type f
```

---

## 🔧 Updating Imports

### Common Import Patterns

#### 1. Root Level Files → Category Folders

**Before** (file at root):
```python
# File: some_script.py (at root)
from another_script import something
import config_module
```

**After** (file moved to `apis/`):
```python
# File: apis/some_script.py
from apis.another_script import something
from config.config_module import something
# OR use relative imports
from .another_script import something
```

#### 2. tools/ Files → tools/ Subfolders

**Before** (file in `tools/`):
```python
# File: tools/some_tool.py
from tools.other_tool import something
```

**After** (file moved to `tools/apis/`):
```python
# File: tools/apis/some_tool.py
from tools.apis.other_tool import something
# OR
from tools.data.other_tool import something  # if moved to data/
```

#### 3. MEDIA_PROCESSING Files

**Before** (file in `MEDIA_PROCESSING/`):
```python
# File: MEDIA_PROCESSING/bot_script.py
from MEDIA_PROCESSING.helper import something
```

**After** (file moved to `MEDIA_PROCESSING/social_media/instagram/`):
```python
# File: MEDIA_PROCESSING/social_media/instagram/bot_script.py
from MEDIA_PROCESSING.social_media.instagram.helper import something
# OR use relative imports
from .helper import something
```

---

## 📝 Updating File Paths

### Hardcoded Paths

**Before**:
```python
script_path = "some_script.py"
config_path = "config.py"
```

**After**:
```python
script_path = "apis/some_script.py"
config_path = "config/config.py"
```

### Relative Paths

**Before**:
```python
import os
script_dir = os.path.dirname(__file__)
other_script = os.path.join(script_dir, "other_script.py")
```

**After** (if moved to subdirectory):
```python
import os
script_dir = os.path.dirname(__file__)
# Go up one level if needed
parent_dir = os.path.dirname(script_dir)
other_script = os.path.join(parent_dir, "other_script.py")
# OR use new path
other_script = os.path.join(script_dir, "..", "other_script.py")
```

---

## 🔄 Common Migration Scenarios

### Scenario 1: Script Uses Root-Level Files

**Problem**: Your script imports from root level files that were moved

**Solution**:
1. Identify which category the file moved to
2. Update import path
3. Test the script

**Example**:
```python
# OLD
from leonardo import something
from instagram_download import something

# NEW
from apis.leonardo import something
from data_processing.instagram_download import something
```

### Scenario 2: Script in tools/ Uses Other tools/

**Problem**: Script in `tools/` imports from other `tools/` files

**Solution**:
1. Check if both files are in same subfolder
2. If yes, use relative imports
3. If no, use full path from tools/

**Example**:
```python
# OLD (both in tools/)
from tools.auth import something
from tools.data_processor import something

# NEW (if auth in tools/apis/, data_processor in tools/data/)
from tools.apis.auth import something
from tools.data.data_processor import something
```

### Scenario 3: MEDIA_PROCESSING Scripts

**Problem**: Scripts in MEDIA_PROCESSING moved to subfolders

**Solution**:
1. Use relative imports within same folder
2. Use full paths for cross-folder imports

**Example**:
```python
# OLD
from MEDIA_PROCESSING.bot_comment import something
from MEDIA_PROCESSING.image_utils import something

# NEW (if in social_media/instagram/)
from .bot_comment import something  # Same folder
from MEDIA_PROCESSING.image.image_utils import something  # Different folder
```

---

## 🛠️ Automated Migration Helpers

### Script to Find Broken Imports

```python
#!/usr/bin/env python3
"""Find potentially broken imports after reorganization."""
import ast
import sys
from pathlib import Path

def find_imports(filepath):
    """Find all imports in a file."""
    try:
        with open(filepath, 'r') as f:
            tree = ast.parse(f.read())

        imports = []
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    imports.append(alias.name)
            elif isinstance(node, ast.ImportFrom):
                if node.module:
                    imports.append(node.module)
        return imports
    except:
        return []

# Check a file
file_path = Path("your_script.py")
imports = find_imports(file_path)
print(f"Imports in {file_path}:")
for imp in imports:
    print(f"  - {imp}")
```

### Script to Check if Import Target Exists

```python
#!/usr/bin/env python3
"""Check if imported modules exist after reorganization."""
import importlib.util
from pathlib import Path

def check_import(module_name, base_path):
    """Check if a module can be imported."""
    # Try to find the module file
    module_path = base_path / f"{module_name.replace('.', '/')}.py"
    if module_path.exists():
        return True

    # Try as directory with __init__.py
    module_dir = base_path / module_name.replace('.', '/')
    if (module_dir / "__init__.py").exists():
        return True

    return False

# Example usage
base = Path(".")
module = "leonardo"
exists = check_import(module, base)
print(f"{module} exists: {exists}")
```

---

## ✅ Testing After Migration

### Checklist

- [ ] Run your main scripts
- [ ] Check for import errors
- [ ] Verify file paths work
- [ ] Test functionality
- [ ] Update documentation
- [ ] Update any configuration files

### Common Issues

1. **ModuleNotFoundError**
   - **Fix**: Update import paths to new locations

2. **FileNotFoundError**
   - **Fix**: Update hardcoded file paths

3. **Relative import errors**
   - **Fix**: Adjust relative import paths

4. **Circular import issues**
   - **Fix**: May need to restructure imports

---

## 📊 Migration Statistics

- **Files moved**: 1,303 files
- **Root level**: 1,070 files → 10 categories
- **tools/**: 233 files → 4 subfolders
- **MEDIA_PROCESSING/**: 54 files → subfolders

### Files That May Need Updates

- Scripts that import from root level: ~500+ files
- Scripts that import from tools/: ~200+ files
- Scripts that import from MEDIA_PROCESSING/: ~100+ files

---

## 🔗 Resources

- **INDEX.md** - Complete directory index
- **QUICK_REFERENCE.md** - Quick lookup guide
- **PARENT_AWARE_ANALYSIS.csv** - Find where files moved
- **DEEP_FUNCTIONALITY_ANALYSIS.csv** - File functionality data

---

## 💡 Tips

1. **Start with critical scripts** - Update your most-used scripts first
2. **Use relative imports** - When possible, use relative imports within folders
3. **Test incrementally** - Update and test one script at a time
4. **Keep backups** - Have backups before making changes
5. **Use version control** - Commit changes frequently

---

*Guide for updating code after reorganization*
