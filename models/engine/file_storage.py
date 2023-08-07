#!/usr/bin/python3
"""It's Defines the FileStorage class."""
import json
from models.base_model import BaseModel
from models.user import User
from models.state import State
from models.city import City
from models.place import Place
from models.amenity import Amenity
from models.review import Review


class FileStorage:
    """It's Represent an abstracted storage engine.

    Attributes:
        __file_path (str): It's The name of the file to save objects to.
        __objects (dict): It's A dictionary of instantiated objects.
    """
    __file_path = "file.json"
    __objects = {}

    def all(self):
        """It's Return the dictionary __objects."""
        return FileStorage.__objects

    def new(self, obj):
        """It's Set in __objects obj with key <obj_class_name>.id"""
        ocn = obj.__class__.__name__
        FileStorage.__objects["{}.{}".format(ocn, obj.id)] = obj

    def save(self):
        """It's Serialize __objects to the JSON file __file_path."""
        odt = FileStorage.__objects
        objt = {obj: odt[obj].to_dict() for obj in odt.keys()}
        with open(FileStorage.__file_path, "w") as f:
            json.dump(objt, f)

    def reload(self):
        """Deserialize for JSON file __file_path to __objects, if it exists."""
        try:
            with open(FileStorage.__file_path) as f:
                objt = json.load(f)
                for u in objt.values():
                    cls_name = u["__class__"]
                    del u["__class__"]
                    self.new(eval(cls_name)(**u))
        except FileNotFoundError:
            return
