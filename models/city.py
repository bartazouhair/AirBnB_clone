#!/usr/bin/python3
"""It's Defines the City class."""
from models.base_model import BaseModel


class City(BaseModel):
    """It's Represent a city.

    Attributes:
        state_id (str): It's The state id.
        name (str): It's The name of the city.
    """

    state_id = ""
    name = ""
