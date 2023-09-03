#!/usr/bin/env python3

"""
A module that defines the quantization table that will be used for the
project

Variables
---------
QUANTIZATION_LUMA_50 : list
    2D numpy array for the JPEG standard at a quantization ratio
    of 50 for luminance
QUANTIZATION_LUMA_50 : list
    2D numpy array for the JPEG standard at a quantization ratio
    of 50 for chrominance

Formula
-------
    # Q - quantization table for JPEG 50 standard
    # quality = the quantization faction
    # IF QUALITY >= 50:
        $ result = (100 - quality) / 50
    # IF QUALITY < 50:
        $ result = 50 / quality

Note
----
Matrix - An array of array | 2D array
"""

import numpy as np

QUANTIZATION_CHROMA_50 = np.array((
    (17, 18, 24, 47, 99, 99, 99, 99),
    (18, 21, 26, 66, 99, 99, 99, 99),
    (24, 26, 56, 99, 99, 99, 99, 99),
    (47, 66, 99, 99, 99, 99, 99, 99),
    (99, 99, 99, 99, 99, 99, 99, 99),
    (99, 99, 99, 99, 99, 99, 99, 99),
    (99, 99, 99, 99, 99, 99, 99, 99),
    (99, 99, 99, 99, 99, 99, 99, 99)
))

QUANTIZATION_LUMA_50 = np.array((
    (16, 11, 10, 16, 24, 40, 51, 61),
    (12, 12, 14, 19, 26, 58, 60, 55),
    (14, 13, 16, 24, 40, 57, 69, 56),
    (14, 17, 22, 29, 51, 87, 80, 62),
    (18, 22, 37, 56, 68, 109, 103, 77),
    (24, 36, 55, 64, 81, 104, 113, 92),
    (49, 64, 78, 87, 103, 121, 120, 101),
    (72, 92, 95, 98, 112, 100, 103, 99)
))


def get_quantRatio(quality, mode='all') -> list | tuple:
    """
    A function that computes the quantization array of array from the user
    quality

    parameters
    ----------
    quality : int
        the compression quality
    mode : str
        the color channel for the quantization
        all (default) - gets both Y and C color channels
        chroma - gets only the C channel (ie CrCb)
        luma - gets only the Y channel

    Returns
    ------
    ndarray :
        An 8X8 nd array of integers ranging from 0-255
        result may be a single nd array or a tuple of ndarrays

        # if mode = 'all'
        # (ndarray_luma, ndarray_chroma)
    """

    # Handle input errors
    if not isinstance(quality, int):
        raise TypeError('Quality must be an integer')
    if not isinstance(mode, str):
        raise TypeError("mode is not an integer")
    if mode.lower().strip() not in ['all', 'luma', 'chroma']:
        raise ValueError('mode must be "all, luma or chroma"')
    if quality < 1 or quality > 100:
        raise ValueError('Quality must be between 1 and 100')

    if quality >= 50:
        ratio = (100 - quality) / 50
    else:
        ratio = 50 / quality

    # Get quantization table for luma
    luma_quant = QUANTIZATION_LUMA_50 * ratio
    luma_quant = luma_quant.round().astype(int)

    # Get quantization table for chroma
    chroma_quant = QUANTIZATION_CHROMA_50 * ratio
    chroma_quant = chroma_quant.round().astype(int)

    # Ensure no value passes 255 or are below 256
    luma_array = np.minimum(luma_quant, 255)
    chroma_array = np.minimum(chroma_quant, 255)

    # # Using lamda to ensure values are below 256
    # mat = list(map(lambda x: list(map(
    #     lambda y: 255 if y > 255 else y, x)),luma_quant))

    if (mode.lower() == 'luma'):
        return (luma_array)
    if (mode.lower() == 'chroma'):
        return (chroma_array)

    return (luma_array, chroma_array)
