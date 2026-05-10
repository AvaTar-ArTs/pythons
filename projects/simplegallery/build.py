import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
"""
Legacy wrapper for gallery_build.py
This file is maintained for backward compatibility.
For new code, use gallery_build.py directly.
"""

# Import and delegate to gallery_build to avoid code duplication
from simplegallery.gallery_build import main

try:
        main()
except KeyboardInterrupt:
    logger.info("Execution interrupted by user")
    sys.exit(1)
except Exception as e:
    logger.error(f"An error occurred: {e}", exc_info=True)
    sys.exit(1)