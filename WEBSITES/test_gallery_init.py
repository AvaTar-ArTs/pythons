"""
Test cases for gallery initialization functionality
Following the dark testing patterns of simplegallery
"""

import unittest
from unittest import mock
import sys
import os
import json
from testfixtures import TempDirectory
import city_gallery.gallery_init as gallery_init
import city_gallery.common as cg_common


class CityGalleryInitTestCase(unittest.TestCase):
    """Test cases for City Gallery initialization functionality"""

    def test_gallery_creation_possible(self):
        """Test gallery creation possibility check"""
        with TempDirectory() as tempdir:
            # Should be possible to create gallery in existing directory
            self.assertTrue(gallery_init.check_if_gallery_creation_possible(tempdir.path))
            
            # Should not be possible in non-existing directory
            self.assertFalse(gallery_init.check_if_gallery_creation_possible("/nonexistent/path"))

    def test_gallery_already_exists(self):
        """Test gallery existence check"""
        with TempDirectory() as tempdir:
            # No gallery should exist initially
            self.assertFalse(gallery_init.check_if_gallery_already_exists(tempdir.path))
            
            # Create gallery.json
            with open(os.path.join(tempdir.path, "gallery.json"), "w") as f:
                json.dump({}, f)
            
            # Gallery should exist now
            self.assertTrue(gallery_init.check_if_gallery_already_exists(tempdir.path))

    @mock.patch("builtins.input", side_effect=["", "", "", ""])
    def test_gallery_initialization(self, input):
        """Test gallery initialization with defaults"""
        with TempDirectory() as tempdir:
            sys.argv = ["gallery_init", "-p", tempdir.path]
            gallery_init.main()

            # Check that all required files and directories are created
            self.assertTrue(os.path.exists(os.path.join(tempdir.path, "gallery.json")))
            self.assertTrue(os.path.exists(os.path.join(tempdir.path, "templates")))
            self.assertTrue(os.path.exists(os.path.join(tempdir.path, "public")))
            self.assertTrue(os.path.exists(os.path.join(tempdir.path, "public", "css")))
            self.assertTrue(os.path.exists(os.path.join(tempdir.path, "public", "js")))
            self.assertTrue(os.path.exists(os.path.join(tempdir.path, "public", "images")))
            self.assertTrue(os.path.exists(os.path.join(tempdir.path, "public", "images", "photos")))
            self.assertTrue(os.path.exists(os.path.join(tempdir.path, "public", "images", "thumbnails")))

    def test_gallery_config_creation(self):
        """Test gallery configuration creation"""
        with TempDirectory() as tempdir:
            gallery_init.create_gallery_json(tempdir.path, "", True)
            
            config_path = os.path.join(tempdir.path, "gallery.json")
            self.assertTrue(os.path.exists(config_path))
            
            with open(config_path, "r") as config_file:
                config = json.load(config_file)
                
                # Check required keys
                required_keys = [
                    "images_data_file", "public_path", "templates_path",
                    "images_path", "thumbnails_path", "title", "description"
                ]
                for key in required_keys:
                    self.assertIn(key, config)
                
                # Check dark theme defaults
                self.assertTrue(config.get("dark_theme", False))
                self.assertTrue(config.get("urban_style", False))
                self.assertEqual(config["title"], "City 16-9")

    def test_force_overwrite(self):
        """Test force overwrite functionality"""
        with TempDirectory() as tempdir:
            # Create initial gallery
            sys.argv = ["gallery_init", "-p", tempdir.path, "--use-defaults"]
            gallery_init.main()
            
            # Try to create again without force (should exit)
            with self.assertRaises(SystemExit) as cm:
                sys.argv = ["gallery_init", "-p", tempdir.path, "--use-defaults"]
                gallery_init.main()
            self.assertEqual(cm.exception.code, 0)
            
            # Create with force (should succeed)
            sys.argv = ["gallery_init", "-p", tempdir.path, "--use-defaults", "--force"]
            gallery_init.main()
            # Should not raise exception

    def test_image_source_copying(self):
        """Test image source copying functionality"""
        with TempDirectory() as tempdir:
            # Create source directory with images
            source_dir = os.path.join(tempdir.path, "source")
            os.makedirs(source_dir)
            
            # Create test images
            with open(os.path.join(source_dir, "test1.jpg"), "w") as f:
                f.write("fake image data")
            with open(os.path.join(source_dir, "test2.png"), "w") as f:
                f.write("fake image data")
            
            # Initialize gallery with image source
            sys.argv = ["gallery_init", "-p", tempdir.path, "--image-source", source_dir, "--use-defaults"]
            gallery_init.main()
            
            # Check images were copied
            photos_dir = os.path.join(tempdir.path, "public", "images", "photos")
            self.assertTrue(os.path.exists(os.path.join(photos_dir, "test1.jpg")))
            self.assertTrue(os.path.exists(os.path.join(photos_dir, "test2.png")))


if __name__ == "__main__":
    unittest.main()