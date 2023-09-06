#!/usr/bin/env python3
"""
A module that passes jpeg raster array through various stages of
jpeg encoding to ultimately compress the image

Raster array are the actual array in jpeg that will be encoded
Raster array are ususally represented with a 3D array to show
the RBG color layout (Though some images with APP14 markers may
specify YCrCb encoded mode for the picture)

STAGES IN ENCODING:
-------------------
    Getting the Image:
        This is implemented using python pillow library and
        converted to 3d array using numpy.
        A library is important in order to account for various JPEG
        formats and permutations/combinations of the JPEG markers
    Padding:
        Image array are usually processed in 8x8 MCUs (minimum coded units)
        and so, both the width and height (dimensions) of the images
        must be in multiples of 8. Any value can be chosen in extending your
        image rows and columns to match the multiples of 8
    Sub Sampling:
        This was not implemented in the project
    YCrCb Conversion:
        This involves transforming the image array from RGB to
        Y(luminance) and Cr, Cb (chrominance values). This method is
        skipped if the image mode is already in YCrCb mode
    Level Shifting:
        Image array are transformed from 8bit unsigned to 8bit signed
        representation by subtraction "128" from each array value
        mat[i][j] - 128
    DCT Transform:
        DCT Transform is then applied to the image to transform to frequency
        domain
    Quantization:
        This is the stage that the actual compression takes place
        A quantization table with the specified compression ratio is
        applied to the image array to compress the array

"""

import numpy as np
from math import ceil, sqrt
from util_func import pad_array
from util_func import cosine_array
from util_func import get_quantRatio


