#!/usr/bin/env python3

from util_func import pad_array
import numpy as np
import unittest
from tests.variables import check_equality
from tests.variables import array_3_2_3d



class TestPadArray(unittest.TestCase):
    """
    Unit tests for the function pad array
    """

    def setUp(self):
        self.ar = array_3_2_3d
        self.A = self.ar[:, :, 0]
        self.B = self.ar[:, :, 1]
        self.C = self.ar[:, :, 2]
        self.one_d = np.array([0, 1, 2, 3])
        self.no_array = ''

    def test_pad_array_2d(self):
        new_ar = pad_array(self.A, 3, 4)
        result = np.array([[1, 4, 7, 7],
                          [10, 13, 16, 16],
                          [10, 13, 16, 16]]
                          )
        self.assertTrue(np.all(check_equality(result, new_ar)))

    def test_pad_array_3d(self):
        new_ar = pad_array(self.ar, 2, 3)
        self.assertTrue(np.all(check_equality(self.ar, new_ar)))

    def test_typeError_ndarray1(self):
        with self.assertRaises(TypeError) as ex:
            pad_array(self.no_array, 8, 10)
        text = 'Array must be an ndarray'
        self.assertEqual(str(ex.exception), text)

    def test_typeError_ndarray2(self):
        with self.assertRaises(TypeError) as ex:
            pad_array(self.one_d, 8, 10)
        text = 'ndarray must be either 2D or 3D'
        self.assertEqual(str(ex.exception), text)

    def test_typeError_height(self):
        with self.assertRaises(TypeError) as ex:
            pad_array(self.A, '8', 10)
        text = 'ndarray dimensions must be integers'
        self.assertEqual(str(ex.exception), text)

    def test_typeError_width(self):
        with self.assertRaises(TypeError) as ex:
            pad_array(self.A, 8, '10')
        text = 'ndarray dimensions must be integers'
        self.assertEqual(str(ex.exception), text)

    def test_valueError_height(self):
        with self.assertRaises(ValueError) as ex:
            pad_array(self.A, 1, 10)
        text = 'padded dimensions is less than array dimensions'
        self.assertEqual(str(ex.exception), text)

    def test_valueError_width(self):
        with self.assertRaises(ValueError) as ex:
            pad_array(self.A, 10, 1)
        text = 'padded dimensions is less than array dimensions'
        self.assertEqual(str(ex.exception), text)
