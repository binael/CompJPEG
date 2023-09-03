#!/usr/bin/env python3

"""
This module contain functions and variables that are either get
or analyse data for Encoders and Decoders

Variables
---------
cosine_array: list of list
    The discreet cosine transform matrix that will be used in
    multiplying the 8X8 block to yield the transformed image matrix

Formular
--------
    # T - cosine_array. 8X8 matrix given below
    # T' - transpose of the cosine_array. 8X8 matrix
    # M - 8X8 section of the image data(matrix)
    # * - matrix multiplication
    # FORWARD DCT:
        $ DCT = T * M * T'
    # INVERSE DCT:
        $ IDCT = T' * M * T

Note
----
Matrix - An array of array | 2D array
cosine_array implementation is from the function get_cosine_array
"""

import numpy as np
from math import cos, sqrt

cosine_array = np.array([
    [0.3536, 0.3536, 0.3536, 0.3536, 0.3536, 0.3536, 0.3536, 0.3536],
    [0.4904, 0.4157, 0.2778, 0.0975, -0.0975, -0.2778, -0.4157, -0.4904],
    [0.4619, 0.1913, -0.1913, -0.4619, -0.4619, -0.1913, 0.1913, 0.4619],
    [0.4157, -0.0975, -0.4904, -0.2778, 0.2778, 0.4904, 0.0975, -0.4157],
    [0.3536, -0.3536, -0.3536, 0.3536, 0.3536, -0.3536, -0.3536, 0.3536],
    [0.2778, -0.4904, 0.0975, 0.4157, -0.4157, -0.0975, 0.4904, -0.2778],
    [0.1913, -0.4619, 0.4619, -0.1913, -0.1913, 0.4619, -0.4619, 0.1913],
    [0.0975, -0.2778, 0.4157, -0.4904, 0.4904, -0.4157, 0.2778, -0.0975]
])


def get_cosine_array(n=8) -> list:
    """
    Function that computes the 8X8 dct cosine values that will be
    used in converting image data to frequency domain

    Parameters
    ----------
    n : int
        the size of the matrix ie the height and width of the matrix
        mat(n, n) or mat(n X n)

    Returns:
    ndarray:
        returns the cosine array used in matrix multiplicaion for
        dct transform
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

    return (np.array(matrix))
