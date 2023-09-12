#!/usr/bin/env python3
# def is_text_file(file_path, block_size=512):
#     try:
#         with open(file_path, 'rb') as file:
#             block = file.read(block_size)
#             while block:
#                 # Check if the block contains any non-printable or non-ASCII characters
#                 if any(byte < 32 or byte > 126 and byte != 10 and byte != 13 for byte in block):
#                     return False
#                 block = file.read(block_size)
#     except Exception as e:
#         # Handle any exceptions that may occur (e.g., file not found)
#         return False
#     return True


from fileIO.image_io import get_path_array
from fileIO.image_io import text_array
import json

# args = "path=./jpeg/file.py quality=50"
# print(get_path_array(args, 'file'))

# args = './example/example_json.json'
# a = json_array(args)
# print(get_path_array(args, 'json'))


# args = './jpeg_images'
# a = dir_array(args)
# print(a)
# print(get_path_array(args, 'directory'))

args = './example/example_text.txt'
# a = text_array(args)
# print(a)
print(get_path_array(args, 'text'))