class Encoder():
    """
    A class that takes a 3D numpy image array and compresses the array

    parameters
    -------
    bits : int = 8
        The number of bits in each row and in each col of the MCU
    """

    bits = 8

    def __init__(self, array, quantRatio=50) -> None:
        """
        Instance variables for the Encoder class

        Attributes
        -----------
        array : ndarray
            A 3D numpy array of image array that will be encoded
        quantRatio : int
            The compression rate selected by the user
        width : int
            The width of the image
        height : int
            The height of the image
        paddedWidth : int
            The width after padding the array
        paddedHeight : int
            The height after padding the array
        """
        self.__array = array
        self.__quantRatio = quantRatio

        if (np.any(array) and isinstance(array, np.ndarray)
                and array.ndim >= 2):
            self.__width = array.shape[0]
            self.__height = array.shape[1]
        else:
            raise ValueError('Cannot determine array dimensions')

        self.__paddedWidth = 0
        self.__paddedHeight = 0


    @property
    def quantRatio(self):
        return self.__quantRatio

    @quantRatio.setter
    def quantRatio(self, value):
        if not isinstance(value, int):
            raise TypeError('quantRatio must be integer')
        if value < 1 or value > 95:
            raise ValueError('quantRatio must be between 1 and 95')
        self.__quantRatio = value

    @property
    def array(self):
        return self.__array

    @array.setter
    def array(self, value):
        if not np.all(np.isin(value.dtype, [np.float_, np.int_])):
            raise TypeError('array values not float or int')
        self.__array = value

    @property
    def width(self):
        return self.__width

    @property
    def height(self):
        return self.__height

    @property
    def paddedWidth(self):
        return self.__paddedWidth

    @property
    def paddedHeight(self):
        return self.__paddedHeight

    def padding(self, section=8):
        """
        A function that pads the array and ensures the width and height
        of the array are in multiples of 8

        Parameters
        ----------
        section : int
            The groupings of the image array to prime. Note that the
            default is 8 to ensure that the image is successfully
            quantized

        Returns
        ----------
        ndarray
            A 3D or 2D numpy array of image that is padded
        """

        # Get the padding dimensions
        self.__paddedWidth = ceil(self.__width / section) * section
        self.__paddedHeight = ceil(self.__height / section) * section

        # Ensure the array is padded or return the initial array
        try:
            new_array = pad_array(self.__array, self.__paddedWidth,
                                     self.__paddedHeight)
        except Exception as er:
            print (f'Padding Failed: {str(er.exception)}')
        else:
            self.__array = new_array

        return (self.__array)


    def RGB2YCrCb(self, default_mode='RBG'):
        """
        A function that converts image array from BRG color space to YCrCb

        Note
        ----
        BRG means Blue Red Green color space
        YCrCb means Y-luminance, CrCb-Chrominance (Chroma)
            Cr - Red Chroma
            Cb - Blue Chroma

        Formula
        -------

            # Getting the RGB Components
            $ array = np.array(image_array_from_pillow)
            $ R, B, G = array[:,:,0], array[:,:,1], array[:,:,2]

            # Converting to YCrCb
            $ Y = R * 0.299  +  G * 0.587  +  B * 0.114
            $ Cr = R * -0.1687  +  G * -0.3317  +  B * 0.5  +  128
            $ Cr = R * 0.5  +  G * -0.4187  +  B * -0.0813  +  128

        Return
        ------
        ndarray:
            A 3D numpy array of image array in YCrCb
        """

        # Get the YCrCb
        Y = self.__array[:, :, 0] * 0.299 + self.__array[:, :, 1] * 0.587 +\
            self.__array[:, :, 2] * 0.114
        Cr = self.__array[:, :, 0] * 0.5 + self.__array[:, :, 1] * -0.4187 +\
            self.__array[:, :, 2] * -0.0813 + 128
        Cb = self.__array[:, :, 0] * -0.1687 + self.__array[:, :, 1] * -0.3317 +\
            self.__array[:, :, 2] * 0.5 + 128

        # # Reversible Color Transform
        # Y = (self.__array[:, :, 0] + 2 * self.__array[:, :, 1] + self.__array[:, :, 2]) / 4
        # Cr = self.__array[:, :, 0] - self.__array[:, :, 1]
        # Cb = self.__array[:, :, 2] - self.__array[:, :, 1]

        # convert back to 3D numpy array and ensures values are within
        # the range of 0 and 255
        self.__array = np.clip(np.stack((Y, Cr, Cb), axis=-1), 0, 255)

        return (self.__array.astype(np.int64))

    def shift_level(self, array=None):
        """
        Convert the array array from unsigned to a signed representation

        Converting floating point to integer was for reduce cost of
        computation when handling float

        Parameters
        ----------
        array: ndarray
            numpy array 

        Note
        ----
        unsigned array: from 0 to 255
        signed representation: from -128 to 127

        Return
        ndarray:
            nd array signed array
        """

        if array is not None:
            return ((array - 128).astype(np.int64))

        self.__array = self.__array - 128
        return (self.__array.astype(np.int64))

    def DCT(self):
        """
        A function that tranforms the image array from spatial domain to frequency
        domain

        Formula
        -------
            # cosine_array - 8X8 cosine transfrom array (find in helpers.py)
            # cosine_array.T - the transpose
            # array - 8X8 section of the image
            # result - 8X8 section of the image that is dct transformed
            # * - matrix multiplication

            $ result = cosine_array * array * cosine_array.T
        """

        if (self.__paddedWidth == 0) or (self.__paddedHeight == 0):
            self.__paddedWidth = ceil(self.__width / 8) * 8
            self.__paddedHeight = ceil(self.__height / 8) * 8

        D = self.__array.ndim
        row_section = self.__paddedWidth // self.bits
        col_section = self.__paddedHeight // self.bits

        ar_copy = np.empty((self.__paddedWidth, self.__paddedHeight, D))

        for d in range(D):
            for row in range(row_section):
                r_start = row * self.bits
                r_end = r_start + self.bits
                for col in range(col_section):
                    c_start = col * self.bits
                    c_end = c_start + self.bits

                    mat_8 = self.__array[r_start:r_end, c_start:c_end, d]
                    ar = np.dot(np.dot(cosine_array, mat_8), (cosine_array.T))
                    ar_copy[r_start:r_end, c_start:c_end, d] = ar[:, :]

        self.__array = ar_copy
        return (ar_copy.astype(np.int64))


    def compression(self):
        """
        A function that compresses the image by applying dct transform
        and the quantization

        Return
        ------
        array: numpy 3D array
            the quantized numpy array
        """

        if (self.__paddedWidth == 0) or (self.__paddedHeight == 0):
            self.__paddedWidth = ceil(self.__width / 8) * 8
            self.__paddedHeight = ceil(self.__height / 8) * 8

        # Get the nd array dimensions
        D = self.__array.ndim

        # Divide the width and height into 8X8 sections
        row_section = self.__paddedWidth // self.bits
        col_section = self.__paddedHeight // self.bits

        # Get chrominance and luminance quantization ratio
        quant_luma, quant_chroma = get_quantRatio(self.__quantRatio)

        # Create a new array
        ar_copy = np.empty((self.__paddedWidth, self.__paddedHeight, D))

        for d in range(D):
            # Handle chrominance and luminance quantization
            # Note luminance is the array[:, : 0]
            if d > 0:
                quant_ratio = quant_chroma
            else:
                quant_ratio = quant_luma

            for row in range(row_section):
                r_start = row * self.bits
                r_end = r_start + self.bits
                for col in range(col_section):
                    c_start = col * self.bits
                    c_end = c_start + self.bits

                    mat_8 = self.__array[r_start:r_end, c_start:c_end, d]
                    ar = np.round(np.divide(mat_8, quant_ratio))

                    ar_copy[r_start:r_end, c_start:c_end, d] = ar
        self.__array = ar_copy
        # self.__array = np.round(self.__array, decimals=0)

        return (ar_copy.astype(np.int64))
