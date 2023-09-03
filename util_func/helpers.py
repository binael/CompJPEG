#!/usr/bin/env python3

"""
This module contain helper functions that imports from C dynamic 
or shared library

Variables
---------
dll : c_type
    Imported C dynamic library

Note
----
Matrix - An array of array | 2D array
"""

from ctypes.util import find_library
from ctypes import *


libc = CDLL(find_library("c"))

try:
    dll = CDLL("./C_library/liball.so")
except OSError as e:
    print("Error loading shared library:", e)
    exit(1)


def picture_resolution(image) -> str:
    """
    Displays a string version of the picture resolution

    parameters
    ----------
    image: str
        the string path of the image file

    Returns:
    str:
        A string represention of the picture resolution

    Example:
        >> picture_resolution(filepath)
        >> 720 X 1024
    """

    if not isinstance(image, str):
        raise TypeError('Input must be a string of filepath')
    if not image:
        raise ValueError('Input must be a string of filepath')
    resolution = dll.picture_resolution

    resolution.argtypes = [c_char_p]
    resolution.restype = c_char_p
    image_file = c_char_p(image.encode())

    result = resolution(image_file)

    if result == None:
        raise FileNotFoundError('File could not be opened')

    return (result.decode())


def get_dimension(image: str) -> tuple:
    """
    A function that uses fetches the dimension (h, w) of an image

    parameters
    ----------
    image: str
        the string path of the image file

    Note
    ----
    This function imports picture_resolution function and extracts
    the dimensions

    Returns
    -------
    dimension: tuple
        (height : int, width : int)
    """
    if not isinstance(image, str):
        raise TypeError('Input must be a string of filepath')
    if not image:
        raise ValueError('Input must be a string of filepath')

    resolution = picture_resolution(image)
    dimension = resolution.split(' X ')

    return (int(dimension[0]), int(dimension[1]))


def get_image_size(image: str) -> str:
    """
    A function that returns the sizes of image files

    parameters
    ----------
    image: str
        the string path of the image file

    Example
    -------
        $ get_image_size(image_file)
        $ > 23.3KB
        $ get_image_size(image_file)
        $ > 489B
        $ get_image_size(image_file)
        $ > 4.45MB

    Return
    ------
    str:
        the size of the image file
    """

    if not isinstance(image, str):
        raise TypeError('Input must be a string of filepath')
    if not image:
        raise ValueError('Input must be a string of filepath')

    picture_size = dll.picture_size_str
    picture_size.argtypes = [c_char_p]
    picture_size.restype = c_char_p

    image_file = c_char_p(image.encode())

    size_in_str = picture_size(image_file)

    if size_in_str == None:
        raise FileNotFoundError('File could not be opened')

    return(size_in_str.decode())
