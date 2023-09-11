#!/usr/bin/env python3

from tests import variables as var
from fileIO import picture
from fileIO import FileStorage

filename = './jpeg_images/fruits.jpg'
quality = 80
pix = picture(filename, quality)
print(f'{pix}\n')

filename = './jpeg_images/nature1.jpg'
quality = 55
pix = picture(filename, quality)
print(f'{pix}\n')

filename = './jpeg_images/cockroach.jpg'
quality = 98
pix = picture(filename, quality)
print(f'{pix}\n')

filename = './jpeg_images/blur-stain.jpg'
quality = 25
pix = picture(filename, quality)
print(f'{pix}\n')

filename = './jpeg_images/grey_image.jpg'
quality = 45
pix = picture(filename, quality)
print(f'{pix}\n')

print(FileStorage.objects)

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
