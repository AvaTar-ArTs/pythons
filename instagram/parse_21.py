import re
import json
from datetime import datetime
from typing import Dict, List, Any, Optional, Tuple, Union
from pathlib import Path
import sys
import os
import logging
from typing import Any, Dict, List, Optional, Union, Tuple, Callable

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
    parser = argparse.ArgumentParser(add_help
    args = parser.parse_args()
    bot = Bot()
    parser.add_argument("-u", type = str, help
    parser.add_argument("-p", type = str, help
    parser.add_argument("-l", type = int, help
    parser.add_argument("-proxy", type = str, help
    parser.add_argument("users", type = str, nargs
    bot.login(username = args.u, password
    bot.like_user(username, amount = args.l, filtration


# Constants


class Config:
    """Configuration class for global variables."""

"""
instabot example

Workflow:
    Like last medias by users.
"""

import argparse
import os
import sys

sys.path.append(os.path.join(sys.path[0], "../"))
from instabot import Bot  # noqa: E402



for username in args.users:


if __name__ == "__main__":
    main()
