#!/usr/bin/env python3

"""
This module implements implements both encoding and decoding
of the image to enable image compression
"""

# Python modules utilized
from uuid import uuid4
from datetime import datetime
import os

# Modules (functions) from codec package
from codec import Encoder
from codec import Decoder

# Modules (functions) from util_func package
from util_func import picture_resolution
from util_func import get_image_size

# Modules (functions) from fileIO package
from fileIO import save_image
from fileIO import get_image_array
from fileIO.filestorage import FileStorage


def picture(filename, quality=50, output_image_name=None):
    """
    The main function that compresses an image file

    Parameters:
    -----------
    filename: str
        The pathname of the image file to compress
    quality: int
        The compression quality required
    output_image_name: str
        The pathname to store the compressed image

    Returns:
    --------
    dict
        A dictionary containing information about the
        compressed image file
        {
            user_id : str - (auto generated id from uuid)
            quality : int - (user compressed quality)
            start_time : str - (datetime compression started)
            end_time : str - (datetime compression was completed)
            time_taken : str - (time in mins for compression)
            image_name: str - (the name of the compressed image file)
            in_size : str - (size of the input image file)
            out_size : str - (size of the compressed image)
            in_resolution : str (input image resolution)
            out_resolution : str (output image resolution)
        }
    """

    start_time = datetime.now()
    ar, input_details = compress_image(filename, quality)
    image_array = decompress_image(ar, input_details)
    end_time = datetime.now()

    # Get unique ID for each user
    user_id = str(uuid4())

    # Get the pathname to save image file
    dirname, in_name, ext = format_image_name(filename)
    output_path = f'{dirname}compressed_jpeg/'
    if output_image_name:
        compressed_image_name = output_image_name
    else:
        compressed_image_name = f'{in_name}-{user_id[0:8]}.{ext}'
    full_path = f'{output_path}{compressed_image_name}'

    # If the directory does not exit, create it
    os.makedirs(output_path, exist_ok=True)
    # Save the image file
    save_image(image_array, full_path)

    # Get the input image size and output image size
    in_size = get_image_size(filename)
    out_size = get_image_size(full_path)

    # Get the image resolution
    in_resolution = picture_resolution(filename)
    out_resolution = picture_resolution(full_path)

    # Get the time taken
    start_time_str = start_time.strftime("%y-%m-%dT%H:%M:%S")
    end_time_str = end_time.strftime("%y-%m-%dT%H:%M:%S")
    t = end_time - start_time
    t = t.total_seconds()
    time_diff = "{:.0f}m:{:.0f}s".format((t // 60), (t % 60))
    im_details = {
        'user_id': user_id,
        'quality': quality,
        'start_time': start_time_str,
        'end_time': end_time_str,
        'time_taken': time_diff,
        'in_image_name': filename,
        'compressed_image_name': compressed_image_name,
        'out_fullpath': full_path,
        'in_size': in_size,
        'in_resolution': in_resolution,
        'out_resolution': out_resolution,
        'out_size': out_size
    }

    # Save the details of the compressed file
    if not FileStorage.objects:
        FileStorage.reload()
    FileStorage.new(im_details)
    FileStorage.save()

    return (im_details)


def compress_image(filename, quality) -> tuple:
    """
    Function that decodes the image, passing the image file
    through extraction to quantization

    Parameters:
    -----------
    filename: str
        The pathname of the image file to compress
    quality: int
        The compression quality required

    Returns
    -------
    tuple
        image_tuple : tuple
            A tuple containing Y, Cr, Cb color channels
        input_details: dict
            {
                width: int
                height: int
                paddedWidth: int
                paddedHeight: int
                quality: int
            }
    """

    image_array = get_image_array(filename)
    R = image_array[:, :, 0]
    G = image_array[:, :, 1]
    B = image_array[:, :, 2]
    image_tuple = (R, G, B)
    input_details = {
        'width': 0,
        'height': 0,
        'paddedHeight': 0,
        'paddedWidth': 0,
        'quality': quality
    }
    if quality > 95 and quality <= 100:
        return (image_tup, input_details)
    # Call the Encode functions to compress Image
    encode = Encoder(image_array, quality)
    encode.RGB2YCrCb()
    encode.sampling()
    encode.padding()
    encode.compression()

    input_details['width'] = encode.width
    input_details['height'] = encode.height
    input_details['paddedHeight'] = encode.paddedHeight
    input_details['paddedWidth'] = encode.paddedWidth

    image_tuple = (encode.Y, encode.Cr, encode.Cb)
    return (image_tuple, input_details)


def decompress_image(image_tuple, input_details):
    """
    A function that decompresses the encoded image arrays
    back to RGB color channel

    Parameters
    ----------
    image_tuple : tuple
        tuple containing the Y, Cr, Cb channels
    input_details : dict
        dict values with the image dimensions

    Returns
    -------
        ndarray:
            3D ndarray in RGB color channel
    """

    quality = input_details['quality']
    if quality > 95 and quality <= 100:
        return image_array

    width = input_details['width']
    height = input_details['height']
    paddedHeight = input_details['paddedHeight']
    paddedWidth = input_details['paddedWidth']
    Y, Cr, Cb = image_tuple[0], image_tuple[1], image_tuple[2]

    decode = Decoder(Y, Cr, Cb, width, height,
                     paddedWidth, paddedHeight, quality)
    decode.decompression()
    decode.reverse_padding()
    decode.reverse_sampling()
    decode.YCrCb2RGB()

    return (decode.array)


def format_image_name(filename):
    """
    Function that formats an input image name

    Parameters:
    -----------
    filename: str
        The pathname of the image file to compress

    Returns:
    --------
    tuple:
        dirname : str
            directory name
        image_file : str
            the formattedimage file name without extension
        ext : str
            the image extension
    """

    # Get the path and the filename
    if os.path.exists(filename):
        dirname, image_file = os.path.split(filename)
    else:
        raise FileNotFoundError('No file found')
    # # Get only the first 10 letters of the image file
    img_name_ar = image_file.split('.')
    # Get the image extension (jpeg or jpg or jfif etc)
    ext = img_name_ar[-1]
    name_without_ext = ''.join(img_name_ar[0:-1])
    if len(name_without_ext) > 10:
        image_file = f'{name_without_ext[0:9]}'
    else:
        image_file = name_without_ext
    if not dirname:
        dirname = '.'
    else:
        dirname = dirname + '/'
    return (dirname, image_file, ext)
