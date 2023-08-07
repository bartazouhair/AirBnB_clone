#!/usr/bin/python3
"""It's a Defines the Place class."""
from models.base_model import BaseModel


class Place(BaseModel):
    """It's a Represent a place.

    Attributes:
        city_id (str): It's a The City id.
        user_id (str): It's a The User id.
        name (str): It's The name of the place.
        description (str): It's a The description of the place.
        number_rooms (int): It's a The number of rooms of the place.
        number_bathrooms (int): It's a The number of bathrooms of the place.
        max_guest (int): It's a The maximum number of guests of the place.
        price_by_night (int): It's a The price by night of the place.
        latitude (float): It's The latitude of the place.
        longitude (float): It's The longitude of the place.
        amenity_ids (list): It'sa A list of Amenity ids.
    """

    city_id = ""
    user_id = ""
    name = ""
    description = ""
    number_rooms = 0
    number_bathrooms = 0
    max_guest = 0
    price_by_night = 0
    latitude = 0.0
    longitude = 0.0
    amenity_ids = []
