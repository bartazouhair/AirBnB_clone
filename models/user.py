#!/usr/bin/python3
"""It's a Defines the User class."""
from models.base_model import BaseModel


class User(BaseModel):
    """It's Represent a User.

    Attributes:
        email (str): It's The email of the user.
        password (str): It's The password of the user.
        first_name (str): It's The first name of the user.
        last_name (str): It's a The last name of the user.
    """

    email = ""
    password = ""
    first_name = ""
    last_name = ""
