#!/usr/bin/env python3

"""
Tests for the module image_io
"""

import unittest
import numpy as np
from PIL import Image

from tests import variables as var
from fileIO import save_image
from fileIO import get_image_array

class TestGetImageArray(unittest.TestCase):
    """
    Tests for the get_image_array function
    """

    def test_get_image_array_jpeg(self):
        ar = get_image_array(var.jpeg_image2)
        self.assertTrue(np.all(ar))

    def test_get_image_array_png(self):
        with self.assertRaises(TypeError) as er:
            get_image_array(var.png_image)
        text = 'Image must be JPEG format'
        self.assertEqual(str(er.exception), text)

    def test_get_image_array_file_not_found(self):
        with self.assertRaises(FileNotFoundError) as er:
            get_image_array(var.not_a_file)
        text = f"[Errno 2] No such file or directory: '{var.not_a_file}'"
        self.assertEqual(str(er.exception), text)

    def test_get_image_array_no_input(self):
        with self.assertRaises(TypeError) as er:
            get_image_array()
        text = f"get_image_array() missing 1 required positional argument: 'filename'"
        self.assertEqual(str(er.exception), text)


class TestSaveImage(unittest.TestCase):
    """
    Tests for save_image function
    """

    def setUp(self):
        self.empty_array = [[]]
        self.array2d = var.array_3_2_3d[:, :, 0]
        self.im_path = './jpeg_images/test_compress.jpg'

    def test_save_image_3d_array(self):
        save_image(var.array_3_2_3d, self.im_path)
        self.assertTrue(var.is_file_path(self.im_path))

    def test_save_image_typeError_empty_array(self):
        with self.assertRaises(ValueError) as er:
            save_image(self.empty_array, self.im_path)
        text = "Array must be a non empty array"
        self.assertEqual(text, str(er.exception))

    def test_save_image_typeError_2d_array(self):
        with self.assertRaises(TypeError) as er:
            save_image(self.array2d, self.im_path)
        text = "Array must be a 3D array"
        self.assertEqual(text, str(er.exception))
