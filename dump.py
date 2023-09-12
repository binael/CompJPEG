#!/usr/bin/env python3
from fileIO.compress import picture
# from fileIO import storage
# from fileIO.image_io import display
# import cmd
# import shlex

filename = './jpeg_images/car-key.jpg'
ratio = 85
picture(filename, ratio)

filename = './jpeg_images/landscape.jpg'
ratio = 60
picture(filename, ratio)

filename = './jpeg_images/cockroach.jpg'
ratio = 70
picture(filename, ratio)

filename = './jpeg_images/grey_image.jpg'
ratio = 5
picture(filename, ratio)

filename = './jpeg_images/fruits.jpg'
ratio = 45
picture(filename, ratio)

filename = './jpeg_images/nature1.jpg'
ratio = 40
picture(filename, ratio)
