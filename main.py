#!/usr/bin/env python3

from tests import variables as var
from fileIO import picture
from PIL import Image
import numpy as np

filename = './jpeg_images/dental-implants.jpg'
quality = 5


pix = picture(filename, quality)


print(pix)
