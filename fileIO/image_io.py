#!/usr/bin/env python3

"""
A module that uses the python pillow module to get an image file,
get the 3D RGB channels from the image file,
and save to JPEG format
"""

# Python modules
import numpy as np
from PIL import Image

def save_image(array, filename) -> None:
    """
    A function that saves a compressed image from array

    Parameters
    ----------
    array: ndarray
        3D nd arrray of the pixels
    filename: file
        The filepath and name to save the image
    """

    if not np.any(array):
        raise ValueError('Array must be a non empty array')

    if not isinstance(array, np.ndarray):
        raise TypeError('Array must be an ndarray')

    if not (array.ndim == 3):
        raise TypeError('Array must be a 3D array')

    image = Image.fromarray(array.astype(np.uint8))
    image.save(filename)


def get_image_array(filename) -> np.ndarray:
    """
    A function that gets an image array from an image file

    Parameters
    ----------
    filename: file
        The filepath of the image file

    Returns
    -------
    ndarray:
        3D ndarray of the image file
    """

    with Image.open(filename) as img:
        if img.format != "JPEG":
            raise TypeError('Image must be JPEG format')
        if img.mode != "RGB":
            raise TypeError(f'Image mode must be RGB. {img.mode} not allowed')
        image_array = np.array(img)

    return (image_array)
