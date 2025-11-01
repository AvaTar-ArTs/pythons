"""
Utilities Misc Exceptions 8

This module provides functionality for utilities misc exceptions 8.

Author: Auto-generated
Date: 2025-11-01
"""


class TwitchTubeError(Exception):
    """General error class for TwitchTube."""


class InvalidCategory(TwitchTubeError):
    """Error for when the specified category is invalid"""


class VideoPathAlreadyExists(TwitchTubeError):
    """Error for when a path already exists."""


class NoClipsFound(TwitchTubeError):
    """Error for when no clips are found."""
