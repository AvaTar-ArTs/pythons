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


if __name__ == "__main__":
    unittest.main()
