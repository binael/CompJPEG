#!/usr/bin/env python3

"""
Module to deserialize json files into object (dictionary)
"""


class Details:
    """
    Class to deserialize json files into objects
    """

    def __init__(self, user_id, quality, start_time, end_time, time_taken,
                 in_image_name, compressed_image_name, out_fullpath,
                 in_size, in_resolution, out_resolution,
                 out_size):
        self.user_id = user_id
        self.quality = quality
        self.start_time = start_time
        self.end_time = end_time
        self.time_taken = time_taken
        self.in_image_name = in_image_name
        self.compressed_image_name = compressed_image_name
        self.out_fullpath = out_fullpath
        self.in_size = in_size
        self.in_resolution = in_resolution
        self.out_resolution = out_resolution
        self.out_size = out_size
