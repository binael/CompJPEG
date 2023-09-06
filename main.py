#!/usr/bin/env python3

import numpy as np
from codec import Encoder
from codec import Decoder
from util_func import pad_array
from PIL import Image

filename = './jpeg_images/fruits.jpg'

img = Image.open(filename)

array_3d = np.array(img)

rat = 25

encode = Encoder(array_3d, rat)
# print(encode.array[:, :, 0].astype(np.int64))
encode.RGB2YCrCb()
encode.sampling()
encode.padding()
encode.compression()
print(encode.array[:, :, 0].astype(np.int64))

pW = encode.paddedWidth
pH = encode.paddedHeight
h = encode.height
w = encode.width
# print(encode.array[:, :, 0].astype(np.int64))
decode = Decoder(encode.array, w, h, pW, pH, rat)
# print(decode.array[:, :, 0])
decode.decompression()
decode.reverse_padding()
decode.reverse_sampling()
decode.YCrCb2BRG()


name = './jpeg_images/compressed.jpg'

image = Image.fromarray(decode.array.astype(np.uint8))
image.save(name)
