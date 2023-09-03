#!/usr/bin/env python3
from encoder import Encoder, get_dimension, picture_resolution
from encoder import np, ceil
from encoder import Image
from reverse import Reverse
from helpers import cosine_array, get_quantRatio
import numpy as np
from PIL import Image
import cv2

np.set_printoptions(suppress=True)

rat = 90

filename = 'nature2.jpg'
encode = Encoder(filename, rat)
encode.get_image_array()
# print(data[:, :, 1])

encode.padding()
encode.BRG2YCrCb()
encode.shift_level()
encode.DCT()
encode.quantization()
height = encode.height
width = encode.width
paddedHeight = encode.paddedHeight
paddedWidth = encode.paddedWidth


rev = Reverse(encode.data.round().astype(int), paddedHeight, paddedWidth, height, width, rat)
# # print(rev.array[:, :, 0])
rev.array
rev.de_quantization()
rev.IDCT()
rev.shift_level()
rev.YCrCb2BRG()
rev.reverse_padding()

print(rev.quantRatio)


# Read the YCrCb image
rgb_image = cv2.imread(filename)
ycrcb_image = cv2.cvtColor(rgb_image, cv2.COLOR_BGR2YCrCb)
Y, Cr, Cb = cv2.split(ycrcb_image)
dct_Y = cv2.dct(np.float32(Y))
dct_Cr = cv2.dct(np.float32(Cr))
dct_Cb = cv2.dct(np.float32(Cb))
idct_Y = cv2.idct(dct_Y)
idct_Cr = cv2.idct(dct_Cr)
idct_Cb = cv2.idct(dct_Cb)
idct_Y_image = cv2.normalize(idct_Y, None, alpha=0, beta=255, norm_type=cv2.NORM_MINMAX, dtype=cv2.CV_8U)
idct_Cr_image = cv2.normalize(idct_Cr, None, alpha=0, beta=255, norm_type=cv2.NORM_MINMAX, dtype=cv2.CV_8U)
idct_Cb_image = cv2.normalize(idct_Cb, None, alpha=0, beta=255, norm_type=cv2.NORM_MINMAX, dtype=cv2.CV_8U)
idct_ycrcb_image = cv2.merge((idct_Y_image, idct_Cr_image, idct_Cb_image))

rgb = cv2.cvtColor(idct_ycrcb_image, cv2.COLOR_YCrCb2BGR)

R, G, B = cv2.split(rgb_image)
R = np.array(R)


# img = Image.open(filename)
# image = img.convert('YCbCr')
# ar = np.array(image)


# print(np.array(img)[:, :, 0])
# print()
# print(rev.array[0:10, 0:10, 0].astype(np.int64))
# print()
# print(R)


# name = 'compressed.jpg'
# ar = rev.array
# image = Image.fromarray(ar.astype(np.uint8))
# image.save(name)
