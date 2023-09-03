#!/usr/bin/env python3

from encoder import Encoder
from helpers import Image, np, ceil
from helpers import picture_resolution, get_dimension, pad_array
from helpers import cosine_array, get_quantRatio


class Reverse:
    """
    """

    bits = 8

    def __init__(self, array, paddedHeight, paddedWidth, height, width, quantRatio=50):
        self.__array = array
        self.__quantRatio = get_quantRatio(quantRatio)
        self.__paddedHeight = paddedHeight
        self.__paddedWidth = paddedWidth
        self.__height = height
        self.__width = width

    @property
    def array(self):
        return self.__array

    @property
    def quantRatio(self):
        return self.__quantRatio

    def de_quantization(self):
        """
        """
        D = 3
        row_section = self.__paddedHeight // self.bits
        col_section = self.__paddedWidth // self.bits

        ar_copy = np.empty((self.__paddedHeight, self.__paddedWidth, D))

        for d in range(3):
            for row in range(row_section):
                r_start = row * self.bits
                r_end = r_start + self.bits
                for col in range(col_section):
                    c_start = col * self.bits
                    c_end = c_start + self.bits

                    mat_8 = self.__array[r_start:r_end, c_start:c_end, d]
                    ar = np.multiply(mat_8, self.__quantRatio)

                    ar_copy[r_start:r_end, c_start:c_end, d] = ar
        self.__array = ar_copy
        # self.__array = np.round(self.__array, decimals=0)

        return (ar_copy.astype(np.int64))


    def IDCT(self):
        """
        A function that transforms the image from the frequency domain to the 
        spatial domain

        Note
        ----
        This reverses the dct transform

        Formula
        -------
            # cosine_array - 8X8 cosine transfrom array (find in helpers.py)
            # cosine_array.T - the transpose
            # array - 8X8 section of the image
            # result - 8X8 section of the image that is dct transformed
            # * - matrix multiplication

            $ result = cosine_array.T * array * cosine_array
        """

        D = 3
        row_section = self.__paddedHeight // self.bits
        col_section = self.__paddedWidth // self.bits

        ar_copy = np.empty((self.__paddedHeight, self.__paddedWidth, D))

        for d in range(D):
            for row in range(row_section):
                r_start = row * self.bits
                r_end = r_start + self.bits
                for col in range(col_section):
                    c_start = col * self.bits
                    c_end = c_start + self.bits

                    mat_8 = self.__array[r_start:r_end, c_start:c_end, d]
                    ar = np.dot(np.dot(cosine_array.T, mat_8), cosine_array)
                    ar_copy[r_start:r_end, c_start:c_end, d] = ar[:, :]

        self.__array = ar_copy
        return (ar_copy.astype(np.int64))


    def reverse_padding(self):
        """
        """
        Y = self.__array[0:self.__height, 0:self.__width, 0]
        Cr = self.__array[0:self.__height, 0:self.__width, 1]
        Cb = self.__array[0:self.__height, 0:self.__width, 2]

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

        # # Reversible Color Transform
        # G = Y - ((Cb - Cr) / 4)
        # R = Cr - G
        # B = Cb - G

        self.__array = np.stack((R, G, B), axis=-1)


    def shift_level(self):
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
