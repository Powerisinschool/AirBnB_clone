#!/usr/bin/python3

import importlib

from models.engine import file_storage

storage = file_storage.FileStorage()
storage.reload()
