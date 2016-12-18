# -*- coding: utf-8  -*-

import sqlite3

from flask import g
from werkzeug.local import LocalProxy

__all__ = ["Database"]

class Database:
    path = None

    def __init__(self):
        if self.path is None:
            raise RuntimeError("Database.path not set")
        self._conn = sqlite3.connect(self.path)
        import traceback

    def __enter__(self):
        return self._conn.__enter__()

    def __exit__(self, exc_type, exc_value, trace):
        return self._conn.__exit__(exc_type, exc_value, trace)

    @classmethod
    def _get(cls):
        if not hasattr(g, "_db"):
            g._db = cls()
        return g._db

    @classmethod
    def pre_hook(cls):
        g.db = LocalProxy(cls._get)

    @classmethod
    def post_hook(cls, exc):
        if hasattr(g, "_db"):
            g._db.close()

    def close(self):
        return self._conn.close()
