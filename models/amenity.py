#!/usr/bin/python3
"""It's Defines the Amenity class."""
from models.base_model import BaseModel


class Amenity(BaseModel):
    """It's Represent an amenity.

    Attributes:
        name (str): It's The name of the amenity.
    """

    name = ""
