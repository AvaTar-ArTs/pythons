#!/usr/bin/env python3
"""
🔧 FIX NAMING ISSUES
Fix spaces, special chars, and confusing names
"""

import re
from pathlib import Path
from datetime import datetime


class NameFixer:
    def __init__(self, pythons_dir="/Users/steven/pythons"):
        self.pythons_dir = Path(pythons_dir)
        self.renames = []

    def clean_filename(self, name):
        """Clean up a filename"""
        # Remove .py
        base = name.replace(".py", "")

        # Replace spaces with underscores
        base = base.replace(" ", "_")

        # Remove special characters (keep only letters, numbers, dash, underscore)
        base = re.sub(r"[^a-zA-Z0-9_\-]", "", base)

        # Remove trailing numbers after underscore (artifact from duplication)
        base = re.sub(r"_+$", "", base)

        # Convert to lowercase for consistency (except cleanup scripts)
        if not any(
            base.startswith(x)
            for x in [
                "DEEP_",
                "INTELLIGENT_",
                "SMART_",
                "CLEANUP_",
                "COMPREHENSIVE_",
                "AGGRESSIVE_",
                "RECURSIVE_",
                "FINAL_",
                "FIND_",
                "SUB_",
                "STRUCTURAL_",
            ]
        ):
            base = base.lower()

        # Remove consecutive underscores
        base = re.sub(r"_+", "_", base)

        # Remove leading/trailing underscores
        base = base.strip("_")

        return base + ".py"

    def find_files_to_rename(self):
        """Find all files that need renaming"""
        print("🔍 Scanning for files with naming issues...\n")

        files = [
            f
            for f in self.pythons_dir.rglob("*.py")
            if "_archive" not in str(f)
            and "2T-Xx-python" not in str(f)
            and ".venv" not in str(f)
            and ".history" not in str(f)
        ]

        for f in files:
            name = f.name
            clean_name = self.clean_filename(name)

            if name != clean_name:
                self.renames.append(
                    {
                        "original": f,
                        "original_name": name,
                        "new_name": clean_name,
                        "parent": f.parent,
                    }
                )

        print(f"Found {len(self.renames)} files that need renaming\n")
        return len(self.renames)

    def execute_renames(self):
        """Execute the renames"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        log_file = self.pythons_dir / f"RENAME_LOG_{timestamp}.txt"

        renamed = 0
        skipped = 0
        errors = []

        print("🔧 Renaming files...\n")

        with open(log_file, "w") as log:
            log.write("RENAME LOG\n")
            log.write("=" * 70 + "\n\n")

            for item in self.renames:
                original = item["original"]
                new_name = item["new_name"]
                parent = item["parent"]
                new_path = parent / new_name

                # Skip if target exists
                if new_path.exists() and new_path != original:
                    skipped += 1
                    log.write(f"SKIP: {original.name} → {new_name} (exists)\n")
                    continue

                try:
                    original.rename(new_path)
                    renamed += 1
                    log.write(f"✅ {original.name} → {new_name}\n")

                    if renamed % 50 == 0:
                        print(f"   ... renamed {renamed} files")

                except Exception as e:
                    errors.append(f"{original.name}: {e}")
                    log.write(f"❌ {original.name}: {e}\n")

        print(f"\n✅ Renamed {renamed} files")
        print(f"⚠️  Skipped {skipped} files (target exists)")

        if errors:
            print(f"❌ Errors: {len(errors)}")
            for err in errors[:10]:
                print(f"   {err}")

        print(f"\n📄 Log saved: {log_file.name}")

        return renamed, skipped, errors


def main():
    print("""
╔═══════════════════════════════════════════════════════════════════╗
║     🔧 FIX NAMING ISSUES                                          ║
║     Clean up spaces, special chars, and confusing names          ║
╚═══════════════════════════════════════════════════════════════════╝
""")

    fixer = NameFixer()
    count = fixer.find_files_to_rename()

    if count == 0:
        print("✅ All filenames are clean!")
        return

    print("This will fix:")
    print("  • Replace spaces with underscores")
    print("  • Remove special characters")
    print("  • Convert to lowercase (except cleanup scripts)")
    print("  • Clean up artifacts from deduplication")
    print()

    confirm = input("Type 'FIX' to rename files: ")

    if confirm == "FIX":
        renamed, skipped, errors = fixer.execute_renames()
        print(f"\n🎉 Naming cleanup complete! {renamed} files renamed.")
    else:
        print("\n❌ Cancelled")


if __name__ == "__main__":
    main()
