#!/usr/bin/env python3

# from tests import variables as var
# from fileIO import picture
# from PIL import Image
# import numpy as np

# filename = './jpeg_images/dental-implants.jpg'
# quality = 5


# pix = picture(filename, quality)


# print(pix)

import numpy as np

a = np.array(42)
b = np.array([1, 2, 3, 4, 5])
c = np.array([[1, 2, 3], [4, 5, 6]])
d = np.zeros((3, 4, 3))

print(a.ndim)
print(b.ndim)
print(c.ndim)
print(d.shape)
print(d)
