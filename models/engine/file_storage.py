#!/usr/bin/python3

import json
import os
from typing import Dict

class FileStorage:
    __file_path = "file.json"
    __objects: Dict[str, any] = {}

    def all(self):
        return self.__objects

    def new(self, obj):
        self.__objects[f"{obj.__class__.__name__}.{obj.id}"] = obj

    def save(self):
        obj = self.__objects.copy()
        if obj == {}:
            return
        for k, v in obj.items():
            obj[k] = v.to_dict()
        with open(self.__file_path, "w") as fp:
            json.dump(obj, fp)

    def reload(self):
        if os.path.exists(self.__file_path):
            with open(self.__file_path, "r") as fp:
                # from models.base_model import BaseModel
                self.__objects: dict[str, any] = json.loads(fp.read())
                for k, v in self.__objects.items():
                    try:
                        from models.classes import classes
                        self.__objects[k] = classes[v['__class__']](**v)
                    except Exception as e:
                        print(e)