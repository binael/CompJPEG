#!/usr/bin/env python3

from util_func import get_dimension
from util_func import picture_resolution
from util_func import get_image_size
from PIL import Image
import unittest


class TestGetDimension(unittest.TestCase):
    """
    Unit test for the function get_dimension
    """

    def setUp(self):
        self.file = './jpeg_images/example1.jpg'
        self.no_image = 'no_image_file_here.jpeg'
        with Image.open(self.file) as img:
            self.dim = img.size

    def test_return_type(self):
        self.assertIsInstance(get_dimension(self.file), tuple)

    def test_get_dimension(self):
        self.assertTrue(get_dimension(self.file), self.dim)

    def test_typeError_filepath(self):
        with self.assertRaises(TypeError) as er:
            get_dimension(50)
        text = "Input must be a string of filepath"
        self.assertEqual(str(er.exception), text)

    def test_typeError_no_argument(self):
        with self.assertRaises(TypeError) as er:
            get_dimension()
        text = "get_dimension() missing 1 required positional argument: 'image'"
        self.assertEqual(str(er.exception), text)

    def test_typeError_many_arguments(self):
        with self.assertRaises(TypeError) as er:
            get_dimension(self.file, self.no_image)
        text = "get_dimension() takes 1 positional argument but 2 were given"
        self.assertEqual(str(er.exception), text)

    def test_valueError_filepath(self):
        with self.assertRaises(ValueError) as er:
            get_dimension('')
        text = "Input must be a string of filepath"
        self.assertEqual(str(er.exception), text)

    def test_file_not_found_error_filepath(self):
        with self.assertRaises(FileNotFoundError) as er:
            get_dimension(self.no_image)
        text = "File could not be opened"
        self.assertEqual(str(er.exception), text)


class TestPictureResolution(unittest.TestCase):
    """
    Unit test for the function picture_resolution
    """

    def setUp(self):
        self.file = './jpeg_images/example1.jpg'
        self.no_image = 'no_image_file_here.jpeg'
        with Image.open(self.file) as img:
            self.width, self.height = img.size
            self.res = f'{self.width} X {self.height}'

    def test_return_type(self):
        self.assertIsInstance(picture_resolution(self.file), str)

    def test_picture_resolution_width(self):
        pix_dim = picture_resolution(self.file).split(' X ')
        self.assertEqual(int(pix_dim[0]), self.width)

    def test_picture_resolution_height(self):
        pix_dim = picture_resolution(self.file).split(' X ')
        self.assertEqual(int(pix_dim[1]), self.height)

    def test_picture_resolution_value(self):
        self.assertEqual(self.res, picture_resolution(self.file))

    def test_typeError_filepath(self):
        with self.assertRaises(TypeError) as er:
            picture_resolution(50)
        text = "Input must be a string of filepath"
        self.assertEqual(str(er.exception), text)

    def test_typeError_no_argument(self):
        with self.assertRaises(TypeError) as er:
            picture_resolution()
        text = "picture_resolution() missing 1 required positional argument: 'image'"
        self.assertEqual(str(er.exception), text)

    def test_typeError_many_arguments(self):
        with self.assertRaises(TypeError) as er:
            picture_resolution(self.file, self.no_image)
        text = "picture_resolution() takes 1 positional argument but 2 were given"
        self.assertEqual(str(er.exception), text)

    def test_valueError_filepath(self):
        with self.assertRaises(ValueError) as er:
            picture_resolution('')
        text = "Input must be a string of filepath"
        self.assertEqual(str(er.exception), text)

    def test_file_not_found_error_filepath(self):
        with self.assertRaises(FileNotFoundError) as er:
            picture_resolution(self.no_image)
        text = "File could not be opened"
        self.assertEqual(str(er.exception), text)
