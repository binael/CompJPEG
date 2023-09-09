#!/usr/bin/env python3

"""
A module that decompresses an image array

Stage in Decoding
-----------------
    Dequantization:
        Dequantization of the YCrCb
    Inverse DCT Transform:
        Applying IDCT to the Dequantized array
    Reverse Padding:
        Bringing the array back to its original form
    Reverse_Sampling (Up Sampling)
    RGB Conversion
"""

# Python modules utilized
import numpy as np

# Modules (functions) from util_func package
from util_func import IDCT
from util_func import de_quantize


class Decoder:
    """
    A class that decompresses an image array

    Parameters:
    -----------
    bits : int
        The MCU dimensions

    Methods:
    --------
    decompression
        Applies dequantization and idct to the each 8X8 image
        array MCU
    reverse_padding:
        Returns the padded arrays to their original shapes
    YCrCb2RGB:
        Converts image array pixels/data from YCrCb color
        channel to RGB
    reverse_sampling:
        returns array data from signed representation to
        unsigned representation
    """

    bits = 8

    def __init__(self, Y, Cr, Cb, width, height,
                 paddedWidth, paddedHeight, quality=50):
        """
        Instance attributes

        Attributes
        ----------
        Y: ndarray
            2D ndarray of Y (luminance) color channel
        Cr: ndarray
            2D ndarray of Cr (red chrominance) color channel
        Cb: ndarray
            2D ndarray of Cb (blue chrominance) color channel
        width: int
            The initial width of the arrays before padding
        height: int
            The initial height of the arrays before padding
        paddedWidth: int
            The padded width of the arrays
        paddedHeight: int
            The padded height of the arrays
        quality: variable int
            The quality needed for image compression
        """
        self.__quality = quality
        self.__paddedWidth = paddedWidth
        self.__paddedHeight = paddedHeight
        self.__width = width
        self.__height = height
        self.__Y = Y
        self.__Cr = Cr
        self.__Cb = Cb
        self.__array = None

    @property
    def array(self):
        return self.__array

    def decompression(self) -> None:
        """
        A function that decompresses the image by applying dct transform
        and then quantization
        """

        # Divide the width and height into 8X8 sections
        row_section = self.__paddedWidth // self.bits
        col_section = self.__paddedHeight // self.bits

        # decompress and perfom dct transform
        for row in range(row_section):
            r_start = row * self.bits
            r_end = r_start + self.bits
            for col in range(col_section):
                c_start = col * self.bits
                c_end = c_start + self.bits

                # ================================ #
                # Get the 8X8 slice of the array   #
                # Dequantize                       #
                # Perform IDCT                     #
                # Copy into the array channel      #
                # ================================ #

                # For Y channel
                mat_8 = self.__Y[r_start:r_end, c_start:c_end]
                dequant = de_quantize(mat_8, self.__quality, channel='luma')
                idct = IDCT(dequant)
                self.__Y[r_start:r_end, c_start:c_end] = idct

                # For Cr channel
                mat_8 = self.__Cr[r_start:r_end, c_start:c_end]
                dequant = de_quantize(mat_8, self.__quality, channel='luma')
                idct = IDCT(dequant)
                self.__Cr[r_start:r_end, c_start:c_end] = idct

                # For Cb channel
                mat_8 = self.__Cb[r_start:r_end, c_start:c_end]
                dequant = de_quantize(mat_8, self.__quality, channel='luma')
                idct = IDCT(dequant)
                self.__Cb[r_start:r_end, c_start:c_end] = idct

    def reverse_padding(self) -> None:
        """
        A function that reverses the padded dimensions of each
        color channel array to the original dimension
        """
        self.__Y = self.__Y[0:self.__width, 0:self.__height]
        self.__Cr = self.__Cr[0:self.__width, 0:self.__height]
        self.__Cb = self.__Cb[0:self.__width, 0:self.__height]

    def YCrCb2RGB(self) -> None:
        """
        Function that converts data from YCrCb to RGB

        Formular
        --------
            $ R = Y + 1.402 * (Cr - 128)
            $ G = Y - 0.34414 * (Cb - 128) - 0.7141 * (Cr - 128)
            $ B = Y + 1.772 * (Cb - 128)
        """

        R = self.__Y + 1.403 * (self.__Cr - 128)
        G = self.__Y - 0.344 * (self.__Cb - 128) - 0.7141 * (self.__Cr - 128)
        B = self.__Y + 1.773 * (self.__Cb - 128)
        # Stack the R, G and B channels to a 3D np array
        # and ensure values are within 0 and 255
        self.__array = np.clip(np.stack((R, G, B), axis=-1), 0, 255)

    def reverse_sampling(self) -> None:
        """
        Function that changes the values from signed representation
        to unsigned representation
        """

        self.__Y = self.__Y + 128
        self.__Cr = self.__Cr + 128
        self.__Cb = self.__Cb + 128
