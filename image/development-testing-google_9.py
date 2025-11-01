"""
Development Testing Google 9

This module provides functionality for development testing google 9.

Author: Auto-generated
Date: 2025-11-01
"""

import os
import unittest
from unittest import mock

import simplegallery.test.helpers as helpers
from simplegallery.logic.variants.google_gallery_logic import GoogleGalleryLogic
from testfixtures import TempDirectory

# Constants
CONSTANT_160 = 160
CONSTANT_213 = 213
CONSTANT_600 = 600
CONSTANT_800 = 800
CONSTANT_1000 = 1000



class GoogleGalleryTestCase(unittest.TestCase):

    remote_link = "https://photos.app.goo.gl/cevaz94hQiF8Z5p67"

    @mock.patch("builtins.input", side_effect=["", "", "", ""])
    def test_create_thumbnails(self, input):
        """test_create_thumbnails function."""

        with TempDirectory() as tempdir:
            # Init files gallery logic
            gallery_config = helpers.init_gallery_and_read_gallery_config(
                tempdir.path, self.remote_link
            )
            file_gallery_logic = GoogleGalleryLogic(gallery_config)

            # Check no thumbnail created
            file_gallery_logic.create_thumbnails()
            tempdir.compare([".empty"], path="public/images/thumbnails")

    @unittest.skipUnless(
        "RUN_LONG_TESTS" in os.environ,
        "Long test - it involves downloading files from Google.",
    )
    @mock.patch("builtins.input", side_effect=["", "", "", ""])
        """test_generate_images_data function."""

    def test_generate_images_data(self, input):
        with TempDirectory() as tempdir:
            # Init files gallery logic
            gallery_config = helpers.init_gallery_and_read_gallery_config(
                tempdir.path, self.remote_link
            )
            file_gallery_logic = GoogleGalleryLogic(gallery_config)

            # Check images_data generated correctly
            file_gallery_logic.create_thumbnails()
            images_data = file_gallery_logic.generate_images_data({})

            self.assertEqual(2, len(images_data))
            helpers.check_image_data(
                self,
                images_data,
                "tGPJDmxLbrr9BTX_IHjh_MH1gJ7JhlcBnMBXPgWQslNLQSUjKGFdYd3TqTqTsGsYkpOJakSgcB05yB9aZJQ03JvRxHRLC0R0W4pYfbV2hXPlAgLHxIy1izHbhdWtrj4izcGbax6Pqw",
                "",
                (CONSTANT_800, CONSTANT_600),
                (CONSTANT_213, CONSTANT_160),
            )
            helpers.check_image_data(
                self,
                images_data,
                "lOHX7xeJqCo_lqxKBobKGjwFTW8qPMPCbaAKeqS3baU-VT_SPC0HrapdAEXFzkL98dAb9nCjlRhnmCSLoz520E1fZ-xuNPXAwXvM2PapP6uolH6rZsR3QKivxr_rtVADKuWVm2lz8Q",
                "",
                (CONSTANT_1000, CONSTANT_1000),
                (CONSTANT_160, CONSTANT_160),
            )


if __name__ == "__main__":
    unittest.main()
