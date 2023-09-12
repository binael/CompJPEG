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
import json
import shlex


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


def get_path_array(args, file_type) -> list:
    """
    Formats input args into lists containing image path and
    quality

    Parameters
    ----------
    args : str
        The string containing the pathname or the details for
        the compressed files
    file_type : string
        The string containing the type of file to process
        Types are:
        ---------
        file :
            file_type for args containing pathnames and qualitys
        json :
            json file type for the image detail
        directory :
            the directory where the image files can be found
        text :
            the text document with image file details

    Returns
    -------
    list of list :
        containing image paths and quality
    """
    if file_type == 'file':
        args_list = file_array(args)
        if not args_list:
            return None
    elif file_type == 'directory':
        args_list = dir_array(args)
        if not args_list:
            return None
    elif file_type == 'json':
        args_list = json_array(args)
        if not args_list:
            return None
    elif file_type == 'text':
        args_list = text_array(args)
        if not args_list:
            return None
    else:
        return None

    image_array = []
    # Loop Through each array
    for arg in args_list:
        # Split into pathname and quality
        arg_list = shlex.split(arg)
        if len(arg_list) != 2:
            print(f"ERROR: Wrong number of input args:\t{arg}")
            return None
        # Loop through pathname and quality
        filename = quality = None
        for key_value in arg_list:
            # Break into key-value
            kv = key_value.split('=')
            check = False
            if len(kv) > 1 and kv[0] == 'path':
                filename = kv[1]
                check = True
            elif len(kv) > 1 and kv[0] == 'quality':
                quality = kv[1]
                check = True
                try:
                    quality = int(quality)
                except:
                    print(f"ERROR: Conversion to int failed:\t{arg}'")
                    return None
            if check == False:
                print(f"ERROR: Wrong key-value pair:\t{arg}")
                return None
        if not (filename and quality):
            print(f"ERROR: path and type must be valid inputs:\t{arg}")
            return None
        image_array.append(list((filename, quality)))
    return (image_array)


def file_array(args):
    """
    Gets the array from input str

    Parameters
    ----------
    args : str
        The string containing the pathname or the details for
        the compressed files

    Returns
    -------
    list :
        containing image paths and quality
    """
    # Get arrays containing individual details
    return (shlex.split(args))


def json_array(args):
    """
    Gets the array from json file

    Parameters
    ----------
    args : str
        The string containing the pathname or the details for
        the compressed files

    Returns
    -------
    list of list :
        containing image paths and quality
    """
    try:
        with open(args, mode="r") as jfile:
            jo = json.load(jfile)
    except:
        print(f'ERROR: Failed to open json file:\t{args}')
        return None
    args_list = []
    for data in jo:
        path = data.get('path')
        quality = data.get('quality')
        if path and quality:
            ar_string = f'path={path} quality={quality}'
            args_list.append(ar_string)
    return (args_list)


def dir_array(args):
    """
    Gets the array from directory

    Parameters
    ----------
    args : str
        The string containing the pathname or the details for
        the compressed files

    Returns
    -------
    list of list :
        containing image paths and quality
    """
    if args[-1] == '/':
        args = args[0:-1]
    if os.path.exists(args) and os.path.isdir(args):
        files_and_dirs = os.listdir(args)
    else:
        print(f"ERROR: No directory found: \t{args}")
        return None
    args_list = []
    for all_files in files_and_dirs:
        new_file = os.path.join(args, all_files)
        if os.path.isfile(new_file):
            path = new_file
            quality = 50
            ar_string = f'path={path} quality={quality}'
            args_list.append(ar_string)
    return (args_list)


def text_array(args):
    """
    Gets the array from text file

    Parameters
    ----------
    args : str
        The string containing the pathname or the details for
        the compressed files

    Returns
    -------
    list of list :
        containing image paths and quality
    """
    if not is_text_file(args):
        print(f'ERROR: Failed to open text file:\t{args}')
        return None
    with open(args, mode="r") as txt:
        lines = txt.readlines()
        args_list = []
        for line in lines:
            if ("path" in line) and ("quality" in line):
                args_list.append(line)
    return (args_list)


def is_text_file(filename):
    """
    Checks if a file is a text file

    Parameters
    ----------
    filename : str
        The filepath of the text file

    Returns
    bool :
        True if text file or False if not
    """
    # Ensure the file exists and no other error in handlig
    try:
        # Check if file has any content
        if os.path.getsize(filename) == 0:
            return False
        # Check if file has any binary or printable value
        with open(filename, mode="r", encoding='utf-8') as text_file:
            # Break into chunks
            data = text_file.read(1024)
            while data:
                for byte in data:
                    c = ord(byte)
                    # Check if values are printable ascii
                    if c not in (10, 13) and (c < 32 or c > 126):
                        return False
                data = text_file.read(1024)
    except Exception:
        return False
    else:
        return True
