#!/usr/bin/env python3

"""
Module that stores objects in a json file and retrieves
objects in the json file
"""

# Python module
import json
import os

from fileIO.im_details import Details


class FileStorage:
    """
    A class that stores the details of all the compressed image
    in a json file and also retrieve details from the
    compressed file
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
                obj = json.load(jfile)
            for key in obj:
                details = Details(**obj[key])
                self.__objects[key] = details.__dict__
        except:
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

    def delete(self, obj) -> None:
        """
        Deletes a detail from the json file

        Parameters
        ----------
        obj : str
            The dict key to delete
        """
        if obj in self.__objects:
            full_path = self.__objects[obj][out_fullpath]
            del self.__objects[obj]
            self.__lastObject = self.last_object()
            self.__save()
            if os.path.exists(full_path):
                os.remove(full_path)
