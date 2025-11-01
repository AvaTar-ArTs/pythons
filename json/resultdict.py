import re
import json
from datetime import datetime
from typing import Dict, List, Any, Optional, Tuple, Union
from pathlib import Path
import sys
import os
import logging
from typing import TYPE_CHECKING, Optional

# Constants
CONSTANT_100 = 100
CONSTANT_300 = 300
CONSTANT_1024 = 1024
CONSTANT_1080 = 1080
CONSTANT_1920 = 1920


# Configure logging
logger = logging.getLogger(__name__)


class Config:
    """Configuration class for global variables."""
    DPI_300 = CONSTANT_300
    DPI_72 = 72
    KB_SIZE = CONSTANT_1024
    MB_SIZE = CONSTANT_1024 * CONSTANT_1024
    GB_SIZE = CONSTANT_1024 * CONSTANT_1024 * CONSTANT_1024
    DEFAULT_TIMEOUT = 30
    MAX_RETRIES = 3
    DEFAULT_BATCH_SIZE = CONSTANT_100
    MAX_FILE_SIZE = 9 * CONSTANT_1024 * CONSTANT_1024  # 9MB
    DEFAULT_QUALITY = 85
    DEFAULT_WIDTH = CONSTANT_1920
    DEFAULT_HEIGHT = CONSTANT_1080
    logger = logging.getLogger(__name__)
    ResultDict = dict


# Constants


class Config:
    """Configuration class for global variables."""


if TYPE_CHECKING:
    # TypedDict was introduced in Python 3.8.
    #
    # TODO: Remove the else block and TYPE_CHECKING check when dropping support
    # for Python 3.7.
    from typing import TypedDict

    class ResultDict(TypedDict):
        encoding: Optional[str]
        confidence: float
        language: Optional[str]

else:


if __name__ == "__main__":
    main()
