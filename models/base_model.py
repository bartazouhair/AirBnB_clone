#!/usr/bin/python3
"""Defines the BaseModel class."""
import models
from uuid import uuid4
from datetime import datetime


class BaseModel:
    """It's Represents the BaseModel of the HBnB project."""

    def __init__(self, *args, **kwargs):
        """It's a Initialize a new BaseModel.

        Args:
            *args (any): It's Unused.
            **kwargs (dict): It's a Key/value pairs of attributes.
        """
        tfr = "%Y-%m-%dT%H:%M:%S.%f"
        self.id = str(uuid4())
        self.created_at = datetime.today()
        self.updated_at = datetime.today()
        if len(kwargs) != 0:
            for d, l in kwargs.items():
                if d == "created_at" or d == "updated_at":
                    self.__dict__[d] = datetime.strptime(l, tfr)
                else:
                    self.__dict__[d] = l
        else:
            models.storage.new(self)

    def save(self):
        """It's a Update updated_at with the current datetime."""
        self.updated_at = datetime.today()
        models.storage.save()

    def to_dict(self):
        """It's a Return the dictionary of the BaseModel instance.

        It's Includes the key/value pair __class__ representing
        the class name of the object.
        """
        rdc = self.__dict__.copy()
        rdc["created_at"] = self.created_at.isoformat()
        rdc["updated_at"] = self.updated_at.isoformat()
        rdc["__class__"] = self.__class__.__name__
        return rdc

    def __str__(self):
        """It's Return the print representation of the BaseModel instance."""
        chm = self.__class__.__name__
        return "[{}] ({}) {}".format(chm, self.id, self.__dict__)
