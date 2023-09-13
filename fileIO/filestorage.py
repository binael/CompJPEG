#!/usr/bin/env python3

"""
Module that stores objects in a json file and retrieves
objects in the json file
"""

# Python module
import json
import os
import shutil

# Modules (functions) from fileIO package
# from fileIO.im_details import Details


class FileStorage:
    """
    A class that stores the details of all the compressed image
    in a json file and also retrieve details from the
    compressed file

    Methods
    -------
    save :
        serializes objects to json
    last_object :
        returns the last compressed object dictionary
    reload :
        de-serializes json to object
    new :
        updates new update
    delete :
        deletes an object and its corresponding compressed
        files
    """

    # json file name to save image details
    __jfile = 'image_details.json'
    # dictionary list of all objects
    __objects = {}
    # Last object name
    __lastObject = None

    @property
    def objects(self):
        return self.__objects

    def save(self) -> None:
        """
        A function to save the __objects to json file
        """
        if self.__objects:
            with open(self.__jfile, 'w') as jfile:
                json.dump(self.__objects, jfile)

    def last_object(self) -> dict:
        """
        get the details of the compressed object
        """
        if not self.__objects:
            return None

        if not self.__lastObject:
            obj_list = list(self.__objects.keys())
            self.__lastObject = obj_list[-1]
        return (self.__objects[self.__lastObject])

    def reload(self) -> None:
        """
        Deserializes a json file to self.__objects
        """
        try:
            with open(self.__jfile, mode='r') as jfile:
                self.__objects = json.load(jfile)
            # for key in obj:
            #     details = Details(**obj[key])
            #     self.__objects[key] = details.__dict__
        except Exception:
            pass

    def new(self, obj) -> None:
        """
        Function that adds a new compressed file detail to objects
        dictionary

        Parameters
        ----------
        obj : dict
            new dictionary to be added
        """
        if obj:
            self.__lastObject = obj['compressed_image_name']
            self.__objects[self.__lastObject] = obj

    def delete(self, obj, remove=True) -> None:
        """
        Deletes object information from the database with
        the option to delete the compressed image file or folder
        the option to delete the compressed image file or folder

        Parameters
        ----------
        obj : str
            The dict key to delete
        remove : bool
            Option to remove only image data object or to remove
            both the object and the compressed file
        """
        # Remove a specific object
        if obj in self.__objects:
            full_path = self.__objects[obj].get('out_fullpath')
            del self.__objects[obj]
            self.__lastObject = None
            self.save()
            print(f"Successfully deleted object with id: {obj}")
            if remove and full_path and os.path.exists(full_path):
                try:
                    os.remove(full_path)
                except Exception:
                    print("ERROR: Image removal failed")
        # Remove all objects
        elif obj == 'all':
            last_object = self.last_object()
            if not last_object:
                return
            full_path = last_object.get('out_fullpath')
            self.__objects = {}
            print(f"All objects have been deleted")
            if os.path.exists(self.__jfile):
                try:
                    os.remove(self.__jfile)
                except Exception:
                    print("ERROR: json file removal failed")
            if remove and full_path and os.path.exists(full_path):
                try:
                    dirname, _ = os.path.split(full_path)
                    shutil.rmtree(dirname)
                except Exception:
                    print("ERROR: Directory removal failed")
        else:
            print("ERROR: No object found")
