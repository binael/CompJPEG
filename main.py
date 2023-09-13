#!/usr/bin/env python3

# Python modules
import cmd
import shlex

# Modules (functions) from fileIO package
from fileIO import storage
from fileIO.compress import picture
from fileIO.image_io import display
from fileIO.image_io import print_details
from fileIO.image_io import get_path_array


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

        USAGE: show id=image_id mode=[ compressed | original | compare ]
        USAGE: show mode=[ compressed | original | compare ]
        USAGE: show id=image_id
        USAGE: show

        Arguments
        ---------
        id : [default=last_object]
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
        # Set default values for mode and id
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
                print(f"ERROR: Wrong number of input arguments\n{args}")
                return
            # Loop through the parameter inputs
            for arg in args_list:
                # Use 'check' to ensure parameters are acceptable
                check = False
                value = arg.split('=')
                if value[0] == 'mode' and len(value) > 1:
                    mode = value[1]
                    check = True
                elif value[0] == 'id' and len(value) > 1:
                    image_id = value[1]
                    check = True
                # Return if the parameters are not valid
                if not check:
                    print(f"ERROR: Wrong key-value pair:\t{arg}")
                    return
        # Ensure image ID is present
        if (not image_id):
            print("ERROR: No image id found")
            return
        # Ensure acceptable mode value
        if mode not in ['compressed', 'original', 'compare']:
            print("ERROR: mode not valid")
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
            print(f'ERROR: Could not found object with id:\t{image_id}')

    def do_detail(self, args):
        """
        Displays a command line information about the
        compressed image file

        USAGE : detail id=[ all | image_id ]
        USAGE : detail    (Note: defaults id to last_object)

        Parameters
        ----------
        id : [default=last_object]
            The id of the image that was compressed
            all :
                Shows the information for all the compressed files
            image_id :
                The exact image_id to show the detail
        """
        # Set default value for image_id
        image_id = ''
        if not args:
            last_object = storage.last_object()
            if last_object:
                image_id = last_object.get('compressed_image_name')
        elif args:
            arg_list = shlex.split(args)
            if len(arg_list) > 1:
                print(f"ERROR: Wrong number of input arguments:\t{args}")
            arg_list = arg_list[0].split('=')
            if len(arg_list) > 1:
                if arg_list[0] != 'id':
                    print(f"ERROR: Wrong key-value pair:\t{arg_list}")
                    return
                image_id = arg_list[1]
        # Ensure image ID is present
        if (not image_id):
            print("ERROR: No image id found")
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
                print('')
            else:
                print(f'ERROR: Could not found object with id:\t{image_id}')

    def do_delete(self, args):
        """
        Deletes an image file data from the database with the
        option to remove the compressed image file

        USAGE : delete id=[ all | image_id ] remove=False
        USAGE : delete id=[ all | image_id ]
        USAGE : delete remove=False
        USAGE : delete

        Parameters
        ----------
        id : [default=last_object]
            The id of the image that was compressed
            all :
                Shows the information for all the compressed files
            image_id :
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
        if args:
            arg_list = shlex.split(args)
            if len(arg_list) > 2:
                print(f"ERROR: Wrong number of input arguments:\t{args}")
            one_arg = True
            for arg in arg_list:
                check = False
                value = arg.split('=')
                if len(value) > 1 and value[0] == 'id':
                    image_id = value[1]
                    check = True
                elif len(value) > 1 and value[0] == 'remove':
                    remove = value[1]
                    check = True
                if check == False:
                    print(f"ERROR: Wrong key-value pair:\t{arg}")
                    return
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
        storage.delete(image_id, remove)

    def do_compressFiles(self, args):
        """
        Version of compress image that requires directory, text or
        json files as sources of input

        USAGE: compressFiles type=[ json | text | directory] path=pathname

        Parameters
        ----------
        type :
            The type of file to source the image details or the directory
            where the images can be found. Note that sub-directories will not
            be considered
        pathname :
            The pathname for the directory or file
        """
        if not args:
            print('ERROR: No input arguments')
            return
        arg_list = shlex.split(args)
        if len(arg_list) != 2:
            print(f"ERROR: Wrong number of input arguments:\t{args}")
            return
        file_path = file_type = ''
        for arg in arg_list:
            value = arg.split('=')
            check = False
            if len(value) > 1 and value[0] == 'type':
                file_type = value[1]
                check = True
            elif len(value) > 1 and value[0] == 'path':
                file_path = value[1]
                check = True
            if check == False:
                print(f"ERROR: Wrong key-value pair:\t{arg}")
                return
        if not (file_path and file_type):
            print("ERROR: path and type must be valid inputs")
            return
        if file_type.lower() not in ['json', 'text', 'directory']:
            print("ERROR: Wrong file type")
            return
        im_ar = get_path_array(file_path, file_type)
        if im_ar:
            for pathname, quality in im_ar:
                try:
                    picture(pathname, quality)
                except Exception as er:
                    print(f"ERROR: compression of {pathname} failed")
                    try:
                        e = er.exception
                    except:
                        print(str(er))
                    else:
                        print(str(e))


    def do_compress(self, args):
        """
        Compresses image file(s) to the desired ratio

        USAGE: compress "path=pathname1 quality=40" "path=pathname2 quality=50" ...

        Parameters
        ----------
        path :
            The pathname of the image file
        quality :
            The compression ratio
        """
        if not args:
            print('ERROR: No input files')
            return
        im_ar = get_path_array(args, file_type='file')
        print(im_ar)
        if im_ar:
            for pathname, quality in im_ar:
                try:
                    picture(pathname, quality)
                except Exception as er:
                    print(f"ERROR: compression of {pathname} failed")
                    try:
                        e = er.exception
                    except:
                        print(str(er))
                    else:
                        print(str(e))


if __name__ == '__main__':
    CompJPEG().cmdloop()
