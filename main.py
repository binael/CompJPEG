#!/usr/bin/env python3

from fileIO.compress import picture
from fileIO import storage
from fileIO.image_io import display
import cmd
import shlex

SHOW_TEXT = 'Usage: show image_id mode=[ "compressed" | "original" | "compare" ]'

class CompJPEG(cmd.Cmd):
    """
    Command Line process for image compression
    """
    prompt = '(CompJPEG) '

    def do_EOF(self, args):
        """Quits or Exits the program"""
        return True

    def do_quit(self, args):
        """Quits or Exits the program"""
        return True

    def do_show(self, args):
        """
        Pulls out a window showing the image file requested
        by the user

        Usage: show image_id mode=[ "compressed" | "original" | "compare" ]

        Arguments
        ---------
        mode : [ "compressed" | "original" | "compare" ]
            Must be a key-value pair that shows the image to
            display
            compressed: default value
                displays the compressed image of the given image_id
            compare:
                displays the compressed and original side by side
            original:
                displays the input image file of the image_id
        image_id : [default="last_object"]
            The input image id. This is a varible input mode
            that default to the last object

        Example
        -------
            $ Usage 1: show image_id mode="compare"
            $ Usage 2: show
            $ Usage 3: show image_id
        """
        # Set default values for mode and image_id
        mode = 'compressed'
        last_object = storage.last_object()
        if not last_object:
            print('No image file found')
            return
        image_id = last_object.get('compressed_image_name')
        # if user input values
        if args:
            args_list = shlex.split(args)
            if len(args_list) > 2:
                print(SHOW_TEXT)
                return
            for arg in args_list:
                value = arg.split('=')
                if len(value) == 1:
                    image_id = value[0]
                elif value[0] == 'mode' and len(value) < 3:
                    mode = value[1]
                elif value[0] == 'image_id' and len(value) < 3:
                    image_id = value[1]
        if (not image_id) and mode not in \
                ['compressed', 'original', 'compare']:
            print(SHOW_TEXT)
            return
        obj = storage.objects
        if obj:
            image_obj = obj.get(image_id)
            if image_obj and mode == 'compressed':
                name2 = image_obj.get('out_fullpath')
                display(name2)
            if image_obj and mode == 'original':
                name1 = image_obj.get('in_image_name')
                display(name1)
            if image_obj and mode == 'compare':
                name1 = image_obj.get('in_image_name')
                name2 = image_obj.get('out_fullpath')
                display(name1, name2)
        if not image_obj:
            print('No image file found')


if __name__ == '__main__':
    CompJPEG().cmdloop()
