#!/usr/bin/python3
"""Class Review inheriting from BaseModel"""
from models.base_model import BaseModel


class Review(BaseModel):
    """Class representing Review"""

    place_id = ""
    user_id = ""
    text = ""
