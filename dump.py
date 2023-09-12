#!/usr/bin/env python3
# import os

# # Specify the folder path you want to list files from
# folder_path = '/path/to/your/folder'

# # Use os.listdir() to get a list of all files and directories in the folder
# files_and_directories = os.listdir(folder_path)

# # Filter the list to include only files (not directories)
# files = [f for f in files_and_directories if os.path.isfile(os.path.join(folder_path, f))]

# # Now, the 'files' list contains the names of all files in the folder
# print("Files in the folder:")
# for file in files:
#     print(file)

from fileIO.image_io import get_path_array

args = "path=./jpeg/file.py quality=50"

print(get_path_array(args, 'file'))
