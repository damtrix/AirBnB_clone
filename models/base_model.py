#!/usr/bin/python3
"""
Base models
"""
import uuid
from datetime import datetime
from models import storage


class BaseModel:
    """
    BaseModel that defines all common attributes/methods for other classes
    """
    def __init__(self, *args, **kwargs):
        """
        Initialising instance
        """
        if kwargs is not None and len(kwargs) != 0:
            for key in kwargs:
                if key == "created_at":
                    kwargs["created_at"] = datetime.fromisoformat(
                        kwargs["created_at"])
                elif key == "updated_at":
                    kwargs["updated_at"] = datetime.fromisoformat(
                        kwargs["updated_at"])
                else:
                    self.__dict__[key] = kwargs[key]

        else:
            self.id = str(uuid.uuid4())
            self.created_at = datetime.now()
            self.updated_at = datetime.now()
            storage.new(self)

    def __str__(self):
        """The string representation of the instance"""
        return "[{}] ({}) {}".format(
            type(self).__name__, self.id, self.__dict__
        )

    def save(self):
        """Updated the public instance attribute at updated_at"""

        self.updated_at = datetime.now()
        storage.save()

    def to_dict(self):
        """Returns all the dictionary attributes of an instance"""

        in_dict = dict(self.__dict__)
        in_dict.update({
            "__class__": type(self).__name__,
            "updated_at": self.updated_at.isoformat(),
            "id": self.id,
            "created_at": self.created_at.isoformat()
        })
        return in_dict
