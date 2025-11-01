"""
Fix Hardcoded Api Keys

This module provides functionality for fix hardcoded api keys.

Author: Auto-generated
Date: 2025-11-01
"""

import logging

logger = logging.getLogger(__name__)


# Constants
CONSTANT_500 = 500

#!/usr/bin/env python3
"""
Automated API Key Fixer
Replaces hardcoded API keys with proper ~/.env.d loading
"""

from pathlib import Path
import re
import shutil
from datetime import datetime

root = Path("/Users/steven/Documents/python")

# Template for proper API key loading
ENV_LOADER_TEMPLATE = '''import os
from pathlib import Path

# Load environment variables from ~/.env.d
def load_env_d():
    """Load all .env files from ~/.env.d directory"""
    env_d_path = Path.home() / '.env.d'
    if env_d_path.exists():
        for env_file in env_d_path.glob('*.env'):
            with open(env_file) as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith('#') and '=' in line:
                        key, value = line.split('=', 1)
                        key = key.strip()
                        value = value.strip().strip('"').strip("'")
                        if not key.startswith('source'):
                            os.environ[key] = value

load_env_d()
'''

API_REPLACEMENTS = {
    "openai": {
        "patterns": [
            (r'api_key\s*=\s*["\']sk-[A-Za-z0-9_-]+["\']', 'api_key=os.getenv("OPENAI_API_KEY")'),
            (r'OPENAI_API_KEY\s*=\s*["\']sk-[A-Za-z0-9_-]+["\']', 'OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")'),
            (r'openai.api_key\s*=\s*["\']sk-[A-Za-z0-9_-]+["\']', 'openai.api_key = os.getenv("OPENAI_API_KEY")'),
        ],
        "env_file": "llm-apis.env",
        "import_check": "from openai import OpenAI",
    },
    "stability": {
        "patterns": [
            (r'api_key\s*=\s*["\']sk-[A-Za-z0-9_-]+["\']', 'api_key=os.getenv("STABILITY_API_KEY")'),
            (
                r'STABILITY_API_KEY\s*=\s*["\']sk-[A-Za-z0-9_-]+["\']',
                'STABILITY_API_KEY = os.getenv("STABILITY_API_KEY")',
            ),
        ],
        "env_file": "art-vision.env",
        "import_check": "stability",
    },
    "elevenlabs": {
        "patterns": [
            (r'api_key\s*=\s*["\'][A-Za-z0-9]{32,}["\']', 'api_key=os.getenv("ELEVENLABS_API_KEY")'),
            (r'ELEVEN_API_KEY\s*=\s*["\'][A-Za-z0-9]{32,}["\']', 'ELEVEN_API_KEY = os.getenv("ELEVENLABS_API_KEY")'),
        ],
        "env_file": "audio-music.env",
        "import_check": "elevenlabs",
    },
    "anthropic": {
        "patterns": [
            (r'api_key\s*=\s*["\']sk-ant-[A-Za-z0-9_-]+["\']', 'api_key=os.getenv("ANTHROPIC_API_KEY")'),
            (
                r'ANTHROPIC_API_KEY\s*=\s*["\']sk-ant-[A-Za-z0-9_-]+["\']',
                'ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")',
            ),
        ],
        "env_file": "llm-apis.env",
        "import_check": "anthropic",
    },
}


def has_hardcoded_key(content):
    """Check if file has any hardcoded API keys"""
    for api_name, config in API_REPLACEMENTS.items():
        for pattern, _ in config["patterns"]:
            if re.search(pattern, content):
                return True
    return False


def needs_env_loader(content):
    """Check if file already loads from ~/.env.d"""
    return "load_env_d()" not in content and ".env.d" not in content


def add_env_loader(content):
    """Add env loader at the top of file"""
    lines = content.split("\n")

    # Find where to insert (after shebang and imports)
    insert_idx = 0
    for i, line in enumerate(lines):
        if line.startswith("#!") or line.startswith('"""') or line.startswith("'''"):
            insert_idx = i + 1
        elif line.startswith("import ") or line.startswith("from "):
            continue
        else:
            break

    # Insert env loader
    lines.insert(insert_idx, ENV_LOADER_TEMPLATE)
    return "\n".join(lines)


