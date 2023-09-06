#!/usr/bin/env python

"""
A module that contains variables and functions needed for
tests
"""

import numpy as np
from pathlib import Path

png_image = './jpeg_images/screenshot1.png'
jpeg_image1 = './jpeg_images/example1.jpg'
jpeg_image2 = './jpeg_images/example_small.jpg'
not_a_file = 'not/a/file/path.jpeg'

array_3_2_3d = np.array([[[1, 2, 3],
                          [4, 5, 6],
                          [7, 8, 9]],
                         [[10, 11, 12],
                          [13, 14, 15],
                          [16, 17, 18]]])


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


def is_file_path(filename):
    """
    Function to check if a file path exists

    Parameters
    ----------
    filename: str
        the  path to file
    """

    path_obj = Path(filename)

    if path_obj.is_file():
        return True
    else:
        return False
