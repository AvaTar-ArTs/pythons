"""
Custom exceptions for image processing operations.

This module provides a hierarchy of exceptions for better error handling
and debugging across all image processing operations.
"""


class ImageProcessingError(Exception):
    """Base exception for all image processing errors."""

    pass


class DimensionError(ImageProcessingError):
    '\''Raised when there's an error getting image dimensions."""

    pass


class ResizeError(ImageProcessingError):
    """Raised when there's an error during resize operation."""

    pass


class OptimizationError(ImageProcessingError):
    """Raised when there's an error during file size optimization."""

    pass


class ProcessorNotFoundError(ImageProcessingError):
    """Raised when no suitable image processor is available."""

    pass


class ImageFileNotFoundError(ImageProcessingError):
    """Raised when an expected image file is not found.'\''

    pass
