#!/usr/bin/env python3

"""
A module that uses the python pillow module to get an image file,
get the 3D RGB channels from the image file,
and save to JPEG format
"""

# Python modules
import numpy as np
from PIL import Image
from multiprocessing import Process
import cv2
import os


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


def show_image(name) -> None:
    """
    A function that uses open cv to show_image an image file

    Parameters
    ----------
    name: str
        The fullpath of the image file to display
    """
    image = cv2.imread(name)
    if image is None:
        raise FileNotFoundError('Cannot Open image')

    _, filename = os.path.split(name)
    cv2.namedWindow(filename, cv2.WINDOW_NORMAL)
    cv2.imshow(filename, image)

    while True:
        k = cv2.waitKey(100)
        if k == 27:
            cv2.destroyAllWindows()
            break
        if cv2.getWindowProperty(filename, cv2.WND_PROP_VISIBLE) < 1:
            break
    cv2.destroyAllWindows()


def display(name1, name2="") -> None:
    """
    A function that uses the show_image function to display either one image
    or two images side by side

    Parameters
    ----------
    name1 : str
        Full path of the first image to dispay
    name2 : str
        Full path of the second image to dispay
    """
    if not name2:
        show_image(name1)
    else:
        t1 = Process(target=show_image, args=(name1,))
        t2 = Process(target=show_image, args=(name2,))
        t1.start()
        t2.start()
        t1.join()
        t2.join()


def print_details(image_details) -> None:
    """
    Prints the details of the compressed image in a
    well formatted way

    Parameters
    ----------
    image_details : dict
        Dictionary of the formatted image
    """
    # From image_details dictionary, the maximum obtainable widths are:
    # name :
    #    Original : 10
    #    Compressed : 18
    # size :
    #    Both are of max length 6

    _, name1 = os.path.split(image_details.get('in_image_name'))
    name2 = image_details.get('compressed_image_name')
    resolution = image_details.get('out_resolution')
    size1 = image_details.get('in_size')
    size2 = image_details.get('out_size')
    comp_time = image_details.get('time_taken')
    quality = image_details.get('quality')

    header = f"    {' ': <{4}} | {'ORIGINAL': <{10}} | {'COMPRESSED': <{18}}"
    name = f"    {'Name': <{4}} | {name1: <{10}} | {name2: <{18}}"
    size = f"    {'Size': <{4}} | {size1: <{10}} | {size2: <{18}}"

    print(f"\t Image ID: {name2}")
    print(f"\t Resolution: {resolution}")
    print(f"\t Time Taken: {comp_time}")
    print(f"\t Quality: {quality}")

    print(header)
    print(f"{'-' * (len(header) + 4)}")
    print(name)
    print(f"{'-' * (len(header) + 4)}")
    print(size)
    print(f"{'-' * (len(header) + 4)}")
