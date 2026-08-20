"""
Core image processing utilities module.

This package provides shared utilities, configuration, and exception handling
for all image upscaling operations.
"""

from .config import UpscaleConfig
from .exceptions import (
    ImageProcessingError,
    DimensionError,
    ResizeError,
    OptimizationError,
    ProcessorNotFoundError,
    ImageFileNotFoundError,
)
from .image_utils import (
    get_image_processor,
    get_image_dimensions,
    get_file_size,
    calculate_target_dimensions,
    resize_to_aspect_ratio,
    optimize_file_size,
    run_command,
    temp_file,
    supports_webp,
)
from .cache import (
    ImageCache,
    get_cache,
    cache_image_result,
    get_cached_result,
)
from .parallel import (
    process_batch_parallel,
    process_images_parallel,
)

__all__ = [
    # Configuration
    'UpscaleConfig',
    # Exceptions
    'ImageProcessingError',
    'DimensionError',
    'ResizeError',
    'OptimizationError',
    'ProcessorNotFoundError',
    'ImageFileNotFoundError',
    # Utilities
    'get_image_processor',
    'get_image_dimensions',
    'get_file_size',
    'calculate_target_dimensions',
    'resize_to_aspect_ratio',
    'optimize_file_size',
    'run_command',
    'temp_file',
    'supports_webp',
    # Caching
    'ImageCache',
    'get_cache',
    'cache_image_result',
    'get_cached_result',
    # Parallel Processing
    'process_batch_parallel',
    'process_images_parallel',
]

