#!/usr/bin/env python3

from tests import variables as var
from fileIO.compress import picture
from fileIO import storage
from fileIO.image_io import display


last = storage.last_object()

print('')
name1 = last['out_fullpath']
name2 = './jpeg_images/fruits.jpg'

display(name1)
