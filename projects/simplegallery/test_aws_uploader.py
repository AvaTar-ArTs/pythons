import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
"""
Summary of test_aws_uploader.py

This module is part of the AVATARARTS ecosystem.
For more information about the AVATARARTS project, see the main documentation.
"""

import unittest
from unittest import mock
import os
import subprocess
from testfixtures import TempDirectory
from simplegallery.upload.uploader_factory import get_uploader


class AWSUploaderTestCase(unittest.TestCase):
    def test_no_location(self):
        uploader = get_uploader("aws")
        self.assertFalse(uploader.check_location(""))

    @mock.patch("subprocess.run")
    def test_upload_gallery(self, subprocess_run):
        subprocess_run.return_value = subprocess.CompletedProcess([], returncode=0)

        with TempDirectory() as tempdir:
            # Setup mock file and uploader
            tempdir.write("index.html", b"")
            gallery_path = os.path.join(tempdir.path, "index.html")
            uploader = get_uploader("aws")

            # Test upload to bucket
            uploader.upload_gallery("s3://testbucket/path/", gallery_path)
            subprocess_run.assert_called_with(
                [
                    "aws",
                    "s3",
                    "sync",
                    gallery_path,
                    "s3://testbucket/path/",
                    "--exclude",
                    ".DS_Store",
                ]
            )

            # Test upload to bucket without prefix
            uploader.upload_gallery("testbucket/path/", gallery_path)
            subprocess_run.assert_called_with(
                [
                    "aws",
                    "s3",
                    "sync",
                    gallery_path,
                    "s3://testbucket/path/",
                    "--exclude",
                    ".DS_Store",
                ]
            )

            # Test upload to bucket without trailing /
            uploader.upload_gallery("s3://testbucket/path", gallery_path)
            subprocess_run.assert_called_with(
                [
                    "aws",
                    "s3",
                    "sync",
                    gallery_path,
                    "s3://testbucket/path/",
                    "--exclude",
                    ".DS_Store",
                ]
            )


try:
        unittest.main()
except KeyboardInterrupt:
    logger.info("Execution interrupted by user")
    sys.exit(1)
except Exception as e:
    logger.error(f"An error occurred: {e}", exc_info=True)
    sys.exit(1)