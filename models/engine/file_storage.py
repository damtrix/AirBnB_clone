#!/usr/bin/python3
"""Serializing and deserialising instance of JSON file and vis-a-vis"""
import json
from datetime import datetime
import os

class FileStorage:
    """Serializing and deserializing of instance to JSON file and vis-a-vis"""
    __file_path = "file.json"
    __objects = {}

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
            data = {key: value.to_dict() for key, value in FileStorage.__objects.items()}
            json.dump(data, myFile)

    def reload(self):
        """
        Deserializes the JSON file to __objects (only if the JSON file (__file_path) exists;
        otherwise, do nothing. If the file doesn’t exist, no exception should be raised)
        """
        if not os.path.isfile(FileStorage.__file_path):
            return

        with open(FileStorage.__file_path, "r", encoding="utf-8") as myFile:
            data = json.loads(myFile)
            from models.base_model import BaseModel
            for key, value in data.items():
                if value['__class__'] == "BaseModel":
                    FileStorage.__objects[key] = BaseModel(**value)