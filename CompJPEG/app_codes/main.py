#!/usr/bin/env python3
from encoder import Encoder, get_dimension, picture_resolution
from encoder import np, ceil
from encoder import Image

np.set_printoptions(suppress=True)

filename = 'example_small.jpg'
encode = Encoder(filename)
data = encode.get_image_array()

# im = Image.open(filename)
# print(im.size)
data2 = encode.padding()
data3 = encode.BRG2YCrCb()
# data4 = encode.shift_level()
data5 = encode.DCT()
q = encode.quantization(90)
# height = encode.height
# width = encode.width
# paddedHeight = encode.paddedHeight
# paddedWidth = encode.paddedWidth

print(q)

# print(data[:,:,0])
# print(data[:,:,1])
# print(data[:,:,2])

# print(padded[:,:,1])
# print(padded[:,:,2])

# print(f'data after opening image: {data.shape}')
# print(f'data after padding {data2.shape}')
# print('')

# print(f'After padding for real dimension: {height} X {width}')
# print(f'After padding for padded dimension: {paddedHeight} X {paddedWidth}')

# print(data2[:,:,0])

# print(data3[:,:,0])
# print(data3[:,:,1])
# print(data3[:,:,2])

# print(data4[:,:,2])

# print(data5[:,:,0])
# print(data5[:,:,1])
# print(data5[:,:,2])

# print(padded[:,:,1])
# print(padded[:,:,2])

# h, w = get_dimension(filename)
# print(picture_resolution(filename))

# print(f'height: {h}')
# print(f'width: {w}')
# print(f'Height: {ceil(h / 8) * 8}')
# print(f'Width: {ceil(h / 8) * 8}')
