#!/usr/bin/env python3

from fileIO.compress import picture
from fileIO import storage
from fileIO.image_io import display
from fileIO.image_io import print_details
import cmd
import shlex


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

        USAGE: show image_id mode=[ "compressed" | "original" | "compare" ]
        USAGE: show mode=mode=[ "compressed" | "original" | "compare" ]
        USAGE: show image_id
        USAGE: show

        Arguments
        ---------
        image_id : [default=last_object]
            The id of the image that was compressed
        mode : [default=compressed]
            Must be a key-value pair that shows the image to
            display
            compressed:
                displays the compressed image of the given image_id
            compare:
                displays the compressed and original side by side
            original:
                displays the input image file of the image_id
        """
        # Set default values for mode and image_id
        mode = 'compressed'
        image_id = ''
        last_object = storage.last_object()
        if last_object:
            image_id = last_object.get('compressed_image_name')
        # if user input values
        if args:
            args_list = shlex.split(args)
            # Ensure only two input parameters
            if len(args_list) > 2:
                print("ERROR: More than two parameters")
                return
            # Loop through the parameter inputs
            one_arg = True
            for arg in args_list:
                # Use 'check' to ensure parameters are acceptable
                check = False
                value = arg.split('=')
                if len(value) == 1 and one_arg:
                    image_id = value[0]
                    check = True
                    one_arg = False
                elif value[0] == 'mode' and len(value) < 3:
                    mode = value[1]
                    check = True
                elif value[0] == 'image_id' and len(value) < 3:
                    image_id = value[1]
                    check = True
                # Return if the parameters are not valid
                if not check:
                    print("ERROR: wrong input")
                    return
        # Ensure image ID is present
        if (not image_id):
            print("ERROR: No image id")
            return
        # Ensure acceptable mode value
        if mode not in ['compressed', 'original', 'compare']:
            print("ERROR: mode not valie")
            return
        # Get the object and display
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
        # If no such object exist in the database
        if not image_obj:
            print('No image file found')

    def do_detail(self, args):
        """
        Displays a command line information about the
        compressed image file

        USAGE : detail image_id=["all" | "id"]
        USAGE : detail    (Note: defaults image_id to last_object)

        Parameters
        ----------
        image_id : [default=last_object]
            The id of the image that was compressed
            all :
                Shows the information for all the compressed files
            id :
                The exact image_id to show the detail
        """
        # Set default value for image_id
        image_id = ''
        if not args:
            last_object = storage.last_object()
            if last_object:
                image_id = last_object.get('compressed_image_name')
        if args:
            arg_list = shlex.split(args)
            if len(arg_list) > 1:
                print("ERROR: More than one input parameter")
            arg_list = arg_list[0].split('=')
            if len(arg_list) > 1:
                if arg_list[0] != 'image_id':
                    print("ERROR: Wrong Parameter")
                    return
                arg_list[0] = arg_list[1]
            image_id = arg_list[0]
        # Ensure image ID is present
        if (not image_id):
            print("ERROR: No image id")
            return
        obj = storage.objects
        if image_id == 'all':
            all_id = list(obj.keys())
            for idx in all_id:
                print_details(obj.get(idx))
                print('')
        else:
            image_dict = obj.get(image_id)
            if image_dict:
                print_details(image_dict)
            else:
                print("ERROR: No image found")

    def do_delete(self, args):
        """
        Deletes an image file data from the database with the
        option to remove the compressed image file

        USAGE : delete image_id=[all | id] remove=False
        USAGE : delete image_id=[all | id]
        USAGE : delete remove=False
        USAGE : delete

        Parameters
        ----------
        image_id : [default=last_object]
            The id of the image that was compressed
            all :
                Shows the information for all the compressed files
            id :
                The exact image_id to show the detail
        remove : [default=True]
            Option to either remove the compressed image or to leave
            it in the database
            True :
                Removes object data and the compressed image
            False :
                Removes only object data but leaves the compressed image
                in the database
        """
        # Set default values for mode and image_id
        remove = True
        image_id = ''
        last_object = storage.last_object()
        if last_object:
            image_id = last_object.get('compressed_image_name')
        elif args:
            arg_list = shlex.split(args)
            if len(arg_list) > 2:
                print("ERROR: more than two parameter used")
            one_arg = True
            for arg in arg_list:
                check = False
                value = args.split('=')
                if len(value) == 1 and one_arg:
                    image_id = value[0]
                    check = True
                    one_arg = False
                elif len(value) == 2 and value[0] == 'image_id':
                    image_id = value[1]
                elif len(value) == 2 and value[0] == 'remove':
                    remove = value[1]
                if check == False:
                    print("ERROR: Wrong parameters")
        if (isinstance(remove, str)) and remove.lower() == 'true':
            remove = True
        elif (isinstance(remove, str)) and remove.lower() == 'false':
            remove = False
        elif not (isinstance(remove, bool)):
            print("ERROR: remove must be either true or false")
            return
        if not image_id:
            print("ERROR: No image id found")
            return
        # print(image_id)
        # print(remove)
        storage.delete(image_id, remove)

if __name__ == '__main__':
    CompJPEG().cmdloop()
