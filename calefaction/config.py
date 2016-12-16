# -*- coding: utf-8  -*-

import yaml

__all__ = ["Config"]

class Config:

    def __init__(self, confdir):
        self._filename = confdir / "config.yml"
        self._data = None
        self._load()

    def _load(self):
        with self._filename.open("rb") as fp:
            self._data = yaml.load(fp)

    def get(self, key="", default=None):
        obj = self._data
        for item in key.split("."):
            if item not in obj:
                return default
            obj = obj[item]
        return obj
