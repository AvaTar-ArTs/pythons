#!/usr/bin/env python3
"""
Tests for product bundle creation.
Following TDD: These tests should FAIL first, then we implement to make them pass.
"""

import pytest
import tempfile
import shutil
from pathlib import Path
import sys

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))


class TestProductBundleCreation:
    """Test that product bundles are created with correct structure."""

    @pytest.fixture
    def products_dir(self):
        """Return the products directory path."""
        return Path(__file__).parent.parent / "products"

    def test_bundle_1_code_quality_exists(self, products_dir):
        """Bundle 1: Code Quality Toolkit should exist."""
        bundle_path = products_dir / "bundle-1-code-quality"
        assert bundle_path.exists(), f"Bundle 1 not found at {bundle_path}"

    def test_bundle_1_has_readme(self, products_dir):
        """Bundle 1 should have a README.md."""
        readme = products_dir / "bundle-1-code-quality" / "README.md"
        assert readme.exists(), "Bundle 1 missing README.md"
        assert readme.stat().st_size > 100, "Bundle 1 README too short"

    def test_bundle_1_has_requirements(self, products_dir):
        """Bundle 1 should have requirements.txt."""
        reqs = products_dir / "bundle-1-code-quality" / "requirements.txt"
        assert reqs.exists(), "Bundle 1 missing requirements.txt"

    def test_bundle_1_has_license(self, products_dir):
        """Bundle 1 should have LICENSE file."""
        license_file = products_dir / "bundle-1-code-quality" / "LICENSE"
        assert license_file.exists(), "Bundle 1 missing LICENSE"

    def test_bundle_2_social_media_exists(self, products_dir):
        """Bundle 2: Social Media Automation should exist."""
        bundle_path = products_dir / "bundle-2-social-media"
        assert bundle_path.exists(), f"Bundle 2 not found at {bundle_path}"

    def test_bundle_2_has_readme(self, products_dir):
        """Bundle 2 should have a README.md."""
        readme = products_dir / "bundle-2-social-media" / "README.md"
        assert readme.exists(), "Bundle 2 missing README.md"
        assert readme.stat().st_size > 100, "Bundle 2 README too short"

    def test_bundle_2_has_requirements(self, products_dir):
        """Bundle 2 should have requirements.txt."""
        reqs = products_dir / "bundle-2-social-media" / "requirements.txt"
        assert reqs.exists(), "Bundle 2 missing requirements.txt"

    def test_bundle_3_ai_toolkit_exists(self, products_dir):
        """Bundle 3: AI Integration Toolkit should exist."""
        bundle_path = products_dir / "bundle-3-ai-toolkit"
        assert bundle_path.exists(), f"Bundle 3 not found at {bundle_path}"

    def test_bundle_3_has_readme(self, products_dir):
        """Bundle 3 should have a README.md."""
        readme = products_dir / "bundle-3-ai-toolkit" / "README.md"
        assert readme.exists(), "Bundle 3 missing README.md"
        assert readme.stat().st_size > 100, "Bundle 3 README too short"

    def test_bundle_3_has_requirements(self, products_dir):
        """Bundle 3 should have requirements.txt."""
        reqs = products_dir / "bundle-3-ai-toolkit" / "requirements.txt"
        assert reqs.exists(), "Bundle 3 missing requirements.txt"


class TestBundleContent:
    """Test that bundles contain the expected source files."""

    @pytest.fixture
    def products_dir(self):
        """Return the products directory path."""
        return Path(__file__).parent.parent / "products"

    def test_bundle_1_contains_core_files(self, products_dir):
        """Bundle 1 should contain core utility files."""
        bundle_path = products_dir / "bundle-1-code-quality"
        # At minimum, should have some Python files
        py_files = list(bundle_path.glob("*.py"))
        assert len(py_files) >= 3, f"Bundle 1 has only {len(py_files)} .py files, expected >= 3"

    def test_bundle_2_contains_scripts(self, products_dir):
        """Bundle 2 should contain social media automation scripts."""
        bundle_path = products_dir / "bundle-2-social-media"
        py_files = list(bundle_path.glob("*.py"))
        assert len(py_files) >= 5, f"Bundle 2 has only {len(py_files)} .py files, expected >= 5"

    def test_bundle_3_contains_ai_scripts(self, products_dir):
        """Bundle 3 should contain AI integration scripts."""
        bundle_path = products_dir / "bundle-3-ai-toolkit"
        py_files = list(bundle_path.glob("*.py"))
        assert len(py_files) >= 5, f"Bundle 3 has only {len(py_files)} .py files, expected >= 5"


class TestBackupFileCleanup:
    """Test that backup files are properly cleaned up."""

    def test_no_backup_files_in_root(self):
        """Root directory should not have .backup_* files."""
        root = Path(__file__).parent.parent
        backup_files = list(root.glob("*.backup_*"))
        assert len(backup_files) == 0, f"Found {len(backup_files)} backup files in root: {backup_files[:5]}"

    def test_no_backup_files_in_products(self):
        """Products directory should not have .backup_* files."""
        products = Path(__file__).parent.parent / "products"
        if products.exists():
            backup_files = list(products.rglob("*.backup_*"))
            assert len(backup_files) == 0, f"Found {len(backup_files)} backup files in products/"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
