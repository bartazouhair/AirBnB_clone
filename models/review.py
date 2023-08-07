#!/usr/bin/python3
"""It's a Defines the Review class."""
from models.base_model import BaseModel


class Review(BaseModel):
    """It's a Represent a review.

    Attributes:
        place_id (str): It's The Place id.
        user_id (str): It's The User id.
        text (str): It's The text of the review.
    """

    place_id = ""
    user_id = ""
    text = ""
