#!/usr/bin/env python3
"""
Update run/ entry points to match new feature-based script organization.

Current run/:
- organization.py → scripts/organization/
- consolidation.py → scripts/consolidation/ (now core)
- transcription.py → scripts/transcription/ (now core)
- verification.py → scripts/verification/ (now verify)
- backup.py → scripts/backup/
- data.py → scripts/data/

New run/ should match features:
- core.py → scripts/core/ (organize, consolidate, transcribe)
- uuid.py → scripts/uuid/
- album.py → scripts/album/
- data.py → scripts/data/
- media.py → scripts/media/
- web.py → scripts/web/
- backup.py → scripts/backup/
- verify.py → scripts/verify/
- specialized.py → scripts/specialized/
- apply.py → scripts/apply/
"""

from pathlib import Path

PROJECT = Path(__file__).parent
RUN_DIR = PROJECT / "run"

# New entry points matching feature-based organization
ENTRY_POINTS = {
    "core": "scripts/core/",
    "uuid": "scripts/uuid/",
    "album": "scripts/album/",
    "data": "scripts/data/",
    "media": "scripts/media/",
    "web": "scripts/web/",
    "backup": "scripts/backup/",
    "verify": "scripts/verify/",
    "specialized": "scripts/specialized/",
    "apply": "scripts/apply/",
}


def create_entry_point(feature: str, script_dir: str) -> str:
    """Create a simple entry point."""
    return f"""#!/usr/bin/env python3
\"\"\"
{feature.title()} scripts entry point.

Available scripts in {script_dir}:
Run: python run/{feature}.py
\"\"\"

print("Available {feature} scripts:")
print("Run individual scripts with: python scripts/{script_dir}/<script_name>")
"""


def main():
    print("Updating run/ entry points for feature-based organization")
    print("=" * 60)

    updated = 0

    # Remove old entry points
    old_entries = [
        "organization.py",
        "consolidation.py",
        "transcription.py",
        "verification.py",
    ]
    for old in old_entries:
        old_path = RUN_DIR / old
        if old_path.exists():
            old_path.unlink()
            print(f"Removed old entry point: {old}")

    # Create new entry points
    for feature, script_dir in ENTRY_POINTS.items():
        entry_script = RUN_DIR / f"{feature}.py"
        entry_content = create_entry_point(feature, script_dir)

        with open(entry_script, "w") as f:
            f.write(entry_content)

        entry_script.chmod(0o755)
        print(f"Created entry point: run/{feature}.py → {script_dir}")
        updated += 1

    print("\nSummary:")
    print(f"  Entry points updated: {updated}")
    print("  Usage: python run/<feature>.py")


if __name__ == "__main__":
    main()
