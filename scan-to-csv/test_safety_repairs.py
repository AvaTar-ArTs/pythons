from __future__ import annotations

import importlib.util
import csv
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


all_for_csv = load_module("all_for_csv_repair", HERE / "all_for_csv.py")
all_scan_v2 = load_module("all_scan_v2_repair", HERE / "all_scan_v2.py")
enforce = load_module(
    "enforce_csv_cleanup_repair",
    HERE.parent / "seLLeable-item-rxtractor" / "enforce_csv_cleanup.py",
)


class SafetyRepairTests(unittest.TestCase):
    def test_backup_cleanup_preview_does_not_remove_files(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            backup = root / "old.bak"
            backup.write_text("keep for preview")

            all_for_csv.cleanup_backups([str(root)], dry_run=True)

            self.assertTrue(backup.exists())

    def test_backup_cleanup_apply_removes_only_after_explicit_flag(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            backup = root / "old.bak"
            backup.write_text("remove")

            all_for_csv.cleanup_backups([str(root)], dry_run=False)

            self.assertFalse(backup.exists())

    def test_v2_deduplication_chooses_lexicographically_first_path(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "b.txt").write_text("same")
            (root / "a.txt").write_text("same")
            output = root / "inventory.csv"
            a_path = str(root / "a.txt")

            all_scan_v2.scan_and_write(
                [str(root)],
                str(output),
                enable_dedup=True,
                enable_media=False,
                max_workers=2,
            )

            with output.open(newline="", encoding="utf-8") as handle:
                rows = list(csv.DictReader(handle))
            duplicate = next(row for row in rows if row["Original Path"] == str(root / "b.txt"))
            self.assertEqual(duplicate["Duplicate Of"], a_path)

    def test_v2_skips_symlinked_files(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            target = root / "target.txt"
            link = root / "link.txt"
            target.write_text("target")
            link.symlink_to(target)

            row = all_scan_v2.scan_one(str(link), enable_media=False)

            self.assertIsNone(row)

    def test_v2_rejects_symlinked_root_by_default(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            target = root / "target"
            link = root / "linked-root"
            target.mkdir()
            link.symlink_to(target, target_is_directory=True)

            with self.assertRaises(ValueError):
                all_scan_v2.scan_and_write(
                    [str(link)], str(root / "inventory.csv"), enable_media=False
                )

    def test_music_enforcement_is_plan_only_by_default(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            mp3 = root / "unmatched.mp3"
            mp3.write_bytes(b"not a real mp3")
            tracks = {
                "known": {
                    "title": "Known",
                    "safe_album": "Known",
                    "norm_title": "known",
                    "norm_album": "known",
                }
            }
            files = [{"path": str(mp3), "filename": mp3.name, "norm": "unmatched mp3", "parent": root.name}]

            stats = enforce.enforce_csv(tracks, files, apply=False, extras_dir=root / "_EXTRAS")

            self.assertTrue(mp3.exists())
            self.assertEqual(stats["moved_to_extras"], 0)
            self.assertEqual(len(stats["planned_files"]), 1)

    def test_music_enforcement_uses_custom_directory_for_conflicts(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            source = root / "source.mp3"
            extras = root / "custom-extras"
            extras.mkdir()
            (extras / source.name).write_bytes(b"existing")
            source.write_bytes(b"new")
            files = [{
                "path": str(source),
                "filename": source.name,
                "norm": "source mp3",
                "parent": root.name,
            }]

            stats = enforce.enforce_csv({}, files, extras_dir=extras)
            changeset = root / "changeset.json"
            enforce._write_changeset(changeset, stats["planned_files"])
            self.assertEqual(stats["planned_files"][0]["status"], "planned")
            self.assertEqual(
                stats["planned_files"][0]["rollback"]["destination"], str(source)
            )
            applied = enforce.apply_changeset(changeset)

            self.assertEqual(applied["entries"][0]["status"], "applied")
            self.assertEqual(applied["entries"][0]["filename"], source.name)
            self.assertTrue((extras / "source_1.mp3").exists())
            self.assertFalse(source.exists())

    def test_changeset_apply_and_rollback_restore_original_file(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            source = root / "source.mp3"
            extras = root / "extras"
            source.write_bytes(b"original")
            files = [{
                "path": str(source),
                "filename": source.name,
                "norm": "source mp3",
                "parent": root.name,
            }]

            stats = enforce.enforce_csv({}, files, extras_dir=extras)
            changeset = root / "changeset.json"
            enforce._write_changeset(changeset, stats["planned_files"])
            applied = enforce.apply_changeset(changeset)

            self.assertFalse(source.exists())
            self.assertTrue((extras / source.name).exists())
            self.assertEqual(applied["status"], "applied")
            self.assertEqual(applied["entries"][0]["status"], "applied")

            rolled_back = enforce.rollback_changeset(changeset)

            self.assertTrue(source.exists())
            self.assertEqual(source.read_bytes(), b"original")
            self.assertFalse((extras / source.name).exists())
            self.assertEqual(rolled_back["status"], "rolled_back")

    def test_changeset_refuses_source_identity_changes(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            source = root / "source.mp3"
            source.write_bytes(b"original")
            files = [{
                "path": str(source),
                "filename": source.name,
                "norm": "source mp3",
                "parent": root.name,
            }]

            stats = enforce.enforce_csv({}, files, extras_dir=root / "extras")
            changeset = root / "changeset.json"
            enforce._write_changeset(changeset, stats["planned_files"])
            source.write_bytes(b"changed")

            with self.assertRaises(ValueError):
                enforce.apply_changeset(changeset)

            self.assertTrue(source.exists())
            self.assertFalse((root / "extras" / source.name).exists())

    def test_enforcement_cli_uses_plan_apply_rollback_lifecycle(self) -> None:
        script = HERE.parent / "seLLeable-item-rxtractor" / "enforce_csv_cleanup.py"
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            disco = root / "disco"
            reports = root / "reports"
            disco.mkdir()
            source = disco / "unmatched.mp3"
            source.write_bytes(b"audio")
            catalog = root / "catalog.csv"
            catalog.write_text("ID,Title\nknown,Known Track\n", encoding="utf-8")
            changeset = root / "changeset.json"
            common = [
                sys.executable,
                str(script),
                "--csv", str(catalog),
                "--disco", str(disco),
                "--report-dir", str(reports),
                "--changeset", str(changeset),
            ]

            planned = subprocess.run(common, capture_output=True, text=True, check=False)
            self.assertEqual(planned.returncode, 0, planned.stderr)
            self.assertTrue(changeset.exists())
            self.assertTrue(source.exists())

            applied = subprocess.run(common + ["--apply"], capture_output=True, text=True, check=False)
            self.assertEqual(applied.returncode, 0, applied.stderr)
            self.assertFalse(source.exists())

            rolled_back = subprocess.run(common + ["--rollback"], capture_output=True, text=True, check=False)
            self.assertEqual(rolled_back.returncode, 0, rolled_back.stderr)
            self.assertTrue(source.exists())


if __name__ == "__main__":
    unittest.main()
