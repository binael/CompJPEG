#!/usr/bin/env python3

"""
Tests cases for quantization module
"""

from util_func import get_quantRatio
import numpy as np
import unittest


chroma50 = np.array((
    (17, 18, 24, 47, 99, 99, 99, 99),
    (18, 21, 26, 66, 99, 99, 99, 99),
    (24, 26, 56, 99, 99, 99, 99, 99),
    (47, 66, 99, 99, 99, 99, 99, 99),
    (99, 99, 99, 99, 99, 99, 99, 99),
    (99, 99, 99, 99, 99, 99, 99, 99),
    (99, 99, 99, 99, 99, 99, 99, 99),
    (99, 99, 99, 99, 99, 99, 99, 99)
))

luma50 = np.array((
    (16, 11, 10, 16, 24, 40, 51, 61),
    (12, 12, 14, 19, 26, 58, 60, 55),
    (14, 13, 16, 24, 40, 57, 69, 56),
    (14, 17, 22, 29, 51, 87, 80, 62),
    (18, 22, 37, 56, 68, 109, 103, 77),
    (24, 36, 55, 64, 81, 104, 113, 92),
    (49, 64, 78, 87, 103, 121, 120, 101),
    (72, 92, 95, 98, 112, 100, 103, 99)
))

luma10 = np.array((
    (80, 55, 50, 80, 120, 200, 255, 255),
    (60, 60, 70, 95, 130, 255, 255, 255),
    (70, 65, 80, 120, 200, 255, 255, 255),
    (70, 85, 110, 145, 255, 255, 255, 255),
    (90, 110, 185, 255, 255, 255, 255, 255),
    (120, 180, 255, 255, 255, 255, 255, 255),
    (245, 255, 255, 255, 255, 255, 255, 255),
    (255, 255, 255, 255, 255, 255, 255, 255)
))

chroma10 = np.array((
    (85, 90, 120, 235, 255, 255, 255, 255),
    (90, 105, 130, 255, 255, 255, 255, 255),
    (120, 130, 255, 255, 255, 255, 255, 255),
    (235, 255, 255, 255, 255, 255, 255, 255),
    (255, 255, 255, 255, 255, 255, 255, 255),
    (255, 255, 255, 255, 255, 255, 255, 255),
    (255, 255, 255, 255, 255, 255, 255, 255),
    (255, 255, 255, 255, 255, 255, 255, 255)
))


def check_equality(q1, q2):
    """
    checks if q1 and 12 are equal

    Parameter
    ---------
    q1:
        quantization list 1
    q2:
        quantization list 2
    """
    return q1 == q2


class TestGetQuantRatio(unittest.TestCase):
    """
    A unittest class that tests the function get_quantRatio
    """

    def test_get_quantRatio_luma_50(self):
        q1 = get_quantRatio(50, 'luma')
        self.assertTrue(np.all(check_equality(q1, luma50)))

    def test_get_quantRatio_luma_10(self):
        q1 = get_quantRatio(10, 'luma')
        self.assertTrue(np.all(check_equality(q1, luma10)))

    def test_get_quantRatio_luma_50(self):
        q1 = get_quantRatio(50, 'chroma')
        self.assertTrue(np.all(check_equality(q1, chroma50)))

    def test_get_quantRatio_luma_50(self):
        q1 = get_quantRatio(10, 'chroma')
        self.assertTrue(np.all(check_equality(q1, chroma10)))

    def test_get_quantRatio_return(self):
        result = get_quantRatio(50)
        self.assertIsInstance(result, tuple)

    def test_get_quantRatio_mode_typeError(self):
        with self.assertRaises(TypeError) as er:
            get_quantRatio(50, mode=50)
        self.assertEqual(str(er.exception), "mode is not an integer")

    def test_get_quantRatio_quality_typeError(self):
        with self.assertRaises(TypeError) as er:
            get_quantRatio('50', 'all')
        text = 'Quality must be an integer'
        self.assertEqual(str(er.exception), text)

    def test_get_quantRatio_quality_valueError(self):
        with self.assertRaises(ValueError) as er:
            get_quantRatio(0, mode='all')
        text = 'Quality must be between 1 and 100'
        self.assertEqual(str(er.exception), text)

    def test_get_quantRatio_mode_valueError(self):
        with self.assertRaises(ValueError) as er:
            get_quantRatio(50, mode='Chromium')
        text = 'mode must be "all, luma or chroma"'
        self.assertEqual(str(er.exception), text)
