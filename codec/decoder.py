#!/usr/bin/env python3

"""
A module that decodes
"""
import numpy as np
from util_func import IDCT
from util_func import de_quantize


class Decoder:
    """
    """

    bits = 8

    def __init__(self, array, width, height, paddedWidth, paddedHeight, quality=50):
        self.__array = array
        self.__quality = quality
        self.__paddedWidth = paddedWidth
        self.__paddedHeight = paddedHeight
        self.__width = width
        self.__height = height

    @property
    def array(self):
        return self.__array

    def decompression(self):
        """
        A function that decompresses the image by applying dct transform
        and then quantization

        Return
        ------
        array: numpy 3D array
            the decompressed YCrCb image array
        """

        # Get the nd array dimensions
        D = self.__array.ndim

        # Divide the width and height into 8X8 sections
        row_section = self.__paddedWidth // self.bits
        col_section = self.__paddedHeight // self.bits

        # Create a new array
        ar_copy = np.empty((self.__paddedWidth, self.__paddedHeight, D))

        # Compress
        for d in range(D):
            if d == 0:
                mode = 'luma'
            else:
                mode = 'chroma'
            for row in range(row_section):
                r_start = row * self.bits
                r_end = r_start + self.bits
                for col in range(col_section):
                    c_start = col * self.bits
                    c_end = c_start + self.bits

                    # Get the 8X8 slice
                    mat_8 = self.__array[r_start:r_end, c_start:c_end, d]
                    # Dequantize
                    quant = de_quantize(mat_8, self.__quality, mode)
                    # Transform using IDCT
                    dct = IDCT(quant)
                    # Copy value into the new array
                    ar_copy[r_start:r_end, c_start:c_end, d] = dct

        self.__array = ar_copy
        return (ar_copy)


    def reverse_padding(self):
        """
        """
        Y = self.__array[0:self.__width, 0:self.__height, 0]
        Cr = self.__array[0:self.__width, 0:self.__height, 1]
        Cb = self.__array[0:self.__width, 0:self.__height, 2]

        self.__array = np.stack((Y, Cr, Cb), axis=-1)


    def YCrCb2BRG(self):
        """
        Function that converts data from YCrCb to RGB

        Formular
        --------
            $ R = Y + 1.402 * (Cr - 128)
            $ G = Y - 0.34414 * (Cb - 128) - 0.7141 * (Cr - 128)
            $ B = Y + 1.772 * (Cb - 128)

        Return
        ------
            array : numpy 3D array
                image array in RBG color space
        """

        Y = self.__array[:, :, 0]
        Cr = self.__array[:, :, 1]
        Cb = self.__array[:, :, 2]

        R = Y + 1.403 * (Cr - 128)
        G = Y - 0.344 * (Cb - 128) - 0.7141 * (Cr - 128)
        B = Y + 1.773 * (Cb - 128)

        self.__array = np.clip(np.stack((R, G, B), axis=-1), 0, 255)


    def reverse_sampling(self):
        """
        Function that changes the values from signed representation
        to unsigned representation

        Return
        ------
        array : numpy 3D array
            An unsigned array with values from 0 - 255
        """

        self.__array = self.__array + 128
        return (self.__array)
