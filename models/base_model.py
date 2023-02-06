#!/usr/bin/python3

from datetime import datetime
import uuid


class BaseModel:
    def __init__(self):
        self.id = str(uuid.uuid4())
        self.created_at = datetime.now()
        self.__update()

    def __update(self):
        self.updated_at = datetime.now()

    def __str__(self):
        return f"[{self.__class__.__name__}] ({self.id}) {self.__dict__}"

    def save(self):
        self.__update()

    def to_dict(self):
        instance_dict = self.__dict__
        instance_dict["__class__"] = self.__class__.__name__
        for k, v in instance_dict.items():
            if isinstance(v, datetime):
                instance_dict[k] = v.strftime("%Y-%m-%dT%H:%M:%S.%f")
        return instance_dict