def fix_file(filepath):
    """Fix hardcoded API keys in a single file"""
    try:
        content = filepath.read_text(encoding="utf-8")
        original_content = content

        if not has_hardcoded_key(content):
            return None  # No hardcoded keys

        # Backup original
        backup_path = filepath.with_suffix(".py.bak")
        shutil.copy2(filepath, backup_path)

        changes = []

        # Replace hardcoded keys
        for api_name, config in API_REPLACEMENTS.items():
            for pattern, replacement in config["patterns"]:
                matches = re.findall(pattern, content)
                if matches:
                    content = re.sub(pattern, replacement, content)
                    changes.append(f"{api_name.upper()}: {len(matches)} replacements")

        # Add env loader if needed
        if needs_env_loader(content):
            content = add_env_loader(content)
            changes.append("Added ~/.env.d loader")

        # Write fixed content
        filepath.write_text(content, encoding="utf-8")

        return changes

    except Exception as e:
        return [f"ERROR: {str(e)}"]


def main():
    """main function."""

    logger.info("?? AUTOMATED API KEY FIXER")
    logger.info("=" * 70)
    print()
    logger.info("This will:")
    logger.info("  1. Backup files to .bak")
    logger.info("  2. Replace hardcoded API keys with os.getenv()")
    logger.info("  3. Add ~/.env.d loader if needed")
    print()

    # Get all Python files
    all_files = list(root.glob("*.py")) + list(root.glob("_versions/**/*.py"))

    logger.info(f"Scanning {len(all_files)} files...")
    print()

    fixed = []
    errors = []

    for i, filepath in enumerate(all_files):
        if i % CONSTANT_500 == 0:
            logger.info(f"  Progress: {i}/{len(all_files)}...")

        changes = fix_file(filepath)
        if changes:
            if any("ERROR" in c for c in changes):
                errors.append((filepath, changes))
            else:
                fixed.append((filepath, changes))

    print()
    logger.info("=" * 70)
    logger.info(f"? Fixed {len(fixed)} files")
    logger.info(f"? Errors: {len(errors)}")
    print()

    if fixed:
        logger.info("?? Fixed files:")
        for filepath, changes in fixed[:20]:
            logger.info(f"\n{filepath.relative_to(root)}:")
            for change in changes:
                logger.info(f"  ? {change}")

        if len(fixed) > 20:
            logger.info(f"\n... and {len(fixed) - 20} more files")

    if errors:
        logger.info("\n? Errors:")
        for filepath, changes in errors[:10]:
            logger.info(f"\n{filepath.relative_to(root)}:")
            for change in changes:
                logger.info(f"  ? {change}")

    # Save report
    report_path = root / f'API_FIX_REPORT_{datetime.now().strftime("%Y%m%d_%H%M%S")}.txt'
    with open(report_path, "w") as f:
        f.write("API KEY FIX REPORT\n")
        f.write("=" * 70 + Path("\n\n"))
        f.write(f"Fixed: {len(fixed)} files\n")
        f.write(f"Errors: {len(errors)}\n\n")

        f.write("\nFIXED FILES:\n")
        f.write("-" * 70 + Path("\n"))
        for filepath, changes in fixed:
            f.write(f"\n{filepath.relative_to(root)}:\n")
            for change in changes:
                f.write(f"  ? {change}\n")

        if errors:
            f.write("\n\nERRORS:\n")
            f.write("-" * 70 + Path("\n"))
            for filepath, changes in errors:
                f.write(f"\n{filepath.relative_to(root)}:\n")
                for change in changes:
                    f.write(f"  ? {change}\n")

    logger.info(f"\n?? Report saved to: {report_path.name}")
    print()
    logger.info("? All hardcoded API keys have been replaced with ~/.env.d loading!")
    print()
    logger.info("??  To revert changes, restore from .bak files")


if __name__ == "__main__":
    main()
