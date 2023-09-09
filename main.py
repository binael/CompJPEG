#!/usr/bin/env python3

from tests import variables as var
from fileIO import picture
import json

filename = './jpeg_images/blur-stain.jpg'
quality = 5


pix = picture(filename, quality)


print(json.dumps(pix))

# img = Image.open(filename)
# ar = np.array(img)

# encode = Encoder(ar, quality)
# encode.RGB2YCrCb()
# encode.sampling()
# encode.padding()
# encode.compression()

# decode = Decoder(encode.Y, encode.Cr, encode.Cb, encode.width,
#                  encode.height, encode.paddedWidth, encode.paddedHeight,
#                  quality)

# decode.decompression()
# decode.reverse_padding()
# decode.reverse_sampling()
# decode.YCrCb2RGB()

# image = Image.fromarray(decode.array.astype(np.uint8))
# image.save('compressed.jpg')
