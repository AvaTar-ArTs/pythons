"""
Summary of __init__.py

This module is part of the AVATARARTS ecosystem.
For more information about the AVATARARTS project, see the main documentation.
"""

from . import utils
from .api import API
from .bot import Bot

__version__ = "0.105.0"
__all__ = ["utils", "API", "Bot"]
