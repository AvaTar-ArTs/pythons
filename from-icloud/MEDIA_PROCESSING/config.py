"""
Centralized configuration management for image upscaling operations.

This module provides a unified configuration system to ensure consistent
behavior across all upscaling scripts.
"""

import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, Tuple


@dataclass
class UpscaleConfig:
    """Configuration for image upscaling operations."""

    max_file_size_mb: float = 9.0
    """Maximum file size in megabytes."""

    target_dpi: int = 300
    """Target DPI for output images."""

    base_size: int = 2000
    """Base size for dimension calculations."""

    max_dimension: int = 4000
    """Maximum dimension (width or height) in pixels."""

    quality_range: Tuple[int, int] = (90, 20)
    """Quality range for optimization (max, min)."""

    quality_step: int = 10
    """Step size for quality reduction during optimization."""

    batch_size: int = 5
    """Number of images to process per batch."""

    aspect_ratios: Dict[str, Tuple[int, int, str]] = field(default_factory=lambda: {
        '16x9': (16, 9, '16:9'),
        '9x16': (9, 16, '9:16'),
        '1x1': (1, 1, '1:1'),
        '4x3': (4, 3, '4:3'),
        '3x4': (3, 4, '3:4'),
        '3x2': (3, 2, '3:2'),
        '2x3': (2, 3, '2:3'),
        '21x9': (21, 9, '21:9'),
        '5x4': (5, 4, '5:4'),
    })
    """Standard aspect ratios with (width_ratio, height_ratio, display_name)."""

    def __post_init__(self):
        """Validate configuration values."""
        if self.max_file_size_mb <= 0:
            raise ValueError("max_file_size_mb must be positive")

        if self.target_dpi not in [72, 150, 300, 600]:
            import warnings
            warnings.warn(
                f"Uncommon DPI value: {self.target_dpi}. "
                f"Standard values are 72, 150, 300, or 600.",
                UserWarning
            )

        if self.base_size <= 0 or self.max_dimension <= 0:
            raise ValueError("base_size and max_dimension must be positive")

        if self.max_dimension < self.base_size:
            import warnings
            warnings.warn(
                "max_dimension is less than base_size. "
                "Some aspect ratios may be constrained.",
                UserWarning
            )

        max_q, min_q = self.quality_range
        if not (0 <= min_q < max_q <= 100):
            raise ValueError(
                "quality_range must be (max, min) where 0 <= min < max <= 100"
            )

        if self.quality_step <= 0:
            raise ValueError("quality_step must be positive")

        if self.batch_size <= 0:
            raise ValueError("batch_size must be positive")

    @classmethod
    def from_file(cls, filepath: str) -> 'UpscaleConfig':
        """
        Load configuration from a JSON file.

        Args:
            filepath: Path to the JSON configuration file

        Returns:
            UpscaleConfig instance

        Raises:
            FileNotFoundError: If config file doesn't exist
            ValueError: If config file is invalid
        """
        config_path = Path(filepath)
        if not config_path.exists():
            raise FileNotFoundError(f"Config file not found: {filepath}")

        try:
            with open(config_path, 'r') as f:
                data = json.load(f)
            return cls(**data)
        except json.JSONDecodeError as e:
            raise ValueError(f"Invalid JSON in config file: {e}")
        except TypeError as e:
            raise ValueError(f"Invalid configuration parameters: {e}")

    def save_to_file(self, filepath: str) -> None:
        """
        Save configuration to a JSON file.

        Args:
            filepath: Path to save the configuration
        """
        config_data = {
            'max_file_size_mb': self.max_file_size_mb,
            'target_dpi': self.target_dpi,
            'base_size': self.base_size,
            'max_dimension': self.max_dimension,
            'quality_range': list(self.quality_range),
            'quality_step': self.quality_step,
            'batch_size': self.batch_size,
        }

        with open(filepath, 'w') as f:
            json.dump(config_data, f, indent=2)

    def get_aspect_ratio(self, key: str) -> Tuple[int, int, str]:
        """Get aspect ratio by key."""
        return self.aspect_ratios.get(key, (1, 1, '1:1'))

    def list_aspect_ratios(self) -> Dict[str, str]:
        """Get a dictionary of aspect ratio keys to display names."""
        return {k: v[2] for k, v in self.aspect_ratios.items()}
