import csv
import importlib.util
import sys
import tempfile
import unittest
from pathlib import Path


SCRIPT_DIR = Path(__file__).resolve().parent
SCRIPT_PATH = SCRIPT_DIR / "doc-source-enriched.py"
sys.path.insert(0, str(SCRIPT_DIR))
spec = importlib.util.spec_from_file_location("doc_source_enriched", SCRIPT_PATH)
if spec is None or spec.loader is None:
    raise RuntimeError(f"Could not load {SCRIPT_PATH}")
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


class DocSourceEnrichedTests(unittest.TestCase):
    def test_root_directory_name_does_not_classify_every_file_as_skill(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            (root / "README.md").write_text("A plain reference document.\n")
            rows = module.scan_and_enrich([str(root)])

        row = rows[0]
        self.assertNotEqual(row["intelligent_category"], "skill")
        self.assertLess(row["confidence_score"], 0.95)

    def test_missing_directory_is_rejected(self):
        with self.assertRaises(ValueError):
            module.scan_and_enrich(["/definitely/not/a/real/directory"])

    def test_sensitive_files_are_not_read_or_hashed(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            secret = root / ".env"
            secret.write_text("API_KEY=do-not-hash\n")
            row = module.scan_and_enrich([str(root)])[0]

        self.assertTrue(row["sensitive_skipped"])
        self.assertEqual(row["content_hash"], "")
        self.assertEqual(row["encoding"], "sensitive-skipped")

    def test_existing_generated_output_is_excluded(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            generated = root / "agent-skills-meta.csv"
            generated.write_text("old,generated,inventory\n")
            rows = module.scan_and_enrich([str(root)])

        self.assertEqual(rows, [])

    def test_reference_inventory_names_are_excluded(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            (root / "pythons-meta.csv").write_text("full_path\n")
            (root / "docs-09-04-23:23.csv").write_text("Filename\n")
            (root / "notes.md").write_text("Keep this document.\n")
            rows = module.scan_and_enrich([str(root)])

        self.assertEqual([row["filename"] for row in rows], ["notes.md"])

    def test_overlapping_roots_do_not_duplicate_rows(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            child = root / "child"
            child.mkdir()
            (child / "notes.md").write_text("One row only.\n")
            rows = module.scan_and_enrich([str(root), str(child)])

        self.assertEqual(len(rows), 1)

    def test_file_symlink_is_skipped(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            source = root / "source.md"
            source.write_text("source\n")
            link = root / "linked.md"
            try:
                link.symlink_to(source)
            except (OSError, NotImplementedError):
                self.skipTest("symlinks unavailable")
            rows = module.scan_and_enrich([str(root)])

        self.assertEqual([row["filename"] for row in rows], ["source.md"])

    def test_symlinked_root_is_rejected_by_default(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            target = root / "target"
            link = root / "linked-root"
            target.mkdir()
            link.symlink_to(target, target_is_directory=True)

            with self.assertRaises(ValueError):
                module.scan_and_enrich([str(link)])

    def test_duplicate_content_remains_visible_and_is_grouped(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            (root / "one.md").write_text("same content\n")
            (root / "two.md").write_text("same content\n")
            rows = module.scan_and_enrich([str(root)])
            module.annotate_duplicates(rows)
            output = root / "duplicates.csv"
            module.write_enhanced_csv(str(output), rows)
            with output.open(newline="", encoding="utf-8") as handle:
                written = list(csv.DictReader(handle))
            sidecar = output.with_suffix(".duplicates.csv")
            with sidecar.open(newline="", encoding="utf-8") as handle:
                members = list(csv.DictReader(handle))

        self.assertEqual(len(written), 2)
        self.assertEqual({row["duplicate_count"] for row in written}, {"2"})
        self.assertEqual(len({row["duplicate_group"] for row in written}), 1)
        self.assertEqual({row["duplicate_basis"] for row in written}, {"full_content_sha256"})
        self.assertEqual({row["same_filename_in_group"] for row in written}, {"no"})
        self.assertEqual({row["duplicate_paths"] for row in written}, {""})
        self.assertEqual(len(members), 2)
        self.assertEqual({row["duplicate_count"] for row in members}, {"2"})
        self.assertEqual({row["relative_path"] for row in members}, {"one.md", "two.md"})

    def test_large_duplicate_group_does_not_repeat_paths_in_main_csv(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            for index in range(40):
                (root / f"empty-{index}.txt").write_text("")
            rows = module.scan_and_enrich([str(root)])
            module.annotate_duplicates(rows)
            output = root / "result.csv"
            module.write_enhanced_csv(str(output), rows)

            main_text = output.read_text(encoding="utf-8")
            sidecar = output.with_suffix(".duplicates.csv")
            with sidecar.open(newline="", encoding="utf-8") as handle:
                members = list(csv.DictReader(handle))

        self.assertLess(len(main_text), 100_000)
        self.assertEqual(len(members), 40)

    def test_legitimate_names_containing_exclusion_words_are_kept(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            (root / "distillation.py").write_text("print(1)\n")
            (root / "targeting.py").write_text("print(2)\n")
            rows = module.scan_and_enrich([str(root)])

        self.assertEqual(
            {row["filename"] for row in rows},
            {"distillation.py", "targeting.py"},
        )

    def test_hash_is_full_sha256(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            (root / "data.txt").write_text("stable content\n")
            row = module.scan_and_enrich([str(root)])[0]

        self.assertEqual(len(row["content_hash"]), 64)

    def test_quality_defaults_are_not_claimed_as_measured(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            (root / "README.md").write_text("Documentation.\n")
            row = module.scan_and_enrich([str(root)])[0]

        self.assertEqual(row["status"], "unverified")
        self.assertEqual(row["maturity_level"], "unknown")
        self.assertEqual(row["test_coverage"], "")
        self.assertEqual(row["code_standards"], "")
        self.assertEqual(row["security_score"], "")

    def test_csv_formula_values_are_neutralized(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            (root / "=formula.txt").write_text("content\n")
            output = root / "result.csv"
            rows = module.scan_and_enrich([str(root)])
            module.write_enhanced_csv(str(output), rows)
            with output.open(newline="", encoding="utf-8") as handle:
                row = next(csv.DictReader(handle))

        self.assertEqual(row["filename"], "'=formula.txt")

    def test_report_paths_are_relative_by_default(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            (root / "notes.md").write_text("Documentation.\n")
            rows = module.scan_and_enrich([str(root)])
            output = root / "report.csv"
            module.write_enhanced_csv(str(output), rows)
            with output.open(newline="", encoding="utf-8") as handle:
                row = next(csv.DictReader(handle))

        self.assertEqual(row["full_path"], "notes.md")
        self.assertNotIn(temp_dir, row["full_path"])

    def test_absolute_report_paths_are_opt_in(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            (root / "notes.md").write_text("Documentation.\n")
            rows = module.scan_and_enrich([str(root)])
            output = root / "report.csv"
            module.write_enhanced_csv(str(output), rows, absolute_paths=True)
            with output.open(newline="", encoding="utf-8") as handle:
                row = next(csv.DictReader(handle))

        self.assertEqual(row["full_path"], str((root / "notes.md").resolve()))


if __name__ == "__main__":
    unittest.main()
