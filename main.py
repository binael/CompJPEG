#!/usr/bin/env python3

from tests import variables as var
from fileIO.compress import picture
from fileIO import storage

# filename = './jpeg_images/fruits.jpg'
# quality = 80
# pix = picture(filename, quality)
# print(f'{pix}\n')

# filename = './jpeg_images/nature1.jpg'
# quality = 55
# pix = picture(filename, quality)
# print(f'{pix}\n')

# filename = './jpeg_images/cockroach.jpg'
# quality = 98
# pix = picture(filename, quality)
# print(f'{pix}\n')

# filename = './jpeg_images/blur-stain.jpg'
# quality = 25
# pix = picture(filename, quality)
# print(f'{pix}\n')

print(storage.last_object())
print('')

filename = './jpeg_images/car-key.jpg'
quality = 55
pix = picture(filename, quality)
print(f'{pix}\n')

filename = './jpeg_images/landscape.jpg'
quality = 35
pix = picture(filename, quality)
print(f'{pix}\n')
