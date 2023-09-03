#!/usr/bin/env python3

"""
Implentation of padding for 3D array
"""

import numpy as np


def pad_array3d(array, height, width, paddedHeight, paddedWidth):
    """
    A function that pads a 3D numpy array to ensure multiples of 8 on both
    rows and columns

    Parameters
    ----------
    array : ndarray
        Numpy 3D array with either float or int type values
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
    ndarray:
        3D numpy array that both the width and the height of the 
        individual 2D arrays are divisible by 8
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


def pad_array2d(array, height, width, paddedHeight, paddedWidth):
    """
    A function that pads a 2D numpy array to ensure multiples of 8 on both
    rows and columns

    Parameters
    ----------
    array : ndarray
        Numpy 2D array with either float or int type values
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
    ndarray:
        2D numpy array that both the width and the height are divisible by 8
    """

    # Create a 2X2 array using '1' as the default element
    ar = np.ones((paddedHeight, paddedWidth), dtype=np.int64)

    # Copy previous array elements into the new array
    ar[0:height:, 0:width] = array[:, :]

    h_diff = paddedHeight - height
    w_diff = paddedWidth - width

    # Extend the last element of the rows and columns to fill the matrix
    for h in range(h_diff):
        last = h + height
        ar[last:last + 1, 0:paddedWidth] = ar[height - 1:height, 0:paddedWidth]

    for w in range(w_diff):
        last = w + width
        ar[0:paddedHeight, last: last + 1] = ar[0:paddedHeight, width - 1:width]

    return (ar)


def pad_array(array, paddedHeight, paddedWidth):
    """
    A function that pads a 3D or 2D numpy array to ensure multiples of 8 on both
    rows and columns

    Parameters
    ----------
    array : ndarray
        Numpy 3D or 2D array with either float or int type values
    paddedHeight : int
        the padded height of the array
    paddedWidth : int
        the padded width of the array

    Return
    ------
    ndarray:
        3D or 2D numpy array that both the width and the height of the 
        arrays are divisible by 8
    """

    if not isinstance(array, np.ndarray):
        raise TypeError('Array must be an ndarray')
    dim = array.ndim
    if (dim < 2) or (dim > 3):
        raise TypeError('ndarray must be either 2D or 3D')
    if not (isinstance(paddedHeight, int)
            and isinstance(paddedWidth, int)):
        raise TypeError('ndarray dimensions must be integers')
    array_shape = array.shape
    h = array_shape[0]
    w = array_shape[1]

    if (h > paddedHeight) or (w > paddedWidth):
        text = 'padded dimensions is less than array dimensions'
        raise ValueError(text)

    if (h == paddedHeight) and (w == paddedWidth):
        return (array)

    if dim == 2:
        return pad_array2d(array, h, w, paddedHeight, paddedWidth)
    else:
        return pad_array3d(array, h, w,paddedHeight, paddedWidth)
