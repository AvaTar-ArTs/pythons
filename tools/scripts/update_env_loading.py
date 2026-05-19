#!/usr/bin/env python3
"""
Batch update script to add sophisticated ~/.env.d/ loading pattern to all Python files
"""

import re
from pathlib import Path
from typing import Tuple

# The sophisticated load_env_d() pattern
ENV_LOADER_CODE = "\'"# Load API keys from ~/.env.d/ (best practice - handles export statements, quotes, comments)
from pathlib import Path as PathLib

def load_env_d():
    """Load all .env files from ~/.env.d directory (sophisticated pattern from youtube-load.py)"""
    env_d_path = PathLib.home() / ".env.d"
    if env_d_path.exists():
        for env_file in env_d_path.glob("*.env"):
            try:
                with open(env_file) as f:
                    for line in f:
                        line = line.strip()
                        if line and not line.startswith("#") and "=" in line:
                            # Handle export statements
                            if line.startswith("export "):
                                line = line[7:]
                            key, value = line.split("=", 1)
                            key = key.strip()
                            value = value.strip().strip('\'').strip("\'")
                            # Skip source statements
                            if not key.startswith("source"):
                                os.environ[key] = value
            except Exception as e:
                # Logger not initialized yet, use print
                print(f"Warning: Error loading {env_file}: {e}")

load_env_d()

# Also load from ~/.env as fallback using dotenv
try:
    from dotenv import load_dotenv
    load_dotenv(os.path.expanduser("~/.env"))
except ImportError:
    pass
"\'"


def needs_update(file_path: Path) -> bool:
    """Check if file needs the sophisticated env loading pattern"""
    try:
        content = file_path.read_text(encoding="utf-8")

        # Skip if already has sophisticated pattern
        if "load_env_d()" in content and "Handle export statements" in content:
            return False

        # Check if it uses API keys or env vars
        has_api_usage = bool(
            re.search(
                r"OPENAI_API_KEY|ASSEMBLYAI|ELEVENLABS|DEEPGRAM|PERPLEXITY|os\.getenv|load_dotenv",
                content,
                re.IGNORECASE,
            )
        )

        return has_api_usage
    except Exception as e:
        print(f"Error reading {file_path}: {e}")
        return False


def find_insertion_point(content: str) -> int:
    """Find the best place to insert the env loading code"""
    lines = content.split("\n")

    # Strategy 1: After shebang and docstring, before other imports
    for i, line in enumerate(lines):
        # Skip shebang
        if i == 0 and line.startswith("#!"):
            continue
        # Skip docstring
        if line.strip().startswith('\"\'"') or line.strip().startswith("\'"'""):
            # Find end of docstring
            quote_char = line.strip()[0:3]
            j = i + 1
            while j < len(lines) and quote_char not in lines[j]:
                j += 1
            if j < len(lines):
                i = j
            continue
        # Skip blank lines
        if not line.strip():
            continue
        # If we hit an import, insert before it
        if line.strip().startswith("import ") or line.strip().startswith("from "):
            # But check if there's already env loading nearby
            for check_i in range(max(0, i - 5), i):
                if "load_env" in lines[check_i] or ".env.d" in lines[check_i]:
                    return None  # Already has env loading
            return i

    # Strategy 2: After first few imports if no docstring
    for i in range(min(10, len(lines))):
        if lines[i].strip().startswith("import os") or "os" in lines[i]:
            return i + 1

    # Strategy 3: After first import block
    for i, line in enumerate(lines):
        if line.strip().startswith("import ") or line.strip().startswith("from "):
            # Find end of import block
            j = i + 1
            while j < len(lines) and (
                lines[j].strip().startswith("import ")
                or lines[j].strip().startswith("from ")
                or not lines[j].strip()
            ):
                j += 1
            return j

    # Fallback: insert at line 5
    return min(5, len(lines))


def update_file(file_path: Path) -> Tuple[bool, str]:
    """Update a single file with the env loading pattern"""
    try:
        content = file_path.read_text(encoding="utf-8")

        # Check if already has sophisticated pattern
        if "load_env_d()" in content and "Handle export statements" in content:
            return False, "Already has sophisticated pattern"

        # Check if has simple pattern that needs upgrade
        has_simple_pattern = bool(
            re.search(
                r"env_dir.*\.env\.d|PathLib\.home.*\.env\.d", content, re.IGNORECASE
            )
        )

        # Find insertion point
        insert_pos = find_insertion_point(content)
        if insert_pos is None:
            return False, "Could not find insertion point or already has env loading"

        # Ensure os is imported
        if "import os" not in content and "from os import" not in content:
            # Add os import if needed
            lines = content.split("\n")
            # Find first import line
            for i, line in enumerate(lines):
                if line.strip().startswith("import ") or line.strip().startswith(
                    "from "
                ):
                    if "os" not in line:
                        lines.insert(i, "import os")
                        content = "\n".join(lines)
                        insert_pos += 1
                    break

        # Insert the env loading code
        lines = content.split("\n")
        lines.insert(insert_pos, ENV_LOADER_CODE)

        # If there's a simple pattern, try to remove it
        if has_simple_pattern:
            # Remove old simple pattern
            new_lines = []
            skip_next = False
            for i, line in enumerate(lines):
                if skip_next:
                    skip_next = False
                    continue
                # Skip old env.d loading pattern
                if (
                    'env_dir = PathLib.home() / ".env.d"' in line
                    or 'env_dir = Path.home() / ".env.d"' in line
                ):
                    # Skip this block
                    j = i
                    while j < len(lines) and (
                        "load_dotenv" in lines[j]
                        or "env_dir" in lines[j]
                        or not lines[j].strip()
                    ):
                        j += 1
                    skip_next = j > i
                    continue
                new_lines.append(line)
            lines = new_lines

        # Write updated content
        file_path.write_text("\n".join(lines), encoding="utf-8")
        return True, "Updated successfully"

    except Exception as e:
        return False, f"Error: {str(e)}"


def main():
    """Main function to update all files"""
    pythons_dir = Path.home() / "pythons"

    # Get list of files to update (including subdirectories)
    files_to_update = []

    # Root level files
    for py_file in pythons_dir.glob("*.py"):
        if needs_update(py_file):
            files_to_update.append(py_file)

    # Subdirectories (excluding certain paths)
    exclude_paths = {
        ".git",
        "axolotl-main",
        "site",
        ".ruff_cache",
        ".claude",
        ".context7",
        ".aider.tags.cache.v4",
        "__pycache__",
        ".venv",
    }

    for py_file in pythons_dir.rglob("*.py"):
        # Skip excluded paths
        if any(excluded in str(py_file) for excluded in exclude_paths):
            continue
        # Skip if already in list (root level)
        if py_file in files_to_update:
            continue
        if needs_update(py_file):
            files_to_update.append(py_file)

    print(f"Found {len(files_to_update)} files to update")

    updated = 0
    skipped = 0
    errors = 0

    for file_path in files_to_update:
        success, message = update_file(file_path)
        if success:
            updated += 1
            print(f"✓ {file_path.name}")
        else:
            if "Error" in message:
                errors += 1
                print(f"✗ {file_path.name}: {message}")
            else:
                skipped += 1
                print(f"- {file_path.name}: {message}")

    print(f"\nSummary: {updated} updated, {skipped} skipped, {errors} errors")


if __name__ == "__main__":
    main()
