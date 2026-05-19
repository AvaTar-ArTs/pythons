#!/usr/bin/env python3
"""
⚡ FAST SIMILARITY SCANNER
Quick detection of similar files using function/class signatures
"""

import ast
from pathlib import Path
from collections import defaultdict
import shutil
from datetime import datetime


class FastSimilarityScanner:
    def __init__(self, pythons_dir="/Users/steven/pythons"):
        self.pythons_dir = Path(pythons_dir)

    def get_signature(self, filepath):
        """Get quick signature"""
        sig = {"path": filepath, "size": 0, "funcs": [], "classes": [], "imports": []}

        try:
            sig["size"] = filepath.stat().st_size

            with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
                content = f.read()

            tree = ast.parse(content)

            for node in ast.walk(tree):
                if isinstance(node, ast.FunctionDef):
                    sig["funcs"].append(node.name)
                elif isinstance(node, ast.ClassDef):
                    sig["classes"].append(node.name)
                elif isinstance(node, (ast.Import, ast.ImportFrom)):
                    if isinstance(node, ast.Import):
                        for alias in node.names:
                            sig["imports"].append(alias.name.split(".")[0])
                    elif node.module:
                        sig["imports"].append(node.module.split(".")[0])
        except:
            pass

        return sig

    def scan_files(self):
        """Scan all files"""
        print("⚡ FAST SIMILARITY SCAN\n")

        files = [
            f
            for f in self.pythons_dir.rglob("*.py")
            if "_archive" not in str(f)
            and "2T-Xx-python" not in str(f)
            and ".venv" not in str(f)
            and ".history" not in str(f)
        ]

        print(f"📂 Scanning {len(files)} files...\n")

        sigs = []
        for i, f in enumerate(files, 1):
            sig = self.get_signature(f)
            sigs.append(sig)

            if i % 1000 == 0:
                print(f"   ... scanned {i} files")

        print(f"\n✅ Scanned {len(sigs)} files\n")
        return sigs

    def find_duplicates(self, sigs):
        """Find duplicates by structure"""
        print("🔍 Grouping by structure...\n")

        # Group by function signature
        by_funcs = defaultdict(list)
        for sig in sigs:
            if len(sig["funcs"]) >= 3:  # At least 3 functions
                func_sig = tuple(sorted(sig["funcs"]))
                by_funcs[func_sig].append(sig)

        func_dupes = [group for group in by_funcs.values() if len(group) >= 3]
        print(f"Found {len(func_dupes)} groups with same functions (3+ files)\n")

        # Group by imports (same imports = similar purpose)
        by_imports = defaultdict(list)
        for sig in sigs:
            if len(sig["imports"]) >= 5:  # At least 5 imports
                import_sig = tuple(sorted(set(sig["imports"])))
                by_imports[import_sig].append(sig)

        import_dupes = [group for group in by_imports.values() if len(group) >= 5]
        print(f"Found {len(import_dupes)} groups with same imports (5+ files)\n")

        # Group by class signature
        by_classes = defaultdict(list)
        for sig in sigs:
            if len(sig["classes"]) >= 2:
                class_sig = tuple(sorted(sig["classes"]))
                by_classes[class_sig].append(sig)

        class_dupes = [group for group in by_classes.values() if len(group) >= 3]
        print(f"Found {len(class_dupes)} groups with same classes (3+ files)\n")

        # Combine all groups (remove overlaps)
        all_groups = func_dupes + import_dupes + class_dupes

        return all_groups

    def remove_duplicates(self, groups):
        """Remove duplicates keeping best"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        archive_dir = self.pythons_dir / "_archive" / f"fast-similarity-{timestamp}"
        archive_dir.mkdir(parents=True, exist_ok=True)

        print("🗑️  Removing similar files (keeping best)...\n")

        removed = 0

        for group in groups:
            # Score each file
            scored = []
            for sig in group:
                score = sig["size"] / 100
                score += len(sig["funcs"]) * 5
                score += len(sig["classes"]) * 10

                # Prefer clean names
                name = sig["path"].name
                if "_from_" not in name and "DOCS_PYTHON_" not in name:
                    score += 50
                if "_copy" not in name and "duplicate" not in name:
                    score += 50

                scored.append((sig, score))

            # Sort
            scored.sort(key=lambda x: x[1], reverse=True)

            # Keep best, remove rest
            scored[0][0]
            to_remove = [sig for sig, _ in scored[1:]]

            for sig in to_remove:
                try:
                    # Archive
                    rel = sig["path"].relative_to(self.pythons_dir)
                    archive_path = archive_dir / rel
                    archive_path.parent.mkdir(parents=True, exist_ok=True)
                    shutil.copy2(sig["path"], archive_path)

                    # Delete
                    sig["path"].unlink()
                    removed += 1

                    if removed % 50 == 0:
                        print(f"   ... removed {removed} files")
                except:
                    pass

        print(f"\n✅ Removed {removed} similar files\n")
        return removed


def main():
    print("""
╔═══════════════════════════════════════════════════════════════════╗
║     ⚡ FAST SIMILARITY SCANNER                                    ║
║     Reduce 4,720 files by removing similar content               ║
╚═══════════════════════════════════════════════════════════════════╝
""")

    scanner = FastSimilarityScanner()

    # Scan
    sigs = scanner.scan_files()

    # Find similar
    groups = scanner.find_duplicates(sigs)

    # Summary
    print("=" * 70)
    total_removable = sum(len(g) - 1 for g in groups)
    print(f"📊 Found {total_removable} files that can be removed")
    print("=" * 70)

    # Show samples
    print("\n🔥 TOP 10 SIMILARITY GROUPS:\n")
    for i, group in enumerate(sorted(groups, key=len, reverse=True)[:10], 1):
        print(f"{i:2}. {len(group)} similar files")
        for sig in group[:4]:
            print(f"    • {sig['path'].name}")
        if len(group) > 4:
            print(f"    ... and {len(group) - 4} more")
        print()

    if groups:
        confirm = input("Type 'CLEAN' to remove: ")
        if confirm == "CLEAN":
            removed = scanner.remove_duplicates(groups)
            print(f"🎉 Removed {removed} similar files!")
        else:
            print("\n❌ Cancelled")


if __name__ == "__main__":
    main()
