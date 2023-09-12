#!/usr/bin/env python3
import os
import json
from fileIO import storage



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


last = storage.last_object()
print_details(last)
