# -*- coding: utf-8  -*-

__all__ = ["EVESwaggerInterface"]

class EVESwaggerInterface:
    """EVE API module for the EVE Swagger Interface (ESI)."""

    def __init__(self, session):
        self._session = session

    def __call__(self, *args):
        ...
        raise NotImplementedError()
