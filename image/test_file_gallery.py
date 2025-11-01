"""
Test File Gallery Logic

This module provides functionality for test file gallery logic.

Author: Auto-generated
Date: 2025-11-01
"""

import unittest
from unittest import mock
import os
from testfixtures import TempDirectory
import simplegallery.test.helpers as helpers
import simplegallery.media as spg_media
from simplegallery.logic.variants.files_gallery_logic import FilesGalleryLogic

# Constants
CONSTANT_160 = 160
CONSTANT_320 = 320
CONSTANT_500 = 500
CONSTANT_640 = 640
CONSTANT_1000 = 1000



class FileGalleryLogicTestCase(unittest.TestCase):
    @mock.patch("builtins.input", side_effect=["", "", "", ""])
    def test_create_thumbnails(self, input):
        """test_create_thumbnails function."""

        with TempDirectory() as tempdir:
            helpers.create_mock_image(
                os.path.join(tempdir.path, "photo.jpg"), CONSTANT_1000, CONSTANT_500
            )
            helpers.create_mock_image(
                os.path.join(tempdir.path, "photo2.gif"), CONSTANT_1000, CONSTANT_500
            )
            helpers.create_mock_image(
                os.path.join(tempdir.path, "photo3.png"), CONSTANT_1000, CONSTANT_500
            )

            thumbnail_path = os.path.join(
                tempdir.path, "public", "images", "thumbnails", "photo.jpg"
            )
            thumbnail_gif_path = os.path.join(
                tempdir.path, "public", "images", "thumbnails", "photo2.jpg"
            )
            thumbnail_png_path = os.path.join(
                tempdir.path, "public", "images", "thumbnails", "photo3.jpg"
            )

            # Init files gallery logic
            gallery_config = helpers.init_gallery_and_read_gallery_config(tempdir.path)
            file_gallery_logic = FilesGalleryLogic(gallery_config)

            # Check no thumbnails exist
            tempdir.compare([".empty"], path="public/images/thumbnails")

            # Check thumbnail created
            file_gallery_logic.create_thumbnails()
            tempdir.compare(
                [".empty", "photo.jpg", "photo2.jpg", "photo3.jpg"],
                path="public/images/thumbnails",
            )
            # The thumbnails are generated twice as big in order to improve the quality on retina displays
            self.assertEqual((CONSTANT_640, CONSTANT_320), spg_media.get_image_size(thumbnail_path))
            self.assertEqual((CONSTANT_640, CONSTANT_320), spg_media.get_image_size(thumbnail_gif_path))
            self.assertEqual((CONSTANT_640, CONSTANT_320), spg_media.get_image_size(thumbnail_png_path))

            # Check thumbnail not regenerated without force
            helpers.create_mock_image(
                os.path.join(tempdir.path, "public", "images", "photos", "photo.jpg"),
                CONSTANT_500,
                CONSTANT_500,
            )
            file_gallery_logic.create_thumbnails()
            self.assertEqual((CONSTANT_640, CONSTANT_320), spg_media.get_image_size(thumbnail_path))

            # Check thumbnail regenerated with force
            file_gallery_logic.create_thumbnails(force=True)
            self.assertEqual((CONSTANT_320, CONSTANT_320), spg_media.get_image_size(thumbnail_path))

            # Check thumbnail regenerated after size changed
            gallery_config["thumbnail_height"] = CONSTANT_320
            file_gallery_logic = FilesGalleryLogic(gallery_config)

            file_gallery_logic.create_thumbnails()
            self.assertEqual((CONSTANT_640, CONSTANT_640), spg_media.get_image_size(thumbnail_path))

    @mock.patch("builtins.input", side_effect=["", "", "", ""])
        """test_generate_images_data function."""

    def test_generate_images_data(self, input):
        with TempDirectory() as tempdir:
            helpers.create_mock_image(
                os.path.join(tempdir.path, "photo.jpg"), CONSTANT_1000, CONSTANT_500
            )

            # Init files gallery logic
            gallery_config = helpers.init_gallery_and_read_gallery_config(tempdir.path)
            file_gallery_logic = FilesGalleryLogic(gallery_config)

            # Check images_data generated correctly
            file_gallery_logic.create_thumbnails()
            images_data = file_gallery_logic.generate_images_data({})

            self.assertEqual(1, len(images_data))
            helpers.check_image_data(
                self,
                images_data,
                "photo.jpg",
                "",
                (CONSTANT_1000, CONSTANT_500),
                (CONSTANT_320, CONSTANT_160),
                local_files=True,
            )

            # Change a description, add a new image and check description of the first is preserved
            images_data["photo.jpg"]["description"] = "Test description"
            helpers.create_mock_image(
                os.path.join(tempdir.path, "public", "images", "photos", "photo2.jpg"),
                CONSTANT_1000,
                CONSTANT_500,
            )
            file_gallery_logic.create_thumbnails()
            images_data = file_gallery_logic.generate_images_data(images_data)
            self.assertEqual(2, len(images_data))
            helpers.check_image_data(
                self,
                images_data,
                "photo.jpg",
                "Test description",
                (CONSTANT_1000, CONSTANT_500),
                (CONSTANT_320, CONSTANT_160),
                local_files=True,
            )


if __name__ == "__main__":
    unittest.main()
