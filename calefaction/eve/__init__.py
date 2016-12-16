# -*- coding: utf-8  -*-

from .image import ImageServer

__all__ = ["EVE"]

class EVE:

    def __init__(self):
        self._image = ImageServer()

    @property
    def image(self):
        return self._image
