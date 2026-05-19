"""
Enhanced logging system for SimpleGallery 2.1
"""

import sys
import logging
from typing import Optional
from enum import Enum


class LogLevel(Enum):
    """Log levels"""

    DEBUG = logging.DEBUG
    INFO = logging.INFO
    WARNING = logging.WARNING
    ERROR = logging.ERROR
    CRITICAL = logging.CRITICAL


class SimpleGalleryLogger:
    """Enhanced logger with progress tracking"""

    def __init__(self, verbose: bool = False, level: LogLevel = LogLevel.INFO):
        """
        Initialize logger
        :param verbose: Enable verbose/debug logging
        :param level: Log level
        """
        self.verbose = verbose
        self.logger = logging.getLogger("simplegallery")
        self.logger.setLevel(level.value if verbose else LogLevel.INFO.value)

        # Create console handler
        handler = logging.StreamHandler(sys.stdout)
        handler.setLevel(level.value if verbose else LogLevel.INFO.value)

        # Create formatter
        formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
            if verbose
            else "%(message)s"
        )
        handler.setFormatter(formatter)

        # Add handler if not already added
        if not self.logger.handlers:
            self.logger.addHandler(handler)

    def debug(self, message: str):
        """Log debug message"""
        if self.verbose:
            self.logger.debug(message)

    def info(self, message: str):
        """Log info message"""
        self.logger.info(message)

    def warning(self, message: str):
        """Log warning message"""
        self.logger.warning(message)

    def error(self, message: str):
        """Log error message"""
        self.logger.error(message)

    def critical(self, message: str):
        """Log critical message"""
        self.logger.critical(message)

    def progress(self, current: int, total: int, item: str = ""):
        """
        Log progress
        :param current: Current item number
        :param total: Total items
        :param item: Item name (optional)
        """
        percentage = (current / total * 100) if total > 0 else 0
        message = f"Progress: {current}/{total} ({percentage:.1f}%)"
        if item:
            message += f" - {item}"
        self.info(message)


# Global logger instance
_logger: Optional[SimpleGalleryLogger] = None


def get_logger(verbose: bool = False) -> SimpleGalleryLogger:
    """Get global logger instance"""
    global _logger
    if _logger is None:
        _logger = SimpleGalleryLogger(verbose=verbose)
    return _logger


def log(message: str):
    """Backward compatible log function"""
    get_logger().info(message)
