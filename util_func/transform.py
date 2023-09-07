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

# Python modules required
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


def FDCT(array):
    """
    A function that implements (Foward) DCT on an 8X8
    subsection of an ndarray

    Parameters
    ----------
    array: ndarray
        8X8 subsection of an nd array

    Formula
    -------
        # cosine_array - 8X8 cosine transfrom array (find in helpers.py)
        # cosine_array.T - the transpose
        # array - 8X8 section of the image
        # result - 8X8 section of the image that is dct transformed
        # * - matrix multiplication

        $ result = cosine_array * array * cosine_array.T

    Returns
    -------
    ndarray:
        DCT transformed 8X8 ndarray
    """

    if not isinstance(array, np.ndarray):
        raise TypeError('Array must be a numpy array')
    

    dim = array.shape
    if len(dim) != 2:
        raise TypeError('Array must be a 2d 8X8 array')
    if dim[0] != 8 or dim[1] != 8:
        raise TypeError('Array must be an 8X8 array')

    # np.dot - matrix multiplication
    return (np.dot(np.dot(cosine_array, array), (cosine_array.T)))


def IDCT(array):
    """
    A function that implements inverse DCT on an 8X8 subsection
    of an ndarray

    Parameters
    ----------
    array: ndarray
        8X8 subsection of an nd array

    Formula
    -------
        # cosine_array - 8X8 cosine transfrom array (find in helpers.py)
        # cosine_array.T - the transpose
        # array - 8X8 section of the image
        # result - 8X8 section of the image that is dct transformed
        # * - matrix multiplication

        $ result = cosine_array.T * array * cosine_array

    Returns
    -------
    ndarray:
        inverse DCT transformed 8X8 ndarray
    """

    if not isinstance(array, np.ndarray):
        raise TypeError('Array must be a numpy array')

    dim = array.shape
    if len(dim) != 2:
        raise TypeError('Array must be a 2d 8X8 array')
    if dim[0] != 8 or dim[1] != 8:
        raise TypeError('Array must be an 8X8 array')

    return (np.dot(np.dot(cosine_array.T, array), cosine_array))
