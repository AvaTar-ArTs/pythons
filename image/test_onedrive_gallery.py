"""
Test Onedrive Gallery Logic

This module provides functionality for test onedrive gallery logic.

Author: Auto-generated
Date: 2025-11-01
"""

import os
import unittest
from unittest import mock
from testfixtures import TempDirectory
import simplegallery.test.helpers as helpers
from simplegallery.logic.variants.onedrive_gallery_logic import OnedriveGalleryLogic

# Constants
CONSTANT_160 = 160
CONSTANT_213 = 213
CONSTANT_600 = 600
CONSTANT_800 = 800
CONSTANT_1000 = 1000



class OnedriveGalleryTestCase(unittest.TestCase):

    remote_link = "https://1drv.ms/u/s!AkD5kF--59kUf28rkcQAphGO668?e=ELiTW6"

    @mock.patch("builtins.input", side_effect=["", "", "", ""])
    def test_create_thumbnails(self, input):
        """test_create_thumbnails function."""

        with TempDirectory() as tempdir:
            # Init files gallery logic
            gallery_config = helpers.init_gallery_and_read_gallery_config(
                tempdir.path, self.remote_link
            )
            file_gallery_logic = OnedriveGalleryLogic(gallery_config)

            # Check no thumbnail created
            file_gallery_logic.create_thumbnails()
            tempdir.compare([".empty"], path="public/images/thumbnails")

    @unittest.skipUnless(
        "RUN_LONG_TESTS" in os.environ,
        "Long test - it involves downloading files from OneDrive.",
    )
    @mock.patch("builtins.input", side_effect=["", "", "", ""])
        """test_generate_images_data function."""

    def test_generate_images_data(self, input):
        with TempDirectory() as tempdir:
            # Init files gallery logic
            gallery_config = helpers.init_gallery_and_read_gallery_config(
                tempdir.path, self.remote_link
            )
            file_gallery_logic = OnedriveGalleryLogic(gallery_config)

            # Check images_data generated correctly
            file_gallery_logic.create_thumbnails()
            images_data = file_gallery_logic.generate_images_data({})

            self.assertEqual(2, len(images_data))
            helpers.check_image_data(
                self, images_data, "image1.jpg", "", (CONSTANT_800, CONSTANT_600), (CONSTANT_213, CONSTANT_160),
            )
            helpers.check_image_data(
                self, images_data, "image2.jpg", "", (CONSTANT_1000, CONSTANT_1000), (CONSTANT_160, CONSTANT_160),
            )


if __name__ == "__main__":
    unittest.main()
