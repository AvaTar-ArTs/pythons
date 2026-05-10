import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
"""
Summary of test_uploader_factory.py

This module is part of the AVATARARTS ecosystem.
For more information about the AVATARARTS project, see the main documentation.
"""

import unittest
import simplegallery.common as spg_common
from simplegallery.upload.uploader_factory import get_uploader
from simplegallery.upload.variants.aws_uploader import AWSUploader
from simplegallery.upload.variants.netlify_uploader import NetlifyUploader


class UploaderFactoryTestCase(unittest.TestCase):
    def test_get_uploader(self):
        self.assertIs(AWSUploader, get_uploader("aws").__class__)
        self.assertIs(NetlifyUploader, get_uploader("netlify").__class__)

        with self.assertRaises(spg_common.SPGException):
            get_uploader("non_existing_uploader")


try:
        unittest.main()
except KeyboardInterrupt:
    logger.info("Execution interrupted by user")
    sys.exit(1)
except Exception as e:
    logger.error(f"An error occurred: {e}", exc_info=True)
    sys.exit(1)