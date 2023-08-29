#!/usr/bin/env python3
"""
A module that passes jpeg raster data through various stages of
jpeg encoding to ultimately compress the image

Raster data are the actual data in jpeg that will be encoded
Raster data are ususally represented with a 3D array to show
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
        Image data are usually processed in 8x8 MCUs (minimum coded units)
        and so, both the height and width (dimensions) of the images
        must be in multiples of 8. Any value can be chosen in extending your
        image rows and columns to match the multiples of 8
    Sub Sampling:
        This was not implemented in the project
    YCrCb Conversion:
        This involves transforming the image data from RGB to
        Y(luminance) and Cr, Cb (chrominance values). This method is
        skipped if the image mode is already in YCrCb mode
    Level Shifting:
        Image data are transformed from 8bit unsigned to 8bit signed
        representation by subtraction "128" from each data value
        mat[i][j] - 128
    DCT Transform:
        DCT Transform is then applied to the image to transform to frequency
        domain
    Quantization:
        This is the stage that the actual compression takes place
        A quantization table with the specified compression ratio is
        applied to the image data to compress the data

"""

from helpers import Image, np, ceil
from helpers import picture_resolution, get_dimension, pad_array
from helpers import dct_array, Quantization50


class Encoder():
    """
    A class that takes a 3D numpy image array and compresses the data

    parameters
    -------
    bits : int = 8
        The number of bits in each row and in each col of the MCU
    """

    bits = 8

    def __init__(self, image, quality=50) -> None:
        """
        Instance variables for the Encoder class

        Attributes
        -----------
        image : str
            The file path of the image to compress
        data : numpy array (3D)
            A 3D numpy array of image data that will be encoded
        quality : int
            The compression rate selected by the user
        height : int
            The height of the image
        width : int
            The width of the image
        paddedHeight : int
            The height after padding the data
        paddedWidth : int
            The width after padding the data
        """
        self.__data = []
        self.__quality = quality
        self.__image = image
        self.__height = 0
        self.__width = 0
        self.__paddedHeight = 0
        self.__paddedWidth = 0

    @property
    def height(self):
        return self.__height

    @property
    def width(self):
        return self.__width

    @property
    def paddedHeight(self):
        return self.__paddedHeight

    @property
    def paddedWidth(self):
        return self.__paddedWidth

    def get_image_array(self):
        """
        Get the image arrays
        """
        img = Image.open(self.__image)
        matrix = np.array(img)

        if not self.__data:
            self.__data = matrix

        return (matrix)

    def padding(self):
        """
        A function that pads the array and ensures the height and width
        of the array are in multiples of 8

        Returns
        ----------
        np.array
            A 3D numpy array of image data that is padded
        """

        if (self.__height > 0 and self.__height == self.__paddedHeight):
            if (self.width > 0 and self.__width == self.__paddedWidth):
                return (self.__data)

        self.__width, self.__height = get_dimension(self.__image)

        # Get the padding dimensions
        self.__paddedHeight = ceil(self.__height / 8) * 8
        self.__paddedWidth = ceil(self.__width / 8) * 8

        if (self.__paddedHeight == self.__height and
                self.__paddedWidth == self.__width):
            return (self.data)

        # Ensure the dimension is in multiples of 8X8
        self.__data = pad_array(self.__data, self.__height, self.__width,
                                self.__paddedHeight, self.__paddedWidth)

        return (self.__data)

    def BRG2YCrCb(self, default_mode='RBG'):
        """
        A function that converts image data from BRG color space to YCrCb

        Note
        ----
        BRG means Blue Red Green color space
        YCrCb means Y-luminance, CrCb-Chrominance (Chroma)
            Cr - Red Chroma
            Cb - Blue Chroma

        Formula
        -------

            # Getting the RGB Components
            $ array = np.array(image_data_from_pillow)
            $ R, B, G = array[:,:,0], array[:,:,1], array[:,:,2]

            # Converting to YCrCb
            $ Y = R * 0.299  +  G * 0.587  +  B * 0.114
            $ Cr = R * -0.1687  +  G * -0.3317  +  B * 0.5  +  128
            $ Cr = R * 0.5  +  G * -0.4187  +  B * -0.0813  +  128

        Return
        ------
        np.array:
            A 3D numpy array of image data in YCrCb
        """

        # Update the image data
        if not (self.__height and self.__width):
            print('Executing padding')
            self.padding()

        # if default_mode != 'RGB':
        #     return self.__data

        # Get the YCrCb
        Y = self.__data[:, :, 0] * 0.299 + self.__data[:, :, 1] * 0.587 +\
            self.__data[:, :, 2] * 0.114
        Cr = self.__data[:, :, 0] * -0.1687 + self.__data[:, :, 1] * -0.3317 +\
            self.__data[:, :, 2] * 0.5 + 128
        Cb = self.__data[:, :, 0] * 0.5 + self.__data[:, :, 1] * -0.4187 +\
            self.__data[:, :, 2] * -0.0813 + 128

        # convert back to 3D numpy array
        self.__data = np.stack((Y, Cr, Cb), axis=-1)

        return (self.__data)

    def shift_level(self):
        """
        Convert the array data from unsigned to a signed representation

        Converting floating point to integer was for reduce cost of
        computation when handling float

        Note
        ----
        unsigned data: from 0 to 255
        signed representation: from -128 to 127

        Return
        """

        # self.__data = self.__data.astype(np.int64)
        self.__data = self.__data - 128

        return (self.__data)

    def DCT(self):
        """
        """

        self.shift_level()
        D = 3
        row_section = self.__paddedHeight // self.bits
        col_section = self.__paddedWidth // self.bits

        for d in range(D):
            for row in range(row_section):
                r_start = row * self.bits
                r_end = r_start + self.bits
                for col in range(col_section):
                    c_start = col * self.bits
                    c_end = c_start + self.bits

                    mat_8 = self.__data[:, :, d][r_start:r_end, c_start:c_end]
                    ar = np.dot(np.dot(dct_array, mat_8), dct_array.T)

                    self.__data[:, :, d][r_start:r_end, c_start:c_end] = ar
                    # self.__data = self.__data.astype(np.int64)
                    self.__data = np.round(self.__data, decimals=1)

        return (self.__data)


    def quantization(self, quality=50):
        """
        """

        ratio = (100 - quality) / 50
        user_quant = Quantization50 * ratio
        user_quant = user_quant.astype(np.int64)

        D = 3
        row_section = self.__paddedHeight // self.bits
        col_section = self.__paddedWidth // self.bits

        for d in range(D):
            for row in range(row_section):
                r_start = row * self.bits
                r_end = r_start + self.bits
                for col in range(col_section):
                    c_start = col * self.bits
                    c_end = c_start + self.bits

                    mat_8 = self.__data[:, :, d][r_start:r_end, c_start:c_end]
                    ar = np.multipy(mat_8, user_quant)

                    self.__data[:, :, d][r_start:r_end, c_start:c_end] = ar
                    # self.__data = self.__data.astype(np.int64)
                    self.__data = np.round(self.__data, decimals=1)
        

        return (self.__data)
