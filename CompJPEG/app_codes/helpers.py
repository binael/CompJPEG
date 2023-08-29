#!/usr/bin/env python3

"""
This module contain functions and variables that are either get
or analyse data for Encoders and Decoders

Variables
---------
q_list: list
    The quantization matrix for quality of 50 in python list
Quantization50 : list
    The quantization matrix for quality of 50 in numpy array
dct_matrix: list of list
    The discreet cosine transform matrix that will be used in
    multiplying the 8X8 block to yield the transformed image matrix
dll : c_type
    Imported C dynamic library

Formular
--------
    # T - dct_matrix. 8X8 matrix
    # T' - transpose of the dct_matrix. 8X8 matrix
    # M - 8X8 section of the image data(matrix)
    # D - transformed 8X8 image matrix
    # * - matrix multiplication

    $ D = T * M * T'

Note
----
Matrix - An array of array | 2D array
dct_matrix implementation is from the function get_dct_matrix
"""

from PIL import Image
import numpy as np
from ctypes.util import find_library
from ctypes import *
from math import ceil, sqrt, cos

libc = CDLL(find_library("c"))

# The below table is the default standard for Q50
q_list = [
    [16, 11, 10, 16, 24, 40, 51, 61],
    [12, 12, 14, 19, 26, 58, 60, 55],
    [14, 13, 16, 24, 40, 57, 69, 56],
    [14, 17, 22, 29, 51, 87, 80, 62],
    [18, 22, 37, 56, 68, 109, 103, 77],
    [24, 35, 55, 64, 81, 104, 113, 92],
    [49, 64, 78, 87, 103, 121, 120, 101],
    [72, 92, 95, 98, 112, 100, 103, 99]
]

dct_matrix = [
    [0.3536, 0.3536, 0.3536, 0.3536, 0.3536, 0.3536, 0.3536, 0.3536],
    [0.4904, 0.4157, 0.2778, 0.0975, -0.0975, -0.2778, -0.4157, -0.4904],
    [0.4619, 0.1913, -0.1913, -0.4619, -0.4619, -0.1913, 0.1913, 0.4619],
    [0.4157, -0.0975, -0.4904, -0.2778, 0.2778, 0.4904, 0.0975, -0.4157],
    [0.3536, -0.3536, -0.3536, 0.3536, 0.3536, -0.3536, -0.3536, 0.3536],
    [0.2778, -0.4904, 0.0975, 0.4157, -0.4157, -0.0975, 0.4904, -0.2778],
    [0.1913, -0.4619, 0.4619, -0.1913, -0.1913, 0.4619, -0.4619, 0.1913],
    [0.0975, -0.2778, 0.4157, -0.4904, 0.4904, -0.4157, 0.2778, -0.0975]
]

Quantization50 = np.array(q_list)
dct_array = np.array(dct_matrix)

try:
    dll = CDLL("./C_library/liball.so")
except OSError as e:
    print("Error loading shared library:", e)
    exit(1)


def picture_resolution(image) -> str:
    """
    """
    resolution = dll.picture_resolution

    resolution.argtypes = [c_char_p]
    resolution.restype = c_char_p
    image_file = c_char_p(image.encode())

    result = resolution(image_file)

    return (result.decode())


def get_dimension(image) -> tuple:
    """
    A function that uses fetches the dimension (h, w) of an image

    Note
    ----
    This function imports picture_resolution function and extracts
    the dimensions

    Returns
    -------
    dimension: tuple
        (height : int, width : int)
    """
    resolution = picture_resolution(image)
    dimension = resolution.split(' X ')

    return (int(dimension[0]), int(dimension[1]))


def get_dct_matrix(n=8) -> list:
    """
    Function that computes the 8X8 dct cosine values that will be
    used in converting image data to frequency domain

    Parameters
    ----------
    n : int
        the size of the matrix ie the height and width of the matrix
        mat(n, n) or mat(n X n)
    """

    matrix = [[0 for _ in range(n)] for _ in range(n)]
    PI = 3.1416

    for j in range(n):
        number = 1 / sqrt(n)
        matrix[0][j] = round(number, 4)

    for i in range(1, n):
        for j in range(n):
            number = sqrt(2 / n) * cos((2 * j + 1) * i * PI / (2 * n))
            matrix[i][j] = round(number, 4)

    return (matrix)


def pad_array(array, height, width, paddedHeight, paddedWidth):
    """
    A function that pads a 3D numpy array to ensure multiples of 8 on both
    rows and columns

    Parameters
    ----------
    array : numpy 3D array
        Numpy 3D array
    height : int
        the original height of the array
    width : int
        the original width of the array
    paddedHeight : int
        the padded height of the array
    paddedWidth : int
        the padded width of the array

    Return
    ------
    array : numpy 3D array
    """

    # Create a 2X2 array for the three channels of the image matrix
    # Using '1' as the default element
    R = np.ones((paddedHeight, paddedWidth), dtype=np.int64)
    B = np.ones((paddedHeight, paddedWidth), dtype=np.int64)
    G = np.ones((paddedHeight, paddedWidth), dtype=np.int64)

    # split the image data into 2X2 and copy into RGB array
    R[0:height:, 0:width] = array[:, :, 0]
    B[0:height:, 0:width] = array[:, :, 1]
    G[0:height:, 0:width] = array[:, :, 2]

    h_diff = paddedHeight - height
    w_diff = paddedWidth - width

    # Extend the last element of the rows and columns to fill the matrix
    for h in range(h_diff):
        last = h + height
        R[last:last + 1, 0:paddedWidth] = R[height - 1:height, 0:paddedWidth]
        B[last:last + 1, 0:paddedWidth] = B[height - 1:height, 0:paddedWidth]
        G[last:last + 1, 0:paddedWidth] = G[height - 1:height, 0:paddedWidth]

    for w in range(w_diff):
        last = w + width
        R[0:paddedHeight, last: last + 1] = R[0:paddedHeight, width - 1:width]
        G[0:paddedHeight, last: last + 1] = G[0:paddedHeight, width - 1:width]
        B[0:paddedHeight, last: last + 1] = B[0:paddedHeight, width - 1:width]

    # Stack the RBG as a 3D numpy array
    array = np.stack((R, B, G), axis=-1)

    return (array)

        
