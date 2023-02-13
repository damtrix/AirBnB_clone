#!/usr/bin/python3
"""Serializing and deserialising instance of JSON file and vis-a-vis"""
import json
import datetime
import os


class FileStorage:
    """Serializing and deserializing of instance to JSON file and vis-a-vis"""
    __file_path = "file.json"
    __objects = {}

    def classes(self):
        """Returns the dictionary of a valid class"""
        from models.base_model import BaseModel
        from models.user import User
        from models.city import City
        from models.amenity import Amenity
        from models.place import Place
        from models.review import Review
        from models.state import State

        classes = {
            "BaseModel": BaseModel,
            "User": User,
            "City": City,
            "Amenity": Amenity,
            "Place": Place,
            "Review": Review,
            "State": State
        }

        return classes

    def all(self):
        """Returns the dictionary __objects"""
        return FileStorage.__objects

    def new(self, obj):
        """Sets in __objects the obj with key <obj class name>.id"""
        key = "{}.{}".format(type(obj).__name__, obj.id)
        FileStorage.__objects[key] = obj

    def save(self):
        """Serializes __objects to the JSON file (path: __file_path)"""
        with open(FileStorage.__file_path, "w", encoding="utf-8") as myFile:
            data = {key: value.to_dict()
                    for key, value in FileStorage.__objects.items()}
            json.dump(data, myFile)

    def reload(self):
        """
        Deserializes the JSON file to __objects
        (only if the JSON file (__file_path) exists;
        otherwise, do nothing. If the file doesn’t
        exist, no exception should be raised)
        """
        if not os.path.isfile(FileStorage.__file_path):
            return

        with open(FileStorage.__file_path, "r", encoding="utf-8") as myFile:
            data = json.load(myFile)
            data = {k: self.classes()[v["__class__"]](**v)
                    for k, v in data.items()}
            FileStorage.__objects = data

    def attributes(self):
        """Returns the valid attributes and their types for classname"""
        attributes = {
            "BaseModel":
                     {"id": str,
                      "created_at": datetime.datetime,
                      "updated_at": datetime.datetime},
            "User":
                     {"email": str,
                      "password": str,
                      "first_name": str,
                      "last_name": str},
            "State":
                     {"name": str},
            "City":
                     {"state_id": str,
                      "name": str},
            "Amenity":
                     {"name": str},
            "Place":
                     {"city_id": str,
                      "user_id": str,
                      "name": str,
                      "description": str,
                      "number_rooms": int,
                      "number_bathrooms": int,
                      "max_guest": int,
                      "price_by_night": int,
                      "latitude": float,
                      "longitude": float,
                      "amenity_ids": list},
            "Review":
            {"place_id": str,
                         "user_id": str,
                         "text": str}
        }
        return attributes
