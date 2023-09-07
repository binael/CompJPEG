#!/usr/bin/env python3

from uuid import uuid4
from datetime import datetime
import os

from codec import Encoder
from codec import Decoder
from util_func import picture_resolution
from util_func import get_image_size
from fileIO import save_image
from fileIO import get_image_array

def picture(filename, quality=50, output_image_name=None):
    """
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
    start_time_str = start_time.strftime("%y:%m:%d:%H:%M:%S")
    end_time_str = end_time.strftime("%y:%m:%d:%H:%M:%S")
    t = end_time - start_time
    t = t.total_seconds()
    time_diff = "{:.0f}m:{:.0f}s".format((t / 60), (t % 60))

    im_details = {
        'user_id': user_id,
        'quality': quality,
        'start_time': start_time_str,
        'end_time': end_time_str,
        'time_taken': time_diff,
        'image_name': compressed_image_name,
        'in_size': in_size,
        'in_resolution': in_resolution,
        'out_resolution': out_resolution,
        'out_size': out_size
	}
    return im_details


def compress_image(filename, quality):
    """
    """
    image_array = get_image_array(filename)
    input_details = {
        'width': 0,
        'height': 0,
        'paddedHeight': 0,
        'paddedWidth': 0,
        'quality': quality
	}

    if quality > 95 and quality <= 100:
        return (image_array, input_details)

    # Call the Encode functions to compress Image
    encode = Encoder(image_array, quality)
    encode.RGB2YCrCb()
    encode.sampling()
    encode.padding()
    # encode.compression()

    input_details['width'] = encode.width
    input_details['height'] = encode.height
    input_details['paddedHeight'] = encode.paddedHeight
    input_details['paddedWidth'] = encode.paddedWidth

    return (encode.array, input_details)


def decompress_image(image_array, input_details):
    """
    """

    quality = input_details['quality']
    if quality > 95 and quality <= 100:
        return image_array

    width = input_details['width']
    height = input_details['height']
    paddedHeight = input_details['paddedHeight']
    paddedWidth = input_details['paddedWidth']

    decode = Decoder(image_array, width, height, paddedWidth,
                     paddedHeight, quality)
    # decode.decompression()
    decode.reverse_padding()
    decode.reverse_sampling()
    decode.YCrCb2RGB()

    return (decode.array)


def format_image_name(filename):
    """
    """

    # Get the path and the filename
    if os.path.exists(filename):
        dirname, image_file = os.path.split(filename)
    else:
        raise FileNotFoundError('No file found')

    ## Get only the first 10 letters of the image file

    img_name_ar = image_file.split('.')

    # Get the image extension (jpeg or jpg or jfif etc)
    ext = img_name_ar[-1]

    name_without_ext = ''.join(img_name_ar[0:-1])

    if len(name_without_ext) > 10:
        image_file = f'{name_without_ext[0:9]}'
    else:
        image_file = name_without_ext

    if not dirname:
        dirname = ''
    else:
        dirname = dirname + '/'

    return (dirname, image_file, ext)
