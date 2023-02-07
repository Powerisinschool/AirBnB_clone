#!/usr/bin/python3

from models.base_model import BaseModel

class State(BaseModel):
    def __init__(self, *args, **kwargs):
        self.name = ""
        super().__init__(*args, **kwargs)
