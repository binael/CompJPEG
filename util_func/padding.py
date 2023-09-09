#!/usr/bin/env python3

"""
Implentation of padding for 3D array
"""

# Python module
import numpy as np


def pad_array3d(array, width, height, paddedWidth, paddedHeight):
    """
    A function that pads a 3D numpy array to ensure multiples of 8 on both
    rows and columns

    Parameters
    ----------
    array : ndarray
        Numpy 3D array with either float or int type values
    width : int
        the original width of the array
    height : int
        the original height of the array
    paddedWidth : int
        the padded width of the array
    paddedHeight : int
        the padded height of the array

    Return
    ------
    ndarray:
        3D numpy array that both the height and the width of the
        individual 2D arrays are divisible by 8
    """

    # Create a 2X2 array for the three channels of the image matrix
    # Using '1' as the default element
    R = np.ones((paddedWidth, paddedHeight), dtype=np.int64)
    B = np.ones((paddedWidth, paddedHeight), dtype=np.int64)
    G = np.ones((paddedWidth, paddedHeight), dtype=np.int64)

    # split the image data into 2X2 and copy into RGB array
    R[0:width:, 0:height] = array[:, :, 0]
    B[0:width:, 0:height] = array[:, :, 1]
    G[0:width:, 0:height] = array[:, :, 2]

    w_diff = paddedWidth - width
    h_diff = paddedHeight - height

    # Extend the last element of the rows and columns to fill the matrix
    for w in range(w_diff):
        last = w + width
        R[last:last + 1, 0:paddedHeight] = R[width - 1:width, 0:paddedHeight]
        B[last:last + 1, 0:paddedHeight] = B[width - 1:width, 0:paddedHeight]
        G[last:last + 1, 0:paddedHeight] = G[width - 1:width, 0:paddedHeight]

    for h in range(h_diff):
        last = h + height
        R[0:paddedWidth, last: last + 1] = R[0:paddedWidth, height - 1:height]
        G[0:paddedWidth, last: last + 1] = G[0:paddedWidth, height - 1:height]
        B[0:paddedWidth, last: last + 1] = B[0:paddedWidth, height - 1:height]

    # Stack the RBG as a 3D numpy array
    array = np.stack((R, B, G), axis=-1)

    return (array)


def pad_array2d(array, width, height, paddedWidth, paddedHeight):
    """
    A function that pads a 2D numpy array to ensure multiples of 8 on both
    rows and columns

    Parameters
    ----------
    array : ndarray
        Numpy 2D array with either float or int type values
    width : int
        the original width of the array
    height : int
        the original height of the array
    paddedWidth : int
        the padded width of the array
    paddedHeight : int
        the padded height of the array

    Return
    ------
    ndarray:
        2D numpy array that both the height and the width are divisible by 8
    """

    # Create a 2X2 array using '1' as the default element
    ar = np.ones((paddedWidth, paddedHeight), dtype=np.int64)

    # Copy previous array elements into the new array
    ar[0:width:, 0:height] = array[:, :]

    w_diff = paddedWidth - width
    h_diff = paddedHeight - height

    # Extend the last element of the rows and columns to fill the matrix
    for w in range(w_diff):
        last = w + width
        ar[last:last + 1, 0:paddedHeight] = ar[width - 1:width, 0:paddedHeight]

    for h in range(h_diff):
        last = h + height
        ar[0:paddedWidth, last: last + 1] =\
            ar[0:paddedWidth, height - 1:height]

    return (ar)


def pad_array(array, paddedWidth, paddedHeight):
    """
    A function that pads a 3D or 2D numpy array to
    ensure multiples of 8 on bothrows and columns

    Parameters
    ----------
    array : ndarray
        Numpy 3D or 2D array with either float or int type values
    paddedWidth : int
        the padded width of the array
    paddedHeight : int
        the padded height of the array

    Return
    ------
    ndarray:
        3D or 2D numpy array that both the height and the width of the
        arrays are divisible by 8
    """

    if not isinstance(array, np.ndarray):
        raise TypeError('Array must be an ndarray')
    dim = array.ndim
    if (dim < 2) or (dim > 3):
        raise TypeError('ndarray must be either 2D or 3D')
    if not (isinstance(paddedWidth, int)
            and isinstance(paddedHeight, int)):
        raise TypeError('ndarray dimensions must be integers')
    array_shape = array.shape
    w = array_shape[0]
    h = array_shape[1]

    if (w > paddedWidth) or (h > paddedHeight):
        text = 'padded dimensions is less than array dimensions'
        raise ValueError(text)

    if (w == paddedWidth) and (h == paddedHeight):
        return (array)

    if dim == 2:
        return pad_array2d(array, w, h, paddedWidth, paddedHeight)
    else:
        return pad_array3d(array, w, h, paddedWidth, paddedHeight)
