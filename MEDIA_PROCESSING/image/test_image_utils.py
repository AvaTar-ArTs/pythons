"""
Unit tests for image processing utilities.
"""

import pytest
import tempfile
import os

from core.image_utils import (
    calculate_target_dimensions,
    get_file_size,
)


class TestCalculateTargetDimensions:
    """Tests for calculate_target_dimensions function."""

    def test_landscape_16x9(self):
        """Test 16:9 landscape calculation."""
        assert width == 3200
        assert height == 1800

    def test_portrait_9x16(self):
        """Test 9:16 portrait calculation."""
        assert width == 1125
        assert height == 2000

    def test_square_1x1(self):
        """Test 1:1 square calculation."""
        assert width == 2000
        assert height == 2000

    def test_max_dimension_limit(self):
        """Test max dimension constraint."""
            16, 9, base_size=2000, max_dimension=3000
        )
        assert width <= 3000
        assert height <= 3000

    def test_custom_base_size(self):
        """Test custom base size."""
        assert width == 1333
        assert height == 1000


class TestGetFileSize:
    """Tests for get_file_size function."""

    def test_existing_file(self):
        """Test getting size of existing file."""
        with tempfile.NamedTemporaryFile(delete=False) as f:
            f.write(b"test content")
            temp_path = f.name

        try:
            size = get_file_size(temp_path)
            assert size > 0
            assert size == len(b"test content")
        finally:
            os.unlink(temp_path)

    def test_nonexistent_file(self):
        """Test getting size of non-existent file."""
        size = get_file_size("/nonexistent/file/path")
        assert size == 0


class TestImageProcessor:
    """Tests for image processor detection."""

    def test_get_image_processor(self):
        """Test processor detection."""
        from core.image_utils import get_image_processor

        processor = get_image_processor()
        # Should return 'sips', 'pil', or None
        assert processor in ("sips", "pil", None)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
